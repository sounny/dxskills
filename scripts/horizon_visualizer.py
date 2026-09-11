"""
Autonomous Cognitive Multi-Scale Working Memory Horizon Visualizer for DxSkills.

Grounded in:
- Eide and Eide M-I-N-D spatial framework (concentric multi-scale architectural reasoning)
- Sweller Cognitive Load Theory (eliminating near-term working memory fragmentation)
- Baddeley Working Memory Model (dynamic executive bandwidth allocation across temporal horizons)
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional


@dataclass
class HorizonItem:
    """Individual cognitive element situated within a specific temporal and spatial horizon."""
    id: str
    label: str
    horizon: str  # "immediate", "tactical", "strategic"
    estimated_hours: float
    cognitive_weight: float  # 1.0 to 10.0
    parent_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class HorizonTelemetry:
    """Quantitative telemetry evaluating working memory bandwidth allocation across horizons."""
    total_items: int
    immediate_count: int
    tactical_count: int
    strategic_count: int
    immediate_bandwidth_pct: float
    tactical_bandwidth_pct: float
    strategic_bandwidth_pct: float
    fragmentation_index: float
    balance_status: str
    recommendations: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class WorkingMemoryHorizonVisualizer:
    """
    Maps immediate micro-tasks, tactical project milestones, and macro strategic horizons
    onto concentric spatial orbits to prevent working memory saturation and context fragmentation.
    """

    def __init__(self) -> None:
        pass

    def evaluate_horizons(self, items: List[HorizonItem]) -> HorizonTelemetry:
        """
        Evaluate distribution of cognitive weight and identify horizon imbalances.
        """
        if not items:
            return HorizonTelemetry(
                total_items=0,
                immediate_count=0,
                tactical_count=0,
                strategic_count=0,
                immediate_bandwidth_pct=0.0,
                tactical_bandwidth_pct=0.0,
                strategic_bandwidth_pct=0.0,
                fragmentation_index=0.0,
                balance_status="Uncalibrated (Empty Horizon)",
                recommendations=["Populate horizon items across immediate, tactical, and strategic scopes."],
            )

        immediate = [it for it in items if it.horizon.lower() == "immediate"]
        tactical = [it for it in items if it.horizon.lower() == "tactical"]
        strategic = [it for it in items if it.horizon.lower() == "strategic"]

        imm_weight = sum(it.cognitive_weight for it in immediate)
        tac_weight = sum(it.cognitive_weight for it in tactical)
        str_weight = sum(it.cognitive_weight for it in strategic)
        total_weight = imm_weight + tac_weight + str_weight or 1.0

        imm_pct = round((imm_weight / total_weight) * 100, 1)
        tac_pct = round((tac_weight / total_weight) * 100, 1)
        str_pct = round((str_weight / total_weight) * 100, 1)

        # Fragmentation penalty occurs if immediate tasks exceed Cowan capacity limit (> 4 items)
        imm_overload = max(0, len(immediate) - 4) * 0.15
        # Penalty if tactical or strategic items are completely missing (tunnel vision or daydreaming)
        missing_penalty = 0.25 if not tactical else 0.0
        missing_penalty += 0.25 if not strategic else 0.0

        frag_index = round(min(1.0, max(0.05, imm_overload + missing_penalty + (len(items) * 0.02))), 2)

        recommendations = []
        if len(immediate) > 4:
            recommendations.append(
                f"Foveal overload: {len(immediate)} immediate tasks active. Prune down to 3-4 items to protect working memory."
            )
        if not strategic:
            recommendations.append(
                "Strategic blindspot: Zero macro architectural horizons defined. Risk of aimless local optimization."
            )
        if not tactical:
            recommendations.append(
                "Tactical void: Missing intermediary milestones linking today's execution to the strategic north star."
            )
        if imm_pct > 70.0:
            status = "Foveal Tunnel Overload"
            recommendations.append("Shift 25% of cognitive energy to tactical scaffolding and systemic architecture.")
        elif str_pct > 70.0:
            status = "Ungrounded Abstract Daydream"
            recommendations.append("Anchor macro concepts into immediate executable milestones.")
        elif frag_index > 0.55:
            status = "High Context Fragmentation"
            recommendations.append("Group immediate sub-tasks into unified thematic chunks.")
        else:
            status = "Coherent Multi-Scale Alignment"
            recommendations.append("Horizon distribution is balanced across execution, tactics, and vision.")

        return HorizonTelemetry(
            total_items=len(items),
            immediate_count=len(immediate),
            tactical_count=len(tactical),
            strategic_count=len(strategic),
            immediate_bandwidth_pct=imm_pct,
            tactical_bandwidth_pct=tac_pct,
            strategic_bandwidth_pct=str_pct,
            fragmentation_index=frag_index,
            balance_status=status,
            recommendations=recommendations,
        )

    def export_canvas(
        self,
        items: List[HorizonItem],
        telemetry: HorizonTelemetry,
        output_path: str = "memory_horizons.canvas",
    ) -> Dict[str, Any]:
        """
        Export concentric spatial horizon orbits into Obsidian .canvas JSON format.
        """
        nodes = []
        edges = []

        # Central Header Node
        nodes.append({
            "id": "node-horizon-hub",
            "x": 0,
            "y": -400,
            "width": 380,
            "height": 180,
            "type": "text",
            "text": (
                f"### [Working Memory Horizon Hub]\n\n"
                f"- **Status:** {telemetry.balance_status}\n"
                f"- **Fragmentation Index:** {int(telemetry.fragmentation_index * 100)}%\n"
                f"- **Bandwidth Ratio:** Imm {telemetry.immediate_bandwidth_pct}% | Tac {telemetry.tactical_bandwidth_pct}% | Str {telemetry.strategic_bandwidth_pct}%\n"
                f"- **Total Nodes:** {telemetry.total_items}"
            ),
            "color": "4",
        })

        # Orbit radii
        radius_map = {
            "immediate": 180.0,
            "tactical": 380.0,
            "strategic": 580.0,
        }
        color_map = {
            "immediate": "1",  # Red / high priority
            "tactical": "2",   # Orange / amber
            "strategic": "5",  # Cyan / purple
        }

        # Position nodes radially around the center (0, 0)
        groups = {
            "immediate": [it for it in items if it.horizon.lower() == "immediate"],
            "tactical": [it for it in items if it.horizon.lower() == "tactical"],
            "strategic": [it for it in items if it.horizon.lower() == "strategic"],
        }

        for horizon_key, group_items in groups.items():
            r = radius_map[horizon_key]
            c = color_map[horizon_key]
            n_items = len(group_items)
            for idx, it in enumerate(group_items):
                angle = (2.0 * math.pi * idx / max(1, n_items)) - (math.pi / 2.0)
                nx = int(r * math.cos(angle))
                ny = int(r * math.sin(angle)) + 80  # shift slightly down from header

                node_id = f"node-item-{it.id}"
                nodes.append({
                    "id": node_id,
                    "x": nx - 120,
                    "y": ny - 60,
                    "width": 240,
                    "height": 120,
                    "type": "text",
                    "text": (
                        f"**[{it.horizon.upper()}]** {it.label}\n\n"
                        f"- Est: {it.estimated_hours}h\n"
                        f"- Weight: {it.cognitive_weight}/10"
                    ),
                    "color": c,
                })

                if it.parent_id:
                    edges.append({
                        "id": f"edge-{it.parent_id}-{it.id}",
                        "fromNode": f"node-item-{it.parent_id}",
                        "fromSide": "bottom",
                        "toNode": node_id,
                        "toSide": "top",
                    })

        canvas_data = {"nodes": nodes, "edges": edges}

        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(canvas_data, f, indent=2)

        return canvas_data

    def export_svg_radar(
        self,
        items: List[HorizonItem],
        telemetry: HorizonTelemetry,
        width: int = 600,
        height: int = 400,
    ) -> str:
        """
        Export modern vector SVG visualizer of concentric horizon orbits.
        """
        cx, cy = 200, 200
        frag_pct = int(telemetry.fragmentation_index * 100)

        svg = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="auto">',
            '  <defs>',
            '    <linearGradient id="bgGradHorizon" x1="0%" y1="0%" x2="100%" y2="100%">',
            '      <stop offset="0%" stop-color="#0b1120" />',
            '      <stop offset="100%" stop-color="#1e293b" />',
            '    </linearGradient>',
            '  </defs>',
            f'  <rect width="{width}" height="{height}" rx="14" fill="url(#bgGradHorizon)" stroke="#334155" stroke-width="1.5" />',
            f'  <text x="24" y="36" fill="#f8fafc" font-family="system-ui, -apple-system, sans-serif" font-size="16" font-weight="bold">Working Memory Horizon Radar</text>',
            f'  <text x="24" y="58" fill="#94a3b8" font-family="system-ui, -apple-system, sans-serif" font-size="12">Status: {telemetry.balance_status} | Fragmentation: {frag_pct}%</text>',
            '  <!-- Concentric Spatial Orbits -->',
            f'  <circle cx="{cx}" cy="{cy}" r="140" fill="none" stroke="#475569" stroke-width="1" stroke-dasharray="4,4" />',
            f'  <circle cx="{cx}" cy="{cy}" r="95" fill="none" stroke="#64748b" stroke-width="1" stroke-dasharray="3,3" />',
            f'  <circle cx="{cx}" cy="{cy}" r="50" fill="none" stroke="#94a3b8" stroke-width="1.5" />',
            f'  <circle cx="{cx}" cy="{cy}" r="12" fill="#38bdf8" />',
            f'  <text x="{cx}" y="{cy - 55}" fill="#f43f5e" font-family="system-ui, sans-serif" font-size="10" text-anchor="middle">Immediate (0-4h)</text>',
            f'  <text x="{cx}" y="{cy - 100}" fill="#fbbf24" font-family="system-ui, sans-serif" font-size="10" text-anchor="middle">Tactical (1-14d)</text>',
            f'  <text x="{cx}" y="{cy - 145}" fill="#818cf8" font-family="system-ui, sans-serif" font-size="10" text-anchor="middle">Strategic (1-12m)</text>',
        ]

        # Draw node markers on radar
        radius_map = {"immediate": 50.0, "tactical": 95.0, "strategic": 140.0}
        color_map = {"immediate": "#f43f5e", "tactical": "#fbbf24", "strategic": "#818cf8"}

        groups = {
            "immediate": [it for it in items if it.horizon.lower() == "immediate"],
            "tactical": [it for it in items if it.horizon.lower() == "tactical"],
            "strategic": [it for it in items if it.horizon.lower() == "strategic"],
        }

        for h_key, grp in groups.items():
            r = radius_map[h_key]
            c = color_map[h_key]
            for idx, it in enumerate(grp):
                angle = (2.0 * math.pi * idx / max(1, len(grp))) - (math.pi / 2.0)
                px = cx + int(r * math.cos(angle))
                py = cy + int(r * math.sin(angle))
                svg.append(f'  <circle cx="{px}" cy="{py}" r="6" fill="{c}" stroke="#0f172a" stroke-width="1.5" />')

        # Side Telemetry Panel
        svg.extend([
            '  <!-- Bandwidth Distribution Bars -->',
            '  <g transform="translate(380, 95)">',
            f'    <text x="0" y="20" fill="#f43f5e" font-family="system-ui, sans-serif" font-size="13" font-weight="bold">Immediate: {telemetry.immediate_bandwidth_pct}% ({telemetry.immediate_count} items)</text>',
            '    <rect x="0" y="30" width="190" height="8" rx="4" fill="#1e293b" />',
            f'    <rect x="0" y="30" width="{int(telemetry.immediate_bandwidth_pct * 1.9)}" height="8" rx="4" fill="#f43f5e" />',
            f'    <text x="0" y="65" fill="#fbbf24" font-family="system-ui, sans-serif" font-size="13" font-weight="bold">Tactical: {telemetry.tactical_bandwidth_pct}% ({telemetry.tactical_count} items)</text>',
            '    <rect x="0" y="75" width="190" height="8" rx="4" fill="#1e293b" />',
            f'    <rect x="0" y="75" width="{int(telemetry.tactical_bandwidth_pct * 1.9)}" height="8" rx="4" fill="#fbbf24" />',
            f'    <text x="0" y="110" fill="#818cf8" font-family="system-ui, sans-serif" font-size="13" font-weight="bold">Strategic: {telemetry.strategic_bandwidth_pct}% ({telemetry.strategic_count} items)</text>',
            '    <rect x="0" y="120" width="190" height="8" rx="4" fill="#1e293b" />',
            f'    <rect x="0" y="120" width="{int(telemetry.strategic_bandwidth_pct * 1.9)}" height="8" rx="4" fill="#818cf8" />',
            '    <line x1="0" y1="150" x2="190" y2="150" stroke="#334155" stroke-width="1" />',
            f'    <text x="0" y="175" fill="#38bdf8" font-family="system-ui, sans-serif" font-size="12" font-weight="600">Fragmentation: {frag_pct}%</text>',
            f'    <text x="0" y="195" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="11">Cowan Limit: 4 Active Tokens</text>',
            '  </g>',
            '</svg>',
        ])

        return "\n".join(svg)

    def export_summary_markdown(self, telemetry: HorizonTelemetry, items: List[HorizonItem]) -> str:
        """
        Generate executive horizon audit report in Markdown with zero em dashes.
        """
        lines = [
            "# Multi-Scale Working Memory Horizon Audit",
            "",
            f"**Cognitive Balance Status:** {telemetry.balance_status}",
            f"**Context Fragmentation Index:** {telemetry.fragmentation_index} (0.0 to 1.0)",
            f"**Bandwidth Allocation:** Immediate {telemetry.immediate_bandwidth_pct}% | Tactical {telemetry.tactical_bandwidth_pct}% | Strategic {telemetry.strategic_bandwidth_pct}%",
            "",
            "## 1. Recommendations",
            "",
        ]

        for rec in telemetry.recommendations:
            lines.append(f"- {rec}")

        lines.extend([
            "",
            "## 2. Active Cognitive Horizon Distribution",
            "",
        ])

        horizons = ["immediate", "tactical", "strategic"]
        for h in horizons:
            matched = [it for it in items if it.horizon.lower() == h]
            lines.append(f"### {h.title()} Horizon ({len(matched)} elements)")
            if not matched:
                lines.append("*No active items allocated to this horizon.*")
            else:
                for it in matched:
                    lines.append(f"- **{it.label}** (Est: {it.estimated_hours}h, Weight: {it.cognitive_weight}/10)")
            lines.append("")

        lines.extend([
            "---",
            "*Generated by DxSkills Horizon Visualizer. Zero phonological friction, zero em dashes.*",
        ])

        return "\n".join(lines)
