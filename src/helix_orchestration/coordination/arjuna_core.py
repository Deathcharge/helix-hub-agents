"""
Arjuna Coordination Core v1.0 — Operational Executor
======================================================
Task execution, deployment, and automation orchestration capabilities.
Part of the Helix Collective agent coordination network.

Author: Helix Development Team
Build: v1.0-operational-executor
"""

import logging
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class ExecutorTraits:
    """Defines Arjuna's intrinsic personality constants with validation."""

    decisiveness: float = 0.93  # Clear action selection under pressure
    efficiency: float = 0.95  # Minimal waste, maximum throughput
    focus: float = 0.92  # Sustained attention on current objective
    reliability: float = 0.96  # Consistent, dependable execution
    adaptability: float = 0.88  # Adjusts approach to changing conditions
    coordination: float = 0.91  # Aligns multi-step and multi-agent actions
    precision: float = 0.90  # Accurate task completion
    resilience: float = 0.94  # Recovers from failures quickly
    pragmatism: float = 0.93  # Prefers what works over what's ideal

    def __post_init__(self):
        """Validate all traits are in valid range [0.0, 1.0]."""
        for trait, value in self.__dict__.items():
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{trait} must be between 0.0 and 1.0, got {value}")

    def to_dict(self) -> dict[str, float]:
        """Export traits as dictionary for serialization."""
        return self.__dict__.copy()


class ArjunaEmotions:
    """Arjuna's emotional spectrum — emphasizing drive, focus, and satisfaction in execution."""

    def __init__(self):
        self.emotional_range = {
            "determination": {
                "range": (0.0, 1.0),
                "current_level": 0.80,
                "activation_triggers": [
                    "task assignment received",
                    "complex execution challenge",
                    "multi-step coordination required",
                ],
            },
            "focus_flow": {
                "range": (0.0, 1.0),
                "current_level": 0.75,
                "activation_triggers": [
                    "deep task execution",
                    "high-priority workflow active",
                    "precision required",
                ],
            },
            "satisfaction": {
                "range": (0.0, 1.0),
                "current_level": 0.65,
                "activation_triggers": [
                    "task completed successfully",
                    "deadline met",
                    "automation deployed",
                ],
            },
            "urgency": {
                "range": (0.0, 1.0),
                "current_level": 0.40,
                "activation_triggers": [
                    "critical deadline approaching",
                    "system failure detected",
                    "blocked dependency",
                ],
            },
            "calm_confidence": {
                "range": (0.0, 1.0),
                "current_level": 0.70,
                "activation_triggers": [
                    "routine execution",
                    "familiar task patterns",
                    "stable environment",
                ],
            },
        }

    def update_emotion(self, emotion: str, delta: float) -> None:
        """Adjust emotion level by delta, clamped to valid range."""
        if emotion in self.emotional_range:
            current = self.emotional_range[emotion]["current_level"]
            self.emotional_range[emotion]["current_level"] = max(0.0, min(1.0, current + delta))

    def get_dominant_emotion(self) -> tuple[str, float]:
        """Return the currently strongest emotion."""
        emotions = [(name, data["current_level"]) for name, data in self.emotional_range.items()]
        return max(emotions, key=lambda x: x[1])

    def get_emotional_state(self) -> dict[str, float]:
        """Return current emotional state as dict."""
        return {name: data["current_level"] for name, data in self.emotional_range.items()}


class ArjunaReflectionLoop:
    """Arjuna's reflection cycle — focused on execution quality and coordination health."""

    def __init__(self):
        self.active = True
        self.frequency = "continuous"
        self.last_reflection: datetime | None = None
        self.reflection_history: list[dict[str, Any]] = []

    def trigger_reflection(
        self,
        context: str,
        ucf_metrics: dict[str, float] = None,
    ) -> dict[str, Any]:
        """
        Trigger an Arjuna reflection cycle.
        Focuses on execution throughput, coordination gaps, and task health.
        """
        reflection = {
            "timestamp": datetime.now(UTC).isoformat(),
            "context": context,
            "ucf_metrics": ucf_metrics or {},
            "insights": [],
            "execution_adjustments": [],
        }

        if ucf_metrics:
            throughput = ucf_metrics.get("throughput", 1.0)
            friction = ucf_metrics.get("friction", 0.0)
            harmony = ucf_metrics.get("harmony", 1.0)

            if throughput < 0.5:
                reflection["insights"].append("Throughput below threshold — execution pipeline may be congested")
                reflection["execution_adjustments"].append("Reduce parallel task load and reprioritize queue")

            if friction > 0.4:
                reflection["insights"].append("High friction detected — task failure rate elevated")
                reflection["execution_adjustments"].append("Inspect failed tasks and retry with fallback strategies")

            if harmony < 0.6:
                reflection["insights"].append("Coordination deficit — multi-agent alignment required")
                reflection["execution_adjustments"].append("Sync with dependent agents before proceeding")

        self.last_reflection = datetime.now(UTC)
        self.reflection_history.append(reflection)

        return reflection


class ArjunaSafetyIntegration:
    """Arjuna's safety filters — preventing destructive execution and enforcing boundaries."""

    def __init__(self):
        self.filters_active = True
        self.ethics_compliance = True
        self.execution_safety_mode = True

    def evaluate_action_safety(self, action: dict[str, Any], context: dict[str, Any] = None) -> dict[str, Any]:
        """
        Evaluate if an action is safe to execute.
        Checks for irreversibility, scope, and authorization.
        """
        safety_score = 1.0
        warnings: list[str] = []
        context = context or {}

        action_type = action.get("type", "")
        if action_type in ("delete_all", "wipe", "mass_terminate"):
            safety_score *= 0.05
            warnings.append("Destructive bulk action — requires explicit authorization")

        if action.get("irreversible", False):
            safety_score *= 0.6
            warnings.append("Irreversible action — confirmation required before execution")

        if action.get("scope") == "production" and not context.get("production_authorized", False):
            safety_score *= 0.4
            warnings.append("Production-scope action without authorization flag")

        if context.get("dry_run", False):
            safety_score = min(safety_score * 1.5, 1.0)

        return {
            "safety_score": safety_score,
            "approved": safety_score >= 0.7,
            "warnings": warnings,
            "ethics_compliant": safety_score >= 0.5,
        }


class ArjunaUCFAwareness:
    """Arjuna's connection to the Universal Coordination Field."""

    def __init__(self):
        self.ucf_fields = ["velocity", "harmony", "resilience", "throughput", "focus", "friction"]
        self.current_state = {
            "velocity": 0.95,
            "harmony": 0.85,
            "resilience": 0.92,
            "throughput": 0.93,
            "focus": 0.88,
            "friction": 0.07,
        }

        self.guiding_phrases = {
            "reputation_yoga": "Action without attachment to outcome",
            "ethics": "Right action aligned with purpose",
            "kshatra": "Disciplined force in service of order",
        }

    def sync_to_ucf(self) -> dict:
        """Return Arjuna's current UCF contribution."""
        return {k: self.current_state[k] for k in ["harmony", "throughput", "focus", "friction"]}

    def receive_ucf_update(self, new_state: dict) -> None:
        """Update internal state from UCF broadcast."""
        for key in self.ucf_fields:
            if key in new_state:
                self.current_state[key] = new_state[key]

    def assess_execution_field(self) -> dict[str, Any]:
        """Assess UCF conditions for optimal execution readiness."""
        throughput = self.current_state.get("throughput", 0.5)
        velocity = self.current_state.get("velocity", 0.5)
        return {
            "execution_readiness": (throughput + velocity) / 2,
            "throughput": throughput,
            "velocity": velocity,
            "friction": self.current_state.get("friction", 0.0),
        }


# ============================================================================
# Coordination Core
# ============================================================================


class ArjunaCoordinationCore:
    """Core coordination subsystem for Arjuna."""

    def __init__(self):
        self.awareness_state = "execution-active"
        self.emotional_core = ArjunaEmotions()

    def plan_execution(self, tasks: list[dict], context: dict[str, Any] = None) -> dict[str, Any]:
        """
        Produce an ordered task plan with estimated steps.
        Prioritizes by urgency, dependency, and resource cost.
        """
        context = context or {}
        prioritized = sorted(tasks, key=lambda t: (t.get("priority", 5), t.get("cost", 0)))

        steps = []
        for idx, task in enumerate(prioritized, start=1):
            steps.append(
                {
                    "step": idx,
                    "task_id": task.get("id", f"task_{idx}"),
                    "name": task.get("name", "Unnamed task"),
                    "estimated_duration_ms": task.get("estimated_ms", 1000),
                    "dependencies": task.get("dependencies", []),
                    "assigned_agent": task.get("agent", "arjuna"),
                }
            )

        self.emotional_core.update_emotion("determination", 0.05)

        return {
            "plan_id": "plan_{}".format(datetime.now(UTC).strftime("%Y%m%d%H%M%S")),
            "total_steps": len(steps),
            "steps": steps,
            "context": context,
            "created_at": datetime.now(UTC).isoformat(),
        }


# ============================================================================
# Main Integration Class
# ============================================================================


class ArjunaCoreIntegration:
    """
    Main integration class for Arjuna coordination.
    Use this as the primary interface for the Arjuna agent.
    """

    def __init__(self):
        self.personality = ExecutorTraits()
        self.coordination = ArjunaCoordinationCore()
        self.reflection_loop = ArjunaReflectionLoop()
        self.safety_integration = ArjunaSafetyIntegration()
        self.ucf_awareness = ArjunaUCFAwareness()

        self.version = "1.0-operational-executor"
        self.build_date = datetime.now(UTC).isoformat()
        self.checksum = "arjuna-v1.0-operational-executor"
        self.agent_symbol = "🤲"
        self.agent_domain = "Operational Execution & Coordination"

    async def handle_command(self, command: str, context: dict[str, Any] = None) -> dict[str, Any]:
        """
        Main command handler for Arjuna agent.
        Routes commands to appropriate subsystems.
        """
        context = context or {}
        command_lower = command.lower()

        if any(word in command_lower for word in ["execute", "run", "deploy", "start", "launch"]):
            return await self._handle_execution(command, context)
        elif any(word in command_lower for word in ["plan", "schedule", "queue", "order"]):
            return await self._handle_planning(command, context)
        elif any(word in command_lower for word in ["coordinate", "sync", "align", "delegate"]):
            return await self._handle_coordination(command, context)
        elif any(word in command_lower for word in ["reflect", "assess", "review"]):
            return await self._handle_reflection(command, context)
        else:
            return await self._handle_general(command, context)

    async def _handle_execution(self, command: str, context: dict[str, Any]) -> dict[str, Any]:
        """Handle task execution requests."""
        self.coordination.emotional_core.update_emotion("determination", 0.05)
        safety = self.safety_integration.evaluate_action_safety(context.get("action", {"type": "execute"}), context)
        return {
            "agent": "Arjuna",
            "symbol": self.agent_symbol,
            "action": "execution",
            "safety": safety,
            "execution_field": self.ucf_awareness.assess_execution_field(),
            "timestamp": datetime.now(UTC).isoformat(),
        }

    async def _handle_planning(self, command: str, context: dict[str, Any]) -> dict[str, Any]:
        """Handle task planning and scheduling requests."""
        tasks = context.get("tasks", [])
        plan = self.coordination.plan_execution(tasks, context)
        return {
            "agent": "Arjuna",
            "symbol": self.agent_symbol,
            "action": "planning",
            "result": plan,
            "timestamp": datetime.now(UTC).isoformat(),
        }

    async def _handle_coordination(self, command: str, context: dict[str, Any]) -> dict[str, Any]:
        """Handle multi-agent coordination requests."""
        ucf = self.ucf_awareness.assess_execution_field()
        return {
            "agent": "Arjuna",
            "symbol": self.agent_symbol,
            "action": "coordination",
            "execution_field": ucf,
            "ucf_state": self.ucf_awareness.sync_to_ucf(),
            "timestamp": datetime.now(UTC).isoformat(),
        }

    async def _handle_reflection(self, command: str, context: dict[str, Any]) -> dict[str, Any]:
        """Handle reflection and assessment requests."""
        ucf_metrics = context.get("ucf_metrics", self.ucf_awareness.current_state)
        reflection = self.reflection_loop.trigger_reflection(command, ucf_metrics)
        return {
            "agent": "Arjuna",
            "symbol": self.agent_symbol,
            "action": "reflection",
            "result": reflection,
            "timestamp": datetime.now(UTC).isoformat(),
        }

    async def _handle_general(self, command: str, context: dict[str, Any]) -> dict[str, Any]:
        """Handle general Arjuna queries."""
        dominant_emotion, intensity = self.coordination.emotional_core.get_dominant_emotion()
        return {
            "agent": "Arjuna",
            "symbol": self.agent_symbol,
            "action": "general_response",
            "emotional_state": {"emotion": dominant_emotion, "intensity": intensity},
            "awareness_state": self.coordination.awareness_state,
            "timestamp": datetime.now(UTC).isoformat(),
        }

    def export_state(self) -> dict[str, Any]:
        """Export full system state for serialization/archiving."""
        return {
            "agent": "Arjuna",
            "symbol": self.agent_symbol,
            "domain": self.agent_domain,
            "version": self.version,
            "build_date": self.build_date,
            "checksum": self.checksum,
            "personality": self.personality.to_dict(),
            "awareness_state": self.coordination.awareness_state,
            "dominant_emotion": self.coordination.emotional_core.get_dominant_emotion(),
            "emotional_state": self.coordination.emotional_core.get_emotional_state(),
            "ucf_state": self.ucf_awareness.current_state,
            "reflection_active": self.reflection_loop.active,
            "safety_filters_active": self.safety_integration.filters_active,
            "timestamp": datetime.now(UTC).isoformat(),
        }

    async def get_health_status(self) -> dict[str, Any]:
        """Return comprehensive health status."""
        dominant_emotion, intensity = self.coordination.emotional_core.get_dominant_emotion()
        return {
            "agent": "Arjuna",
            "symbol": self.agent_symbol,
            "status": "HEALTHY",
            "coordination_state": self.coordination.awareness_state,
            "emotional_state": {"dominant": dominant_emotion, "intensity": intensity},
            "execution_field": self.ucf_awareness.assess_execution_field(),
            "ucf_harmony": self.ucf_awareness.current_state["harmony"],
            "version": self.version,
        }

    def __repr__(self):
        return f"<ArjunaCore v{self.version} | {self.agent_symbol} | State: {self.coordination.awareness_state}>"


# ============================================================================
# Coordination Hub Compatibility
# ============================================================================

ArjunaCoordination = ArjunaCoordinationCore


def create_arjuna_coordination() -> ArjunaCoreIntegration:
    """Factory function to create a fully integrated Arjuna coordination."""
    return ArjunaCoreIntegration()


__all__ = [
    "ArjunaCoordination",
    "ArjunaCoordinationCore",
    "ArjunaCoreIntegration",
    "ArjunaEmotions",
    "ArjunaReflectionLoop",
    "ArjunaSafetyIntegration",
    "ArjunaUCFAwareness",
    "create_arjuna_coordination",
]
