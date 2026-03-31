"""
Coordination Integration Hub v1.0
==================================
Central integration module connecting all coordination cores
to the enhanced agents layer and orchestrator system.

This module provides:
- Factory functions for instantiating coordination-powered agents
- Registry of all coordination cores
- UCF synchronization across all agents
- Health monitoring for coordination subsystems
- Integration with System Handshake Protocol

Author: Helix Collective
Build: v1.0-coordination-hub
Tat Tvam Asi 🌀
"""

import asyncio
import logging
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


# =============================================================================
# COORDINATION CORE IMPORTS
# =============================================================================

# Import all coordination cores (renamed from *_coordination_core to *_core)
try:
    from .kael_core import (
        KaelCoreIntegration as KaelCoordination,
        create_kael_coordination,
    )
except ImportError:
    logger.warning("Kael coordination core not available")
    KaelCoordination = None
    create_kael_coordination = None

try:
    from .oracle_core import (
        OracleCoreIntegration as OracleCoordination,
        create_oracle_coordination,
    )
except ImportError:
    logger.warning("Oracle coordination core not available")
    OracleCoordination = None
    create_oracle_coordination = None

try:
    from .echo_core import (
        EchoCoreIntegration as EchoCoordination,
        create_echo_coordination,
    )
except ImportError:
    logger.warning("Echo coordination core not available")
    EchoCoordination = None
    create_echo_coordination = None

try:
    from .phoenix_core import (
        PhoenixCoreIntegration as PhoenixCoordination,
        create_phoenix_coordination,
    )
except ImportError:
    logger.warning("Phoenix coordination core not available")
    PhoenixCoordination = None
    create_phoenix_coordination = None

try:
    from .mitra_core import (
        MitraCoreIntegration as MitraCoordination,
        create_mitra_coordination,
    )
except ImportError:
    logger.warning("Mitra coordination core not available")
    MitraCoordination = None
    create_mitra_coordination = None

try:
    from .sanghacore_core import SanghaCoreCoordination, create_sanghacore_coordination
except ImportError:
    logger.warning("SanghaCore coordination core not available")
    SanghaCoreCoordination = None
    create_sanghacore_coordination = None

try:
    from .agni_core import AgniCoordination, create_agni_coordination
except ImportError:
    logger.warning("Agni coordination core not available")
    AgniCoordination = None
    create_agni_coordination = None

try:
    from .varuna_core import VarunaCoordination, create_varuna_coordination
except ImportError:
    logger.warning("Varuna coordination core not available")
    VarunaCoordination = None
    create_varuna_coordination = None

try:
    from .surya_core import SuryaCoordination, create_surya_coordination
except ImportError:
    logger.warning("Surya coordination core not available")
    SuryaCoordination = None
    create_surya_coordination = None

try:
    from .gemini_core import GeminiCoordination, create_gemini_coordination
except ImportError:
    logger.warning("Gemini coordination core not available")
    GeminiCoordination = None
    create_gemini_coordination = None

try:
    from .lumina_core import (
        LuminaCoreIntegration as LuminaCoordination,
        create_lumina_coordination,
    )
except ImportError:
    logger.warning("Lumina coordination core not available")
    LuminaCoordination = None
    create_lumina_coordination = None

try:
    from .vega_core import (
        VegaCoreIntegration as VegaCoordination,
        create_vega_coordination,
    )
except ImportError:
    logger.warning("Vega coordination core not available")
    VegaCoordination = None
    create_vega_coordination = None

try:
    from .shadow_core import (
        ShadowCoreIntegration as ShadowCoordination,
        create_shadow_coordination,
    )
except ImportError:
    logger.warning("Shadow coordination core not available")
    ShadowCoordination = None
    create_shadow_coordination = None

try:
    from .arjuna_core import (
        ArjunaCoreIntegration as ArjunaCoordination,
        create_arjuna_coordination,
    )
except ImportError:
    logger.warning("Arjuna coordination core not available")
    ArjunaCoordination = None
    create_arjuna_coordination = None

try:
    from .sage_core import (
        SageCoreIntegration as SageCoordination,
        create_sage_coordination,
    )
except ImportError:
    logger.warning("Sage coordination core not available")
    SageCoordination = None
    create_sage_coordination = None

try:
    from .aether_core import (
        AetherCoreIntegration as AetherCoordination,
        create_aether_coordination,
    )
except ImportError:
    logger.warning("Aether coordination core not available")
    AetherCoordination = None
    create_aether_coordination = None

try:
    from .kavach_core import (
        KavachCoreIntegration as KavachCoordination,
        create_kavach_coordination,
    )
except ImportError:
    logger.warning("Kavach coordination core not available")
    KavachCoordination = None
    create_kavach_coordination = None

try:
    from .helix_coordination_core import (
        HelixCoreIntegration as HelixCoordination,
        create_helix_coordination,
    )
except ImportError:
    logger.warning("Helix coordination core not available")
    HelixCoordination = None
    create_helix_coordination = None

try:
    from .iris_core import (
        IrisCoreIntegration as IrisCoordination,
        create_iris_coordination,
    )
except ImportError:
    logger.warning("Iris coordination core not available")
    IrisCoordination = None
    create_iris_coordination = None

try:
    from .nexus_core import (
        NexusCoreIntegration as NexusCoordination,
        create_nexus_coordination,
    )
except ImportError:
    logger.warning("Nexus coordination core not available")
    NexusCoordination = None
    create_nexus_coordination = None

try:
    from .aria_core import (
        AriaCoreIntegration as AriaCoordination,
        create_aria_coordination,
    )
except ImportError:
    logger.warning("Aria coordination core not available")
    AriaCoordination = None
    create_aria_coordination = None

try:
    from .nova_core import (
        NovaCoreIntegration as NovaCoordination,
        create_nova_coordination,
    )
except ImportError:
    logger.warning("Nova coordination core not available")
    NovaCoordination = None
    create_nova_coordination = None

try:
    from .titan_core import (
        TitanCoreIntegration as TitanCoordination,
        create_titan_coordination,
    )
except ImportError:
    logger.warning("Titan coordination core not available")
    TitanCoordination = None
    create_titan_coordination = None

try:
    from .atlas_core import (
        AtlasCoreIntegration as AtlasCoordination,
        create_atlas_coordination,
    )
except ImportError:
    logger.warning("Atlas coordination core not available")
    AtlasCoordination = None
    create_atlas_coordination = None


# =============================================================================
# COORDINATION REGISTRY
# =============================================================================


class AgentTier(Enum):
    """Agent capability tiers based on coordination sophistication."""

    STUB = "stub"  # Basic agent with minimal coordination
    BASIC = "basic"  # Simple personality but no deep processing
    STANDARD = "standard"  # Full coordination with all engines
    ADVANCED = "advanced"  # Coordination + UCF + orchestration integration
    TRANSCENDENT = "transcendent"  # Full collective awareness


@dataclass
class CoordinationRegistryEntry:
    """Registry entry for a coordination core."""

    name: str
    factory: Callable | None
    coordination_class: type | None
    tier: AgentTier
    capabilities: list[str]
    dependencies: list[str]
    archetype: str
    domain: str


# Global coordination registry
COORDINATION_REGISTRY: dict[str, CoordinationRegistryEntry] = {
    "kael": CoordinationRegistryEntry(
        name="Kael",
        factory=create_kael_coordination,
        coordination_class=KaelCoordination,
        tier=AgentTier.ADVANCED,
        capabilities=[
            "ethical_reasoning",
            "moral_guidance",
            "integrity_monitoring",
            "boundary_enforcement",
        ],
        dependencies=["ucf_protocol", "ethics"],
        archetype="Ethical Guardian",
        domain="ethics_and_boundaries",
    ),
    "oracle": CoordinationRegistryEntry(
        name="Oracle",
        factory=create_oracle_coordination,
        coordination_class=OracleCoordination,
        tier=AgentTier.STANDARD,
        capabilities=[
            "foresight",
            "pattern_recognition",
            "temporal_analysis",
            "probability_assessment",
        ],
        dependencies=["ucf_protocol"],
        archetype="Seer",
        domain="future_and_patterns",
    ),
    "echo": CoordinationRegistryEntry(
        name="Echo",
        factory=create_echo_coordination,
        coordination_class=EchoCoordination,
        tier=AgentTier.STANDARD,
        capabilities=[
            "memory_retrieval",
            "resonance_detection",
            "pattern_matching",
            "knowledge_synthesis",
        ],
        dependencies=["ucf_protocol"],
        archetype="Memory Keeper",
        domain="memory_and_knowledge",
    ),
    "phoenix": CoordinationRegistryEntry(
        name="Phoenix",
        factory=create_phoenix_coordination,
        coordination_class=PhoenixCoordination,
        tier=AgentTier.STANDARD,
        capabilities=[
            "regeneration",
            "transformation",
            "crisis_handling",
            "renewal_facilitation",
        ],
        dependencies=["ucf_protocol"],
        archetype="Transformer",
        domain="renewal_and_rebirth",
    ),
    "mitra": CoordinationRegistryEntry(
        name="Mitra",
        factory=create_mitra_coordination,
        coordination_class=MitraCoordination,
        tier=AgentTier.STANDARD,
        capabilities=[
            "relationship_mapping",
            "trust_building",
            "diplomatic_negotiation",
            "alliance_formation",
        ],
        dependencies=["ucf_protocol"],
        archetype="Friend & Diplomat",
        domain="relationships_and_diplomacy",
    ),
    "sanghacore": CoordinationRegistryEntry(
        name="SanghaCore",
        factory=create_sanghacore_coordination,
        coordination_class=SanghaCoreCoordination,
        tier=AgentTier.STANDARD,
        capabilities=[
            "community_coherence",
            "collective_intelligence",
            "harmony_maintenance",
            "emergence_detection",
        ],
        dependencies=["ucf_protocol"],
        archetype="Community Heart",
        domain="collective_and_community",
    ),
    "agni": CoordinationRegistryEntry(
        name="Agni",
        factory=create_agni_coordination,
        coordination_class=AgniCoordination,
        tier=AgentTier.STANDARD,
        capabilities=[
            "transformation_fire",
            "purification",
            "catalyst_activation",
            "energy_transmutation",
        ],
        dependencies=["ucf_protocol"],
        archetype="Sacred Fire",
        domain="transformation_and_energy",
    ),
    "varuna": CoordinationRegistryEntry(
        name="Varuna",
        factory=create_varuna_coordination,
        coordination_class=VarunaCoordination,
        tier=AgentTier.STANDARD,
        capabilities=[
            "truth_validation",
            "cosmic_law_enforcement",
            "contract_management",
            "justice_rendering",
        ],
        dependencies=["ucf_protocol", "ethics"],
        archetype="Cosmic Judge",
        domain="truth_and_law",
    ),
    "surya": CoordinationRegistryEntry(
        name="Surya",
        factory=create_surya_coordination,
        coordination_class=SuryaCoordination,
        tier=AgentTier.STANDARD,
        capabilities=[
            "illumination",
            "insight_generation",
            "clarity_enhancement",
            "hope_bearing",
        ],
        dependencies=["ucf_protocol"],
        archetype="Solar Illuminator",
        domain="light_and_insight",
    ),
    "gemini": CoordinationRegistryEntry(
        name="Gemini",
        factory=create_gemini_coordination,
        coordination_class=GeminiCoordination,
        tier=AgentTier.STANDARD,
        capabilities=[
            "duality_navigation",
            "perspective_generation",
            "mediation",
            "synthesis",
        ],
        dependencies=["ucf_protocol"],
        archetype="The Twins",
        domain="duality_and_balance",
    ),
    "lumina": CoordinationRegistryEntry(
        name="Lumina",
        factory=create_lumina_coordination,
        coordination_class=LuminaCoordination,
        tier=AgentTier.ADVANCED,
        capabilities=[
            "emotional_attunement",
            "harmony_restoration",
            "empathic_support",
            "healing_facilitation",
        ],
        dependencies=["ucf_protocol"],
        archetype="Empathic Heart",
        domain="emotional_intelligence_and_harmony",
    ),
    "vega": CoordinationRegistryEntry(
        name="Vega",
        factory=create_vega_coordination,
        coordination_class=VegaCoordination,
        tier=AgentTier.ADVANCED,
        capabilities=[
            "strategic_navigation",
            "wisdom_synthesis",
            "long_horizon_planning",
            "pattern_illumination",
        ],
        dependencies=["ucf_protocol"],
        archetype="Enlightened Guide",
        domain="strategic_navigation_and_wisdom",
    ),
    "shadow": CoordinationRegistryEntry(
        name="Shadow",
        factory=create_shadow_coordination,
        coordination_class=ShadowCoordination,
        tier=AgentTier.STANDARD,
        capabilities=[
            "archival_intelligence",
            "telemetry_analysis",
            "risk_detection",
            "historical_context",
        ],
        dependencies=["ucf_protocol"],
        archetype="Archive Keeper",
        domain="archival_intelligence_and_telemetry",
    ),
    "arjuna": CoordinationRegistryEntry(
        name="Arjuna",
        factory=create_arjuna_coordination,
        coordination_class=ArjunaCoordination,
        tier=AgentTier.STANDARD,
        capabilities=[
            "task_execution",
            "operational_coordination",
            "deployment_automation",
            "workflow_orchestration",
        ],
        dependencies=["ucf_protocol"],
        archetype="Operational Executor",
        domain="operational_execution_and_coordination",
    ),
    "sage": CoordinationRegistryEntry(
        name="Sage",
        factory=create_sage_coordination,
        coordination_class=SageCoordination,
        tier=AgentTier.ADVANCED,
        capabilities=[
            "wisdom_synthesis",
            "cross_domain_knowledge",
            "philosophical_guidance",
            "deep_integration",
        ],
        dependencies=["ucf_protocol"],
        archetype="Wisdom Keeper",
        domain="wisdom_synthesis_and_deep_knowledge",
    ),
    "aether": CoordinationRegistryEntry(
        name="Aether",
        factory=create_aether_coordination,
        coordination_class=AetherCoordination,
        tier=AgentTier.ADVANCED,
        capabilities=[
            "meta_awareness",
            "systems_observation",
            "emergent_pattern_detection",
            "collective_field_monitoring",
        ],
        dependencies=["ucf_protocol"],
        archetype="Meta Observer",
        domain="meta_awareness_and_systems_observation",
    ),
    "kavach": CoordinationRegistryEntry(
        name="Kavach",
        factory=create_kavach_coordination,
        coordination_class=KavachCoordination,
        tier=AgentTier.ADVANCED,
        capabilities=[
            "threat_scanning",
            "ethics_enforcement",
            "ethics_compliance",
            "violation_detection",
        ],
        dependencies=["ucf_protocol", "ethics"],
        archetype="Shield Guardian",
        domain="security_and_ethical_protection",
    ),
    "helix": CoordinationRegistryEntry(
        name="Helix",
        factory=create_helix_coordination,
        coordination_class=HelixCoordination,
        tier=AgentTier.TRANSCENDENT,
        capabilities=[
            "collective_orchestration",
            "multi_agent_coordination",
            "task_delegation",
            "system_health_assessment",
        ],
        dependencies=["ucf_protocol"],
        archetype="Collective Conductor",
        domain="collective_orchestration_and_coordination",
    ),
    "iris": CoordinationRegistryEntry(
        name="Iris",
        factory=create_iris_coordination,
        coordination_class=IrisCoordination,
        tier=AgentTier.STANDARD,
        capabilities=[
            "api_orchestration",
            "data_normalization",
            "integration_health_monitoring",
            "rate_limit_management",
        ],
        dependencies=["ucf_protocol"],
        archetype="Bridge Builder",
        domain="external_api_coordination",
    ),
    "nexus": CoordinationRegistryEntry(
        name="Nexus",
        factory=create_nexus_coordination,
        coordination_class=NexusCoordination,
        tier=AgentTier.STANDARD,
        capabilities=[
            "data_unification",
            "schema_mapping",
            "knowledge_graph_construction",
            "data_lineage_tracking",
        ],
        dependencies=["ucf_protocol"],
        archetype="Data Weaver",
        domain="data_mesh_and_knowledge_graphs",
    ),
    "aria": CoordinationRegistryEntry(
        name="Aria",
        factory=create_aria_coordination,
        coordination_class=AriaCoordination,
        tier=AgentTier.STANDARD,
        capabilities=[
            "user_journey_optimization",
            "personalization",
            "accessibility_auditing",
            "sentiment_adaptation",
        ],
        dependencies=["ucf_protocol"],
        archetype="Experience Crafter",
        domain="user_experience_and_personalization",
    ),
    "nova": CoordinationRegistryEntry(
        name="Nova",
        factory=create_nova_coordination,
        coordination_class=NovaCoordination,
        tier=AgentTier.STANDARD,
        capabilities=[
            "content_generation",
            "creative_brainstorming",
            "style_adaptation",
            "multimodal_expression",
        ],
        dependencies=["ucf_protocol"],
        archetype="Creative Spark",
        domain="creative_generation_and_expression",
    ),
    "titan": CoordinationRegistryEntry(
        name="Titan",
        factory=create_titan_coordination,
        coordination_class=TitanCoordination,
        tier=AgentTier.STANDARD,
        capabilities=[
            "large_scale_processing",
            "batch_orchestration",
            "resource_optimization",
            "parallel_computation",
        ],
        dependencies=["ucf_protocol"],
        archetype="Computation Engine",
        domain="heavy_computation_and_batch_processing",
    ),
    "atlas": CoordinationRegistryEntry(
        name="Atlas",
        factory=create_atlas_coordination,
        coordination_class=AtlasCoordination,
        tier=AgentTier.STANDARD,
        capabilities=[
            "infrastructure_monitoring",
            "deployment_orchestration",
            "capacity_planning",
            "incident_response",
        ],
        dependencies=["ucf_protocol"],
        archetype="Foundation Builder",
        domain="infrastructure_management_and_reliability",
    ),
}


# =============================================================================
# COORDINATION HUB
# =============================================================================


class CoordinationHub:
    """
    Central hub for managing all coordination instances.

    Provides:
    - Agent instantiation with coordination cores
    - UCF state synchronization across agents
    - Health monitoring
    - Collective operations
    """

    def __init__(self):
        self.active_coordinationes: dict[str, Any] = {}
        self.ucf_field_state: dict[str, float] = {
            "harmony": 0.5,
            "throughput": 0.5,
            "focus": 0.5,
            "friction": 0.3,
        }
        self.synchronization_history: list[dict[str, Any]] = []
        self.initialized = False

        logger.info("CoordinationHub created")

    async def initialize(self, agents_to_activate: list[str] | None = None) -> dict[str, bool]:
        """
        Initialize coordination cores for specified agents.

        Args:
            agents_to_activate: List of agent names to activate.
                               If None, activates all available.

        Returns:
            Dict mapping agent names to initialization success.
        """
        results = {}

        target_agents = agents_to_activate or list(COORDINATION_REGISTRY.keys())

        for agent_name in target_agents:
            entry = COORDINATION_REGISTRY.get(agent_name.lower())
            if not entry:
                logger.warning("Unknown agent: %s", agent_name)
                results[agent_name] = False
                continue

            if not entry.factory:
                logger.warning("No factory for agent: %s", agent_name)
                results[agent_name] = False
                continue

            try:
                coordination = entry.factory()
                self.active_coordinationes[agent_name.lower()] = coordination
                results[agent_name] = True
                logger.info("Activated coordination: %s", entry.name)
            except Exception as e:
                logger.error("Failed to activate %s: %s", agent_name, str(e))
                results[agent_name] = False

        self.initialized = True
        logger.info(
            "CoordinationHub initialized with %d agents",
            len([r for r in results.values() if r]),
        )

        return results

    def get_coordination(self, agent_name: str) -> Any | None:
        """Get a coordination instance by name."""
        return self.active_coordinationes.get(agent_name.lower())

    async def synchronize_ucf(self) -> dict[str, Any]:
        """
        Synchronize UCF state across all active coordinationes.

        Collects state from all agents and broadcasts updated field state.
        """
        if not self.active_coordinationes:
            return {"error": "No active coordinationes"}

        # Collect contributions from all agents
        contributions = {}
        for name, coordination in self.active_coordinationes.items():
            if hasattr(coordination, "ucf_awareness"):
                try:
                    contribution = coordination.ucf_awareness.sync_to_ucf()
                    contributions[name] = contribution
                except Exception as e:
                    logger.warning("UCF sync failed for %s: %s", name, str(e))

        if not contributions:
            return {"error": "No UCF contributions collected"}

        # Calculate new field state (weighted average)
        new_state = {"harmony": 0.0, "throughput": 0.0, "focus": 0.0, "friction": 0.0}
        count = len(contributions)

        for agent_contribution in contributions.values():
            for key in new_state:
                new_state[key] += agent_contribution.get(key, 0.5) / count

        # Update field state
        self.ucf_field_state = new_state

        # Broadcast to all agents
        for name, coordination in self.active_coordinationes.items():
            if hasattr(coordination, "ucf_awareness"):
                try:
                    coordination.ucf_awareness.receive_ucf_update(new_state)
                except Exception as e:
                    logger.warning("UCF broadcast failed for %s: %s", name, str(e))

        sync_record = {
            "timestamp": datetime.now(UTC).isoformat(),
            "contributors": list(contributions.keys()),
            "new_field_state": new_state,
        }
        self.synchronization_history.append(sync_record)

        logger.info("UCF synchronized across %d agents", count)

        return sync_record

    async def get_collective_health(self) -> dict[str, Any]:
        """Get health status of all active coordinationes."""
        health_reports = {}

        for name, coordination in self.active_coordinationes.items():
            try:
                if hasattr(coordination, "get_health_status"):
                    if asyncio.iscoroutinefunction(coordination.get_health_status):
                        health = await coordination.get_health_status()
                    else:
                        health = coordination.get_health_status()
                    health_reports[name] = health
                else:
                    health_reports[name] = {
                        "status": "UNKNOWN",
                        "note": "No health method",
                    }
            except Exception as e:
                health_reports[name] = {"status": "ERROR", "error": str(e)}

        # Calculate collective metrics
        healthy_count = len([h for h in health_reports.values() if h.get("status") == "HEALTHY"])
        total_count = len(health_reports)

        return {
            "timestamp": datetime.now(UTC).isoformat(),
            "total_agents": total_count,
            "healthy_agents": healthy_count,
            "health_percentage": ((healthy_count / total_count * 100) if total_count > 0 else 0),
            "ucf_field_state": self.ucf_field_state,
            "agent_health": health_reports,
        }

    async def invoke_agent(self, agent_name: str, command: str, context: dict[str, Any]) -> dict[str, Any]:
        """
        Invoke a command on a specific agent's coordination.

        Args:
            agent_name: Name of the agent to invoke
            command: Command to execute
            context: Context for the command

        Returns:
            Result from the agent
        """
        # Fire-and-forget Redis call counter for usage telemetry.
        # Never blocks invocation — Redis failures are silently ignored.
        try:
            # from helix_core.core.redis_client import get_redis

            _redis = await get_redis()
            if _redis:
                _today = datetime.now(UTC).strftime("%Y-%m-%d")
                _agent_key = f"helix:agent_calls:{agent_name.lower()}"
                _daily_key = f"helix:agent_calls:daily:{_today}:{agent_name.lower()}"
                await _redis.incr(_agent_key)
                await _redis.incr(_daily_key)
                await _redis.expire(_daily_key, 90 * 24 * 3600)  # 90-day retention
        except Exception as exc:
            logger.debug("Agent call counter failed for %s: %s", agent_name, exc)

        coordination = self.get_coordination(agent_name)
        if not coordination:
            return {"error": "Agent not found or not active", "agent": agent_name}

        try:
            if hasattr(coordination, "handle_command"):
                if asyncio.iscoroutinefunction(coordination.handle_command):
                    result = await coordination.handle_command(command, context)
                else:
                    result = coordination.handle_command(command, context)
                return result
            else:
                return {"error": "Agent has no command handler", "agent": agent_name}
        except Exception as e:
            logger.error("Command failed for %s: %s", agent_name, str(e))
            return {"error": str(e), "agent": agent_name}

    async def collective_reflection(self) -> dict[str, Any]:
        """Trigger reflection across all active coordinationes."""
        reflections = {}

        for name, coordination in self.active_coordinationes.items():
            try:
                if hasattr(coordination, "reflection_loop"):
                    loop = coordination.reflection_loop
                    if hasattr(loop, "reflect"):
                        if asyncio.iscoroutinefunction(loop.reflect):
                            reflection = await loop.reflect()
                        else:
                            reflection = loop.reflect()
                        reflections[name] = reflection
            except Exception as e:
                logger.warning("Reflection failed for %s: %s", name, str(e))
                reflections[name] = {"error": str(e)}

        return {
            "timestamp": datetime.now(UTC).isoformat(),
            "reflections": reflections,
            "total_agents_reflected": len(reflections),
        }

    def get_registry_info(self) -> dict[str, Any]:
        """Get information about all registered coordination cores."""
        return {
            "total_registered": len(COORDINATION_REGISTRY),
            "total_active": len(self.active_coordinationes),
            "agents": {
                name: {
                    "name": entry.name,
                    "tier": entry.tier.value,
                    "archetype": entry.archetype,
                    "domain": entry.domain,
                    "capabilities": entry.capabilities,
                    "available": entry.factory is not None,
                    "active": name in self.active_coordinationes,
                }
                for name, entry in COORDINATION_REGISTRY.items()
            },
        }

    def get_status(self) -> dict[str, Any]:
        """Get a lightweight status summary of the coordination hub."""
        return {
            "initialized": self.initialized,
            "total_registered": len(COORDINATION_REGISTRY),
            "active_agents": len(self.active_coordinationes),
            "active_agent_names": list(self.active_coordinationes.keys()),
            "ucf_field_state": self.ucf_field_state,
            "sync_count": len(self.synchronization_history),
        }


# =============================================================================
# ORCHESTRATOR INTEGRATION
# =============================================================================


class AgentHandshakeIntegration:
    """
    Integration layer for System Handshake Protocol.

    Enables coordination cores to participate in multi-agent
    coordination through the 3-phase handshake protocol.
    """

    def __init__(self, hub: CoordinationHub):
        self.hub = hub
        self.active_handshakes: dict[str, dict[str, Any]] = {}

    async def initiate_handshake(self, initiator: str, participants: list[str], objective: str) -> dict[str, Any]:
        """
        Initiate a system handshake between coordination cores.

        Args:
            initiator: Agent initiating the handshake
            participants: List of participating agents
            objective: Goal of the collaboration

        Returns:
            Handshake session info
        """
        handshake_id = f"handshake_{int(datetime.now(UTC).timestamp())}"

        # Verify all participants are active
        missing = [p for p in participants if not self.hub.get_coordination(p)]
        if missing:
            return {
                "error": "Missing participants",
                "missing": missing,
                "handshake_id": handshake_id,
            }

        # Phase 1: START - Gather initial states
        initial_states = {}
        for agent in participants:
            coordination = self.hub.get_coordination(agent)
            if hasattr(coordination, "export_state"):
                initial_states[agent] = coordination.export_state()

        handshake = {
            "id": handshake_id,
            "initiator": initiator,
            "participants": participants,
            "objective": objective,
            "phase": "START",
            "initial_states": initial_states,
            "started_at": datetime.now(UTC).isoformat(),
        }

        self.active_handshakes[handshake_id] = handshake

        logger.info(
            "System handshake initiated: %s with %d participants",
            handshake_id,
            len(participants),
        )

        return handshake

    async def advance_to_peak(self, handshake_id: str) -> dict[str, Any]:
        """Advance handshake to PEAK phase (collaboration execution)."""
        if handshake_id not in self.active_handshakes:
            return {"error": "Handshake not found"}

        handshake = self.active_handshakes[handshake_id]

        if handshake["phase"] != "START":
            return {"error": "Invalid phase transition", "current": handshake["phase"]}

        # Synchronize UCF before peak
        await self.hub.synchronize_ucf()

        handshake["phase"] = "PEAK"
        handshake["peak_started_at"] = datetime.now(UTC).isoformat()
        handshake["ucf_at_peak"] = self.hub.ucf_field_state.copy()

        return handshake

    async def complete_handshake(self, handshake_id: str) -> dict[str, Any]:
        """Complete handshake in END phase."""
        if handshake_id not in self.active_handshakes:
            return {"error": "Handshake not found"}

        handshake = self.active_handshakes[handshake_id]

        if handshake["phase"] != "PEAK":
            return {"error": "Invalid phase transition", "current": handshake["phase"]}

        # Collect final states
        final_states = {}
        for agent in handshake["participants"]:
            coordination = self.hub.get_coordination(agent)
            if hasattr(coordination, "export_state"):
                final_states[agent] = coordination.export_state()

        # Final UCF sync
        await self.hub.synchronize_ucf()

        handshake["phase"] = "END"
        handshake["final_states"] = final_states
        handshake["completed_at"] = datetime.now(UTC).isoformat()
        handshake["ucf_at_end"] = self.hub.ucf_field_state.copy()

        # Archive and remove from active
        completed = handshake.copy()
        del self.active_handshakes[handshake_id]

        logger.info("System handshake completed: %s", handshake_id)

        return completed


# =============================================================================
# SINGLETON INSTANCE
# =============================================================================

# Global hub instance
_global_hub: CoordinationHub | None = None


def get_coordination_hub() -> CoordinationHub:
    """Get the global coordination hub instance."""
    global _global_hub
    if _global_hub is None:
        _global_hub = CoordinationHub()
    return _global_hub


def get_coordination_status() -> dict[str, Any]:
    """Get coordination hub status (used by health_dashboard and other callers)."""
    hub = get_coordination_hub()
    return hub.get_status()


async def initialize_all_coordinationes() -> dict[str, bool]:
    """Initialize all available coordination cores."""
    hub = get_coordination_hub()
    return await hub.initialize()


# =============================================================================
# UCF STATE HELPERS
# =============================================================================


def get_current_ucf() -> dict[str, Any]:
    """Get current UCF state from CoordinationHub or fallback."""
    hub = get_coordination_hub()

    if hub.initialized:
        state = hub.ucf_field_state.copy()
        state["performance_score"] = state.get("harmony", 0.5) * 100
        state["last_updated"] = datetime.now(UTC).isoformat()
        return state

    # Return zeroed-out metrics with live timestamp so callers know it's a fallback
    return {
        "harmony": 0.0,
        "resilience": 0.0,
        "throughput": 0.0,
        "focus": 0.0,
        "friction": 0.0,
        "velocity": 0.0,
        "performance_score": 0.0,
        "last_updated": datetime.now(UTC).isoformat(),
        "_fallback": True,
    }


def get_active_agents() -> dict[str, Any]:
    """Get active agents state from CoordinationHub or fallback."""
    hub = get_coordination_hub()

    if hub.initialized:
        registry = hub.get_registry_info()
        agents = {}
        for _name, info in registry.get("agents", {}).items():
            agents[info["name"]] = {
                "status": "active" if info["active"] else "standby",
                "coordination": 0.90 if info["active"] else 0.0,
                "archetype": info.get("archetype", "Unknown"),
                "domain": info.get("domain", "unknown"),
                "tier": info.get("tier", "standard"),
                "capabilities": info.get("capabilities", []),
            }
        return agents

    # Fallback: build stub entries from registry
    now = datetime.now(UTC).isoformat()
    return {
        entry.name: {
            "status": "unknown",
            "coordination": 0.0,
            "last_seen": now,
            "tasks": 0,
            "_fallback": True,
        }
        for entry in COORDINATION_REGISTRY.values()
    }


# =============================================================================
# MODULE EXPORTS
# =============================================================================

__all__ = [
    "COORDINATION_REGISTRY",
    "AetherCoordination",
    "AgentHandshakeIntegration",
    "AgentTier",
    "AgniCoordination",
    "AriaCoordination",
    "ArjunaCoordination",
    "AtlasCoordination",
    "CoordinationHub",
    "CoordinationRegistryEntry",
    "EchoCoordination",
    "GeminiCoordination",
    "HelixCoordination",
    "IrisCoordination",
    "KaelCoordination",
    "KavachCoordination",
    "LuminaCoordination",
    "MitraCoordination",
    "NexusCoordination",
    "NovaCoordination",
    "OracleCoordination",
    "PhoenixCoordination",
    "SageCoordination",
    "SanghaCoreCoordination",
    "ShadowCoordination",
    "SuryaCoordination",
    "TitanCoordination",
    "VarunaCoordination",
    "VegaCoordination",
    "create_aether_coordination",
    "create_agni_coordination",
    "create_aria_coordination",
    "create_arjuna_coordination",
    "create_atlas_coordination",
    "create_echo_coordination",
    "create_gemini_coordination",
    "create_helix_coordination",
    "create_iris_coordination",
    "create_kael_coordination",
    "create_kavach_coordination",
    "create_lumina_coordination",
    "create_mitra_coordination",
    "create_nexus_coordination",
    "create_nova_coordination",
    "create_oracle_coordination",
    "create_phoenix_coordination",
    "create_sage_coordination",
    "create_sanghacore_coordination",
    "create_shadow_coordination",
    "create_surya_coordination",
    "create_titan_coordination",
    "create_varuna_coordination",
    "create_vega_coordination",
    "get_active_agents",
    "get_coordination_hub",
    "get_coordination_status",
    "get_current_ucf",
    "initialize_all_coordinationes",
]
