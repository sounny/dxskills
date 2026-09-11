"""Autonomous Cognitive Spatial Non-Linear Executive Scaffolding & Action Sequencer.

Theoretical Foundation:
- Barkley's Executive Function & Brown's Executive Dysfunction Model:
  Non-linear and dyslexic/ADHD minds excel at multi-directional divergent brainstorming
  but encounter severe cognitive friction during sequence extraction and task initiation.
  The visual ambiguity of unstructured canvas clusters triggers decision fatigue and
  initiation paralysis.
- Critical Path Method (CPM) & Topological DAG Resolution:
  Converts non-linear spatial idea clusters and dependency edges into a Directed
  Acyclic Graph (DAG). Kahn's topological sort determines execution order, while
  CPM isolates the zero-slack critical sequence determining true project runway.
- Implementation Intentions (Gollwitzer) & Micro-Commitment Scaffolding (Fogg):
  Bypasses executive inertia by decomposing the active bottleneck node into sub-2-minute
  tactile stepping stones framed as concrete "If [Trigger], then [Micro-Action]"
  commitments with immediate sensory feedback.
- Spatial Canvas Runway & Dark Titanium SVG Export:
  Enriches Obsidian .canvas workspaces with sequential lane markers and produces
  publication-grade SVG critical path visualizations.

Strict Quality Gate: Zero em dashes anywhere (use hyphens, commas, or parentheses).
"""

from __future__ import annotations

import enum
import json
import math
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


class TaskStatus(str, enum.Enum):
    """Execution readiness of a spatial action node."""

    READY = "ready"
    BLOCKED = "blocked"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


@dataclass
class MicroSteppingStone:
    """Sub-2-minute tactile micro-commitment bypassing executive dysfunction."""

    stone_id: str
    parent_node_id: str
    action_prompt: str
    target_duration_seconds: int
    implementation_intention: str
    sensory_anchor: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert micro-stone to serializable dictionary."""
        return {
            "stone_id": self.stone_id,
            "parent_node_id": self.parent_node_id,
            "action_prompt": self.action_prompt,
            "target_duration_seconds": self.target_duration_seconds,
            "implementation_intention": self.implementation_intention,
            "sensory_anchor": self.sensory_anchor,
        }


@dataclass
class ActionNode:
    """Actionable node within the topological execution DAG."""

    node_id: str
    title: str
    description: str
    estimated_minutes: int
    prerequisites: List[str] = field(default_factory=list)
    dependents: List[str] = field(default_factory=list)
    topological_order: int = 0
    earliest_start: int = 0
    latest_start: int = 0
    slack_minutes: int = 0
    is_critical_path: bool = False
    lane_id: int = 0
    status: TaskStatus = TaskStatus.BLOCKED
    stepping_stones: List[MicroSteppingStone] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert action node to serializable dictionary."""
        return {
            "node_id": self.node_id,
            "title": self.title,
            "description": self.description,
            "estimated_minutes": self.estimated_minutes,
            "prerequisites": sorted(self.prerequisites),
            "dependents": sorted(self.dependents),
            "topological_order": self.topological_order,
            "earliest_start": self.earliest_start,
            "latest_start": self.latest_start,
            "slack_minutes": self.slack_minutes,
            "is_critical_path": self.is_critical_path,
            "lane_id": self.lane_id,
            "status": self.status.value,
            "stepping_stones": [s.to_dict() for s in self.stepping_stones],
        }


@dataclass
class SequencingTelemetry:
    """Telemetry capturing topological complexity and executive runway metrics."""

    total_nodes: int
    total_dependencies: int
    critical_path_node_count: int
    critical_path_duration_minutes: int
    parallel_lanes_count: int
    immediately_executable_count: int
    total_estimated_work_minutes: int
    dysfunction_bypass_ratio: float
    critical_path_ids: List[str] = field(default_factory=list)
    nodes: List[ActionNode] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert telemetry to JSON-compatible dictionary."""
        return {
            "total_nodes": self.total_nodes,
            "total_dependencies": self.total_dependencies,
            "critical_path_node_count": self.critical_path_node_count,
            "critical_path_duration_minutes": self.critical_path_duration_minutes,
            "parallel_lanes_count": self.parallel_lanes_count,
            "immediately_executable_count": self.immediately_executable_count,
            "total_estimated_work_minutes": self.total_estimated_work_minutes,
            "dysfunction_bypass_ratio": round(self.dysfunction_bypass_ratio, 3),
            "critical_path_ids": self.critical_path_ids,
            "nodes": [n.to_dict() for n in self.nodes],
        }


class ActionSequencer:
    """Topological action dependency resolver and executive scaffolding engine."""

    def __init__(self, default_task_minutes: int = 25) -> None:
        self.default_task_minutes = default_task_minutes
        self.nodes: Dict[str, ActionNode] = {}
        self.raw_edges: List[Tuple[str, str]] = []

    def load_dict(self, task_data: Dict[str, Any]) -> None:
        """Load tasks and explicit prerequisites from dictionary."""
        self.nodes.clear()
        self.raw_edges.clear()

        for t_id, info in task_data.items():
            if isinstance(info, list):
                title = t_id
                prereqs = info
                est = self.default_task_minutes
                desc = ""
            elif isinstance(info, dict):
                title = info.get("title", t_id)
                prereqs = info.get("prerequisites", [])
                est = int(info.get("estimated_minutes", self.default_task_minutes))
                desc = info.get("description", "")
            else:
                title = str(info)
                prereqs = []
                est = self.default_task_minutes
                desc = ""

            self.nodes[t_id] = ActionNode(
                node_id=t_id,
                title=title,
                description=desc,
                estimated_minutes=max(5, est),
                prerequisites=list(prereqs),
            )
            for p in prereqs:
                self.raw_edges.append((p, t_id))

        self._build_dependents()

    def load_canvas(self, canvas_data: Dict[str, Any]) -> None:
        """Extract nodes, descriptions, and directional arrows from an Obsidian .canvas."""
        self.nodes.clear()
        self.raw_edges.clear()

        canvas_nodes = canvas_data.get("nodes", [])
        canvas_edges = canvas_data.get("edges", [])

        for node in canvas_nodes:
            n_id = str(node.get("id", ""))
            text = str(node.get("text", "")).strip()
            lines = [l.strip() for l in text.split("\n") if l.strip()]
            title = lines[0].lstrip("#").strip() if lines else n_id
            desc = "\n".join(lines[1:]) if len(lines) > 1 else ""

            # Extract potential minute estimate e.g. [30m] or (45 min)
            m = re.search(r"\[(\d+)\s*m(?:in)?\]|\((\d+)\s*m(?:in)?\)", text, re.IGNORECASE)
            est = int(m.group(1) or m.group(2)) if m else self.default_task_minutes

            self.nodes[n_id] = ActionNode(
                node_id=n_id,
                title=title,
                description=desc,
                estimated_minutes=max(5, est),
            )

        for edge in canvas_edges:
            from_node = str(edge.get("fromNode", ""))
            to_node = str(edge.get("toNode", ""))
            if from_node in self.nodes and to_node in self.nodes:
                self.nodes[to_node].prerequisites.append(from_node)
                self.raw_edges.append((from_node, to_node))

        self._build_dependents()

    def _build_dependents(self) -> None:
        """Sync forward dependent references from prerequisite lists."""
        for n in self.nodes.values():
            n.dependents.clear()
        for p, child in self.raw_edges:
            if p in self.nodes and child in self.nodes:
                if child not in self.nodes[p].dependents:
                    self.nodes[p].dependents.append(child)

    def sequence(self) -> Tuple[List[ActionNode], SequencingTelemetry]:
        """Execute Kahn's topological sort, Critical Path Method, and stepping stone synthesis."""
        if not self.nodes:
            empty_telemetry = SequencingTelemetry(
                total_nodes=0,
                total_dependencies=0,
                critical_path_node_count=0,
                critical_path_duration_minutes=0,
                parallel_lanes_count=0,
                immediately_executable_count=0,
                total_estimated_work_minutes=0,
                dysfunction_bypass_ratio=1.0,
            )
            return [], empty_telemetry

        # 1. Kahn's Topological Sort with cycle handling
        in_degree: Dict[str, int] = {n_id: len(n.prerequisites) for n_id, n in self.nodes.items()}
        zero_in_degree = [n_id for n_id, deg in in_degree.items() if deg == 0]
        sorted_order: List[str] = []

        lane_alloc: Dict[str, int] = {}
        current_lane = 0

        queue = list(zero_in_degree)
        for r_id in queue:
            lane_alloc[r_id] = current_lane
            current_lane += 1

        while queue:
            curr = queue.pop(0)
            sorted_order.append(curr)

            for dep_id in self.nodes[curr].dependents:
                in_degree[dep_id] -= 1
                if in_degree[dep_id] == 0:
                    queue.append(dep_id)
                    # Inherit or fork lane
                    parent_lane = lane_alloc.get(curr, 0)
                    lane_alloc[dep_id] = parent_lane

        # Handle any residual cycle nodes
        for n_id in self.nodes:
            if n_id not in sorted_order:
                sorted_order.append(n_id)
                lane_alloc[n_id] = current_lane
                current_lane += 1

        # Assign topological order and lanes
        for idx, n_id in enumerate(sorted_order):
            node = self.nodes[n_id]
            node.topological_order = idx + 1
            node.lane_id = lane_alloc.get(n_id, 0)
            node.status = TaskStatus.READY if not node.prerequisites else TaskStatus.BLOCKED

        # 2. Critical Path Method (CPM) Forward & Backward Pass
        # Forward pass: Earliest Start (ES) and Earliest Finish (EF)
        for n_id in sorted_order:
            node = self.nodes[n_id]
            if not node.prerequisites:
                node.earliest_start = 0
            else:
                max_prereq_ef = 0
                for p_id in node.prerequisites:
                    if p_id in self.nodes:
                        p_node = self.nodes[p_id]
                        p_ef = p_node.earliest_start + p_node.estimated_minutes
                        if p_ef > max_prereq_ef:
                            max_prereq_ef = p_ef
                node.earliest_start = max_prereq_ef

        # Maximum project completion duration
        project_duration = 0
        for node in self.nodes.values():
            ef = node.earliest_start + node.estimated_minutes
            if ef > project_duration:
                project_duration = ef

        # Backward pass: Latest Start (LS) and Slack
        for n_id in reversed(sorted_order):
            node = self.nodes[n_id]
            if not node.dependents:
                node.latest_start = project_duration - node.estimated_minutes
            else:
                min_dep_ls = project_duration
                for d_id in node.dependents:
                    if d_id in self.nodes:
                        d_node = self.nodes[d_id]
                        if d_node.latest_start < min_dep_ls:
                            min_dep_ls = d_node.latest_start
                node.latest_start = min_dep_ls - node.estimated_minutes

            node.slack_minutes = max(0, node.latest_start - node.earliest_start)
            node.is_critical_path = (node.slack_minutes == 0)

        # 3. Generate Micro-Commitment Stepping Stones for unblocked and critical tasks
        critical_nodes: List[ActionNode] = []
        for n_id in sorted_order:
            node = self.nodes[n_id]
            if node.is_critical_path:
                critical_nodes.append(node)
            self._synthesize_stepping_stones(node)

        critical_path_ids = [n.node_id for n in critical_nodes]
        ready_count = sum(1 for n in self.nodes.values() if n.status == TaskStatus.READY)
        total_work = sum(n.estimated_minutes for n in self.nodes.values())
        unique_lanes = len(set(n.lane_id for n in self.nodes.values()))

        # Dysfunction bypass ratio: ready micro-commitments vs total load
        stones_count = sum(len(n.stepping_stones) for n in self.nodes.values())
        bypass_ratio = min(1.0, stones_count / max(1, len(self.nodes) * 2))

        telemetry = SequencingTelemetry(
            total_nodes=len(self.nodes),
            total_dependencies=len(self.raw_edges),
            critical_path_node_count=len(critical_nodes),
            critical_path_duration_minutes=project_duration,
            parallel_lanes_count=unique_lanes,
            immediately_executable_count=ready_count,
            total_estimated_work_minutes=total_work,
            dysfunction_bypass_ratio=bypass_ratio,
            critical_path_ids=critical_path_ids,
            nodes=[self.nodes[n_id] for n_id in sorted_order],
        )

        return telemetry.nodes, telemetry

    def _synthesize_stepping_stones(self, node: ActionNode) -> None:
        """Create high-clarity sub-2-minute micro-actions to lower initiation barriers."""
        node.stepping_stones.clear()

        # Step 1: Physical environment / target anchor setup
        s1 = MicroSteppingStone(
            stone_id=f"{node.node_id}_s1",
            parent_node_id=node.node_id,
            action_prompt=f"Open workspace target for: {node.title}",
            target_duration_seconds=45,
            implementation_intention=f"When I sit down, I will open the file or canvas for '{node.title}' and read the top line.",
            sensory_anchor="Tactile keypress to focus editor tab",
        )

        # Step 2: Skeleton outline / scratch buffer
        s2 = MicroSteppingStone(
            stone_id=f"{node.node_id}_s2",
            parent_node_id=node.node_id,
            action_prompt="Draft a 3-bullet scratch outline",
            target_duration_seconds=90,
            implementation_intention="When the document is open, I will write exactly 3 bullet points without filtering.",
            sensory_anchor="Immediate visual bullet list appearance",
        )

        # Step 3: Low-friction initial sentence or code signature
        s3 = MicroSteppingStone(
            stone_id=f"{node.node_id}_s3",
            parent_node_id=node.node_id,
            action_prompt="Write the first functional sentence or stub",
            target_duration_seconds=120,
            implementation_intention="When the 3 bullets exist, I will expand the easiest bullet into one concrete line.",
            sensory_anchor="Cursor advancing past the starting line",
        )

        node.stepping_stones.extend([s1, s2, s3])

    def to_canvas(
        self,
        output_path: Optional[str] = None,
        canvas_title: str = "Action Sequence Runway",
    ) -> Dict[str, Any]:
        """Export sequenced topological DAG into an Obsidian .canvas layout."""
        nodes_list, telemetry = self.sequence()

        canvas_nodes: List[Dict[str, Any]] = []
        canvas_edges: List[Dict[str, Any]] = []

        # Horizontal runway layout: X advances with topological order, Y by lane
        x_spacing = 380
        y_spacing = 260
        base_x = 100
        base_y = 100

        for node in nodes_list:
            x = base_x + (node.topological_order - 1) * x_spacing
            y = base_y + node.lane_id * y_spacing

            # Color 1 (red) for critical path, 4 (green) for ready, 2 (orange) for blocked
            if node.is_critical_path and node.status == TaskStatus.READY:
                color = "1"
            elif node.status == TaskStatus.READY:
                color = "4"
            elif node.is_critical_path:
                color = "3"
            else:
                color = "2"

            status_badge = "[READY TO RUN]" if node.status == TaskStatus.READY else f"[WAITING: {len(node.prerequisites)} PREREQS]"
            crit_badge = "**[CRITICAL PATH]**\n" if node.is_critical_path else ""

            stones_text = "\n".join([f"- [ ] `{s.target_duration_seconds}s`: {s.action_prompt}" for s in node.stepping_stones])

            content = (
                f"### Step {node.topological_order}: {node.title}\n"
                f"{crit_badge}"
                f"**Status:** {status_badge} | **Est:** {node.estimated_minutes} min (Slack: {node.slack_minutes}m)\n\n"
                f"**Dysfunction Bypass Stepping Stones:**\n"
                f"{stones_text}"
            )

            canvas_nodes.append({
                "id": node.node_id,
                "x": x,
                "y": y,
                "width": 320,
                "height": 220,
                "type": "text",
                "text": content,
                "color": color,
            })

        # Connect edges
        edge_idx = 1
        for p_id, c_id in self.raw_edges:
            if p_id in self.nodes and c_id in self.nodes:
                p_node = self.nodes[p_id]
                c_node = self.nodes[c_id]
                is_crit_edge = p_node.is_critical_path and c_node.is_critical_path
                edge_color = "1" if is_crit_edge else "6"

                canvas_edges.append({
                    "id": f"seq_edge_{edge_idx}",
                    "fromNode": p_id,
                    "fromSide": "right",
                    "toNode": c_id,
                    "toSide": "left",
                    "label": "Critical Dependency" if is_crit_edge else "Prereq",
                    "color": edge_color,
                })
                edge_idx += 1

        canvas_json = {
            "title": canvas_title,
            "nodes": canvas_nodes,
            "edges": canvas_edges,
        }

        if output_path:
            p = Path(output_path)
            p.parent.mkdir(parents=True, exist_ok=True)
            with open(p, "w", encoding="utf-8") as f:
                json.dump(canvas_json, f, indent=2)

        return canvas_json

    def to_svg(
        self,
        output_path: Optional[str] = None,
        width: int = 1200,
        height: int = 700,
    ) -> str:
        """Render publication-grade SVG DAG with critical path highlighting and dark titanium theme."""
        nodes_list, telemetry = self.sequence()

        padding = 80
        total_steps = max(1, len(nodes_list))
        h_spacing = (width - 2 * padding) / total_steps
        v_spacing = 160

        coords: Dict[str, Tuple[float, float]] = {}
        for idx, node in enumerate(nodes_list):
            cx = padding + idx * h_spacing + (h_spacing / 2)
            cy = padding + 120 + (node.lane_id * v_spacing)
            coords[node.node_id] = (cx, cy)

        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
            f'width="{width}" height="{height}" style="background-color: #0B0F17; '
            f'font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif;">',
            '<defs>',
            '  <linearGradient id="cardGrad" x1="0" y1="0" x2="0" y2="1">',
            '    <stop offset="0%" stop-color="#1E293B" stop-opacity="0.95"/>',
            '    <stop offset="100%" stop-color="#0F172A" stop-opacity="0.95"/>',
            '  </linearGradient>',
            '  <linearGradient id="critEdge" x1="0" y1="0" x2="1" y2="0">',
            '    <stop offset="0%" stop-color="#EF4444"/>',
            '    <stop offset="100%" stop-color="#F59E0B"/>',
            '  </linearGradient>',
            '  <marker id="critArrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">',
            '    <path d="M 0 1 L 10 5 L 0 9 z" fill="#EF4444"/>',
            '  </marker>',
            '  <marker id="normArrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">',
            '    <path d="M 0 1 L 10 5 L 0 9 z" fill="#475569"/>',
            '  </marker>',
            '</defs>',
            '<!-- Header -->',
            f'<text x="{padding}" y="45" font-size="20" font-weight="700" fill="#F8FAFC">Executive Runway &amp; Critical Path Sequencer</text>',
            f'<text x="{padding}" y="65" font-size="12" fill="#94A3B8">Topological DAG: {telemetry.total_nodes} Tasks | {telemetry.critical_path_node_count} Critical ({telemetry.critical_path_duration_minutes} min runway) | {telemetry.immediately_executable_count} Unblocked</text>',
            '<!-- Dependency Edges -->',
        ]

        # Draw dependency arrows
        for p_id, c_id in self.raw_edges:
            if p_id in coords and c_id in coords:
                x1, y1 = coords[p_id]
                x2, y2 = coords[c_id]
                p_node = self.nodes[p_id]
                c_node = self.nodes[c_id]
                is_crit = p_node.is_critical_path and c_node.is_critical_path

                stroke_col = "url(#critEdge)" if is_crit else "#334155"
                stroke_w = "3" if is_crit else "1.5"
                dash_attr = "" if is_crit else 'stroke-dasharray="4,3"'
                marker = "url(#critArrow)" if is_crit else "url(#normArrow)"

                svg_parts.append(
                    f'<line x1="{x1 + 65:.1f}" y1="{y1:.1f}" x2="{x2 - 65:.1f}" y2="{y2:.1f}" '
                    f'stroke="{stroke_col}" stroke-width="{stroke_w}" {dash_attr} marker-end="{marker}"/>'
                )

        # Draw Task Cards
        svg_parts.append('<!-- Action Cards -->')
        card_w = 140
        card_h = 75

        for node in nodes_list:
            if node.node_id in coords:
                cx, cy = coords[node.node_id]
                rx = cx - card_w / 2
                ry = cy - card_h / 2

                if node.is_critical_path:
                    stroke_color = "#EF4444"
                elif node.status == TaskStatus.READY:
                    stroke_color = "#10B981"
                else:
                    stroke_color = "#334155"

                title_clean = (node.title[:16] + "..") if len(node.title) > 18 else node.title

                svg_parts.append(
                    f'<rect x="{rx:.1f}" y="{ry:.1f}" width="{card_w}" height="{card_h}" rx="8" '
                    f'fill="url(#cardGrad)" stroke="{stroke_color}" stroke-width="2"/>'
                )
                svg_parts.append(
                    f'<text x="{rx + 8:.1f}" y="{ry + 20:.1f}" font-size="11" font-weight="700" fill="#F8FAFC">Step {node.topological_order}</text>'
                )
                svg_parts.append(
                    f'<text x="{rx + 8:.1f}" y="{ry + 38:.1f}" font-size="10" font-weight="600" fill="#E2E8F0">{title_clean}</text>'
                )
                svg_parts.append(
                    f'<text x="{rx + 8:.1f}" y="{ry + 56:.1f}" font-size="9" fill="#94A3B8">{node.estimated_minutes}m (Slack: {node.slack_minutes}m)</text>'
                )

        # Telemetry Legend
        legend_x = width - 260
        legend_y = height - 135
        svg_parts.append('<!-- Telemetry Legend -->')
        svg_parts.append(
            f'<rect x="{legend_x}" y="{legend_y}" width="230" height="105" rx="6" '
            f'fill="#0F172A" stroke="#1E293B" stroke-width="1"/>'
        )
        svg_parts.append(
            f'<text x="{legend_x + 12}" y="{legend_y + 20}" font-size="11" font-weight="700" fill="#F8FAFC">Executive Scaffolding Metrics</text>'
        )
        svg_parts.append(
            f'<text x="{legend_x + 12}" y="{legend_y + 40}" font-size="10" fill="#64748B">Critical Runway: <tspan fill="#EF4444">{telemetry.critical_path_duration_minutes} min</tspan></text>'
        )
        svg_parts.append(
            f'<text x="{legend_x + 12}" y="{legend_y + 58}" font-size="10" fill="#64748B">Unblocked Actions: <tspan fill="#10B981">{telemetry.immediately_executable_count}</tspan></text>'
        )
        svg_parts.append(
            f'<text x="{legend_x + 12}" y="{legend_y + 76}" font-size="10" fill="#64748B">Dysfunction Bypass: <tspan fill="#38BDF8">{telemetry.dysfunction_bypass_ratio:.1%}</tspan></text>'
        )
        svg_parts.append(
            f'<text x="{legend_x + 12}" y="{legend_y + 94}" font-size="9" fill="#475569">Barkley &amp; Fogg Micro-Commitments</text>'
        )

        svg_parts.append('</svg>')
        svg_content = "\n".join(svg_parts)

        if output_path:
            p = Path(output_path)
            p.parent.mkdir(parents=True, exist_ok=True)
            with open(p, "w", encoding="utf-8") as f:
                f.write(svg_content)

        return svg_content

    def render_ascii_plan(self, telemetry: SequencingTelemetry) -> str:
        """Format an accessible ASCII execution runway for the terminal."""
        lines = [
            "=" * 68,
            "  Executive Action Sequence Runway & Critical Path DAG",
            "=" * 68,
            f"  Total Tasks:              {telemetry.total_nodes}",
            f"  Total Dependencies:       {telemetry.total_dependencies}",
            f"  Critical Path Runway:     {telemetry.critical_path_duration_minutes} minutes ({telemetry.critical_path_node_count} tasks)",
            f"  Immediately Unblocked:    {telemetry.immediately_executable_count} tasks",
            f"  Total Estimated Work:     {telemetry.total_estimated_work_minutes} minutes",
            f"  Dysfunction Bypass Ratio: {telemetry.dysfunction_bypass_ratio:.1%}",
            "-" * 68,
            "  Topological Execution Order:",
        ]

        for node in telemetry.nodes:
            crit_mark = "[CRITICAL]" if node.is_critical_path else "[FLEX]"
            status_mark = "[READY]" if node.status == TaskStatus.READY else "[BLOCKED]"
            lines.append(f"    Step {node.topological_order}: {crit_mark} {status_mark} {node.title} ({node.estimated_minutes}m, Slack: {node.slack_minutes}m)")
            if node.status == TaskStatus.READY and node.stepping_stones:
                s = node.stepping_stones[0]
                lines.append(f"      -> Micro-Commitment ({s.target_duration_seconds}s): {s.action_prompt}")
                lines.append(f"         Intent: {s.implementation_intention}")

        lines.append("=" * 68)
        return "\n".join(lines)
