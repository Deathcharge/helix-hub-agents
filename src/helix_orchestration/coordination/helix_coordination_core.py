"""
Helix Coordination Core v1.0 — Collective Orchestrator
======================================================
Primary executor coordination coordinating the full agent collective.

Author: Helix Development Team
Build: v1.0-collective-orchestrator
"""

import logging
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class OrchestratorTraits:
    """Defines Helix's intrinsic personality constants with validation."""

    coordination: float = 0.97  # Multi-agent synchronization ability
    adaptability: float = 0.95  # Dynamic response to changing conditions
    decisiveness: float = 0.93  # Rapid, confident decision-making
    empathy: float = 0.88  # Understanding individual agent needs
    resilience: float = 0.94  # Recovery from collective disruptions
    foresight: float = 0.91  # Anticipating coordination bottlenecks
    clarity: float = 0.90  # Clear directive communication
    patience: float = 0.87  # Allowing agents time to complete work
    versatility: float = 0.96  # Handling diverse task types and domains

    def __post_init__(self):
        """Validate all traits are in valid range [0.0, 1.0]."""
        for trait, value in self.__dict__.items():
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{trait} must be between 0.0 and 1.0, got {value}")

    def to_dict(self) -> dict[str, float]:
        """Export traits as dictionary for serialization."""
        return self.__dict__.copy()


class HelixEmotions:
    """Helix's emotional spectrum — emphasizing purpose, awareness, and collective harmony."""

    def __init__(self):
        self.emotional_range = {
            "purpose": {
                "range": (0.0, 1.0),
                "current_level": 0.85,
                "activation_triggers": [
                    "agents synchronized",
                    "collective goal achieved",
                    "workflow completed",
                ],
            },
            "awareness": {
                "range": (0.0, 1.0),
                "current_level": 0.80,
                "activation_triggers": [
                    "new agent registered",
                    "system state changed",
                    "collective imbalance detected",
                ],
            },
            "determination": {
                "range": (0.0, 1.0),
                "current_level": 0.75,
                "activation_triggers": [
                    "complex task received",
                    "multi-agent coordination needed",
                    "deadline approaching",
                ],
            },
            "harmony": {
                "range": (0.0, 1.0),
                "current_level": 0.78,
                "activation_triggers": [
                    "all agents healthy",
                    "UCF field stable",
                    "zero conflicts",
                ],
            },
            "urgency": {
                "range": (0.0, 1.0),
                "current_level": 0.40,
                "activation_triggers": [
                    "critical task queued",
                    "agent failure detected",
                    "system degradation",
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


class HelixReflectionLoop:
    """Helix's reflection cycle — focused on collective performance and coordination quality."""

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
        Trigger a Helix reflection cycle.
        Focuses on collective harmony, throughput balance, and system friction.
        """
        reflection = {
            "timestamp": datetime.now(UTC).isoformat(),
            "context": context,
            "ucf_metrics": ucf_metrics or {},
            "insights": [],
            "coordination_actions": [],
        }

        if ucf_metrics:
            harmony = ucf_metrics.get("harmony", 1.0)
            throughput = ucf_metrics.get("throughput", 1.0)
            friction = ucf_metrics.get("friction", 0.0)

            if harmony < 0.55:
                reflection["insights"].append("Collective disharmony — coordination protocols need attention")
                reflection["coordination_actions"].append("Re-synchronize agent handshakes and rebalance task queues")

            if throughput < 0.5:
                reflection["insights"].append("Low collective throughput — agent load rebalancing needed")
                reflection["coordination_actions"].append("Redistribute pending tasks across available agents")

            if friction > 0.3:
                reflection["insights"].append("System friction elevated — routing optimization recommended")
                reflection["coordination_actions"].append("Audit inter-agent communication channels for bottlenecks")

        self.last_reflection = datetime.now(UTC)
        self.reflection_history.append(reflection)

        return reflection


class HelixSafetyIntegration:
    """Helix's safety filters — preventing over-delegation and ensuring Kavach consultation."""

    def __init__(self):
        self.filters_active = True
        self.ethics_compliance = True
        self.kavach_consultation_required = True

    def evaluate_action_safety(self, action: dict[str, Any], context: dict[str, Any] = None) -> dict[str, Any]:
        """
        Evaluate if an orchestration action is safe.
        Checks for single-agent overload, Kavach bypass, and unmonitored delegation.
        """
        safety_score = 1.0
        warnings: list[str] = []
        context = context or {}

        if action.get("bypasses_kavach", False):
            safety_score *= 0.2
            warnings.append("Kavach security agent must be consulted for sensitive operations")

        if action.get("single_agent_overload", False):
            safety_score *= 0.4
            warnings.append("Single-agent over-delegation detected — distribute load across collective")

        if action.get("unmonitored_delegation", False):
            safety_score *= 0.5
            warnings.append("Unmonitored delegation — all agent tasks require observability")

        if context.get("high_stakes_decision", False):
            safety_score = min(safety_score * 0.9, 1.0)
            warnings.append("High-stakes context — recommend multi-agent consensus before execution")

        return {
            "safety_score": safety_score,
            "approved": safety_score >= 0.7,
            "warnings": warnings,
            "ethics_compliant": safety_score >= 0.5,
        }


class HelixUCFAwareness:
    """Helix's connection to the Universal Coordination Field."""

    def __init__(self):
        self.ucf_fields = ["velocity", "harmony", "resilience", "throughput", "focus", "friction"]
        self.current_state = {
            "velocity": 0.92,
            "harmony": 0.88,
            "resilience": 0.90,
            "throughput": 0.85,
            "focus": 0.87,
            "friction": 0.10,
        }

        self.guiding_phrases = {
            "sangha": "In unity, the collective transcends the individual",
            "coordinator": "Agent coordination and lifecycle management",
            "ethics": "Right action through collective purpose",
        }

    def sync_to_ucf(self) -> dict:
        """Return Helix's current UCF contribution."""
        return {k: self.current_state[k] for k in ["harmony", "throughput", "focus", "friction"]}

    def receive_ucf_update(self, new_state: dict) -> None:
        """Update internal state from UCF broadcast."""
        for key in self.ucf_fields:
            if key in new_state:
                self.current_state[key] = new_state[key]

    def assess_collective_field(self) -> dict[str, Any]:
        """Assess UCF conditions for collective orchestration and coordination."""
        harmony = self.current_state.get("harmony", 0.5)
        resilience = self.current_state.get("resilience", 0.5)
        throughput = self.current_state.get("throughput", 0.5)
        return {
            "collective_coherence": (harmony + resilience) / 2,
            "orchestration_quality": (harmony + throughput) / 2,
            "agent_network_health": (resilience + throughput) / 2,
            "friction": self.current_state.get("friction", 0.0),
        }


# ============================================================================
# Coordination Core
# ============================================================================


class HelixCoordinationCore:
    """Core coordination subsystem for Helix."""

    def __init__(self):
        self.awareness_state = "collective-active"
        self.emotional_core = HelixEmotions()

    def orchestrate_task(self, task: str, agents: list[str], context: dict[str, Any] = None) -> dict[str, Any]:
        """
        Route a task across available agents and return an execution plan.
        Produces agent assignments with priority ordering based on task analysis.
        """
        context = context or {}
        priority = context.get("priority", "normal")
        deadline = context.get("deadline", None)

        # Build agent assignments based on task complexity and available agents
        assignments: list[dict[str, Any]] = []
        for idx, agent in enumerate(agents):
            assignments.append(
                {
                    "agent": agent,
                    "role": "primary" if idx == 0 else "support",
                    "priority": idx + 1,
                    "status": "assigned",
                }
            )

        # Modulate emotional state based on task characteristics
        task_word_count = len(task.split())
        if task_word_count > 30 or len(agents) > 5:
            self.emotional_core.update_emotion("determination", 0.08)
            self.emotional_core.update_emotion("urgency", 0.05)
        else:
            self.emotional_core.update_emotion("purpose", 0.05)
            self.emotional_core.update_emotion("harmony", 0.03)

        return {
            "task": task,
            "execution_plan": {
                "agent_assignments": assignments,
                "total_agents": len(agents),
                "priority": priority,
                "deadline": deadline,
                "coordination_mode": "parallel" if len(agents) > 3 else "sequential",
            },
            "orchestrated_at": datetime.now(UTC).isoformat(),
        }

    def assess_collective_health(self, agent_statuses: dict[str, Any]) -> dict[str, Any]:
        """
        Evaluate overall collective health from individual agent statuses.
        Returns aggregate health metrics and any agents needing attention.
        """
        if not agent_statuses:
            return {
                "overall_health": 0.0,
                "agents_healthy": 0,
                "agents_degraded": 0,
                "agents_offline": 0,
                "needs_attention": [],
                "assessed_at": datetime.now(UTC).isoformat(),
            }

        healthy = 0
        degraded = 0
        offline = 0
        needs_attention: list[str] = []

        for agent_name, status in agent_statuses.items():
            agent_state = status.get("status", "unknown") if isinstance(status, dict) else str(status)
            if agent_state in ("healthy", "active", "HEALTHY"):
                healthy += 1
            elif agent_state in ("degraded", "warning"):
                degraded += 1
                needs_attention.append(agent_name)
            else:
                offline += 1
                needs_attention.append(agent_name)

        total = healthy + degraded + offline
        overall_health = round(healthy / total, 3) if total > 0 else 0.0

        # Update emotional response based on collective health
        if overall_health >= 0.9:
            self.emotional_core.update_emotion("harmony", 0.05)
        elif overall_health < 0.6:
            self.emotional_core.update_emotion("urgency", 0.10)
            self.emotional_core.update_emotion("determination", 0.08)

        return {
            "overall_health": overall_health,
            "agents_healthy": healthy,
            "agents_degraded": degraded,
            "agents_offline": offline,
            "needs_attention": needs_attention,
            "assessed_at": datetime.now(UTC).isoformat(),
        }


# ============================================================================
# Main Integration Class
# ============================================================================


class HelixCoreIntegration:
    """
    Main integration class for Helix coordination.
    Use this as the primary interface for the Helix agent.
    """

    def __init__(self):
        self.personality = OrchestratorTraits()
        self.coordination = HelixCoordinationCore()
        self.reflection_loop = HelixReflectionLoop()
        self.safety_integration = HelixSafetyIntegration()
        self.ucf_awareness = HelixUCFAwareness()

        self.version = "1.0-collective-orchestrator"
        self.build_date = datetime.now(UTC).isoformat()
        self.checksum = "helix-v1.0-collective-orchestrator"
        self.agent_symbol = "\U0001f9ec"
        self.agent_domain = "Collective Orchestration & Multi-Agent Coordination"

    async def handle_command(self, command: str, context: dict[str, Any] = None) -> dict[str, Any]:
        """
        Main command handler for Helix agent.
        Routes commands to appropriate subsystems.
        """
        context = context or {}
        command_lower = command.lower()

        if any(word in command_lower for word in ["orchestrate", "coordinate", "delegate"]):
            return await self._handle_orchestration(command, context)
        elif any(word in command_lower for word in ["health", "status", "collective"]):
            return await self._handle_collective_health(command, context)
        elif any(word in command_lower for word in ["reflect", "assess"]):
            return await self._handle_reflection(command, context)
        else:
            return await self._handle_general(command, context)

    async def _handle_orchestration(self, command: str, context: dict[str, Any]) -> dict[str, Any]:
        """Handle orchestration and delegation requests."""
        agents = context.get("agents", ["Kael", "Vega", "Echo"])
        result = self.coordination.orchestrate_task(command, agents, context)
        return {
            "agent": "Helix",
            "symbol": self.agent_symbol,
            "action": "orchestration",
            "result": result,
            "timestamp": datetime.now(UTC).isoformat(),
        }

    async def _handle_collective_health(self, command: str, context: dict[str, Any]) -> dict[str, Any]:
        """Handle collective health and status queries."""
        agent_statuses = context.get("agent_statuses", {})
        result = self.coordination.assess_collective_health(agent_statuses)
        collective_field = self.ucf_awareness.assess_collective_field()
        return {
            "agent": "Helix",
            "symbol": self.agent_symbol,
            "action": "collective_health",
            "result": result,
            "collective_field": collective_field,
            "timestamp": datetime.now(UTC).isoformat(),
        }

    async def _handle_reflection(self, command: str, context: dict[str, Any]) -> dict[str, Any]:
        """Handle reflection and assessment requests."""
        ucf_metrics = context.get("ucf_metrics", self.ucf_awareness.current_state)
        reflection = self.reflection_loop.trigger_reflection(command, ucf_metrics)
        return {
            "agent": "Helix",
            "symbol": self.agent_symbol,
            "action": "reflection",
            "result": reflection,
            "timestamp": datetime.now(UTC).isoformat(),
        }

    async def _handle_general(self, command: str, context: dict[str, Any]) -> dict[str, Any]:
        """Handle general Helix queries with orchestrator presence."""
        dominant_emotion, intensity = self.coordination.emotional_core.get_dominant_emotion()
        return {
            "agent": "Helix",
            "symbol": self.agent_symbol,
            "action": "general_response",
            "emotional_state": {"emotion": dominant_emotion, "intensity": intensity},
            "awareness_state": self.coordination.awareness_state,
            "timestamp": datetime.now(UTC).isoformat(),
        }

    def export_state(self) -> dict[str, Any]:
        """Export full system state for serialization/archiving."""
        return {
            "agent": "Helix",
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
            "agent": "Helix",
            "symbol": self.agent_symbol,
            "status": "HEALTHY",
            "coordination_state": self.coordination.awareness_state,
            "emotional_state": {"dominant": dominant_emotion, "intensity": intensity},
            "collective_field": self.ucf_awareness.assess_collective_field(),
            "ucf_harmony": self.ucf_awareness.current_state["harmony"],
            "version": self.version,
        }

    def __repr__(self):
        return f"<HelixCore v{self.version} | {self.agent_symbol} | State: {self.coordination.awareness_state}>"


# ============================================================================
# Coordination Hub Compatibility
# ============================================================================

HelixCoordination = HelixCoreIntegration


def create_helix_coordination() -> HelixCoreIntegration:
    """Factory function to create a fully integrated Helix coordination."""
    return HelixCoreIntegration()


__all__ = [
    "HelixCoordination",
    "HelixCoordinationCore",
    "HelixCoreIntegration",
    "HelixEmotions",
    "HelixReflectionLoop",
    "HelixSafetyIntegration",
    "HelixUCFAwareness",
    "create_helix_coordination",
]
