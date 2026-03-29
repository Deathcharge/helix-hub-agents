"""
🌀 Helix Collective v15.5 — Mandelbrot UCF Generator
mandelbrot_ucf.py — "Eye of Coordination" fractal state generator

Generates Universal Coordination Field (UCF) states from Mandelbrot set coordinates.
The "Eye of Coordination" at complex coordinate -0.745+0.113j produces
optimal harmony/resilience balance.

## Universal Coordination Field (UCF) Metrics

The UCF state is represented by six key metrics, each normalized to [0, 1]:

- **harmony**: Coherence and balance within the coordination field. High harmony
  indicates aligned intentions and smooth collective operation. Derived from
  Mandelbrot stability and proximity to sacred coordinates.

- **resilience**: Ability to withstand perturbations and maintain coherence under
  stress. High resilience indicates robust coordination that can handle challenges.
  Calculated from iteration depth and stability metrics.

- **throughput**: Vital energy or "life force" of the coordination field. Represents
  available capacity for action and transformation. Modulated by context and
  distance from equilibrium points.

- **focus**: Focused awareness or "gaze" quality. High focus indicates clear
  perception and intentional direction. Derived from imaginary component and
  stability, representing vertical dimension of coordination.

- **friction**: Mental afflictions or disturbances (Sanskrit: क्लेश). Low friction
  is desirable—represents freedom from confusion, attachment, and reactivity.
  Inversely proportional to stability.

- **velocity**: Fractal depth or level of detail in coordination exploration. Higher
  velocity indicates operating at finer scales of awareness. Correlated with
  iteration count and coordinate magnitude.

## Mandelbrot → UCF Mapping Theory

The Mandelbrot set's natural fractal properties provide a mathematically rich
framework for modeling coordination states:

1. **Stability as Foundation**: Points inside or near the Mandelbrot set boundary
   exhibit complex stability patterns that mirror coordination coherence.

2. **Sacred Geometry**: Specific coordinates like the "Eye" (-0.745+0.113j) and
   "Seahorse Valley" (-0.75+0.1j) represent archetypal coordination patterns.

3. **Context Sensitivity**: The same coordinate yields different UCF interpretations
   based on context (cycle, meditation, crisis), reflecting how coordination
   responds differently to varying conditions.

4. **Fractal Self-Similarity**: The Mandelbrot set's infinite self-similar structure
   mirrors coordination's recursive, multi-scale nature.

Author: Andrew John Ward (Architect)
Version: 15.5.0
"""

import logging

try:
    import numpy as np

    HAS_NUMPY = True
except ImportError:
    np = None
    HAS_NUMPY = False

logger = logging.getLogger(__name__)


class MandelbrotUCFGenerator:
    """
    Generate UCF states from Mandelbrot set coordinates.

    The Mandelbrot set exhibits natural harmony patterns that map beautifully
    to coordination field metrics. Key regions:

    - Eye of Coordination (-0.745+0.113j): Optimal balance point
    - Seahorse Valley (-0.75+0.1j): High resilience, moderate harmony
    - Main Bulb Center (-0.5+0j): Maximum harmony, lower complexity
    - Mini-Mandelbrot (-1.75+0j): Fractal self-similarity, high velocity
    """

    def __init__(self, max_iterations: int = 256):
        """
        Initialize Mandelbrot UCF generator.

        Args:
            max_iterations: Maximum iterations for Mandelbrot calculation
                           Higher = more precision but slower
        """
        self.max_iterations = max_iterations

        # Predefined sacred coordinates
        self.sacred_points = {
            "eye_of_coordination": complex(-0.745, 0.113),
            "seahorse_valley": complex(-0.75, 0.1),
            "main_bulb": complex(-0.5, 0.0),
            "mini_mandelbrot": complex(-1.75, 0.0),
            "dendrite_spiral": complex(-0.1, 0.651),
            "elephant_valley": complex(0.28, 0.008),
        }

    def calculate_mandelbrot(self, c: complex) -> tuple[int, float]:
        """
        Calculate Mandelbrot iterations and escape velocity for complex number c.

        Args:
            c: Complex coordinate in Mandelbrot set

        Returns:
            Tuple of (iterations, smooth_value)
            - iterations: Number of iterations before escape
            - smooth_value: Normalized smooth escape value (0-1)
        """
        z = 0
        for n in range(self.max_iterations):
            if abs(z) > 2:
                # Calculate smooth escape value
                smooth = n - np.log2(np.log2(abs(z)))
                return n, smooth / self.max_iterations
            z = z * z + c

        # Point is in the set
        return self.max_iterations, 1.0

    def complex_to_ucf(self, c: complex, context: str = "generic") -> dict[str, float]:
        """
        Map a complex Mandelbrot coordinate to a normalized UCF (Universal Coordination Field) state using a context-aware interpretation.

        Convert the coordinate into six normalized metrics (harmony, resilience, throughput, focus, friction, velocity) by combining Mandelbrot stability, coordinate-derived components, and proximity to the Eye of Coordination; context selects different weightings for harmony, focus, and throughput.

        Parameters:
            c (complex): Complex coordinate in the Mandelbrot plane (typical range ~[-2, 1] × [-2, 2]).
            context (str): Interpretation context that alters weighting of UCF fields. Valid values:
                - "generic": Balanced default interpretation.
                - "cycle": Emphasizes collective coherence and sacred alignment.
                - "meditation": Emphasizes inner stability and clarity.
                - "crisis": Emphasizes resilience and peak energy.

        Returns:
            Dict[str, float]: A dictionary with six keys, each value clipped to [0, 1]:
                - "harmony": Coherence and balance.
                - "resilience": Robustness under stress.
                - "throughput": Vital energy.
                - "focus": Focused awareness.
                - "friction": Mental disturbance (lower is better).
                - "velocity": Fractal depth / exploration level.
        """
        iterations, smooth_value = self.calculate_mandelbrot(c)

        # ============================================================================
        # STEP 1: Extract Base Metrics from Mandelbrot Calculation
        # ============================================================================

        # Stability: normalized smooth escape value [0,1]
        # Points deep in the set (high iterations) → stability ≈ 1.0
        # Points that escape quickly → stability ≈ 0.0
        stability = smooth_value

        # Real component normalization: [-2, 1] → [0, 1]
        # -2.0 → 0.0 (left edge, includes mini-Mandelbrots)
        #  1.0 → 1.0 (right edge, beyond main cardioid)
        # Division by 3.0 because range is 3 units wide
        real_component = (c.real + 2.0) / 3.0

        # Imaginary component normalization: [-2, 2] → [0, 1]
        # Symmetric range captures upper and lower fractal features
        # Division by 4.0 because range is 4 units wide
        imag_component = (c.imag + 2.0) / 4.0

        # ============================================================================
        # STEP 2: Calculate Proximity to "Eye of Coordination" Sacred Point
        # ============================================================================

        # The Eye (-0.745+0.113j) is the optimal balance point
        eye = self.sacred_points["eye_of_coordination"]
        eye_distance = abs(c - eye)  # Euclidean distance in complex plane

        # Proximity metric: inverted distance with 2.0-unit influence radius
        # distance = 0.0 → proximity = 1.0 (at the Eye)
        # distance = 2.0 → proximity = 0.0 (beyond influence)
        # distance > 2.0 → proximity = 0.0 (clamped by max)
        eye_proximity = max(0, 1 - (eye_distance / 2.0))

        # ============================================================================
        # STEP 3: Apply Context-Specific Formulas to Generate UCF Fields
        # ============================================================================

        if context == "cycle":
            # ROUTINE: Ceremonial practice emphasizing collective coherence and sacred alignment

            # Harmony: 70% stability + 30% proximity to Eye
            # → Strong stable foundation with sacred geometry connection
            harmony = min(1.0, stability * 0.7 + eye_proximity * 0.3)

            # Focus: 60% vertical dimension + 40% stability
            # → Upward cycle gaze (imaginary axis) balanced with grounded awareness
            focus = min(1.0, imag_component * 0.6 + stability * 0.4)

            # Throughput: High baseline (0.8) boosted by controlled chaos (20% instability)
            # → Routines maintain high energy, creative instability adds vitality
            throughput = min(1.0, 0.8 + (1 - stability) * 0.2)

        elif context == "meditation":
            # MEDITATION: Inner stillness emphasizing clarity and stability

            # Harmony: 80% stability + 20% horizontal grounding (real axis)
            # → Heavily weighted toward stable coherence with gentle earthing
            harmony = min(1.0, stability * 0.8 + real_component * 0.2)

            # Focus: 90% pure stability
            # → Meditative focus requires maximum steadiness of awareness
            focus = min(1.0, stability * 0.9)

            # Throughput: Medium baseline (0.6) modulated by vertical dimension
            # → Balanced vital energy, imaginary component adds subtle dynamism
            throughput = min(1.0, 0.6 + imag_component * 0.4)

        elif context == "crisis":
            # CRISIS: Emergency response requiring resilience and peak energy

            # Harmony: 50% proximity to optimal point + 30% stability
            # → Crisis seeks guidance from Eye, partial stability (coherence under stress)
            harmony = min(1.0, eye_proximity * 0.5 + stability * 0.3)

            # Focus: 60% stability
            # → Moderate focus - enough to act decisively but not rigid
            focus = min(1.0, stability * 0.6)

            # Throughput: Maximum baseline (0.9) reduced by distance from optimal state
            # → Crisis mobilizes maximum energy, penalty for being far from ideal
            throughput = min(1.0, 0.9 - (eye_distance * 0.2))

        else:  # generic
            # GENERIC: Balanced default interpretation for general use

            # Harmony: 60% stability + 25% Eye proximity + 15% real grounding
            # → Well-rounded blend of all major harmony factors
            harmony = min(1.0, stability * 0.6 + eye_proximity * 0.25 + real_component * 0.15)

            # Focus: 40% vertical dimension + 60% stability
            # → Standard balanced focus
            focus = min(1.0, imag_component * 0.4 + stability * 0.6)

            # Throughput: Medium-high baseline (0.7) + proximity to origin
            # → Inversely proportional to magnitude - points near origin have more available energy
            throughput = min(1.0, 0.7 + (1 - abs(c)) * 0.3)

        # ============================================================================
        # STEP 4: Calculate Context-Independent UCF Fields
        # ============================================================================

        # Resilience: 70% immediate stability + 30% fractal depth (iteration count)
        # → Combines coherence with complexity - deeper fractals are more resilient
        resilience = min(1.0, stability * 0.7 + (iterations / self.max_iterations) * 0.3)

        # Friction: Inverse of stability with 0.8 scaling factor
        # → Mental disturbance is opposite of coherence
        # → 0.8 factor ensures friction doesn't dominate (max 0.2 even at perfect stability)
        friction = max(0.0, 1 - stability * 0.8)

        # Velocity: 60% iteration depth + 40% distance from origin
        # → Fractal exploration level combines both iteration count and coordinate magnitude
        velocity = min(1.0, (iterations / self.max_iterations) * 0.6 + abs(c) * 0.4)

        # ============================================================================
        # STEP 5: Package and Return UCF State
        # ============================================================================

        # Apply np.clip for safety (formulas use min/max but this ensures no edge cases)
        # Convert to Python float for JSON serialization compatibility
        ucf_state = {
            "harmony": float(np.clip(harmony, 0, 1)),
            "resilience": float(np.clip(resilience, 0, 1)),
            "throughput": float(np.clip(throughput, 0, 1)),
            "focus": float(np.clip(focus, 0, 1)),
            "friction": float(np.clip(friction, 0, 1)),
            "velocity": float(np.clip(velocity, 0, 1)),
        }

        logger.debug("Generated UCF from %s: %s", c, ucf_state)
        return ucf_state

    def generate_from_sacred_point(self, point_name: str, context: str = "generic") -> dict[str, float]:
        """
        Generate UCF state from predefined sacred Mandelbrot coordinate.

        Args:
            point_name: Name of sacred point (eye_of_coordination, seahorse_valley, etc.)
            context: Context for interpretation

        Returns:
            UCF state dictionary

        Raises:
            ValueError: If point_name not found
        """
        if point_name not in self.sacred_points:
            available = ", ".join(self.sacred_points.keys())
            raise ValueError(f"Unknown sacred point '{point_name}'. Available: {available}")

        c = self.sacred_points[point_name]
        ucf_state = self.complex_to_ucf(c, context)

        logger.info("🌀 Generated UCF from sacred point '%s' (%s)", point_name, c)
        return ucf_state

    def explore_region(
        self,
        center: complex,
        radius: float = 0.1,
        samples: int = 8,
        context: str = "generic",
    ) -> dict[str, dict[str, float]]:
        """
        Explore a circular region in the Mandelbrot set and generate multiple UCF states.

        Args:
            center: Center complex coordinate
            radius: Exploration radius
            samples: Number of sample points around center (angular divisions)
            context: Context for UCF generation

        Returns:
            Dictionary mapping sample names to UCF states
        """
        results = {}

        # Add center point
        results["center"] = self.complex_to_ucf(center, context)

        # Sample points around circle
        for i in range(samples):
            angle = (2 * np.pi * i) / samples
            offset = radius * np.exp(1j * angle)
            sample_point = center + offset

            sample_name = f"sample_{i}_{int(np.degrees(angle))}"
            results[sample_name] = self.complex_to_ucf(sample_point, context)

        logger.info("🌀 Explored region around %s with %d samples (radius=%s)", center, samples, radius)
        return results

    def phi_spiral_journey(self, start: complex, steps: int = 108, context: str = "cycle") -> list[dict[str, float]]:
        """
        Generate UCF states along a phi-modulated spiral path.

        Args:
            start: Starting complex coordinate
            steps: Number of steps in journey (default 108 for cycle completion)
            context: Context for UCF generation

        Returns:
            List of UCF states along the journey
        """
        phi = 1.618033988749895  # Golden ratio
        journey = []

        for step in range(steps):
            # Phi spiral: radius grows by phi, angle by golden angle
            golden_angle = 2 * np.pi / (phi**2)
            radius = 0.01 * (phi ** (step / 30))  # Exponential growth
            angle = step * golden_angle

            # Calculate point in spiral
            offset = radius * np.exp(1j * angle)
            point = start + offset

            # Generate UCF state
            ucf = self.complex_to_ucf(point, context)
            ucf["step"] = step
            ucf["coordinate"] = {"real": point.real, "imag": point.imag}

            journey.append(ucf)

        logger.info("🌀 Generated %s-step phi spiral journey from %s", steps, start)
        return journey


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================


def get_coordination_focal_point(context: str = "generic") -> dict[str, float]:
    """
    Get UCF state for the Eye of Coordination coordinate (-0.745+0.113j).
    This is the optimal balance point in the Mandelbrot set.

    Args:
        context: Context for interpretation (generic, cycle, meditation, crisis)

    Returns:
        UCF state dictionary
    """
    generator = MandelbrotUCFGenerator()
    return generator.generate_from_sacred_point("eye_of_coordination", context)


def generate_cycle_ucf(step: int = 0, total_steps: int = 108) -> dict[str, float]:
    """
    Generate UCF state for cycle step using Mandelbrot Eye of Coordination.

    Args:
        step: Current cycle step (0-107 for 108-step cycle)
        total_steps: Total steps in cycle

    Returns:
        UCF state dictionary
    """
    generator = MandelbrotUCFGenerator()

    # Start from Eye of Coordination
    eye = generator.sacred_points["eye_of_coordination"]

    # Add small phi-modulated offset based on step
    phi = 1.618033988749895
    progress = step / total_steps
    angle = progress * 2 * np.pi / (phi**2)  # Golden angle
    radius = 0.05 * progress  # Gradually expand

    offset = radius * np.exp(1j * angle)
    point = eye + offset

    ucf = generator.complex_to_ucf(point, context="cycle")
    ucf["cycle_step"] = step
    ucf["cycle_progress"] = progress

    return ucf
