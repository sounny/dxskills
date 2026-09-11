"""
Multimodal Concept Hologram and Interference Pattern Weaver Engine
Autonomous cognitive spatial module computing constructive semantic wave overlaps
across multi-modal concept vectors and generating diffractive holographic webs.
Grounded in Karl Pribram holonomic brain theory, Gabor optical holography,
and Eide Interconnected Reasoning to reveal latent multidimensional conceptual synthesis.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Any
import math
import html


@dataclass
class WaveEmitter:
    """Represents a discrete multimodal concept emitting a semantic spherical wavefront."""
    emitter_id: str
    title: str
    x: float
    y: float
    amplitude: float = 1.0
    wavelength_px: float = 60.0
    phase_rad: float = 0.0
    modality: str = "SPATIAL"  # SPATIAL, STRUCTURAL, TEMPORAL, CONCEPTUAL
    color: str = "#58a6ff"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "emitter_id": self.emitter_id,
            "title": self.title,
            "x": round(self.x, 2),
            "y": round(self.y, 2),
            "amplitude": round(self.amplitude, 2),
            "wavelength_px": round(self.wavelength_px, 2),
            "phase_rad": round(self.phase_rad, 3),
            "modality": self.modality,
            "color": self.color,
        }


@dataclass
class InterferencePeak:
    """Represents a constructive semantic wave superposition node across concept fields."""
    peak_id: str
    x: float
    y: float
    intensity: float
    participating_emitters: List[str]
    resonance_type: str = "CONSTRUCTIVE"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "peak_id": self.peak_id,
            "x": round(self.x, 2),
            "y": round(self.y, 2),
            "intensity": round(self.intensity, 3),
            "participating_emitters": self.participating_emitters,
            "resonance_type": self.resonance_type,
        }


@dataclass
class HolographicTelemetry:
    """Comprehensive telemetry capturing optical wave superposition and fringe coherence."""
    total_emitters: int
    interference_peaks: List[InterferencePeak]
    peak_constructive_intensity: float
    mean_field_intensity: float
    global_coherence_index: float
    fringe_density_score: float
    status_level: str
    emitters: List[WaveEmitter]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_emitters": self.total_emitters,
            "peak_constructive_intensity": round(self.peak_constructive_intensity, 3),
            "mean_field_intensity": round(self.mean_field_intensity, 3),
            "global_coherence_index": round(self.global_coherence_index, 3),
            "fringe_density_score": round(self.fringe_density_score, 3),
            "status_level": self.status_level,
            "emitters": [e.to_dict() for e in self.emitters],
            "interference_peaks": [p.to_dict() for p in self.interference_peaks],
        }


class ConceptHologramWeaver:
    """
    Simulates optical semantic wave interference across concept emitters
    to synthesize holographic cognitive models and constructive fringe lattices.
    """

    def __init__(self, sample_grid_step: float = 35.0, coherence_threshold: float = 0.60):
        self.sample_grid_step = max(10.0, min(100.0, sample_grid_step))
        self.coherence_threshold = max(0.1, min(0.95, coherence_threshold))

    def compute_wave_field(
        self,
        emitters: List[WaveEmitter],
        width: float = 880.0,
        height: float = 580.0,
    ) -> HolographicTelemetry:
        """
        Calculates wave superposition and detects constructive interference nodes.
        Uses optical field equations:
        psi_i(r) = A_i * cos(2 * pi * d_i / lambda_i + phi_i)
        Total intensity I(r) = (sum psi_i)^2
        """
        if not emitters:
            return HolographicTelemetry(
                total_emitters=0,
                interference_peaks=[],
                peak_constructive_intensity=0.0,
                mean_field_intensity=0.0,
                global_coherence_index=0.0,
                fringe_density_score=0.0,
                status_level="DISPERSED",
                emitters=[],
            )

        intensities: List[Tuple[float, float, float, List[str]]] = []
        incoherent_sum = sum(e.amplitude * e.amplitude for e in emitters)
        theoretical_max = (sum(e.amplitude for e in emitters)) ** 2

        # Probe grid
        step = self.sample_grid_step
        x_probes = int(width // step)
        y_probes = int(height // step)

        for ix in range(1, x_probes):
            gx = ix * step
            for iy in range(1, y_probes):
                gy = iy * step
                total_amp = 0.0
                active_contributors: List[str] = []

                for em in emitters:
                    dist = math.hypot(gx - em.x, gy - em.y)
                    k = (2.0 * math.pi) / em.wavelength_px
                    wave_val = em.amplitude * math.cos(k * dist + em.phase_rad)
                    total_amp += wave_val
                    if wave_val > 0.3 * em.amplitude:
                        active_contributors.append(em.emitter_id)

                intensity = total_amp * total_amp
                intensities.append((intensity, gx, gy, active_contributors))

        if not intensities:
            mean_intensity = 0.0
            peak_intensity = 0.0
            peaks: List[InterferencePeak] = []
        else:
            mean_intensity = sum(item[0] for item in intensities) / len(intensities)
            intensities.sort(key=lambda item: item[0], reverse=True)
            peak_intensity = intensities[0][0]

            # Detect local constructive resonance peaks
            peaks = []
            peak_threshold = incoherent_sum * 1.35
            for idx, (val, px, py, contribs) in enumerate(intensities):
                if val >= peak_threshold and len(contribs) >= 2:
                    # Spatial separation check from existing peaks
                    is_distinct = True
                    for ep in peaks:
                        if math.hypot(px - ep.x, py - ep.y) < step * 1.2:
                            is_distinct = False
                            break
                    if is_distinct:
                        peaks.append(
                            InterferencePeak(
                                peak_id=f"peak-{len(peaks)+1}",
                                x=px,
                                y=py,
                                intensity=val,
                                participating_emitters=contribs,
                                resonance_type="CONSTRUCTIVE" if val > incoherent_sum * 1.8 else "HARMONIC",
                            )
                        )
                        if len(peaks) >= 8:
                            break

        coherence = min(1.0, (mean_intensity / (incoherent_sum + 1e-6)) * 0.75)
        fringe_score = min(1.0, len(peaks) / 6.0)

        if coherence >= self.coherence_threshold and len(peaks) >= 3:
            status = "HIGH_COHERENCE"
        elif len(peaks) >= 1:
            status = "RESONANT"
        else:
            status = "DISPERSED"

        return HolographicTelemetry(
            total_emitters=len(emitters),
            interference_peaks=peaks,
            peak_constructive_intensity=peak_intensity,
            mean_field_intensity=mean_intensity,
            global_coherence_index=coherence,
            fringe_density_score=fringe_score,
            status_level=status,
            emitters=emitters,
        )

    def generate_markdown_report(self, telemetry: HolographicTelemetry) -> str:
        """Builds a structured diagnostic Markdown report on holographic wave interference."""
        status_icons = {
            "HIGH_COHERENCE": "🟢",
            "RESONANT": "🟡",
            "DISPERSED": "⚪",
        }
        icon = status_icons.get(telemetry.status_level, "⚪")

        lines = [
            "# Multimodal Concept Hologram & Interference Pattern Report",
            "",
            f"**Holographic Coherence Status:** {icon} `{telemetry.status_level}`",
            "",
            "## Optical Field Superposition & Interference Telemetry",
            "",
            "| Holographic Dimension | Value | Theoretical Benchmark | Cognitive Significance |",
            "| :--- | :--- | :--- | :--- |",
            f"| **Total Wave Emitters** | `{telemetry.total_emitters}` | >= 3 modalities | Breadth of multimodal concept origins |",
            f"| **Peak Constructive Intensity** | `{telemetry.peak_constructive_intensity:.2f}` | > Incoherent Sum | Maximum cross-modal semantic resonance |",
            f"| **Mean Field Intensity** | `{telemetry.mean_field_intensity:.2f}` | Balanced | Global energetic density of the mental model |",
            f"| **Global Coherence Index** | `{telemetry.global_coherence_index * 100:.1f}%` | >= 60.0% | Degree of phase alignment across domains |",
            f"| **Constructive Resonance Peaks** | `{len(telemetry.interference_peaks)}` | >= 3 peaks | Discrete holographic synthesis nodes |",
            f"| **Fringe Density Score** | `{telemetry.fringe_density_score * 100:.1f}%` | >= 50.0% | Richness of diffractive concept lattice |",
            "",
            "## Multimodal Concept Wave Emitters",
            "",
        ]

        if not telemetry.emitters:
            lines.append("_No concept emitters present in the holographic field._")
        else:
            lines.append("| Emitter ID | Title | Modality | Origin (X, Y) | Wavelength | Amplitude | Phase |")
            lines.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
            for em in telemetry.emitters:
                lines.append(
                    f"| `{em.emitter_id}` | {em.title} | `{em.modality}` | ({em.x:.0f}, {em.y:.0f}) | `{em.wavelength_px:.0f} px` | `{em.amplitude:.1f}` | `{em.phase_rad:.2f} rad` |"
                )
            lines.append("")

        lines.extend([
            "## Constructive Interference Peaks & Synthetic Nodes",
            "",
        ])

        if not telemetry.interference_peaks:
            lines.append("_No constructive interference peaks detected; waves are mutually out of phase._")
        else:
            lines.append("| Peak ID | Location (X, Y) | Intensity | Resonance Type | Resonating Concepts |")
            lines.append("| :--- | :--- | :--- | :--- | :--- |")
            for pk in telemetry.interference_peaks:
                lines.append(
                    f"| `{pk.peak_id}` | ({pk.x:.0f}, {pk.y:.0f}) | `{pk.intensity:.2f}` | `{pk.resonance_type}` | {', '.join(pk.participating_emitters)} |"
                )
            lines.append("")

        lines.extend([
            "## Cognitive Holography & Dyslexic Synthesis Mechanics",
            "",
            "- **Karl Pribram Holonomic Brain Theory:** Memory and associative conceptualization operate as distributed wave interference fields rather than localized indexical bins.",
            "- **Constructive Interference:** When spatial, structural, and temporal perspectives overlap constructively, they forge durable eureka insights that resist forgetting.",
            "- **Diffractive Cognitive Webs:** High-density fringe patterns reveal emergent properties undetectable when viewing concepts in linear isolation.",
        ])

        return "\n".join(lines)

    def generate_svg(
        self,
        telemetry: HolographicTelemetry,
        width: int = 880,
        height: int = 580,
    ) -> str:
        """Renders an interactive dark titanium SVG visualization of the concept hologram."""
        parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
            f'width="{width}" height="{height}" style="background-color: #0d1117; font-family: -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif;">',
            '<defs>',
            '  <radialGradient id="peakGlow" cx="50%" cy="50%" r="50%">',
            '    <stop offset="0%" stop-color="#3fb950" stop-opacity="0.9" />',
            '    <stop offset="50%" stop-color="#2ea043" stop-opacity="0.4" />',
            '    <stop offset="100%" stop-color="#0d1117" stop-opacity="0" />',
            '  </radialGradient>',
            '  <filter id="holoFilter" x="-40%" y="-40%" width="180%" height="180%">',
            '    <feGaussianBlur stdDeviation="3.5" result="blur" />',
            '    <feComposite in="SourceGraphic" in2="blur" operator="over" />',
            '  </filter>',
            '</defs>',
            '<!-- Canvas Base -->',
            f'<rect width="{width}" height="{height}" fill="#0d1117" />',
        ]

        # Draw Concentric Wavefront Rings for each Emitter
        for em in telemetry.emitters:
            max_r = math.hypot(width, height) * 0.65
            num_rings = int(max_r // em.wavelength_px)
            for r_idx in range(1, num_rings + 1):
                r_val = r_idx * em.wavelength_px
                opacity = max(0.04, min(0.25, 0.35 - (r_idx * 0.03)))
                parts.append(
                    f'<circle cx="{em.x}" cy="{em.y}" r="{r_val}" fill="none" '
                    f'stroke="{em.color}" stroke-width="1.2" stroke-opacity="{opacity:.3f}" />'
                )

        # Draw Diffractive Interference Lines linking coherent emitter pairs
        for i in range(len(telemetry.emitters)):
            for j in range(i + 1, len(telemetry.emitters)):
                e1 = telemetry.emitters[i]
                e2 = telemetry.emitters[j]
                parts.append(
                    f'<line x1="{e1.x}" y1="{e1.y}" x2="{e2.x}" y2="{e2.y}" '
                    f'stroke="#8b949e" stroke-width="1" stroke-dasharray="3,3" stroke-opacity="0.35" />'
                )

        # Draw Constructive Interference Resonance Peak Nodes
        for pk in telemetry.interference_peaks:
            radius = min(24.0, max(10.0, math.sqrt(pk.intensity) * 3.2))
            # Glowing aura
            parts.append(
                f'<circle cx="{pk.x}" cy="{pk.y}" r="{radius * 1.8}" fill="url(#peakGlow)" />'
            )
            # Center constructive core
            parts.append(
                f'<circle cx="{pk.x}" cy="{pk.y}" r="{radius * 0.5}" fill="#3fb950" '
                f'stroke="#ffffff" stroke-width="1.5" filter="url(#holoFilter)" />'
            )
            parts.append(
                f'<text x="{pk.x}" y="{pk.y - radius - 4}" fill="#3fb950" font-size="9" font-weight="700" text-anchor="middle">PEAK {pk.intensity:.1f}</text>'
            )

        # Draw Concept Emitters
        for em in telemetry.emitters:
            # Outer ring
            parts.append(
                f'<circle cx="{em.x}" cy="{em.y}" r="22" fill="#161b22" stroke="{em.color}" stroke-width="2.5" />'
            )
            # Inner beacon
            parts.append(
                f'<circle cx="{em.x}" cy="{em.y}" r="8" fill="{em.color}" />'
            )
            # Modality badge
            parts.append(
                f'<text x="{em.x}" y="{em.y + 36}" fill="#f0f6fc" font-size="12" font-weight="700" text-anchor="middle">{html.escape(em.title)}</text>'
            )
            parts.append(
                f'<text x="{em.x}" y="{em.y + 50}" fill="{em.color}" font-size="10" font-weight="600" text-anchor="middle">[{em.modality}]</text>'
            )

        # Header Block
        parts.extend([
            '<!-- Header Block -->',
            '<text x="28" y="38" fill="#38bdf8" font-size="18" font-weight="700" letter-spacing="0.5">MULTIMODAL CONCEPT HOLOGRAM WEAVER</text>',
            '<text x="28" y="56" fill="#8b949e" font-size="11">Holonomic Brain Field Superposition & Diffractive Interference Lattice</text>',
        ])

        # Status badge
        badge_cols = {
            "HIGH_COHERENCE": ("#238636", "#3fb950"),
            "RESONANT": ("#9e6a03", "#d29922"),
            "DISPERSED": ("#30363d", "#8b949e"),
        }
        bg_col, fg_col = badge_cols.get(telemetry.status_level, ("#30363d", "#8b949e"))
        badge_x = width - 180
        parts.extend([
            f'<rect x="{badge_x}" y="22" width="152" height="34" rx="6" fill="{bg_col}" fill-opacity="0.3" stroke="{fg_col}" stroke-width="1.2" />',
            f'<circle cx="{badge_x + 18}" cy="39" r="5" fill="{fg_col}" />',
            f'<text x="{badge_x + 32}" y="43" fill="#f0f6fc" font-size="11" font-weight="700">{telemetry.status_level}</text>',
        ])

        # Telemetry HUD Card (Bottom Right)
        card_w = 320
        card_h = 138
        card_x = width - card_w - 24
        card_y = height - card_h - 24
        parts.extend([
            f'<g transform="translate({card_x}, {card_y})">',
            f'  <rect width="{card_w}" height="{card_h}" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1.5" />',
            '  <text x="16" y="24" fill="#f0f6fc" font-size="12" font-weight="700">Holographic Field Telemetry</text>',
            f'  <line x1="16" y1="32" x2="{card_w - 16}" y2="32" stroke="#30363d" stroke-width="1" />',
            f'  <text x="16" y="52" fill="#8b949e" font-size="11">Global Coherence Index:</text>',
            f'  <text x="{card_w - 16}" y="52" fill="#38bdf8" font-size="11" font-weight="600" text-anchor="end">{telemetry.global_coherence_index * 100:.1f}%</text>',
            f'  <text x="16" y="72" fill="#8b949e" font-size="11">Peak Constructive Intensity:</text>',
            f'  <text x="{card_w - 16}" y="72" fill="#3fb950" font-size="11" font-weight="600" text-anchor="end">{telemetry.peak_constructive_intensity:.2f}</text>',
            f'  <text x="16" y="92" fill="#8b949e" font-size="11">Constructive Resonance Peaks:</text>',
            f'  <text x="{card_w - 16}" y="92" fill="#d29922" font-size="11" font-weight="600" text-anchor="end">{len(telemetry.interference_peaks)} nodes</text>',
            f'  <text x="16" y="112" fill="#8b949e" font-size="11">Mean Field Intensity:</text>',
            f'  <text x="{card_w - 16}" y="112" fill="#c9d1d9" font-size="11" font-weight="600" text-anchor="end">{telemetry.mean_field_intensity:.2f}</text>',
            f'  <text x="16" y="128" fill="#8b949e" font-size="11">Fringe Density Score:</text>',
            f'  <text x="{card_w - 16}" y="128" fill="#bc8cff" font-size="11" font-weight="600" text-anchor="end">{telemetry.fringe_density_score * 100:.1f}%</text>',
            '</g>',
        ])

        # Legend (Bottom Left)
        leg_w = 340
        leg_h = 105
        leg_x = 24
        leg_y = height - leg_h - 24
        parts.extend([
            f'<g transform="translate({leg_x}, {leg_y})">',
            f'  <rect width="{leg_w}" height="{leg_h}" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1.2" opacity="0.9" />',
            '  <text x="16" y="20" fill="#f0f6fc" font-size="11" font-weight="700">Hologram Weaver Legend</text>',
            '  <circle cx="26" cy="36" r="6" fill="#161b22" stroke="#58a6ff" stroke-width="2" />',
            '  <text x="44" y="39" fill="#8b949e" font-size="10">Concept Wave Emitter (Multimodal Origin)</text>',
            '  <circle cx="26" cy="56" r="6" fill="#3fb950" />',
            '  <text x="44" y="59" fill="#8b949e" font-size="10">Constructive Interference Peak (Resonance Node)</text>',
            '  <circle cx="26" cy="76" r="6" fill="none" stroke="#38bdf8" stroke-width="1.5" />',
            '  <text x="44" y="79" fill="#8b949e" font-size="10">Concentric Wavefront Crest (Wavelength Ring)</text>',
            '  <line x1="16" y1="94" x2="36" y2="94" stroke="#8b949e" stroke-width="1" stroke-dasharray="3,3" />',
            '  <text x="44" y="97" fill="#8b949e" font-size="10">Diffractive Baseline Ray (Phase Coherence)</text>',
            '</g>',
        ])

        parts.append('</svg>')
        return "\n".join(parts)

    @classmethod
    def create_demo_telemetry(cls) -> HolographicTelemetry:
        """Constructs a realistic technical concept hologram: Spatial UI, Vector Physics, and Reactive Dataflow."""
        emitters = [
            WaveEmitter(
                emitter_id="em-spatial",
                title="Spatial Topography",
                x=220.0,
                y=320.0,
                amplitude=1.0,
                wavelength_px=65.0,
                phase_rad=0.0,
                modality="SPATIAL",
                color="#58a6ff",
            ),
            WaveEmitter(
                emitter_id="em-physics",
                title="Kinetic Vector Physics",
                x=640.0,
                y=300.0,
                amplitude=1.0,
                wavelength_px=70.0,
                phase_rad=0.35,
                modality="STRUCTURAL",
                color="#bc8cff",
            ),
            WaveEmitter(
                emitter_id="em-reactive",
                title="Reactive Event Mesh",
                x=430.0,
                y=160.0,
                amplitude=1.2,
                wavelength_px=60.0,
                phase_rad=-0.25,
                modality="TEMPORAL",
                color="#38bdf8",
            ),
        ]

        weaver = cls(sample_grid_step=30.0, coherence_threshold=0.55)
        return weaver.compute_wave_field(emitters)
