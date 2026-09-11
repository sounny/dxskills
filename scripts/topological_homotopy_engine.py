"""
topological_homotopy_engine.py - Autonomous Cognitive Spatial Topological Invariant & Homotopy Visualizer

Part of the DxSkills cognitive scaffolding suite (Phase 110, Cycle 106).
Grounded in Eide & Eide (2011) Dynamic Reasoning, Poincaré (1895) algebraic topology,
Hatcher (2002) homotopy deformation tracks, and Cowan (2001) bounded state transitions.

Strict constraint: Strictly zero em dashes (Unicode U+2014) anywhere.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


@dataclass
class TopologicalNode:
    """Relational node tracked across continuous deformation state spaces."""
    node_id: str
    label: str
    pos_start: Tuple[float, float]
    pos_end: Tuple[float, float]
    mass_weight: float = 1.0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class TopologicalEdge:
    """Structural invariant link between two topological entities."""
    source_id: str
    target_id: str
    relation_label: str = "CONNECTED"
    elastic_tension: float = 1.0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class TopologicalInvariants:
    """Deformation-invariant algebraic properties preserved under continuous homotopy."""
    betti_0: int  # Number of connected components
    betti_1: int  # 1-dimensional cycles or structural tunnels
    euler_characteristic: int  # V - E
    total_nodes: int
    total_edges: int
    is_homeomorphic: bool  # Preserves core topological invariants

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class HomotopyStep:
    """Discrete interpolation step along continuous deformation parameter t in [0, 1]."""
    t_value: float  # 0.0 to 1.0
    interpolated_positions: Dict[str, Tuple[float, float]]
    deformation_energy: float  # Integrated elastic strain
    visual_inertia_score: float  # Smoothness metric

    def to_dict(self) -> Dict[str, Any]:
        return {
            "t_value": self.t_value,
            "interpolated_positions": {k: list(v) for k, v in self.interpolated_positions.items()},
            "deformation_energy": self.deformation_energy,
            "visual_inertia_score": self.visual_inertia_score,
        }


@dataclass
class HomotopyTelemetry:
    """Cognitive telemetry measuring deformation smoothness, invariant preservation, and Cowan bounds."""
    nodes_count: int
    edges_count: int
    betti_0: int
    betti_1: int
    euler_characteristic: int
    structural_preservation_score: float  # 0.0 to 1.0
    mean_deformation_energy: float
    cowan_bounded: bool

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class HomotopyResult:
    """Master result bundle containing invariants, deformation steps, telemetry, and SVG visual assets."""
    source_invariants: TopologicalInvariants
    target_invariants: TopologicalInvariants
    homotopy_steps: List[HomotopyStep]
    telemetry: HomotopyTelemetry
    svg_homotopy_diagram: str
    invariant_audit_md: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "telemetry": self.telemetry.to_dict(),
            "source_invariants": self.source_invariants.to_dict(),
            "target_invariants": self.target_invariants.to_dict(),
            "homotopy_steps": [s.to_dict() for s in self.homotopy_steps],
            "svg_homotopy_diagram": self.svg_homotopy_diagram,
            "invariant_audit_md": self.invariant_audit_md,
        }


class TopologicalHomotopyEngine:
    """
    Autonomous Cognitive Spatial Topological Invariant & Homotopy Visualizer.

    Evaluates continuous topological invariants (Betti numbers, Euler characteristics)
    and synthesizes smooth homotopic path deformations across spatial state spaces.
    """

    def __init__(self, steps_count: int = 5, max_cowan_nodes: int = 6) -> None:
        self.steps_count = max(2, steps_count)
        self.max_cowan_nodes = max_cowan_nodes

    def evaluate_and_deform(
        self,
        nodes: List[Dict[str, Any]],
        edges: Optional[List[Dict[str, str]]] = None,
    ) -> HomotopyResult:
        """
        Task 110.1 & 110.2: Evaluates deformation-resistant structural invariants
        and computes smooth homotopic interpolation tracks between spatial states.
        """
        if not nodes:
            empty_inv = TopologicalInvariants(
                betti_0=0,
                betti_1=0,
                euler_characteristic=0,
                total_nodes=0,
                total_edges=0,
                is_homeomorphic=True,
            )
            empty_telemetry = HomotopyTelemetry(
                nodes_count=0,
                edges_count=0,
                betti_0=0,
                betti_1=0,
                euler_characteristic=0,
                structural_preservation_score=1.0,
                mean_deformation_energy=0.0,
                cowan_bounded=True,
            )
            return HomotopyResult(
                source_invariants=empty_inv,
                target_invariants=empty_inv,
                homotopy_steps=[],
                telemetry=empty_telemetry,
                svg_homotopy_diagram="",
                invariant_audit_md="",
            )

        # Parse nodes and coordinates
        parsed_nodes: List[TopologicalNode] = []
        for idx, item in enumerate(nodes):
            nid = str(item.get("id") or item.get("node_id") or f"tn_{idx+1}")
            lbl = str(item.get("label") or item.get("name") or f"Entity {idx+1}")
            start_x = float(item.get("start_x", 120.0 + (idx % 3) * 160.0))
            start_y = float(item.get("start_y", 120.0 + (idx // 3) * 140.0))
            end_x = float(item.get("end_x", 650.0 + (idx % 3) * 80.0))
            end_y = float(item.get("end_y", 120.0 + (idx // 3) * 140.0))
            mass = float(item.get("mass", 1.0))
            parsed_nodes.append(TopologicalNode(
                node_id=nid,
                label=lbl,
                pos_start=(start_x, start_y),
                pos_end=(end_x, end_y),
                mass_weight=mass,
            ))

        # Parse edges
        parsed_edges: List[TopologicalEdge] = []
        if edges:
            for e in edges:
                src = str(e.get("source") or e.get("source_id") or "")
                tgt = str(e.get("target") or e.get("target_id") or "")
                rel = str(e.get("relation") or "CONNECTED")
                if src and tgt:
                    parsed_edges.append(TopologicalEdge(source_id=src, target_id=tgt, relation_label=rel))

        # Compute Topological Invariants (Task 110.1)
        v = len(parsed_nodes)
        e = len(parsed_edges)

        # Graph connected components (Betti 0)
        adj: Dict[str, Set[str]] = {n.node_id: set() for n in parsed_nodes}
        for edge in parsed_edges:
            if edge.source_id in adj and edge.target_id in adj:
                adj[edge.source_id].add(edge.target_id)
                adj[edge.target_id].add(edge.source_id)

        visited: Set[str] = set()
        betti_0 = 0
        for n in parsed_nodes:
            if n.node_id not in visited:
                betti_0 += 1
                q = [n.node_id]
                visited.add(n.node_id)
                while q:
                    curr = q.pop(0)
                    for neighbor in adj.get(curr, set()):
                        if neighbor not in visited:
                            visited.add(neighbor)
                            q.append(neighbor)

        # Betti 1: Cyclomatic complexity b1 = E - V + b0
        betti_1 = max(0, e - v + betti_0)
        euler_char = v - e

        invariants = TopologicalInvariants(
            betti_0=betti_0,
            betti_1=betti_1,
            euler_characteristic=euler_char,
            total_nodes=v,
            total_edges=e,
            is_homeomorphic=True,  # Continuity preserves homotopy equivalence
        )

        # Compute Homotopic Path Deformation (Task 110.2)
        # Smooth cubic Hermite / ease-in-out S-curve interpolation
        steps: List[HomotopyStep] = []
        node_lookup = {n.node_id: n for n in parsed_nodes}

        for s_idx in range(self.steps_count):
            t_linear = s_idx / max(1, self.steps_count - 1)
            # Smoothstep curve: 3t^2 - 2t^3
            t_smooth = (3.0 * (t_linear ** 2)) - (2.0 * (t_linear ** 3))

            interp_pos: Dict[str, Tuple[float, float]] = {}
            step_strain = 0.0

            for n in parsed_nodes:
                ix = round(n.pos_start[0] + (n.pos_end[0] - n.pos_start[0]) * t_smooth, 2)
                iy = round(n.pos_start[1] + (n.pos_end[1] - n.pos_start[1]) * t_smooth, 2)
                interp_pos[n.node_id] = (ix, iy)

            # Calculate elastic deformation strain across edges
            for edge in parsed_edges:
                if edge.source_id in interp_pos and edge.target_id in interp_pos:
                    p1 = interp_pos[edge.source_id]
                    p2 = interp_pos[edge.target_id]
                    d_cur = math.hypot(p1[0] - p2[0], p1[1] - p2[1])

                    # Reference start distance
                    n1 = node_lookup[edge.source_id]
                    n2 = node_lookup[edge.target_id]
                    d_ref = math.hypot(n1.pos_start[0] - n2.pos_start[0], n1.pos_start[1] - n2.pos_start[1])
                    strain = abs(d_cur - d_ref) * 0.05
                    step_strain += strain

            inertia = round(1.0 - (0.2 * abs(t_smooth - 0.5)), 3)

            steps.append(HomotopyStep(
                t_value=round(t_linear, 2),
                interpolated_positions=interp_pos,
                deformation_energy=round(step_strain, 2),
                visual_inertia_score=inertia,
            ))

        mean_energy = round(sum(s.deformation_energy for s in steps) / max(1, len(steps)), 2)
        preservation_score = 1.0 if invariants.is_homeomorphic else 0.50
        cowan_bounded = v <= self.max_cowan_nodes

        telemetry = HomotopyTelemetry(
            nodes_count=v,
            edges_count=e,
            betti_0=betti_0,
            betti_1=betti_1,
            euler_characteristic=euler_char,
            structural_preservation_score=preservation_score,
            mean_deformation_energy=mean_energy,
            cowan_bounded=cowan_bounded,
        )

        # Build Invariant Audit Markdown
        md_lines = [
            "# Topological Invariant & Homotopy Audit Report",
            "",
            f"**Total Entities:** {telemetry.nodes_count} Nodes | {telemetry.edges_count} Invariant Edges",
            f"**Connected Components (Betti 0):** {telemetry.betti_0} | **Cyclic Holes (Betti 1):** {telemetry.betti_1}",
            f"**Euler Characteristic:** {telemetry.euler_characteristic} | **Preservation Score:** {telemetry.structural_preservation_score * 100:.0f}%",
            f"**Cowan Bounded (V<=6):** {'Yes [OPTIMAL]' if telemetry.cowan_bounded else 'No [HIGH COMPLEXITY]'}",
            "",
            "## Homotopic Deformation Keyframes",
            "",
            "| Keyframe (t) | Visual Inertia | Deformation Energy | Invariants Preserved |",
            "| :--- | :--- | :--- | :--- |",
        ]
        for s in steps:
            md_lines.append(
                f"| `t = {s.t_value:.2f}` | {s.visual_inertia_score:.3f} | {s.deformation_energy:.2f} J | [PRESERVED] |"
            )

        md_lines.append("")
        md_lines.append("## Deformation-Resistant Entity Coordinates")
        md_lines.append("")
        for n in parsed_nodes:
            md_lines.append(
                f"- **{n.label} (`{n.node_id}`):** Start: {n.pos_start} -> End: {n.pos_end}"
            )

        audit_md = "\n".join(md_lines)

        svg_diagram = self._render_homotopy_svg(
            nodes=parsed_nodes,
            edges=parsed_edges,
            steps=steps,
            telemetry=telemetry,
        )

        return HomotopyResult(
            source_invariants=invariants,
            target_invariants=invariants,
            homotopy_steps=steps,
            telemetry=telemetry,
            svg_homotopy_diagram=svg_diagram,
            invariant_audit_md=audit_md,
        )

    def _render_homotopy_svg(
        self,
        nodes: List[TopologicalNode],
        edges: List[TopologicalEdge],
        steps: List[HomotopyStep],
        telemetry: HomotopyTelemetry,
    ) -> str:
        """Renders dark titanium homotopy continuous deformation paths and vector tracks."""
        w, h = 920, 520
        t = telemetry

        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">',
            '  <defs>',
            '    <linearGradient id="homoBg" x1="0%" y1="0%" x2="100%" y2="100%">',
            '      <stop offset="0%" stop-color="#080c14"/>',
            '      <stop offset="100%" stop-color="#0f172a"/>',
            '    </linearGradient>',
            '    <linearGradient id="streamGrad" x1="0%" y1="0%" x2="100%" y2="0%">',
            '      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.8"/>',
            '      <stop offset="100%" stop-color="#10b981" stop-opacity="0.8"/>',
            '    </linearGradient>',
            '  </defs>',
            '  <rect width="100%" height="100%" fill="url(#homoBg)"/>',
            '  <!-- Header -->',
            '  <text x="40" y="44" font-family="system-ui, -apple-system, sans-serif" font-size="18" font-weight="700" fill="#f8fafc">Topological Invariant &amp; Homotopy Visualizer</text>',
            f'  <text x="40" y="68" font-family="system-ui, -apple-system, sans-serif" font-size="12" fill="#94a3b8">Poincar&eacute; Algebraic Topology &bull; &beta;0: {t.betti_0} &bull; &beta;1: {t.betti_1} &bull; Euler &chi;: {t.euler_characteristic} &bull; Preservation: {t.structural_preservation_score * 100:.0f}%</text>',
            '  <!-- Main Canvas -->',
            '  <g transform="translate(40, 95)">',
            '    <rect x="0" y="0" width="840" height="270" rx="12" fill="#0b1120" stroke="#1e293b" stroke-width="1.5"/>',
            '    <!-- Grid Markings -->',
            '    <line x1="280" y1="0" x2="280" y2="270" stroke="#1e293b" stroke-width="1" stroke-dasharray="3,3"/>',
            '    <line x1="560" y1="0" x2="560" y2="270" stroke="#1e293b" stroke-width="1" stroke-dasharray="3,3"/>',
            '    <text x="140" y="24" font-family="monospace" font-size="10" fill="#64748b" text-anchor="middle">INITIAL STATE (t=0.0)</text>',
            '    <text x="420" y="24" font-family="monospace" font-size="10" fill="#38bdf8" text-anchor="middle">HOMOTOPIC DEFORMATION</text>',
            '    <text x="700" y="24" font-family="monospace" font-size="10" fill="#10b981" text-anchor="middle">TERMINAL STATE (t=1.0)</text>',
        ]

        # Draw Node Deformation Tracks (Vector Streaks)
        for n in nodes[:5]:
            p_start = n.pos_start
            p_end = n.pos_end
            # Continuous Bezier streamline connecting start and end
            mid_x = (p_start[0] + p_end[0]) / 2.0
            svg_parts.extend([
                f'    <!-- Streamline for {n.node_id} -->',
                f'    <path d="M {p_start[0]} {p_start[1]} Q {mid_x} {p_start[1] - 40}, {p_end[0]} {p_end[1]}" fill="none" stroke="url(#streamGrad)" stroke-width="2" stroke-dasharray="4,4"/>',
                f'    <!-- Start Node {n.node_id} -->',
                f'    <circle cx="{p_start[0]}" cy="{p_start[1]}" r="8" fill="#0284c7" stroke="#38bdf8" stroke-width="2"/>',
                f'    <text x="{p_start[0]}" y="{p_start[1] + 20}" font-family="system-ui, -apple-system, sans-serif" font-size="9" fill="#94a3b8" text-anchor="middle">{n.label}</text>',
                f'    <!-- End Node {n.node_id} -->',
                f'    <circle cx="{p_end[0]}" cy="{p_end[1]}" r="8" fill="#059669" stroke="#10b981" stroke-width="2"/>',
                f'    <text x="{p_end[0]}" y="{p_end[1] + 20}" font-family="system-ui, -apple-system, sans-serif" font-size="9" fill="#94a3b8" text-anchor="middle">{n.label}</text>',
            ])

        # Draw intermediate positions from middle step
        if len(steps) >= 3:
            mid_step = steps[len(steps) // 2]
            for nid, pos in mid_step.interpolated_positions.items():
                svg_parts.append(
                    f'    <circle cx="{pos[0]}" cy="{pos[1]}" r="4" fill="#a855f7" opacity="0.7"/>'
                )

        svg_parts.append('  </g>')

        # Bottom Cards: Telemetry
        svg_parts.extend([
            '  <!-- Bottom Cards: Telemetry Badges -->',
            '  <g transform="translate(40, 390)">',
            '    <rect x="0" y="0" width="260" height="85" rx="10" fill="#0b1120" stroke="#1e293b" stroke-width="1.5"/>',
            '    <text x="20" y="26" font-family="system-ui, -apple-system, sans-serif" font-size="11" fill="#94a3b8">Algebraic Topology Invariants</text>',
            f'    <text x="20" y="56" font-family="system-ui, -apple-system, sans-serif" font-size="24" font-weight="800" fill="#10b981">&beta;0={t.betti_0} | &beta;1={t.betti_1}</text>',
            f'    <text x="20" y="74" font-family="system-ui, -apple-system, sans-serif" font-size="10" fill="#64748b">Euler characteristic: {t.euler_characteristic}</text>',
            '    <rect x="290" y="0" width="260" height="85" rx="10" fill="#0b1120" stroke="#1e293b" stroke-width="1.5"/>',
            '    <text x="310" y="26" font-family="system-ui, -apple-system, sans-serif" font-size="11" fill="#94a3b8">Homeomorphic Preservation</text>',
            f'    <text x="310" y="56" font-family="system-ui, -apple-system, sans-serif" font-size="24" font-weight="800" fill="#38bdf8">{t.structural_preservation_score * 100:.0f}%</text>',
            f'    <text x="310" y="74" font-family="system-ui, -apple-system, sans-serif" font-size="10" fill="#64748b">{len(steps)} continuous keyframes interpolated</text>',
            '    <rect x="580" y="0" width="260" height="85" rx="10" fill="#0b1120" stroke="#1e293b" stroke-width="1.5"/>',
            '    <text x="600" y="26" font-family="system-ui, -apple-system, sans-serif" font-size="11" fill="#94a3b8">Mean Deformation Strain</text>',
            f'    <text x="600" y="56" font-family="system-ui, -apple-system, sans-serif" font-size="24" font-weight="800" fill="#a855f7">{t.mean_deformation_energy:.2f} J</text>',
            f'    <text x="600" y="74" font-family="system-ui, -apple-system, sans-serif" font-size="10" fill="#64748b">Cowan bounded: {t.cowan_bounded}</text>',
            '  </g>',
            '</svg>',
        ])

        return "\n".join(svg_parts)

    def export_svg(self, result: HomotopyResult, output_path: Optional[str] = None) -> str:
        """Exports SVG diagram to file or returns XML string."""
        if output_path:
            p = Path(output_path)
            p.parent.mkdir(parents=True, exist_ok=True)
            with open(p, "w", encoding="utf-8") as f:
                f.write(result.svg_homotopy_diagram)
        return result.svg_homotopy_diagram

    def generate_ascii_report(self, result: HomotopyResult) -> str:
        """Generates terminal ASCII summary table of topological invariant and deformation metrics."""
        t = result.telemetry
        lines = [
            "================================================================================",
            "   TOPOLOGICAL INVARIANT & HOMOTOPY VISUALIZER (PHASE 110 / CYCLE 106)",
            "================================================================================",
            f" Entities Evaluated    : {t.nodes_count} nodes | {t.edges_count} structural edges",
            f" Connected (Betti 0)   : {t.betti_0} components",
            f" Cycles (Betti 1)      : {t.betti_1} topological 1D holes/tunnels",
            f" Euler Characteristic  : {t.euler_characteristic} (V - E)",
            f" Invariant Fidelity    : {t.structural_preservation_score * 100:.0f}% continuous preservation",
            f" Mean Strain Energy    : {t.mean_deformation_energy:.2f} J",
            f" Cowan Bounded (V<=6)  : {'Yes [OPTIMAL]' if t.cowan_bounded else 'No [EXCEEDS CAPACITY]'}",
            "--------------------------------------------------------------------------------",
            " HOMOTOPIC DEFORMATION KEYFRAME TRACKS",
            "--------------------------------------------------------------------------------",
        ]

        if not result.homotopy_steps:
            lines.append(" (No homotopy deformation steps computed; empty input)")
        else:
            for s in result.homotopy_steps:
                lines.append(f" [KEYFRAME] t = {s.t_value:.2f} | Inertia: {s.visual_inertia_score:.3f} | Strain: {s.deformation_energy:.2f} J")

        lines.append("================================================================================")
        return "\n".join(lines)
