"""Autonomous Cognitive Spatial Working Memory Anchor Stacking & Compaction Harness.

Theoretical Foundation:
- Cowan's Embedded-Processes Model (Cowan, 2001) & Working Memory Span:
  Human focal working memory is restricted to 3-5 concurrent structural chunks.
  During deep problem solving, uncompacted sub-canvases saturate attention channels,
  inducing cognitive fatigue and loss of high-level situational awareness.
- Real-Time Semantic Stack Compaction:
  Condenses resolved and inactive subgraphs into hierarchical memory tokens.
  Preserves core invariants, decision rationales, and interface contracts while
  collapsing extensive visual clutter into single allocentric cognitive anchors.
- Multi-Scale Spatial Breadcrumb Trails:
  Supplies an orientation coordinate trail across hierarchical zoom levels.
  Enables instantaneous context restoration when traversing between broad
  system architecture and granular implementation leaves.
- Dark Titanium SVG & Obsidian .canvas Integration:
  Outputs balanced canvas layouts with tokenized stack cards and generates
  publication-grade SVG visualizations illustrating compaction metrics and
  hierarchical navigation ribbons.

Strict Quality Gate: Zero em dashes anywhere (use hyphens, commas, or parentheses).
"""

from __future__ import annotations

import enum
import json
import math
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


class StackStatus(str, enum.Enum):
    """Execution and lifecycle status of a cognitive stack layer."""

    RESOLVED = "resolved"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    ARCHIVED = "archived"


@dataclass
class MemoryToken:
    """Compact cognitive representation of a collapsed or resolved subgraph."""

    token_id: str
    subgraph_title: str
    status: StackStatus
    original_node_count: int
    compaction_ratio: float
    key_insights: List[str]
    depth_level: int
    parent_token_id: Optional[str] = None
    x: float = 0.0
    y: float = 0.0
    width: float = 280.0
    height: float = 160.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert memory token to serializable dictionary."""
        return {
            "token_id": self.token_id,
            "subgraph_title": self.subgraph_title,
            "status": self.status.value,
            "original_node_count": self.original_node_count,
            "compaction_ratio": round(self.compaction_ratio, 2),
            "key_insights": self.key_insights,
            "depth_level": self.depth_level,
            "parent_token_id": self.parent_token_id,
            "x": round(self.x, 1),
            "y": round(self.y, 1),
            "width": round(self.width, 1),
            "height": round(self.height, 1),
        }


@dataclass
class SpatialBreadcrumb:
    """Spatial navigation waypoint maintaining mental orientation across zoom depth."""

    breadcrumb_id: str
    label: str
    depth: int
    focus_x: float
    focus_y: float
    zoom_scale: float

    def to_dict(self) -> Dict[str, Any]:
        """Convert breadcrumb to serializable dictionary."""
        return {
            "breadcrumb_id": self.breadcrumb_id,
            "label": self.label,
            "depth": self.depth,
            "focus_x": round(self.focus_x, 1),
            "focus_y": round(self.focus_y, 1),
            "zoom_scale": round(self.zoom_scale, 2),
        }


@dataclass
class AnchorStackTelemetry:
    """Telemetry capturing working memory load reduction and stack compaction metrics."""

    total_input_nodes: int
    compacted_tokens_count: int
    memory_load_reduction_pct: float
    max_stack_depth: int
    active_working_memory_slots: int
    tokens: List[MemoryToken] = field(default_factory=list)
    breadcrumbs: List[SpatialBreadcrumb] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert telemetry to JSON-compatible dictionary."""
        return {
            "total_input_nodes": self.total_input_nodes,
            "compacted_tokens_count": self.compacted_tokens_count,
            "memory_load_reduction_pct": round(self.memory_load_reduction_pct, 1),
            "max_stack_depth": self.max_stack_depth,
            "active_working_memory_slots": self.active_working_memory_slots,
            "tokens": [t.to_dict() for t in self.tokens],
            "breadcrumbs": [b.to_dict() for b in self.breadcrumbs],
        }


class AnchorStackCompactor:
    """Manages working memory compaction and multi-scale breadcrumb orientation."""

    def __init__(self, max_working_memory_capacity: int = 4) -> None:
        self.max_working_memory_capacity = max_working_memory_capacity
        self.raw_subgraphs: Dict[str, Dict[str, Any]] = {}
        self.raw_edges: List[Dict[str, Any]] = []

    def load_dict(self, stack_data: Dict[str, Any]) -> None:
        """Load subgraphs and tasks from dictionary configuration."""
        self.raw_subgraphs.clear()
        self.raw_edges.clear()

        subgraphs = stack_data.get("subgraphs", stack_data)
        for sg_id, info in subgraphs.items():
            if isinstance(info, dict):
                self.raw_subgraphs[sg_id] = {
                    "title": info.get("title", sg_id),
                    "status": info.get("status", "active"),
                    "nodes": list(info.get("nodes", [info.get("title", sg_id)])),
                    "insights": list(info.get("insights", [])),
                    "depth": int(info.get("depth", 0)),
                    "parent": info.get("parent"),
                    "x": float(info.get("x", 0.0)),
                    "y": float(info.get("y", 0.0)),
                }
            else:
                self.raw_subgraphs[sg_id] = {
                    "title": str(info),
                    "status": "active",
                    "nodes": [str(info)],
                    "insights": [],
                    "depth": 0,
                    "parent": None,
                    "x": 0.0,
                    "y": 0.0,
                }

        if "edges" in stack_data:
            self.raw_edges = list(stack_data.get("edges", []))

    def load_canvas(self, canvas_data: Dict[str, Any]) -> None:
        """Extract grouped clusters and nodes from Obsidian .canvas format."""
        self.raw_subgraphs.clear()
        self.raw_edges = list(canvas_data.get("edges", []))

        nodes = canvas_data.get("nodes", [])
        groups: Dict[str, Dict[str, Any]] = {}
        loose_nodes: List[Dict[str, Any]] = []

        for node in nodes:
            node_type = node.get("type", "text")
            if node_type == "group":
                g_id = str(node.get("id", ""))
                groups[g_id] = {
                    "title": str(node.get("label", g_id)),
                    "status": "resolved" if "resolved" in str(node.get("label", "")).lower() else "active",
                    "nodes": [],
                    "insights": [],
                    "depth": 0,
                    "parent": None,
                    "x": float(node.get("x", 0.0)),
                    "y": float(node.get("y", 0.0)),
                }
            else:
                loose_nodes.append(node)

        # Place loose nodes into groups if coordinates lie within group boundaries
        for item in loose_nodes:
            item_x = float(item.get("x", 0.0))
            item_y = float(item.get("y", 0.0))
            item_text = str(item.get("text", "")).strip()
            title = item_text.split("\n")[0].lstrip("#").strip() if item_text else str(item.get("id", ""))

            assigned = False
            for g_id, g_info in groups.items():
                gx = g_info["x"]
                gy = g_info["y"]
                # Approximate bounding check
                if abs(item_x - gx) < 600 and abs(item_y - gy) < 400:
                    g_info["nodes"].append(title)
                    assigned = True
                    break

            if not assigned:
                sg_id = str(item.get("id", f"loose_{len(self.raw_subgraphs)}"))
                self.raw_subgraphs[sg_id] = {
                    "title": title,
                    "status": "active",
                    "nodes": [title],
                    "insights": [],
                    "depth": 0,
                    "parent": None,
                    "x": item_x,
                    "y": item_y,
                }

        self.raw_subgraphs.update(groups)

    def compact_stack(self) -> Tuple[List[MemoryToken], List[SpatialBreadcrumb], AnchorStackTelemetry]:
        """Condense resolved subgraphs into hierarchical memory tokens and build breadcrumbs."""
        if not self.raw_subgraphs:
            empty_telemetry = AnchorStackTelemetry(
                total_input_nodes=0,
                compacted_tokens_count=0,
                memory_load_reduction_pct=0.0,
                max_stack_depth=0,
                active_working_memory_slots=0,
            )
            return [], [], empty_telemetry

        tokens: List[MemoryToken] = []
        breadcrumbs: List[SpatialBreadcrumb] = []
        total_input_nodes = 0
        active_slots = 0
        max_depth = 0

        # Sort subgraphs by depth and status
        sorted_keys = sorted(
            self.raw_subgraphs.keys(),
            key=lambda k: (self.raw_subgraphs[k].get("depth", 0), self.raw_subgraphs[k].get("status", "active"))
        )

        x_stride = 320.0
        y_stride = 200.0

        for idx, sg_id in enumerate(sorted_keys):
            info = self.raw_subgraphs[sg_id]
            title = info.get("title", sg_id)
            raw_status = str(info.get("status", "active")).lower()
            status = (
                StackStatus.RESOLVED if "resolved" in raw_status else (
                    StackStatus.ARCHIVED if "archive" in raw_status else (
                        StackStatus.SUSPENDED if "suspend" in raw_status else StackStatus.ACTIVE
                    )
                )
            )
            node_items = list(info.get("nodes", [title]))
            count = len(node_items)
            total_input_nodes += count

            depth = int(info.get("depth", 0))
            if depth > max_depth:
                max_depth = depth

            # Compaction ratio: 1 token for N items
            compaction_ratio = max(1.0, float(count))

            # Synthesize key insights if not provided
            insights = list(info.get("insights", []))
            if not insights:
                if status == StackStatus.RESOLVED:
                    insights.append(f"Sub-system consensus stabilized ({count} nodes condensed)")
                elif status == StackStatus.ACTIVE:
                    insights.append(f"In-flight focus locus ({count} active components)")
                else:
                    insights.append(f"Suspended execution context ({count} deferred items)")

            col = idx % 3
            row = idx // 3
            pos_x = info.get("x", 0.0) or (80.0 + col * x_stride)
            pos_y = info.get("y", 0.0) or (140.0 + row * y_stride)

            token = MemoryToken(
                token_id=sg_id,
                subgraph_title=title,
                status=status,
                original_node_count=count,
                compaction_ratio=compaction_ratio,
                key_insights=insights,
                depth_level=depth,
                parent_token_id=info.get("parent"),
                x=pos_x,
                y=pos_y,
            )
            tokens.append(token)

            if status == StackStatus.ACTIVE:
                active_slots += 1

            # Build spatial breadcrumb entry
            zoom = max(0.4, 1.0 - (depth * 0.15))
            breadcrumbs.append(
                SpatialBreadcrumb(
                    breadcrumb_id=f"bc_{sg_id}",
                    label=title[:24],
                    depth=depth,
                    focus_x=pos_x,
                    focus_y=pos_y,
                    zoom_scale=zoom,
                )
            )

        # Sort breadcrumbs strictly by hierarchy depth
        breadcrumbs.sort(key=lambda b: b.depth)

        compacted_tokens_count = len(tokens)
        reduction_pct = max(0.0, ((total_input_nodes - compacted_tokens_count) / max(1, total_input_nodes))) * 100.0

        telemetry = AnchorStackTelemetry(
            total_input_nodes=total_input_nodes,
            compacted_tokens_count=compacted_tokens_count,
            memory_load_reduction_pct=reduction_pct,
            max_stack_depth=max_depth,
            active_working_memory_slots=active_slots,
            tokens=tokens,
            breadcrumbs=breadcrumbs,
        )

        return tokens, breadcrumbs, telemetry

    def to_canvas(
        self,
        output_path: Optional[str] = None,
        canvas_title: str = "Compacted Anchor Stack Canvas",
    ) -> Dict[str, Any]:
        """Export compacted memory tokens to Obsidian .canvas structure."""
        tokens, breadcrumbs, telemetry = self.compact_stack()

        canvas_nodes: List[Dict[str, Any]] = []

        # Color mapping by status
        for t in tokens:
            if t.status == StackStatus.RESOLVED:
                color = "4"  # Green
            elif t.status == StackStatus.ACTIVE:
                color = "5"  # Cyan / Blue
            elif t.status == StackStatus.SUSPENDED:
                color = "3"  # Yellow / Amber
            else:
                color = "0"  # Gray / Archived

            insights_text = "\n".join(f"- {i}" for i in t.key_insights[:2])
            content = (
                f"### {t.subgraph_title} [{t.status.value.upper()}]\n"
                f"**Tokens Compacted:** {t.original_node_count} nodes (ratio {t.compaction_ratio:.1f}x)\n"
                f"**Stack Depth:** Layer {t.depth_level}\n"
                f"{insights_text}"
            )

            canvas_nodes.append({
                "id": t.token_id,
                "x": t.x,
                "y": t.y,
                "width": t.width,
                "height": t.height,
                "type": "text",
                "text": content,
                "color": color,
            })

        # Add breadcrumb banner card at the top
        bc_chain = " > ".join(b.label for b in breadcrumbs[:6])
        canvas_nodes.append({
            "id": "breadcrumb_ribbon",
            "x": 80.0,
            "y": 40.0,
            "width": 920.0,
            "height": 70.0,
            "type": "text",
            "text": f"## Spatial Navigation Breadcrumb\n`{bc_chain}`\n*Load Reduction: {telemetry.memory_load_reduction_pct:.1f}% | Active Slots: {telemetry.active_working_memory_slots}/{self.max_working_memory_capacity}*",
            "color": "6",  # Purple
        })

        canvas_json = {
            "title": canvas_title,
            "nodes": canvas_nodes,
            "edges": self.raw_edges,
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
        height: int = 800,
    ) -> str:
        """Render publication-grade SVG memory anchor stack in dark titanium theme."""
        tokens, breadcrumbs, telemetry = self.compact_stack()

        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
            f'width="{width}" height="{height}" style="background-color: #0B0F17; '
            f'font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif;">',
            '<defs>',
            '  <filter id="stackShadow" x="-10%" y="-10%" width="120%" height="120%">',
            '    <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#000000" flood-opacity="0.6"/>',
            '  </filter>',
            '</defs>',
            '<!-- Header -->',
            f'<text x="60" y="45" font-size="20" font-weight="700" fill="#F8FAFC">Spatial Working Memory Anchor Stacking &amp; Compaction Harness</text>',
            f'<text x="60" y="65" font-size="12" fill="#94A3B8">Working Memory Relief: -{telemetry.memory_load_reduction_pct:.1f}% | Active Slots: {telemetry.active_working_memory_slots}/{self.max_working_memory_capacity} | Max Stack Depth: {telemetry.max_stack_depth}</text>',
            '<!-- Breadcrumb Ribbon -->',
        ]

        # Render Breadcrumb Waypoint Ribbon
        ribbon_y = 85
        svg_parts.append(f'<rect x="60" y="{ribbon_y}" width="1080" height="34" rx="6" fill="#1E293B" stroke="#334155" stroke-width="1"/>')
        bc_x = 75
        for i, bc in enumerate(breadcrumbs[:6]):
            svg_parts.append(
                f'<rect x="{bc_x}" y="{ribbon_y + 6}" width="120" height="22" rx="4" fill="#0F172A" stroke="#38BDF8" stroke-width="1"/>'
            )
            svg_parts.append(
                f'<text x="{bc_x + 60}" y="{ribbon_y + 20}" font-size="10" font-weight="600" fill="#E2E8F0" text-anchor="middle">{bc.label[:14]}</text>'
            )
            bc_x += 130
            if i < len(breadcrumbs[:6]) - 1:
                svg_parts.append(
                    f'<text x="{bc_x - 6}" y="{ribbon_y + 20}" font-size="11" fill="#64748B">&gt;</text>'
                )

        # Render Memory Tokens
        svg_parts.append('<!-- Compacted Memory Tokens -->')
        for t in tokens:
            if t.status == StackStatus.RESOLVED:
                stroke_col = "#10B981"
                badge_bg = "#064E3B"
                badge_text = "#6EE7B7"
            elif t.status == StackStatus.ACTIVE:
                stroke_col = "#38BDF8"
                badge_bg = "#082F49"
                badge_text = "#7DD3FC"
            elif t.status == StackStatus.SUSPENDED:
                stroke_col = "#F59E0B"
                badge_bg = "#451A03"
                badge_text = "#FCD34D"
            else:
                stroke_col = "#64748B"
                badge_bg = "#1E293B"
                badge_text = "#94A3B8"

            svg_parts.append(
                f'<g transform="translate({t.x:.1f}, {t.y:.1f})" filter="url(#stackShadow)">'
                f'  <rect width="{t.width:.1f}" height="{t.height:.1f}" rx="8" fill="#1E293B" stroke="{stroke_col}" stroke-width="2"/>'
                f'  <rect x="14" y="14" width="70" height="18" rx="4" fill="{badge_bg}"/>'
                f'  <text x="49" y="26" font-size="9" font-weight="700" fill="{badge_text}" text-anchor="middle">{t.status.value.upper()}</text>'
                f'  <text x="92" y="27" font-size="12" font-weight="700" fill="#F8FAFC">{t.subgraph_title[:16]}</text>'
                f'  <line x1="14" y1="40" x2="{t.width - 14:.1f}" y2="40" stroke="#334155" stroke-width="1"/>'
                f'  <text x="14" y="58" font-size="10" fill="#94A3B8">Compacted: <tspan fill="{stroke_col}">{t.original_node_count} nodes</tspan> ({t.compaction_ratio:.1f}x)</text>'
                f'  <text x="14" y="74" font-size="9" fill="#64748B">Stack Depth: Layer {t.depth_level}</text>'
            )

            if t.key_insights:
                insight_snip = t.key_insights[0][:30]
                svg_parts.append(
                    f'  <text x="14" y="98" font-size="9" fill="#E2E8F0">&bull; {insight_snip}</text>'
                )

            svg_parts.append('</g>')

        # Telemetry Box
        legend_x = width - 260
        legend_y = height - 145
        svg_parts.append('<!-- Telemetry Legend -->')
        svg_parts.append(
            f'<rect x="{legend_x}" y="{legend_y}" width="230" height="115" rx="6" '
            f'fill="#0F172A" stroke="#1E293B" stroke-width="1"/>'
        )
        svg_parts.append(
            f'<text x="{legend_x + 12}" y="{legend_y + 22}" font-size="11" font-weight="700" fill="#F8FAFC">Anchor Stack Telemetry</text>'
        )
        svg_parts.append(
            f'<text x="{legend_x + 12}" y="{legend_y + 42}" font-size="10" fill="#64748B">Nodes Condensed: <tspan fill="#F8FAFC">{telemetry.total_input_nodes} &rarr; {telemetry.compacted_tokens_count}</tspan></text>'
        )
        svg_parts.append(
            f'<text x="{legend_x + 12}" y="{legend_y + 60}" font-size="10" fill="#64748B">Memory Relief: <tspan fill="#10B981">-{telemetry.memory_load_reduction_pct:.1f}%</tspan></text>'
        )
        svg_parts.append(
            f'<text x="{legend_x + 12}" y="{legend_y + 78}" font-size="10" fill="#64748B">Active Slots: <tspan fill="#38BDF8">{telemetry.active_working_memory_slots}/{self.max_working_memory_capacity}</tspan></text>'
        )
        svg_parts.append(
            f'<text x="{legend_x + 12}" y="{legend_y + 98}" font-size="9" fill="#475569">Cowan Bounds &amp; Breadcrumb Trail</text>'
        )

        svg_parts.append('</svg>')
        svg_content = "\n".join(svg_parts)

        if output_path:
            p = Path(output_path)
            p.parent.mkdir(parents=True, exist_ok=True)
            with open(p, "w", encoding="utf-8") as f:
                f.write(svg_content)

        return svg_content

    def render_ascii_stack(self, telemetry: AnchorStackTelemetry) -> str:
        """Format an accessible ASCII summary of the anchor stack and breadcrumb trail."""
        lines = [
            "=" * 68,
            "  Spatial Working Memory Anchor Stacking & Compaction Report",
            "=" * 68,
            f"  Total Subgraph Items:         {telemetry.total_input_nodes}",
            f"  Compacted Memory Tokens:      {telemetry.compacted_tokens_count}",
            f"  Memory Load Reduction:        -{telemetry.memory_load_reduction_pct:.1f}%",
            f"  Active Working Memory Slots:  {telemetry.active_working_memory_slots}/{self.max_working_memory_capacity}",
            f"  Max Stack Hierarchy Depth:    {telemetry.max_stack_depth}",
            "-" * 68,
            "  [SPATIAL BREADCRUMB TRAIL]:",
        ]

        for b in telemetry.breadcrumbs:
            indent = "    " + ("  " * b.depth)
            lines.append(f"{indent}> [L{b.depth}] {b.label} (Zoom: {b.zoom_scale:.2f}x at {b.focus_x:.0f}, {b.focus_y:.0f})")

        if telemetry.tokens:
            lines.append("-" * 68)
            lines.append("  [COMPACTED TOKEN INVENTORY]:")
            for t in telemetry.tokens:
                lines.append(f"    * [{t.status.value.upper()}] {t.subgraph_title}: {t.original_node_count} nodes ({t.compaction_ratio:.1f}x)")
                if t.key_insights:
                    lines.append(f"      Insight: {t.key_insights[0]}")

        lines.append("=" * 68)
        return "\n".join(lines)
