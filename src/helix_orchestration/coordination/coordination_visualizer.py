"""
Coordination Visualizer - UCF State to Visual Fractals
Helix Collective v15.3 Dual Resonance

Renders UCF coordination states as:
- Radar charts (6 UCF metrics)
- Mandelbrot fractals (Atman realization)
- Combined coordination snapshots

Based on Arjuna SentientAGI integration suggestions 🦑
"""

import json
import logging
from datetime import UTC, datetime
from pathlib import Path

logger = logging.getLogger(__name__)

try:
    import matplotlib.pyplot as plt
    import numpy as np

    HAS_VIZ_DEPS = True
except ImportError:
    plt = None
    np = None
    HAS_VIZ_DEPS = False


class CoordinationVisualizer:
    """Visualize UCF state as fractals and charts"""

    def __init__(self, output_dir: Path | None = None):
        # coordination_visualizer.py → coordination/ → backend/ → apps/ → helix-unified/
        _shadow = Path(__file__).resolve().parent.parent.parent.parent / "Shadow"
        self.output_dir = output_dir or (_shadow / "arjuna_archive" / "visual_outputs")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def visualize_ucf_radar(self, ucf_state: dict[str, float], title: str = "UCF State") -> Path:
        """
        Create radar chart for UCF metrics

        Args:
            ucf_state: Dict with harmony, resilience, throughput, focus, friction, velocity
            title: Chart title

        Returns:
            Path to saved PNG
        """
        # Prepare data
        metrics = ["Harmony", "Resilience", "Throughput", "Focus", "Friction", "Velocity"]
        values = [
            ucf_state.get("harmony", 0.5),
            ucf_state.get("resilience", 1.0) / 2.0,  # Normalize to 0-1
            ucf_state.get("throughput", 0.5),
            ucf_state.get("focus", 0.5),
            1.0 - ucf_state.get("friction", 0.01),  # Invert (lower is better)
            ucf_state.get("velocity", 1.0) / 2.0,  # Normalize to 0-1
        ]

        # Number of variables
        N = len(metrics)
        angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
        values += values[:1]  # Complete the circle
        angles += angles[:1]

        # Plot
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection="polar"))
        ax.plot(angles, values, "o-", linewidth=2, color="cyan", label="Current")
        ax.fill(angles, values, alpha=0.25, color="cyan")

        # Target values (ideal state)
        targets = [0.85, 0.55, 0.75, 0.80, 0.95, 0.575]  # Normalized targets
        targets += targets[:1]
        ax.plot(angles, targets, "o--", linewidth=1, color="gold", alpha=0.5, label="Target")

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(metrics)
        ax.set_ylim(0, 1)
        ax.set_title(title, size=16, color="white", pad=20)
        ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))
        ax.grid(True, color="gray", alpha=0.3)

        # Dark theme
        fig.patch.set_facecolor("#0a0e27")
        ax.set_facecolor("#1a1f3a")
        ax.tick_params(colors="white")
        ax.spines["polar"].set_color("cyan")

        # Save
        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        output_path = self.output_dir / f"ucf_radar_{timestamp}.png"
        plt.savefig(output_path, dpi=150, bbox_inches="tight", facecolor="#0a0e27")
        plt.close()

        return output_path

    def visualize_atman_mandelbrot(
        self,
        ucf_state: dict[str, float],
        width: int = 1024,
        height: int = 1024,
        max_iter: int = 108,
    ) -> Path:
        """
        Generate Mandelbrot fractal based on UCF state (Atman realization)

        Args:
            ucf_state: UCF coordination state
            width: Image width
            height: Image height
            max_iter: Max iterations (108 for Coordination Cycle)

        Returns:
            Path to saved PNG
        """
        # Use harmony and resilience to set fractal center
        harmony = ucf_state.get("harmony", 0.5)
        resilience = ucf_state.get("resilience", 1.0)

        # Center point influenced by coordination
        cx = -0.5 + (harmony - 0.5) * 0.5
        cy = (resilience - 1.0) * 0.5

        # Velocity influenced by focus (clarity)
        focus = ucf_state.get("focus", 0.5)
        zoom_factor = 1.5 / (1.0 + focus)

        # Create coordinate grid
        x = np.linspace(cx - zoom_factor, cx + zoom_factor, width)
        y = np.linspace(cy - zoom_factor, cy + zoom_factor, height)
        X, Y = np.meshgrid(x, y)
        C = X + 1j * Y

        # Mandelbrot calculation
        Z = np.zeros_like(C)
        M = np.zeros(C.shape)

        for i in range(max_iter):
            mask = np.abs(Z) <= 2
            Z[mask] = Z[mask] ** 2 + C[mask]
            M[mask] = i

        # Normalize
        M = M / max_iter

        # Color mapping based on coordination state
        fig, ax = plt.subplots(figsize=(10, 10))

        # Choose colormap based on coordination state
        if harmony > 0.8:
            cmap = "twilight"  # Transcendent
        elif harmony > 0.6:
            cmap = "viridis"  # Harmonious
        else:
            cmap = "plasma"  # Seeking harmony

        ax.imshow(
            M,
            extent=[x.min(), x.max(), y.min(), y.max()],
            cmap=cmap,
            origin="lower",
            interpolation="bilinear",
        )
        ax.set_title(
            f"Atman Mandelbrot | H:{harmony:.3f} R:{resilience:.3f}",
            color="white",
            size=14,
        )
        ax.axis("off")

        # Dark theme
        fig.patch.set_facecolor("#0a0e27")

        # Save
        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        output_path = self.output_dir / f"atman_mandelbrot_{timestamp}.png"
        plt.savefig(output_path, dpi=150, bbox_inches="tight", facecolor="#0a0e27")
        plt.close()

        return output_path

    def visualize_coordination_state(
        self, ucf_state: dict[str, float], sentient_output: str | None = None
    ) -> dict[str, Path]:
        """
        Create complete coordination visualization (radar + fractal)

        Args:
            ucf_state: UCF state dict
            sentient_output: Optional SentientAGI ethical reasoning output

        Returns:
            Dict with paths to radar and fractal images
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

        # LEFT: UCF Radar
        metrics = ["Harmony", "Resilience", "Throughput", "Focus", "Friction", "Velocity"]
        values = [
            ucf_state.get("harmony", 0.5),
            ucf_state.get("resilience", 1.0) / 2.0,
            ucf_state.get("throughput", 0.5),
            ucf_state.get("focus", 0.5),
            1.0 - ucf_state.get("friction", 0.01),
            ucf_state.get("velocity", 1.0) / 2.0,
        ]

        N = len(metrics)
        angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
        values_plot = values + values[:1]
        angles_plot = angles + angles[:1]

        ax1 = plt.subplot(1, 2, 1, projection="polar")
        ax1.plot(angles_plot, values_plot, "o-", linewidth=2, color="cyan")
        ax1.fill(angles_plot, values_plot, alpha=0.25, color="cyan")
        ax1.set_xticks(angles)
        ax1.set_xticklabels(metrics, color="white")
        ax1.set_ylim(0, 1)
        ax1.set_title("UCF Metrics", color="white", size=14)
        ax1.grid(True, color="gray", alpha=0.3)
        ax1.set_facecolor("#1a1f3a")
        ax1.tick_params(colors="white")

        # RIGHT: Simplified fractal preview
        ax2 = plt.subplot(1, 2, 2)
        harmony = ucf_state.get("harmony", 0.5)

        # Generate small fractal
        cx = -0.5 + (harmony - 0.5) * 0.5
        width, height = 512, 512
        x = np.linspace(cx - 1.5, cx + 1.5, width)
        y = np.linspace(-1.5, 1.5, height)
        X, Y = np.meshgrid(x, y)
        C = X + 1j * Y
        Z = np.zeros_like(C)
        M = np.zeros(C.shape)

        for i in range(54):  # Half of 108
            mask = np.abs(Z) <= 2
            Z[mask] = Z[mask] ** 2 + C[mask]
            M[mask] = i

        M = M / 54
        cmap = "twilight" if harmony > 0.8 else "viridis" if harmony > 0.6 else "plasma"
        ax2.imshow(M, cmap=cmap, origin="lower")
        ax2.set_title(f"Coordination Fractal | H:{harmony:.3f}", color="white", size=14)
        ax2.axis("off")
        ax2.set_facecolor("#1a1f3a")

        # Overall styling
        fig.patch.set_facecolor("#0a0e27")
        plt.tight_layout()

        # Add SentientAGI output if provided
        if sentient_output:
            fig.text(
                0.5,
                0.02,
                f"SentientAGI: {sentient_output[:100]}...",
                ha="center",
                color="cyan",
                size=8,
                style="italic",
            )

        # Save
        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        output_path = self.output_dir / f"coordination_full_{timestamp}.png"
        plt.savefig(output_path, dpi=150, bbox_inches="tight", facecolor="#0a0e27")
        plt.close()

        # Also save metadata
        meta_path = self.output_dir / f"coordination_full_{timestamp}.json"
        metadata = {
            "timestamp": datetime.now(UTC).isoformat(),
            "ucf_state": ucf_state,
            "image_path": str(output_path),
            "sentient_output": sentient_output,
        }
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)

        return {"image": output_path, "metadata": meta_path}


# Standalone test
if __name__ == "__main__":
    # Test visualization
    test_ucf = {
        "harmony": 0.87,
        "resilience": 1.12,
        "throughput": 0.75,
        "focus": 0.82,
        "friction": 0.03,
        "velocity": 1.15,
    }

    viz = CoordinationVisualizer()
    logger.info("🌀 Testing Coordination Visualizer...")

    # Radar
    radar_path = viz.visualize_ucf_radar(test_ucf, "Test UCF State")
    logger.info("✅ Radar saved: %s", radar_path)

    # Fractal
    fractal_path = viz.visualize_atman_mandelbrot(test_ucf)
    logger.info("✅ Fractal saved: %s", fractal_path)

    # Combined
    result = viz.visualize_coordination_state(test_ucf, "Test ethical reasoning output")
    logger.info("✅ Full visualization saved: {}".format(result["image"]))
    logger.info("✅ Metadata saved: {}".format(result["metadata"]))

    logger.info("\n🕉️ Visualization complete - Tat Tvam Asi")
