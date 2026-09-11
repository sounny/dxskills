#!/usr/bin/env python3
"""
Autonomous Cognitive Multi-Perspective Decision Matrix & Spatial Opportunity Cost Evaluator
Part of the DxSkills Cognitive Architecture Suite (https://dxskills.sounny.com)

Plots multi-criteria decision options across immediate tactical utility, compounding
leverage, cognitive friction, and hidden opportunity costs. Maps candidate initiatives
into 4 spatial quadrants to eliminate executive dysfunction and analysis paralysis.

Core Principles:
- Non-Linear Leverage Evaluation: Distinguishes between shallow urgency and compounding assets.
- Spatial Quadrant Mapping: Replaces flat 1D lists with high-contrast 2D decision geometry.
- Opportunity Cost Quantification: Exposes the hidden long-term penalty of delayed action.
- Zero Jargon Friction: Translates complex decision theory into immediate spatial actions.
"""

import os
import re
import json
import math
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple, Set


QUADRANT_METADATA = {
    "q1": {
        "title": "Compounding Superhighway",
        "description": "High Leverage, High Flow. Execute immediately to trigger exponential gains.",
        "color": "4",  # Emerald Green
        "theme": "#10b981",
        "badge": "[EXECUTE NOW]"
    },
    "q2": {
        "title": "Strategic Breakthrough",
        "description": "High Leverage, High Friction. Decompose into micro-anchors to overcome resistance.",
        "color": "5",  # Cyan / Sky Blue
        "theme": "#38bdf8",
        "badge": "[CHUNK & DECOMPOSE]"
    },
    "q3": {
        "title": "Flow Sprints",
        "description": "Low Leverage, High Flow. Quick wins; batch during low cognitive energy periods.",
        "color": "2",  # Amber
        "theme": "#f59e0b",
        "badge": "[BATCH PROCESS]"
    },
    "q4": {
        "title": "Cognitive Debt Traps",
        "description": "Low Leverage, High Friction. Ruthlessly eliminate, automate, or delegate.",
        "color": "1",  # Red / Muted
        "theme": "#f43f5e",
        "badge": "[ELIMINATE / DELEGATE]"
    }
}


@dataclass
class DecisionOption:
    """An individual architectural initiative or strategic decision candidate."""
    option_id: str
    name: str
    description: str
    immediate_utility: float      # 0.0 to 1.0 (tactical short-term payoff)
    compounding_leverage: float   # 0.0 to 1.0 (long-term compounding multiplier)
    opportunity_cost_risk: float  # 0.0 to 1.0 (penalty of inaction / delay)
    cognitive_flow: float         # 0.0 to 1.0 (1.0 = frictionless flow; 0.0 = high drag)
    reversibility: float          # 0.0 to 1.0 (ease of reversing / pivoting)
    quadrant: str = "q4"
    leverage_score: float = 0.0
    tags: List[str] = field(default_factory=list)

    def calculate_scores(self) -> None:
        """Compute composite opportunity cost leverage score and assign spatial quadrant."""
        # Higher compounding leverage + high cost of inaction = massive opportunity cost
        # Bounded by cognitive flow friction
        drag = max(0.15, 1.05 - self.cognitive_flow)
        raw_leverage = (self.compounding_leverage * (1.0 + self.opportunity_cost_risk)) / drag
        self.leverage_score = round(raw_leverage, 2)

        # Quadrant placement based on Compounding Leverage (Y) and Cognitive Flow (X)
        is_high_leverage = self.compounding_leverage >= 0.50
        is_high_flow = self.cognitive_flow >= 0.50

        if is_high_leverage and is_high_flow:
            self.quadrant = "q1"
        elif is_high_leverage and not is_high_flow:
            self.quadrant = "q2"
        elif not is_high_leverage and is_high_flow:
            self.quadrant = "q3"
        else:
            self.quadrant = "q4"


@dataclass
class DecisionAudit:
    """Telemetry report summarizing spatial decision balance and prioritized actions."""
    total_options: int
    q1_count: int
    q2_count: int
    q3_count: int
    q4_count: int
    highest_leverage_option: Optional[DecisionOption]
    highest_opportunity_cost_option: Optional[DecisionOption]
    action_roadmap: List[DecisionOption]


class SpatialDecisionMatrix:
    """Evaluates multi-perspective decision candidates and generates spatial decision maps."""

    def __init__(self):
        self.options: Dict[str, DecisionOption] = {}
        self._next_idx = 1

    def add_option(
        self,
        name: str,
        immediate_utility: float,
        compounding_leverage: float,
        opportunity_cost_risk: float,
        cognitive_flow: float,
        reversibility: float = 0.5,
        description: str = "",
        option_id: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> DecisionOption:
        """Register a decision option with normalized 0.0-1.0 criteria."""
        oid = option_id or f"opt-{self._next_idx}"
        self._next_idx += 1

        opt = DecisionOption(
            option_id=oid,
            name=name.strip(),
            description=description.strip(),
            immediate_utility=max(0.0, min(1.0, float(immediate_utility))),
            compounding_leverage=max(0.0, min(1.0, float(compounding_leverage))),
            opportunity_cost_risk=max(0.0, min(1.0, float(opportunity_cost_risk))),
            cognitive_flow=max(0.0, min(1.0, float(cognitive_flow))),
            reversibility=max(0.0, min(1.0, float(reversibility))),
            tags=list(tags) if tags else []
        )
        opt.calculate_scores()
        self.options[oid] = opt
        return opt

    def evaluate_matrix(self) -> DecisionAudit:
        """Evaluate all registered options, classify quadrants, and prioritize execution."""
        for opt in self.options.values():
            opt.calculate_scores()

        opts = list(self.options.values())
        # Sort roadmap by leverage score descending
        opts.sort(key=lambda o: (o.leverage_score, o.compounding_leverage), reverse=True)

        q1 = sum(1 for o in opts if o.quadrant == "q1")
        q2 = sum(1 for o in opts if o.quadrant == "q2")
        q3 = sum(1 for o in opts if o.quadrant == "q3")
        q4 = sum(1 for o in opts if o.quadrant == "q4")

        highest_lev = max(opts, key=lambda o: o.leverage_score, default=None)
        highest_opp = max(opts, key=lambda o: o.opportunity_cost_risk, default=None)

        return DecisionAudit(
            total_options=len(opts),
            q1_count=q1,
            q2_count=q2,
            q3_count=q3,
            q4_count=q4,
            highest_leverage_option=highest_lev,
            highest_opportunity_cost_option=highest_opp,
            action_roadmap=opts
        )

    def export_canvas(self, audit: DecisionAudit) -> Dict[str, Any]:
        """
        Generate an Obsidian .canvas structure mapping decision cards onto a 2D matrix.
        X-Axis = Cognitive Flow (Friction -> Flow: 100 -> 900)
        Y-Axis = Compounding Leverage (Shallow -> High: 900 -> 100)
        """
        canvas_nodes = []
        canvas_edges = []

        min_pos = 120
        span_pos = 840

        # Place candidate cards
        for opt in audit.action_roadmap:
            # High cognitive flow is right (+X); High compounding leverage is top (-Y)
            pos_x = int(min_pos + opt.cognitive_flow * span_pos)
            pos_y = int(min_pos + (1.0 - opt.compounding_leverage) * span_pos)

            q_info = QUADRANT_METADATA[opt.quadrant]
            card_text = (
                f"### {opt.name}\n"
                f"> **{q_info['badge']} | {q_info['title']}**\n\n"
                f"{opt.description}\n\n"
                f"- **Leverage Score:** `{opt.leverage_score}`\n"
                f"- **Compounding:** `{opt.compounding_leverage:.2f}` | **Flow:** `{opt.cognitive_flow:.2f}`\n"
                f"- **Opportunity Risk:** `{opt.opportunity_cost_risk:.2f}` | **Reversibility:** `{opt.reversibility:.2f}`"
            )

            canvas_nodes.append({
                "id": f"node-{opt.option_id}",
                "type": "text",
                "text": card_text,
                "x": pos_x,
                "y": pos_y,
                "width": 270,
                "height": 190,
                "color": q_info["color"]
            })

        # Add 4 Quadrant Background Bounding Labels
        quadrant_hubs = [
            ("hub-q1", "QUADRANT 1: Compounding Superhighways (High Leverage / High Flow)", min_pos + span_pos * 0.55, min_pos, "4"),
            ("hub-q2", "QUADRANT 2: Strategic Breakthroughs (High Leverage / High Friction)", min_pos, min_pos, "5"),
            ("hub-q3", "QUADRANT 3: Flow Sprints (Low Leverage / High Flow)", min_pos + span_pos * 0.55, min_pos + span_pos * 0.55, "2"),
            ("hub-q4", "QUADRANT 4: Cognitive Debt Traps (Low Leverage / High Friction)", min_pos, min_pos + span_pos * 0.55, "1"),
        ]

        for hid, htitle, hx, hy, hcol in quadrant_hubs:
            canvas_nodes.append({
                "id": hid,
                "type": "text",
                "text": f"## {htitle}",
                "x": int(hx),
                "y": int(hy) - 50,
                "width": 420,
                "height": 45,
                "color": hcol
            })

        # Connect top 3 items sequentially to form optimal decision execution sequence
        top_picks = [o for o in audit.action_roadmap if o.quadrant in ("q1", "q2")][:4]
        for i in range(len(top_picks) - 1):
            curr_opt = top_picks[i]
            next_opt = top_picks[i + 1]
            canvas_edges.append({
                "id": f"edge-seq-{i + 1}",
                "fromNode": f"node-{curr_opt.option_id}",
                "toNode": f"node-{next_opt.option_id}",
                "toEnd": "arrow",
                "label": f"Priority Step {i + 1} -> {i + 2}",
                "color": "4"
            })

        return {
            "nodes": canvas_nodes,
            "edges": canvas_edges
        }

    def export_svg_matrix(self, audit: DecisionAudit, width: int = 760, height: int = 560) -> str:
        """
        Generate vector SVG displaying the 2D decision quadrant geometry,
        opportunity cost leverage meters, and prioritized action nodes.
        """
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
            '<!-- Title Header -->',
            f'<text x="28" y="32" fill="#f8fafc" font-size="16" font-weight="700">Multi-Perspective Decision Matrix &amp; Opportunity Cost Evaluator</text>',
            f'<text x="28" y="50" fill="#94a3b8" font-size="12">Compounding Leverage vs. Cognitive Flow Spatial Geometry</text>',
            '<!-- Matrix Grid Bounds -->',
        ]

        grid_x = 70
        grid_y = 75
        grid_w = width - 110
        grid_h = height - 145

        mid_x = grid_x + grid_w / 2.0
        mid_y = grid_y + grid_h / 2.0

        # Background Quadrants
        svg_parts.append(
            f'<rect x="{grid_x}" y="{grid_y}" width="{grid_w / 2.0}" height="{grid_h / 2.0}" fill="#38bdf8" fill-opacity="0.04"/>'
        )
        svg_parts.append(
            f'<rect x="{mid_x}" y="{grid_y}" width="{grid_w / 2.0}" height="{grid_h / 2.0}" fill="#10b981" fill-opacity="0.06"/>'
        )
        svg_parts.append(
            f'<rect x="{grid_x}" y="{mid_y}" width="{grid_w / 2.0}" height="{grid_h / 2.0}" fill="#f43f5e" fill-opacity="0.04"/>'
        )
        svg_parts.append(
            f'<rect x="{mid_x}" y="{mid_y}" width="{grid_w / 2.0}" height="{grid_h / 2.0}" fill="#f59e0b" fill-opacity="0.04"/>'
        )

        # Border and Axes
        svg_parts.append(
            f'<rect x="{grid_x}" y="{grid_y}" width="{grid_w}" height="{grid_h}" fill="none" stroke="#334155" stroke-width="1.5"/>'
        )
        svg_parts.append(
            f'<line x1="{grid_x}" y1="{mid_y}" x2="{grid_x + grid_w}" y2="{mid_y}" stroke="#475569" stroke-width="1.5" stroke-dasharray="3,3"/>'
        )
        svg_parts.append(
            f'<line x1="{mid_x}" y1="{grid_y}" x2="{mid_x}" y2="{grid_y + grid_h}" stroke="#475569" stroke-width="1.5" stroke-dasharray="3,3"/>'
        )

        # Quadrant Watermark Titles
        svg_parts.append(f'<text x="{mid_x + 12}" y="{grid_y + 24}" fill="#10b981" font-size="11" font-weight="700">Q1: Compounding Superhighway</text>')
        svg_parts.append(f'<text x="{grid_x + 12}" y="{grid_y + 24}" fill="#38bdf8" font-size="11" font-weight="700">Q2: Strategic Breakthrough</text>')
        svg_parts.append(f'<text x="{mid_x + 12}" y="{mid_y + 24}" fill="#f59e0b" font-size="11" font-weight="700">Q3: Flow Sprints</text>')
        svg_parts.append(f'<text x="{grid_x + 12}" y="{mid_y + 24}" fill="#f43f5e" font-size="11" font-weight="700">Q4: Cognitive Debt Traps</text>')

        # Axis Labels
        svg_parts.append(f'<text x="{grid_x + grid_w / 2.0}" y="{height - 20}" fill="#94a3b8" font-size="11.5" font-weight="600" text-anchor="middle">Cognitive Flow (Friction &lt;---&gt; Flow State)</text>')
        svg_parts.append(
            f'<text transform="rotate(-90)" x="{- (grid_y + grid_h / 2.0)}" y="25" fill="#94a3b8" font-size="11.5" font-weight="600" text-anchor="middle">Compounding Leverage (Shallow &lt;---&gt; High Multiplier)</text>'
        )

        # Plot Options as Glowing Nodes
        for opt in audit.action_roadmap:
            px = grid_x + opt.cognitive_flow * grid_w
            py = grid_y + (1.0 - opt.compounding_leverage) * grid_h

            q_color = QUADRANT_METADATA[opt.quadrant]["theme"]
            r_size = 6.0 + (opt.leverage_score * 2.0)
            r_size = min(15.0, max(6.0, r_size))

            glow = ' filter="url(#glow)"' if opt.quadrant in ("q1", "q2") else ""
            svg_parts.append(
                f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{r_size:.1f}" fill="{q_color}" fill-opacity="0.8" stroke="#ffffff" stroke-width="1.5"{glow}/>'
            )
            # Label
            svg_parts.append(
                f'<text x="{px + r_size + 6:.1f}" y="{py + 4:.1f}" fill="#f8fafc" font-size="10.5" font-weight="600">{opt.name[:22]}</text>'
            )

        svg_parts.append('</svg>')
        return "\n".join(svg_parts)

    def export_summary_markdown(self, audit: DecisionAudit) -> str:
        """Generate executive decision synthesis report with opportunity cost analysis."""
        lines = [
            "# Multi-Perspective Decision Matrix & Opportunity Cost Report",
            "",
            "## Executive Synthesis",
            f"- **Total Initiatives Evaluated:** {audit.total_options}",
            f"- **Q1 Compounding Superhighways:** {audit.q1_count} (Immediate execution)",
            f"- **Q2 Strategic Breakthroughs:** {audit.q2_count} (High leverage, requires chunking)",
            f"- **Q3 Flow Sprints:** {audit.q3_count} (Batch process during low energy)",
            f"- **Q4 Cognitive Debt Traps:** {audit.q4_count} (Eliminate, automate, or delegate)",
            ""
        ]

        if audit.highest_leverage_option:
            top = audit.highest_leverage_option
            lines.append(f"> **Top Strategic Imperative:** **{top.name}** (Leverage Score: `{top.leverage_score}` in {QUADRANT_METADATA[top.quadrant]['title']})")
            lines.append(f"> {top.description}")
            lines.append("")

        lines.append("## Prioritized Action Roadmap")
        lines.append("")
        lines.append("| Priority | Option Name | Quadrant | Leverage Score | Compounding | Flow | Opportunity Risk | Reversible |")
        lines.append("| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: |")

        for idx, opt in enumerate(audit.action_roadmap, 1):
            q_title = QUADRANT_METADATA[opt.quadrant]["title"]
            lines.append(
                f"| #{idx} | **{opt.name}** | {q_title} | `{opt.leverage_score}` | "
                f"`{opt.compounding_leverage:.2f}` | `{opt.cognitive_flow:.2f}` | "
                f"`{opt.opportunity_cost_risk:.2f}` | `{opt.reversibility:.2f}` |"
            )
        lines.append("")

        lines.append("## Tactical Execution Directives")
        for opt in audit.action_roadmap:
            directive = QUADRANT_METADATA[opt.quadrant]["badge"]
            lines.append(f"### {opt.name} {directive}")
            lines.append(f"- **Assessment:** {opt.description}")
            lines.append(f"- **Tactical Advice:** {QUADRANT_METADATA[opt.quadrant]['description']}")
            lines.append("")

        return "\n".join(lines)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize matrix state to dictionary."""
        return {
            "options": [
                {
                    "option_id": o.option_id,
                    "name": o.name,
                    "description": o.description,
                    "immediate_utility": o.immediate_utility,
                    "compounding_leverage": o.compounding_leverage,
                    "opportunity_cost_risk": o.opportunity_cost_risk,
                    "cognitive_flow": o.cognitive_flow,
                    "reversibility": o.reversibility,
                    "quadrant": o.quadrant,
                    "leverage_score": o.leverage_score,
                    "tags": o.tags
                }
                for o in self.options.values()
            ]
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SpatialDecisionMatrix":
        """Construct matrix instance from dictionary."""
        matrix = cls()
        for opt_data in data.get("options", []):
            matrix.add_option(
                name=opt_data["name"],
                immediate_utility=opt_data["immediate_utility"],
                compounding_leverage=opt_data["compounding_leverage"],
                opportunity_cost_risk=opt_data["opportunity_cost_risk"],
                cognitive_flow=opt_data["cognitive_flow"],
                reversibility=opt_data.get("reversibility", 0.5),
                description=opt_data.get("description", ""),
                option_id=opt_data.get("option_id"),
                tags=opt_data.get("tags", [])
            )
        return matrix


def create_sample_decision_matrix() -> SpatialDecisionMatrix:
    """Create sample strategic decision matrix representing software initiatives."""
    matrix = SpatialDecisionMatrix()

    # Q1: High Leverage, High Flow
    matrix.add_option(
        name="Automate CLI Scaffolding Pipeline",
        description="Write single script unifying manual multi-repo packaging and release.",
        immediate_utility=0.85,
        compounding_leverage=0.92,
        opportunity_cost_risk=0.88,
        cognitive_flow=0.85,
        reversibility=0.95,
        tags=["automation", "tooling"]
    )

    # Q2: High Leverage, High Friction
    matrix.add_option(
        name="Refactor Database Core Schema to Event Sourcing",
        description="Transition legacy mutable PostgreSQL tables to immutable append-only event stream.",
        immediate_utility=0.45,
        compounding_leverage=0.95,
        opportunity_cost_risk=0.90,
        cognitive_flow=0.30,
        reversibility=0.25,
        tags=["architecture", "refactoring"]
    )

    # Q3: Low Leverage, High Flow
    matrix.add_option(
        name="Polish Terminal Status Badges and Colors",
        description="Adjust ANSI terminal highlight palette for aesthetic satisfaction.",
        immediate_utility=0.60,
        compounding_leverage=0.25,
        opportunity_cost_risk=0.15,
        cognitive_flow=0.90,
        reversibility=1.0,
        tags=["ui", "quick-win"]
    )

    # Q4: Low Leverage, High Friction
    matrix.add_option(
        name="Manual Email Vendor Compliance Questionnaire",
        description="Fill out 40-page repetitive procurement form manually without automation.",
        immediate_utility=0.20,
        compounding_leverage=0.10,
        opportunity_cost_risk=0.20,
        cognitive_flow=0.15,
        reversibility=0.50,
        tags=["bureaucracy", "debt"]
    )

    return matrix


if __name__ == "__main__":
    matrix = create_sample_decision_matrix()
    audit = matrix.evaluate_matrix()
    print(matrix.export_summary_markdown(audit))
