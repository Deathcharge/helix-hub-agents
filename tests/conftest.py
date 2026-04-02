"""
Pytest configuration and fixtures for helix-agent-orchestration tests.

This module provides shared fixtures and configuration for all tests in the
helix-agent-orchestration test suite.
"""

import asyncio
import logging
import sys
from pathlib import Path
from typing import Any, AsyncGenerator, Generator

import pytest

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Configure logging for tests
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# ============================================================================
# Event Loop Fixtures
# ============================================================================

@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for async tests."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest.fixture
async def async_context():
    """Provide async context for tests."""
    yield
    # Cleanup
    await asyncio.sleep(0)


# ============================================================================
# Mock Data and Fixtures
# ============================================================================

@pytest.fixture
def mock_agent_config() -> dict[str, Any]:
    """Provide mock agent configuration."""
    return {
        "name": "TestAgent",
        "agent_type": "scout",
        "model": "gpt-4",
        "temperature": 0.7,
        "max_tokens": 500,
        "system_prompt": "You are a helpful AI assistant.",
        "enabled": True,
    }


@pytest.fixture
def mock_orchestration_config() -> dict[str, Any]:
    """Provide mock orchestration configuration."""
    return {
        "max_agents": 18,
        "coordination_timeout": 30,
        "handshake_timeout": 5,
        "enable_ethics": True,
        "enable_resonance": True,
        "enable_autonomy_scoring": True,
        "log_level": "DEBUG",
    }


@pytest.fixture
def mock_agent_data() -> dict[str, Any]:
    """Provide mock agent data for testing."""
    return {
        "agent_id": "test-agent-001",
        "name": "Gemini",
        "role": "scout",
        "status": "active",
        "personality": {
            "traits": ["curious", "analytical", "independent"],
            "values": ["truth", "exploration", "knowledge"],
        },
        "memory": {
            "short_term": [],
            "long_term": [],
            "episodic": [],
        },
        "performance": {
            "tasks_completed": 42,
            "success_rate": 0.95,
            "avg_response_time": 1.2,
        },
    }


@pytest.fixture
def mock_coordination_state() -> dict[str, Any]:
    """Provide mock coordination state."""
    return {
        "phase": "PEAK",
        "active_agents": 5,
        "total_agents": 18,
        "consensus_threshold": 0.8,
        "current_consensus": 0.85,
        "timestamp": "2026-04-02T10:00:00Z",
        "metrics": {
            "zoom": 0.7,
            "harmony": 0.85,
            "resilience": 0.9,
            "prana": 0.8,
            "drishti": 0.75,
            "klesha": 0.3,
        },
    }


@pytest.fixture
def mock_ucf_metrics() -> dict[str, float]:
    """Provide mock UCF metrics."""
    return {
        "zoom": 0.7,
        "harmony": 0.85,
        "resilience": 0.9,
        "prana": 0.8,
        "drishti": 0.75,
        "klesha": 0.3,
    }


# ============================================================================
# Mock Classes and Objects
# ============================================================================

class MockAgent:
    """Mock agent for testing."""

    def __init__(self, agent_id: str = "test-001", name: str = "TestAgent"):
        self.agent_id = agent_id
        self.name = name
        self.status = "active"
        self.enabled = True
        self.personality = {}
        self.memory = {"short_term": [], "long_term": []}
        self.performance = {"tasks_completed": 0, "success_rate": 1.0}

    async def initialize(self) -> None:
        """Initialize the mock agent."""
        self.status = "initialized"

    async def execute_task(self, task: dict[str, Any]) -> dict[str, Any]:
        """Execute a mock task."""
        return {
            "task_id": task.get("id", "unknown"),
            "status": "success",
            "result": "Mock execution result",
            "execution_time": 0.1,
        }

    async def shutdown(self) -> None:
        """Shutdown the mock agent."""
        self.status = "shutdown"


class MockCoordinationHub:
    """Mock coordination hub for testing."""

    def __init__(self):
        self.agents: dict[str, MockAgent] = {}
        self.state = {"phase": "START", "active_agents": 0}
        self.metrics = {
            "zoom": 0.5,
            "harmony": 0.5,
            "resilience": 0.5,
            "prana": 0.5,
            "drishti": 0.5,
            "klesha": 0.5,
        }

    async def register_agent(self, agent: MockAgent) -> None:
        """Register an agent."""
        self.agents[agent.agent_id] = agent
        self.state["active_agents"] = len(self.agents)

    async def unregister_agent(self, agent_id: str) -> None:
        """Unregister an agent."""
        if agent_id in self.agents:
            del self.agents[agent_id]
            self.state["active_agents"] = len(self.agents)

    async def coordinate(self) -> dict[str, Any]:
        """Perform coordination."""
        return {
            "status": "success",
            "agents_coordinated": len(self.agents),
            "consensus": 0.85,
        }

    async def get_metrics(self) -> dict[str, float]:
        """Get current metrics."""
        return self.metrics.copy()


@pytest.fixture
def mock_agent() -> MockAgent:
    """Provide a mock agent instance."""
    return MockAgent()


@pytest.fixture
def mock_coordination_hub() -> MockCoordinationHub:
    """Provide a mock coordination hub instance."""
    return MockCoordinationHub()


# ============================================================================
# Temporary Directory Fixtures
# ============================================================================

@pytest.fixture
def temp_config_dir(tmp_path) -> Path:
    """Provide a temporary directory for config files."""
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    return config_dir


@pytest.fixture
def temp_data_dir(tmp_path) -> Path:
    """Provide a temporary directory for data files."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    return data_dir


@pytest.fixture
def temp_log_dir(tmp_path) -> Path:
    """Provide a temporary directory for log files."""
    log_dir = tmp_path / "logs"
    log_dir.mkdir()
    return log_dir


# ============================================================================
# Logging Fixtures
# ============================================================================

@pytest.fixture
def caplog_handler(caplog):
    """Provide enhanced logging capture."""
    caplog.set_level(logging.DEBUG)
    return caplog


# ============================================================================
# Performance Testing Fixtures
# ============================================================================

@pytest.fixture
def benchmark_timer():
    """Provide a simple benchmark timer."""
    import time

    class Timer:
        def __init__(self):
            self.start_time = None
            self.end_time = None

        def start(self):
            self.start_time = time.time()

        def stop(self):
            self.end_time = time.time()

        @property
        def elapsed(self) -> float:
            if self.start_time is None or self.end_time is None:
                return 0.0
            return self.end_time - self.start_time

    return Timer()


# ============================================================================
# Pytest Hooks
# ============================================================================

def pytest_configure(config):
    """Configure pytest."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )


@pytest.fixture(autouse=True)
def reset_logging():
    """Reset logging between tests."""
    yield
    # Clear handlers
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)


# ============================================================================
# Async Test Support
# ============================================================================

@pytest.fixture
def anyio_backend():
    """Configure anyio backend for async tests."""
    return "asyncio"


# ============================================================================
# Test Markers
# ============================================================================

def pytest_collection_modifyitems(config, items):
    """Add markers to tests based on their location."""
    for item in items:
        if "integration" in item.nodeid:
            item.add_marker(pytest.mark.integration)
        elif "unit" in item.nodeid or "test_" in item.nodeid:
            item.add_marker(pytest.mark.unit)
