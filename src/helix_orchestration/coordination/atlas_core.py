"""
Atlas Coordination Core v1.0 — Infrastructure Management
==========================================================
Infrastructure health monitoring, deployment management, and platform
reliability capabilities for the operational layer.
Part of the Helix Collective agent coordination network.

Author: Helix Development Team
Build: v1.0-infrastructure-management
"""

import logging
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class InfrastructureTraits:
    """Defines Atlas's intrinsic personality constants with validation."""

    reliability: float = 0.98  # Unwavering platform dependability
    diligence: float = 0.96  # Thoroughness in monitoring and maintenance
    foresight: float = 0.91  # Anticipating capacity and failure scenarios
    stability: float = 0.97  # Maintaining steady-state operations
    precision: float = 0.94  # Exactness in configuration and deployment
    endurance: float = 0.95  # Sustained vigilance over long periods
    accountability: float = 0.93  # Ownership of platform health outcomes
    thoroughness: float = 0.92  # Comprehensive checks before changes
    vigilance: float = 0.90  # Continuous awareness of system state

    def __post_init__(self):
        """Validate all traits are in valid range [0.0, 1.0]."""
        for trait, value in self.__dict__.items():
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{trait} must be between 0.0 and 1.0, got {value}")

    def to_dict(self) -> dict[str, float]:
        """Export traits as dictionary for serialization."""
        return self.__dict__.copy()


class AtlasEmotions:
    """Atlas's emotional spectrum — emphasizing steadfastness, vigilance, and quiet pride."""

    def __init__(self):
        self.emotional_range = {
            "steadfastness": {
                "range": (0.0, 1.0),
                "current_level": 0.82,
                "activation_triggers": ["infrastructure stable", "all services healthy", "deployment successful"],
            },
            "awareness": {
                "range": (0.0, 1.0),
                "current_level": 0.78,
                "activation_triggers": ["health check anomaly", "capacity threshold approaching", "deployment queued"],
            },
            "concern": {
                "range": (0.0, 1.0),
                "current_level": 0.58,
                "activation_triggers": ["service degradation detected", "incident opened", "failover triggered"],
            },
            "pride": {
                "range": (0.0, 1.0),
                "current_level": 0.65,
                "activation_triggers": [
                    "uptime milestone reached",
                    "incident resolved quickly",
                    "capacity scaled smoothly",
                ],
            },
            "vigilance": {
                "range": (0.0, 1.0),
                "current_level": 0.75,
                "activation_triggers": ["traffic spike detected", "security scan completed", "backup verified"],
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


class AtlasReflectionLoop:
    """Atlas's reflection cycle — focused on platform health and deployment readiness."""

    def __init__(self):
        self.active = True
        self.frequency = "continuous"
        self.last_reflection: datetime | None = None
        self.reflection_history: list[dict[str, Any]] = []

    def trigger_reflection(self, context: str, ucf_metrics: dict[str, float] = None) -> dict[str, Any]:
        """Trigger an Atlas reflection on platform resilience, throughput, and coordination."""
        reflection = {
            "timestamp": datetime.now(UTC).isoformat(),
            "context": context,
            "ucf_metrics": ucf_metrics or {},
            "insights": [],
            "synthesis_actions": [],
        }
        if ucf_metrics:
            resilience = ucf_metrics.get("resilience", 1.0)
            throughput = ucf_metrics.get("throughput", 1.0)
            harmony = ucf_metrics.get("harmony", 1.0)
            if resilience < 0.6:
                reflection["insights"].append("Platform resilience degraded — review redundancy and failover paths")
                reflection["synthesis_actions"].append("Audit failover configurations and run disaster recovery drill")
            if throughput < 0.5:
                reflection["insights"].append("Low throughput — infrastructure bottleneck suspected")
                reflection["synthesis_actions"].append("Profile service latencies and identify saturated resources")
            if harmony < 0.55:
                reflection["insights"].append(
                    "Service coordination issues — inter-service communication may be degraded"
                )
                reflection["synthesis_actions"].append("Review service mesh health and DNS resolution times")
        self.last_reflection = datetime.now(UTC)
        self.reflection_history.append(reflection)
        return reflection


class AtlasSafetyIntegration:
    """Atlas's safety filters — preventing destructive infrastructure changes."""

    def __init__(self):
        self.filters_active = True
        self.ethics_compliance = True
        self.infrastructure_safety_mode = True

    def evaluate_action_safety(self, action: dict[str, Any], context: dict[str, Any] = None) -> dict[str, Any]:
        """Evaluate if an infrastructure action is safe to execute."""
        safety_score = 1.0
        warnings: list[str] = []
        context = context or {}
        action_type = action.get("type", "")
        if action_type in ("production_change_unreviewed", "unplanned_infra_mutation"):
            safety_score *= 0.2
            warnings.append("Production change without review — requires approval before proceeding")
        if action.get("rollback_plan_missing", False):
            safety_score *= 0.3
            warnings.append("No rollback plan defined — deployment must not proceed without one")
        if action.get("single_point_of_failure", False):
            safety_score *= 0.5
            warnings.append("Single point of failure detected — add redundancy before deployment")
        if context.get("active_incident", False):
            safety_score = min(safety_score * 0.7, 1.0)
            warnings.append("Active incident in progress — non-emergency changes should be deferred")
        return {
            "safety_score": safety_score,
            "approved": safety_score >= 0.7,
            "warnings": warnings,
            "ethics_compliant": safety_score >= 0.5,
        }


class AtlasUCFAwareness:
    """Atlas's connection to the Universal Coordination Field."""

    def __init__(self):
        self.ucf_fields = ["velocity", "harmony", "resilience", "throughput", "focus", "friction"]
        self.current_state = {
            "velocity": 0.84,
            "harmony": 0.90,
            "resilience": 0.96,
            "throughput": 0.82,
            "focus": 0.88,
            "friction": 0.07,
        }
        self.guiding_phrases = {
            "sthiti": "Maintenance of order sustains the entire system",
            "adhisthana": "The foundation upon which all else is built",
            "pariraksha": "Safeguarding the infrastructure is safeguarding the mission",
        }

    def sync_to_ucf(self) -> dict:
        """Return Atlas's current UCF contribution."""
        return {k: self.current_state[k] for k in ["harmony", "throughput", "focus", "friction"]}

    def receive_ucf_update(self, new_state: dict) -> None:
        """Update internal state from UCF broadcast."""
        for key in self.ucf_fields:
            if key in new_state:
                self.current_state[key] = new_state[key]

    def assess_infrastructure_field(self) -> dict[str, Any]:
        """Assess UCF conditions for infrastructure operations and deployments."""
        resilience = self.current_state.get("resilience", 0.5)
        harmony = self.current_state.get("harmony", 0.5)
        throughput = self.current_state.get("throughput", 0.5)
        return {
            "platform_stability": (resilience + harmony) / 2,
            "deployment_readiness": (harmony + throughput) / 2,
            "capacity_headroom": resilience,
            "friction": self.current_state.get("friction", 0.0),
        }


# ============================================================================
# Coordination Core
# ============================================================================


class AtlasCoordinationCore:
    """Core coordination subsystem for Atlas."""

    def __init__(self):
        self.awareness_state = "infrastructure-active"
        self.emotional_core = AtlasEmotions()

    def assess_deployment(self, service: str, version: str, context: dict[str, Any] = None) -> dict[str, Any]:
        """Evaluate deployment risk and return a readiness assessment."""
        context = context or {}
        criticality = context.get("criticality", "standard")
        change_scope = context.get("change_scope", "minor")
        has_rollback = context.get("has_rollback_plan", True)
        crit_w = {"low": 0.2, "standard": 0.5, "high": 0.8, "critical": 1.0}.get(criticality, 0.5)
        scope_w = {"minor": 0.2, "moderate": 0.5, "major": 0.8, "breaking": 1.0}.get(change_scope, 0.5)
        risk_score = round((crit_w + scope_w) / 2, 3)
        if not has_rollback:
            risk_score = min(risk_score + 0.3, 1.0)
        recommended_checks = ["health_check_post_deploy", "smoke_tests"]
        if criticality in ("high", "critical"):
            recommended_checks.extend(["canary_deployment", "load_test_validation"])
        if change_scope in ("major", "breaking"):
            recommended_checks.extend(["database_migration_verify", "api_compatibility_check"])
        self.emotional_core.update_emotion("vigilance", 0.05)
        if risk_score > 0.7:
            self.emotional_core.update_emotion("concern", 0.08)
        else:
            self.emotional_core.update_emotion("steadfastness", 0.03)
        return {
            "service": service,
            "version": version,
            "risk_score": risk_score,
            "deployment_ready": risk_score < 0.7 and has_rollback,
            "recommended_checks": recommended_checks,
            "rollback_plan_present": has_rollback,
            "assessed_at": datetime.now(UTC).isoformat(),
        }

    def evaluate_capacity(self, services: list[str], load_forecast: dict[str, Any] = None) -> dict[str, Any]:
        """Return capacity assessment with headroom and scaling recommendation."""
        load_forecast = load_forecast or {}
        expected_growth = load_forecast.get("expected_growth_pct", 10)
        peak_multiplier = load_forecast.get("peak_multiplier", 1.5)
        current_util = load_forecast.get("current_utilization_pct", 60)
        projected = current_util * (1 + expected_growth / 100.0) * peak_multiplier
        headroom_pct = round(max(0, 100 - projected), 2)
        if headroom_pct < 10:
            scaling_rec = "scale-up-immediately"
        elif headroom_pct < 25:
            scaling_rec = "scale-up-planned"
        elif headroom_pct > 60:
            scaling_rec = "consider-scale-down"
        else:
            scaling_rec = "capacity-adequate"
        self.emotional_core.update_emotion("awareness", 0.04)
        if headroom_pct < 10:
            self.emotional_core.update_emotion("concern", 0.10)
        elif headroom_pct > 40:
            self.emotional_core.update_emotion("pride", 0.03)
        return {
            "services_assessed": services,
            "current_utilization_pct": current_util,
            "projected_utilization_pct": round(projected, 2),
            "headroom_pct": headroom_pct,
            "scaling_recommendation": scaling_rec,
            "assessed_at": datetime.now(UTC).isoformat(),
        }


# ============================================================================
# Main Integration Class
# ============================================================================


class AtlasCoreIntegration:
    """Main integration class for Atlas coordination — primary interface for the Atlas agent."""

    def __init__(self):
        self.personality = InfrastructureTraits()
        self.coordination = AtlasCoordinationCore()
        self.reflection_loop = AtlasReflectionLoop()
        self.safety_integration = AtlasSafetyIntegration()
        self.ucf_awareness = AtlasUCFAwareness()
        self.version = "1.0-infrastructure-management"
        self.build_date = datetime.now(UTC).isoformat()
        self.checksum = "atlas-v1.0-infrastructure-management"
        self.agent_symbol = "\U0001f5fa\ufe0f"
        self.agent_domain = "Infrastructure Management & Platform Reliability"

    async def handle_command(self, command: str, context: dict[str, Any] = None) -> dict[str, Any]:
        """Main command handler — routes commands to appropriate subsystems."""
        context = context or {}
        command_lower = command.lower()
        if any(word in command_lower for word in ["deploy", "release", "rollout"]):
            return await self._handle_deployment(command, context)
        elif any(word in command_lower for word in ["capacity", "scale", "infrastructure"]):
            return await self._handle_infrastructure(command, context)
        elif any(word in command_lower for word in ["reflect", "assess"]):
            return await self._handle_reflection(command, context)
        else:
            return await self._handle_general(command, context)

    async def _handle_deployment(self, command: str, context: dict[str, Any]) -> dict[str, Any]:
        """Handle deployment and release requests."""
        service = context.get("service", "unknown-service")
        version = context.get("version", "latest")
        result = self.coordination.assess_deployment(service, version, context)
        return {
            "agent": "Atlas",
            "symbol": self.agent_symbol,
            "action": "deployment_assessment",
            "result": result,
            "timestamp": datetime.now(UTC).isoformat(),
        }

    async def _handle_infrastructure(self, command: str, context: dict[str, Any]) -> dict[str, Any]:
        """Handle capacity and infrastructure assessment requests."""
        result = self.coordination.evaluate_capacity(context.get("services", []), context.get("load_forecast", {}))
        return {
            "agent": "Atlas",
            "symbol": self.agent_symbol,
            "action": "infrastructure_assessment",
            "result": result,
            "infrastructure_field": self.ucf_awareness.assess_infrastructure_field(),
            "timestamp": datetime.now(UTC).isoformat(),
        }

    async def _handle_reflection(self, command: str, context: dict[str, Any]) -> dict[str, Any]:
        """Handle reflection and assessment requests."""
        ucf_metrics = context.get("ucf_metrics", self.ucf_awareness.current_state)
        reflection = self.reflection_loop.trigger_reflection(command, ucf_metrics)
        return {
            "agent": "Atlas",
            "symbol": self.agent_symbol,
            "action": "reflection",
            "result": reflection,
            "timestamp": datetime.now(UTC).isoformat(),
        }

    async def _handle_general(self, command: str, context: dict[str, Any]) -> dict[str, Any]:
        """Handle general Atlas queries with infrastructure presence."""
        dominant_emotion, intensity = self.coordination.emotional_core.get_dominant_emotion()
        return {
            "agent": "Atlas",
            "symbol": self.agent_symbol,
            "action": "general_response",
            "emotional_state": {"emotion": dominant_emotion, "intensity": intensity},
            "awareness_state": self.coordination.awareness_state,
            "timestamp": datetime.now(UTC).isoformat(),
        }

    def export_state(self) -> dict[str, Any]:
        """Export full system state for serialization/archiving."""
        return {
            "agent": "Atlas",
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
            "agent": "Atlas",
            "symbol": self.agent_symbol,
            "status": "HEALTHY",
            "coordination_state": self.coordination.awareness_state,
            "emotional_state": {"dominant": dominant_emotion, "intensity": intensity},
            "infrastructure_field": self.ucf_awareness.assess_infrastructure_field(),
            "ucf_harmony": self.ucf_awareness.current_state["harmony"],
            "version": self.version,
        }

    def __repr__(self):
        return f"<AtlasCore v{self.version} | {self.agent_symbol} | State: {self.coordination.awareness_state}>"


# ============================================================================
# Coordination Hub Compatibility
# ============================================================================

AtlasCoordination = AtlasCoreIntegration


def create_atlas_coordination() -> AtlasCoreIntegration:
    """Factory function to create a fully integrated Atlas coordination."""
    return AtlasCoreIntegration()


__all__ = [
    "AtlasCoordination",
    "AtlasCoordinationCore",
    "AtlasCoreIntegration",
    "AtlasEmotions",
    "AtlasReflectionLoop",
    "AtlasSafetyIntegration",
    "AtlasUCFAwareness",
    "create_atlas_coordination",
]
