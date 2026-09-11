"""
Topological Tesseract Lattice & 4D Schema Morphing Engine
Autonomous cognitive spatial module for 4-dimensional hypercube projection,
multi-axis conceptual orthogonalization, and planar stereoscopic wireframe
slicing. Grounded in Eide & Eide M-I-N-D framework, 4D spatial reasoning,
and orthogonal cognitive architecture decoupling.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
import math
import html


@dataclass
class HyperVertex:
    """Represents a 4D vertex in {-1, 1}^4 hyper-dimensional schema space."""
    vertex_id: str
    coords_4d: Tuple[float, float, float, float]  # (x, y, z, w)
    title: str
    axis_labels: Dict[str, str] = field(default_factory=dict)
    active: bool = True


@dataclass
class HyperEdge:
    """Represents a 1D edge connecting two vertices along a 4D axis."""
    source_id: str
    target_id: str
    axis_dimension: int  # 0: X, 1: Y, 2: Z, 3: W
    weight: float = 1.0


@dataclass
class TesseractProjection:
    """Projected 2D coordinates and depth profiles for a hyper-vertex."""
    vertex_id: str
    proj_x: float
    proj_y: float
    depth_z: float
    w_depth: float
    title: str


@dataclass
class TesseractTelemetry:
    """Comprehensive telemetry report for 4D schema hypercube projection."""
    total_vertices: int
    total_edges: int
    rotation_angles_deg: Tuple[float, float]
    cell_count: int
    symmetry_metric: float
    projected_vertices: List[TesseractProjection] = field(default_factory=list)
    edges: List[HyperEdge] = field(default_factory=list)


AXIS_NAMES = ["Domain (X)", "Execution (Y)", "Agency (Z)", "Bandwidth (W)"]


class TopologicalTesseractLattice:
    """
    Autonomous engine that manages 4-dimensional conceptual tesseracts.
    Rotates hyper-dimensional schemata in 4D space and projects them down
    to intuitive 2D/3D planar wireframes without semantic tangle.
    """

    def __init__(
        self,
        camera_distance_4d: float = 3.2,
        camera_distance_3d: float = 4.5,
        default_scale: float = 135.0,
    ):
        self.dist_4d = max(1.5, float(camera_distance_4d))
        self.dist_3d = max(1.5, float(camera_distance_3d))
        self.scale = max(20.0, float(default_scale))

    def rotate_4d(
        self,
        x: float,
        y: float,
        z: float,
        w: float,
        theta_rad: float,
        phi_rad: float,
    ) -> Tuple[float, float, float, float]:
        """
        Applies dual isoclinic/planar 4D rotations:
        R_xw(theta) in the X-W plane and R_zw(phi) in the Z-W plane.
        """
        # Rotation in X-W plane
        cos_t = math.cos(theta_rad)
        sin_t = math.sin(theta_rad)
        rx = x * cos_t - w * sin_t
        rw = x * sin_t + w * cos_t

        # Rotation in Z-W plane
        cos_p = math.cos(phi_rad)
        sin_p = math.sin(phi_rad)
        rz = z * cos_p - rw * sin_p
        final_w = z * sin_p + rw * cos_p

        return rx, y, rz, final_w

    def project_vertex(
        self,
        rx: float,
        ry: float,
        rz: float,
        rw: float,
        center_x: float,
        center_y: float,
    ) -> Tuple[float, float, float, float]:
        """
        Perspective projection from 4D to 3D, followed by perspective
        projection from 3D to 2D screen coordinates.
        """
        # 4D to 3D perspective foreshortening
        scale_4d = self.dist_4d / (self.dist_4d - rw if abs(self.dist_4d - rw) > 1e-4 else 1e-4)
        x3 = rx * scale_4d
        y3 = ry * scale_4d
        z3 = rz * scale_4d

        # 3D to 2D projection
        scale_3d = self.dist_3d / (self.dist_3d - z3 if abs(self.dist_3d - z3) > 1e-4 else 1e-4)
        px = center_x + x3 * scale_3d * self.scale
        py = center_y + y3 * scale_3d * self.scale

        return px, py, z3, rw

    def solve_lattice(
        self,
        vertices: List[HyperVertex],
        edges: List[HyperEdge],
        theta_deg: float = 35.0,
        phi_deg: float = 25.0,
        center_x: float = 460.0,
        center_y: float = 280.0,
    ) -> TesseractTelemetry:
        """
        Transforms 4D hyper-vertices through 4D rotation and double perspective
        projection onto the viewing canvas.
        """
        theta_rad = math.radians(theta_deg)
        phi_rad = math.radians(phi_deg)

        projected: List[TesseractProjection] = []

        for v in vertices:
            vx, vy, vz, vw = v.coords_4d
            rx, ry, rz, rw = self.rotate_4d(vx, vy, vz, vw, theta_rad, phi_rad)
            px, py, depth_z, w_depth = self.project_vertex(rx, ry, rz, rw, center_x, center_y)

            projected.append(
                TesseractProjection(
                    vertex_id=v.vertex_id,
                    proj_x=round(px, 2),
                    proj_y=round(py, 2),
                    depth_z=round(depth_z, 3),
                    w_depth=round(w_depth, 3),
                    title=v.title,
                )
            )

        # Symmetry score (1.0 = balanced canonical hypercube)
        mean_x = sum(p.proj_x for p in projected) / max(1, len(projected))
        mean_y = sum(p.proj_y for p in projected) / max(1, len(projected))
        offset_dist = math.hypot(mean_x - center_x, mean_y - center_y)
        symmetry = round(max(0.0, 1.0 - (offset_dist / 100.0)), 3)

        return TesseractTelemetry(
            total_vertices=len(vertices),
            total_edges=len(edges),
            rotation_angles_deg=(round(theta_deg, 1), round(phi_deg, 1)),
            cell_count=8,  # Canonical 8 hypercube cubic cells
            symmetry_metric=symmetry,
            projected_vertices=projected,
            edges=edges,
        )

    def generate_markdown_report(self, telemetry: TesseractTelemetry) -> str:
        """Generates structured markdown audit report with zero em dashes."""
        lines = [
            "# Topological Tesseract Lattice and 4D Schema Telemetry",
            "",
            "## 1. Hyper-Dimensional Projection Overview",
            f"- **Total Hyper-Vertices:** {telemetry.total_vertices} (Canonical 16-Cell System)",
            f"- **Orthogonal Edges:** {telemetry.total_edges} (32 Dimensional Tethers)",
            f"- **4D Rotation Angles:** X-W {telemetry.rotation_angles_deg[0]} deg, Z-W {telemetry.rotation_angles_deg[1]} deg",
            f"- **Hypercube Cubic Cells:** {telemetry.cell_count}",
            f"- **Projection Symmetry Score:** {round(telemetry.symmetry_metric * 100.0, 1)}%",
            "",
            "## 2. Theoretical Grounding",
            "- **4-Dimensional Schema Decoupling:** Orthogonal axes eliminate planar coupling and circular dependency loops.",
            "- **Double Perspective Foreshortening:** Preserves relative depth and inner vs outer cell nesting.",
            "- **Isoclinic Rotational Invariance:** Allows inspecting internal cubic cells without occluding boundary anchors.",
            "",
            "## 3. Projected Hyper-Vertex Coordinates",
            "| Vertex ID | Semantic Title | Canvas (x, y) | Z-Depth | W-Depth |",
            "| :--- | :--- | :--- | :--- | :--- |",
        ]

        for p in telemetry.projected_vertices:
            lines.append(
                f"| `{p.vertex_id}` | {p.title} | ({p.proj_x}, {p.proj_y}) | {p.depth_z} | {p.w_depth} |"
            )

        lines.extend([
            "",
            "## 4. Operational Ergonomics Guidance",
            "- Inner cube vertices represent core conceptual invariants, outer cube vertices represent surface adapters.",
            "- Connecting diagonal tethers bridge domain logic to runtime infrastructure.",
            "- Adjusting rotation angle unfolds hidden architectural facets without spatial jitter.",
        ])

        return "\n".join(lines)

    def generate_svg(
        self,
        telemetry: TesseractTelemetry,
        width: int = 920,
        height: int = 560,
    ) -> str:
        """Generates publication-grade dark titanium 4D wireframe tesseract SVG."""
        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" style="background:#070b14; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">',
            '<defs>',
            '  <radialGradient id="hyperGlow" cx="50%" cy="50%" r="50%">',
            '    <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.18"/>',
            '    <stop offset="65%" stop-color="#0284c7" stop-opacity="0.04"/>',
            '    <stop offset="100%" stop-color="#070b14" stop-opacity="0"/>',
            '  </radialGradient>',
            '  <filter id="nodeGlow" x="-30%" y="-30%" width="160%" height="160%">',
            '    <feDropShadow dx="0" dy="0" stdDeviation="3" flood-color="#38bdf8" flood-opacity="0.7"/>',
            '  </filter>',
            '</defs>',
            '<!-- Background Atmosphere -->',
            f'<circle cx="{width // 2}" cy="{height // 2}" r="260" fill="url(#hyperGlow)"/>',
        ]

        v_map = {p.vertex_id: p for p in telemetry.projected_vertices}

        # Draw 32 Hypercube Edges
        # Differentiate edge colors based on axis dimension
        dim_colors = ["#0284c7", "#10b981", "#f59e0b", "#a855f7"]
        for edge in telemetry.edges:
            p1 = v_map.get(edge.source_id)
            p2 = v_map.get(edge.target_id)
            if p1 and p2:
                col = dim_colors[edge.axis_dimension % len(dim_colors)]
                # Opacity scales with average w-depth
                avg_w = (p1.w_depth + p2.w_depth) / 2.0
                opacity = max(0.25, min(0.85, 0.55 + avg_w * 0.25))
                svg_parts.append(
                    f'<line x1="{p1.proj_x}" y1="{p1.proj_y}" x2="{p2.proj_x}" y2="{p2.proj_y}" stroke="{col}" stroke-width="1.4" opacity="{round(opacity, 2)}"/>'
                )

        # Draw 16 Hyper-Vertices
        for p in telemetry.projected_vertices:
            # Radius scales with w_depth (outer cube larger, inner cube smaller)
            r = max(5.0, min(11.0, 7.5 + p.w_depth * 2.0))
            is_inner = p.w_depth < 0.0
            fill_c = "#0f172a" if is_inner else "#0284c7"
            stroke_c = "#38bdf8" if is_inner else "#ffffff"

            svg_parts.append(
                f'<circle cx="{p.proj_x}" cy="{p.proj_y}" r="{r}" fill="{fill_c}" stroke="{stroke_c}" stroke-width="1.8" filter="url(#nodeGlow)"/>'
            )
            svg_parts.append(
                f'<text x="{p.proj_x}" y="{p.proj_y + r + 11}" font-size="8" font-weight="600" fill="#e2e8f0" text-anchor="middle">{html.escape(p.title)}</text>'
            )

        # HUD Overlay Box
        svg_parts.append(
            f'<rect x="20" y="16" width="340" height="74" rx="8" fill="#0f172a" fill-opacity="0.88" stroke="#1e293b" stroke-width="1"/>'
        )
        svg_parts.append(
            f'<text x="32" y="36" font-size="11" font-weight="700" fill="#38bdf8">TOPOLOGICAL TESSERACT HUD</text>'
        )
        svg_parts.append(
            f'<text x="32" y="52" font-size="9" fill="#94a3b8">Rotation: X-W {telemetry.rotation_angles_deg[0]} deg, Z-W {telemetry.rotation_angles_deg[1]} deg | 16 Vertices, 32 Edges</text>'
        )
        svg_parts.append(
            f'<text x="32" y="68" font-size="9" fill="#94a3b8">Projection Symmetry: {round(telemetry.symmetry_metric * 100.0, 1)}% | 8 Canonical Cubic Cells</text>'
        )

        svg_parts.append('</svg>')
        return "\n".join(svg_parts)


def sample_4d_schema_hypercube() -> Tuple[List[HyperVertex], List[HyperEdge]]:
    """Generates canonical 16-vertex, 32-edge 4D hypercube schema."""
    vertices: List[HyperVertex] = []
    edges: List[HyperEdge] = []

    # 16 vertices: bit permutations of (x, y, z, w) where each is -1 or +1
    titles = [
        "Contract Core", "Static Runtime", "Interactive Core", "Active Runtime",
        "Deep Contract", "Deep Runtime", "Deep Interactive", "Deep Active",
        "Surface Contract", "Surface Runtime", "Surface UI", "Surface Event",
        "Edge Contract", "Edge Runtime", "Edge Gateway", "Edge Observer",
    ]

    idx = 0
    for w in [-1.0, 1.0]:
        for z in [-1.0, 1.0]:
            for y in [-1.0, 1.0]:
                for x in [-1.0, 1.0]:
                    v_id = f"v-{idx}"
                    title = titles[idx] if idx < len(titles) else f"Vertex {idx}"
                    labels = {
                        "X": "Macro" if x > 0 else "Micro",
                        "Y": "Dynamic" if y > 0 else "Static",
                        "Z": "Interactive" if z > 0 else "Autonomous",
                        "W": "Deep" if w > 0 else "Surface",
                    }
                    vertices.append(HyperVertex(v_id, (x, y, z, w), title, labels))
                    idx += 1

    # 32 edges: connect pairs differing by exactly 1 coordinate
    for i in range(len(vertices)):
        for j in range(i + 1, len(vertices)):
            c1 = vertices[i].coords_4d
            c2 = vertices[j].coords_4d
            diffs = [k for k in range(4) if c1[k] != c2[k]]
            if len(diffs) == 1:
                edges.append(
                    HyperEdge(
                        source_id=vertices[i].vertex_id,
                        target_id=vertices[j].vertex_id,
                        axis_dimension=diffs[0],
                    )
                )

    return vertices, edges
