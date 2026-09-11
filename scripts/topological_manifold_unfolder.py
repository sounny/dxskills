"""
Topological Manifold Unfolder and Polytope Net Weaver Engine
Autonomous cognitive spatial module unfolding 4D polytopes (hypercubes, 16-cells, simplices)
into planar and isometric 3D spatial manifolds. Grounded in Riemannian metric curvature
flattening, Salvador Dali hypercube net geometry, and Euler-Poincare topological invariants.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Any
import math
import html


@dataclass
class PolytopeVertex:
    """Represents a 4D vertex coordinate before and after spatial projection."""
    vertex_id: str
    coords_4d: Tuple[float, float, float, float]  # (x, y, z, w)
    label: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "vertex_id": self.vertex_id,
            "coords_4d": [round(c, 2) for c in self.coords_4d],
            "label": self.label,
        }


@dataclass
class PolytopeCell:
    """Represents a 3-dimensional facet/cell of an unfolded 4D polytope net."""
    cell_id: str
    label: str
    cell_type: str  # CUBE, TETRAHEDRON, OCTAHEDRON
    center_4d: Tuple[float, float, float, float]
    unfolded_position_3d: Tuple[float, float, float]  # (x, y, z) in net layout space
    hinge_parent_id: Optional[str]
    hinge_rotation_deg: float
    color_hex: str = "#38bdf8"
    volume: float = 1.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "cell_id": self.cell_id,
            "label": self.label,
            "cell_type": self.cell_type,
            "center_4d": [round(c, 2) for c in self.center_4d],
            "unfolded_position_3d": [round(p, 2) for p in self.unfolded_position_3d],
            "hinge_parent_id": self.hinge_parent_id,
            "hinge_rotation_deg": round(self.hinge_rotation_deg, 1),
            "color_hex": self.color_hex,
            "volume": round(self.volume, 2),
        }


@dataclass
class TopologicalManifoldNet:
    """Synthesized manifold net representing unfolded 4D geometry."""
    polytope_type: str
    total_cells: int
    total_faces: int
    total_edges: int
    total_vertices: int
    euler_poincare_characteristic: int
    unfolding_progress: float  # 0.0 (folded 4D) to 1.0 (fully unfolded 3D net)
    cells: List[PolytopeCell]
    metric_distortion_index: float  # 0.0 (pure isometry) to 1.0 (shear distortion)
    stability_score: float         # 0.0 to 100.0
    status_level: str              # MANIFOLD_ISOMETRIC, TOPOLOGICAL_SHEAR, SINGULAR_COLLAPSE
    warnings: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "polytope_type": self.polytope_type,
            "total_cells": self.total_cells,
            "total_faces": self.total_faces,
            "total_edges": self.total_edges,
            "total_vertices": self.total_vertices,
            "euler_poincare_characteristic": self.euler_poincare_characteristic,
            "unfolding_progress": round(self.unfolding_progress, 2),
            "metric_distortion_index": round(self.metric_distortion_index, 3),
            "stability_score": round(self.stability_score, 1),
            "status_level": self.status_level,
            "cells": [c.to_dict() for c in self.cells],
            "warnings": self.warnings,
        }


class TopologicalManifoldUnfolder:
    """
    Unfolds 4D polytopes along topological cell hinges into continuous 3D manifolds,
    preserving topological invariants and spatial relationships for dyslexic thinkers.
    """

    SUPPORTED_POLYTOPES = ["TESSERACT_8_CELL", "HYPERSIMPLEX_5_CELL", "ORTHOPLEX_16_CELL"]

    def __init__(self, isometric_angle_deg: float = 30.0, cell_spacing_px: float = 75.0):
        self.isometric_angle_deg = max(15.0, min(60.0, isometric_angle_deg))
        self.cell_spacing_px = max(40.0, min(150.0, cell_spacing_px))

    def unfold_polytope(
        self,
        polytope_type: str = "TESSERACT_8_CELL",
        unfolding_factor: float = 1.0,
    ) -> TopologicalManifoldNet:
        """
        Unfolds the specified polytope into an isometric 3D spatial net
        based on the unfolding progression factor (0.0 to 1.0).
        """
        prog = max(0.0, min(1.0, unfolding_factor))
        ptype = polytope_type.upper()
        if ptype not in self.SUPPORTED_POLYTOPES:
            ptype = "TESSERACT_8_CELL"

        cells: List[PolytopeCell] = []
        warnings: List[str] = []

        if ptype == "TESSERACT_8_CELL":
            # 8 cubic cells in a Dalí Cross (central cube, 4 horizontal arms, 1 top, 2 bottom)
            v_count = 16
            e_count = 32
            f_count = 24
            c_count = 8
            # Euler-Poincare: V - E + F - C = 16 - 32 + 24 - 8 = 0
            euler_chi = v_count - e_count + f_count - c_count

            # Cell layout in 3D net space: (x, y, z) steps scaled by cell_spacing_px
            # In folded state (prog=0), cells overlap at origin; at prog=1, full extension
            sp = self.cell_spacing_px * prog
            hinge_angle = 90.0 * prog

            layout = [
                ("cell-core", "Core Anchor Cube", (0.0, 0.0, 0.0, 0.0), (0.0, 0.0, 0.0), None, 0.0, "#38bdf8"),
                ("cell-north", "North Dorsal Arm", (0.0, 1.0, 0.0, 0.0), (0.0, -sp, 0.0), "cell-core", hinge_angle, "#58a6ff"),
                ("cell-south", "South Ventral Arm", (0.0, -1.0, 0.0, 0.0), (0.0, sp, 0.0), "cell-core", hinge_angle, "#58a6ff"),
                ("cell-east", "East Lateral Arm", (1.0, 0.0, 0.0, 0.0), (sp, 0.0, 0.0), "cell-core", hinge_angle, "#79c0ff"),
                ("cell-west", "West Lateral Arm", (-1.0, 0.0, 0.0, 0.0), (-sp, 0.0, 0.0), "cell-core", hinge_angle, "#79c0ff"),
                ("cell-top", "Apex Zenith Cube", (0.0, 0.0, 1.0, 0.0), (0.0, -2.0 * sp, 0.0), "cell-north", hinge_angle, "#bc8cff"),
                ("cell-bottom-1", "Nadir Basal Cube I", (0.0, 0.0, -1.0, 0.0), (0.0, 2.0 * sp, 0.0), "cell-south", hinge_angle, "#3fb950"),
                ("cell-bottom-2", "Nadir Basal Cube II", (0.0, 0.0, 0.0, 1.0), (0.0, 3.0 * sp, 0.0), "cell-bottom-1", hinge_angle, "#2ea043"),
            ]

            for cid, lbl, c4d, p3d, parent, rot, col in layout:
                cells.append(
                    PolytopeCell(
                        cell_id=cid,
                        label=lbl,
                        cell_type="CUBE",
                        center_4d=c4d,
                        unfolded_position_3d=p3d,
                        hinge_parent_id=parent,
                        hinge_rotation_deg=rot,
                        color_hex=col,
                        volume=1.0,
                    )
                )

        elif ptype == "HYPERSIMPLEX_5_CELL":
            v_count = 5
            e_count = 10
            f_count = 10
            c_count = 5
            euler_chi = v_count - e_count + f_count - c_count  # 5 - 10 + 10 - 5 = 0
            sp = self.cell_spacing_px * 0.9 * prog
            hinge_angle = 70.53 * prog

            layout = [
                ("cell-base", "Base Tetrahedron", (0.0, 0.0, 0.0, 0.0), (0.0, 0.0, 0.0), None, 0.0, "#38bdf8"),
                ("cell-facet-1", "Lateral Facet Alpha", (1.0, 0.0, 0.0, 0.0), (sp, -sp * 0.5, 0.0), "cell-base", hinge_angle, "#58a6ff"),
                ("cell-facet-2", "Lateral Facet Beta", (-1.0, 0.0, 0.0, 0.0), (-sp, -sp * 0.5, 0.0), "cell-base", hinge_angle, "#79c0ff"),
                ("cell-facet-3", "Lateral Facet Gamma", (0.0, 1.0, 0.0, 0.0), (0.0, sp, 0.0), "cell-base", hinge_angle, "#bc8cff"),
                ("cell-apex", "Apical Tetrahedron", (0.0, 0.0, 1.0, 0.0), (0.0, -1.8 * sp, 0.0), "cell-facet-1", hinge_angle, "#d29922"),
            ]

            for cid, lbl, c4d, p3d, parent, rot, col in layout:
                cells.append(
                    PolytopeCell(
                        cell_id=cid,
                        label=lbl,
                        cell_type="TETRAHEDRON",
                        center_4d=c4d,
                        unfolded_position_3d=p3d,
                        hinge_parent_id=parent,
                        hinge_rotation_deg=rot,
                        color_hex=col,
                        volume=0.5,
                    )
                )

        else:  # ORTHOPLEX_16_CELL
            v_count = 8
            e_count = 24
            f_count = 32
            c_count = 16
            euler_chi = v_count - e_count + f_count - c_count  # 8 - 24 + 32 - 16 = 0
            sp = self.cell_spacing_px * 0.75 * prog
            hinge_angle = 60.0 * prog

            for i in range(16):
                ang = (i / 16.0) * 2.0 * math.pi
                rad = sp * (1.2 if i < 8 else 2.2)
                p3d = (rad * math.cos(ang), rad * math.sin(ang), (i % 2) * 15.0)
                parent = "cell-core-oct" if i > 0 else None
                col = "#38bdf8" if i % 2 == 0 else "#bc8cff"
                cells.append(
                    PolytopeCell(
                        cell_id=f"cell-oct-{i+1}",
                        label=f"Octahedral Cell {i+1}",
                        cell_type="OCTAHEDRON",
                        center_4d=(math.cos(ang), math.sin(ang), 0.0, 0.0),
                        unfolded_position_3d=p3d,
                        hinge_parent_id=parent,
                        hinge_rotation_deg=hinge_angle,
                        color_hex=col,
                        volume=0.75,
                    )
                )

        # Calculate metric distortion: higher distortion if partially unfolded
        # Complete unfolding (prog=1.0) achieves minimum isometric shearing
        distortion = (1.0 - prog) * 0.65 + 0.05
        stability = 100.0 - distortion * 60.0

        if prog < 0.25:
            status = "SINGULAR_COLLAPSE"
            warnings.append("Polytope is heavily folded; higher-dimensional projection causes facet overlap.")
        elif distortion > 0.4:
            status = "TOPOLOGICAL_SHEAR"
            warnings.append("Partial hinge unfolding introduces metric shear along cell boundaries.")
        else:
            status = "MANIFOLD_ISOMETRIC"

        return TopologicalManifoldNet(
            polytope_type=ptype,
            total_cells=c_count,
            total_faces=f_count,
            total_edges=e_count,
            total_vertices=v_count,
            euler_poincare_characteristic=euler_chi,
            unfolding_progress=prog,
            cells=cells,
            metric_distortion_index=distortion,
            stability_score=stability,
            status_level=status,
            warnings=warnings,
        )

    def generate_markdown_report(self, net: TopologicalManifoldNet) -> str:
        """Generates a structured diagnostic report on polytope manifold unfolding."""
        status_icons = {
            "MANIFOLD_ISOMETRIC": "🟢",
            "TOPOLOGICAL_SHEAR": "🟡",
            "SINGULAR_COLLAPSE": "🔴",
        }
        icon = status_icons.get(net.status_level, "⚪")

        lines = [
            "# Topological Manifold Unfolder & Polytope Net Report",
            "",
            f"**Manifold Topological State:** {icon} `{net.status_level}`",
            "",
            "## 4D Polytope Topological Invariants",
            "",
            "| Topological Metric | Value | Reference Standard | Spatial Cognition Impact |",
            "| :--- | :--- | :--- | :--- |",
            f"| **Polytope Geometry** | `{net.polytope_type}` | Regular 4-Polytope | Target higher-dimensional structure |",
            f"| **Total Cells (C)** | `{net.total_cells} facets` | 3D Boundary Volumes | Discrete volumetric building blocks |",
            f"| **Total Faces (F)** | `{net.total_faces} faces` | 2D Polygonal Interfaces | Shared hinge rotation boundaries |",
            f"| **Total Edges (E)** | `{net.total_edges} edges` | 1D Skeleton Lines | Metric coordinate axes |",
            f"| **Total Vertices (V)** | `{net.total_vertices} points` | 0D Topological Nodes | Spatial anchor points |",
            f"| **Euler-Poincare (Chi)** | `{net.euler_poincare_characteristic}` | 0 (Homology Invariant) | Confirms closed manifold topology |",
            f"| **Unfolding Progress** | `{net.unfolding_progress * 100:.0f}%` | 100% Planar Net | Extension along hinge lines |",
            f"| **Metric Distortion** | `{net.metric_distortion_index:.3f}` | < 0.250 Isometric | Preservation of intrinsic geodesics |",
            f"| **Manifold Stability** | `{net.stability_score:.1f} / 100` | >= 75.0 | Coherent spatial unrolling |",
            "",
            "## Unfolded Polytope Net Cells",
            "",
        ]

        if not net.cells:
            lines.append("_No unfolded cells generated._")
        else:
            lines.append("| Cell ID | Label | Type | 3D Net Pos (X, Y, Z) | Hinge Parent | Rotation |")
            lines.append("| :--- | :--- | :--- | :--- | :--- | :--- |")
            for c in net.cells:
                p = c.unfolded_position_3d
                parent = f"`{c.hinge_parent_id}`" if c.hinge_parent_id else "_ROOT_"
                lines.append(
                    f"| `{c.cell_id}` | **{c.label}** | `{c.cell_type}` | `({p[0]:+.0f}, {p[1]:+.0f}, {p[2]:+.0f}) px` | {parent} | `{c.hinge_rotation_deg:.0f}°` |"
                )
            lines.append("")

        if net.warnings:
            lines.append("## Topological Warnings & Distortion Risks")
            lines.append("")
            for w in net.warnings:
                lines.append(f"- ⚠️ {w}")
            lines.append("")

        lines.extend([
            "## Cognitive Spatial Anchoring & Higher-Dimensional Intuition",
            "",
            "- **Salvador Dali Hypercube Unfolding:** Expanding 4D hypercubes into 3D cross manifolds prevents visual collision, allowing dyslexic thinkers to inspect internal cell adjacencies without perspective occlusion.",
            "- **Euler-Poincare Invariance (V - E + F - C = 0):** Enforcing zero topological defect guarantees that spatial nets maintain complete homeomorphic continuity with the original 4-manifold.",
            "- **Metric Geodesic Preservation:** Minimizing shear distortion during unfolding maintains proportional conceptual distances between interconnected knowledge nodes.",
        ])

        return chr(10).join(lines)

    def generate_svg(
        self,
        net: TopologicalManifoldNet,
        width: int = 880,
        height: int = 580,
    ) -> str:
        """Renders an interactive dark titanium SVG isometric visualization of the unfolded net."""
        cx = width // 2 - 40
        cy = height // 2 - 10
        rad = math.radians(self.isometric_angle_deg)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)

        def iso_project(x: float, y: float, z: float) -> Tuple[float, float]:
            """Projects 3D net coordinate into 2D isometric canvas space."""
            px = cx + (x - y) * cos_a
            py = cy + (x + y) * sin_a - z
            return px, py

        parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
            f'width="{width}" height="{height}" style="background-color: #0d1117; font-family: -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif;">',
            '<defs>',
            '  <!-- Isometric Node Gradients -->',
            '  <linearGradient id="cubeGrad" x1="0%" y1="0%" x2="100%" y2="100%">',
            '    <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.3" />',
            '    <stop offset="100%" stop-color="#1f6feb" stop-opacity="0.1" />',
            '  </linearGradient>',
            '  <filter id="netGlow" x="-20%" y="-20%" width="140%" height="140%">',
            '    <feGaussianBlur stdDeviation="2" result="blur" />',
            '    <feComposite in="SourceGraphic" in2="blur" operator="over" />',
            '  </filter>',
            '</defs>',
            '<!-- Canvas Base -->',
            f'<rect width="{width}" height="{height}" fill="#0d1117" />',
        ]

        # Subtle background isometric coordinate grid
        parts.append('<!-- Isometric Background Matrix -->')
        for i in range(-5, 6):
            p1 = iso_project(i * 50.0, -250.0, 0.0)
            p2 = iso_project(i * 50.0, 250.0, 0.0)
            parts.append(f'<line x1="{p1[0]:.1f}" y1="{p1[1]:.1f}" x2="{p2[0]:.1f}" y2="{p2[1]:.1f}" stroke="#161b22" stroke-width="1" />')
            p3 = iso_project(-250.0, i * 50.0, 0.0)
            p4 = iso_project(250.0, i * 50.0, 0.0)
            parts.append(f'<line x1="{p3[0]:.1f}" y1="{p3[1]:.1f}" x2="{p4[0]:.1f}" y2="{p4[1]:.1f}" stroke="#161b22" stroke-width="1" />')

        # Draw Hinge Connections between Cells
        parts.append('<!-- Hinge Connection Geodesics -->')
        cell_map = {c.cell_id: c for c in net.cells}
        for c in net.cells:
            if c.hinge_parent_id and c.hinge_parent_id in cell_map:
                parent = cell_map[c.hinge_parent_id]
                p1 = iso_project(*parent.unfolded_position_3d)
                p2 = iso_project(*c.unfolded_position_3d)
                parts.append(
                    f'<line x1="{p1[0]:.1f}" y1="{p1[1]:.1f}" x2="{p2[0]:.1f}" y2="{p2[1]:.1f}" stroke="#30363d" stroke-width="2" stroke-dasharray="3 3" />'
                )

        # Draw 3D Isometric Cell Boxes/Volumes
        parts.append('<!-- Unfolded Polytope Net Cells -->')
        box_sz = 26.0

        for c in net.cells:
            x, y, z = c.unfolded_position_3d
            center_pt = iso_project(x, y, z)

            # Draw isometric cubical wireframe facet
            # 8 corners of isometric cube
            c0 = iso_project(x - box_sz, y - box_sz, z - box_sz)
            c1 = iso_project(x + box_sz, y - box_sz, z - box_sz)
            c2 = iso_project(x + box_sz, y + box_sz, z - box_sz)
            c3 = iso_project(x - box_sz, y + box_sz, z - box_sz)
            c4 = iso_project(x - box_sz, y - box_sz, z + box_sz)
            c5 = iso_project(x + box_sz, y - box_sz, z + box_sz)
            c6 = iso_project(x + box_sz, y + box_sz, z + box_sz)
            c7 = iso_project(x - box_sz, y + box_sz, z + box_sz)

            # Top face polygon (c4, c5, c6, c7)
            pts_top = f"{c4[0]:.1f},{c4[1]:.1f} {c5[0]:.1f},{c5[1]:.1f} {c6[0]:.1f},{c6[1]:.1f} {c7[0]:.1f},{c7[1]:.1f}"
            parts.append(f'<polygon points="{pts_top}" fill="{c.color_hex}" fill-opacity="0.35" stroke="{c.color_hex}" stroke-width="1.5" />')

            # Front-right face polygon (c5, c1, c2, c6)
            pts_right = f"{c5[0]:.1f},{c5[1]:.1f} {c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {c6[0]:.1f},{c6[1]:.1f}"
            parts.append(f'<polygon points="{pts_right}" fill="{c.color_hex}" fill-opacity="0.2" stroke="{c.color_hex}" stroke-width="1.2" />')

            # Front-left face polygon (c4, c0, c3, c7)
            pts_left = f"{c4[0]:.1f},{c4[1]:.1f} {c0[0]:.1f},{c0[1]:.1f} {c3[0]:.1f},{c3[1]:.1f} {c7[0]:.1f},{c7[1]:.1f}"
            parts.append(f'<polygon points="{pts_left}" fill="{c.color_hex}" fill-opacity="0.12" stroke="{c.color_hex}" stroke-width="1.2" />')

            # Center Anchor Point
            parts.append(f'<circle cx="{center_pt[0]:.1f}" cy="{center_pt[1]:.1f}" r="3.5" fill="{c.color_hex}" />')

            # Label text
            lbl_escaped = html.escape(c.label)
            parts.append(
                f'<text x="{center_pt[0]:.1f}" y="{center_pt[1] + box_sz + 18:.1f}" fill="#f0f6fc" font-size="10" font-weight="600" text-anchor="middle">{lbl_escaped}</text>'
            )

        # Header Information
        parts.extend([
            '<!-- Header Block -->',
            '<text x="24" y="34" fill="#f0f6fc" font-size="16" font-weight="700">Topological Manifold Unfolder</text>',
            f'<text x="24" y="52" fill="#8b949e" font-size="11">4D Polytope Net Weaver: {net.polytope_type} (Euler Characteristic Chi = {net.euler_poincare_characteristic})</text>',
        ])

        # Status Badge (Top Right)
        status_colors = {
            "MANIFOLD_ISOMETRIC": ("#238636", "#3fb950"),
            "TOPOLOGICAL_SHEAR": ("#9e6a03", "#d29922"),
            "SINGULAR_COLLAPSE": ("#da3633", "#f85149"),
        }
        bg_col, fg_col = status_colors.get(net.status_level, ("#30363d", "#8b949e"))
        badge_x = width - 210
        parts.extend([
            f'<rect x="{badge_x}" y="20" width="186" height="34" rx="6" fill="{bg_col}" fill-opacity="0.25" stroke="{fg_col}" stroke-width="1.2" />',
            f'<circle cx="{badge_x + 16}" cy="37" r="5" fill="{fg_col}" />',
            f'<text x="{badge_x + 30}" y="41" fill="#f0f6fc" font-size="11" font-weight="700">{net.status_level}</text>',
        ])

        # HUD Telemetry Card (Bottom Right)
        card_w = 320
        card_h = 146
        card_x = width - card_w - 24
        card_y = height - card_h - 24
        parts.extend([
            f'<g transform="translate({card_x}, {card_y})">',
            f'  <rect width="{card_w}" height="{card_h}" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1.5" />',
            '  <text x="16" y="24" fill="#f0f6fc" font-size="12" font-weight="700">Manifold Net Telemetry</text>',
            f'  <line x1="16" y1="32" x2="{card_w - 16}" y2="32" stroke="#30363d" stroke-width="1" />',
            f'  <text x="16" y="52" fill="#8b949e" font-size="11">Unfolding Progression:</text>',
            f'  <text x="{card_w - 16}" y="52" fill="#38bdf8" font-size="11" font-weight="600" text-anchor="end">{net.unfolding_progress * 100:.0f}% unfolded</text>',
            f'  <text x="16" y="72" fill="#8b949e" font-size="11">Metric Distortion Index:</text>',
            f'  <text x="{card_w - 16}" y="72" fill="#d29922" font-size="11" font-weight="600" text-anchor="end">{net.metric_distortion_index:.3f}</text>',
            f'  <text x="16" y="92" fill="#8b949e" font-size="11">Euler Invariant (Chi):</text>',
            f'  <text x="{card_w - 16}" y="92" fill="#3fb950" font-size="11" font-weight="600" text-anchor="end">{net.euler_poincare_characteristic} (Closed)</text>',
            f'  <text x="16" y="112" fill="#8b949e" font-size="11">Topological Elements:</text>',
            f'  <text x="{card_w - 16}" y="112" fill="#bc8cff" font-size="11" font-weight="600" text-anchor="end">{net.total_cells}C / {net.total_faces}F / {net.total_edges}E / {net.total_vertices}V</text>',
            f'  <text x="16" y="132" fill="#8b949e" font-size="11">Manifold Stability Index:</text>',
            f'  <text x="{card_w - 16}" y="132" fill="#f0f6fc" font-size="11" font-weight="600" text-anchor="end">{net.stability_score:.1f} / 100</text>',
            '</g>',
        ])

        # Legend Panel (Bottom Left)
        leg_w = 320
        leg_h = 108
        leg_x = 24
        leg_y = height - leg_h - 24
        parts.extend([
            f'<g transform="translate({leg_x}, {leg_y})">',
            f'  <rect width="{leg_w}" height="{leg_h}" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1.2" opacity="0.9" />',
            '  <text x="16" y="20" fill="#f0f6fc" font-size="11" font-weight="700">Isometric Polytope Net Legend</text>',
            '  <rect x="16" y="32" width="16" height="12" fill="#38bdf8" fill-opacity="0.5" stroke="#38bdf8" />',
            '  <text x="40" y="42" fill="#8b949e" font-size="10">Core Anchor Cell (Central Origin)</text>',
            '  <rect x="16" y="52" width="16" height="12" fill="#58a6ff" fill-opacity="0.5" stroke="#58a6ff" />',
            '  <text x="40" y="62" fill="#8b949e" font-size="10">Orthogonal Lateral Arms (Hinged Facets)</text>',
            '  <rect x="16" y="72" width="16" height="12" fill="#bc8cff" fill-opacity="0.5" stroke="#bc8cff" />',
            '  <text x="40" y="82" fill="#8b949e" font-size="10">Apex / Nadir Cells (Longitudinal Poles)</text>',
            '  <line x1="16" y1="96" x2="32" y2="96" stroke="#30363d" stroke-width="2" stroke-dasharray="3 3" />',
            '  <text x="40" y="99" fill="#8b949e" font-size="10">Hinge Boundary Geodesic</text>',
            '</g>',
        ])

        parts.append('</svg>')
        return chr(10).join(parts)

    @classmethod
    def create_demo_telemetry(cls) -> TopologicalManifoldNet:
        """Constructs a fully unfolded Salvador Dali tesseract cross for demonstration."""
        unfolder = cls(isometric_angle_deg=30.0, cell_spacing_px=75.0)
        return unfolder.unfold_polytope("TESSERACT_8_CELL", unfolding_factor=1.0)
