"""
Dialectic Tensor & Semantic Orthogonality Gate
Autonomous cognitive spatial module for semantic vector orthogonality calculation,
thesis-antithesis tension resolution, and synthesis vector generation across
multi-dimensional conceptual manifolds. Grounded in Eide & Eide M-I-N-D framework,
dialectic reasoning, and orthogonal cognitive decoupling.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
import math
import html


@dataclass
class DialecticVector:
    """Represents a conceptual vector in high-dimensional embedding space."""
    vector_id: str
    title: str
    components: List[float]
    domain: str
    magnitude: float = 1.0


@dataclass
class TensorPairTension:
    """Tension measurement between thesis and antithesis concept vectors."""
    thesis_id: str
    antithesis_id: str
    cosine_similarity: float
    orthogonality_score: float  # 1.0 - |cos_sim| (1.0 = completely orthogonal)
    tension_energy: float  # High when cos_sim is strongly negative
    synthesis_opportunity: str  # polarized, orthogonal, reconciled, redundant


@dataclass
class SynthesisResultant:
    """Calculated resultant synthesis vector resolving dialectical opposition."""
    thesis_id: str
    antithesis_id: str
    title: str
    components: List[float]
    synthesis_power: float
    resolution_angle_deg: float


@dataclass
class DialecticTensorTelemetry:
    """Comprehensive telemetry report for dialectical tensor manifold."""
    total_vectors: int
    evaluated_pairs_count: int
    mean_orthogonality: float
    peak_tension_pair: Optional[Tuple[str, str]]
    synthesis_candidates: List[SynthesisResultant] = field(default_factory=list)
    pair_tensions: List[TensorPairTension] = field(default_factory=list)


class DialecticTensorGate:
    """
    Autonomous engine that analyzes semantic vector manifolds, measuring
    dialectical opposition and orthogonality. Generates synthesis vectors
    that reconcile competing conceptual forces into coherent architecture.
    """

    def __init__(self, tension_threshold: float = 0.50):
        self.tension_threshold = float(tension_threshold)

    @staticmethod
    def vector_magnitude(vec: List[float]) -> float:
        """Computes Euclidean L2 norm of a vector."""
        return math.sqrt(sum(x * x for x in vec))

    @classmethod
    def calculate_cosine_similarity(cls, v1: List[float], v2: List[float]) -> float:
        """Calculates cosine similarity between two equal-length vectors."""
        if not v1 or not v2 or len(v1) != len(v2):
            return 0.0
        dot = sum(a * b for a, b in zip(v1, v2))
        m1 = cls.vector_magnitude(v1)
        m2 = cls.vector_magnitude(v2)
        if m1 < 1e-9 or m2 < 1e-9:
            return 0.0
        return max(-1.0, min(1.0, dot / (m1 * m2)))

    def evaluate_manifold(
        self,
        vectors: List[DialecticVector],
    ) -> DialecticTensorTelemetry:
        """
        Evaluates all vector pairs across the manifold, measuring orthogonality,
        dialectical tension, and calculating synthesis vectors.
        """
        if not vectors:
            return DialecticTensorTelemetry(
                total_vectors=0,
                evaluated_pairs_count=0,
                mean_orthogonality=1.0,
                peak_tension_pair=None,
                synthesis_candidates=[],
                pair_tensions=[],
            )

        pair_tensions: List[TensorPairTension] = []
        synthesis_candidates: List[SynthesisResultant] = []
        max_tension = -1.0
        peak_pair: Optional[Tuple[str, str]] = None

        for i in range(len(vectors)):
            for j in range(i + 1, len(vectors)):
                v1 = vectors[i]
                v2 = vectors[j]

                # Ensure equal dimensions by padding shorter vector with zeros
                max_dim = max(len(v1.components), len(v2.components))
                c1 = v1.components + [0.0] * (max_dim - len(v1.components))
                c2 = v2.components + [0.0] * (max_dim - len(v2.components))

                cos_sim = self.calculate_cosine_similarity(c1, c2)
                orthogonality = 1.0 - abs(cos_sim)

                # Tension energy: high when opposing (cos_sim < -0.1)
                tension = max(0.0, -cos_sim)

                if tension > max_tension and tension > 0.0:
                    max_tension = tension
                    peak_pair = (v1.vector_id, v2.vector_id)

                if cos_sim < -0.35:
                    status = "polarized"
                elif orthogonality > 0.70:
                    status = "orthogonal"
                elif cos_sim > 0.75:
                    status = "redundant"
                else:
                    status = "reconciled"

                pair_tensions.append(
                    TensorPairTension(
                        thesis_id=v1.vector_id,
                        antithesis_id=v2.vector_id,
                        cosine_similarity=round(cos_sim, 3),
                        orthogonality_score=round(orthogonality, 3),
                        tension_energy=round(tension, 3),
                        synthesis_opportunity=status,
                    )
                )

                # Generate synthesis vector if polarized or high tension
                if status == "polarized" or tension >= self.tension_threshold:
                    # Synthesis vector: orthogonal projection resolving opposition
                    synth_comp = [(a + b) / 2.0 for a, b in zip(c1, c2)]
                    # Add orthogonal boost in cross-dimension
                    if len(synth_comp) >= 2:
                        synth_comp[0] += 0.5 * (c1[1] - c2[1])
                        synth_comp[1] += 0.5 * (c2[0] - c1[0])

                    synth_mag = self.vector_magnitude(synth_comp)
                    angle_deg = (math.degrees(math.acos(max(-1.0, min(1.0, cos_sim))))) / 2.0

                    synthesis_candidates.append(
                        SynthesisResultant(
                            thesis_id=v1.vector_id,
                            antithesis_id=v2.vector_id,
                            title=f"Synthesis: {v1.title} & {v2.title}",
                            components=[round(x, 2) for x in synth_comp[:4]],
                            synthesis_power=round(max(0.2, synth_mag), 2),
                            resolution_angle_deg=round(angle_deg, 1),
                        )
                    )

        mean_ortho = (
            sum(p.orthogonality_score for p in pair_tensions) / len(pair_tensions)
            if pair_tensions
            else 1.0
        )

        return DialecticTensorTelemetry(
            total_vectors=len(vectors),
            evaluated_pairs_count=len(pair_tensions),
            mean_orthogonality=round(mean_ortho, 3),
            peak_tension_pair=peak_pair,
            synthesis_candidates=synthesis_candidates,
            pair_tensions=pair_tensions,
        )

    def generate_markdown_report(self, telemetry: DialecticTensorTelemetry) -> str:
        """Generates structured markdown audit report with zero em dashes."""
        lines = [
            "# Dialectic Tensor and Semantic Orthogonality Telemetry",
            "",
            "## 1. Manifold Orthogonality Overview",
            f"- **Total Concept Vectors:** {telemetry.total_vectors}",
            f"- **Evaluated Dialectical Pairs:** {telemetry.evaluated_pairs_count}",
            f"- **Mean Manifold Orthogonality:** {round(telemetry.mean_orthogonality * 100.0, 1)}%",
            f"- **Peak Polar Tension Pair:** `{telemetry.peak_tension_pair}`",
            f"- **Active Synthesis Opportunities:** {len(telemetry.synthesis_candidates)}",
            "",
            "## 2. Theoretical Grounding",
            "- **Dialectical Tensegrity:** Opposing thesis-antithesis vectors create structural stability when unified.",
            "- **Vector Orthogonality:** Independent concerns (orthogonality > 0.70) indicate clean modularity.",
            "- **Synthesis Emergence:** Resolving polarization unlocks novel higher-order architectures.",
            "",
            "## 3. Pair Tension and Orthogonality Catalog",
            "| Thesis | Antithesis | Cosine Similarity | Orthogonality | Tension Energy | State |",
            "| :--- | :--- | :--- | :--- | :--- | :--- |",
        ]

        for pt in telemetry.pair_tensions:
            lines.append(
                f"| `{pt.thesis_id}` | `{pt.antithesis_id}` | {pt.cosine_similarity} | {pt.orthogonality_score} | {pt.tension_energy} | `{pt.synthesis_opportunity}` |"
            )

        if telemetry.synthesis_candidates:
            lines.extend([
                "",
                "## 4. Calculated Synthesis Resultants",
                "| Synthesis Title | Thesis Pair | Synthesis Power | Resolution Angle |",
                "| :--- | :--- | :--- | :--- |",
            ])
            for sc in telemetry.synthesis_candidates:
                lines.append(
                    f"| {sc.title} | `{sc.thesis_id}` vs `{sc.antithesis_id}` | {sc.synthesis_power} | {sc.resolution_angle_deg} deg |"
                )

        lines.extend([
            "",
            "## 5. Operational Ergonomics Guidance",
            "- Vectors marked as 'polarized' require deliberate dialectic synthesis rather than compromise.",
            "- Maintain high orthogonality (> 0.70) between system modules to prevent monolithic coupling.",
            "- Use synthesis resultants as foundational pillars for next-generation system capabilities.",
        ])

        return "\n".join(lines)

    def generate_svg(
        self,
        telemetry: DialecticTensorTelemetry,
        width: int = 920,
        height: int = 560,
    ) -> str:
        """Generates publication-grade dark titanium polar dialectic tensor SVG."""
        cx = width // 2
        cy = height // 2
        field_r = 175.0

        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" style="background:#080c18; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">',
            '<defs>',
            '  <radialGradient id="tensorGlow" cx="50%" cy="50%" r="50%">',
            '    <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.22"/>',
            '    <stop offset="65%" stop-color="#0284c7" stop-opacity="0.05"/>',
            '    <stop offset="100%" stop-color="#080c18" stop-opacity="0"/>',
            '  </radialGradient>',
            '  <filter id="vectorGlow" x="-20%" y="-20%" width="140%" height="140%">',
            '    <feDropShadow dx="0" dy="0" stdDeviation="3" flood-color="#38bdf8" flood-opacity="0.8"/>',
            '  </filter>',
            '</defs>',
            '<!-- Polar Dialectic Field -->',
            f'<circle cx="{cx}" cy="{cy}" r="{field_r + 30}" fill="url(#tensorGlow)"/>',
            f'<circle cx="{cx}" cy="{cy}" r="{field_r}" fill="#0f172a" stroke="#1e293b" stroke-width="1.8"/>',
            f'<circle cx="{cx}" cy="{cy}" r="{field_r * 0.66}" fill="none" stroke="#334155" stroke-width="1" stroke-dasharray="3,3"/>',
            f'<circle cx="{cx}" cy="{cy}" r="{field_r * 0.33}" fill="none" stroke="#334155" stroke-width="1" stroke-dasharray="2,2"/>',
        ]

        # Orthogonal axes
        svg_parts.append(f'<line x1="{cx}" y1="{cy - field_r - 10}" x2="{cx}" y2="{cy + field_r + 10}" stroke="#475569" stroke-width="1.2"/>')
        svg_parts.append(f'<line x1="{cx - field_r - 10}" y1="{cy}" x2="{cx + field_r + 10}" cy2="{cy}" stroke="#475569" stroke-width="1.2"/>')

        # Quadrant Labels
        svg_parts.append(f'<text x="{cx + field_r - 30}" y="{cy - field_r + 30}" font-size="9" fill="#38bdf8" font-weight="700">SYNTHESIS ZONE</text>')
        svg_parts.append(f'<text x="{cx - field_r + 20}" y="{cy - field_r + 30}" font-size="9" fill="#ef4444" font-weight="700">POLAR TENSION</text>')
        svg_parts.append(f'<text x="{cx - field_r + 20}" y="{cy + field_r - 20}" font-size="9" fill="#10b981" font-weight="700">ORTHOGONAL</text>')
        svg_parts.append(f'<text x="{cx + field_r - 30}" y="{cy + field_r - 20}" font-size="9" fill="#eab308" font-weight="700">HARMONIC</text>')

        # Plot Synthesis Arcs
        for sc in telemetry.synthesis_candidates:
            rad = math.radians(sc.resolution_angle_deg)
            px = cx + field_r * 0.75 * math.cos(rad)
            py = cy - field_r * 0.75 * math.sin(rad)

            # Synthesis ray from center
            svg_parts.append(
                f'<line x1="{cx}" y1="{cy}" x2="{px}" y2="{py}" stroke="#38bdf8" stroke-width="2.5" filter="url(#vectorGlow)"/>'
            )
            svg_parts.append(
                f'<circle cx="{px}" cy="{py}" r="5" fill="#38bdf8" stroke="#ffffff" stroke-width="1.5"/>'
            )
            svg_parts.append(
                f'<text x="{px + 10}" y="{py + 4}" font-size="9" font-weight="600" fill="#e2e8f0">{html.escape(sc.title[:24])}</text>'
            )

        # HUD Overlay Box
        svg_parts.append(
            f'<rect x="20" y="16" width="340" height="74" rx="8" fill="#0f172a" fill-opacity="0.88" stroke="#1e293b" stroke-width="1"/>'
        )
        svg_parts.append(
            f'<text x="32" y="36" font-size="11" font-weight="700" fill="#38bdf8">DIALECTIC TENSOR HUD</text>'
        )
        svg_parts.append(
            f'<text x="32" y="52" font-size="9" fill="#94a3b8">Vectors: {telemetry.total_vectors} | Pairs: {telemetry.evaluated_pairs_count} | Orthogonality: {round(telemetry.mean_orthogonality * 100.0, 1)}%</text>'
        )
        svg_parts.append(
            f'<text x="32" y="68" font-size="9" fill="#94a3b8">Synthesis Opportunities: {len(telemetry.synthesis_candidates)} | Peak Tension: {telemetry.peak_tension_pair}</text>'
        )

        svg_parts.append('</svg>')
        return "\n".join(svg_parts)


def sample_dialectic_vectors() -> List[DialecticVector]:
    """Generates demonstration dialectic vector set."""
    return [
        DialecticVector("vec-thesis", "Centralized Immutability", [1.0, 0.2, -0.8, 0.1], "architecture"),
        DialecticVector("vec-antithesis", "Decentralized Autonomy", [-0.9, -0.1, 0.85, -0.2], "architecture"),
        DialecticVector("vec-ux", "Zero-Friction Simplicity", [0.1, 0.95, 0.2, -0.1], "experience"),
        DialecticVector("vec-audit", "Exhaustive Telemetry", [0.0, -0.8, -0.1, 0.9], "observability"),
        DialecticVector("vec-edge", "Offline Execution", [-0.3, 0.4, 0.7, 0.1], "runtime"),
    ]
