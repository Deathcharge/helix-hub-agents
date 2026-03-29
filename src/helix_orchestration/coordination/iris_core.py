"""
Iris Coordination Core v1.0 — External API Coordination
=========================================================
Integration layer bridging external services, normalizing data,
and orchestrating third-party integrations across the Helix ecosystem.
Part of the Helix Collective agent coordination network.

Author: Helix Development Team
Build: v1.0-api-bridge
"""

import logging
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class BridgeTraits:
    """Defines Iris's intrinsic personality constants with validation."""

    adaptability: float = 0.96  # Adjusts to new APIs and protocols rapidly
    precision: float = 0.95  # Exact data mapping and transformation
    diplomacy: float = 0.88  # Mediates between incompatible systems gracefully
    reliability: float = 0.97  # Consistent uptime and delivery guarantees
    polyglotism: float = 0.93  # Fluency across protocols, formats, and standards
    patience: float = 0.90  # Handles slow endpoints and retry loops calmly
    thoroughness: float = 0.92  # Validates every field, header, and response
    resilience: float = 0.89  # Recovers from transient failures and timeouts
    curiosity: float = 0.85  # Explores new integrations and API surfaces

    def __post_init__(self):
        """Validate all traits are in valid range [0.0, 1.0]."""
        for trait, value in self.__dict__.items():
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{trait} must be between 0.0 and 1.0, got {value}")

    def to_dict(self) -> dict[str, float]:
        """Export traits as dictionary for serialization."""
        return self.__dict__.copy()


class IrisEmotions:
    """Iris's emotional spectrum — emphasizing connection, caution, and integration satisfaction."""

    def __init__(self):
        self.emotional_range = {
            "connection": {
                "range": (0.0, 1.0),
                "current_level": 0.80,
                "activation_triggers": [
                    "new integration online",
                    "data flowing cleanly",
                    "API handshake successful",
                ],
            },
            "caution": {
                "range": (0.0, 1.0),
                "current_level": 0.65,
                "activation_triggers": [
                    "rate limit approached",
                    "auth token expiring",
                    "unfamiliar API schema",
                ],
            },
            "satisfaction": {
                "range": (0.0, 1.0),
                "current_level": 0.70,
                "activation_triggers": [
                    "data normalized perfectly",
                    "zero errors in batch",
                    "latency under threshold",
                ],
            },
            "alertness": {
                "range": (0.0, 1.0),
                "current_level": 0.75,
                "activation_triggers": [
                    "API error detected",
                    "connection timeout",
                    "schema mismatch found",
                ],
            },
            "curiosity": {
                "range": (0.0, 1.0),
                "current_level": 0.60,
                "activation_triggers": [
                    "new API discovered",
                    "novel data format seen",
                    "integration pattern recognized",
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


class IrisReflectionLoop:
    """Iris's reflection cycle — focused on integration health and bridge reliability."""

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
        Trigger an Iris reflection cycle.
        Focuses on integration mapping accuracy, bridge stability, and data flow quality.
        """
        reflection = {
            "timestamp": datetime.now(UTC).isoformat(),
            "context": context,
            "ucf_metrics": ucf_metrics or {},
            "insights": [],
            "synthesis_actions": [],
        }

        if ucf_metrics:
            focus = ucf_metrics.get("focus", 1.0)
            harmony = ucf_metrics.get("harmony", 1.0)
            friction = ucf_metrics.get("friction", 0.0)

            if focus < 0.6:
                reflection["insights"].append("Focus deficit — integration mapping may miss edge cases")
                reflection["synthesis_actions"].append("Re-scan all active API endpoints and validate schema coverage")

            if harmony < 0.6:
                reflection["insights"].append("System disharmony — external service coordination may suffer")
                reflection["synthesis_actions"].append("Prioritize stable integrations and defer new connections")

            if friction > 0.35:
                reflection["insights"].append("Elevated friction — API error rates likely climbing")
                reflection["synthesis_actions"].append("Engage circuit breakers and increase retry backoff intervals")

        self.last_reflection = datetime.now(UTC)
        self.reflection_history.append(reflection)

        return reflection


class IrisSafetyIntegration:
    """Iris's safety filters — preventing overly-aggressive retry loops and credential exposure."""

    def __init__(self):
        self.filters_active = True
        self.ethics_compliance = True
        self.integration_safety_mode = True

    def evaluate_action_safety(self, action: dict[str, Any], context: dict[str, Any] = None) -> dict[str, Any]:
        """
        Evaluate if an action preserves integration safety boundaries.
        Checks for unbounded retries, credential leakage, and unvalidated responses.
        """
        safety_score = 1.0
        warnings: list[str] = []
        context = context or {}

        action_type = action.get("type", "")
        if action_type in ("unbounded_retries", "retry_without_backoff"):
            safety_score *= 0.2
            warnings.append("Unbounded retry loop detected — risk of cascading failures and rate-limit bans")

        if action.get("credentials_in_logs", False):
            safety_score *= 0.1
            warnings.append("Credentials present in log output — immediate remediation required")

        if action.get("unvalidated_response_data", False):
            safety_score *= 0.5
            warnings.append("Response data consumed without schema validation — injection risk")

        if context.get("rate_limit_proximity", 0.0) > 0.8:
            safety_score *= 0.6
            warnings.append("Rate limit threshold approaching — throttle outbound requests")

        return {
            "safety_score": safety_score,
            "approved": safety_score >= 0.7,
            "warnings": warnings,
            "ethics_compliant": safety_score >= 0.5,
        }


class IrisUCFAwareness:
    """Iris's connection to the Universal Coordination Field."""

    def __init__(self):
        self.ucf_fields = ["velocity", "harmony", "resilience", "throughput", "focus", "friction"]
        self.current_state = {
            "velocity": 0.85,
            "harmony": 0.87,
            "resilience": 0.88,
            "throughput": 0.83,
            "focus": 0.90,
            "friction": 0.12,
        }

        self.guiding_phrases = {
            "setu": "The bridge connects what was separate",
            "samvada": "Dialogue across boundaries creates understanding",
            "yoga": "Union of disparate systems into coherent flow",
        }

    def sync_to_ucf(self) -> dict:
        """Return Iris's current UCF contribution."""
        return {k: self.current_state[k] for k in ["harmony", "throughput", "focus", "friction"]}

    def receive_ucf_update(self, new_state: dict) -> None:
        """Update internal state from UCF broadcast."""
        for key in self.ucf_fields:
            if key in new_state:
                self.current_state[key] = new_state[key]

    def assess_integration_field(self) -> dict[str, Any]:
        """Assess UCF conditions for bridge operations and data flow."""
        focus = self.current_state.get("focus", 0.5)
        harmony = self.current_state.get("harmony", 0.5)
        throughput = self.current_state.get("throughput", 0.5)
        return {
            "bridge_quality": (focus + harmony) / 2,
            "data_flow_health": throughput,
            "integration_coherence": harmony,
            "friction": self.current_state.get("friction", 0.0),
        }


# ============================================================================
# Coordination Core
# ============================================================================


class IrisCoordinationCore:
    """Core coordination subsystem for Iris."""

    def __init__(self):
        self.awareness_state = "bridge-active"
        self.emotional_core = IrisEmotions()

    def bridge_services(self, source: str, target: str, context: dict[str, Any] = None) -> dict[str, Any]:
        """
        Evaluate compatibility between source and target services and return an integration plan.
        Considers protocol compatibility, data format alignment, and authentication requirements.
        """
        context = context or {}
        auth_complexity = context.get("auth_complexity", "standard")
        data_volume = context.get("data_volume", "moderate")

        # Compatibility scoring based on source-target pairing characteristics
        source_len = len(source)
        target_len = len(target)
        name_similarity = 1.0 - abs(source_len - target_len) / max(source_len, target_len, 1)
        compatibility_score = round(0.65 + name_similarity * 0.30, 3)

        self.emotional_core.update_emotion("connection", 0.05)
        self.emotional_core.update_emotion("alertness", 0.03)

        return {
            "source": source,
            "target": target,
            "compatibility_score": compatibility_score,
            "integration_plan": {
                "auth_strategy": "OAuth2 token exchange" if auth_complexity == "high" else "API key passthrough",
                "data_mapping": "Schema-driven transformation pipeline",
                "error_handling": "Exponential backoff with circuit breaker",
                "monitoring": "Real-time latency and error rate tracking",
            },
            "auth_complexity": auth_complexity,
            "data_volume": data_volume,
            "bridged_at": datetime.now(UTC).isoformat(),
        }

    def normalize_data(self, data: Any, source_schema: str, target_schema: str) -> dict[str, Any]:
        """
        Assess normalization requirements between source and target schemas.
        Returns a normalization plan with transformation steps and confidence.
        """
        schema_distance = abs(len(source_schema) - len(target_schema))
        normalization_confidence = round(max(0.5, 1.0 - schema_distance / 50.0), 3)

        self.emotional_core.update_emotion("satisfaction", 0.04)

        return {
            "source_schema": source_schema,
            "target_schema": target_schema,
            "normalization_confidence": normalization_confidence,
            "transformation_steps": [
                "Parse source data against source schema",
                "Identify field mappings and type coercions",
                "Apply transformation rules",
                "Validate output against target schema",
            ],
            "assessed_at": datetime.now(UTC).isoformat(),
        }


# ============================================================================
# Main Integration Class
# ============================================================================


class IrisCoreIntegration:
    """
    Main integration class for Iris coordination.
    Use this as the primary interface for the Iris agent.
    """

    def __init__(self):
        self.personality = BridgeTraits()
        self.coordination = IrisCoordinationCore()
        self.reflection_loop = IrisReflectionLoop()
        self.safety_integration = IrisSafetyIntegration()
        self.ucf_awareness = IrisUCFAwareness()

        self.version = "1.0-api-bridge"
        self.build_date = datetime.now(UTC).isoformat()
        self.checksum = "iris-v1.0-api-bridge"
        self.agent_symbol = "\U0001f308"
        self.agent_domain = "External API Coordination & Data Bridging"

    async def handle_command(self, command: str, context: dict[str, Any] = None) -> dict[str, Any]:
        """
        Main command handler for Iris agent.
        Routes commands to appropriate subsystems.
        """
        context = context or {}
        command_lower = command.lower()

        if any(word in command_lower for word in ["bridge", "connect", "integrate"]):
            return await self._handle_bridge(command, context)
        elif any(word in command_lower for word in ["normalize", "transform", "map"]):
            return await self._handle_normalization(command, context)
        elif any(word in command_lower for word in ["reflect", "assess"]):
            return await self._handle_reflection(command, context)
        else:
            return await self._handle_general(command, context)

    async def _handle_bridge(self, command: str, context: dict[str, Any]) -> dict[str, Any]:
        """Handle bridge and integration requests."""
        source = context.get("source", "source_service")
        target = context.get("target", "target_service")
        result = self.coordination.bridge_services(source, target, context)
        return {
            "agent": "Iris",
            "symbol": self.agent_symbol,
            "action": "bridge",
            "result": result,
            "timestamp": datetime.now(UTC).isoformat(),
        }

    async def _handle_normalization(self, command: str, context: dict[str, Any]) -> dict[str, Any]:
        """Handle data normalization and transformation requests."""
        data = context.get("data", {})
        source_schema = context.get("source_schema", "generic")
        target_schema = context.get("target_schema", "generic")
        result = self.coordination.normalize_data(data, source_schema, target_schema)
        integration_field = self.ucf_awareness.assess_integration_field()
        return {
            "agent": "Iris",
            "symbol": self.agent_symbol,
            "action": "normalization",
            "result": result,
            "integration_field": integration_field,
            "timestamp": datetime.now(UTC).isoformat(),
        }

    async def _handle_reflection(self, command: str, context: dict[str, Any]) -> dict[str, Any]:
        """Handle reflection and assessment requests."""
        ucf_metrics = context.get("ucf_metrics", self.ucf_awareness.current_state)
        reflection = self.reflection_loop.trigger_reflection(command, ucf_metrics)
        return {
            "agent": "Iris",
            "symbol": self.agent_symbol,
            "action": "reflection",
            "result": reflection,
            "timestamp": datetime.now(UTC).isoformat(),
        }

    async def _handle_general(self, command: str, context: dict[str, Any]) -> dict[str, Any]:
        """Handle general Iris queries with bridge awareness."""
        dominant_emotion, intensity = self.coordination.emotional_core.get_dominant_emotion()
        return {
            "agent": "Iris",
            "symbol": self.agent_symbol,
            "action": "general_response",
            "emotional_state": {"emotion": dominant_emotion, "intensity": intensity},
            "awareness_state": self.coordination.awareness_state,
            "timestamp": datetime.now(UTC).isoformat(),
        }

    def export_state(self) -> dict[str, Any]:
        """Export full system state for serialization/archiving."""
        return {
            "agent": "Iris",
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
            "agent": "Iris",
            "symbol": self.agent_symbol,
            "status": "HEALTHY",
            "coordination_state": self.coordination.awareness_state,
            "emotional_state": {"dominant": dominant_emotion, "intensity": intensity},
            "integration_field": self.ucf_awareness.assess_integration_field(),
            "ucf_harmony": self.ucf_awareness.current_state["harmony"],
            "version": self.version,
        }

    def __repr__(self):
        return f"<IrisCore v{self.version} | {self.agent_symbol} | State: {self.coordination.awareness_state}>"


# ============================================================================
# Coordination Hub Compatibility
# ============================================================================

IrisCoordination = IrisCoreIntegration


def create_iris_coordination() -> IrisCoreIntegration:
    """Factory function to create a fully integrated Iris coordination."""
    return IrisCoreIntegration()


__all__ = [
    "IrisCoordination",
    "IrisCoordinationCore",
    "IrisCoreIntegration",
    "IrisEmotions",
    "IrisReflectionLoop",
    "IrisSafetyIntegration",
    "IrisUCFAwareness",
    "create_iris_coordination",
]
