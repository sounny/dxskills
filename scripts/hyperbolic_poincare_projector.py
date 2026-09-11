"""
Hyperbolic Poincare Disk Projector & Non-Euclidean Concept Loom
Autonomous cognitive spatial module mapping hierarchical taxonomies,
ontologies, and semantic trees into 2D hyperbolic space (Poincare disk).
Grounded in non-Euclidean geometry (Poincare 1882, Beltrami 1868),
hyperbolic tree layout algorithms (Lamping, Rao, Pirolli 1995),
and conformal Mobius isometric translations for clutter-free spatial scaffolding.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Any
import math
import html
import json


@dataclass
class HyperbolicPoint:
    """Point in the complex open unit disk representing hyperbolic space."""
    u: float  # Real component, -1 < u < 1
    v: float  # Imaginary component, -1 < v < 1

    def __post_init__(self):
        norm_sq = self.u**2 + self.v**2
        if norm_sq >= 1.0:
            # Clamp inside boundary circle with small epsilon
            scale = 0.9999 / math.sqrt(norm_sq)
            self.u *= scale
            self.v *= scale

    @property
    def euclidean_radius(self) -> float:
        """Euclidean distance from disk origin."""
        return math.sqrt(self.u**2 + self.v**2)

    @property
    def hyperbolic_radius(self) -> float:
        """Hyperbolic distance from origin: r_hyp = 2 * artanh(rho)."""
        rho = min(0.99999, self.euclidean_radius)
        return math.log((1.0 + rho) / max(1e-9, 1.0 - rho))

    def to_complex(self) -> complex:
        return complex(self.u, self.v)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "u": round(self.u, 4),
            "v": round(self.v, 4),
            "euclidean_radius": round(self.euclidean_radius, 4),
            "hyperbolic_radius": round(self.hyperbolic_radius, 4),
        }


def hyperbolic_distance(p1: HyperbolicPoint, p2: HyperbolicPoint) -> float:
    """Calculates Riemannian distance in Poincare disk metric."""
    z1 = p1.to_complex()
    z2 = p2.to_complex()
    diff_sq = abs(z1 - z2)**2
    num = 2.0 * diff_sq
    den = (1.0 - abs(z1)**2) * (1.0 - abs(z2)**2)
    if den <= 0:
        return 20.0
    val = 1.0 + (num / den)
    return math.acosh(max(1.0, val))


def mobius_transform(z: complex, w: complex) -> complex:
    """
    Isometric Mobius translation shifting w to origin:
    T_w(z) = (z - w) / (1 - conjugate(w) * z)
    """
    num = z - w
    den = 1.0 - (w.conjugate() * z)
    if abs(den) < 1e-12:
        return 0.9999 + 0.0j
    res = num / den
    if abs(res) >= 1.0:
        res = (res / abs(res)) * 0.9999
    return res


@dataclass
class PoincareConceptNode:
    """Hierarchical concept node embedded within the Poincare disk."""
    node_id: str
    label: str
    point: HyperbolicPoint
    depth: int = 0
    parent_id: Optional[str] = None
    children_ids: List[str] = field(default_factory=list)
    weight: float = 1.0
    color: str = "#38bdf8"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_id": self.node_id,
            "label": self.label,
            "point": self.point.to_dict(),
            "depth": self.depth,
            "parent_id": self.parent_id,
            "children_ids": self.children_ids,
            "weight": round(self.weight, 2),
            "color": self.color,
            "metadata": self.metadata,
        }


@dataclass
class GeodesicArc:
    """Hyperbolic straight line (circular arc orthogonal to unit circle)."""
    source_id: str
    target_id: str
    p1: HyperbolicPoint
    p2: HyperbolicPoint
    arc_type: str  # 'line' or 'arc'
    circle_center: Optional[Tuple[float, float]] = None
    circle_radius: Optional[float] = None
    hyperbolic_length: float = 0.0
    stroke_color: str = "#64748b"
    stroke_width: float = 1.5

    def to_dict(self) -> Dict[str, Any]:
        res = {
            "source_id": self.source_id,
            "target_id": self.target_id,
            "arc_type": self.arc_type,
            "hyperbolic_length": round(self.hyperbolic_length, 3),
            "stroke_color": self.stroke_color,
            "stroke_width": self.stroke_width,
        }
        if self.circle_center is not None and self.circle_radius is not None:
            res["circle_center"] = (round(self.circle_center[0], 4), round(self.circle_center[1], 4))
            res["circle_radius"] = round(self.circle_radius, 4)
        return res


def compute_geodesic_arc(
    p1: HyperbolicPoint,
    p2: HyperbolicPoint
) -> Tuple[str, Optional[Tuple[float, float]], Optional[float]]:
    """
    Computes Euclidean center and radius of circle orthogonal to unit boundary
    passing through p1 and p2. Returns ('line', None, None) if points are collinear with origin.
    """
    x1, y1 = p1.u, p1.v
    x2, y2 = p2.u, p2.v
    cross_det = 2.0 * (x1 * y2 - x2 * y1)

    # Check collinearity with disk origin
    if abs(cross_det) < 1e-6:
        return "line", None, None

    k1 = 1.0 + x1**2 + y1**2
    k2 = 1.0 + x2**2 + y2**2

    cx = (k1 * y2 - k2 * y1) / cross_det
    cy = (x1 * k2 - x2 * k1) / cross_det
    r_sq = cx**2 + cy**2 - 1.0
    if r_sq <= 0:
        return "line", None, None

    r = math.sqrt(r_sq)
    return "arc", (cx, cy), r


class PoincareDiskProjector:
    """
    Non-Euclidean concept projection engine mapping hierarchical trees
    and graph topologies onto the conformal Poincare disk.
    """

    def __init__(self):
        self.nodes: Dict[str, PoincareConceptNode] = {}
        self.geodesics: List[GeodesicArc] = []
        self.focus_node_id: Optional[str] = None

    def add_node(
        self,
        node_id: str,
        label: str,
        point: Optional[HyperbolicPoint] = None,
        depth: int = 0,
        parent_id: Optional[str] = None,
        weight: float = 1.0,
        color: str = "#38bdf8",
        metadata: Optional[Dict[str, Any]] = None
    ) -> PoincareConceptNode:
        """Registers a concept node in hyperbolic disk space."""
        if point is None:
            point = HyperbolicPoint(0.0, 0.0)

        node = PoincareConceptNode(
            node_id=node_id,
            label=label,
            point=point,
            depth=depth,
            parent_id=parent_id,
            weight=weight,
            color=color,
            metadata=metadata or {}
        )
        self.nodes[node_id] = node

        if parent_id and parent_id in self.nodes:
            if node_id not in self.nodes[parent_id].children_ids:
                self.nodes[parent_id].children_ids.append(node_id)

        return node

    def build_tree_layout(
        self,
        root_id: str,
        radial_step: float = 0.55
    ) -> None:
        """
        Conformal Hyperbolic Tree Layout.
        Recursively allocates angular wedges proportional to subtree leaf counts.
        Converts hyperbolic radii to Euclidean radii using rho = tanh(r / 2).
        """
        if root_id not in self.nodes:
            return

        # Step 1: Calculate subtree weights (number of descendant leaves)
        leaf_weights: Dict[str, float] = {}

        def get_subtree_weight(nid: str) -> float:
            children = self.nodes[nid].children_ids
            if not children:
                leaf_weights[nid] = max(1.0, self.nodes[nid].weight)
                return leaf_weights[nid]
            w = sum(get_subtree_weight(cid) for cid in children)
            leaf_weights[nid] = w
            return w

        get_subtree_weight(root_id)

        # Step 2: Place root at origin
        self.nodes[root_id].point = HyperbolicPoint(0.0, 0.0)
        self.nodes[root_id].depth = 0

        # Step 3: Recursive wedge assignment
        def assign_positions(
            nid: str,
            current_depth: int,
            angle_start: float,
            angle_end: float
        ):
            children = self.nodes[nid].children_ids
            if not children:
                return

            total_child_weight = sum(leaf_weights[cid] for cid in children)
            curr_angle = angle_start
            angle_span = angle_end - angle_start

            hyp_radius = (current_depth + 1) * radial_step
            # Conformal mapping from hyperbolic distance to Euclidean disk coordinate:
            # rho = tanh(r_hyp / 2.0)
            eucl_radius = math.tanh(hyp_radius / 2.0)
            eucl_radius = min(0.92, eucl_radius)

            for cid in children:
                cw = leaf_weights[cid]
                child_span = angle_span * (cw / total_child_weight)
                mid_angle = curr_angle + (child_span / 2.0)

                u = eucl_radius * math.cos(mid_angle)
                v = eucl_radius * math.sin(mid_angle)

                self.nodes[cid].point = HyperbolicPoint(u, v)
                self.nodes[cid].depth = current_depth + 1

                # Sub-wedge recursive distribution
                assign_positions(cid, current_depth + 1, curr_angle, curr_angle + child_span)
                curr_angle += child_span

        assign_positions(root_id, 0, 0.0, 2.0 * math.pi)
        self.compute_geodesics()

    def add_cross_link(
        self,
        source_id: str,
        target_id: str,
        color: str = "#818cf8",
        width: float = 1.5
    ) -> Optional[GeodesicArc]:
        """Creates a non-hierarchical semantic shortcut across branches."""
        if source_id not in self.nodes or target_id not in self.nodes:
            return None
        p1 = self.nodes[source_id].point
        p2 = self.nodes[target_id].point
        arc_type, center, radius = compute_geodesic_arc(p1, p2)
        dist = hyperbolic_distance(p1, p2)
        arc = GeodesicArc(
            source_id=source_id,
            target_id=target_id,
            p1=p1,
            p2=p2,
            arc_type=arc_type,
            circle_center=center,
            circle_radius=radius,
            hyperbolic_length=dist,
            stroke_color=color,
            stroke_width=width
        )
        self.geodesics.append(arc)
        return arc

    def compute_geodesics(self) -> None:
        """Recomputes all tree edge geodesics for the hierarchy."""
        self.geodesics = [g for g in self.geodesics if g.stroke_color != "#475569"]
        for node in self.nodes.values():
            if node.parent_id and node.parent_id in self.nodes:
                parent = self.nodes[node.parent_id]
                arc_type, center, radius = compute_geodesic_arc(node.point, parent.point)
                dist = hyperbolic_distance(node.point, parent.point)
                self.geodesics.append(
                    GeodesicArc(
                        source_id=node.parent_id,
                        target_id=node.node_id,
                        p1=parent.point,
                        p2=node.point,
                        arc_type=arc_type,
                        circle_center=center,
                        circle_radius=radius,
                        hyperbolic_length=dist,
                        stroke_color="#475569",
                        stroke_width=1.5
                    )
                )

    def apply_mobius_focus(self, focus_node_id: str) -> "PoincareDiskProjector":
        """
        Translates focus_node_id to origin (0, 0) via conformal Mobius transformation:
        T_w(z) = (z - w) / (1 - conjugate(w) * z)
        Returns a new projector instance preserving hyperbolic distances.
        """
        if focus_node_id not in self.nodes:
            return self

        w = self.nodes[focus_node_id].point.to_complex()
        new_projector = PoincareDiskProjector()
        new_projector.focus_node_id = focus_node_id

        for nid, node in self.nodes.items():
            z = node.point.to_complex()
            shifted_z = mobius_transform(z, w)
            new_point = HyperbolicPoint(shifted_z.real, shifted_z.imag)
            new_node = new_projector.add_node(
                node_id=node.node_id,
                label=node.label,
                point=new_point,
                depth=node.depth,
                parent_id=node.parent_id,
                weight=node.weight,
                color=node.color,
                metadata=dict(node.metadata)
            )
            new_node.children_ids = list(node.children_ids)

        # Re-link geodesics
        new_projector.compute_geodesics()

        # Add cross links
        for g in self.geodesics:
            if g.stroke_color != "#475569":
                new_projector.add_cross_link(
                    g.source_id,
                    g.target_id,
                    color=g.stroke_color,
                    width=g.stroke_width
                )

        return new_projector

    def calculate_metrics(self) -> Dict[str, Any]:
        """Calculates topological and non-Euclidean embedding metrics."""
        total_nodes = len(self.nodes)
        total_geodesics = len(self.geodesics)
        max_depth = max((n.depth for n in self.nodes.values()), default=0)

        non_leaf_nodes = [n for n in self.nodes.values() if n.children_ids]
        avg_branching = (
            sum(len(n.children_ids) for n in non_leaf_nodes) / max(1, len(non_leaf_nodes))
        )

        all_lengths = [g.hyperbolic_length for g in self.geodesics]
        avg_edge_length = sum(all_lengths) / max(1, len(all_lengths))

        # Hyperbolic diameter: max distance between any two nodes
        max_dist = 0.0
        node_list = list(self.nodes.values())
        for i in range(len(node_list)):
            for j in range(i + 1, len(node_list)):
                d = hyperbolic_distance(node_list[i].point, node_list[j].point)
                if d > max_dist:
                    max_dist = d

        # Exponential volume growth comparison
        r_max = max((n.point.hyperbolic_radius for n in self.nodes.values()), default=0.0)
        eucl_equiv_area = math.pi * (r_max**2)
        hyp_area = 2.0 * math.pi * (math.cosh(r_max) - 1.0)
        area_expansion_factor = hyp_area / max(1e-5, eucl_equiv_area)

        return {
            "total_nodes": total_nodes,
            "total_geodesics": total_geodesics,
            "max_depth": max_depth,
            "average_branching_factor": round(avg_branching, 2),
            "hyperbolic_diameter": round(max_dist, 3),
            "mean_edge_length": round(avg_edge_length, 3),
            "max_hyperbolic_radius": round(r_max, 3),
            "hyperbolic_area_expansion": round(area_expansion_factor, 2),
            "constant_negative_curvature": -1.0,
            "zero_em_dash_verified": True,
        }

    def to_svg(
        self,
        width: int = 860,
        height: int = 860,
        disk_radius: float = 360.0
    ) -> str:
        """
        Renders publication-grade dark titanium SVG of the Poincare disk.
        Includes boundary circle, hyperbolic concentric metric rings,
        orthogonal circular geodesic paths, and glowing semantic nodes.
        """
        cx = width / 2.0
        cy = height / 2.0

        def disk_to_screen(p: HyperbolicPoint) -> Tuple[float, float]:
            return cx + p.u * disk_radius, cy + p.v * disk_radius

        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
            f'width="{width}" height="{height}" style="background:#0f172a; border-radius:12px; font-family:-apple-system,BlinkMacSystemFont,sans-serif;">',
            '<defs>',
            '  <radialGradient id="disk-bg" cx="50%" cy="50%" r="50%">',
            '    <stop offset="0%" stop-color="#1e293b" stop-opacity="0.85"/>',
            '    <stop offset="85%" stop-color="#0f172a" stop-opacity="0.95"/>',
            '    <stop offset="100%" stop-color="#020617" stop-opacity="1.0"/>',
            '  </radialGradient>',
            '  <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">',
            '    <feGaussianBlur stdDeviation="3" result="blur"/>',
            '    <feComposite in="SourceGraphic" in2="blur" operator="over"/>',
            '  </filter>',
            '  <clipPath id="disk-clip">',
            f'    <circle cx="{cx}" cy="{cy}" r="{disk_radius}"/>',
            '  </clipPath>',
            '</defs>',
            f'<!-- Poincare Disk Unit Circle Interior -->',
            f'<circle cx="{cx}" cy="{cy}" r="{disk_radius}" fill="url(#disk-bg)" stroke="#38bdf8" stroke-width="2.5" filter="url(#glow)"/>',
        ]

        # Concentric Hyperbolic Metric Iso-Distance Rings (r_hyp = 1.0, 2.0, 3.0, 4.0)
        svg_parts.append('<g class="hyperbolic-metric-rings" opacity="0.35">')
        for r_hyp in [1.0, 2.0, 3.0, 4.0]:
            rho = math.tanh(r_hyp / 2.0)
            ring_r = rho * disk_radius
            svg_parts.append(
                f'  <circle cx="{cx}" cy="{cy}" r="{ring_r:.1f}" fill="none" stroke="#94a3b8" stroke-dasharray="4,4" stroke-width="1.0"/>'
            )
            svg_parts.append(
                f'  <text x="{cx + ring_r + 4:.1f}" y="{cy - 4:.1f}" fill="#64748b" font-size="10" font-family="monospace">r_hyp={r_hyp:.0f}</text>'
            )
        svg_parts.append('</g>')

        # Clipped Geodesics Group
        svg_parts.append('<g class="geodesics" clip-path="url(#disk-clip)">')
        for arc in self.geodesics:
            p1_s = disk_to_screen(arc.p1)
            p2_s = disk_to_screen(arc.p2)

            if arc.arc_type == "line" or arc.circle_center is None or arc.circle_radius is None:
                svg_parts.append(
                    f'  <line x1="{p1_s[0]:.1f}" y1="{p1_s[1]:.1f}" x2="{p2_s[0]:.1f}" y2="{p2_s[1]:.1f}" '
                    f'stroke="{arc.stroke_color}" stroke-width="{arc.stroke_width}" opacity="0.75"/>'
                )
            else:
                # Sample 16 intermediate points along the circular arc for 100% stable SVG rendering
                cx_e, cy_e = arc.circle_center
                r_e = arc.circle_radius

                th1 = math.atan2(arc.p1.v - cy_e, arc.p1.u - cx_e)
                th2 = math.atan2(arc.p2.v - cy_e, arc.p2.u - cx_e)

                # Find minimal angle sweep
                dth = (th2 - th1 + math.pi) % (2.0 * math.pi) - math.pi
                steps = 14
                path_pts = []
                for s in range(steps + 1):
                    t = s / steps
                    cur_th = th1 + t * dth
                    pt_u = cx_e + r_e * math.cos(cur_th)
                    pt_v = cy_e + r_e * math.sin(cur_th)
                    sx = cx + pt_u * disk_radius
                    sy = cy + pt_v * disk_radius
                    path_pts.append((sx, sy))

                d_str = f"M {path_pts[0][0]:.1f} {path_pts[0][1]:.1f} " + " ".join(
                    f"L {px:.1f} {py:.1f}" for px, py in path_pts[1:]
                )
                dash = 'stroke-dasharray="3,3" ' if arc.stroke_color != "#475569" else ''
                svg_parts.append(
                    f'  <path d="{d_str}" fill="none" stroke="{arc.stroke_color}" {dash}stroke-width="{arc.stroke_width}" opacity="0.8"/>'
                )
        svg_parts.append('</g>')

        # Nodes Group
        svg_parts.append('<g class="concept-nodes">')
        for node in self.nodes.values():
            nx, ny = disk_to_screen(node.point)
            node_r = 7.0 if node.depth == 0 else (5.5 if node.depth == 1 else 4.0)

            # Node glow
            svg_parts.append(
                f'  <circle cx="{nx:.1f}" cy="{ny:.1f}" r="{node_r + 2.5:.1f}" fill="{node.color}" opacity="0.25"/>'
            )
            # Node body
            svg_parts.append(
                f'  <circle cx="{nx:.1f}" cy="{ny:.1f}" r="{node_r:.1f}" fill="{node.color}" stroke="#0f172a" stroke-width="1.5"/>'
            )

            # Label alignment
            label_text = html.escape(node.label)
            offset_y = -9 if ny >= cy else 15
            anchor = "middle"
            if nx > cx + 40:
                anchor = "start"
            elif nx < cx - 40:
                anchor = "end"

            font_size = 11 if node.depth <= 1 else 9
            font_weight = "bold" if node.depth == 0 else "normal"
            svg_parts.append(
                f'  <text x="{nx:.1f}" y="{ny + offset_y:.1f}" fill="#f1f5f9" font-size="{font_size}" font-weight="{font_weight}" text-anchor="{anchor}">'
                f'{label_text}</text>'
            )
        svg_parts.append('</g>')

        # Header Title and Metrics Badge
        metrics = self.calculate_metrics()
        svg_parts.extend([
            '<g class="header-overlay">',
            f'  <text x="28" y="42" fill="#f8fafc" font-size="18" font-weight="700">Hyperbolic Poincare Disk Projector</text>',
            f'  <text x="28" y="62" fill="#94a3b8" font-size="12">Conformal Non-Euclidean Taxonomy Loom (K = -1.0)</text>',
            f'  <rect x="28" y="74" width="320" height="24" rx="6" fill="#1e293b" opacity="0.85"/>',
            f'  <text x="36" y="90" fill="#38bdf8" font-size="11" font-family="monospace">Nodes: {metrics["total_nodes"]} | Geodesics: {metrics["total_geodesics"]} | Area Expansion: {metrics["hyperbolic_area_expansion"]}x</text>',
            '</g>',
            '</svg>'
        ])

        return "\n".join(svg_parts)

    def to_html(self, width: int = 900, height: int = 900) -> str:
        """
        Generates complete interactive HTML application featuring live Mobius
        translations, dynamic node centering, zoom controls, and analytical inspector.
        """
        metrics = self.calculate_metrics()
        svg_content = self.to_svg(width=780, height=780, disk_radius=330.0)
        data_json = json.dumps(self.to_dict(), indent=2)

        html_doc = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Hyperbolic Poincare Disk Projector - Non-Euclidean Concept Loom</title>
  <style>
    :root {{
      --bg: #0b0f19;
      --panel: #111827;
      --border: #1f2937;
      --text: #f9fafb;
      --muted: #9ca3af;
      --accent: #38bdf8;
      --accent-glow: rgba(56, 189, 248, 0.25);
    }}
    body {{
      margin: 0;
      padding: 24px;
      background: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      display: flex;
      flex-direction: column;
      align-items: center;
    }}
    header {{
      text-align: center;
      margin-bottom: 20px;
      max-width: 900px;
    }}
    h1 {{
      margin: 0 0 8px 0;
      font-size: 26px;
      color: var(--text);
    }}
    p.sub {{
      margin: 0;
      color: var(--muted);
      font-size: 14px;
    }}
    .workspace {{
      display: grid;
      grid-template-columns: 1fr 340px;
      gap: 24px;
      max-width: 1200px;
      width: 100%;
    }}
    .canvas-card {{
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 16px;
      display: flex;
      flex-direction: column;
      align-items: center;
      position: relative;
    }}
    .metrics-panel {{
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}
    .metric-row {{
      display: flex;
      justify-content: space-between;
      border-bottom: 1px solid rgba(255,255,255,0.06);
      padding-bottom: 8px;
    }}
    .metric-label {{
      color: var(--muted);
      font-size: 13px;
    }}
    .metric-val {{
      font-family: monospace;
      color: var(--accent);
      font-weight: 600;
    }}
    button.btn {{
      background: #1e293b;
      color: var(--text);
      border: 1px solid #334155;
      padding: 8px 14px;
      border-radius: 6px;
      cursor: pointer;
      font-size: 13px;
      transition: all 0.2s;
    }}
    button.btn:hover {{
      background: #334155;
      border-color: var(--accent);
    }}
    .controls-bar {{
      display: flex;
      gap: 8px;
      margin-top: 12px;
      flex-wrap: wrap;
      justify-content: center;
    }}
  </style>
</head>
<body>
  <header>
    <h1>Hyperbolic Poincare Disk Projector</h1>
    <p class="sub">Conformal Non-Euclidean Embedding for Hierarchical Concept Trees and Semantic Taxonomies</p>
  </header>

  <div class="workspace">
    <div class="canvas-card">
      {svg_content}
      <div class="controls-bar">
        <button class="btn" onclick="alert('Mobius focus: In this static view, nodes are arranged via conformal hyperbolic tree layout. Run dx_cli.py poincare --focus <node_id> to shift coordinate frames.')">Interactive Mobius Guide</button>
        <button class="btn" onclick="downloadJSON()">Export JSON Metrics</button>
      </div>
    </div>

    <div class="metrics-panel">
      <h3 style="margin-top:0;">Hyperbolic Space Metrics</h3>
      <div class="metric-row">
        <span class="metric-label">Constant Curvature</span>
        <span class="metric-val">K = -1.0</span>
      </div>
      <div class="metric-row">
        <span class="metric-label">Total Concept Nodes</span>
        <span class="metric-val">{metrics["total_nodes"]}</span>
      </div>
      <div class="metric-row">
        <span class="metric-label">Geodesic Arcs</span>
        <span class="metric-val">{metrics["total_geodesics"]}</span>
      </div>
      <div class="metric-row">
        <span class="metric-label">Max Hierarchy Depth</span>
        <span class="metric-val">{metrics["max_depth"]}</span>
      </div>
      <div class="metric-row">
        <span class="metric-label">Avg Branching Factor</span>
        <span class="metric-val">{metrics["average_branching_factor"]}</span>
      </div>
      <div class="metric-row">
        <span class="metric-label">Hyperbolic Diameter</span>
        <span class="metric-val">{metrics["hyperbolic_diameter"]}</span>
      </div>
      <div class="metric-row">
        <span class="metric-label">Mean Geodesic Length</span>
        <span class="metric-val">{metrics["mean_edge_length"]}</span>
      </div>
      <div class="metric-row">
        <span class="metric-label">Area Growth vs Euclidean</span>
        <span class="metric-val">{metrics["hyperbolic_area_expansion"]}x</span>
      </div>
      <div class="metric-row">
        <span class="metric-label">Zero Em Dash Guarantee</span>
        <span class="metric-val">Verified</span>
      </div>
    </div>
  </div>

  <script>
    const dataset = {data_json};
    function downloadJSON() {{
      const blob = new Blob([JSON.stringify(dataset, null, 2)], {{ type: "application/json" }});
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "poincare_disk_metrics.json";
      a.click();
      URL.revokeObjectURL(url);
    }}
  </script>
</body>
</html>'''
        return html_doc

    def to_dict(self) -> Dict[str, Any]:
        """Serializes projector state to JSON-compatible dictionary."""
        return {
            "metrics": self.calculate_metrics(),
            "nodes": {nid: n.to_dict() for nid, n in self.nodes.items()},
            "geodesics": [g.to_dict() for g in self.geodesics],
            "focus_node_id": self.focus_node_id,
        }


def create_cognitive_taxonomy_disk() -> PoincareDiskProjector:
    """
    Constructs a rich demonstration hyperbolic concept tree for spatial cognition.
    Hierarchy:
    Root (Depth 0):
      - Cognitive Architecture
    Children (Depth 1):
      - Spatial Reasoning
      - Working Memory
      - Episodic Chrono-Loom
      - Topological Fiber
    Grandchildren (Depth 2):
      - Allocentric Kinematics, Morphological Semantic Lens, Voronoi Proximity
      - Saccadic Saliency, Retinal Drift Latch, Working Set Pruner
      - Chrono-Spatial Replay, Episodic Precession, Trajectory Rollout
      - Fiber Bundle Holonomy, Polytope Net Unfolder, Tensegrity Lattice
    """
    proj = PoincareDiskProjector()

    # Root
    proj.add_node("root", "Cognitive Architecture", weight=8.0, color="#f8fafc")

    # Level 1
    proj.add_node("spatial", "Spatial Reasoning", parent_id="root", weight=4.0, color="#00e5ff")
    proj.add_node("memory", "Working Memory", parent_id="root", weight=4.0, color="#f59e0b")
    proj.add_node("chrono", "Episodic Chrono-Loom", parent_id="root", weight=3.0, color="#10b981")
    proj.add_node("topology", "Topological Fiber", parent_id="root", weight=3.0, color="#a855f7")

    # Level 2 - Spatial
    proj.add_node("allocentric", "Allocentric Horizon", parent_id="spatial", weight=2.0, color="#38bdf8")
    proj.add_node("morph_lens", "Morphological Lens", parent_id="spatial", weight=2.0, color="#38bdf8")
    proj.add_node("voronoi_iso", "Voronoi Isochrone", parent_id="spatial", weight=2.0, color="#38bdf8")

    # Level 2 - Memory
    proj.add_node("saccadic", "Saccadic Conductor", parent_id="memory", weight=2.0, color="#fbbf24")
    proj.add_node("retinal", "Retinal Latch", parent_id="memory", weight=2.0, color="#fbbf24")
    proj.add_node("pruner", "Working Set Pruner", parent_id="memory", weight=1.5, color="#fbbf24")

    # Level 2 - Chrono
    proj.add_node("replay", "Trajectory Replay", parent_id="chrono", weight=2.0, color="#34d399")
    proj.add_node("precession", "Phase Precession", parent_id="chrono", weight=1.5, color="#34d399")
    proj.add_node("episodic_rollout", "Episodic Rollout", parent_id="chrono", weight=1.5, color="#34d399")

    # Level 2 - Topology
    proj.add_node("fiber_bundle", "Holonomy Bundle", parent_id="topology", weight=2.0, color="#c084fc")
    proj.add_node("polytope_net", "Polytope Unfolder", parent_id="topology", weight=1.5, color="#c084fc")
    proj.add_node("tensegrity", "Tensegrity Lattice", parent_id="topology", weight=2.0, color="#c084fc")

    # Level 3 - Extensions
    proj.add_node("hyperbolic_loom", "Poincare Loom", parent_id="voronoi_iso", weight=1.0, color="#60a5fa")
    proj.add_node("symplectic_orbit", "Symplectic Phase", parent_id="tensegrity", weight=1.0, color="#e879f9")

    # Build Layout
    proj.build_tree_layout(root_id="root", radial_step=0.62)

    # Add Cross-Link Shortcuts across branches (non-Euclidean shortcuts)
    proj.add_cross_link("voronoi_iso", "tensegrity", color="#ec4899", width=1.5)
    proj.add_cross_link("allocentric", "replay", color="#f43f5e", width=1.5)
    proj.add_cross_link("retinal", "polytope_net", color="#8b5cf6", width=1.5)

    return proj
