"""
🌀 UCF State Loader
Loads real coordination metrics from state files
"""

import json
import logging
import os
import time
from datetime import UTC, datetime
from pathlib import Path

logger = logging.getLogger(__name__)

# Default state file locations
STATE_DIR = os.getenv("UCF_STATE_DIR", "/home/ubuntu/coordination-logs")
FALLBACK_STATE_DIR = Path(__file__).parent.parent / "coordination-logs"


def find_latest_state_file() -> Path | None:
    """Find the most recent UCF state file"""
    # Try environment variable path first
    state_dir = Path(STATE_DIR)
    if not state_dir.exists():
        # Try fallback path
        state_dir = FALLBACK_STATE_DIR
        if not state_dir.exists():
            logger.warning("UCF state directory not found: %s", STATE_DIR)
            return None

    # Find all .json state files
    state_files = list(state_dir.glob("ucf_state_*.json"))

    if not state_files:
        logger.warning("No UCF state files found in %s", state_dir)
        return None

    # Return most recent file
    latest = max(state_files, key=lambda p: p.stat().st_mtime)
    logger.info("Loading UCF state from: %s", latest)
    return latest


def load_ucf_state() -> dict:
    """Load current UCF state from file"""
    state_file = find_latest_state_file()

    if not state_file:
        # Return default state if no state file found
        logger.warning("Using default UCF state (no state file found)")
        return get_default_state()

    try:
        with open(state_file, encoding="utf-8") as f:
            state = json.load(f)

        # Validate required fields
        required_fields = ["coherence", "entropy", "performance_score"]
        if not all(field in state for field in required_fields):
            logger.warning("State file missing required fields, using defaults")
            return get_default_state()

        # Add timestamp if missing
        if "last_update" not in state:
            state["last_update"] = datetime.fromtimestamp(state_file.stat().st_mtime).isoformat()

        logger.info("Loaded UCF state: coherence=%.2f", state.get("coherence"))
        return state

    except json.JSONDecodeError as e:
        logger.error("Failed to parse UCF state file: %s", e)
        return get_default_state()
    except Exception as e:
        logger.error("Error loading UCF state: %s", e)
        return get_default_state()


def get_default_state() -> dict:
    """Return UCF state from DB snapshot, or hardcoded defaults when unavailable"""
    # Try loading the most recent CoordinationSnapshot from the database
    try:
        # from helix_core.db_models import CoordinationSnapshot, SessionLocal

        db = SessionLocal()
        try:
            from sqlalchemy import desc

            row = db.query(CoordinationSnapshot).order_by(desc(CoordinationSnapshot.timestamp)).first()
            if row:
                logger.info("Loaded UCF default from DB snapshot id=%s", row.id)
                return {
                    "coherence": (row.harmony or 0.5) * 100,
                    "entropy": row.friction or 0.234,
                    "performance_score": int((row.performance_score or 0.5) * 28),
                    "active_agents": 0,
                    "cycles_completed": 0,
                    "harmony": row.harmony,
                    "resilience": row.resilience,
                    "throughput": row.throughput,
                    "focus": row.focus,
                    "friction": row.friction,
                    "velocity": row.velocity,
                    "last_update": (row.timestamp.isoformat() if row.timestamp else datetime.now(UTC).isoformat()),
                    "_source": "database",
                }
        finally:
            db.close()
    except Exception as db_err:
        logger.debug("DB fallback unavailable for UCF state: %s", db_err)

    # Ultimate fallback: zeroed defaults
    return {
        "coherence": 0.0,
        "entropy": 0.0,
        "performance_score": 0,
        "active_agents": 0,
        "cycles_completed": 0,
        "last_update": None,
        "_default": True,  # Flag to indicate this is default data
    }


# Cache for UCF metrics
_ucf_cache = None
_cache_timestamp = 0
_CACHE_TTL = 5  # seconds


def get_ucf_metrics() -> dict:
    """Get current UCF metrics (cached for performance)"""
    global _ucf_cache, _cache_timestamp

    current_time = time.time()
    if _ucf_cache is None or (current_time - _cache_timestamp) > _CACHE_TTL:
        _ucf_cache = load_ucf_state()
        _cache_timestamp = current_time

    return _ucf_cache


def watch_state_file(callback):
    """Watch state file for changes and call callback

    Args:
        callback: Function to call when state changes
    """
    import asyncio
    from pathlib import Path

    from watchdog.events import FileSystemEventHandler
    from watchdog.observers import Observer

    class StateFileHandler(FileSystemEventHandler):
        def __init__(self, callback):
            self.callback = callback
            self.last_state = None

        def on_modified(self, event):
            if event.src_path.endswith("ucf_state.json"):
                try:
                    current_state = load_ucf_state()
                    if current_state != self.last_state:
                        # Run callback in event loop
                        asyncio.create_task(self.callback(current_state))
                        self.last_state = current_state
                except Exception as e:
                    logger.warning("Error processing state file change: %s", e)

    # Get the state file path
    state_file = Path(__file__).parent / "config" / "ucf_state.json"

    # Create observer and handler
    event_handler = StateFileHandler(callback)
    observer = Observer()
    observer.schedule(event_handler, path=str(state_file.parent), recursive=False)

    # Start watching
    observer.start()

    async def watch_loop():
        """Keep the observer running"""
        try:
            while True:
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            observer.stop()
            observer.join()

    return watch_loop


# Example state file format:
"""
{
  "coherence": 87.3,
  "entropy": 0.234,
  "performance_score": 14,
  "active_agents": 17,
  "cycles_completed": 42,
  "harmony_score": 0.4922,
  "phase": "COHERENT",
  "last_update": "2025-12-19T10:30:00Z",
  "agent_states": {
    "nexus": {"status": "active", "load": 0.7},
    "oracle": {"status": "active", "load": 0.5}
  }
}
"""
