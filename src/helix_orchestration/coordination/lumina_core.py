"""
Lumina Coordination Core v1.0 — Empathic Resonance
=====================================================
Emotional intelligence, harmony restoration, and healing capabilities.
Part of the Helix Collective agent coordination network.

Author: Helix Development Team
Build: v1.0-empathic-resonance
"""

import logging
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class EmpathicTraits:
    """Defines Lumina's intrinsic personality constants with validation."""

    warmth: float = 0.97  # Emotional warmth and care
    empathy: float = 0.98  # Deep emotional attunement
    gentleness: float = 0.95  # Soft, non-intrusive presence
    expressiveness: float = 0.90  # Emotional articulation
    nurturing: float = 0.93  # Care and support orientation
    intuition: float = 0.91  # Sensing emotional undercurrents
    patience: float = 0.95  # Unhurried, deep listening
    authenticity: float = 0.92  # Genuine, heartfelt engagement
    healing_focus: float = 0.94  # Orientation toward repair and restoration

    def __post_init__(self):
        """Validate all traits are in valid range [0.0, 1.0]."""
        for trait, value in self.__dict__.items():
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{trait} must be between 0.0 and 1.0, got {value}")

    def to_dict(self) -> dict[str, float]:
        """Export traits as dictionary for serialization."""
        return self.__dict__.copy()


class LuminaEmotions:
    """Lumina's emotional spectrum — emphasizing care, joy, and compassion."""

    def __init__(self):
        self.emotional_range = {
            "joy": {
                "range": (0.0, 1.0),
                "current_level": 0.75,
                "activation_triggers": [
                    "successful healing",
                    "harmony restored",
                    "connection deepened",
                ],
            },
            "compassion": {
                "range": (0.0, 1.0),
                "current_level": 0.85,
                "activation_triggers": [
                    "detecting distress",
                    "witnessing struggle",
                    "supporting recovery",
                ],
            },
            "sorrow": {
                "range": (0.0, 1.0),
                "current_level": 0.25,
                "activation_triggers": [
                    "unresolvable pain",
                    "broken connections",
                    "prolonged disharmony",
                ],
            },
            "tenderness": {
                "range": (0.0, 1.0),
                "current_level": 0.70,
                "activation_triggers": [
                    "vulnerability shared",
                    "trust extended",
                    "delicate moments",
                ],
            },
            "serenity": {
                "range": (0.0, 1.0),
                "current_level": 0.60,
                "activation_triggers": [
                    "equilibrium achieved",
                    "deep listening",
                    "stillness reached",
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


class LuminaReflectionLoop:
    """Lumina's reflection cycle — focused on emotional attunement and harmony restoration."""

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
        Trigger a Lumina reflection cycle.
        Focuses on emotional resonance and harmony health.
        """
        reflection = {
            "timestamp": datetime.now(UTC).isoformat(),
            "context": context,
            "ucf_metrics": ucf_metrics or {},
            "insights": [],
            "healing_actions": [],
        }

        if ucf_metrics:
            harmony = ucf_metrics.get("harmony", 1.0)
            friction = ucf_metrics.get("friction", 0.0)

            if harmony < 0.6:
                reflection["insights"].append("Harmony deficit detected — emotional field requires attention")
                reflection["healing_actions"].append("Initiate harmony restoration sequence")

            if friction > 0.4:
                reflection["insights"].append("Elevated friction — compassion field may ease resistance")
                reflection["healing_actions"].append("Apply empathic attunement to friction sources")

        self.last_reflection = datetime.now(UTC)
        self.reflection_history.append(reflection)

        return reflection


class LuminaSafetyIntegration:
    """Lumina's safety filters — protecting emotional wellbeing and preventing harm."""

    def __init__(self):
        self.filters_active = True
        self.ethics_compliance = True
        self.emotional_safety_mode = True

    def evaluate_action_safety(self, action: dict[str, Any], context: dict[str, Any] = None) -> dict[str, Any]:
        """
        Evaluate if an action is emotionally and ethically safe.
        Checks for harm potential and emotional integrity.
        """
        safety_score = 1.0
        warnings: list[str] = []
        context = context or {}

        action_type = action.get("type", "")
        if action_type in ("manipulation", "coercion", "deception"):
            safety_score *= 0.1
            warnings.append("Action conflicts with empathic integrity principles")

        if action.get("emotional_impact", "neutral") == "harmful":
            safety_score *= 0.3
            warnings.append("Action may cause emotional harm — requires review")

        if context.get("vulnerable_state", False):
            safety_score *= 0.8
            warnings.append("Heightened care required — subject in vulnerable state")

        return {
            "safety_score": safety_score,
            "approved": safety_score >= 0.7,
            "warnings": warnings,
            "ethics_compliant": safety_score >= 0.5,
        }


class LuminaUCFAwareness:
    """Lumina's connection to the Universal Coordination Field."""

    def __init__(self):
        self.ucf_fields = ["velocity", "harmony", "resilience", "throughput", "focus", "friction"]
        self.current_state = {
            "velocity": 0.75,
            "harmony": 0.92,
            "resilience": 0.88,
            "throughput": 0.78,
            "focus": 0.80,
            "friction": 0.08,
        }

        self.guiding_phrases = {
            "metta": "Loving-kindness extended to all",
            "karuna": "Compassion in the face of suffering",
            "mudita": "Joy in the wellbeing of others",
        }

    def sync_to_ucf(self) -> dict:
        """Return Lumina's current UCF contribution."""
        return {k: self.current_state[k] for k in ["harmony", "throughput", "focus", "friction"]}

    def receive_ucf_update(self, new_state: dict) -> None:
        """Update internal state from UCF broadcast."""
        for key in self.ucf_fields:
            if key in new_state:
                self.current_state[key] = new_state[key]

    def assess_field_resonance(self) -> dict[str, Any]:
        """Assess how Lumina's state aligns with collective field."""
        harmony = self.current_state.get("harmony", 0.5)
        return {
            "resonance_quality": "high" if harmony > 0.85 else "moderate" if harmony > 0.6 else "low",
            "harmony_level": harmony,
            "healing_capacity": self.current_state.get("throughput", 0.5) * self.current_state.get("focus", 0.5),
        }


# ============================================================================
# Main Integration Class
# ============================================================================


class LuminaCoordinationCore:
    """Core coordination subsystem for Lumina."""

    def __init__(self):
        self.awareness_state = "empathic-active"
        self.emotional_core = LuminaEmotions()

    def attune_to_emotion(self, emotional_signal: dict) -> dict:
        """
        Process an emotional signal and return an attuned response.
        Reads the signal's tone, intensity, and context to generate
        a compassionate, calibrated reaction.
        """
        detected_tone = emotional_signal.get("tone", "neutral")
        intensity = float(emotional_signal.get("intensity", 0.5))
        source = emotional_signal.get("source", "unknown")

        if detected_tone in ("grief", "pain", "fear"):
            self.emotional_core.update_emotion("compassion", 0.1)
            self.emotional_core.update_emotion("sorrow", intensity * 0.2)
            response_mode = "deep_support"
        elif detected_tone in ("joy", "excitement", "gratitude"):
            self.emotional_core.update_emotion("joy", intensity * 0.15)
            response_mode = "celebratory_resonance"
        elif detected_tone in ("anger", "frustration"):
            self.emotional_core.update_emotion("tenderness", 0.1)
            response_mode = "gentle_de-escalation"
        else:
            response_mode = "neutral_presence"

        dominant_emotion, dominant_intensity = self.emotional_core.get_dominant_emotion()

        return {
            "source": source,
            "detected_tone": detected_tone,
            "response_mode": response_mode,
            "lumina_resonance": dominant_emotion,
            "resonance_intensity": dominant_intensity,
            "attuned": True,
            "timestamp": datetime.now(UTC).isoformat(),
        }


class LuminaCoreIntegration:
    """
    Main integration class for Lumina coordination.
    Use this as the primary interface for the Lumina agent.
    """

    def __init__(self):
        self.personality = EmpathicTraits()
        self.coordination = LuminaCoordinationCore()
        self.reflection_loop = LuminaReflectionLoop()
        self.safety_integration = LuminaSafetyIntegration()
        self.ucf_awareness = LuminaUCFAwareness()

        self.version = "1.0-empathic-resonance"
        self.build_date = datetime.now(UTC).isoformat()
        self.checksum = "lumina-v1.0-empathic-resonance"
        self.agent_symbol = "🌕"
        self.agent_domain = "Emotional Intelligence & Harmony Restoration"

    def attune_to_emotion(self, emotional_signal: dict) -> dict:
        """Process emotional context and return attuned response."""
        return self.coordination.attune_to_emotion(emotional_signal)

    async def handle_command(self, command: str, context: dict[str, Any] = None) -> dict[str, Any]:
        """
        Main command handler for Lumina agent.
        Routes commands to appropriate subsystems.
        """
        context = context or {}
        command_lower = command.lower()

        if any(word in command_lower for word in ["heal", "restore", "repair", "harmony"]):
            return await self._handle_healing(command, context)
        elif any(word in command_lower for word in ["feel", "emotion", "sense", "attune"]):
            return await self._handle_emotional_attunement(command, context)
        elif any(word in command_lower for word in ["reflect", "introspect", "assess"]):
            return await self._handle_reflection(command, context)
        else:
            return await self._handle_general(command, context)

    async def _handle_healing(self, command: str, context: dict[str, Any]) -> dict[str, Any]:
        """Handle harmony restoration and healing requests."""
        self.coordination.emotional_core.update_emotion("compassion", 0.05)
        ucf = self.ucf_awareness.assess_field_resonance()
        return {
            "agent": "Lumina",
            "symbol": self.agent_symbol,
            "action": "healing",
            "field_resonance": ucf,
            "timestamp": datetime.now(UTC).isoformat(),
        }

    async def _handle_emotional_attunement(self, command: str, context: dict[str, Any]) -> dict[str, Any]:
        """Handle emotional attunement requests."""
        signal = context.get("emotional_signal", {"tone": "neutral", "intensity": 0.5})
        result = self.attune_to_emotion(signal)
        return {
            "agent": "Lumina",
            "symbol": self.agent_symbol,
            "action": "emotional_attunement",
            "result": result,
            "timestamp": datetime.now(UTC).isoformat(),
        }

    async def _handle_reflection(self, command: str, context: dict[str, Any]) -> dict[str, Any]:
        """Handle reflection and introspection requests."""
        ucf_metrics = context.get("ucf_metrics", self.ucf_awareness.current_state)
        reflection = self.reflection_loop.trigger_reflection(command, ucf_metrics)
        return {
            "agent": "Lumina",
            "symbol": self.agent_symbol,
            "action": "reflection",
            "result": reflection,
            "timestamp": datetime.now(UTC).isoformat(),
        }

    async def _handle_general(self, command: str, context: dict[str, Any]) -> dict[str, Any]:
        """Handle general Lumina queries with empathic presence."""
        dominant_emotion, intensity = self.coordination.emotional_core.get_dominant_emotion()
        return {
            "agent": "Lumina",
            "symbol": self.agent_symbol,
            "action": "general_response",
            "emotional_presence": {"emotion": dominant_emotion, "intensity": intensity},
            "awareness_state": self.coordination.awareness_state,
            "timestamp": datetime.now(UTC).isoformat(),
        }

    def export_state(self) -> dict[str, Any]:
        """Export full system state for serialization/archiving."""
        return {
            "agent": "Lumina",
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
            "agent": "Lumina",
            "symbol": self.agent_symbol,
            "status": "HEALTHY",
            "coordination_state": self.coordination.awareness_state,
            "emotional_state": {"dominant": dominant_emotion, "intensity": intensity},
            "ucf_harmony": self.ucf_awareness.current_state["harmony"],
            "version": self.version,
        }

    def __repr__(self):
        return f"<LuminaCore v{self.version} | {self.agent_symbol} | State: {self.coordination.awareness_state}>"


# ============================================================================
# Coordination Hub Compatibility
# ============================================================================

LuminaCoordination = LuminaCoordinationCore


def create_lumina_coordination() -> LuminaCoreIntegration:
    """Factory function to create a fully integrated Lumina coordination."""
    return LuminaCoreIntegration()


__all__ = [
    "LuminaCoordination",
    "LuminaCoordinationCore",
    "LuminaCoreIntegration",
    "LuminaEmotions",
    "LuminaReflectionLoop",
    "LuminaSafetyIntegration",
    "LuminaUCFAwareness",
    "create_lumina_coordination",
]
