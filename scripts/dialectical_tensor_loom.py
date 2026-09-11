"""
Dialectical Tensor Lattice and Hegelian Synthesis Loom Engine
Autonomous cognitive spatial module tracking multi-pole conceptual antithesis friction
across argument graphs and weaving constructive Aufhebung resolution structures.
Grounded in Hegelian dialectics (Thesis - Antithesis - Aufhebung Synthesis)
and Eide Interconnected Reasoning to resolve high-dimensional cognitive paradoxes.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Any
import math
import html


@dataclass
class DialecticalPole:
    """Represents a conceptual pole within a dialectical argument graph."""
    pole_id: str
    title: str
    dimension_vector: List[float]
    core_axiom: str
    pole_type: str = "THESIS"  # THESIS, ANTITHESIS, or SYNTHESIS
    pos_x: float = 0.0
    pos_y: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "pole_id": self.pole_id,
            "title": self.title,
            "dimension_vector": [round(v, 3) for v in self.dimension_vector],
            "core_axiom": self.core_axiom,
            "pole_type": self.pole_type,
            "pos_x": round(self.pos_x, 1),
            "pos_y": round(self.pos_y, 1),
        }


@dataclass
class DialecticalTensionEdge:
    """Represents semantic opposition and friction between two poles."""
    source_id: str
    target_id: str
    cosine_similarity: float
    antithesis_friction: float
    tension_level: str  # LOW, MODERATE, ACUTE, PARADOX
    friction_weight: float = 1.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_id": self.source_id,
            "target_id": self.target_id,
            "cosine_similarity": round(self.cosine_similarity, 3),
            "antithesis_friction": round(self.antithesis_friction, 3),
            "tension_level": self.tension_level,
            "friction_weight": round(self.friction_weight, 3),
        }


@dataclass
class AufhebungResolution:
    """Triadic higher-order synthesis resolving thesis and antithesis opposition."""
    resolution_id: str
    thesis_id: str
    antithesis_id: str
    synthesis_title: str
    preserved_tenets: List[str]
    negated_biases: List[str]
    emergent_axiom: str
    resolution_ratio: float  # Friction dissipated vs value preserved (0.0 - 1.0)
    cognitive_harmony_index: float  # 0.0 to 100.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "resolution_id": self.resolution_id,
            "thesis_id": self.thesis_id,
            "antithesis_id": self.antithesis_id,
            "synthesis_title": self.synthesis_title,
            "preserved_tenets": self.preserved_tenets,
            "negated_biases": self.negated_biases,
            "emergent_axiom": self.emergent_axiom,
            "resolution_ratio": round(self.resolution_ratio, 3),
            "cognitive_harmony_index": round(self.cognitive_harmony_index, 1),
        }


@dataclass
class DialecticalLatticeTelemetry:
    """Telemetry report capturing dialectical tensions and synthesis integration."""
    poles: List[DialecticalPole]
    tension_edges: List[DialecticalTensionEdge]
    resolutions: List[AufhebungResolution]
    mean_lattice_friction: float
    acute_tension_count: int
    resolution_coverage: float
    overall_harmony_score: float
    status_level: str = "SYNTHESIZED"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "poles": [p.to_dict() for p in self.poles],
            "tension_edges": [e.to_dict() for e in self.tension_edges],
            "resolutions": [r.to_dict() for r in self.resolutions],
            "mean_lattice_friction": round(self.mean_lattice_friction, 3),
            "acute_tension_count": self.acute_tension_count,
            "resolution_coverage": round(self.resolution_coverage, 3),
            "overall_harmony_score": round(self.overall_harmony_score, 1),
            "status_level": self.status_level,
        }


class DialecticalTensorLoom:
    """
    Evaluates multi-pole opposition vectors using semantic tensors
    and constructs Aufhebung triadic synthesis bridges.
    """

    def __init__(self, acute_friction_threshold: float = 0.65):
        self.acute_friction_threshold = max(0.1, min(0.95, acute_friction_threshold))

    @staticmethod
    def vector_norm(v: List[float]) -> float:
        """Euclidean norm of vector."""
        return math.sqrt(sum(x * x for x in v))

    @staticmethod
    def cosine_sim(v1: List[float], v2: List[float]) -> float:
        """Calculates normalized cosine similarity between two dimensional vectors."""
        if len(v1) != len(v2) or not v1:
            return 0.0
        n1 = math.sqrt(sum(x * x for x in v1))
        n2 = math.sqrt(sum(x * x for x in v2))
        if n1 < 1e-9 or n2 < 1e-9:
            return 0.0
        dot = sum(a * b for a, b in zip(v1, v2))
        return max(-1.0, min(1.0, dot / (n1 * n2)))

    def calculate_tension_edge(self, p1: DialecticalPole, p2: DialecticalPole) -> DialecticalTensionEdge:
        """Quantifies dialectical opposition friction between two poles."""
        sim = self.cosine_sim(p1.dimension_vector, p2.dimension_vector)
        # Friction is highest when vectors are diametrically opposed (sim -> -1.0)
        # Friction = (1.0 - sim) / 2.0 (normalized 0.0 to 1.0)
        friction = (1.0 - sim) / 2.0

        if friction >= 0.80:
            level = "PARADOX"
        elif friction >= self.acute_friction_threshold:
            level = "ACUTE"
        elif friction >= 0.35:
            level = "MODERATE"
        else:
            level = "LOW"

        return DialecticalTensionEdge(
            source_id=p1.pole_id,
            target_id=p2.pole_id,
            cosine_similarity=sim,
            antithesis_friction=friction,
            tension_level=level,
            friction_weight=1.0 + friction,
        )

    def evaluate_lattice(
        self,
        poles: List[DialecticalPole],
        custom_resolutions: Optional[List[AufhebungResolution]] = None,
    ) -> DialecticalLatticeTelemetry:
        """
        Evaluates all pair-wise conceptual tensions in the argument lattice
        and derives synthesis resolution telemetry.
        """
        if not poles:
            return DialecticalLatticeTelemetry(
                poles=[],
                tension_edges=[],
                resolutions=[],
                mean_lattice_friction=0.0,
                acute_tension_count=0,
                resolution_coverage=1.0,
                overall_harmony_score=100.0,
                status_level="SYNTHESIZED",
            )

        edges: List[DialecticalTensionEdge] = []
        acute_count = 0
        total_friction = 0.0

        for i in range(len(poles)):
            for j in range(i + 1, len(poles)):
                edge = self.calculate_tension_edge(poles[i], poles[j])
                edges.append(edge)
                total_friction += edge.antithesis_friction
                if edge.tension_level in ["ACUTE", "PARADOX"]:
                    acute_count += 1

        mean_friction = total_friction / len(edges) if edges else 0.0

        # Match resolutions or generate heuristic Aufhebung structures for acute pairs
        resolutions: List[AufhebungResolution] = custom_resolutions or []
        if not custom_resolutions:
            # Auto-weave synthesis for top acute oppositions
            acute_edges = [e for e in edges if e.tension_level in ["ACUTE", "PARADOX"]]
            pole_map = {p.pole_id: p for p in poles}
            for idx, ae in enumerate(acute_edges):
                tp = pole_map.get(ae.source_id)
                ap = pole_map.get(ae.target_id)
                if tp and ap:
                    res_ratio = max(0.4, 1.0 - ae.antithesis_friction * 0.5)
                    harmony = res_ratio * 92.0
                    res = AufhebungResolution(
                        resolution_id=f"res-{idx+1}",
                        thesis_id=tp.pole_id,
                        antithesis_id=ap.pole_id,
                        synthesis_title=f"Harmonic Integration: {tp.title} & {ap.title}",
                        preserved_tenets=[
                            f"Core operational validity of {tp.title}",
                            f"Adaptive resilience of {ap.title}",
                        ],
                        negated_biases=[
                            f"Dogmatic isolation of {tp.title}",
                            f"Unchecked overshoot of {ap.title}",
                        ],
                        emergent_axiom=f"Dynamic dialectical balance transcending rigid dichotomies",
                        resolution_ratio=res_ratio,
                        cognitive_harmony_index=harmony,
                    )
                    resolutions.append(res)

        resolved_pairs = set()
        for r in resolutions:
            resolved_pairs.add((r.thesis_id, r.antithesis_id))
            resolved_pairs.add((r.antithesis_id, r.thesis_id))

        pole_map = {p.pole_id: p for p in poles}
        acute_opposites = [
            e for e in edges
            if e.tension_level in ["ACUTE", "PARADOX"]
            and pole_map.get(e.source_id) is not None and pole_map[e.source_id].pole_type != "SYNTHESIS"
            and pole_map.get(e.target_id) is not None and pole_map[e.target_id].pole_type != "SYNTHESIS"
        ]
        if acute_opposites:
            resolved_acute = sum(
                1 for e in acute_opposites if (e.source_id, e.target_id) in resolved_pairs
            )
            coverage = resolved_acute / len(acute_opposites)
        else:
            coverage = 1.0

        mean_harmony = (
            sum(r.cognitive_harmony_index for r in resolutions) / len(resolutions)
            if resolutions
            else (100.0 - mean_friction * 60.0)
        )

        if coverage >= 0.85 and acute_count <= 1:
            status = "HARMONIZED"
        elif coverage >= 0.50:
            status = "SYNTHESIZED"
        else:
            status = "UNRESOLVED_TENSION"

        return DialecticalLatticeTelemetry(
            poles=poles,
            tension_edges=edges,
            resolutions=resolutions,
            mean_lattice_friction=mean_friction,
            acute_tension_count=acute_count,
            resolution_coverage=coverage,
            overall_harmony_score=mean_harmony,
            status_level=status,
        )

    def generate_markdown_report(self, telemetry: DialecticalLatticeTelemetry) -> str:
        """Builds a structured diagnostic Markdown report analyzing dialectical tensions and synthesis."""
        status_icons = {
            "HARMONIZED": "🟢",
            "SYNTHESIZED": "🟡",
            "UNRESOLVED_TENSION": "🔴",
        }
        icon = status_icons.get(telemetry.status_level, "⚪")

        lines = [
            "# Dialectical Tensor Lattice & Hegelian Synthesis Report",
            "",
            f"**Synthesis Status:** {icon} `{telemetry.status_level}`",
            "",
            "## Dialectical Tension & Harmony Telemetry",
            "",
            "| Telemetry Dimension | Metric | Benchmark Threshold | Epistemic Significance |",
            "| :--- | :--- | :--- | :--- |",
            f"| **Active Conceptual Poles** | `{len(telemetry.poles)}` | >= 2 poles | Breadth of multi-pole conceptual space |",
            f"| **Evaluated Tension Edges** | `{len(telemetry.tension_edges)}` | N/A | Total pairwise dialectical vectors |",
            f"| **Mean Lattice Friction** | `{telemetry.mean_lattice_friction:.3f}` | < 0.500 | Normalized semantic opposition load |",
            f"| **Acute Tension Count** | `{telemetry.acute_tension_count}` | <= 2 acute edges | Points of potential cognitive paradox |",
            f"| **Aufhebung Coverage** | `{telemetry.resolution_coverage * 100:.1f}%` | >= 80.0% | Ratio of acute tensions with synthesis |",
            f"| **Overall Cognitive Harmony** | `{telemetry.overall_harmony_score:.1f} / 100` | >= 75.0 | Integrated gestalt coherence |",
            "",
            "## Conceptual Poles & Axiomatic Anchors",
            "",
        ]

        if not telemetry.poles:
            lines.append("_No conceptual poles registered in the current lattice._")
        else:
            lines.append("| Pole ID | Title | Paradigm Type | Core Axiom | Position (X, Y) |")
            lines.append("| :--- | :--- | :--- | :--- | :--- |")
            for p in telemetry.poles:
                lines.append(
                    f"| `{p.pole_id}` | {p.title} | `{p.pole_type}` | {p.core_axiom} | ({p.pos_x:.0f}, {p.pos_y:.0f}) |"
                )
            lines.append("")

        lines.extend([
            "## Dialectical Tension Edges",
            "",
            "| Source Pole | Target Pole | Cosine Sim | Antithesis Friction | Tension Level |",
            "| :--- | :--- | :--- | :--- | :--- |",
        ])
        for e in telemetry.tension_edges:
            lines.append(
                f"| `{e.source_id}` | `{e.target_id}` | `{e.cosine_similarity:+.3f}` | `{e.antithesis_friction:.3f}` | `{e.tension_level}` |"
            )
        lines.append("")

        lines.extend([
            "## Aufhebung Triadic Resolutions",
            "",
        ])
        if not telemetry.resolutions:
            lines.append("_No higher-order synthesis structures currently woven._")
        else:
            for r in telemetry.resolutions:
                lines.extend([
                    f"### {r.synthesis_title}",
                    f"- **Thesis / Antithesis:** `{r.thesis_id}` vs `{r.antithesis_id}`",
                    f"- **Preserved Tenets:** {', '.join(r.preserved_tenets)}",
                    f"- **Negated Biases:** {', '.join(r.negated_biases)}",
                    f"- **Emergent Axiom:** *{r.emergent_axiom}*",
                    f"- **Resolution Efficiency:** `{r.resolution_ratio * 100:.1f}%` (Harmony Index: `{r.cognitive_harmony_index:.1f}`)",
                    "",
                ])

        lines.extend([
            "## Cognitive Architecture & Dyslexic Synthesis Mechanics",
            "",
            "- **Non-Linear Paradox Holding:** Dyslexic thinkers naturally sustain opposing hypotheses without forced premature collapse. Tensor lattices map this multi-variable equilibrium.",
            "- **Aufhebung Transcendence:** Rather than compromising into an anemic middle ground, Hegelian synthesis preserves functional truths while discarding peripheral orthodoxies.",
            "- **Cognitive Load Shielding:** Isolating acute tensions converts paralyzing cognitive friction into actionable generative synthesis vectors.",
        ])

        return "\n".join(lines)

    def generate_svg(
        self,
        telemetry: DialecticalLatticeTelemetry,
        width: int = 880,
        height: int = 580,
    ) -> str:
        """Renders an interactive dark titanium SVG visualization of the dialectical tensor loom."""
        parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
            f'width="{width}" height="{height}" style="background-color: #0d1117; font-family: -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif;">',
            '<defs>',
            '  <pattern id="diagGrid" width="30" height="30" patternUnits="userSpaceOnUse">',
            '    <path d="M 30 0 L 0 30 M 0 0 L 30 30" fill="none" stroke="#21262d" stroke-width="0.5" />',
            '  </pattern>',
            '  <linearGradient id="thesisGrad" x1="0%" y1="0%" x2="100%" y2="100%">',
            '    <stop offset="0%" stop-color="#58a6ff" />',
            '    <stop offset="100%" stop-color="#1f6feb" />',
            '  </linearGradient>',
            '  <linearGradient id="antiGrad" x1="0%" y1="0%" x2="100%" y2="100%">',
            '    <stop offset="0%" stop-color="#f85149" />',
            '    <stop offset="100%" stop-color="#da3633" />',
            '  </linearGradient>',
            '  <linearGradient id="synthGrad" x1="0%" y1="0%" x2="100%" y2="100%">',
            '    <stop offset="0%" stop-color="#3fb950" />',
            '    <stop offset="100%" stop-color="#2ea043" />',
            '  </linearGradient>',
            '  <filter id="tensorGlow" x="-30%" y="-30%" width="160%" height="160%">',
            '    <feGaussianBlur stdDeviation="4" result="blur" />',
            '    <feComposite in="SourceGraphic" in2="blur" operator="over" />',
            '  </filter>',
            '</defs>',
            '<!-- Canvas Base & Grid -->',
            f'<rect width="{width}" height="{height}" fill="#0d1117" />',
            f'<rect width="{width}" height="{height}" fill="url(#diagGrid)" opacity="0.45" />',
        ]

        pole_map = {p.pole_id: p for p in telemetry.poles}

        # Draw Tension Edges (Friction lines between opposing poles)
        for e in telemetry.tension_edges:
            p1 = pole_map.get(e.source_id)
            p2 = pole_map.get(e.target_id)
            if p1 and p2:
                # Color code tension level
                if e.tension_level == "PARADOX":
                    stroke_col = "#f85149"
                    dash = "3,3"
                    width_val = 3.0
                elif e.tension_level == "ACUTE":
                    stroke_col = "#d29922"
                    dash = "5,4"
                    width_val = 2.2
                elif e.tension_level == "MODERATE":
                    stroke_col = "#8b949e"
                    dash = "6,4"
                    width_val = 1.5
                else:
                    stroke_col = "#30363d"
                    dash = "none"
                    width_val = 1.0

                parts.append(
                    f'<line x1="{p1.pos_x}" y1="{p1.pos_y}" x2="{p2.pos_x}" y2="{p2.pos_y}" '
                    f'stroke="{stroke_col}" stroke-width="{width_val}" stroke-dasharray="{dash}" stroke-opacity="0.75" />'
                )

                # Midpoint tension label
                mid_x = (p1.pos_x + p2.pos_x) / 2.0
                mid_y = (p1.pos_y + p2.pos_y) / 2.0
                parts.append(
                    f'<rect x="{mid_x - 30}" y="{mid_y - 10}" width="60" height="20" rx="4" fill="#161b22" stroke="{stroke_col}" stroke-width="1" />'
                )
                parts.append(
                    f'<text x="{mid_x}" y="{mid_y + 4}" fill="{stroke_col}" font-size="9" font-weight="700" text-anchor="middle">F: {e.antithesis_friction:.2f}</text>'
                )

        # Draw Synthesis Aufhebung Convergence Arcs
        for r in telemetry.resolutions:
            tp = pole_map.get(r.thesis_id)
            ap = pole_map.get(r.antithesis_id)
            # Find or construct synthesis apex point
            synth_pole = next((p for p in telemetry.poles if p.pole_type == "SYNTHESIS"), None)
            if tp and ap and synth_pole:
                # Quadratic bezier curve from Thesis to Synthesis
                parts.append(
                    f'<path d="M {tp.pos_x} {tp.pos_y} Q {(tp.pos_x + synth_pole.pos_x)/2.0} {synth_pole.pos_y + 40} {synth_pole.pos_x} {synth_pole.pos_y}" '
                    f'fill="none" stroke="#58a6ff" stroke-width="2" stroke-opacity="0.65" stroke-dasharray="4,3" />'
                )
                # Quadratic bezier curve from Antithesis to Synthesis
                parts.append(
                    f'<path d="M {ap.pos_x} {ap.pos_y} Q {(ap.pos_x + synth_pole.pos_x)/2.0} {synth_pole.pos_y + 40} {synth_pole.pos_x} {synth_pole.pos_y}" '
                    f'fill="none" stroke="#f85149" stroke-width="2" stroke-opacity="0.65" stroke-dasharray="4,3" />'
                )

        # Draw Poles
        for p in telemetry.poles:
            if p.pole_type == "THESIS":
                grad = "url(#thesisGrad)"
                stroke = "#58a6ff"
                r = 28.0
            elif p.pole_type == "ANTITHESIS":
                grad = "url(#antiGrad)"
                stroke = "#f85149"
                r = 28.0
            else:  # SYNTHESIS
                grad = "url(#synthGrad)"
                stroke = "#3fb950"
                r = 34.0

            # Outer aura
            parts.append(
                f'<circle cx="{p.pos_x}" cy="{p.pos_y}" r="{r + 6}" fill="{stroke}" fill-opacity="0.18" filter="url(#tensorGlow)" />'
            )
            # Core circle
            parts.append(
                f'<circle cx="{p.pos_x}" cy="{p.pos_y}" r="{r}" fill="{grad}" stroke="{stroke}" stroke-width="2.5" />'
            )
            # Title inside/below
            parts.append(
                f'<text x="{p.pos_x}" y="{p.pos_y + 4}" fill="#ffffff" font-size="11" font-weight="700" text-anchor="middle">{p.pole_type[0]}</text>'
            )
            parts.append(
                f'<text x="{p.pos_x}" y="{p.pos_y + r + 16}" fill="#f0f6fc" font-size="12" font-weight="700" text-anchor="middle">{html.escape(p.title)}</text>'
            )
            parts.append(
                f'<text x="{p.pos_x}" y="{p.pos_y + r + 30}" fill="#8b949e" font-size="9" text-anchor="middle">{html.escape(p.core_axiom[:28])}...</text>'
            )

        # Header Titles
        parts.extend([
            '<!-- Header Block -->',
            '<text x="28" y="38" fill="#bc8cff" font-size="18" font-weight="700" letter-spacing="0.5">HEGELIAN DIALECTICAL TENSOR LOOM</text>',
            '<text x="28" y="56" fill="#8b949e" font-size="11">Multi-Pole Antithesis Friction Evaluator & Constructive Aufhebung Synthesizer</text>',
        ])

        # Status badge
        badge_cols = {
            "HARMONIZED": ("#238636", "#3fb950"),
            "SYNTHESIZED": ("#9e6a03", "#d29922"),
            "UNRESOLVED_TENSION": ("#da3633", "#f85149"),
        }
        bg_col, fg_col = badge_cols.get(telemetry.status_level, ("#30363d", "#8b949e"))
        badge_x = width - 190
        parts.extend([
            f'<rect x="{badge_x}" y="22" width="162" height="34" rx="6" fill="{bg_col}" fill-opacity="0.3" stroke="{fg_col}" stroke-width="1.2" />',
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
            '  <text x="16" y="24" fill="#f0f6fc" font-size="12" font-weight="700">Dialectical Tensor Telemetry</text>',
            f'  <line x1="16" y1="32" x2="{card_w - 16}" y2="32" stroke="#30363d" stroke-width="1" />',
            f'  <text x="16" y="52" fill="#8b949e" font-size="11">Mean Lattice Friction:</text>',
            f'  <text x="{card_w - 16}" y="52" fill="#d29922" font-size="11" font-weight="600" text-anchor="end">{telemetry.mean_lattice_friction:.3f}</text>',
            f'  <text x="16" y="72" fill="#8b949e" font-size="11">Acute Tensions / Paradoxes:</text>',
            f'  <text x="{card_w - 16}" y="72" fill="{"#f85149" if telemetry.acute_tension_count > 0 else "#3fb950"}" font-size="11" font-weight="600" text-anchor="end">{telemetry.acute_tension_count} edges</text>',
            f'  <text x="16" y="92" fill="#8b949e" font-size="11">Aufhebung Coverage:</text>',
            f'  <text x="{card_w - 16}" y="92" fill="#58a6ff" font-size="11" font-weight="600" text-anchor="end">{telemetry.resolution_coverage * 100:.1f}%</text>',
            f'  <text x="16" y="112" fill="#8b949e" font-size="11">Cognitive Harmony Score:</text>',
            f'  <text x="{card_w - 16}" y="112" fill="#3fb950" font-size="11" font-weight="600" text-anchor="end">{telemetry.overall_harmony_score:.1f} / 100</text>',
            f'  <text x="16" y="128" fill="#8b949e" font-size="11">Active Pole Triad:</text>',
            f'  <text x="{card_w - 16}" y="128" fill="#c9d1d9" font-size="11" font-weight="600" text-anchor="end">{len(telemetry.poles)} poles ({len(telemetry.resolutions)} synthesized)</text>',
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
            '  <text x="16" y="20" fill="#f0f6fc" font-size="11" font-weight="700">Dialectical Loom Legend</text>',
            '  <circle cx="26" cy="36" r="6" fill="#58a6ff" />',
            '  <text x="44" y="39" fill="#8b949e" font-size="10">Thesis Node (Affirmative Foundation)</text>',
            '  <circle cx="26" cy="56" r="6" fill="#f85149" />',
            '  <text x="44" y="59" fill="#8b949e" font-size="10">Antithesis Node (Negation & Critique)</text>',
            '  <circle cx="26" cy="76" r="7" fill="#3fb950" />',
            '  <text x="44" y="79" fill="#8b949e" font-size="10">Aufhebung Synthesis (Preserve + Elevate)</text>',
            '  <line x1="16" y1="94" x2="36" y2="94" stroke="#d29922" stroke-width="2" stroke-dasharray="4,3" />',
            '  <text x="44" y="97" fill="#8b949e" font-size="10">Tensor Opposition Vector (Friction Index)</text>',
            '</g>',
        ])

        parts.append('</svg>')
        return "\n".join(parts)

    @classmethod
    def create_demo_telemetry(cls) -> DialecticalLatticeTelemetry:
        """Constructs a realistic technical dialectic: Monolith vs Microservices vs Modular Microkernel."""
        poles = [
            DialecticalPole(
                pole_id="pole-thesis",
                title="Monolithic Cohesion",
                dimension_vector=[0.90, -0.20, 0.85, -0.15],
                core_axiom="Single deployment atomicity maximizes operational simplicity and transactional consistency",
                pole_type="THESIS",
                pos_x=190.0,
                pos_y=320.0,
            ),
            DialecticalPole(
                pole_id="pole-antithesis",
                title="Microservice Isolation",
                dimension_vector=[-0.85, 0.92, -0.75, 0.80],
                core_axiom="Decoupled bounded contexts maximize autonomous team velocity and domain scalability",
                pole_type="ANTITHESIS",
                pos_x=690.0,
                pos_y=320.0,
            ),
            DialecticalPole(
                pole_id="pole-synthesis",
                title="Modular Microkernel Engine",
                dimension_vector=[0.60, 0.65, 0.70, 0.60],
                core_axiom="Strict in-process boundary contracts with dynamic plugin isolation unify safety and agility",
                pole_type="SYNTHESIS",
                pos_x=440.0,
                pos_y=140.0,
            ),
        ]

        resolutions = [
            AufhebungResolution(
                resolution_id="res-arch-1",
                thesis_id="pole-thesis",
                antithesis_id="pole-antithesis",
                synthesis_title="Modular Microkernel Architecture",
                preserved_tenets=[
                    "Transactional ACID simplicity of Monolithic execution",
                    "Bounded context domain isolation of Microservices",
                ],
                negated_biases=[
                    "Spaghetti code coupled entanglement of monolithic codebases",
                    "Network latency and distributed consensus tax of microservices",
                ],
                emergent_axiom="Polymorphic module sandboxing running within a unified high-performance binary runtime",
                resolution_ratio=0.88,
                cognitive_harmony_index=91.5,
            )
        ]

        loom = cls(acute_friction_threshold=0.65)
        return loom.evaluate_lattice(poles, resolutions)
