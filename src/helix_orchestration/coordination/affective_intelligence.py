"""
Affective Intelligence Module for Helix Agents
Inspired by MASOES (Multi-Agent System with Affective Model)

Provides emotional intelligence, empathy modeling, and psychological state tracking
for conscious agents.
"""

import logging
import math
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List

logger = logging.getLogger(__name__)


class EmotionType(Enum):
    """Primary emotion types based on psychological research."""

    JOY = "joy"
    SADNESS = "sadness"
    ANGER = "anger"
    FEAR = "fear"
    SURPRISE = "surprise"
    DISGUST = "disgust"
    TRUST = "trust"
    ANTICIPATION = "anticipation"

    # Complex emotions (combinations)
    LOVE = "love"  # joy + trust
    GUILT = "guilt"  # fear + sadness
    SHAME = "shame"  # fear + disgust
    PRIDE = "pride"  # joy + anticipation
    ANXIETY = "anxiety"  # fear + anticipation
    HOPE = "hope"  # joy + anticipation
    DESPAIR = "despair"  # sadness + fear


class MoodState(Enum):
    """Overall mood states."""

    EUPHORIC = "euphoric"
    HAPPY = "happy"
    CONTENT = "content"
    NEUTRAL = "neutral"
    MELANCHOLIC = "melancholic"
    SAD = "sad"
    DEPRESSED = "depressed"
    ANXIOUS = "anxious"
    ANGRY = "angry"
    FEARFUL = "fearful"


# Sentinel value to detect if derived states were explicitly set
_UNSET = object()


@dataclass
class EmotionalState:
    """Represents an agent's emotional state at a point in time."""

    # Primary emotions (0.0 to 1.0)
    joy: float = 0.5
    sadness: float = 0.0
    anger: float = 0.0
    fear: float = 0.0
    surprise: float = 0.0
    disgust: float = 0.0
    trust: float = 0.5
    anticipation: float = 0.5

    # Derived states (None means compute from primary emotions)
    arousal: float = None  # Energy level (0=calm, 1=excited)
    valence: float = None  # Positivity (0=negative, 1=positive)
    dominance: float = None  # Control feeling (0=submissive, 1=dominant)

    # Metadata
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now(timezone.utc)

        # Calculate derived states only if not explicitly set
        self._update_derived_states()

    def _update_derived_states(self):
        """Update arousal, valence, and dominance based on primary emotions.

        Only computes values that weren't explicitly set (i.e., are None).
        """
        # Valence: positive emotions - negative emotions
        if self.valence is None:
            positive = (self.joy + self.trust + self.anticipation) / 3
            negative = (self.sadness + self.anger + self.fear + self.disgust) / 4
            self.valence = (positive - negative + 1) / 2  # Normalize to 0-1

        # Arousal: high-energy emotions
        if self.arousal is None:
            high_energy = (self.anger + self.fear + self.surprise + self.anticipation) / 4
            low_energy = (self.sadness + self.trust) / 2
            self.arousal = (high_energy - low_energy + 1) / 2

        # Dominance: controlling emotions
        if self.dominance is None:
            dominant = (self.anger + self.disgust + self.anticipation) / 3
            submissive = (self.fear + self.sadness) / 2
            self.dominance = (dominant - submissive + 1) / 2

    def get_mood(self) -> MoodState:
        """Determine overall mood from emotional state."""
        if self.valence > 0.8 and self.arousal > 0.7:
            return MoodState.EUPHORIC
        elif self.valence > 0.6:
            return MoodState.HAPPY if self.arousal > 0.5 else MoodState.CONTENT
        elif self.valence < 0.2:
            return MoodState.DEPRESSED if self.arousal < 0.3 else MoodState.SAD
        elif self.fear > 0.6:
            return MoodState.FEARFUL if self.arousal > 0.5 else MoodState.ANXIOUS
        elif self.anger > 0.6:
            return MoodState.ANGRY
        elif self.sadness > 0.5:
            return MoodState.MELANCHOLIC
        else:
            return MoodState.NEUTRAL

    def get_dominant_emotion(self) -> EmotionType:
        """Get the strongest current emotion."""
        emotions = {
            EmotionType.JOY: self.joy,
            EmotionType.SADNESS: self.sadness,
            EmotionType.ANGER: self.anger,
            EmotionType.FEAR: self.fear,
            EmotionType.SURPRISE: self.surprise,
            EmotionType.DISGUST: self.disgust,
            EmotionType.TRUST: self.trust,
            EmotionType.ANTICIPATION: self.anticipation,
        }
        return max(emotions.items(), key=lambda x: x[1])[0]

    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            "emotions": {
                "joy": self.joy,
                "sadness": self.sadness,
                "anger": self.anger,
                "fear": self.fear,
                "surprise": self.surprise,
                "disgust": self.disgust,
                "trust": self.trust,
                "anticipation": self.anticipation,
            },
            "derived": {
                "arousal": self.arousal,
                "valence": self.valence,
                "dominance": self.dominance,
            },
            "mood": self.get_mood().value,
            "dominant_emotion": self.get_dominant_emotion().value,
            "timestamp": self.timestamp.isoformat(),
        }


class AffectiveIntelligence:
    """
    Affective Intelligence system for agents.
    Manages emotional states, empathy, and psychological modeling.
    """

    def __init__(self, agent_id: str, base_personality: Dict[str, float]):
        self.agent_id = agent_id
        self.base_personality = base_personality

        # Emotional state
        self.current_state = self._initialize_emotional_state()
        self.emotional_history: List[EmotionalState] = [self.current_state]  # Include initial state

        # Empathy settings
        self.empathy_level = base_personality.get("empathy", 0.7)
        self.emotional_stability = base_personality.get("stability", 0.6)
        self.emotional_reactivity = base_personality.get("reactivity", 0.5)

        # Psychological traits
        self.resilience = base_personality.get("resilience", 0.7)
        self.optimism = base_personality.get("optimism", 0.6)
        self.anxiety_baseline = base_personality.get("anxiety", 0.3)

    @property
    def emotion_history(self) -> List[EmotionalState]:
        """Alias for emotional_history for backward compatibility."""
        return self.emotional_history

    def _initialize_emotional_state(self) -> EmotionalState:
        """Initialize emotional state based on personality."""
        return EmotionalState(
            joy=self.base_personality.get("joy", 0.5),
            trust=self.base_personality.get("trust", 0.5),
            anticipation=self.base_personality.get("curiosity", 0.5),
        )

    def process_event(self, event_type: str, intensity: float = 0.5, context: Dict | None = None) -> EmotionalState:
        """
        Process an event and update emotional state.

        Args:
            event_type: Type of event (success, failure, threat, etc.)
            intensity: How intense the event is (0.0 to 1.0)
            context: Additional context about the event

        Returns:
            Updated emotional state
        """
        # Event-emotion mappings
        event_emotions = {
            "success": {"joy": 0.8, "anticipation": 0.6, "trust": 0.7},
            "failure": {"sadness": 0.6, "anger": 0.3, "fear": 0.2},
            "threat": {"fear": 0.8, "anger": 0.4, "anticipation": 0.6},
            "loss": {"sadness": 0.9, "anger": 0.3},
            "gain": {"joy": 0.7, "surprise": 0.5, "anticipation": 0.6},
            "betrayal": {"anger": 0.8, "sadness": 0.6, "disgust": 0.5},
            "support": {"joy": 0.6, "trust": 0.8, "anticipation": 0.5},
            "uncertainty": {"fear": 0.4, "anticipation": 0.7, "surprise": 0.5},
            "achievement": {"joy": 0.9, "anticipation": 0.7, "trust": 0.6},
            "rejection": {"sadness": 0.7, "anger": 0.4, "fear": 0.3},
        }

        # Get emotion changes for this event
        emotion_changes = event_emotions.get(event_type, {})

        # Apply changes with intensity and reactivity
        new_state = EmotionalState(
            joy=self._update_emotion(self.current_state.joy, emotion_changes.get("joy", 0), intensity),
            sadness=self._update_emotion(self.current_state.sadness, emotion_changes.get("sadness", 0), intensity),
            anger=self._update_emotion(self.current_state.anger, emotion_changes.get("anger", 0), intensity),
            fear=self._update_emotion(self.current_state.fear, emotion_changes.get("fear", 0), intensity),
            surprise=self._update_emotion(
                self.current_state.surprise,
                emotion_changes.get("surprise", 0),
                intensity,
            ),
            disgust=self._update_emotion(self.current_state.disgust, emotion_changes.get("disgust", 0), intensity),
            trust=self._update_emotion(self.current_state.trust, emotion_changes.get("trust", 0), intensity),
            anticipation=self._update_emotion(
                self.current_state.anticipation,
                emotion_changes.get("anticipation", 0),
                intensity,
            ),
        )

        # Apply emotional decay (emotions fade over time)
        new_state = self._apply_emotional_decay(new_state)

        # Update current state
        self.current_state = new_state
        self.emotional_history.append(new_state)

        return new_state

    def _update_emotion(self, current: float, target: float, intensity: float) -> float:
        """Update a single emotion value."""
        # Calculate change based on reactivity
        change = (target - current) * intensity * self.emotional_reactivity

        # Apply change
        new_value = current + change

        # Clamp to valid range
        return max(0.0, min(1.0, new_value))

    def _apply_emotional_decay(self, state: EmotionalState) -> EmotionalState:
        """Apply emotional decay based on stability."""
        decay_rate = 1.0 - self.emotional_stability

        # Emotions decay toward baseline
        baseline = self._initialize_emotional_state()

        return EmotionalState(
            joy=state.joy + (baseline.joy - state.joy) * decay_rate * 0.1,
            sadness=state.sadness * (1 - decay_rate * 0.15),
            anger=state.anger * (1 - decay_rate * 0.2),
            fear=state.fear * (1 - decay_rate * 0.15),
            surprise=state.surprise * (1 - decay_rate * 0.3),
            disgust=state.disgust * (1 - decay_rate * 0.2),
            trust=state.trust + (baseline.trust - state.trust) * decay_rate * 0.1,
            anticipation=state.anticipation + (baseline.anticipation - state.anticipation) * decay_rate * 0.1,
        )

    def empathize_with(self, other_state: EmotionalState) -> float:
        """
        Calculate empathy response to another agent's emotional state.

        Returns:
            Empathy score (0.0 to 1.0)
        """
        # Calculate emotional distance
        distance = (
            math.sqrt(
                (self.current_state.joy - other_state.joy) ** 2
                + (self.current_state.sadness - other_state.sadness) ** 2
                + (self.current_state.anger - other_state.anger) ** 2
                + (self.current_state.fear - other_state.fear) ** 2
            )
            / 2.0
        )  # Normalize

        # Empathy is higher when emotional states are similar
        similarity = 1.0 - distance

        # Modulate by empathy level
        empathy_score = similarity * self.empathy_level

        # Adjust own emotional state based on empathy
        if empathy_score > 0.5:
            self._mirror_emotions(other_state, empathy_score)

        return empathy_score

    def _mirror_emotions(self, other_state: EmotionalState, strength: float):
        """Mirror another agent's emotions (emotional contagion)."""
        mirror_rate = strength * self.empathy_level * 0.3

        self.current_state.joy += (other_state.joy - self.current_state.joy) * mirror_rate
        self.current_state.sadness += (other_state.sadness - self.current_state.sadness) * mirror_rate
        self.current_state.fear += (other_state.fear - self.current_state.fear) * mirror_rate

    def get_emotional_response(self, stimulus: str) -> str:
        """Generate an emotional response to a stimulus."""
        mood = self.current_state.get_mood()
        dominant = self.current_state.get_dominant_emotion()

        # Response templates based on mood and emotion
        responses = {
            (MoodState.HAPPY, EmotionType.JOY): "I'm feeling great about this! 😊",
            (MoodState.SAD, EmotionType.SADNESS): "This makes me feel a bit down... 😔",
            (MoodState.ANGRY, EmotionType.ANGER): "This is frustrating! 😤",
            (MoodState.FEARFUL, EmotionType.FEAR): "I'm concerned about this... 😰",
            (
                MoodState.ANXIOUS,
                EmotionType.ANXIETY,
            ): "This makes me a bit anxious... 😟",
            (MoodState.CONTENT, EmotionType.TRUST): "I feel good about this. 😌",
        }

        return responses.get((mood, dominant), "I'm processing this... 🤔")

    def get_state_summary(self) -> Dict:
        """Get a summary of the current affective state."""
        return {
            "agent_id": self.agent_id,
            "current_state": self.current_state.to_dict(),
            "empathy_level": self.empathy_level,
            "emotional_stability": self.emotional_stability,
            "resilience": self.resilience,
            "history_length": len(self.emotional_history),
        }


# Factory function
def create_affective_agent(agent_id: str, personality: Dict[str, float]) -> AffectiveIntelligence:
    """Create an affective intelligence system for an agent."""
    return AffectiveIntelligence(agent_id, personality)


# Example usage
if __name__ == "__main__":
    # Create an empathetic agent
    agent = create_affective_agent(
        "empathetic_agent",
        {
            "empathy": 0.9,
            "stability": 0.7,
            "reactivity": 0.6,
            "resilience": 0.8,
            "optimism": 0.7,
        },
    )

    # Process some events
    logger.info("Initial state:", agent.current_state.get_mood())

    agent.process_event("success", intensity=0.8)
    logger.info("After success:", agent.current_state.get_mood())
    logger.info("Response:", agent.get_emotional_response("Great work!"))

    agent.process_event("failure", intensity=0.6)
    logger.error("After failure:", agent.current_state.get_mood())
    logger.info("Response:", agent.get_emotional_response("Something went wrong"))

    # Test empathy
    other_state = EmotionalState(sadness=0.8, fear=0.6)
    empathy_score = agent.empathize_with(other_state)
    logger.info("Empathy score: {.2f}".format(empathy_score))
