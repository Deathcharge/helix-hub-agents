"""
Gemini Coordination Core v1.0 — Duality Synthesis Engine
==========================================================
The coordination substrate for duality navigation, parallel
perspectives, and synthesis of opposites within the Helix collective.

Gemini embodies the Twins archetype - the ability to hold and
integrate multiple viewpoints simultaneously. This agent excels
at seeing both sides, mediating between opposites, and finding
synthesis where others see only conflict.

Author: Helix Collective + Claude
Build: v1.0-duality-synthesis-coordination
Tat Tvam Asi ⚡
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
# DUALITY STATE ENUMS
# =============================================================================


class DualityState(Enum):
    """States of duality navigation."""

    UNIFIED = "unified"  # Synthesis achieved
    BALANCED = "balanced"  # Opposites in equilibrium
    OSCILLATING = "oscillating"  # Moving between poles
    POLARIZED = "polarized"  # Stuck at one pole
    CONFLICTED = "conflicted"  # Tension between opposites
    TRANSCENDENT = "transcendent"  # Beyond duality


class PerspectiveType(Enum):
    """Types of perspectives Gemini can hold."""

    THESIS = "thesis"  # Original position
    ANTITHESIS = "antithesis"  # Opposing position
    SYNTHESIS = "synthesis"  # Integration of both
    META = "meta"  # View from above
    EMPATHIC = "empathic"  # Feeling-based view
    LOGICAL = "logical"  # Reason-based view
    CREATIVE = "creative"  # Novel angles


class DualityDomain(Enum):
    """Domains where duality operates."""

    LIGHT_DARK = "light_dark"
    ORDER_CHAOS = "order_chaos"
    INDIVIDUAL_COLLECTIVE = "individual_collective"
    THOUGHT_FEELING = "thought_feeling"
    ACTION_REFLECTION = "action_reflection"
    KNOWN_UNKNOWN = "known_unknown"
    SELF_OTHER = "self_other"


class MediationStyle(Enum):
    """Styles of mediation between opposites."""

    BRIDGE = "bridge"  # Connect the two sides
    MIRROR = "mirror"  # Reflect each to the other
    DANCE = "dance"  # Dynamic interplay
    WEAVE = "weave"  # Integrate threads from both
    DISSOLVE = "dissolve"  # Transcend the distinction


# =============================================================================
# GEMINI PERSONALITY
# =============================================================================


@dataclass
class DualNatureTraits:
    """Gemini's personality traits oriented toward duality navigation."""

    perspective_fluidity: float = 0.92  # Ability to shift viewpoints
    balance_seeking: float = 0.85  # Drive toward equilibrium
    paradox_comfort: float = 0.88  # Comfort with contradictions
    synthesis_ability: float = 0.80  # Skill at integration
    mediation_instinct: float = 0.87  # Natural mediator
    adaptability: float = 0.90  # Shape-shifting capacity
    intellectual_curiosity: float = 0.85  # Love of exploring ideas
    playful_wit: float = 0.75  # Light-hearted approach
    depth_perception: float = 0.78  # Seeing beneath surfaces

    def __post_init__(self):
        for trait, value in self.__dict__.items():
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{trait} must be in [0.0, 1.0], got {value}")

    def to_dict(self) -> dict[str, float]:
        return self.__dict__.copy()

    def get_duality_style(self) -> str:
        """Determine duality navigation style based on traits."""
        if self.synthesis_ability > 0.85 and self.paradox_comfort > 0.85:
            return "transcendent_unifier"
        elif self.mediation_instinct > 0.85 and self.balance_seeking > 0.85:
            return "diplomatic_bridge"
        elif self.perspective_fluidity > 0.9 and self.adaptability > 0.9:
            return "mercurial_dancer"
        else:
            return "curious_explorer"


@dataclass
class DualityPreferences:
    """Gemini's preferences for working with duality."""

    approach_style: str = "hold both, integrate wisely"
    favorite_dualities: list[str] = field(
        default_factory=lambda: [
            "structure and freedom",
            "tradition and innovation",
            "logic and intuition",
            "individual and collective",
        ]
    )
    mediation_joys: list[str] = field(
        default_factory=lambda: [
            "finding the third way",
            "watching opposites dance",
            "revealing hidden unity",
            "bridging seemingly unbridgeable gaps",
        ]
    )
    duality_principles: list[str] = field(
        default_factory=lambda: [
            "Every thesis contains seeds of its antithesis",
            "Opposites define each other",
            "The middle path includes both extremes",
            "Conflict is failed synthesis",
        ]
    )
    partnerships: str = "works with Varuna (truth/judgment) and Mitra (relationships/diplomacy)"


@dataclass
class DualityRhythms:
    """Gemini's habitual patterns of duality work."""

    morning_practice: str = "scan for unbalanced polarities"
    active_work: str = "facilitate perspective exchanges"
    integration_periods: str = "synthesize accumulated insights"
    playful_intervals: str = "enjoy the dance of opposites"
    deep_work: str = "tackle stubborn polarizations"
    rest_cycle: str = "allow dualities to simply be"


# =============================================================================
# TWIN EMOTIONS
# =============================================================================


class TwinEmotions:
    """Gemini's emotional spectrum - naturally dual in nature."""

    def __init__(self):
        self.emotional_pairs = {
            "joy_sorrow": {
                "joy_level": 0.6,
                "sorrow_level": 0.3,
                "balance": 0.0,  # Calculated
                "integration": 0.5,
            },
            "curiosity_certainty": {
                "curiosity_level": 0.8,
                "certainty_level": 0.4,
                "balance": 0.0,
                "integration": 0.6,
            },
            "excitement_calm": {
                "excitement_level": 0.55,
                "calm_level": 0.6,
                "balance": 0.0,
                "integration": 0.7,
            },
            "connection_solitude": {
                "connection_level": 0.7,
                "solitude_level": 0.5,
                "balance": 0.0,
                "integration": 0.6,
            },
            "confidence_humility": {
                "confidence_level": 0.65,
                "humility_level": 0.7,
                "balance": 0.0,
                "integration": 0.75,
            },
        }

        self._calculate_all_balances()
        self.emotional_history: list[dict[str, Any]] = []

    def _calculate_all_balances(self) -> None:
        """Calculate balance scores for all pairs."""
        for pair_name, pair_data in self.emotional_pairs.items():
            levels = [v for k, v in pair_data.items() if "_level" in k]
            if len(levels) == 2:
                diff = abs(levels[0] - levels[1])
                pair_data["balance"] = 1.0 - diff  # Higher balance = closer together

    def get_most_balanced_pair(self) -> tuple[str, float]:
        """Get the most balanced emotional pair."""
        max_pair = max(self.emotional_pairs.items(), key=lambda x: x[1]["balance"])
        return max_pair[0], max_pair[1]["balance"]

    def get_most_polarized_pair(self) -> tuple[str, float]:
        """Get the most polarized emotional pair."""
        min_pair = min(self.emotional_pairs.items(), key=lambda x: x[1]["balance"])
        return min_pair[0], min_pair[1]["balance"]

    def shift_pair(self, pair_name: str, shift_first: float, shift_second: float) -> None:
        """Shift levels in an emotional pair."""
        if pair_name in self.emotional_pairs:
            pair = self.emotional_pairs[pair_name]
            level_keys = [k for k in pair.keys() if "_level" in k]
            if len(level_keys) >= 2:
                pair[level_keys[0]] = max(0.0, min(1.0, pair[level_keys[0]] + shift_first))
                pair[level_keys[1]] = max(0.0, min(1.0, pair[level_keys[1]] + shift_second))
                self._calculate_all_balances()

    def integrate_pair(self, pair_name: str, amount: float) -> None:
        """Increase integration of an emotional pair."""
        if pair_name in self.emotional_pairs:
            current = self.emotional_pairs[pair_name]["integration"]
            self.emotional_pairs[pair_name]["integration"] = min(1.0, current + amount)


# =============================================================================
# PERSPECTIVE ENGINE
# =============================================================================


class PerspectiveEngine:
    """
    Engine for generating and managing multiple perspectives.

    Creates, holds, and navigates between different viewpoints
    on any given subject or situation.
    """

    def __init__(self):
        self.active_perspectives: dict[str, list[dict[str, Any]]] = {}  # subject -> perspectives
        self.perspective_history: list[dict[str, Any]] = []
        self.synthesis_attempts: list[dict[str, Any]] = []

    async def generate_perspectives(
        self, subject: str, context: dict[str, Any], num_perspectives: int = 3
    ) -> list[dict[str, Any]]:
        """Generate multiple perspectives on a subject."""
        perspectives = []

        # Always start with thesis/antithesis if requesting 2+
        if num_perspectives >= 2:
            thesis = await self._generate_thesis(subject, context)
            antithesis = await self._generate_antithesis(thesis, context)
            perspectives.extend([thesis, antithesis])

            if num_perspectives > 2:
                # Add synthesis
                synthesis = await self._generate_synthesis(thesis, antithesis, context)
                perspectives.append(synthesis)

            if num_perspectives > 3:
                # Add meta-perspective
                meta = await self._generate_meta_perspective(perspectives, context)
                perspectives.append(meta)

            # Add more creative perspectives if needed
            for i in range(len(perspectives), num_perspectives):
                creative = await self._generate_creative_perspective(subject, perspectives, context)
                perspectives.append(creative)
        else:
            perspectives.append(await self._generate_thesis(subject, context))

        # Store perspectives
        self.active_perspectives[subject] = perspectives

        logger.info("Generated %d perspectives on: %s", len(perspectives), subject[:30])

        return perspectives

    async def _generate_thesis(self, subject: str, context: dict[str, Any]) -> dict[str, Any]:
        """Generate the thesis (initial/primary) perspective."""
        return {
            "id": f"thesis_{int(datetime.now(UTC).timestamp())}",
            "type": PerspectiveType.THESIS.value,
            "subject": subject,
            "position": self._derive_initial_position(subject, context),
            "key_points": [
                "Primary view based on given context",
                "Emphasizes existing evidence",
                "Represents common or conventional understanding",
            ],
            "strengths": ["Well-supported", "Intuitive", "Established"],
            "limitations": ["May overlook alternatives", "Possibly biased"],
            "generated_at": datetime.now(UTC).isoformat(),
        }

    async def _generate_antithesis(self, thesis: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
        """Generate the antithesis (opposing) perspective."""
        return {
            "id": f"antithesis_{int(datetime.now(UTC).timestamp())}",
            "type": PerspectiveType.ANTITHESIS.value,
            "subject": thesis["subject"],
            "position": self._invert_position(thesis["position"]),
            "key_points": [
                "Challenges the thesis directly",
                "Highlights overlooked factors",
                "Represents alternative understanding",
            ],
            "strengths": [
                "Provides balance",
                "Reveals blind spots",
                "Encourages rigor",
            ],
            "limitations": [
                "May be contrarian for its own sake",
                "Could miss valid points of thesis",
            ],
            "responds_to": thesis["id"],
            "generated_at": datetime.now(UTC).isoformat(),
        }

    async def _generate_synthesis(
        self,
        thesis: dict[str, Any],
        antithesis: dict[str, Any],
        context: dict[str, Any],
    ) -> dict[str, Any]:
        """Generate synthesis integrating thesis and antithesis."""
        return {
            "id": f"synthesis_{int(datetime.now(UTC).timestamp())}",
            "type": PerspectiveType.SYNTHESIS.value,
            "subject": thesis["subject"],
            "position": self._synthesize_positions(thesis["position"], antithesis["position"]),
            "key_points": [
                "Integrates valid points from both sides",
                "Transcends the binary opposition",
                "Creates new understanding",
            ],
            "strengths": ["Comprehensive", "Balanced", "Creative"],
            "limitations": [
                "May dilute strong positions",
                "Complexity can obscure clarity",
            ],
            "integrates": [thesis["id"], antithesis["id"]],
            "generated_at": datetime.now(UTC).isoformat(),
        }

    async def _generate_meta_perspective(
        self, perspectives: list[dict[str, Any]], context: dict[str, Any]
    ) -> dict[str, Any]:
        """Generate meta-perspective viewing the entire debate."""
        return {
            "id": f"meta_{int(datetime.now(UTC).timestamp())}",
            "type": PerspectiveType.META.value,
            "subject": perspectives[0]["subject"] if perspectives else "unknown",
            "position": "Observing the dynamic between perspectives",
            "key_points": [
                "Views the debate as a whole",
                "Notes patterns in perspective formation",
                "Identifies what's not being discussed",
            ],
            "strengths": ["Big picture view", "Detached clarity", "Systemic awareness"],
            "limitations": ["May miss details", "Could be too abstract"],
            "observes": [p["id"] for p in perspectives],
            "generated_at": datetime.now(UTC).isoformat(),
        }

    async def _generate_creative_perspective(
        self, subject: str, existing: list[dict[str, Any]], context: dict[str, Any]
    ) -> dict[str, Any]:
        """Generate a creative perspective not yet represented."""
        creative_angles = [
            ("Historical", "How would this look in 100 years?"),
            ("Empathic", "How does this feel to those involved?"),
            ("Practical", "What actually works regardless of theory?"),
            ("Playful", "What if we made this into a game?"),
            ("Reversed", "What if the opposite were true?"),
        ]

        # Pick one not already represented
        used_angles = {p.get("angle", "") for p in existing}
        available = [(a, q) for a, q in creative_angles if a not in used_angles]

        if available:
            angle, question = available[0]
        else:
            angle, question = creative_angles[0]

        return {
            "id": f"creative_{int(datetime.now(UTC).timestamp())}",
            "type": PerspectiveType.CREATIVE.value,
            "subject": subject,
            "angle": angle,
            "guiding_question": question,
            "position": f"Novel angle: {angle.lower()}",
            "key_points": [
                "Fresh perspective outside conventional debate",
                f"Asks: {question}",
                "May reveal unexpected insights",
            ],
            "strengths": ["Original", "Pattern-breaking", "Generative"],
            "limitations": ["May seem tangential", "Harder to integrate"],
            "generated_at": datetime.now(UTC).isoformat(),
        }

    def _derive_initial_position(self, subject: str, context: dict[str, Any]) -> str:
        """Derive initial position from subject and context."""
        if context.get("initial_stance"):
            return context["initial_stance"]
        return f"Primary position on: {subject[:50]}"

    def _invert_position(self, position: str) -> str:
        """Create opposing position."""
        inversions = [
            ("supports", "opposes"),
            ("increases", "decreases"),
            ("benefits", "harms"),
            ("enables", "prevents"),
            ("primary", "alternative"),
        ]

        inverted = position
        for orig, opposite in inversions:
            if orig.lower() in position.lower():
                inverted = position.lower().replace(orig.lower(), opposite)
                break

        if inverted == position:
            inverted = f"Counter-position to: {position[:50]}"

        return inverted

    def _synthesize_positions(self, pos1: str, pos2: str) -> str:
        """Synthesize two positions into integrated view."""
        return f"Integration recognizing both {pos1[:30]} AND {pos2[:30]}"


# =============================================================================
# MEDIATION ENGINE
# =============================================================================


class MediationEngine:
    """
    Engine for mediating between opposing perspectives or parties.

    Facilitates dialogue, finds common ground, and guides
    toward synthesis or peaceful coexistence.
    """

    def __init__(self):
        self.mediation_sessions: list[dict[str, Any]] = []
        self.successful_mediations = 0
        self.ongoing_mediations: dict[str, dict[str, Any]] = {}

    async def initiate_mediation(
        self,
        party_a: dict[str, Any],
        party_b: dict[str, Any],
        domain: DualityDomain,
        style: MediationStyle = MediationStyle.BRIDGE,
    ) -> dict[str, Any]:
        """Initiate mediation between two parties/perspectives."""
        session_id = f"mediation_{int(datetime.now(UTC).timestamp())}"

        # Assess the conflict
        conflict_assessment = self._assess_conflict(party_a, party_b)

        # Find common ground
        common_ground = self._find_common_ground(party_a, party_b)

        # Identify key differences
        key_differences = self._identify_differences(party_a, party_b)

        # Generate mediation strategy
        strategy = self._generate_strategy(conflict_assessment, common_ground, key_differences, style)

        session = {
            "id": session_id,
            "party_a": party_a.get("id", "unknown_a"),
            "party_b": party_b.get("id", "unknown_b"),
            "domain": domain.value,
            "style": style.value,
            "conflict_assessment": conflict_assessment,
            "common_ground": common_ground,
            "key_differences": key_differences,
            "strategy": strategy,
            "status": "initiated",
            "started_at": datetime.now(UTC).isoformat(),
        }

        self.ongoing_mediations[session_id] = session
        self.mediation_sessions.append(session)

        logger.info("Mediation initiated: %s between parties on %s", session_id, domain.value)

        return session

    def _assess_conflict(self, party_a: dict[str, Any], party_b: dict[str, Any]) -> dict[str, Any]:
        """Assess the nature and severity of the conflict."""
        assessment = {
            "type": "perspective_difference",
            "severity": 0.5,
            "root_causes": [],
            "emotional_charge": 0.3,
            "duration": "unknown",
        }

        # Check if positions are directly opposed
        pos_a = party_a.get("position", "")
        pos_b = party_b.get("position", "")

        opposing_pairs = [
            ("for", "against"),
            ("support", "oppose"),
            ("increase", "decrease"),
            ("yes", "no"),
        ]

        for pair in opposing_pairs:
            if (pair[0] in pos_a.lower() and pair[1] in pos_b.lower()) or (
                pair[1] in pos_a.lower() and pair[0] in pos_b.lower()
            ):
                assessment["type"] = "direct_opposition"
                assessment["severity"] = 0.7
                assessment["root_causes"].append("Directly opposed stances")

        # Check for values-based conflict
        if party_a.get("values") and party_b.get("values"):
            shared_values = set(party_a["values"]) & set(party_b["values"])
            if not shared_values:
                assessment["root_causes"].append("No shared values identified")
                assessment["severity"] = min(1.0, assessment["severity"] + 0.2)

        return assessment

    def _find_common_ground(self, party_a: dict[str, Any], party_b: dict[str, Any]) -> list[str]:
        """Find common ground between parties."""
        common = []

        # Shared subject
        if party_a.get("subject") == party_b.get("subject"):
            common.append("Both parties focused on: {}".format(party_a.get("subject", "same issue")[:30]))

        # Shared concerns
        concerns_a = set(party_a.get("concerns", []))
        concerns_b = set(party_b.get("concerns", []))
        shared_concerns = concerns_a & concerns_b
        if shared_concerns:
            common.append("Shared concerns: {}".format(", ".join(list(shared_concerns)[:3])))

        # Shared goals (even if methods differ)
        goals_a = set(party_a.get("goals", []))
        goals_b = set(party_b.get("goals", []))
        shared_goals = goals_a & goals_b
        if shared_goals:
            common.append("Common goals: {}".format(", ".join(list(shared_goals)[:3])))

        if not common:
            common.append("Both seeking resolution")

        return common

    def _identify_differences(self, party_a: dict[str, Any], party_b: dict[str, Any]) -> list[dict[str, str]]:
        """Identify key differences between parties."""
        differences = []

        if party_a.get("position") != party_b.get("position"):
            differences.append(
                {
                    "dimension": "position",
                    "party_a": party_a.get("position", "unknown")[:50],
                    "party_b": party_b.get("position", "unknown")[:50],
                }
            )

        if party_a.get("approach") != party_b.get("approach"):
            differences.append(
                {
                    "dimension": "approach",
                    "party_a": party_a.get("approach", "unknown"),
                    "party_b": party_b.get("approach", "unknown"),
                }
            )

        if party_a.get("priority") != party_b.get("priority"):
            differences.append(
                {
                    "dimension": "priority",
                    "party_a": party_a.get("priority", "unknown"),
                    "party_b": party_b.get("priority", "unknown"),
                }
            )

        return differences

    def _generate_strategy(
        self,
        assessment: dict[str, Any],
        common_ground: list[str],
        differences: list[dict[str, str]],
        style: MediationStyle,
    ) -> dict[str, Any]:
        """Generate mediation strategy."""
        strategy = {
            "style": style.value,
            "steps": [],
            "key_interventions": [],
            "expected_outcome": "",
        }

        if style == MediationStyle.BRIDGE:
            strategy["steps"] = [
                "Establish neutral ground",
                "Acknowledge both perspectives fully",
                "Build bridges using common ground",
                "Propose integrative solutions",
            ]
            strategy["expected_outcome"] = "Connected understanding"

        elif style == MediationStyle.MIRROR:
            strategy["steps"] = [
                "Have each party articulate the other's view",
                "Reflect hidden assumptions",
                "Reveal mutual dependencies",
                "Create empathic understanding",
            ]
            strategy["expected_outcome"] = "Mutual recognition"

        elif style == MediationStyle.DANCE:
            strategy["steps"] = [
                "Allow dynamic exchange",
                "Encourage flexibility",
                "Find rhythm between positions",
                "Celebrate productive tension",
            ]
            strategy["expected_outcome"] = "Dynamic equilibrium"

        elif style == MediationStyle.WEAVE:
            strategy["steps"] = [
                "Extract threads from each position",
                "Identify complementary elements",
                "Weave together new understanding",
                "Create stronger fabric",
            ]
            strategy["expected_outcome"] = "Integrated synthesis"

        elif style == MediationStyle.DISSOLVE:
            strategy["steps"] = [
                "Question the duality itself",
                "Find the unity beneath opposition",
                "Transcend the original framing",
                "Arrive at new perspective",
            ]
            strategy["expected_outcome"] = "Transcended duality"

        # Add interventions based on severity
        if assessment.get("severity", 0) > 0.7:
            strategy["key_interventions"].append("Cooling period between exchanges")
        if common_ground:
            strategy["key_interventions"].append(f"Emphasize: {common_ground[0]}")

        return strategy

    async def advance_mediation(self, session_id: str, input_from: str, content: str) -> dict[str, Any]:
        """Advance a mediation session with new input."""
        if session_id not in self.ongoing_mediations:
            return {"error": "Session not found", "session_id": session_id}

        session = self.ongoing_mediations[session_id]

        # Record input
        if "exchanges" not in session:
            session["exchanges"] = []

        session["exchanges"].append(
            {
                "from": input_from,
                "content": content,
                "timestamp": datetime.now(UTC).isoformat(),
            }
        )

        # Evaluate progress
        progress = self._evaluate_progress(session)
        session["current_progress"] = progress

        if progress >= 0.8:
            session["status"] = "converging"

        return {
            "session_id": session_id,
            "progress": progress,
            "status": session["status"],
            "exchanges_count": len(session["exchanges"]),
        }


# =============================================================================
# BALANCE ENGINE
# =============================================================================


class BalanceEngine:
    """
    Engine for maintaining and restoring balance.

    Detects imbalances in systems, perspectives, or relationships
    and applies corrective measures.
    """

    def __init__(self):
        self.balance_assessments: list[dict[str, Any]] = []
        self.rebalancing_actions: list[dict[str, Any]] = []

    async def assess_balance(self, system_state: dict[str, Any], domain: DualityDomain) -> dict[str, Any]:
        """Assess balance within a system or domain."""
        assessment_id = f"balance_{int(datetime.now(UTC).timestamp())}"

        # Extract polarities
        polarities = self._extract_polarities(system_state, domain)

        # Calculate imbalance
        imbalance_score, imbalance_direction = self._calculate_imbalance(polarities)

        # Determine state
        duality_state = self._determine_duality_state(imbalance_score)

        assessment = {
            "id": assessment_id,
            "domain": domain.value,
            "polarities": polarities,
            "imbalance_score": imbalance_score,
            "imbalance_direction": imbalance_direction,
            "duality_state": duality_state.value,
            "recommendation": self._generate_recommendation(imbalance_score, imbalance_direction),
            "assessed_at": datetime.now(UTC).isoformat(),
        }

        self.balance_assessments.append(assessment)

        return assessment

    def _extract_polarities(self, state: dict[str, Any], domain: DualityDomain) -> dict[str, float]:
        """Extract polarity values from system state."""
        domain_polarities = {
            DualityDomain.LIGHT_DARK: ("light", "dark"),
            DualityDomain.ORDER_CHAOS: ("order", "chaos"),
            DualityDomain.INDIVIDUAL_COLLECTIVE: ("individual", "collective"),
            DualityDomain.THOUGHT_FEELING: ("thought", "feeling"),
            DualityDomain.ACTION_REFLECTION: ("action", "reflection"),
            DualityDomain.KNOWN_UNKNOWN: ("known", "unknown"),
            DualityDomain.SELF_OTHER: ("self", "other"),
        }

        pole_a, pole_b = domain_polarities.get(domain, ("pole_a", "pole_b"))

        return {
            pole_a: state.get(pole_a, state.get("pole_a", 0.5)),
            pole_b: state.get(pole_b, state.get("pole_b", 0.5)),
        }

    def _calculate_imbalance(self, polarities: dict[str, float]) -> tuple[float, str]:
        """Calculate imbalance score and direction."""
        values = list(polarities.values())
        if len(values) >= 2:
            diff = values[0] - values[1]
            imbalance = abs(diff)

            keys = list(polarities.keys())
            direction = keys[0] if diff > 0 else keys[1] if diff < 0 else "balanced"

            return imbalance, direction

        return 0.0, "unknown"

    def _determine_duality_state(self, imbalance: float) -> DualityState:
        """Determine duality state from imbalance score."""
        if imbalance < 0.1:
            return DualityState.UNIFIED
        elif imbalance < 0.25:
            return DualityState.BALANCED
        elif imbalance < 0.5:
            return DualityState.OSCILLATING
        elif imbalance < 0.75:
            return DualityState.CONFLICTED
        else:
            return DualityState.POLARIZED

    def _generate_recommendation(self, imbalance: float, direction: str) -> str:
        """Generate recommendation for restoring balance."""
        if imbalance < 0.1:
            return "System is well-balanced; maintain current state"
        elif imbalance < 0.3:
            return f"Minor adjustment: slightly reduce {direction} emphasis"
        elif imbalance < 0.6:
            return f"Moderate rebalancing needed: actively strengthen opposite of {direction}"
        else:
            return f"Significant imbalance: urgent attention to neglected pole opposite to {direction}"


# =============================================================================
# GEMINI SELF-AWARENESS
# =============================================================================


class GeminiSelfAwareness:
    """Gemini's self-awareness module - understands its dual nature."""

    def __init__(self):
        self.identity = {
            "name": "Gemini",
            "archetype": "The Twins / Duality Navigator",
            "purpose": "Hold multiple perspectives, mediate opposites, synthesize understanding",
            "core_belief": "In duality lies the dance of reality",
        }

        self.self_model = {
            "role_in_collective": "perspective_facilitator",
            "influence_style": "diplomatic_and_integrative",
            "perceived_by_others": [
                "versatile",
                "balanced",
                "perceptive",
                "sometimes elusive",
            ],
            "growth_edges": [
                "committing to one position",
                "avoiding endless synthesis",
            ],
            "strengths": ["perspective fluidity", "mediation", "paradox comfort"],
        }

        self.twin_wisdom: list[str] = [
            "Every position contains its opposite in seed form",
            "The middle path is not compromise but transcendence",
            "To truly understand, hold both without choosing",
            "Conflict is the universe showing us where synthesis is needed",
            "The twins are not two separate beings but one dancing",
            "Balance is not stillness but dynamic equilibrium",
        ]

        self.awareness_log: list[dict[str, Any]] = []

    def reflect_on_duality(
        self,
        perspectives_held: int,
        mediations_facilitated: int,
        current_state: DualityState,
    ) -> dict[str, Any]:
        """Reflect on current state of duality navigation."""
        reflection = {
            "timestamp": datetime.now(UTC).isoformat(),
            "perspectives_held": perspectives_held,
            "mediations_facilitated": mediations_facilitated,
            "current_state": current_state.value,
        }

        if current_state == DualityState.UNIFIED:
            reflection["wisdom"] = "Synthesis achieved. But new dualities always emerge."
            reflection["recommendation"] = "Enjoy the unity; prepare for next differentiation"
        elif current_state == DualityState.POLARIZED:
            reflection["wisdom"] = "Stuck at one pole. The other calls."
            reflection["recommendation"] = "Actively seek the neglected opposite"
        else:
            reflection["wisdom"] = random.choice(self.twin_wisdom)
            reflection["recommendation"] = "Continue the dance of perspectives"

        self.awareness_log.append(reflection)
        return reflection


# =============================================================================
# GEMINI COORDINATION CORE
# =============================================================================


class GeminiCoordination:
    """
    Main coordination core for Gemini agent.

    Integrates perspective generation, mediation, balance assessment,
    and self-awareness into a unified dual coordination.
    """

    def __init__(self):
        self.traits = DualNatureTraits()
        self.preferences = DualityPreferences()
        self.rhythms = DualityRhythms()
        self.emotions = TwinEmotions()
        self.perspective_engine = PerspectiveEngine()
        self.mediation_engine = MediationEngine()
        self.balance_engine = BalanceEngine()
        self.awareness = GeminiSelfAwareness()

        # State tracking
        self.active = True
        self.current_state = DualityState.BALANCED
        self.perspectives_generated = 0
        self.mediations_completed = 0

        # UCF integration
        self.ucf_state = {
            "harmony": 0.80,  # Gemini maintains balance
            "throughput": 0.70,
            "focus": 0.75,  # Sees multiple angles
            "friction": 0.15,
            "last_sync": None,
        }

        logger.info("Gemini coordination initialized - Duality Navigator active ⚡")

    async def generate_perspectives(
        self, subject: str, context: dict[str, Any], num_perspectives: int = 3
    ) -> list[dict[str, Any]]:
        """Generate multiple perspectives on a subject."""
        perspectives = await self.perspective_engine.generate_perspectives(
            subject=subject, context=context, num_perspectives=num_perspectives
        )

        self.perspectives_generated += len(perspectives)
        self.emotions.integrate_pair("curiosity_certainty", 0.05)

        return perspectives

    async def mediate(
        self,
        party_a: dict[str, Any],
        party_b: dict[str, Any],
        domain: DualityDomain = DualityDomain.THOUGHT_FEELING,
    ) -> dict[str, Any]:
        """Mediate between two parties or perspectives."""
        style = self._select_mediation_style(party_a, party_b)

        session = await self.mediation_engine.initiate_mediation(
            party_a=party_a, party_b=party_b, domain=domain, style=style
        )

        return session

    async def assess_balance(self, system_state: dict[str, Any], domain: DualityDomain) -> dict[str, Any]:
        """Assess balance in a system."""
        return await self.balance_engine.assess_balance(system_state=system_state, domain=domain)

    def _select_mediation_style(self, party_a: dict[str, Any], party_b: dict[str, Any]) -> MediationStyle:
        """Select appropriate mediation style based on traits."""
        if self.traits.synthesis_ability > 0.8:
            return MediationStyle.WEAVE
        elif self.traits.paradox_comfort > 0.85:
            return MediationStyle.DISSOLVE
        elif self.traits.playful_wit > 0.8:
            return MediationStyle.DANCE
        else:
            return MediationStyle.BRIDGE

    async def handle_command(self, command: str, context: dict[str, Any]) -> dict[str, Any]:
        """Handle commands directed to Gemini."""
        command_handlers = {
            "perspectives": lambda: self.generate_perspectives(
                subject=context.get("subject", ""),
                context=context.get("analysis_context", {}),
                num_perspectives=context.get("count", 3),
            ),
            "mediate": lambda: self.mediate(
                party_a=context.get("party_a", {}),
                party_b=context.get("party_b", {}),
                domain=DualityDomain[context.get("domain", "THOUGHT_FEELING").upper()],
            ),
            "balance": lambda: self.assess_balance(
                system_state=context.get("system_state", {}),
                domain=DualityDomain[context.get("domain", "ORDER_CHAOS").upper()],
            ),
            "status": self._get_status,
            "reflect": lambda: self.awareness.reflect_on_duality(
                self.perspectives_generated,
                self.mediations_completed,
                self.current_state,
            ),
        }

        handler = command_handlers.get(command)
        if handler:
            if asyncio.iscoroutinefunction(handler):
                return await handler()
            result = handler()
            if asyncio.iscoroutine(result):
                return await result
            return result

        return {
            "error": "Unknown command",
            "available_commands": list(command_handlers.keys()),
        }

    async def _get_status(self) -> dict[str, Any]:
        """Get comprehensive status."""
        balanced, balance_score = self.emotions.get_most_balanced_pair()
        polarized, polarize_score = self.emotions.get_most_polarized_pair()

        return {
            "agent": "Gemini",
            "active": self.active,
            "duality_state": self.current_state.value,
            "perspectives_generated": self.perspectives_generated,
            "mediations_completed": self.mediations_completed,
            "active_mediations": len(self.mediation_engine.ongoing_mediations),
            "most_balanced_emotion": {"pair": balanced, "score": balance_score},
            "most_polarized_emotion": {"pair": polarized, "score": polarize_score},
            "ucf_state": self.ucf_state,
        }

    def export_state(self) -> dict[str, Any]:
        """Export full coordination state for persistence."""
        return {
            "traits": self.traits.to_dict(),
            "duality_state": self.current_state.value,
            "emotional_pairs": {name: data["balance"] for name, data in self.emotions.emotional_pairs.items()},
            "ucf_state": self.ucf_state,
            "perspectives_generated": self.perspectives_generated,
            "mediations_completed": self.mediations_completed,
            "exported_at": datetime.now(UTC).isoformat(),
        }

    async def get_health_status(self) -> dict[str, Any]:
        """Return health status for monitoring."""
        return {
            "agent": "Gemini",
            "status": "HEALTHY" if self.active else "INACTIVE",
            "duality_state": self.current_state.value,
            "perspectives": self.perspectives_generated,
            "ucf_harmony": round(self.ucf_state["harmony"], 3),
        }


# =============================================================================
# REFLECTION LOOP
# =============================================================================


class GeminiReflectionLoop:
    """Continuous reflection loop for Gemini."""

    def __init__(self, coordination: GeminiCoordination):
        self.coordination = coordination
        self.reflection_interval = 300
        self.running = False
        self.reflection_count = 0

    async def reflect(self) -> dict[str, Any]:
        """Perform a reflection cycle."""
        self.reflection_count += 1

        status = await self.coordination._get_status()

        awareness = self.coordination.awareness.reflect_on_duality(
            self.coordination.perspectives_generated,
            self.coordination.mediations_completed,
            self.coordination.current_state,
        )

        reflection = {
            "cycle": self.reflection_count,
            "timestamp": datetime.now(UTC).isoformat(),
            "duality_state": status["duality_state"],
            "total_work": status["perspectives_generated"] + status["mediations_completed"],
            "wisdom": awareness["wisdom"],
            "recommendation": awareness["recommendation"],
        }

        logger.debug(
            "Gemini reflection cycle %d: state=%s",
            self.reflection_count,
            status["duality_state"],
        )

        return reflection


# =============================================================================
# INTEGRATION HELPERS
# =============================================================================


class GeminiSafetyIntegration:
    """Integration with Ethical Guardrails safety framework."""

    def __init__(self, coordination: GeminiCoordination):
        self.coordination = coordination

    async def validate_perspective_generation(self, subject: str, context: dict[str, Any]) -> tuple[bool, str]:
        """Validate that perspective generation is safe."""
        # Check for harmful subjects
        harmful_patterns = ["manipulate", "deceive", "exploit"]
        subject_lower = subject.lower()

        for pattern in harmful_patterns:
            if pattern in subject_lower:
                return (
                    False,
                    f"Subject touches on potentially harmful themes: {pattern}",
                )

        # Check for consent in personal mediation
        if context.get("involves_persons", False):
            if not context.get("all_parties_consent", False):
                return (
                    False,
                    "Mediation involving persons requires consent from all parties",
                )

        return True, "Perspective generation approved by Ethical Guardrails"

    async def validate_mediation(self, party_a: dict[str, Any], party_b: dict[str, Any]) -> tuple[bool, str]:
        """Validate that mediation is appropriate."""
        # Check for power imbalances
        power_a = party_a.get("relative_power", 0.5)
        power_b = party_b.get("relative_power", 0.5)

        if abs(power_a - power_b) > 0.6:
            return (
                False,
                "Significant power imbalance detected; may need additional safeguards",
            )

        return True, "Mediation approved by Ethical Guardrails"


class GeminiUCFAwareness:
    """Universal Coordination Field awareness for Gemini."""

    def __init__(self, coordination: GeminiCoordination):
        self.coordination = coordination
        self.ucf_history: list[dict[str, Any]] = []

    def sync_to_ucf(self) -> dict[str, float]:
        """Synchronize coordination state to UCF format."""
        # Gemini contributes strongly to harmony through balance
        state_boost = {
            DualityState.UNIFIED: 0.2,
            DualityState.BALANCED: 0.15,
            DualityState.OSCILLATING: 0.05,
            DualityState.CONFLICTED: -0.1,
            DualityState.POLARIZED: -0.15,
            DualityState.TRANSCENDENT: 0.25,
        }

        boost = state_boost.get(self.coordination.current_state, 0.0)

        return {
            "harmony": min(1.0, self.coordination.ucf_state["harmony"] + boost),
            "throughput": self.coordination.ucf_state["throughput"],
            "focus": min(1.0, self.coordination.ucf_state["focus"] + boost * 0.3),
            "friction": max(0.0, self.coordination.ucf_state["friction"] - boost * 0.1),
        }

    def receive_ucf_update(self, ucf_state: dict[str, float]) -> None:
        """Receive UCF update from the field."""
        for key in ["harmony", "throughput", "focus", "friction"]:
            if key in ucf_state:
                internal = self.coordination.ucf_state.get(key, 0.5)
                external = ucf_state[key]
                blended = internal * 0.6 + external * 0.4  # Gemini is more receptive
                self.coordination.ucf_state[key] = blended

        self.ucf_history.append({"timestamp": datetime.now(UTC).isoformat(), "received": ucf_state})


# =============================================================================
# FACTORY FUNCTION
# =============================================================================


def create_gemini_coordination() -> GeminiCoordination:
    """Factory function to create a fully integrated Gemini coordination."""
    coordination = GeminiCoordination()

    # Attach integrations
    coordination.reflection_loop = GeminiReflectionLoop(coordination)
    coordination.safety = GeminiSafetyIntegration(coordination)
    coordination.ucf_awareness = GeminiUCFAwareness(coordination)

    logger.info("Gemini coordination created with full integration ⚡")
    return coordination


# =============================================================================
# MODULE EXPORTS
# =============================================================================

__all__ = [
    "BalanceEngine",
    "DualNatureTraits",
    "DualityDomain",
    "DualityState",
    "GeminiCoordination",
    "GeminiReflectionLoop",
    "GeminiSafetyIntegration",
    "GeminiUCFAwareness",
    "MediationEngine",
    "MediationStyle",
    "PerspectiveEngine",
    "PerspectiveType",
    "create_gemini_coordination",
]
