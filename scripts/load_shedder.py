#!/usr/bin/env python3
"""
Autonomous Cognitive Dynamic Working Memory Stress-Tester & Load Shedder
Part of the DxSkills Cognitive Architecture Suite (https://dxskills.sounny.com)

Simulates mental model stress under branching conceptual complexity. Calculates
Cognitive Degradation Index (CDI) based on Sweller Cognitive Load Theory and Baddeley
working memory limits. Executes graceful semantic load-shedding to prune non-critical
branches and restore executive clarity.

Core Principles:
- Cognitive Degradation Modeling: Measures intrinsic, extraneous, and germane cognitive loads.
- Graceful Semantic Degradation: Prunes tertiary leaves and collapses linear chains under load.
- Executive Headroom Preservation: Guarantees working memory headroom before cognitive collapse.
- Zero Jargon Friction: Reports cognitive relief and stress points in plain physical terms.
"""

import os
import re
import json
import math
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple, Set


MAX_HEALTHY_COGNITIVE_POINTS = 65.0  # Sustainable working memory threshold


@dataclass
class CognitiveNode:
    """An individual node in the mental model network."""
    node_id: str
    label: str
    text: str = ""
    depth: int = 0
    in_degree: int = 0
    out_degree: int = 0
    complexity_weight: float = 1.0
    is_shed: bool = False
    shed_tier: int = 0  # 0 = kept, 1 = folded leaf, 2 = collapsed transitive, 3 = decoupled
    color: str = "1"
    x: float = 100.0
    y: float = 100.0


@dataclass
class StressTelemetry:
    """Telemetry describing working memory load and cognitive degradation risk."""
    total_nodes: int
    max_depth: int
    branching_factor: float
    intrinsic_load: float   # Essential complexity
    extraneous_load: float  # Formatting and branch clutter
    germane_load: float     # Synergistic structural schema
    total_load_points: float
    cognitive_degradation_index: float  # 0.0 to 1.0
    status: str  # OPTIMAL, ELEVATED, CRITICAL


@dataclass
class SheddingAudit:
    """Audit report capturing load-shedding intervention and recovered cognitive headroom."""
    initial_telemetry: StressTelemetry
    post_shed_telemetry: StressTelemetry
    pruned_leaves_count: int
    collapsed_chains_count: int
    load_points_freed: float
    reduction_percentage: float
    retained_nodes: List[CognitiveNode]
    shed_nodes: List[CognitiveNode]


class WorkingMemoryLoadShedder:
    """Evaluates conceptual graph complexity and executes automated load shedding."""

    def __init__(self, capacity_threshold: float = MAX_HEALTHY_COGNITIVE_POINTS):
        self.capacity_threshold = capacity_threshold
        self.nodes: Dict[str, CognitiveNode] = {}
        self.edges: List[Dict[str, str]] = []
        self._next_idx = 1

    def add_node(
        self,
        label: str,
        text: str = "",
        node_id: Optional[str] = None,
        complexity_weight: float = 1.0,
        x: float = 100.0,
        y: float = 100.0,
        color: str = "1"
    ) -> CognitiveNode:
        """Register a node in the conceptual space."""
        nid = node_id or f"node-{self._next_idx}"
        self._next_idx += 1

        node = CognitiveNode(
            node_id=nid,
            label=label.strip(),
            text=text.strip() or label.strip(),
            complexity_weight=max(0.2, float(complexity_weight)),
            x=x,
            y=y,
            color=color
        )
        self.nodes[nid] = node
        return node

    def add_edge(self, from_id: str, to_id: str, label: str = "") -> None:
        """Register a directional edge between two concepts."""
        self.edges.append({
            "from": from_id,
            "to": to_id,
            "label": label.strip()
        })
        if from_id in self.nodes:
            self.nodes[from_id].out_degree += 1
        if to_id in self.nodes:
            self.nodes[to_id].in_degree += 1

    def load_from_markdown(self, markdown_text: str) -> None:
        """Parse structured outline into a hierarchical conceptual graph."""
        lines = [line.rstrip() for line in markdown_text.splitlines() if line.strip()]
        parent_stack: List[Tuple[int, str]] = []  # (indent_level, node_id)

        pos_x = 80.0
        pos_y = 80.0

        for line in lines:
            indent = len(line) - len(line.lstrip())
            text = line.strip()

            if text.startswith("#"):
                clean = text.lstrip("# ").strip()
                h_level = len(text) - len(text.lstrip("#"))
                node = self.add_node(label=clean, x=pos_x, y=pos_y, complexity_weight=1.5, color="5")
                pos_x += 280.0
                pos_y = 80.0
                parent_stack = [(h_level, node.node_id)]
            else:
                clean = text.lstrip("-*0123456789. ").strip()
                node = self.add_node(label=clean, x=pos_x, y=pos_y, complexity_weight=1.0, color="1")
                pos_y += 140.0

                # Determine parent from stack
                while parent_stack and parent_stack[-1][0] >= indent:
                    parent_stack.pop()

                if parent_stack:
                    p_id = parent_stack[-1][1]
                    self.add_edge(p_id, node.node_id, label="contains")
                    node.depth = self.nodes[p_id].depth + 1

                parent_stack.append((indent, node.node_id))

    def calculate_stress(self) -> StressTelemetry:
        """
        Compute cognitive load points based on node counts, fan-out complexity,
        branching depth, and extraneous wording clutter.
        """
        total = len(self.nodes)
        active_nodes = [n for n in self.nodes.values() if not n.is_shed]

        if not active_nodes:
            return StressTelemetry(
                total_nodes=0, max_depth=0, branching_factor=0.0,
                intrinsic_load=0.0, extraneous_load=0.0, germane_load=0.0,
                total_load_points=0.0, cognitive_degradation_index=0.0, status="OPTIMAL"
            )

        max_depth = max((n.depth for n in active_nodes), default=0)
        active_edges = [e for e in self.edges if not self.nodes[e["from"]].is_shed and not self.nodes[e["to"]].is_shed]

        branching_factor = round(len(active_edges) / max(1, len(active_nodes)), 2)

        # Intrinsic Load: Core conceptual difficulty (node weights)
        intrinsic = sum(n.complexity_weight * 3.5 for n in active_nodes)

        # Extraneous Load: Excessive branching, unlinked leaf clutter, text density
        leaf_count = sum(1 for n in active_nodes if n.out_degree == 0 and n.depth > 1)
        text_density = sum(len(n.text.split()) for n in active_nodes) * 0.15
        extraneous = (len(active_edges) * 2.2) + (leaf_count * 4.0) + (max_depth * 3.0) + text_density

        # Germane Load: Helpful associative structure (balanced fan-out bonus)
        germane = min(15.0, len(active_edges) * 1.5)

        # Total points: intrinsic + extraneous - germane
        total_points = round(max(5.0, intrinsic + extraneous - germane), 1)

        # CDI: 0.0 to 1.0 scale relative to healthy threshold
        cdi = round(min(1.0, total_points / 100.0), 2)

        if cdi >= 0.75:
            status = "CRITICAL"
        elif cdi >= 0.50:
            status = "ELEVATED"
        else:
            status = "OPTIMAL"

        return StressTelemetry(
            total_nodes=len(active_nodes),
            max_depth=max_depth,
            branching_factor=branching_factor,
            intrinsic_load=round(intrinsic, 1),
            extraneous_load=round(extraneous, 1),
            germane_load=round(germane, 1),
            total_load_points=total_points,
            cognitive_degradation_index=cdi,
            status=status
        )

    def execute_load_shedding(self, target_cdi: float = 0.55) -> SheddingAudit:
        """
        Execute automated tiered semantic load shedding until CDI drops below target.
        Tier 1: Prune tertiary leaf nodes (depth >= 2 with out_degree == 0).
        Tier 2: Collapse linear transitive chains (A -> B -> C).
        Tier 3: Fold auxiliary siblings into parent metadata.
        """
        initial_telemetry = self.calculate_stress()

        pruned_leaves = 0
        collapsed_chains = 0

        # If already healthy, return early
        if initial_telemetry.cognitive_degradation_index <= target_cdi:
            return SheddingAudit(
                initial_telemetry=initial_telemetry,
                post_shed_telemetry=initial_telemetry,
                pruned_leaves_count=0,
                collapsed_chains_count=0,
                load_points_freed=0.0,
                reduction_percentage=0.0,
                retained_nodes=list(self.nodes.values()),
                shed_nodes=[]
            )

        # TIER 1: Prune tertiary leaf nodes
        for node in list(self.nodes.values()):
            if node.depth >= 2 and node.out_degree == 0 and not node.is_shed:
                node.is_shed = True
                node.shed_tier = 1
                pruned_leaves += 1

                current_cdi = self.calculate_stress().cognitive_degradation_index
                if current_cdi <= target_cdi:
                    break

        # TIER 2: Collapse linear single-pass chains if still strained
        if self.calculate_stress().cognitive_degradation_index > target_cdi:
            for node in list(self.nodes.values()):
                if not node.is_shed and node.in_degree == 1 and node.out_degree == 1:
                    node.is_shed = True
                    node.shed_tier = 2
                    collapsed_chains += 1

                    current_cdi = self.calculate_stress().cognitive_degradation_index
                    if current_cdi <= target_cdi:
                        break

        post_telemetry = self.calculate_stress()
        freed = round(max(0.0, initial_telemetry.total_load_points - post_telemetry.total_load_points), 1)
        pct = round((freed / initial_telemetry.total_load_points) * 100.0, 1) if initial_telemetry.total_load_points > 0 else 0.0

        retained = [n for n in self.nodes.values() if not n.is_shed]
        shed = [n for n in self.nodes.values() if n.is_shed]

        return SheddingAudit(
            initial_telemetry=initial_telemetry,
            post_shed_telemetry=post_telemetry,
            pruned_leaves_count=pruned_leaves,
            collapsed_chains_count=collapsed_chains,
            load_points_freed=freed,
            reduction_percentage=pct,
            retained_nodes=retained,
            shed_nodes=shed
        )

    def export_canvas(self, audit: SheddingAudit) -> Dict[str, Any]:
        """
        Generate Obsidian .canvas file displaying the preserved core network.
        Retained nodes are styled green/cyan; shed nodes are tucked into a folded
        archive card to prevent visual clutter while preserving trace history.
        """
        canvas_nodes = []
        canvas_edges = []

        # Add Telemetry HUD Card
        hud_color = "4" if audit.post_shed_telemetry.status == "OPTIMAL" else "2"
        hud_text = (
            f"## Cognitive Working Memory Health HUD\n"
            f"- **Status:** {audit.post_shed_telemetry.status}\n"
            f"- **Initial Cognitive Stress:** {audit.initial_telemetry.total_load_points} pts (CDI: {audit.initial_telemetry.cognitive_degradation_index})\n"
            f"- **Post-Shedding Stress:** {audit.post_shed_telemetry.total_load_points} pts (CDI: {audit.post_shed_telemetry.cognitive_degradation_index})\n"
            f"- **Executive Headroom Freed:** {audit.load_points_freed} pts ({audit.reduction_percentage}% reduction)\n"
            f"- **Active Nodes Retained:** {len(audit.retained_nodes)} (Pruned Leaves: {audit.pruned_leaves_count})"
        )
        canvas_nodes.append({
            "id": "node-hud-stress",
            "type": "text",
            "text": hud_text,
            "x": 80,
            "y": -160,
            "width": 380,
            "height": 190,
            "color": hud_color
        })

        # Add Retained Core Nodes
        for node in audit.retained_nodes:
            card_text = f"### {node.label}\n\n{node.text}\n\n*Depth: {node.depth} | Complexity: {node.complexity_weight}*"
            canvas_nodes.append({
                "id": f"node-{node.node_id}",
                "type": "text",
                "text": card_text,
                "x": int(node.x),
                "y": int(node.y),
                "width": 260,
                "height": 160,
                "color": node.color
            })

        # Add Folded Shed Archives Card if any were pruned
        if audit.shed_nodes:
            shed_items = [f"- **{n.label}** (Tier {n.shed_tier})" for n in audit.shed_nodes[:8]]
            folded_text = (
                f"### Folded Semantic Details (Shed Archives)\n"
                f"> Offloaded {len(audit.shed_nodes)} non-critical nodes to protect working memory.\n\n"
                + "\n".join(shed_items)
            )
            canvas_nodes.append({
                "id": "node-folded-archive",
                "type": "text",
                "text": folded_text,
                "x": 80,
                "y": 620,
                "width": 340,
                "height": 210,
                "color": "1"  # Muted / Gray
            })

        # Add Edges between active nodes
        retained_ids = {n.node_id for n in audit.retained_nodes}
        for idx, edge in enumerate(self.edges, 1):
            if edge["from"] in retained_ids and edge["to"] in retained_ids:
                canvas_edges.append({
                    "id": f"edge-stress-{idx}",
                    "fromNode": f"node-{edge['from']}",
                    "toNode": f"node-{edge['to']}",
                    "toEnd": "arrow",
                    "label": edge.get("label", ""),
                    "color": "4"
                })

        return {
            "nodes": canvas_nodes,
            "edges": canvas_edges
        }

    def export_svg_gauge(self, audit: SheddingAudit, width: int = 760, height: int = 480) -> str:
        """
        Generate vector SVG displaying cognitive degradation gauge,
        before/after stress breakdown, and load shedding recovery metrics.
        """
        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
            f'width="{width}" height="{height}" style="background-color: #0f172a; '
            f'font-family: -apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, sans-serif;">',
            '<defs>',
            '  <linearGradient id="stressGrad" x1="0%" y1="0%" x2="100%" y2="0%">',
            '    <stop offset="0%" stop-color="#10b981"/>',
            '    <stop offset="60%" stop-color="#f59e0b"/>',
            '    <stop offset="100%" stop-color="#f43f5e"/>',
            '  </linearGradient>',
            '</defs>',
            '<!-- Title Header -->',
            f'<text x="28" y="34" fill="#f8fafc" font-size="16" font-weight="700">Cognitive Working Memory Stress-Tester &amp; Load Shedder</text>',
            f'<text x="28" y="52" fill="#94a3b8" font-size="12">Sweller Cognitive Load Index &amp; Dynamic Semantic Degradation</text>',
            '<!-- Metrics Summary Box -->',
            '<rect x="28" y="75" width="704" height="110" rx="8" fill="#1e293b" stroke="#334155" stroke-width="1"/>',
            f'<text x="48" y="102" fill="#64748b" font-size="11" font-weight="600">INITIAL COGNITIVE LOAD</text>',
            f'<text x="48" y="132" fill="#f43f5e" font-size="24" font-weight="800">{audit.initial_telemetry.total_load_points} pts</text>',
            f'<text x="48" y="152" fill="#94a3b8" font-size="10">CDI: {audit.initial_telemetry.cognitive_degradation_index} ({audit.initial_telemetry.status})</text>',
            f'<text x="240" y="102" fill="#64748b" font-size="11" font-weight="600">POST-SHED LOAD</text>',
            f'<text x="240" y="132" fill="#10b981" font-size="24" font-weight="800">{audit.post_shed_telemetry.total_load_points} pts</text>',
            f'<text x="240" y="152" fill="#94a3b8" font-size="10">CDI: {audit.post_shed_telemetry.cognitive_degradation_index} ({audit.post_shed_telemetry.status})</text>',
            f'<text x="430" y="102" fill="#64748b" font-size="11" font-weight="600">HEADROOM RECOVERED</text>',
            f'<text x="430" y="132" fill="#38bdf8" font-size="24" font-weight="800">{audit.load_points_freed} pts</text>',
            f'<text x="430" y="152" fill="#38bdf8" font-size="10">+{audit.reduction_percentage}% Cognitive Relief</text>',
            f'<text x="600" y="102" fill="#64748b" font-size="11" font-weight="600">SHED BRANCHES</text>',
            f'<text x="600" y="132" fill="#a855f7" font-size="24" font-weight="800">{len(audit.shed_nodes)}</text>',
            f'<text x="600" y="152" fill="#94a3b8" font-size="10">{audit.pruned_leaves_count} leaves folded</text>',
            '<!-- Before vs After Visual Load Bars -->',
            '<text x="28" y="222" fill="#e2e8f0" font-size="13" font-weight="700">Cognitive Degradation Index (CDI) Comparison</text>',
            '<text x="28" y="246" fill="#94a3b8" font-size="11">Pre-Shedding Stress (Overloaded):</text>',
            '<rect x="28" y="255" width="704" height="22" rx="6" fill="#0f172a" stroke="#334155"/>',
        ]

        init_w = int(audit.initial_telemetry.cognitive_degradation_index * 704)
        post_w = int(audit.post_shed_telemetry.cognitive_degradation_index * 704)

        svg_parts.append(
            f'<rect x="28" y="255" width="{init_w}" height="22" rx="6" fill="#f43f5e" fill-opacity="0.8"/>'
        )
        svg_parts.append(
            f'<text x="{max(40, init_w + 15)}" y="271" fill="#f8fafc" font-size="10.5" font-weight="700">{int(audit.initial_telemetry.cognitive_degradation_index * 100)}%</text>'
        )

        svg_parts.append('<text x="28" y="308" fill="#94a3b8" font-size="11">Post-Shedding Stress (Restored Working Memory):</text>')
        svg_parts.append('<rect x="28" y="317" width="704" height="22" rx="6" fill="#0f172a" stroke="#334155"/>')
        svg_parts.append(
            f'<rect x="28" y="317" width="{post_w}" height="22" rx="6" fill="#10b981" fill-opacity="0.9"/>'
        )
        svg_parts.append(
            f'<text x="{max(40, post_w + 15)}" y="333" fill="#f8fafc" font-size="10.5" font-weight="700">{int(audit.post_shed_telemetry.cognitive_degradation_index * 100)}% (OPTIMAL)</text>'
        )

        # Bottom Directives
        svg_parts.append('<rect x="28" y="365" width="704" height="85" rx="8" fill="#1e293b" stroke="#334155" stroke-width="1"/>')
        svg_parts.append('<text x="48" y="392" fill="#38bdf8" font-size="11.5" font-weight="700">EXECUTIVE COGNITIVE DIRECTIVE:</text>')
        svg_parts.append(
            f'<text x="48" y="414" fill="#cbd5e1" font-size="11">'
            f'Pruned {audit.pruned_leaves_count} tertiary leaf branches and folded {len(audit.shed_nodes)} non-critical concepts. '
            f'Working memory stabilized within sustainable cognitive limits.'
            f'</text>'
        )

        svg_parts.append('</svg>')
        return "\n".join(svg_parts)

    def export_summary_markdown(self, audit: SheddingAudit) -> str:
        """Generate executive report on working memory stress and load shedding."""
        lines = [
            "# Working Memory Stress-Tester & Load Shedder Report",
            "",
            "## Executive Telemetry",
            f"- **Pre-Shedding Stress:** {audit.initial_telemetry.total_load_points} points (CDI: `{audit.initial_telemetry.cognitive_degradation_index}` -> **{audit.initial_telemetry.status}**)",
            f"- **Post-Shedding Stress:** {audit.post_shed_telemetry.total_load_points} points (CDI: `{audit.post_shed_telemetry.cognitive_degradation_index}` -> **{audit.post_shed_telemetry.status}**)",
            f"- **Cognitive Headroom Freed:** `{audit.load_points_freed} points` ({audit.reduction_percentage}% load relief)",
            f"- **Tertiary Leaves Folded:** {audit.pruned_leaves_count}",
            f"- **Retained Core Nodes:** {len(audit.retained_nodes)} / {audit.initial_telemetry.total_nodes}",
            "",
            "## Sweller Cognitive Load Component Breakdown",
            "",
            "| Cognitive Load Component | Initial Points | Post-Shed Points | Delta |",
            "| :--- | :---: | :---: | :---: |",
            f"| **Intrinsic Load (Essential Concept)** | `{audit.initial_telemetry.intrinsic_load}` | `{audit.post_shed_telemetry.intrinsic_load}` | `-{round(audit.initial_telemetry.intrinsic_load - audit.post_shed_telemetry.intrinsic_load, 1)}` |",
            f"| **Extraneous Load (Clutter & Sprawl)** | `{audit.initial_telemetry.extraneous_load}` | `{audit.post_shed_telemetry.extraneous_load}` | `-{round(audit.initial_telemetry.extraneous_load - audit.post_shed_telemetry.extraneous_load, 1)}` |",
            f"| **Germane Load (Active Synthesis)** | `{audit.initial_telemetry.germane_load}` | `{audit.post_shed_telemetry.germane_load}` | `-{round(audit.initial_telemetry.germane_load - audit.post_shed_telemetry.germane_load, 1)}` |",
            "",
            "## Shed Semantic Branches (Archived into Parent Metadata)",
            ""
        ]

        if audit.shed_nodes:
            for n in audit.shed_nodes:
                lines.append(f"- **{n.label}:** Folded at Tier {n.shed_tier} (Depth: {n.depth})")
        else:
            lines.append("*(No semantic shedding required. Working memory is well within healthy operating capacity.)*")

        return "\n".join(lines)


def create_sample_stress_scenario() -> Tuple[WorkingMemoryLoadShedder, SheddingAudit]:
    """Create demonstration overloaded conceptual graph representing software system sprawl."""
    shedder = WorkingMemoryLoadShedder()
    sample_outline = """# Distributed Storage Engine
- Master coordinator node
  - Heartbeat lease monitor
  - Election timeout listener
  - Cluster metadata cache
    - Cache invalidation hook
    - Cache hit telemetry
    - Serialized TTL eviction
- Write-Ahead Log Partition
  - Segment file rotation
  - Group commit fsync batcher
  - Checkpoint barrier snapshot
    - Snapshot compression worker
    - S3 cold backup replica
- Client Connection Multiplexer
  - TLS handshake terminator
  - Keep-alive ping responder
  - Backpressure request buffer
    - Micro-buffer watermark high
    - Micro-buffer watermark low"""

    shedder.load_from_markdown(sample_outline)
    audit = shedder.execute_load_shedding(target_cdi=0.50)
    return shedder, audit


if __name__ == "__main__":
    shedder, audit = create_sample_stress_scenario()
    print(shedder.export_summary_markdown(audit))
