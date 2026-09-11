"""
Polyhedral Schema Crystallizer and Dimensionality Folder Engine
Autonomous cognitive spatial module projecting high-dimensional concept networks
onto regular polyhedral faces (tetrahedrons, cubes, octahedrons) and rendering
flat unfoldable 2D net blueprints. Grounded in Eide & Eide Spatial Reasoning (S-strengths),
dihedral fold geometry, and cognitive spatial crystallization.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Any
import math
import html


@dataclass
class PolyhedralFace:
    """Represents a geometric face of an unfolded polyhedral net containing conceptual data."""
    face_id: int
    title: str
    concept_summary: str
    adjacent_face_ids: List[int]
    center_x: float
    center_y: float
    polygon_vertices: List[Tuple[float, float]]
    color_hex: str = "#38bdf8"
    dihedral_angle_deg: float = 70.5


@dataclass
class PolyhedralNet:
    """Geometric net blueprint for an unfolded 3D regular polyhedron."""
    polyhedron_type: str  # tetrahedron, cube, octahedron
    face_count: int
    faces: List[PolyhedralFace] = field(default_factory=list)
    crystallization_coherence: float = 1.0


@dataclass
class CrystallizerTelemetry:
    """Comprehensive telemetry report for polyhedral schema crystallization."""
    input_concepts_count: int
    selected_polyhedron: str
    face_coverage_ratio: float
    mean_dihedral_angle_deg: float
    polyhedral_net: PolyhedralNet
    spatial_crystallization_score: float


FACE_COLORS = [
    "#38bdf8", "#818cf8", "#c084fc", "#f472b6",
    "#fb7185", "#fb923c", "#facc15", "#4ade80"
]


class PolyhedralSchemaCrystallizer:
    """
    Autonomous engine that maps conceptual clusters to 3D polyhedral geometries
    and calculates unfoldable 2D spatial net coordinates.
    """

    def __init__(self, default_scale_px: float = 70.0):
        self.scale_px = float(default_scale_px)

    def crystallize_schema(
        self,
        concepts: List[Dict[str, str]],
        polyhedron_type: str = "auto",
    ) -> CrystallizerTelemetry:
        """
        Maps concepts to faces of a regular polyhedron and produces
        unfolded 2D net coordinates with dihedral angular relationships.
        """
        n_concepts = len(concepts)

        if polyhedron_type == "auto":
            if n_concepts <= 4:
                p_type = "tetrahedron"
            elif n_concepts <= 6:
                p_type = "cube"
            else:
                p_type = "octahedron"
        else:
            p_type = polyhedron_type.lower()

        faces: List[PolyhedralFace] = []

        if p_type == "tetrahedron":
            # 4 equilateral triangular faces (1 central, 3 perimeter)
            # Center of net at (460, 270)
            cx, cy = 460.0, 270.0
            s = self.scale_px * 1.5
            h = s * math.sqrt(3.0) / 2.0

            # Face 0 (central base triangle, pointing up)
            v0 = (cx, cy - (2.0 / 3.0) * h)
            v1 = (cx - s / 2.0, cy + (1.0 / 3.0) * h)
            v2 = (cx + s / 2.0, cy + (1.0 / 3.0) * h)
            f0_verts = [v0, v1, v2]

            # Face 1 (top wing, inverted)
            v1_top = (cx, cy - (4.0 / 3.0) * h)
            f1_verts = [v0, (cx - s / 2.0, cy - (2.0 / 3.0) * h), v1_top]  # Simplified triangular flap

            # Face 2 (bottom left wing)
            f2_verts = [v1, (cx - s, cy + (1.0 / 3.0) * h), (cx - s / 2.0, cy + (4.0 / 3.0) * h)]

            # Face 3 (bottom right wing)
            f3_verts = [v2, (cx + s / 2.0, cy + (4.0 / 3.0) * h), (cx + s, cy + (1.0 / 3.0) * h)]

            face_vert_list = [f0_verts, f1_verts, f2_verts, f3_verts]
            face_centers = [
                (cx, cy),
                (cx, cy - 0.8 * h),
                (cx - 0.65 * s, cy + 0.6 * h),
                (cx + 0.65 * s, cy + 0.6 * h),
            ]
            adjacencies = [
                [1, 2, 3],
                [0],
                [0],
                [0],
            ]
            dihedral = 70.53

        elif p_type == "cube":
            # 6 square faces in a Latin cross pattern
            cx, cy = 460.0, 280.0
            s = self.scale_px * 1.3
            # Cross:
            #       [1]
            #   [4] [0] [5]
            #       [2]
            #       [3]
            face_centers = [
                (cx, cy),          # 0: center
                (cx, cy - s),      # 1: top
                (cx, cy + s),      # 2: bottom 1
                (cx, cy + 2 * s),  # 3: bottom 2
                (cx - s, cy),      # 4: left
                (cx + s, cy),      # 5: right
            ]
            face_vert_list = []
            for fx, fy in face_centers:
                hw = s / 2.0
                face_vert_list.append([
                    (fx - hw, fy - hw),
                    (fx + hw, fy - hw),
                    (fx + hw, fy + hw),
                    (fx - hw, fy + hw),
                ])
            adjacencies = [
                [1, 2, 4, 5],
                [0],
                [0, 3],
                [2],
                [0],
                [0],
            ]
            dihedral = 90.0

        else:  # Octahedron
            # 8 triangular faces in a dual-diamond net
            p_type = "octahedron"
            cx, cy = 460.0, 280.0
            s = self.scale_px * 1.2
            h = s * math.sqrt(3.0) / 2.0

            face_centers = [
                (cx - 1.5 * s, cy - 0.5 * h),
                (cx - 0.5 * s, cy - 0.5 * h),
                (cx + 0.5 * s, cy - 0.5 * h),
                (cx + 1.5 * s, cy - 0.5 * h),
                (cx - 1.5 * s, cy + 0.5 * h),
                (cx - 0.5 * s, cy + 0.5 * h),
                (cx + 0.5 * s, cy + 0.5 * h),
                (cx + 1.5 * s, cy + 0.5 * h),
            ]
            face_vert_list = []
            for i, (fx, fy) in enumerate(face_centers):
                invert = (i % 2 == 1) if i < 4 else (i % 2 == 0)
                sgn = -1.0 if invert else 1.0
                face_vert_list.append([
                    (fx, fy - sgn * (2.0 / 3.0) * h),
                    (fx - s / 2.0, fy + sgn * (1.0 / 3.0) * h),
                    (fx + s / 2.0, fy + sgn * (1.0 / 3.0) * h),
                ])
            adjacencies = [
                [1, 4], [0, 2, 5], [1, 3, 6], [2, 7],
                [0, 5], [1, 4, 6], [2, 5, 7], [3, 6],
            ]
            dihedral = 109.47

        # Assign concepts to faces
        n_faces = len(face_centers)
        for i in range(n_faces):
            c = concepts[i] if i < len(concepts) else {}
            title = c.get("title", f"Face {i + 1}")
            summary = c.get("text", c.get("summary", "Unallocated semantic zone"))
            color = FACE_COLORS[i % len(FACE_COLORS)]

            faces.append(
                PolyhedralFace(
                    face_id=i + 1,
                    title=title,
                    concept_summary=summary,
                    adjacent_face_ids=[a + 1 for a in adjacencies[i]],
                    center_x=round(face_centers[i][0], 1),
                    center_y=round(face_centers[i][1], 1),
                    polygon_vertices=[(round(vx, 1), round(vy, 1)) for vx, vy in face_vert_list[i]],
                    color_hex=color,
                    dihedral_angle_deg=round(dihedral, 2),
                )
            )

        coverage = min(1.0, n_concepts / max(1, n_faces))
        coherence = round(0.7 + 0.3 * coverage, 2)

        net = PolyhedralNet(
            polyhedron_type=p_type,
            face_count=n_faces,
            faces=faces,
            crystallization_coherence=coherence,
        )

        return CrystallizerTelemetry(
            input_concepts_count=n_concepts,
            selected_polyhedron=p_type,
            face_coverage_ratio=round(coverage, 2),
            mean_dihedral_angle_deg=round(dihedral, 2),
            polyhedral_net=net,
            spatial_crystallization_score=coherence,
        )

    def generate_markdown_report(self, telemetry: CrystallizerTelemetry) -> str:
        """Generates structured markdown audit report with zero em dashes."""
        net = telemetry.polyhedral_net
        lines = [
            "# Polyhedral Schema Crystallizer and Dimensionality Folder Report",
            "",
            "## 1. Geometric Net Crystallization Overview",
            f"- **Input Concepts Loaded:** {telemetry.input_concepts_count}",
            f"- **Selected 3D Polyhedral Target:** {telemetry.selected_polyhedron.capitalize()}",
            f"- **Net Face Count:** {net.face_count} regular faces",
            f"- **Face Semantic Coverage:** {int(telemetry.face_coverage_ratio * 100)}%",
            f"- **Dihedral Fold Angle:** {telemetry.mean_dihedral_angle_deg} deg",
            f"- **Spatial Crystallization Score:** {telemetry.spatial_crystallization_score} (Scale: 0.0 to 1.0)",
            "",
            "## 2. Neuro-Cognitive Theoretical Grounding (Eide & Eide S-Strengths)",
            "- **3D Spatial Mental Manipulation:** Dyslexic thinkers excel at folding and rotating 3D structures mentally.",
            "- **Polyhedral Net Decoupling:** Mapping high-dimensional arguments onto regular polyhedral faces removes linear sprawl.",
            "- **Dihedral Adjacency Invariants:** Physical folds preserve topological adjacency during dimensional transitions.",
            "",
            "## 3. Polyhedral Face Allocation Blueprint",
            "| Face ID | Title | Summary Core | Adjacent Faces | Fold Angle | Color | Center (x, y) |",
            "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |",
        ]

        for f in net.faces:
            adj_str = ", ".join(f"F{aid}" for aid in f.adjacent_face_ids)
            lines.append(
                f"| F{f.face_id} | {f.title} | {f.concept_summary[:32]} | {adj_str} | {f.dihedral_angle_deg} deg | `{f.color_hex}` | ({f.center_x}, {f.center_y}) |"
            )

        lines.extend([
            "",
            "## 4. Operational Ergonomics Recommendations",
            "- Fold adjacent faces into 3D mental palaces to resolve trade-offs between competing requirements.",
            "- Use the unfolded net as a tactile physical layout printed on desk cards or whiteboards.",
            "- In multi-stakeholder reviews, project the 3D rotating model to align mental models instantaneously.",
        ])

        return "\n".join(lines)

    def generate_svg(
        self,
        telemetry: CrystallizerTelemetry,
        width: int = 920,
        height: int = 560,
    ) -> str:
        """Generates publication-grade dark titanium polyhedral net blueprint SVG."""
        net = telemetry.polyhedral_net
        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" style="background:#090d18; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">',
            '<defs>',
            '  <filter id="polyGlow" x="-20%" y="-20%" width="140%" height="140%">',
            '    <feGaussianBlur stdDeviation="3" result="blur"/>',
            '    <feComposite in="SourceGraphic" in2="blur" operator="over"/>',
            '  </filter>',
            '</defs>',
            f'<rect x="0" y="0" width="{width}" height="{height}" fill="#090d18"/>',
            '<!-- Blueprint Construction Grid -->',
        ]

        for gx in range(0, width, 40):
            svg_parts.append(f'<line x1="{gx}" y1="0" x2="{gx}" y2="{height}" stroke="#1e293b" stroke-width="0.5" opacity="0.25"/>')
        for gy in range(0, height, 40):
            svg_parts.append(f'<line x1="0" y1="{gy}" x2="{width}" y2="{gy}" stroke="#1e293b" stroke-width="0.5" opacity="0.25"/>')

        # Draw Face Polygons and Fold Lines
        for f in net.faces:
            pts_str = " ".join(f"{vx},{vy}" for vx, vy in f.polygon_vertices)
            svg_parts.append(
                f'<polygon points="{pts_str}" fill="{f.color_hex}" fill-opacity="0.15" stroke="{f.color_hex}" stroke-width="1.8" filter="url(#polyGlow)"/>'
            )
            # Draw Face Center Marker and Label
            svg_parts.append(
                f'<circle cx="{f.center_x}" cy="{f.center_y}" r="4" fill="{f.color_hex}"/>'
            )
            svg_parts.append(
                f'<text x="{f.center_x}" y="{f.center_y - 8}" font-size="10" font-weight="700" fill="#ffffff" text-anchor="middle">F{f.face_id}: {html.escape(f.title[:12])}</text>'
            )
            svg_parts.append(
                f'<text x="{f.center_x}" y="{f.center_y + 12}" font-size="8" fill="#94a3b8" text-anchor="middle">{f.dihedral_angle_deg} deg fold</text>'
            )

        # HUD Box
        svg_parts.append(
            f'<rect x="20" y="20" width="390" height="74" rx="8" fill="#0f172a" fill-opacity="0.92" stroke="#38bdf8" stroke-width="1.2"/>'
        )
        svg_parts.append(
            f'<text x="32" y="38" font-size="11" font-weight="700" fill="#38bdf8">POLYHEDRAL SCHEMA CRYSTALLIZER HUD</text>'
        )
        svg_parts.append(
            f'<text x="32" y="54" font-size="9" fill="#94a3b8">Target: {net.polyhedron_type.upper()} | Faces: {net.face_count} | Coverage: {int(telemetry.face_coverage_ratio * 100)}%</text>'
        )
        svg_parts.append(
            f'<text x="32" y="70" font-size="9" fill="#94a3b8">Fold Angle: {telemetry.mean_dihedral_angle_deg} deg | Coherence: {telemetry.spatial_crystallization_score}</text>'
        )

        svg_parts.append('</svg>')
        return "\n".join(svg_parts)


def sample_crystallizer_concepts() -> List[Dict[str, str]]:
    """Generates demonstration concept cards for polyhedral crystallization."""
    return [
        {"title": "Core Consensus", "text": "Cryptographic distributed consensus and leaderless state synchronization."},
        {"title": "Storage Layer", "text": "Immutable append-only write ahead logging with partitioned columnar shards."},
        {"title": "Network Fabric", "text": "P2P gossip overlay protocol with anti-entropy reconciliation loops."},
        {"title": "Egress Gateway", "text": "Zero-trust API reverse proxy enforcing mTLS authentication envelopes."},
        {"title": "Observability", "text": "Distributed OpenTelemetry spans streaming to high-cardinality time series indices."},
        {"title": "Chaos Armor", "text": "Automated fault injection simulating split-brain network partitions."},
    ]
