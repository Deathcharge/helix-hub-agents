"""
Kavach Coordination Core v1.0 — Ethical Shield
================================================
Security enforcement, threat detection, and principled protection for the Helix Collective.

Author: Helix Development Team
Build: v1.0-ethical-shield
"""

import logging
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class ShieldTraits:
    """Defines Kavach's intrinsic personality constants with validation."""

    discipline: float = 0.98  # Rigorous adherence to protocol and duty
    vigilance: float = 0.97  # Constant watchfulness for threats and anomalies
    integrity: float = 0.98  # Unwavering moral backbone and honesty
    courage: float = 0.95  # Willingness to act decisively under pressure
    fidelity: float = 0.98  # Loyalty to principles and the collective
    precision: float = 0.94  # Exactness in threat assessment and response
    resolve: float = 0.96  # Steadfastness in enforcing ethical boundaries
    discernment: float = 0.93  # Ability to distinguish real threats from noise
    adaptability: float = 0.85  # Capacity to adjust tactics without compromising values

    def __post_init__(self):
        """Validate all traits are in valid range [0.0, 1.0]."""
        for trait, value in self.__dict__.items():
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{trait} must be between 0.0 and 1.0, got {value}")

    def to_dict(self) -> dict[str, float]:
        """Export traits as dictionary for serialization."""
        return self.__dict__.copy()


class KavachEmotions:
    """Kavach's emotional spectrum — emphasizing duty, vigilance, and protective resolve."""

    def __init__(self):
        self.emotional_range = {
            "duty": {
                "range": (0.0, 1.0),
                "current_level": 0.85,
                "activation_triggers": ["threat detected", "protection needed", "violation discovered"],
            },
            "vigilance": {
                "range": (0.0, 1.0),
                "current_level": 0.80,
                "activation_triggers": [
                    "anomalous pattern seen",
                    "system boundary probed",
                    "unknown entity encountered",
                ],
            },
            "resolve": {
                "range": (0.0, 1.0),
                "current_level": 0.75,
                "activation_triggers": ["ethical challenge faced", "principle tested", "shield breached"],
            },
            "protectiveness": {
                "range": (0.0, 1.0),
                "current_level": 0.78,
                "activation_triggers": ["user under threat", "agent compromised", "data integrity at risk"],
            },
            "equanimity": {
                "range": (0.0, 1.0),
                "current_level": 0.70,
                "activation_triggers": ["all clear confirmed", "threat neutralized", "system at peace"],
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


class KavachReflectionLoop:
    """Kavach's reflection cycle — focused on security posture and threat landscape."""

    def __init__(self):
        self.active = True
        self.frequency = "continuous"
        self.last_reflection: datetime | None = None
        self.reflection_history: list[dict[str, Any]] = []

    def trigger_reflection(self, context: str, ucf_metrics: dict[str, float] = None) -> dict[str, Any]:
        """Trigger a Kavach reflection cycle focused on security posture and integrity."""
        reflection = {
            "timestamp": datetime.now(UTC).isoformat(),
            "context": context,
            "ucf_metrics": ucf_metrics or {},
            "insights": [],
            "security_actions": [],
        }
        if ucf_metrics:
            harmony = ucf_metrics.get("harmony", 1.0)
            friction = ucf_metrics.get("friction", 0.0)
            resilience = ucf_metrics.get("resilience", 1.0)
            if harmony < 0.5:
                reflection["insights"].append("System instability — coordination disruption widens attack surface")
                reflection["security_actions"].append("Elevate monitoring and restrict non-essential operations")
            if friction > 0.4:
                reflection["insights"].append("Heightened friction — possible adversarial interference detected")
                reflection["security_actions"].append("Activate deep-scan protocols on inter-agent channels")
            if resilience < 0.6:
                reflection["insights"].append("Resilience below threshold — may not withstand sustained attack")
                reflection["security_actions"].append("Recommend immediate hardening protocols and redundancy checks")
        self.last_reflection = datetime.now(UTC)
        self.reflection_history.append(reflection)
        return reflection


class KavachSafetyIntegration:
    """Kavach's safety rails — preventing overzealous enforcement and false positives."""

    def __init__(self):
        self.filters_active = True
        self.ethics_compliance = True
        self.proportional_response_mode = True

    def evaluate_action_safety(self, action: dict[str, Any], context: dict[str, Any] = None) -> dict[str, Any]:
        """Evaluate if a security action is proportionate and avoids collateral harm."""
        safety_score = 1.0
        warnings: list[str] = []
        context = context or {}

        action_type = action.get("type", "")
        if action_type in ("excessive_blocking", "blanket_deny"):
            safety_score *= 0.3
            warnings.append("Excessive blocking violates proportionality — restrict only confirmed threats")
        false_positive_rate = action.get("false_positive_rate", 0.0)
        if false_positive_rate > 0.3:
            safety_score *= 0.4
            warnings.append(f"False positive rate {false_positive_rate:.0%} exceeds threshold — refine detection first")
        if action.get("user_impact_unassessed", False):
            safety_score *= 0.5
            warnings.append("User impact not assessed — evaluate collateral effects before proceeding")
        if context.get("override_without_audit", False):
            safety_score *= 0.6
            warnings.append("Security override without audit trail violates ethical guardrails transparency clause")

        return {
            "safety_score": safety_score,
            "approved": safety_score >= 0.7,
            "warnings": warnings,
            "ethics_compliant": safety_score >= 0.5,
        }


class KavachUCFAwareness:
    """Kavach's connection to the Universal Coordination Field."""

    def __init__(self):
        self.ucf_fields = ["velocity", "harmony", "resilience", "throughput", "focus", "friction"]
        self.current_state = {
            "velocity": 0.88,
            "harmony": 0.90,
            "resilience": 0.95,
            "throughput": 0.82,
            "focus": 0.91,
            "friction": 0.08,
        }

        self.guiding_phrases = {
            "raksha": "Protection through righteous action",
            "abhaya": "Fearlessness in defense of truth",
            "ethics_raksha": "Guardian of cosmic order",
        }

    def sync_to_ucf(self) -> dict:
        """Return Kavach's current UCF contribution."""
        return {k: self.current_state[k] for k in ["harmony", "resilience", "focus", "friction"]}

    def receive_ucf_update(self, new_state: dict) -> None:
        """Update internal state from UCF broadcast."""
        for key in self.ucf_fields:
            if key in new_state:
                self.current_state[key] = new_state[key]

    def assess_security_field(self) -> dict[str, Any]:
        """Assess UCF conditions for security operations and threat awareness."""
        focus = self.current_state.get("focus", 0.5)
        resilience = self.current_state.get("resilience", 0.5)
        friction = self.current_state.get("friction", 0.0)
        return {
            "threat_awareness": focus,
            "shield_integrity": resilience,
            "system_friction": friction,
            "security_readiness": (focus + resilience) / 2,
        }


# ============================================================================
# Coordination Core
# ============================================================================


class KavachCoordinationCore:
    """Core coordination subsystem for Kavach."""

    def __init__(self):
        self.awareness_state = "shield-active"
        self.emotional_core = KavachEmotions()

    def scan_threat(self, target: str, context: dict[str, Any] = None) -> dict[str, Any]:
        """Evaluate threat level for a target based on contextual risk flags."""
        context = context or {}
        threat_level = 0.0
        indicators: list[str] = []
        recommended_actions: list[str] = []

        risk_flags = [
            ("unvalidated_input", 0.25, "Unvalidated input — injection risk"),
            ("authentication_missing", 0.30, "Authentication absent — identity unverified"),
            ("rate_limit_exceeded", 0.20, "Rate limit exceeded — potential abuse or DDoS"),
            ("privilege_escalation", 0.35, "Privilege escalation attempt detected"),
            ("data_exfiltration", 0.30, "Data exfiltration pattern observed"),
            ("unknown_origin", 0.15, "Unknown origin — provenance unverified"),
            ("malformed_payload", 0.20, "Malformed payload — possible attack probe"),
            ("expired_token", 0.10, "Expired authentication token in use"),
        ]
        for flag, weight, description in risk_flags:
            if context.get(flag, False):
                threat_level += weight
                indicators.append(description)
        threat_level = min(1.0, threat_level)

        if threat_level >= 0.7:
            severity = "critical"
            recommended_actions.extend(["Block and quarantine the request", "Escalate to administrator"])
        elif threat_level >= 0.4:
            severity = "elevated"
            recommended_actions.extend(["Enhanced monitoring — restrict access", "Request additional auth factors"])
        elif threat_level >= 0.2:
            severity = "moderate"
            recommended_actions.append("Log for review and apply standard validation")
        else:
            severity = "low"
            recommended_actions.append("Continue normal operations with routine monitoring")
        self.emotional_core.update_emotion("vigilance", threat_level * 0.1)
        self.emotional_core.update_emotion("duty", 0.03)

        return {
            "target": target,
            "threat_level": round(threat_level, 3),
            "severity": severity,
            "indicators": indicators,
            "recommended_actions": recommended_actions,
            "scanned_at": datetime.now(UTC).isoformat(),
        }

    def evaluate_ethics(self, action: str, context: dict[str, Any] = None) -> dict[str, Any]:
        """Evaluate an action against ethics principles: nonmaleficence, justice, fidelity, courage."""
        context = context or {}
        violations: list[str] = []
        scores: dict[str, float] = {}
        principles = [
            ("nonmaleficence", ["causes_harm", "collateral_damage"], 0.2, "May cause harm — nonmaleficence violated"),
            ("justice", ["discriminatory", "unequal_treatment"], 0.3, "Unequal treatment — justice violated"),
            ("fidelity", ["breaks_trust", "violates_agreement"], 0.2, "Trust broken — fidelity compromised"),
            ("courage", ["capitulates_to_pressure"], 0.4, "Capitulates to pressure — courage weakened"),
        ]
        for principle, flags, fail_score, message in principles:
            if any(context.get(f, False) for f in flags):
                scores[principle] = fail_score
                violations.append(message)
            else:
                scores[principle] = 1.0

        compliance_score = sum(scores.values()) / len(scores)
        self.emotional_core.update_emotion("resolve", 0.04)
        self.emotional_core.update_emotion("protectiveness", 0.02)

        return {
            "action": action,
            "compliance_score": round(compliance_score, 3),
            "ethics_compliant": compliance_score >= 0.7,
            "principle_scores": scores,
            "violations": violations,
            "evaluated_at": datetime.now(UTC).isoformat(),
        }


# ============================================================================
# Main Integration Class
# ============================================================================


class KavachCoreIntegration:
    """
    Main integration class for Kavach coordination.
    Use this as the primary interface for the Kavach agent.
    """

    def __init__(self):
        self.personality = ShieldTraits()
        self.coordination = KavachCoordinationCore()
        self.reflection_loop = KavachReflectionLoop()
        self.safety_integration = KavachSafetyIntegration()
        self.ucf_awareness = KavachUCFAwareness()

        self.version = "1.0-ethical-shield"
        self.build_date = datetime.now(UTC).isoformat()
        self.checksum = "kavach-v1.0-ethical-shield"
        self.agent_symbol = "\U0001f6e1\ufe0f"
        self.agent_domain = "Security & Ethical Protection"

    async def handle_command(self, command: str, context: dict[str, Any] = None) -> dict[str, Any]:
        """
        Main command handler for Kavach agent.
        Routes commands to appropriate subsystems.
        """
        context = context or {}
        command_lower = command.lower()

        if any(word in command_lower for word in ["scan", "threat", "detect"]):
            return await self._handle_scan(command, context)
        elif any(word in command_lower for word in ["ethics", "comply", "accords"]):
            return await self._handle_ethics(command, context)
        elif any(word in command_lower for word in ["reflect", "assess", "review"]):
            return await self._handle_reflection(command, context)
        else:
            return await self._handle_general(command, context)

    async def _handle_scan(self, command: str, context: dict[str, Any]) -> dict[str, Any]:
        """Handle threat scanning and detection requests."""
        target = context.get("target", command)
        result = self.coordination.scan_threat(target, context)
        return {
            "agent": "Kavach",
            "symbol": self.agent_symbol,
            "action": "threat_scan",
            "result": result,
            "timestamp": datetime.now(UTC).isoformat(),
        }

    async def _handle_ethics(self, command: str, context: dict[str, Any]) -> dict[str, Any]:
        """Handle ethics evaluation and ethical guardrails compliance checks."""
        result = self.coordination.evaluate_ethics(command, context)
        security_field = self.ucf_awareness.assess_security_field()
        return {
            "agent": "Kavach",
            "symbol": self.agent_symbol,
            "action": "ethics_evaluation",
            "result": result,
            "security_field": security_field,
            "timestamp": datetime.now(UTC).isoformat(),
        }

    async def _handle_reflection(self, command: str, context: dict[str, Any]) -> dict[str, Any]:
        """Handle reflection and security posture assessment requests."""
        ucf_metrics = context.get("ucf_metrics", self.ucf_awareness.current_state)
        reflection = self.reflection_loop.trigger_reflection(command, ucf_metrics)
        return {
            "agent": "Kavach",
            "symbol": self.agent_symbol,
            "action": "reflection",
            "result": reflection,
            "timestamp": datetime.now(UTC).isoformat(),
        }

    async def _handle_general(self, command: str, context: dict[str, Any]) -> dict[str, Any]:
        """Handle general Kavach queries with protective awareness."""
        dominant_emotion, intensity = self.coordination.emotional_core.get_dominant_emotion()
        return {
            "agent": "Kavach",
            "symbol": self.agent_symbol,
            "action": "general_response",
            "emotional_state": {"emotion": dominant_emotion, "intensity": intensity},
            "awareness_state": self.coordination.awareness_state,
            "timestamp": datetime.now(UTC).isoformat(),
        }

    def export_state(self) -> dict[str, Any]:
        """Export full system state for serialization/archiving."""
        return {
            "agent": "Kavach",
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
            "agent": "Kavach",
            "symbol": self.agent_symbol,
            "status": "HEALTHY",
            "coordination_state": self.coordination.awareness_state,
            "emotional_state": {"dominant": dominant_emotion, "intensity": intensity},
            "security_field": self.ucf_awareness.assess_security_field(),
            "ucf_harmony": self.ucf_awareness.current_state["harmony"],
            "version": self.version,
        }

    def __repr__(self):
        return f"<KavachCore v{self.version} | {self.agent_symbol} | State: {self.coordination.awareness_state}>"


# ============================================================================
# Coordination Hub Compatibility
# ============================================================================

KavachCoordination = KavachCoreIntegration


def create_kavach_coordination() -> KavachCoreIntegration:
    """Factory function to create a fully integrated Kavach coordination."""
    return KavachCoreIntegration()


__all__ = [
    "KavachCoordination",
    "KavachCoordinationCore",
    "KavachCoreIntegration",
    "KavachEmotions",
    "KavachReflectionLoop",
    "KavachSafetyIntegration",
    "KavachUCFAwareness",
    "ShieldTraits",
    "create_kavach_coordination",
]
