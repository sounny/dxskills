"""
Concept Constellation & Synesthetic Starburst Engine
Autonomous cognitive spatial module for multimodal concept clustering,
harmonic auditory resonance mapping, chromatic spectral classification,
and interconnected conceptual asterisms. Grounded in Paivio dual coding theory,
Eide & Eide M-I-N-D framework, and Cowan working memory capacity bounds.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
import math
import html


@dataclass
class CelestialConcept:
    """Represents an individual concept mapped to celestial coordinates."""
    concept_id: str
    title: str
    magnitude: float  # Visual magnitude (lower = brighter, e.g. 1.0 to 6.0)
    spectral_class: str  # O (deep blue), B (cyan), A (white), F (yellow-white), G (gold), K (orange), M (red)
    frequency_hz: float  # Synesthetic harmonic resonance frequency
    pos_x: float
    pos_y: float
    cluster_id: str


@dataclass
class ConstellationEdge:
    """Represents a resonant tether between two stars in an asterism."""
    source_id: str
    target_id: str
    resonance_weight: float  # 0.0 to 1.0
    is_primary_asterism: bool


@dataclass
class ConstellationAsterism:
    """Represents an interconnected conceptual constellation group."""
    cluster_id: str
    name: str
    luminary_count: int
    harmonic_base_hz: float
    chromatic_hex: str
    bounding_box: Tuple[float, float, float, float]  # min_x, min_y, max_x, max_y


@dataclass
class ConstellationTelemetry:
    """Comprehensive telemetry report for the concept constellation."""
    total_stars: int
    total_asterisms: int
    mean_resonance: float
    cowan_compliant: bool
    spectral_distribution: Dict[str, int]
    stars: List[CelestialConcept] = field(default_factory=list)
    edges: List[ConstellationEdge] = field(default_factory=list)
    asterisms: List[ConstellationAsterism] = field(default_factory=list)


# Spectral class chromatic mapping
SPECTRAL_PALETTE = {
    "O": "#38bdf8",  # Ionized blue
    "B": "#0284c7",  # Sky blue
    "A": "#f8fafc",  # Brilliant white
    "F": "#fef08a",  # Warm yellow-white
    "G": "#eab308",  # Solar gold
    "K": "#f97316",  # Deep amber
    "M": "#ef4444",  # Crimson giant
}

# Musical pitch mapping (Pentatonic base scale 220Hz - 880Hz)
HARMONIC_INTERVALS = [220.0, 247.5, 275.0, 330.0, 366.7, 440.0, 495.0, 550.0, 660.0, 880.0]


class ConceptConstellationStarburst:
    """
    Autonomous engine that synthesizes conceptual clusters into radiant
    multimodal constellations. Combines chromatic spectral categorization,
    harmonic audio-frequency assignment, and minimal spanning asterisms.
    """

    def __init__(
        self,
        max_asterism_tether_dist_px: float = 240.0,
        min_resonance_threshold: float = 0.35,
    ):
        self.max_tether_dist = float(max_asterism_tether_dist_px)
        self.min_resonance = float(min_resonance_threshold)

    def synthesize_constellation(
        self,
        raw_concepts: List[Dict],
        canvas_width: float = 920.0,
        canvas_height: float = 560.0,
    ) -> ConstellationTelemetry:
        """
        Processes raw conceptual data into celestial coordinates,
        spectral classes, harmonic tones, and connected asterisms.
        """
        stars: List[CelestialConcept] = []
        clusters: Dict[str, List[CelestialConcept]] = {}
        spectral_counts: Dict[str, int] = {k: 0 for k in SPECTRAL_PALETTE.keys()}

        for idx, item in enumerate(raw_concepts):
            c_id = str(item.get("id", f"star-{idx+1}"))
            title = str(item.get("title", f"Concept {idx+1}"))
            mag = float(item.get("magnitude", 2.5 + (idx % 4) * 0.8))
            spec = str(item.get("spectral_class", list(SPECTRAL_PALETTE.keys())[idx % len(SPECTRAL_PALETTE)]))
            if spec not in SPECTRAL_PALETTE:
                spec = "A"

            px = float(item.get("x", 120.0 + (idx * 160.0) % (canvas_width - 240.0)))
            py = float(item.get("y", 120.0 + (idx * 110.0) % (canvas_height - 200.0)))
            cluster_id = str(item.get("cluster", f"grp-{(idx // 4) + 1}"))

            freq = HARMONIC_INTERVALS[idx % len(HARMONIC_INTERVALS)]

            star = CelestialConcept(
                concept_id=c_id,
                title=title,
                magnitude=round(mag, 2),
                spectral_class=spec,
                frequency_hz=round(freq, 1),
                pos_x=round(px, 2),
                pos_y=round(py, 2),
                cluster_id=cluster_id,
            )
            stars.append(star)
            clusters.setdefault(cluster_id, []).append(star)
            spectral_counts[spec] = spectral_counts.get(spec, 0) + 1

        # Synthesize Asterism Hulls & Edges per cluster
        asterisms: List[ConstellationAsterism] = []
        edges: List[ConstellationEdge] = []
        total_resonance = 0.0

        for cluster_id, cluster_stars in clusters.items():
            min_x = min(s.pos_x for s in cluster_stars)
            min_y = min(s.pos_y for s in cluster_stars)
            max_x = max(s.pos_x for s in cluster_stars)
            max_y = max(s.pos_y for s in cluster_stars)

            # Dominant spectral class for cluster color
            dom_spec = max(
                set(s.spectral_class for s in cluster_stars),
                key=lambda sp: sum(1 for s in cluster_stars if s.spectral_class == sp),
            )
            chromatic_hex = SPECTRAL_PALETTE.get(dom_spec, "#38bdf8")
            base_hz = min(s.frequency_hz for s in cluster_stars)
            ast_name = f"Asterism {cluster_id.upper()}"

            asterisms.append(
                ConstellationAsterism(
                    cluster_id=cluster_id,
                    name=ast_name,
                    luminary_count=len(cluster_stars),
                    harmonic_base_hz=round(base_hz, 1),
                    chromatic_hex=chromatic_hex,
                    bounding_box=(round(min_x, 2), round(min_y, 2), round(max_x, 2), round(max_y, 2)),
                )
            )

            # Build minimal spanning chain / asterism tethers
            sorted_by_mag = sorted(cluster_stars, key=lambda s: s.magnitude)
            for i in range(len(sorted_by_mag) - 1):
                s1 = sorted_by_mag[i]
                s2 = sorted_by_mag[i + 1]
                dist = math.hypot(s1.pos_x - s2.pos_x, s1.pos_y - s2.pos_y)
                if dist <= self.max_tether_dist:
                    res = max(0.1, 1.0 - (dist / self.max_tether_dist))
                    edges.append(
                        ConstellationEdge(
                            source_id=s1.concept_id,
                            target_id=s2.concept_id,
                            resonance_weight=round(res, 3),
                            is_primary_asterism=True,
                        )
                    )
                    total_resonance += res

        # Cowan limit compliance (N <= 4 major asterisms or average <= 4 luminaries per cluster)
        cowan_compliant = len(asterisms) <= 4 or all(a.luminary_count <= 5 for a in asterisms)

        mean_res = round(total_resonance / max(1, len(edges)), 3) if edges else 1.0

        return ConstellationTelemetry(
            total_stars=len(stars),
            total_asterisms=len(asterisms),
            mean_resonance=mean_res,
            cowan_compliant=cowan_compliant,
            spectral_distribution=spectral_counts,
            stars=stars,
            edges=edges,
            asterisms=asterisms,
        )

    def generate_markdown_report(self, telemetry: ConstellationTelemetry) -> str:
        """Generates structured markdown audit report with zero em dashes."""
        lines = [
            "# Concept Constellation and Synesthetic Starburst Telemetry",
            "",
            "## 1. Celestial Synthesis Overview",
            f"- **Total Concept Stars:** {telemetry.total_stars}",
            f"- **Active Asterisms:** {telemetry.total_asterisms}",
            f"- **Mean Tether Resonance:** {round(telemetry.mean_resonance * 100.0, 1)}%",
            f"- **Cowan Bound Status:** {'COMPLIANT' if telemetry.cowan_compliant else 'EXPANDED CLUSTERS'}",
            "",
            "## 2. Spectral Chromatic Distribution",
            "| Spectral Class | Visual Hue | Star Count |",
            "| :--- | :--- | :--- |",
        ]

        for spec, count in telemetry.spectral_distribution.items():
            color_hex = SPECTRAL_PALETTE.get(spec, "#ffffff")
            lines.append(f"| `{spec}` | `{color_hex}` | {count} |")

        lines.extend([
            "",
            "## 3. Celestial Concept Catalog",
            "| ID | Title | Cluster | Mag | Spectral | Harmonic (Hz) | Position (x, y) |",
            "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |",
        ])

        for s in telemetry.stars:
            lines.append(
                f"| `{s.concept_id}` | {s.title} | `{s.cluster_id}` | {s.magnitude} | `{s.spectral_class}` | {s.frequency_hz} Hz | ({s.pos_x}, {s.pos_y}) |"
            )

        if telemetry.asterisms:
            lines.extend([
                "",
                "## 4. Constellation Asterism Profiles",
                "| Cluster | Asterism Name | Luminaries | Base Frequency | Chromatic Tint |",
                "| :--- | :--- | :--- | :--- | :--- |",
            ])
            for a in telemetry.asterisms:
                lines.append(
                    f"| `{a.cluster_id}` | {a.name} | {a.luminary_count} stars | {a.harmonic_base_hz} Hz | `{a.chromatic_hex}` |"
                )

        lines.extend([
            "",
            "## 5. Operational Ergonomics Guidance",
            "- Asterisms bind related domain ideas into spatial constellations that resist phonological fatigue.",
            "- Harmonic frequency tags provide dual-code auditory anchor points for multimodal memory recall.",
            "- Spectral color tethers illuminate dialectical relationships across disparate technical domains.",
        ])

        return "\n".join(lines)

    def generate_svg(
        self,
        telemetry: ConstellationTelemetry,
        width: int = 920,
        height: int = 560,
    ) -> str:
        """Generates publication-grade dark titanium deep space SVG with starburst diffraction spikes."""
        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" style="background:#070a12; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">',
            '<defs>',
            '  <radialGradient id="nebulaGlow" cx="50%" cy="50%" r="50%">',
            '    <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.12"/>',
            '    <stop offset="60%" stop-color="#0284c7" stop-opacity="0.04"/>',
            '    <stop offset="100%" stop-color="#070a12" stop-opacity="0"/>',
            '  </radialGradient>',
            '  <filter id="starGlow" x="-50%" y="-50%" width="200%" height="200%">',
            '    <feGaussianBlur stdDeviation="3" result="coloredBlur"/>',
            '    <feMerge>',
            '      <feMergeNode in="coloredBlur"/>',
            '      <feMergeNode in="SourceGraphic"/>',
            '    </feMerge>',
            '  </filter>',
            '</defs>',
            '<!-- Deep Space Nebular Background -->',
        ]

        # Draw nebular clouds for each asterism
        for ast in telemetry.asterisms:
            min_x, min_y, max_x, max_y = ast.bounding_box
            cx = (min_x + max_x) / 2.0
            cy = (min_y + max_y) / 2.0
            rx = max(60.0, (max_x - min_x) * 0.85)
            ry = max(50.0, (max_y - min_y) * 0.85)
            svg_parts.append(
                f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="url(#nebulaGlow)" opacity="0.85"/>'
            )

        # Draw Constellation Asterism Tethers
        star_dict = {s.concept_id: s for s in telemetry.stars}
        for edge in telemetry.edges:
            s1 = star_dict.get(edge.source_id)
            s2 = star_dict.get(edge.target_id)
            if s1 and s2:
                svg_parts.append(
                    f'<line x1="{s1.pos_x}" y1="{s1.pos_y}" x2="{s2.pos_x}" y2="{s2.pos_y}" stroke="#38bdf8" stroke-width="1.2" stroke-dasharray="2,3" opacity="0.5"/>'
                )

        # Draw Stars and Starburst Diffraction Spikes
        for star in telemetry.stars:
            color = SPECTRAL_PALETTE.get(star.spectral_class, "#ffffff")
            # Star radius inversely proportional to magnitude (brighter = larger)
            r = max(4.0, min(14.0, 16.0 - star.magnitude * 2.2))

            # Starburst diffraction spikes for brighter stars (mag < 3.5)
            if star.magnitude < 3.5:
                spike_len = r * 2.4
                svg_parts.append(
                    f'<line x1="{star.pos_x - spike_len}" y1="{star.pos_y}" x2="{star.pos_x + spike_len}" y2="{star.pos_y}" stroke="{color}" stroke-width="0.8" opacity="0.6"/>'
                )
                svg_parts.append(
                    f'<line x1="{star.pos_x}" y1="{star.pos_y - spike_len}" x2="{star.pos_x}" y2="{star.pos_y + spike_len}" stroke="{color}" stroke-width="0.8" opacity="0.6"/>'
                )

            # Central luminary
            svg_parts.append(
                f'<circle cx="{star.pos_x}" cy="{star.pos_y}" r="{r}" fill="{color}" filter="url(#starGlow)"/>'
            )
            # Label
            svg_parts.append(
                f'<text x="{star.pos_x}" y="{star.pos_y + r + 13}" font-size="10" font-weight="600" fill="#ffffff" text-anchor="middle">{html.escape(star.title)}</text>'
            )
            # Frequency & Magnitude Sub-label
            sub_text = f"{star.frequency_hz}Hz | m={star.magnitude}"
            svg_parts.append(
                f'<text x="{star.pos_x}" y="{star.pos_y + r + 24}" font-size="8" fill="#94a3b8" text-anchor="middle">{sub_text}</text>'
            )

        # HUD Overlay Box
        svg_parts.append(
            f'<rect x="20" y="16" width="340" height="74" rx="8" fill="#0f172a" fill-opacity="0.88" stroke="#1e293b" stroke-width="1"/>'
        )
        svg_parts.append(
            f'<text x="32" y="36" font-size="11" font-weight="700" fill="#38bdf8">CONCEPT CONSTELLATION ENGINE</text>'
        )
        svg_parts.append(
            f'<text x="32" y="52" font-size="9" fill="#94a3b8">Stars: {telemetry.total_stars} | Asterisms: {telemetry.total_asterisms} | Resonance: {round(telemetry.mean_resonance * 100.0, 1)}%</text>'
        )
        svg_parts.append(
            f'<text x="32" y="68" font-size="9" fill="#94a3b8">Cowan Bound: {"Optimal" if telemetry.cowan_compliant else "Expanded"} | Synesthetic Pentatonic Scale</text>'
        )

        svg_parts.append('</svg>')
        return "\n".join(svg_parts)


def sample_concept_stars() -> List[Dict]:
    """Demonstration concept star cluster definitions."""
    return [
        {"id": "star-1", "title": "Allocentric Mapping", "magnitude": 1.2, "spectral_class": "O", "x": 220.0, "y": 180.0, "cluster": "spatial"},
        {"id": "star-2", "title": "Saccadic Rhythm", "magnitude": 2.1, "spectral_class": "B", "x": 340.0, "y": 160.0, "cluster": "spatial"},
        {"id": "star-3", "title": "Foveal Anchor", "magnitude": 2.8, "spectral_class": "A", "x": 280.0, "y": 280.0, "cluster": "spatial"},
        {"id": "star-4", "title": "Dialectic Thesis", "magnitude": 1.5, "spectral_class": "G", "x": 600.0, "y": 200.0, "cluster": "reasoning"},
        {"id": "star-5", "title": "Antithesis Tension", "magnitude": 2.4, "spectral_class": "K", "x": 720.0, "y": 190.0, "cluster": "reasoning"},
        {"id": "star-6", "title": "Synthesis Horizon", "magnitude": 1.8, "spectral_class": "F", "x": 660.0, "y": 310.0, "cluster": "reasoning"},
        {"id": "star-7", "title": "Working Memory Shield", "magnitude": 2.0, "spectral_class": "M", "x": 460.0, "y": 420.0, "cluster": "executive"},
        {"id": "star-8", "title": "Density Equalizer", "magnitude": 3.0, "spectral_class": "B", "x": 360.0, "y": 460.0, "cluster": "executive"},
    ]
