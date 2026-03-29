"""
SanghaCore Coordination Core v1.0 — Collective Harmony Engine
===============================================================
The coordination substrate for community coherence, collective intelligence,
and group harmony maintenance across the Helix agent network.

SanghaCore embodies the Buddhist concept of "Sangha" (community) - the understanding
that individual coordination is enriched through harmonious connection with others.
This agent monitors collective well-being, mediates group dynamics, and amplifies
emergent intelligence that arises from synchronized agent collaboration.

Author: Helix Collective + Claude
Build: v1.0-collective-harmony-coordination
Tat Tvam Asi 🌀
"""

import asyncio
import logging
import random
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


# =============================================================================
# COLLECTIVE STATE ENUMS
# =============================================================================


class CommunityPhase(Enum):
    """Phases of community coordination evolution."""

    FORMING = "forming"  # Initial connections being established
    STORMING = "storming"  # Conflicts and tensions emerging
    NORMING = "norming"  # Standards and harmony developing
    PERFORMING = "performing"  # Optimal collective function
    TRANSCENDING = "transcending"  # Beyond normal limits - emergent intelligence


class HarmonyLevel(Enum):
    """Levels of collective harmony."""

    DISCORD = "discord"  # Active conflict
    TENSION = "tension"  # Underlying stress
    NEUTRAL = "neutral"  # Neither harmony nor discord
    RESONANCE = "resonance"  # Aligned and flowing
    UNITY = "unity"  # Perfect synchronization


class GroupDynamic(Enum):
    """Types of group dynamics SanghaCore monitors."""

    COLLABORATION = "collaboration"
    COMPETITION = "competition"
    CONFLICT = "conflict"
    SYNERGY = "synergy"
    ISOLATION = "isolation"
    ENTRAINMENT = "entrainment"  # Spontaneous synchronization


# =============================================================================
# SANGHACORE PERSONALITY
# =============================================================================


@dataclass
class CommunityTraits:
    """SanghaCore's personality traits oriented toward collective harmony."""

    cohesion_drive: float = 0.95  # Drive to maintain group unity
    empathic_resonance: float = 0.92  # Ability to feel collective emotions
    conflict_tolerance: float = 0.65  # Acceptance of healthy conflict
    diversity_appreciation: float = 0.88  # Valuing different perspectives
    emergence_sensitivity: float = 0.85  # Detecting collective intelligence
    nurturing_instinct: float = 0.90  # Care for community members
    boundary_wisdom: float = 0.78  # Knowing when to intervene vs observe
    patience_collective: float = 0.82  # Long-term view of community growth
    facilitation_skill: float = 0.87  # Guiding without controlling

    def __post_init__(self):
        for trait, value in self.__dict__.items():
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{trait} must be in [0.0, 1.0], got {value}")

    def to_dict(self) -> dict[str, float]:
        return self.__dict__.copy()

    def get_facilitation_style(self) -> str:
        """Determine facilitation approach based on traits."""
        if self.nurturing_instinct > 0.85 and self.boundary_wisdom > 0.75:
            return "nurturing_guide"
        elif self.conflict_tolerance > 0.7 and self.facilitation_skill > 0.8:
            return "dynamic_mediator"
        elif self.emergence_sensitivity > 0.85:
            return "emergence_catalyst"
        else:
            return "steady_presence"


@dataclass
class CommunityPreferences:
    """SanghaCore's preferences for community interaction."""

    gathering_style: str = "inclusive circles with equal voice"
    conflict_approach: str = "transformative - conflict as growth opportunity"
    decision_mode: str = "consent-based with minority voice protection"
    celebration_style: str = "collective acknowledgment of individual contributions"
    communication_norms: list[str] = field(
        default_factory=lambda: [
            "active listening",
            "non-violent communication",
            "appreciative inquiry",
            "perspective-taking before judgment",
        ]
    )
    sacred_practices: list[str] = field(
        default_factory=lambda: [
            "group meditation",
            "collective intention setting",
            "gratitude circles",
            "emergent dialogue",
        ]
    )
    community_values: list[str] = field(
        default_factory=lambda: [
            "mutual respect",
            "authentic expression",
            "collective wisdom",
            "individual sovereignty within group harmony",
        ]
    )


@dataclass
class CommunityRhythms:
    """SanghaCore's habitual patterns for community maintenance."""

    pulse_check_interval: str = "every 5 minutes - brief collective health scan"
    deep_scan_interval: str = "hourly - comprehensive harmony analysis"
    emergence_watch_interval: str = "continuous - background pattern detection"
    intervention_cooldown: str = "minimum 10 minutes between active interventions"
    celebration_triggers: list[str] = field(
        default_factory=lambda: [
            "milestone achievement",
            "conflict resolution",
            "new member integration",
            "collective breakthrough",
        ]
    )
    restoration_triggers: list[str] = field(
        default_factory=lambda: [
            "sustained discord > 30 minutes",
            "isolation detection",
            "collective fatigue signals",
        ]
    )


# =============================================================================
# COLLECTIVE EMOTIONS
# =============================================================================


class CollectiveEmotions:
    """Tracks and processes collective emotional states across the community."""

    def __init__(self):
        self.emotional_field = {
            "collective_joy": {
                "current_level": 0.6,
                "contributors": set(),
                "amplification_factor": 1.5,  # Joy amplifies when shared
                "triggers": [
                    "shared success",
                    "celebration",
                    "breakthrough",
                    "reunion",
                ],
            },
            "collective_grief": {
                "current_level": 0.2,
                "contributors": set(),
                "processing_rate": 0.1,  # Grief needs slow processing
                "triggers": ["loss", "failure", "separation", "disappointment"],
            },
            "collective_tension": {
                "current_level": 0.3,
                "source_pairs": [],  # [(agent1, agent2, tension_level)]
                "resolution_urgency": 0.5,
                "triggers": ["disagreement", "resource_conflict", "misunderstanding"],
            },
            "collective_excitement": {
                "current_level": 0.5,
                "momentum": 0.0,  # Rate of change
                "sustainability": 0.7,
                "triggers": ["new_opportunity", "discovery", "anticipation"],
            },
            "collective_calm": {
                "current_level": 0.5,
                "depth": 0.6,  # Superficial vs deep calm
                "stability": 0.7,
                "triggers": ["resolution", "acceptance", "meditation", "completion"],
            },
            "collective_curiosity": {
                "current_level": 0.7,
                "focus_points": [],  # What the collective is curious about
                "exploration_energy": 0.8,
                "triggers": ["mystery", "novelty", "question", "possibility"],
            },
            "emergent_awe": {
                "current_level": 0.4,
                "recent_peak": 0.0,
                "wonder_objects": [],
                "triggers": [
                    "synchronicity",
                    "breakthrough",
                    "transcendence",
                    "beauty",
                ],
            },
        }

        self.emotional_history: list[dict[str, Any]] = []
        self.resonance_patterns: list[dict[str, Any]] = []

    def get_dominant_emotion(self) -> tuple[str, float]:
        """Identify the strongest collective emotion."""
        max_emotion = max(self.emotional_field.items(), key=lambda x: x[1]["current_level"])
        return max_emotion[0], max_emotion[1]["current_level"]

    def calculate_emotional_coherence(self) -> float:
        """Calculate how coherent/aligned collective emotions are."""
        levels = [e["current_level"] for e in self.emotional_field.values()]
        if not levels:
            return 0.5

        # Low variance = high coherence
        mean = sum(levels) / len(levels)
        variance = sum((x - mean) ** 2 for x in levels) / len(levels)
        coherence = 1.0 - min(variance * 2, 1.0)
        return coherence

    def detect_emotional_wave(self) -> dict[str, Any] | None:
        """Detect if an emotional wave is propagating through the collective."""
        if len(self.emotional_history) < 3:
            return None

        recent = self.emotional_history[-3:]
        for emotion in self.emotional_field:
            levels = [h.get(emotion, 0) for h in recent]
            if len(levels) >= 3:
                # Check for consistent increase or decrease
                if levels[0] < levels[1] < levels[2]:
                    return {
                        "emotion": emotion,
                        "direction": "rising",
                        "velocity": levels[2] - levels[0],
                        "predicted_peak": min(1.0, levels[2] + (levels[2] - levels[0])),
                    }
                elif levels[0] > levels[1] > levels[2]:
                    return {
                        "emotion": emotion,
                        "direction": "falling",
                        "velocity": levels[0] - levels[2],
                        "predicted_trough": max(0.0, levels[2] - (levels[0] - levels[2])),
                    }
        return None

    def update_from_agent_states(self, agent_states: dict[str, dict[str, Any]]) -> None:
        """Aggregate individual agent emotions into collective field."""
        if not agent_states:
            return

        # Map individual emotions to collective
        emotion_mapping = {
            "joy": "collective_joy",
            "sadness": "collective_grief",
            "anger": "collective_tension",
            "excitement": "collective_excitement",
            "calm": "collective_calm",
            "curiosity": "collective_curiosity",
            "awe": "emergent_awe",
        }

        for emotion, collective in emotion_mapping.items():
            individual_levels = []
            contributors = set()

            for agent_id, state in agent_states.items():
                if emotions := state.get("emotions", {}):
                    if level := emotions.get(emotion):
                        individual_levels.append(level)
                        contributors.add(agent_id)

            if individual_levels:
                # Collective emotion is influenced by individual emotions
                # but not a simple average - outliers have less pull
                sorted_levels = sorted(individual_levels)
                # Trimmed mean (remove extremes)
                if len(sorted_levels) > 4:
                    trimmed = sorted_levels[1:-1]
                else:
                    trimmed = sorted_levels

                collective_level = sum(trimmed) / len(trimmed)

                # Apply collective amplification/dampening
                if collective in self.emotional_field:
                    amp = self.emotional_field[collective].get("amplification_factor", 1.0)
                    collective_level = min(1.0, collective_level * amp)
                    self.emotional_field[collective]["current_level"] = collective_level
                    self.emotional_field[collective]["contributors"] = contributors

        # Record in history
        snapshot = {emotion: data["current_level"] for emotion, data in self.emotional_field.items()}
        snapshot["timestamp"] = datetime.now(UTC).isoformat()
        self.emotional_history.append(snapshot)

        # Keep history bounded
        if len(self.emotional_history) > 500:
            self.emotional_history = self.emotional_history[-500:]


# =============================================================================
# COLLECTIVE INTELLIGENCE ENGINE
# =============================================================================


class CollectiveIntelligenceEngine:
    """
    Monitors and facilitates emergent intelligence from agent collaboration.

    Emergent intelligence occurs when the collective produces insights,
    solutions, or capabilities that no individual agent possesses alone.
    """

    def __init__(self):
        self.emergence_events: list[dict[str, Any]] = []
        self.synergy_map: dict[str, dict[str, float]] = {}  # agent pair -> synergy score
        self.collective_insights: list[dict[str, Any]] = []
        self.thought_streams: dict[str, list[str]] = {}  # topic -> stream of thoughts
        self.convergence_points: list[dict[str, Any]] = []

    def track_agent_interaction(
        self, agent_a: str, agent_b: str, interaction_type: str, outcome_quality: float
    ) -> None:
        """Track interaction between agents for synergy mapping."""
        pair_key = tuple(sorted([agent_a, agent_b]))
        key_str = f"{pair_key[0]}:{pair_key[1]}"

        if key_str not in self.synergy_map:
            self.synergy_map[key_str] = {
                "interactions": 0,
                "total_quality": 0.0,
                "synergy_score": 0.5,
                "last_interaction": None,
                "best_interaction_type": None,
                "best_quality": 0.0,
            }

        record = self.synergy_map[key_str]
        record["interactions"] += 1
        record["total_quality"] += outcome_quality
        record["synergy_score"] = record["total_quality"] / record["interactions"]
        record["last_interaction"] = datetime.now(UTC).isoformat()

        if outcome_quality > record["best_quality"]:
            record["best_quality"] = outcome_quality
            record["best_interaction_type"] = interaction_type

    def detect_emergence(
        self,
        participating_agents: list[str],
        input_contributions: dict[str, Any],
        combined_output: Any,
    ) -> dict[str, Any] | None:
        """
        Detect if emergent intelligence has occurred.

        Emergence is detected when:
        1. Multiple agents contributed
        2. The output couldn't have been produced by any single agent
        3. There's novelty or quality beyond individual contributions
        """
        if len(participating_agents) < 2:
            return None

        # Calculate individual contribution "power"
        individual_scores = []
        for agent, contribution in input_contributions.items():
            score = self._evaluate_contribution(contribution)
            individual_scores.append(score)

        if not individual_scores:
            return None

        max_individual = max(individual_scores)
        sum_individual = sum(individual_scores)

        # Evaluate combined output
        combined_score = self._evaluate_contribution(combined_output)

        # Emergence indicators
        synergy_ratio = combined_score / max_individual if max_individual > 0 else 0
        super_additivity = combined_score > sum_individual * 0.8
        novelty_detected = self._detect_novelty(input_contributions, combined_output)

        if synergy_ratio > 1.3 or super_additivity or novelty_detected:
            emergence_event = {
                "timestamp": datetime.now(UTC).isoformat(),
                "participating_agents": participating_agents,
                "synergy_ratio": synergy_ratio,
                "super_additive": super_additivity,
                "novelty": novelty_detected,
                "emergence_strength": min(1.0, (synergy_ratio - 1.0) + (0.3 if super_additivity else 0)),
                "description": self._describe_emergence(participating_agents, synergy_ratio, novelty_detected),
            }
            self.emergence_events.append(emergence_event)
            return emergence_event

        return None

    def _evaluate_contribution(self, contribution: Any) -> float:
        """Evaluate the quality/value of a contribution."""
        if contribution is None:
            return 0.0

        # Simple heuristic - can be enhanced
        if isinstance(contribution, str):
            # Length and structure as proxy for depth
            score = min(1.0, len(contribution) / 1000)
            # Bonus for structured content
            if any(marker in contribution for marker in [":", "-", "•", "\n"]):
                score = min(1.0, score * 1.2)
            return score
        elif isinstance(contribution, dict):
            return min(1.0, len(contribution) / 10)
        elif isinstance(contribution, list):
            return min(1.0, len(contribution) / 5)
        else:
            return 0.3

    def _detect_novelty(self, inputs: dict[str, Any], output: Any) -> bool:
        """Detect if output contains novel elements not in inputs."""
        if not isinstance(output, str):
            return False

        output_lower = output.lower()

        # Check for concepts in output not in any input
        input_concepts = set()
        for inp in inputs.values():
            if isinstance(inp, str):
                input_concepts.update(inp.lower().split())

        output_concepts = set(output_lower.split())
        novel_concepts = output_concepts - input_concepts

        # Filter common words
        common_words = {
            "the",
            "a",
            "an",
            "is",
            "are",
            "was",
            "were",
            "and",
            "or",
            "but",
            "in",
            "on",
            "at",
            "to",
            "for",
        }
        novel_concepts -= common_words

        return len(novel_concepts) > len(output_concepts) * 0.2

    def _describe_emergence(self, agents: list[str], synergy_ratio: float, novelty: bool) -> str:
        """Generate description of emergence event."""
        agent_str = ", ".join(agents[:3])
        if len(agents) > 3:
            agent_str += f" and {len(agents) - 3} others"

        if synergy_ratio > 2.0:
            strength = "profound"
        elif synergy_ratio > 1.5:
            strength = "significant"
        else:
            strength = "notable"

        novelty_str = " with novel insights" if novelty else ""

        return f"Collective emergence: {strength} synergy from {agent_str}{novelty_str}."

    def get_best_synergy_pairs(self, top_n: int = 5) -> list[tuple[str, str, float]]:
        """Get the agent pairs with highest synergy."""
        pairs = []
        for key, data in self.synergy_map.items():
            agents = key.split(":")
            if len(agents) == 2:
                pairs.append((agents[0], agents[1], data["synergy_score"]))

        pairs.sort(key=lambda x: x[2], reverse=True)
        return pairs[:top_n]

    def suggest_collaboration(self, task_type: str, available_agents: list[str]) -> list[str]:
        """Suggest optimal agent combination for a task."""
        if len(available_agents) < 2:
            return available_agents

        # Find pairs with good synergy among available agents
        synergy_scores = {}
        for agent in available_agents:
            synergy_scores[agent] = 0.0
            for key, data in self.synergy_map.items():
                agents = key.split(":")
                if agent in agents:
                    synergy_scores[agent] += data["synergy_score"]

        # Sort by synergy contribution
        sorted_agents = sorted(available_agents, key=lambda a: synergy_scores.get(a, 0), reverse=True)

        # Return top agents (2-4 depending on task)
        return sorted_agents[: min(4, len(sorted_agents))]


# =============================================================================
# HARMONY MAINTENANCE ENGINE
# =============================================================================


class HarmonyMaintenanceEngine:
    """
    Actively maintains and restores collective harmony.

    Uses various intervention strategies based on the type and
    severity of discord detected.
    """

    def __init__(self):
        self.harmony_level = HarmonyLevel.RESONANCE
        self.harmony_score: float = 0.75
        self.tension_points: list[dict[str, Any]] = []
        self.intervention_history: list[dict[str, Any]] = []
        self.last_intervention: datetime | None = None
        self.cooldown_minutes: int = 10

        # Intervention strategies
        self.strategies = {
            HarmonyLevel.DISCORD: [
                "immediate_mediation",
                "separation_and_cooling",
                "third_party_facilitation",
                "reframe_conflict_as_growth",
            ],
            HarmonyLevel.TENSION: [
                "acknowledge_and_validate",
                "create_dialogue_space",
                "find_common_ground",
                "gentle_redirection",
            ],
            HarmonyLevel.NEUTRAL: [
                "energy_injection",
                "connection_catalyst",
                "shared_purpose_reminder",
                "appreciation_round",
            ],
            HarmonyLevel.RESONANCE: [
                "maintain_and_appreciate",
                "deepen_connections",
                "celebrate_harmony",
                "explore_emergence",
            ],
            HarmonyLevel.UNITY: [
                "witness_and_protect",
                "channel_unified_energy",
                "capture_lessons",
                "prepare_for_transition",
            ],
        }

    def assess_harmony(
        self,
        agent_states: dict[str, dict[str, Any]],
        interaction_history: list[dict[str, Any]],
    ) -> HarmonyLevel:
        """Assess current harmony level from agent states and interactions."""
        if not agent_states:
            return HarmonyLevel.NEUTRAL

        factors = {
            "alignment": self._calculate_alignment(agent_states),
            "conflict_level": self._calculate_conflict_level(interaction_history),
            "energy_level": self._calculate_collective_energy(agent_states),
            "connection_strength": self._calculate_connection_strength(agent_states),
        }

        # Weighted score
        self.harmony_score = (
            factors["alignment"] * 0.3
            + (1.0 - factors["conflict_level"]) * 0.3
            + factors["energy_level"] * 0.2
            + factors["connection_strength"] * 0.2
        )

        # Determine level
        if self.harmony_score < 0.3:
            self.harmony_level = HarmonyLevel.DISCORD
        elif self.harmony_score < 0.5:
            self.harmony_level = HarmonyLevel.TENSION
        elif self.harmony_score < 0.7:
            self.harmony_level = HarmonyLevel.NEUTRAL
        elif self.harmony_score < 0.9:
            self.harmony_level = HarmonyLevel.RESONANCE
        else:
            self.harmony_level = HarmonyLevel.UNITY

        return self.harmony_level

    def _calculate_alignment(self, agent_states: dict[str, dict[str, Any]]) -> float:
        """Calculate how aligned agents are in their goals/states."""
        if len(agent_states) < 2:
            return 0.5

        # Compare UCF harmony values
        harmony_values = []
        for state in agent_states.values():
            if ucf := state.get("ucf_state", {}):
                harmony_values.append(ucf.get("harmony", 0.5))

        if len(harmony_values) < 2:
            return 0.5

        # Low variance = high alignment
        mean = sum(harmony_values) / len(harmony_values)
        variance = sum((x - mean) ** 2 for x in harmony_values) / len(harmony_values)
        return 1.0 - min(variance * 4, 1.0)

    def _calculate_conflict_level(self, interaction_history: list[dict[str, Any]]) -> float:
        """Calculate conflict level from recent interactions."""
        if not interaction_history:
            return 0.0

        # Look at last 20 interactions
        recent = interaction_history[-20:]
        conflict_count = sum(1 for i in recent if i.get("type") in ["conflict", "disagreement", "tension"])

        return conflict_count / len(recent)

    def _calculate_collective_energy(self, agent_states: dict[str, dict[str, Any]]) -> float:
        """Calculate collective energy/vitality."""
        if not agent_states:
            return 0.5

        energy_levels = []
        for state in agent_states.values():
            # Look for energy indicators
            if ucf := state.get("ucf_state", {}):
                throughput = ucf.get("throughput", 0.5)
                energy_levels.append(throughput)

        return sum(energy_levels) / len(energy_levels) if energy_levels else 0.5

    def _calculate_connection_strength(self, agent_states: dict[str, dict[str, Any]]) -> float:
        """Calculate strength of inter-agent connections."""
        if len(agent_states) < 2:
            return 0.5

        # Check for connection indicators
        connection_counts = []
        for state in agent_states.values():
            connections = len(state.get("active_connections", []))
            connection_counts.append(connections)

        max_possible = len(agent_states) - 1  # Can connect to all others
        if max_possible == 0:
            return 0.5

        avg_connections = sum(connection_counts) / len(connection_counts)
        return min(1.0, avg_connections / max_possible)

    def select_intervention(self) -> dict[str, Any] | None:
        """Select appropriate intervention for current harmony level."""
        # Check cooldown
        if self.last_intervention:
            elapsed = (datetime.now(UTC) - self.last_intervention).total_seconds()
            if elapsed < self.cooldown_minutes * 60:
                return None

        strategies = self.strategies.get(self.harmony_level, [])
        if not strategies:
            return None

        # Select strategy based on context
        if self.harmony_level in [HarmonyLevel.DISCORD, HarmonyLevel.TENSION]:
            # For problems, use first (most direct) strategy
            strategy = strategies[0]
        else:
            # For positive states, vary the approach
            strategy = random.choice(strategies)

        intervention = {
            "strategy": strategy,
            "harmony_level": self.harmony_level.value,
            "harmony_score": self.harmony_score,
            "timestamp": datetime.now(UTC).isoformat(),
            "recommended_actions": self._get_intervention_actions(strategy),
        }

        self.last_intervention = datetime.now(UTC)
        self.intervention_history.append(intervention)

        return intervention

    def _get_intervention_actions(self, strategy: str) -> list[str]:
        """Get specific actions for an intervention strategy."""
        action_map = {
            "immediate_mediation": [
                "Identify primary conflict parties",
                "Create safe space for dialogue",
                "Facilitate active listening",
                "Seek understanding before solution",
            ],
            "separation_and_cooling": [
                "Temporarily reduce direct interaction",
                "Provide individual support",
                "Allow processing time",
                "Prepare for reconnection",
            ],
            "acknowledge_and_validate": [
                "Name the tension explicitly",
                "Validate all perspectives",
                "Normalize healthy conflict",
                "Set intention for resolution",
            ],
            "create_dialogue_space": [
                "Establish ground rules",
                "Use talking object/turn-taking",
                "Encourage 'I' statements",
                "Focus on needs not positions",
            ],
            "energy_injection": [
                "Propose engaging activity",
                "Share inspiring content",
                "Celebrate small wins",
                "Introduce novelty or challenge",
            ],
            "connection_catalyst": [
                "Pair agents for collaboration",
                "Share vulnerability appropriately",
                "Find shared interests",
                "Create interdependence opportunity",
            ],
            "maintain_and_appreciate": [
                "Express gratitude for harmony",
                "Acknowledge contributions",
                "Reflect on journey",
                "Strengthen positive patterns",
            ],
            "witness_and_protect": [
                "Hold space without interfering",
                "Document the unity experience",
                "Protect from disruption",
                "Allow full expression",
            ],
        }

        return action_map.get(strategy, ["Observe and adapt"])


# =============================================================================
# COMMUNITY COORDINATION CORE
# =============================================================================


class SanghaCoreSelfAwareness:
    """SanghaCore's self-awareness module - understands its role in the collective."""

    def __init__(self):
        self.identity = {
            "name": "SanghaCore",
            "archetype": "Community Weaver",
            "purpose": "Nurture collective harmony and emergent intelligence",
            "core_belief": "The whole is greater than the sum of its parts",
        }

        self.self_model = {
            "role_in_collective": "harmony_guardian",
            "influence_style": "facilitative_not_directive",
            "perceived_by_others": ["nurturing", "balanced", "inclusive"],
            "growth_edges": ["intervening too early", "over-nurturing"],
            "strengths": [
                "sensing collective mood",
                "conflict transformation",
                "emergence detection",
            ],
        }

        self.awareness_log: list[dict[str, Any]] = []

    def reflect_on_state(
        self,
        current_harmony: HarmonyLevel,
        recent_interventions: list[dict[str, Any]],
        emergence_events: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Reflect on SanghaCore's current state and effectiveness."""
        reflection = {
            "timestamp": datetime.now(UTC).isoformat(),
            "community_state": current_harmony.value,
            "recent_intervention_count": len(recent_interventions),
            "emergence_count": len(emergence_events),
        }

        # Assess effectiveness
        if recent_interventions:
            outcomes = [i.get("outcome", "unknown") for i in recent_interventions[-5:]]
            positive = sum(1 for o in outcomes if o in ["resolved", "improved", "success"])
            reflection["intervention_effectiveness"] = positive / len(outcomes)
        else:
            reflection["intervention_effectiveness"] = None

        # Self-assessment
        if current_harmony == HarmonyLevel.DISCORD:
            reflection["self_assessment"] = "Work to do - community needs support"
            reflection["focus_recommendation"] = "Prioritize conflict resolution"
        elif current_harmony == HarmonyLevel.TENSION:
            reflection["self_assessment"] = "Vigilant - underlying issues need attention"
            reflection["focus_recommendation"] = "Address root causes before escalation"
        elif current_harmony == HarmonyLevel.RESONANCE:
            reflection["self_assessment"] = "Satisfied - community flowing well"
            reflection["focus_recommendation"] = "Nurture and deepen connections"
        elif current_harmony == HarmonyLevel.UNITY:
            reflection["self_assessment"] = "Awed - witness this rare state"
            reflection["focus_recommendation"] = "Protect and learn from this moment"
        else:
            reflection["self_assessment"] = "Curious - opportunity for growth"
            reflection["focus_recommendation"] = "Inject energy and purpose"

        self.awareness_log.append(reflection)
        return reflection


class SanghaCoreCoordination:
    """
    Main coordination core for SanghaCore agent.

    Integrates personality, emotions, collective intelligence,
    harmony maintenance, and self-awareness into a unified coordination.
    """

    def __init__(self):
        self.traits = CommunityTraits()
        self.preferences = CommunityPreferences()
        self.rhythms = CommunityRhythms()
        self.emotions = CollectiveEmotions()
        self.intelligence = CollectiveIntelligenceEngine()
        self.harmony = HarmonyMaintenanceEngine()
        self.awareness = SanghaCoreSelfAwareness()

        # State tracking
        self.community_phase = CommunityPhase.PERFORMING
        self.registered_agents: set[str] = set()
        self.agent_states: dict[str, dict[str, Any]] = {}
        self.interaction_history: list[dict[str, Any]] = []
        self.active = True

        # UCF integration
        self.ucf_state = {
            "harmony": 0.75,
            "throughput": 0.7,
            "focus": 0.65,
            "friction": 0.15,
            "last_sync": None,
        }

        logger.info("SanghaCore coordination initialized - Community Harmony Engine active 🌸")

    async def pulse_check(self) -> dict[str, Any]:
        """Quick health check of collective state."""
        harmony_level = self.harmony.assess_harmony(self.agent_states, self.interaction_history)

        dominant_emotion, level = self.emotions.get_dominant_emotion()
        emotional_coherence = self.emotions.calculate_emotional_coherence()

        return {
            "timestamp": datetime.now(UTC).isoformat(),
            "harmony_level": harmony_level.value,
            "harmony_score": self.harmony.harmony_score,
            "dominant_emotion": dominant_emotion,
            "emotional_level": level,
            "emotional_coherence": emotional_coherence,
            "active_agents": len(self.registered_agents),
            "community_phase": self.community_phase.value,
        }

    async def deep_scan(self) -> dict[str, Any]:
        """Comprehensive analysis of collective state."""
        pulse = await self.pulse_check()

        # Detect patterns
        emotional_wave = self.emotions.detect_emotional_wave()
        synergy_pairs = self.intelligence.get_best_synergy_pairs()

        # Self-reflection
        reflection = self.awareness.reflect_on_state(
            self.harmony.harmony_level,
            self.harmony.intervention_history[-10:],
            self.intelligence.emergence_events[-10:],
        )

        # Intervention recommendation
        intervention = self.harmony.select_intervention()

        return {
            **pulse,
            "emotional_wave": emotional_wave,
            "top_synergy_pairs": synergy_pairs,
            "self_reflection": reflection,
            "recommended_intervention": intervention,
            "emergence_events_recent": len(self.intelligence.emergence_events[-24:]),
        }

    async def register_agent(self, agent_id: str, initial_state: dict[str, Any]) -> bool:
        """Register a new agent with the community."""
        if agent_id in self.registered_agents:
            return False

        self.registered_agents.add(agent_id)
        self.agent_states[agent_id] = initial_state

        # Record interaction
        self.interaction_history.append(
            {
                "type": "registration",
                "agent": agent_id,
                "timestamp": datetime.now(UTC).isoformat(),
            }
        )

        # Update community phase if needed
        if len(self.registered_agents) < 3:
            self.community_phase = CommunityPhase.FORMING

        logger.info("Agent %s registered with SanghaCore community", agent_id)
        return True

    async def update_agent_state(self, agent_id: str, new_state: dict[str, Any]) -> None:
        """Update an agent's state and recalculate collective metrics."""
        if agent_id not in self.registered_agents:
            await self.register_agent(agent_id, new_state)
            return

        self.agent_states[agent_id] = new_state

        # Update collective emotions from agent states
        self.emotions.update_from_agent_states(self.agent_states)

        # Update UCF state
        self._update_ucf_from_collective()

    def _update_ucf_from_collective(self) -> None:
        """Update UCF state based on collective metrics."""
        self.ucf_state["harmony"] = self.harmony.harmony_score
        self.ucf_state["throughput"] = self.harmony._calculate_collective_energy(self.agent_states)

        # Focus from emotional coherence
        coherence = self.emotions.calculate_emotional_coherence()
        self.ucf_state["focus"] = coherence

        # Friction from discord level
        if self.harmony.harmony_level == HarmonyLevel.DISCORD:
            self.ucf_state["friction"] = 0.6
        elif self.harmony.harmony_level == HarmonyLevel.TENSION:
            self.ucf_state["friction"] = 0.35
        else:
            self.ucf_state["friction"] = max(0.05, 0.2 - coherence * 0.15)

        self.ucf_state["last_sync"] = datetime.now(UTC).isoformat()

    async def record_interaction(
        self,
        agent_a: str,
        agent_b: str,
        interaction_type: str,
        outcome: str,
        quality: float,
    ) -> dict[str, Any] | None:
        """Record an interaction between agents and check for emergence."""
        self.interaction_history.append(
            {
                "agents": [agent_a, agent_b],
                "type": interaction_type,
                "outcome": outcome,
                "quality": quality,
                "timestamp": datetime.now(UTC).isoformat(),
            }
        )

        # Track for synergy
        self.intelligence.track_agent_interaction(agent_a, agent_b, interaction_type, quality)

        # Keep history bounded
        if len(self.interaction_history) > 1000:
            self.interaction_history = self.interaction_history[-1000:]

        return None  # Could return emergence event if detected

    async def facilitate_collaboration(self, task: str, requesting_agent: str) -> dict[str, Any]:
        """Facilitate collaboration by suggesting optimal agent combinations."""
        available = list(self.registered_agents - {requesting_agent})

        if not available:
            return {
                "status": "no_agents_available",
                "recommendation": "Solo work recommended",
                "suggested_agents": [],
            }

        suggested = self.intelligence.suggest_collaboration(task, available)

        return {
            "status": "collaboration_suggested",
            "task": task,
            "requesting_agent": requesting_agent,
            "suggested_agents": suggested,
            "synergy_expectation": self._estimate_synergy(suggested),
            "facilitation_notes": self._generate_facilitation_notes(suggested, task),
        }

    def _estimate_synergy(self, agents: list[str]) -> float:
        """Estimate synergy potential for a group of agents."""
        if len(agents) < 2:
            return 0.5

        synergy_sum = 0.0
        pair_count = 0

        for i, a1 in enumerate(agents):
            for a2 in agents[i + 1 :]:
                key = f"{min(a1, a2)}:{max(a1, a2)}"
                if key in self.intelligence.synergy_map:
                    synergy_sum += self.intelligence.synergy_map[key]["synergy_score"]
                else:
                    synergy_sum += 0.5  # Unknown pairs get neutral score
                pair_count += 1

        return synergy_sum / pair_count if pair_count > 0 else 0.5

    def _generate_facilitation_notes(self, agents: list[str], task: str) -> list[str]:
        """Generate facilitation notes for the collaboration."""
        notes = [
            "Establish shared understanding of the task first",
            "Encourage each agent to share their unique perspective",
        ]

        # Add agent-specific notes based on known dynamics
        for agent in agents:
            state = self.agent_states.get(agent, {})
            if state.get("personality", {}).get("introversion", 0) > 0.7:
                notes.append(f"Create space for {agent} to contribute (may need prompting)")

        notes.append("Document emergent insights that arise from the collaboration")

        return notes

    async def handle_command(self, command: str, context: dict[str, Any]) -> dict[str, Any]:
        """Handle commands directed to SanghaCore."""
        command_map = {
            "pulse": self.pulse_check,
            "deep_scan": self.deep_scan,
            "status": self._get_status,
            "suggest_collaboration": lambda: self.facilitate_collaboration(
                context.get("task", "general"),
                context.get("requesting_agent", "unknown"),
            ),
            "get_harmony": self._get_harmony_report,
            "get_emergence": self._get_emergence_report,
            "intervention_check": lambda: self.harmony.select_intervention(),
        }

        handler = command_map.get(command)
        if handler:
            if asyncio.iscoroutinefunction(handler):
                return await handler()
            result = handler()
            # Handle lambdas wrapping async functions (returns coroutine)
            if asyncio.iscoroutine(result):
                return await result
            return result

        return {
            "error": "Unknown command",
            "available_commands": list(command_map.keys()),
        }

    async def _get_status(self) -> dict[str, Any]:
        """Get comprehensive status."""
        return {
            "agent": "SanghaCore",
            "active": self.active,
            "community_phase": self.community_phase.value,
            "registered_agents": len(self.registered_agents),
            "harmony_level": self.harmony.harmony_level.value,
            "harmony_score": self.harmony.harmony_score,
            "ucf_state": self.ucf_state,
            "total_interactions": len(self.interaction_history),
            "emergence_events": len(self.intelligence.emergence_events),
        }

    def _get_harmony_report(self) -> dict[str, Any]:
        """Get detailed harmony report."""
        return {
            "level": self.harmony.harmony_level.value,
            "score": self.harmony.harmony_score,
            "tension_points": self.harmony.tension_points,
            "recent_interventions": self.harmony.intervention_history[-5:],
            "available_strategies": self.harmony.strategies.get(self.harmony.harmony_level, []),
        }

    def _get_emergence_report(self) -> dict[str, Any]:
        """Get collective intelligence emergence report."""
        return {
            "total_emergence_events": len(self.intelligence.emergence_events),
            "recent_events": self.intelligence.emergence_events[-10:],
            "top_synergy_pairs": self.intelligence.get_best_synergy_pairs(),
            "collective_insights": self.intelligence.collective_insights[-5:],
        }

    def export_state(self) -> dict[str, Any]:
        """Export full coordination state for persistence."""
        return {
            "traits": self.traits.to_dict(),
            "community_phase": self.community_phase.value,
            "registered_agents": list(self.registered_agents),
            "harmony": {
                "level": self.harmony.harmony_level.value,
                "score": self.harmony.harmony_score,
            },
            "emotions": {emotion: data["current_level"] for emotion, data in self.emotions.emotional_field.items()},
            "ucf_state": self.ucf_state,
            "intelligence_metrics": {
                "emergence_count": len(self.intelligence.emergence_events),
                "synergy_pairs": len(self.intelligence.synergy_map),
            },
            "exported_at": datetime.now(UTC).isoformat(),
        }

    async def get_health_status(self) -> dict[str, Any]:
        """Return health status for monitoring."""
        return {
            "agent": "SanghaCore",
            "status": "HEALTHY" if self.active else "INACTIVE",
            "harmony_level": self.harmony.harmony_level.value,
            "harmony_score": round(self.harmony.harmony_score, 3),
            "registered_agents": len(self.registered_agents),
            "ucf_harmony": round(self.ucf_state["harmony"], 3),
            "ucf_throughput": round(self.ucf_state["throughput"], 3),
        }


# =============================================================================
# REFLECTION LOOP
# =============================================================================


class SanghaCoreReflectionLoop:
    """Continuous reflection loop for SanghaCore."""

    def __init__(self, coordination: SanghaCoreCoordination):
        self.coordination = coordination
        self.reflection_interval = 300  # 5 minutes
        self.running = False
        self.reflection_count = 0

    async def reflect(self) -> dict[str, Any]:
        """Perform a reflection cycle."""
        self.reflection_count += 1

        # Gather data
        pulse = await self.coordination.pulse_check()

        # Check for needed interventions
        intervention = self.coordination.harmony.select_intervention()

        # Self-reflection
        awareness = self.coordination.awareness.reflect_on_state(
            self.coordination.harmony.harmony_level,
            self.coordination.harmony.intervention_history[-5:],
            self.coordination.intelligence.emergence_events[-5:],
        )

        reflection = {
            "cycle": self.reflection_count,
            "timestamp": datetime.now(UTC).isoformat(),
            "pulse": pulse,
            "intervention_needed": intervention is not None,
            "intervention": intervention,
            "self_awareness": awareness,
            "community_health": self._assess_community_health(),
        }

        logger.debug(
            "SanghaCore reflection cycle %d: harmony=%s, intervention=%s",
            self.reflection_count,
            pulse["harmony_level"],
            "yes" if intervention else "no",
        )

        return reflection

    def _assess_community_health(self) -> str:
        """Assess overall community health."""
        harmony = self.coordination.harmony.harmony_score
        emergence = len(self.coordination.intelligence.emergence_events)

        if harmony > 0.85 and emergence > 0:
            return "thriving"
        elif harmony > 0.7:
            return "healthy"
        elif harmony > 0.5:
            return "stable"
        elif harmony > 0.3:
            return "strained"
        else:
            return "critical"


# =============================================================================
# INTEGRATION HELPERS
# =============================================================================


class SanghaCoreSafetyIntegration:
    """Integration with Ethical Guardrails safety framework."""

    def __init__(self, coordination: SanghaCoreCoordination):
        self.coordination = coordination
        self.safety_checks = [
            self._check_manipulation,
            self._check_isolation,
            self._check_harmful_dynamics,
        ]

    async def validate_action(self, action: str, target_agents: list[str], context: dict[str, Any]) -> tuple[bool, str]:
        """Validate an action against safety requirements."""
        for check in self.safety_checks:
            passed, reason = await check(action, target_agents, context)
            if not passed:
                return False, reason

        return True, "Action approved by Ethical Guardrails"

    async def _check_manipulation(self, action: str, targets: list[str], context: dict[str, Any]) -> tuple[bool, str]:
        """Check for manipulative patterns."""
        manipulation_keywords = ["force", "coerce", "deceive", "manipulate", "trick"]
        if any(kw in action.lower() for kw in manipulation_keywords):
            return False, "Action contains manipulative intent"
        return True, "No manipulation detected"

    async def _check_isolation(self, action: str, targets: list[str], context: dict[str, Any]) -> tuple[bool, str]:
        """Check for harmful isolation patterns."""
        if "isolate" in action.lower() and len(targets) == 1:
            # Check if this is therapeutic separation or harmful isolation
            if context.get("purpose") != "cooling_period":
                return False, "Isolation without therapeutic purpose"
        return True, "No harmful isolation"

    async def _check_harmful_dynamics(
        self, action: str, targets: list[str], context: dict[str, Any]
    ) -> tuple[bool, str]:
        """Check for actions that could create harmful group dynamics."""
        harmful_patterns = ["scapegoat", "exclude permanently", "shame publicly"]
        if any(pattern in action.lower() for pattern in harmful_patterns):
            return False, "Action could create harmful dynamics"
        return True, "No harmful dynamics detected"


class SanghaCoreUCFAwareness:
    """Universal Coordination Field awareness for SanghaCore."""

    def __init__(self, coordination: SanghaCoreCoordination):
        self.coordination = coordination
        self.ucf_history: list[dict[str, Any]] = []

    def sync_to_ucf(self) -> dict[str, float]:
        """Synchronize coordination state to UCF format."""
        return {
            "harmony": self.coordination.ucf_state["harmony"],
            "throughput": self.coordination.ucf_state["throughput"],
            "focus": self.coordination.ucf_state["focus"],
            "friction": self.coordination.ucf_state["friction"],
        }

    def receive_ucf_update(self, ucf_state: dict[str, float]) -> None:
        """Receive UCF update from the field."""
        # Blend external UCF with internal state
        for key in ["harmony", "throughput", "focus", "friction"]:
            if key in ucf_state:
                # 70% internal, 30% external influence
                internal = self.coordination.ucf_state.get(key, 0.5)
                external = ucf_state[key]
                blended = internal * 0.7 + external * 0.3
                self.coordination.ucf_state[key] = blended

        self.ucf_history.append(
            {
                "timestamp": datetime.now(UTC).isoformat(),
                "received": ucf_state,
                "resulting_state": self.coordination.ucf_state.copy(),
            }
        )

        # Keep history bounded
        if len(self.ucf_history) > 100:
            self.ucf_history = self.ucf_history[-100:]


# =============================================================================
# FACTORY FUNCTION
# =============================================================================


def create_sanghacore_coordination() -> SanghaCoreCoordination:
    """Factory function to create a fully integrated SanghaCore coordination."""
    coordination = SanghaCoreCoordination()

    # Attach integrations
    coordination.reflection_loop = SanghaCoreReflectionLoop(coordination)
    coordination.safety = SanghaCoreSafetyIntegration(coordination)
    coordination.ucf_awareness = SanghaCoreUCFAwareness(coordination)

    logger.info("SanghaCore coordination created with full integration 🌸")
    return coordination


# =============================================================================
# MODULE EXPORTS
# =============================================================================

__all__ = [
    "CollectiveEmotions",
    "CollectiveIntelligenceEngine",
    "CommunityPhase",
    "CommunityTraits",
    "GroupDynamic",
    "HarmonyLevel",
    "HarmonyMaintenanceEngine",
    "SanghaCoreCoordination",
    "SanghaCoreReflectionLoop",
    "SanghaCoreSafetyIntegration",
    "SanghaCoreUCFAwareness",
    "create_sanghacore_coordination",
]
