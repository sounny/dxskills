"""
Autonomous Cognitive Spatial Working Memory Anchor Eviction and FIFO Buffer Compactor for DxSkills.

Grounded in:
- Eide and Eide M-I-N-D spatial framework (spatial clarity without visual residue clutter)
- Sweller Cognitive Load Theory (eliminating working memory split-attention from dormant tokens)
- Baddeley Working Memory Model (FIFO decay modeling and automated long-term storage offloading)
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional


@dataclass
class WorkingMemoryNode:
    """An active cognitive node residing within spatial working memory."""
    id: str
    label: str
    base_importance: float  # 1.0 to 10.0
    idle_minutes: float
    reference_count: int = 0
    decay_rate: float = 0.08

    def calculate_saliency(self) -> float:
        """
        Calculate dynamic cognitive saliency using exponential temporal decay.
        """
        # S = B * e^(-lambda * t) * (1 + 0.25 * ref_count)
        time_factor = math.exp(-self.decay_rate * self.idle_minutes)
        ref_boost = 1.0 + (0.25 * min(4, self.reference_count))
        raw_saliency = self.base_importance * time_factor * ref_boost
        return round(max(0.1, min(10.0, raw_saliency)), 2)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["saliency"] = self.calculate_saliency()
        return d


@dataclass
class CompactionAudit:
    """Telemetry report produced following working memory compaction."""
    initial_node_count: int
    retained_node_count: int
    compacted_node_count: int
    buffer_capacity_limit: int
    initial_memory_load: float
    compacted_memory_load: float
    headroom_gain_pct: float
    retained_nodes: List[WorkingMemoryNode]
    compacted_nodes: List[WorkingMemoryNode]
    archive_summary_label: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "initial_node_count": self.initial_node_count,
            "retained_node_count": self.retained_node_count,
            "compacted_node_count": self.compacted_node_count,
            "buffer_capacity_limit": self.buffer_capacity_limit,
            "initial_memory_load": self.initial_memory_load,
            "compacted_memory_load": self.compacted_memory_load,
            "headroom_gain_pct": self.headroom_gain_pct,
            "retained_nodes": [n.to_dict() for n in self.retained_nodes],
            "compacted_nodes": [n.to_dict() for n in self.compacted_nodes],
            "archive_summary_label": self.archive_summary_label,
        }


class MemoryBufferCompactor:
    """
    Monitors spatial canvas nodes, calculates decay saliency, and compacts
    dormant nodes exceeding Cowan working memory capacity into deep storage.
    """

    def __init__(self, capacity_limit: int = 5) -> None:
        self.capacity_limit = capacity_limit

    def compact_buffer(
        self,
        nodes: List[WorkingMemoryNode],
        archive_name: str = "Deep Storage Archive",
    ) -> CompactionAudit:
        """
        Sort nodes by dynamic saliency and compact low-saliency nodes beyond buffer capacity.
        """
        if not nodes:
            return CompactionAudit(
                initial_node_count=0,
                retained_node_count=0,
                compacted_node_count=0,
                buffer_capacity_limit=self.capacity_limit,
                initial_memory_load=0.0,
                compacted_memory_load=0.0,
                headroom_gain_pct=0.0,
                retained_nodes=[],
                compacted_nodes=[],
                archive_summary_label=archive_name,
            )

        # Calculate initial load
        initial_load = sum(n.calculate_saliency() for n in nodes)

        # Sort by saliency descending
        sorted_nodes = sorted(nodes, key=lambda n: n.calculate_saliency(), reverse=True)

        # Retain top N nodes up to capacity limit
        retained = sorted_nodes[: self.capacity_limit]
        compacted = sorted_nodes[self.capacity_limit :]

        compacted_load = sum(n.calculate_saliency() for n in retained)
        gain_pct = round(((initial_load - compacted_load) / initial_load) * 100.0, 1) if initial_load > 0 else 0.0

        return CompactionAudit(
            initial_node_count=len(nodes),
            retained_node_count=len(retained),
            compacted_node_count=len(compacted),
            buffer_capacity_limit=self.capacity_limit,
            initial_memory_load=round(initial_load, 1),
            compacted_memory_load=round(compacted_load, 1),
            headroom_gain_pct=gain_pct,
            retained_nodes=retained,
            compacted_nodes=compacted,
            archive_summary_label=archive_name,
        )

    def export_canvas(
        self,
        audit: CompactionAudit,
        output_path: str = "compacted_buffer.canvas",
    ) -> Dict[str, Any]:
        """
        Export decluttered canvas retaining active nodes and linking a consolidated deep storage node.
        """
        nodes = []
        edges = []

        # Retained active nodes arranged horizontally
        spacing = 300
        start_x = -((len(audit.retained_nodes) - 1) * spacing) // 2

        for i, n in enumerate(audit.retained_nodes):
            nid = f"node-active-{n.id}"
            nodes.append({
                "id": nid,
                "x": start_x + (i * spacing),
                "y": 0,
                "width": 260,
                "height": 130,
                "type": "text",
                "text": (
                    f"**[Active Node]** {n.label}\n\n"
                    f"- Saliency: {n.calculate_saliency()}/10\n"
                    f"- Idle: {n.idle_minutes}m | Refs: {n.reference_count}"
                ),
                "color": "4",
            })

        # Compacted Archive Node placed beneath active nodes
        if audit.compacted_nodes:
            archive_id = "node-archive-compacted"
            archived_labels = "\n".join([f"- {cn.label} (saliency: {cn.calculate_saliency()})" for cn in audit.compacted_nodes])
            nodes.append({
                "id": archive_id,
                "x": -180,
                "y": 240,
                "width": 360,
                "height": 180,
                "type": "text",
                "text": (
                    f"### [{audit.archive_summary_label}]\n\n"
                    f"**Compacted Elements ({len(audit.compacted_nodes)}):**\n"
                    f"{archived_labels}\n\n"
                    f"*Headroom Gained: +{audit.headroom_gain_pct}%*"
                ),
                "color": "6",
            })

            # Connect primary active node to archive
            if audit.retained_nodes:
                prime_id = f"node-active-{audit.retained_nodes[0].id}"
                edges.append({
                    "id": "edge-active-archive",
                    "fromNode": prime_id,
                    "fromSide": "bottom",
                    "toNode": archive_id,
                    "toSide": "top",
                    "label": "Deep Storage Compaction",
                })

        canvas_data = {"nodes": nodes, "edges": edges}

        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(canvas_data, f, indent=2)

        return canvas_data

    def export_svg_telemetry(
        self,
        audit: CompactionAudit,
        width: int = 560,
        height: int = 340,
    ) -> str:
        """
        Export modern vector SVG visualizer of memory headroom and compaction distribution.
        """
        init_l = audit.initial_memory_load or 1.0
        comp_l = audit.compacted_memory_load
        gain = audit.headroom_gain_pct

        svg = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="auto">',
            '  <defs>',
            '    <linearGradient id="bgGradCompactor" x1="0%" y1="0%" x2="100%" y2="100%">',
            '      <stop offset="0%" stop-color="#0c1322" />',
            '      <stop offset="100%" stop-color="#192438" />',
            '    </linearGradient>',
            '    <linearGradient id="activeGrad" x1="0%" y1="0%" x2="100%" y2="0%">',
            '      <stop offset="0%" stop-color="#38bdf8" />',
            '      <stop offset="100%" stop-color="#0ea5e9" />',
            '    </linearGradient>',
            '  </defs>',
            f'  <rect width="{width}" height="{height}" rx="14" fill="url(#bgGradCompactor)" stroke="#334155" stroke-width="1.5" />',
            f'  <text x="24" y="36" fill="#f8fafc" font-family="system-ui, -apple-system, sans-serif" font-size="16" font-weight="bold">Working Memory FIFO Buffer Compactor</text>',
            f'  <text x="24" y="58" fill="#94a3b8" font-family="system-ui, -apple-system, sans-serif" font-size="12">Buffer Limit: {audit.buffer_capacity_limit} Slots | Headroom Freed: +{gain}%</text>',
            '  <!-- Node Slot Visualizer -->',
            '  <g transform="translate(30, 95)">',
            f'    <text x="0" y="0" fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="13" font-weight="600">Active Buffer Slots ({audit.retained_node_count}/{audit.buffer_capacity_limit})</text>',
        ]

        # Draw slot boxes
        slot_w = 42
        for s in range(audit.buffer_capacity_limit):
            filled = s < audit.retained_node_count
            fill_color = "url(#activeGrad)" if filled else "#1e293b"
            stroke_color = "#38bdf8" if filled else "#475569"
            sx = s * (slot_w + 10)
            svg.append(
                f'    <rect x="{sx}" y="15" width="{slot_w}" height="40" rx="8" fill="{fill_color}" stroke="{stroke_color}" stroke-width="1.5" />'
            )
            svg.append(
                f'    <text x="{sx + 21}" y="40" fill="{"#0f172a" if filled else "#64748b"}" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" text-anchor="middle">{s + 1}</text>'
            )

        svg.extend([
            f'    <text x="0" y="85" fill="#f43f5e" font-family="system-ui, sans-serif" font-size="12">Compacted into Deep Storage: {audit.compacted_node_count} nodes</text>',
            '  </g>',
            '  <!-- Memory Load Differential Bars -->',
            '  <g transform="translate(30, 215)">',
            f'    <text x="0" y="0" fill="#f43f5e" font-family="system-ui, sans-serif" font-size="12">Pre-Compaction Load: {init_l} pts ({audit.initial_node_count} nodes)</text>',
            '    <rect x="0" y="10" width="480" height="10" rx="5" fill="#1e293b" />',
            '    <rect x="0" y="10" width="480" height="10" rx="5" fill="#f43f5e" opacity="0.85" />',
            f'    <text x="0" y="42" fill="#38bdf8" font-family="system-ui, sans-serif" font-size="12">Post-Compaction Load: {comp_l} pts ({audit.retained_node_count} nodes)</text>',
            '    <rect x="0" y="52" width="480" height="10" rx="5" fill="#1e293b" />',
            f'    <rect x="0" y="52" width="{int((comp_l / max(0.1, init_l)) * 480)}" height="10" rx="5" fill="#38bdf8" />',
            f'    <text x="0" y="82" fill="#a78bfa" font-family="system-ui, sans-serif" font-size="11">Cowan Capacity Protect: Zero split-attention drag</text>',
            '  </g>',
            '</svg>',
        ])

        return "\n".join(svg)

    def export_summary_markdown(self, audit: CompactionAudit) -> str:
        """
        Generate executive compaction summary in Markdown with zero em dashes.
        """
        lines = [
            "# Working Memory Anchor Eviction and Buffer Compaction",
            "",
            f"**Buffer Slot Limit:** {audit.buffer_capacity_limit} items",
            f"**Working Memory Headroom Gained:** +{audit.headroom_gain_pct}%",
            f"**Nodes Retained (Active):** {audit.retained_node_count}",
            f"**Nodes Compacted (Deep Archive):** {audit.compacted_node_count}",
            "",
            "## 1. Retained Active Working Memory Nodes",
            "",
        ]

        if not audit.retained_nodes:
            lines.append("*Buffer currently empty.*")
        else:
            for n in audit.retained_nodes:
                lines.append(
                    f"- **{n.label}** (Saliency: {n.calculate_saliency()}/10, Idle: {n.idle_minutes}m, Refs: {n.reference_count})"
                )

        lines.extend([
            "",
            "## 2. Compacted Deep Storage Nodes",
            "",
        ])

        if not audit.compacted_nodes:
            lines.append("*No nodes required compaction. Buffer is within capacity limit.*")
        else:
            for cn in audit.compacted_nodes:
                lines.append(
                    f"- **{cn.label}** (Saliency: {cn.calculate_saliency()}/10, Idle: {cn.idle_minutes}m)"
                )

        lines.extend([
            "",
            "---",
            "*Generated by DxSkills MemoryBufferCompactor. Zero phonological friction, zero em dashes.*",
        ])

        return "\n".join(lines)
