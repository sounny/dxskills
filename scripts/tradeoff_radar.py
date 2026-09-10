#!/usr/bin/env python3
"""
Autonomous Cognitive Multi-Perspective Architectural Trade-Off Radar & Pareto Frontier
Part of the DxSkills Cognitive Architecture Suite (https://dxskills.sounny.com)

Evaluates candidate architectural solutions across orthogonal design axes, computes
Pareto-optimal non-dominated frontiers, visualizes trade-off geometries via SVG
spider radar charts, and exports Obsidian .canvas decision spaces.

Core Principles:
- Multi-Objective Pareto Optimization: Isolates optimal architectures without arbitrary scalar weighting.
- Spatial Cognitive Contrast: Maps multi-dimensional trade-offs onto polar spider radar meshes.
- Non-Linear Architectural Reasoning: Visualizes tensions between speed, cognitive load, cost, and resilience.
- Zero Jargon Friction: Translates mathematical dominance into intuitive spatial decisions.
"""

import os
import re
import json
import math
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple, Set


DEFAULT_AXES = [
    "cognitive_simplicity",
    "throughput_speed",
    "maintainability",
    "fault_resilience",
    "developer_ergonomics"
]

AXIS_DISPLAY_NAMES = {
    "cognitive_simplicity": "Cognitive Simplicity",
    "throughput_speed": "Throughput & Speed",
    "maintainability": "Maintainability",
    "fault_resilience": "Fault Resilience",
    "developer_ergonomics": "Developer Ergonomics",
    "cost_efficiency": "Cost Efficiency",
    "observability": "Observability",
    "scalability": "Scalability"
}

PALETTE = [
    {"stroke": "#10b981", "fill": "rgba(16, 185, 129, 0.22)", "name": "Emerald"},
    {"stroke": "#38bdf8", "fill": "rgba(56, 189, 248, 0.22)", "name": "Sky"},
    {"stroke": "#a855f7", "fill": "rgba(168, 85, 247, 0.22)", "name": "Purple"},
    {"stroke": "#f59e0b", "fill": "rgba(245, 158, 11, 0.22)", "name": "Amber"},
    {"stroke": "#ec4899", "fill": "rgba(236, 72, 153, 0.22)", "name": "Rose"},
    {"stroke": "#06b6d4", "fill": "rgba(6, 182, 212, 0.22)", "name": "Cyan"},
]


@dataclass
class ArchitectureCandidate:
    """A proposed architectural design or technical decision candidate."""
    candidate_id: str
    name: str
    description: str
    scores: Dict[str, float]  # 0.0 to 1.0 per axis (higher is better)
    tags: List[str] = field(default_factory=list)
    is_pareto_optimal: bool = False
    dominated_by: List[str] = field(default_factory=list)
    dominates: List[str] = field(default_factory=list)

    def get_score(self, axis: str) -> float:
        """Return score bounded between 0.0 and 1.0."""
        val = self.scores.get(axis, 0.0)
        return max(0.0, min(1.0, float(val)))


@dataclass
class TradeoffAnalysis:
    """Synthesis telemetry describing the Pareto frontier and architectural tensions."""
    candidates: List[ArchitectureCandidate]
    axes: List[str]
    axis_labels: Dict[str, str]
    pareto_frontier_ids: List[str]
    dominated_ids: List[str]
    tradeoff_tensions: List[Dict[str, Any]]
    archetype_recommendations: Dict[str, str]


class ArchitecturalTradeoffRadar:
    """Evaluates multi-perspective architectural candidates and generates trade-off radars."""

    def __init__(self, axes: Optional[List[str]] = None):
        self.axes: List[str] = axes if axes else list(DEFAULT_AXES)
        self.axis_labels: Dict[str, str] = {
            ax: AXIS_DISPLAY_NAMES.get(ax, ax.replace("_", " ").title())
            for ax in self.axes
        }
        self.candidates: Dict[str, ArchitectureCandidate] = {}
        self._next_idx = 1

    def define_axes(self, axes: List[str], labels: Optional[Dict[str, str]] = None) -> None:
        """Set or update evaluation axes and their display labels."""
        if not axes:
            raise ValueError("Must provide at least one evaluation axis.")
        self.axes = list(axes)
        self.axis_labels = {}
        for ax in self.axes:
            if labels and ax in labels:
                self.axis_labels[ax] = labels[ax]
            else:
                self.axis_labels[ax] = AXIS_DISPLAY_NAMES.get(ax, ax.replace("_", " ").title())

    def add_candidate(
        self,
        name: str,
        scores: Dict[str, float],
        description: str = "",
        candidate_id: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> ArchitectureCandidate:
        """Register an architectural candidate solution."""
        cid = candidate_id or f"arch-{self._next_idx}"
        self._next_idx += 1

        normalized_scores = {}
        for ax in self.axes:
            val = scores.get(ax, 0.0)
            normalized_scores[ax] = max(0.0, min(1.0, float(val)))

        candidate = ArchitectureCandidate(
            candidate_id=cid,
            name=name.strip(),
            description=description.strip(),
            scores=normalized_scores,
            tags=list(tags) if tags else []
        )
        self.candidates[cid] = candidate
        return candidate

    def check_dominance(self, a: ArchitectureCandidate, b: ArchitectureCandidate) -> bool:
        """
        Check if candidate A dominates candidate B.
        A dominates B iff A >= B on all axes and A > B on at least one axis.
        """
        strictly_better_in_any = False
        for ax in self.axes:
            score_a = a.get_score(ax)
            score_b = b.get_score(ax)
            if score_a < score_b:
                return False
            if score_a > score_b:
                strictly_better_in_any = True
        return strictly_better_in_any

    def evaluate_pareto(self) -> TradeoffAnalysis:
        """
        Compute Pareto-optimal non-dominated frontier and identify architectural tensions.
        """
        all_candidates = list(self.candidates.values())

        # Reset dominance relations
        for cand in all_candidates:
            cand.is_pareto_optimal = True
            cand.dominated_by = []
            cand.dominates = []

        # Pairwise comparison
        for i, cand_a in enumerate(all_candidates):
            for j, cand_b in enumerate(all_candidates):
                if i == j:
                    continue
                if self.check_dominance(cand_a, cand_b):
                    cand_a.dominates.append(cand_b.candidate_id)
                    cand_b.dominated_by.append(cand_a.candidate_id)
                    cand_b.is_pareto_optimal = False

        pareto_ids = [c.candidate_id for c in all_candidates if c.is_pareto_optimal]
        dominated_ids = [c.candidate_id for c in all_candidates if not c.is_pareto_optimal]

        # Calculate trade-off tensions (negative correlation between pairs of axes)
        tensions = self._detect_tradeoff_tensions()

        # Best picks per axis
        archetype_recs = {}
        for ax in self.axes:
            best_cand = max(all_candidates, key=lambda c: c.get_score(ax), default=None)
            if best_cand:
                archetype_recs[ax] = best_cand.candidate_id

        return TradeoffAnalysis(
            candidates=all_candidates,
            axes=self.axes,
            axis_labels=self.axis_labels,
            pareto_frontier_ids=pareto_ids,
            dominated_ids=dominated_ids,
            tradeoff_tensions=tensions,
            archetype_recommendations=archetype_recs
        )

    def _detect_tradeoff_tensions(self) -> List[Dict[str, Any]]:
        """Identify axes pairs that exhibit inverse relationship across candidates."""
        candidates = list(self.candidates.values())
        if len(candidates) < 2 or len(self.axes) < 2:
            return []

        tensions = []
        n_axes = len(self.axes)
        for i in range(n_axes):
            for j in range(i + 1, n_axes):
                ax1 = self.axes[i]
                ax2 = self.axes[j]
                vals1 = [c.get_score(ax1) for c in candidates]
                vals2 = [c.get_score(ax2) for c in candidates]

                # Compute Pearson correlation
                mean1 = sum(vals1) / len(vals1)
                mean2 = sum(vals2) / len(vals2)
                var1 = sum((v - mean1) ** 2 for v in vals1)
                var2 = sum((v - mean2) ** 2 for v in vals2)

                if var1 > 1e-9 and var2 > 1e-9:
                    cov = sum((v1 - mean1) * (v2 - mean2) for v1, v2 in zip(vals1, vals2))
                    corr = cov / math.sqrt(var1 * var2)
                else:
                    corr = 0.0

                if corr < -0.2:  # Distinct inverse tension
                    tensions.append({
                        "axis_1": ax1,
                        "axis_2": ax2,
                        "label_1": self.axis_labels.get(ax1, ax1),
                        "label_2": self.axis_labels.get(ax2, ax2),
                        "tension_score": round(abs(corr), 3),
                        "description": f"Strong inverse trade-off between {self.axis_labels.get(ax1, ax1)} and {self.axis_labels.get(ax2, ax2)}."
                    })

        tensions.sort(key=lambda x: x["tension_score"], reverse=True)
        return tensions

    def export_radar_svg(self, width: int = 740, height: int = 540) -> str:
        """
        Generate a multi-polygon spider radar chart SVG.
        Pareto-optimal candidates are emphasized with solid glowing strokes.
        Dominated candidates use subtle dashed lines to eliminate visual clutter.
        """
        analysis = self.evaluate_pareto()
        cx = width * 0.38
        cy = height * 0.50
        max_r = min(width * 0.32, height * 0.38)
        num_axes = len(self.axes)

        if num_axes < 3:
            # Fallback if too few axes
            angles = [i * (2 * math.pi / max(1, num_axes)) - math.pi / 2 for i in range(num_axes)]
        else:
            angles = [i * (2 * math.pi / num_axes) - math.pi / 2 for i in range(num_axes)]

        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
            f'width="{width}" height="{height}" style="background-color: #0f172a; '
            f'font-family: -apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, sans-serif;">',
            '<defs>',
            '  <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">',
            '    <feGaussianBlur stdDeviation="3" result="blur" />',
            '    <feMerge><feMergeNode in="blur" /><feMergeNode in="SourceGraphic" /></feMerge>',
            '  </filter>',
            '</defs>',
            '<!-- Header Title -->',
            f'<text x="24" y="32" fill="#f8fafc" font-size="16" font-weight="700">Architectural Trade-Off Radar &amp; Pareto Frontier</text>',
            f'<text x="24" y="50" fill="#94a3b8" font-size="12">Non-dominated Pareto candidates highlighted with radiant contours</text>',
            '<!-- Concentric Reference Rings -->',
        ]

        # Draw grid rings (25%, 50%, 75%, 100%)
        rings = [0.25, 0.50, 0.75, 1.00]
        for ring in rings:
            r = max_r * ring
            if num_axes >= 3:
                pts = []
                for ang in angles:
                    px = cx + r * math.cos(ang)
                    py = cy + r * math.sin(ang)
                    pts.append(f"{px:.1f},{py:.1f}")
                polygon_str = " ".join(pts)
                svg_parts.append(
                    f'<polygon points="{polygon_str}" fill="none" stroke="#334155" '
                    f'stroke-width="1" stroke-dasharray="3,3" opacity="0.6"/>'
                )
            else:
                svg_parts.append(
                    f'<circle cx="{cx}" cy="{cy}" r="{r:.1f}" fill="none" stroke="#334155" '
                    f'stroke-width="1" stroke-dasharray="3,3" opacity="0.6"/>'
                )
            # Add percentage label along vertical axis
            svg_parts.append(
                f'<text x="{cx + 6:.1f}" y="{cy - r + 4:.1f}" fill="#64748b" font-size="10">{int(ring * 100)}%</text>'
            )

        # Draw Radial Axis Spokes and Labels
        svg_parts.append('<!-- Radial Spokes & Labels -->')
        for idx, (axis_key, ang) in enumerate(zip(self.axes, angles)):
            ax_x = cx + max_r * math.cos(ang)
            ax_y = cy + max_r * math.sin(ang)
            svg_parts.append(
                f'<line x1="{cx}" y1="{cy}" x2="{ax_x:.1f}" y2="{ax_y:.1f}" '
                f'stroke="#475569" stroke-width="1.2" opacity="0.7"/>'
            )

            # Label positioning offset
            label_offset = 20
            lbl_x = cx + (max_r + label_offset) * math.cos(ang)
            lbl_y = cy + (max_r + label_offset) * math.sin(ang)

            text_anchor = "middle"
            if math.cos(ang) > 0.3:
                text_anchor = "start"
            elif math.cos(ang) < -0.3:
                text_anchor = "end"

            disp_label = self.axis_labels.get(axis_key, axis_key).replace("&", "&amp;")
            svg_parts.append(
                f'<text x="{lbl_x:.1f}" y="{lbl_y + 4:.1f}" fill="#cbd5e1" '
                f'font-size="11" font-weight="600" text-anchor="{text_anchor}">{disp_label}</text>'
            )

        # Draw Candidate Polygons (Dominated first, Pareto-optimal on top)
        svg_parts.append('<!-- Candidate Radar Profiles -->')
        ordered_candidates = sorted(
            analysis.candidates,
            key=lambda c: 1 if c.is_pareto_optimal else 0
        )

        for c_idx, candidate in enumerate(ordered_candidates):
            color = PALETTE[c_idx % len(PALETTE)]
            is_pareto = candidate.is_pareto_optimal

            coords = []
            for ax, ang in zip(self.axes, angles):
                score = candidate.get_score(ax)
                r_cand = max_r * score
                px = cx + r_cand * math.cos(ang)
                py = cy + r_cand * math.sin(ang)
                coords.append((px, py))

            pts_str = " ".join([f"{p[0]:.1f},{p[1]:.1f}" for p in coords])

            stroke_width = "2.8" if is_pareto else "1.2"
            dash_array = "none" if is_pareto else "4,4"
            opacity = "1.0" if is_pareto else "0.45"
            fill_style = color["fill"] if is_pareto else "rgba(100, 116, 139, 0.08)"
            glow_filter = ' filter="url(#glow)"' if is_pareto else ""

            svg_parts.append(
                f'<polygon points="{pts_str}" fill="{fill_style}" stroke="{color["stroke"]}" '
                f'stroke-width="{stroke_width}" stroke-dasharray="{dash_array}" '
                f'opacity="{opacity}"{glow_filter}/>'
            )

            # Draw vertices
            for px, py in coords:
                v_rad = "4" if is_pareto else "2.5"
                svg_parts.append(
                    f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{v_rad}" '
                    f'fill="{color["stroke"]}" opacity="{opacity}"/>'
                )

        # Draw Right Legend & Pareto Summary
        leg_x = width * 0.72
        leg_y = 65
        svg_parts.append('<!-- Interactive Legend -->')
        svg_parts.append(f'<rect x="{leg_x - 12}" y="{leg_y - 12}" width="{width - leg_x - 12}" height="{height - 80}" rx="8" fill="#1e293b" stroke="#334155" stroke-width="1"/>')
        svg_parts.append(f'<text x="{leg_x}" y="{leg_y + 8}" fill="#f8fafc" font-size="13" font-weight="700">Candidates &amp; Pareto Status</text>')

        cur_y = leg_y + 32
        for c_idx, candidate in enumerate(ordered_candidates):
            color = PALETTE[c_idx % len(PALETTE)]
            is_pareto = candidate.is_pareto_optimal
            status_text = "[PARETO]" if is_pareto else "[Dominated]"
            status_color = "#34d399" if is_pareto else "#94a3b8"

            svg_parts.append(
                f'<rect x="{leg_x}" y="{cur_y - 9}" width="14" height="14" rx="3" fill="{color["stroke"]}"/>'
            )
            svg_parts.append(
                f'<text x="{leg_x + 22}" y="{cur_y + 2}" fill="#f1f5f9" font-size="11" font-weight="600">{candidate.name}</text>'
            )
            svg_parts.append(
                f'<text x="{leg_x + 22}" y="{cur_y + 16}" fill="{status_color}" font-size="9.5" font-weight="500">{status_text}</text>'
            )
            cur_y += 34

        # Pareto summary badge at bottom
        svg_parts.append(f'<line x1="{leg_x}" y1="{cur_y}" x2="{width - 24}" y2="{cur_y}" stroke="#334155" stroke-width="1"/>')
        cur_y += 18
        svg_parts.append(
            f'<text x="{leg_x}" y="{cur_y}" fill="#94a3b8" font-size="10.5">'
            f'Frontier Count: <tspan fill="#34d399" font-weight="700">{len(analysis.pareto_frontier_ids)}</tspan> / {len(analysis.candidates)}'
            f'</text>'
        )

        svg_parts.append('</svg>')
        return "\n".join(svg_parts)

    def export_pareto_canvas(
        self,
        primary_x_axis: Optional[str] = None,
        primary_y_axis: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate an Obsidian .canvas structure mapping candidates onto a 2D trade-off canvas.
        Green cards denote Pareto-optimal candidates; red cards represent dominated options.
        Dominance relationship edges indicate strictly superior alternatives.
        """
        analysis = self.evaluate_pareto()
        x_ax = primary_x_axis if (primary_x_axis and primary_x_axis in self.axes) else self.axes[0]
        y_ax = primary_y_axis if (primary_y_axis and primary_y_axis in self.axes) else (
            self.axes[1] if len(self.axes) > 1 else self.axes[0]
        )

        x_label = self.axis_labels.get(x_ax, x_ax)
        y_label = self.axis_labels.get(y_ax, y_ax)

        canvas_nodes = []
        canvas_edges = []

        # Coordinate space: 0 to 1 mapped to 100 to 900
        min_canvas = 100
        span_canvas = 800

        # Create candidate cards
        for cand in analysis.candidates:
            score_x = cand.get_score(x_ax)
            score_y = cand.get_score(y_ax)

            pos_x = int(min_canvas + score_x * span_canvas)
            # Invert Y so high score is visually higher on the canvas
            pos_y = int(min_canvas + (1.0 - score_y) * span_canvas)

            card_color = "4" if cand.is_pareto_optimal else "1"  # 4 = Green, 1 = Red/Muted

            scores_summary = " | ".join(
                f"{self.axis_labels.get(a, a)[:8]}: {cand.get_score(a):.2f}"
                for a in self.axes
            )

            status_header = "**PARETO-OPTIMAL FRONTIER**" if cand.is_pareto_optimal else "*Dominated Candidate*"
            text_body = (
                f"### {cand.name}\n"
                f"{status_header}\n\n"
                f"{cand.description}\n\n"
                f"**Metrics:** {scores_summary}\n\n"
                f"- **{x_label}:** {score_x:.2f}\n"
                f"- **{y_label}:** {score_y:.2f}"
            )

            canvas_nodes.append({
                "id": f"node-{cand.candidate_id}",
                "type": "text",
                "text": text_body,
                "x": pos_x,
                "y": pos_y,
                "width": 260,
                "height": 180,
                "color": card_color
            })

        # Create dominance directional edges (dominating -> dominated)
        edge_idx = 1
        for cand in analysis.candidates:
            for dominated_id in cand.dominates:
                canvas_edges.append({
                    "id": f"edge-{edge_idx}",
                    "fromNode": f"node-{cand.candidate_id}",
                    "fromSide": "bottom",
                    "toNode": f"node-{dominated_id}",
                    "toSide": "top",
                    "toEnd": "arrow",
                    "label": "Dominates",
                    "color": "4"
                })
                edge_idx += 1

        # Add an informational legend node
        canvas_nodes.append({
            "id": "node-legend",
            "type": "text",
            "text": (
                f"## Architectural Pareto Frontier Space\n"
                f"- **X-Axis:** {x_label}\n"
                f"- **Y-Axis:** {y_label}\n"
                f"- **Green Cards:** Pareto-optimal (non-dominated candidates)\n"
                f"- **Red Cards:** Dominated designs (strictly improved by upstream solutions)\n"
                f"- **Edges:** Mathematical dominance trajectories"
            ),
            "x": 100,
            "y": -120,
            "width": 380,
            "height": 160,
            "color": "5"  # Cyan/Blue
        })

        return {
            "nodes": canvas_nodes,
            "edges": canvas_edges
        }

    def export_summary_markdown(self) -> str:
        """Generate an executive architectural trade-off synthesis markdown report."""
        analysis = self.evaluate_pareto()
        lines = [
            "# Architectural Trade-Off Radar & Pareto Frontier Report",
            "",
            "## Executive Summary",
            f"- **Total Candidates Evaluated:** {len(analysis.candidates)}",
            f"- **Pareto-Optimal Solutions:** {len(analysis.pareto_frontier_ids)}",
            f"- **Dominated Configurations:** {len(analysis.dominated_ids)}",
            "",
            "## Non-Dominated Pareto Frontier",
            ""
        ]

        for cid in analysis.pareto_frontier_ids:
            cand = self.candidates[cid]
            lines.append(f"### {cand.name} (`{cand.candidate_id}`)")
            lines.append(f"{cand.description}")
            lines.append("")
            lines.append("| Evaluation Axis | Score | Relative Standing |")
            lines.append("| :--- | :--- | :--- |")
            for ax in self.axes:
                score = cand.get_score(ax)
                bar = "[" + "=" * int(score * 10) + "." * (10 - int(score * 10)) + "]"
                lines.append(f"| {self.axis_labels.get(ax, ax)} | `{score:.2f}` | `{bar}` |")
            lines.append("")

        if analysis.dominated_ids:
            lines.append("## Dominated Configurations")
            lines.append("These candidate solutions are strictly inferior to at least one frontier option:")
            lines.append("")
            for cid in analysis.dominated_ids:
                cand = self.candidates[cid]
                dom_names = [self.candidates[d].name for d in cand.dominated_by]
                lines.append(f"- **{cand.name}:** Dominated by {', '.join(dom_names)}")
            lines.append("")

        if analysis.tradeoff_tensions:
            lines.append("## Key Architectural Tensions")
            for tension in analysis.tradeoff_tensions:
                lines.append(f"- **{tension['label_1']} vs {tension['label_2']}:** Tension score `{tension['tension_score']}`. {tension['description']}")
            lines.append("")

        lines.append("## Archetype Recommendations")
        for ax, cid in analysis.archetype_recommendations.items():
            cand = self.candidates[cid]
            lbl = self.axis_labels.get(ax, ax)
            lines.append(f"- **Best for {lbl}:** {cand.name} (Score: `{cand.get_score(ax):.2f}`)")

        return "\n".join(lines)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize state to structured dictionary."""
        return {
            "axes": self.axes,
            "axis_labels": self.axis_labels,
            "candidates": [
                {
                    "candidate_id": c.candidate_id,
                    "name": c.name,
                    "description": c.description,
                    "scores": c.scores,
                    "tags": c.tags,
                    "is_pareto_optimal": c.is_pareto_optimal,
                    "dominated_by": c.dominated_by,
                    "dominates": c.dominates
                }
                for c in self.candidates.values()
            ]
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ArchitecturalTradeoffRadar":
        """Reconstruct instance from dictionary."""
        axes = data.get("axes", DEFAULT_AXES)
        radar = cls(axes=axes)
        if "axis_labels" in data:
            radar.axis_labels = data["axis_labels"]

        for cand_data in data.get("candidates", []):
            radar.add_candidate(
                name=cand_data["name"],
                scores=cand_data.get("scores", {}),
                description=cand_data.get("description", ""),
                candidate_id=cand_data.get("candidate_id"),
                tags=cand_data.get("tags", [])
            )
        return radar


def create_sample_tradeoff_radar() -> ArchitecturalTradeoffRadar:
    """Create a demonstration trade-off radar representing software architecture choices."""
    radar = ArchitecturalTradeoffRadar(axes=[
        "cognitive_simplicity",
        "throughput_speed",
        "maintainability",
        "fault_resilience",
        "developer_ergonomics"
    ])

    # Candidate 1: Modular Monolith
    radar.add_candidate(
        name="Modular Monolith",
        description="Unified codebase with strictly enforced domain module boundaries and zero network hops.",
        scores={
            "cognitive_simplicity": 0.95,
            "throughput_speed": 0.88,
            "maintainability": 0.82,
            "fault_resilience": 0.65,
            "developer_ergonomics": 0.92
        },
        tags=["monolith", "low-latency"]
    )

    # Candidate 2: Event-Driven Microservices
    radar.add_candidate(
        name="Event-Driven Microservices",
        description="Decoupled micro-services communicating via asynchronous event bus.",
        scores={
            "cognitive_simplicity": 0.40,
            "throughput_speed": 0.75,
            "maintainability": 0.70,
            "fault_resilience": 0.94,
            "developer_ergonomics": 0.58
        },
        tags=["distributed", "resilient"]
    )

    # Candidate 3: Edge Serverless Functions
    radar.add_candidate(
        name="Edge Serverless Mesh",
        description="Ephemerally invoked edge functions placed near end-users with global replication.",
        scores={
            "cognitive_simplicity": 0.60,
            "throughput_speed": 0.92,
            "maintainability": 0.62,
            "fault_resilience": 0.85,
            "developer_ergonomics": 0.70
        },
        tags=["serverless", "edge"]
    )

    # Candidate 4: Legacy Spaghetti Monolith (Dominated design)
    radar.add_candidate(
        name="Tangled Legacy Core",
        description="Tight coupling, shared mutable global database state, manual deployment.",
        scores={
            "cognitive_simplicity": 0.25,
            "throughput_speed": 0.35,
            "maintainability": 0.20,
            "fault_resilience": 0.30,
            "developer_ergonomics": 0.20
        },
        tags=["legacy", "technical-debt"]
    )

    return radar


if __name__ == "__main__":
    demo_radar = create_sample_tradeoff_radar()
    analysis = demo_radar.evaluate_pareto()
    print(f"Evaluated {len(analysis.candidates)} candidates.")
    print(f"Pareto Frontier: {', '.join(analysis.pareto_frontier_ids)}")
    print(f"Dominated: {', '.join(analysis.dominated_ids)}")
    print(demo_radar.export_summary_markdown())
