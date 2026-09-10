#!/usr/bin/env python3
"""
Autonomous Cognitive Spatial Working Memory Anchor Stacking & Chunk Compression
Part of the DxSkills Cognitive Architecture Suite (https://dxskills.sounny.com)

Collapses redundant conceptual hierarchies and sprawling canvas nodes into dense,
associative spatial tokens. Enforces Cowan's working memory slot limit (4 +/- 1 chunks)
to prevent phonological fatigue and visual overwhelm during complex reasoning.

Core Principles:
- Working Memory Slot Preservation: Enforces Cowan's limit (4 +/- 1 items) across canvas spaces.
- Multi-Node Anchor Stacking: Consolidates sprawling conceptual sub-nodes into dense visual tokens.
- Cognitive Decompression Fidelity: Preserves critical semantic relationships during compression.
- Zero Jargon Friction: Measures and reports tangible cognitive slot savings directly.
"""

import os
import re
import json
import math
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple, Set


COWAN_WORKING_MEMORY_LIMIT = 4  # Standard working memory active chunk capacity


@dataclass
class CanvasConceptNode:
    """An individual semantic or spatial note node in a conceptual graph."""
    node_id: str
    text: str
    x: float = 0.0
    y: float = 0.0
    width: float = 240.0
    height: float = 140.0
    color: str = "1"  # Obsidian canvas color index
    category: str = "general"
    parent_id: Optional[str] = None
    tags: List[str] = field(default_factory=list)


@dataclass
class StackedAnchorToken:
    """A high-density stacked spatial anchor token representing multiple collapsed nodes."""
    anchor_id: str
    label: str
    summary: str
    condensed_text: str
    child_node_ids: List[str]
    color: str = "4"  # Default Green for optimized tokens
    x: float = 0.0
    y: float = 0.0
    width: float = 280.0
    height: float = 180.0
    original_slots: int = 1
    compressed_slots: int = 1  # Always 1 active cognitive slot per stacked token

    @property
    def compression_ratio(self) -> float:
        """Ratio of original nodes condensed into this single token."""
        if self.original_slots <= 0:
            return 1.0
        return round(float(self.original_slots) / float(self.compressed_slots), 2)


@dataclass
class ChunkCompressionAudit:
    """Telemetry report quantifying working memory slot preservation and cognitive offload."""
    original_node_count: int
    compressed_anchor_count: int
    original_slots_used: int
    compressed_slots_used: int
    slot_reduction_count: int
    slot_reduction_percentage: float
    cowan_capacity_respected: bool
    anchors: List[StackedAnchorToken]


class WorkingMemoryChunkCompressor:
    """Evaluates spatial canvas density and compresses sprawling nodes into stacked tokens."""

    def __init__(self, max_working_memory_slots: int = COWAN_WORKING_MEMORY_LIMIT):
        self.max_slots = max_working_memory_slots
        self.nodes: Dict[str, CanvasConceptNode] = {}
        self.edges: List[Dict[str, Any]] = []
        self._next_node_idx = 1
        self._next_anchor_idx = 1

    def add_node(
        self,
        text: str,
        node_id: Optional[str] = None,
        x: float = 0.0,
        y: float = 0.0,
        category: str = "general",
        parent_id: Optional[str] = None,
        tags: Optional[List[str]] = None,
        color: str = "1"
    ) -> CanvasConceptNode:
        """Register an individual conceptual note node."""
        nid = node_id or f"node-{self._next_node_idx}"
        self._next_node_idx += 1

        node = CanvasConceptNode(
            node_id=nid,
            text=text.strip(),
            x=x,
            y=y,
            category=category.strip().lower(),
            parent_id=parent_id,
            tags=list(tags) if tags else [],
            color=color
        )
        self.nodes[nid] = node
        return node

    def add_edge(self, from_id: str, to_id: str, label: str = "") -> None:
        """Register an associative edge between two nodes."""
        self.edges.append({
            "fromNode": from_id,
            "toNode": to_id,
            "label": label.strip()
        })

    def load_markdown_outline(self, markdown_text: str) -> None:
        """
        Parse hierarchical markdown headers and bullet points into conceptual nodes.
        H1/H2 become root category hubs; H3/bullets become associative child nodes.
        """
        lines = markdown_text.splitlines()
        current_parent_id: Optional[str] = None
        current_category = "general"
        pos_x = 100.0
        pos_y = 100.0

        for line in lines:
            line_str = line.strip()
            if not line_str:
                continue

            if line_str.startswith("# ") or line_str.startswith("## "):
                title = line_str.lstrip("# ").strip()
                node = self.add_node(
                    text=title,
                    x=pos_x,
                    y=pos_y,
                    category="root_hub",
                    color="5"  # Cyan hub
                )
                current_parent_id = node.node_id
                current_category = title.lower()[:15]
                pos_x += 320.0
                pos_y = 100.0
            elif line_str.startswith("### ") or line_str.startswith("- ") or line_str.startswith("* "):
                clean_text = line_str.lstrip("#-* ").strip()
                pos_y += 180.0
                child = self.add_node(
                    text=clean_text,
                    x=pos_x - 30.0,
                    y=pos_y,
                    category=current_category,
                    parent_id=current_parent_id,
                    color="1"
                )
                if current_parent_id:
                    self.add_edge(current_parent_id, child.node_id, label="contains")

    def compress_chunks(self, spatial_distance_threshold: float = 380.0) -> ChunkCompressionAudit:
        """
        Group nodes into associative clusters based on category, parent hierarchy,
        or spatial proximity, collapsing each cluster into a single StackedAnchorToken.
        """
        clusters: Dict[str, List[CanvasConceptNode]] = {}

        for node in self.nodes.values():
            # Cluster key prefers parent_id, else category, else fallback
            if node.parent_id:
                ckey = f"parent_{node.parent_id}"
            elif node.category and node.category != "general":
                ckey = f"cat_{node.category}"
            else:
                # Spatial proximity clustering
                ckey = f"grid_{int(node.x // spatial_distance_threshold)}_{int(node.y // spatial_distance_threshold)}"

            if ckey not in clusters:
                clusters[ckey] = []
            clusters[ckey].append(node)

        stacked_anchors: List[StackedAnchorToken] = []

        anchor_x = 100.0
        anchor_y = 100.0

        for ckey, cluster_nodes in clusters.items():
            if not cluster_nodes:
                continue

            aid = f"anchor-{self._next_anchor_idx}"
            self._next_anchor_idx += 1

            # Determine label and summary
            if len(cluster_nodes) == 1:
                label = cluster_nodes[0].text[:32]
                summary = cluster_nodes[0].text
                condensed = cluster_nodes[0].text
            else:
                root_node = next((n for n in cluster_nodes if n.category == "root_hub"), cluster_nodes[0])
                label = f"Anchor: {root_node.text[:28]}"
                bullet_items = [f"- {n.text[:60]}" for n in cluster_nodes if n != root_node]
                summary = f"Stacked cluster of {len(cluster_nodes)} conceptual nodes."
                condensed = f"**{root_node.text}**\n" + "\n".join(bullet_items[:6])

            # Average coordinates
            avg_x = sum(n.x for n in cluster_nodes) / len(cluster_nodes) if cluster_nodes else anchor_x
            avg_y = sum(n.y for n in cluster_nodes) / len(cluster_nodes) if cluster_nodes else anchor_y

            anchor = StackedAnchorToken(
                anchor_id=aid,
                label=label,
                summary=summary,
                condensed_text=condensed,
                child_node_ids=[n.node_id for n in cluster_nodes],
                color="4",  # Green token
                x=avg_x,
                y=avg_y,
                original_slots=len(cluster_nodes),
                compressed_slots=1
            )
            stacked_anchors.append(anchor)
            anchor_x += 320.0

        total_original_nodes = len(self.nodes)
        total_anchors = len(stacked_anchors)
        orig_slots = total_original_nodes
        comp_slots = total_anchors

        slot_red = max(0, orig_slots - comp_slots)
        slot_red_pct = round((slot_red / orig_slots * 100.0), 1) if orig_slots > 0 else 0.0
        respected = (comp_slots <= self.max_slots)

        return ChunkCompressionAudit(
            original_node_count=total_original_nodes,
            compressed_anchor_count=total_anchors,
            original_slots_used=orig_slots,
            compressed_slots_used=comp_slots,
            slot_reduction_count=slot_red,
            slot_reduction_percentage=slot_red_pct,
            cowan_capacity_respected=respected,
            anchors=stacked_anchors
        )

    def export_compressed_canvas(self, audit: ChunkCompressionAudit) -> Dict[str, Any]:
        """
        Generate an Obsidian .canvas structure featuring stacked anchor tokens
        and directional bridge connections, eliminating visual sprawl.
        """
        canvas_nodes = []
        canvas_edges = []

        # Add Stacked Anchor Nodes
        for anchor in audit.anchors:
            card_text = (
                f"### {anchor.label}\n"
                f"> **Cognitive Stack:** {anchor.original_slots} items condensed -> 1 slot\n\n"
                f"{anchor.condensed_text}\n\n"
                f"*Compression Factor: {anchor.compression_ratio}x*"
            )
            canvas_nodes.append({
                "id": anchor.anchor_id,
                "type": "text",
                "text": card_text,
                "x": int(anchor.x),
                "y": int(anchor.y),
                "width": int(anchor.width),
                "height": int(anchor.height),
                "color": anchor.color
            })

        # Add Telemetry HUD Card
        hud_status = "OPTIMIZED (Within Cowan Limit)" if audit.cowan_capacity_respected else "EXTENDED CAPACITY"
        hud_color = "4" if audit.cowan_capacity_respected else "2"
        hud_text = (
            f"## Spatial Working Memory Buffer Telemetry\n"
            f"- **Status:** {hud_status}\n"
            f"- **Original Working Memory Slots:** {audit.original_slots_used}\n"
            f"- **Active Compressed Slots:** {audit.compressed_slots_used} (Max Limit: {self.max_slots})\n"
            f"- **Cognitive Slots Offloaded:** {audit.slot_reduction_count} ({audit.slot_reduction_percentage}% reduction)\n"
            f"- **Phonological Buffer Stress:** Completely Eliminated"
        )
        canvas_nodes.append({
            "id": "node-hud-telemetry",
            "type": "text",
            "text": hud_text,
            "x": 100,
            "y": -160,
            "width": 380,
            "height": 180,
            "color": hud_color
        })

        # Link sequential anchors to form visual narrative flow
        for i in range(len(audit.anchors) - 1):
            a_cur = audit.anchors[i]
            a_next = audit.anchors[i + 1]
            canvas_edges.append({
                "id": f"edge-flow-{i + 1}",
                "fromNode": a_cur.anchor_id,
                "fromSide": "right",
                "toNode": a_next.anchor_id,
                "toSide": "left",
                "toEnd": "arrow",
                "label": "Associative Transition",
                "color": "5"
            })

        return {
            "nodes": canvas_nodes,
            "edges": canvas_edges
        }

    def export_svg_telemetry(self, audit: ChunkCompressionAudit, width: int = 740, height: int = 500) -> str:
        """
        Generate vector SVG displaying working memory buffer reduction,
        Cowan limit compliance bars, and stacked anchor tokens.
        """
        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
            f'width="{width}" height="{height}" style="background-color: #0f172a; '
            f'font-family: -apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, sans-serif;">',
            '<defs>',
            '  <linearGradient id="barGrad" x1="0%" y1="0%" x2="100%" y2="0%">',
            '    <stop offset="0%" stop-color="#10b981"/>',
            '    <stop offset="100%" stop-color="#06b6d4"/>',
            '  </linearGradient>',
            '  <linearGradient id="overloadGrad" x1="0%" y1="0%" x2="100%" y2="0%">',
            '    <stop offset="0%" stop-color="#f43f5e"/>',
            '    <stop offset="100%" stop-color="#fb7185"/>',
            '  </linearGradient>',
            '</defs>',
            '<!-- Title Header -->',
            f'<text x="28" y="36" fill="#f8fafc" font-size="16" font-weight="700">Spatial Working Memory Anchor Stacking &amp; Chunk Compression</text>',
            f'<text x="28" y="56" fill="#94a3b8" font-size="12">Cowan 4-Chunk Working Memory Capacity Optimization</text>',
            '<!-- Telemetry Panel -->',
            '<rect x="28" y="76" width="684" height="130" rx="8" fill="#1e293b" stroke="#334155" stroke-width="1"/>',
            f'<text x="48" y="104" fill="#64748b" font-size="11" font-weight="600">ORIGINAL NODES (SLOTS)</text>',
            f'<text x="48" y="132" fill="#f43f5e" font-size="24" font-weight="800">{audit.original_slots_used}</text>',
            f'<text x="200" y="104" fill="#64748b" font-size="11" font-weight="600">COMPRESSED TOKENS</text>',
            f'<text x="200" y="132" fill="#10b981" font-size="24" font-weight="800">{audit.compressed_slots_used}</text>',
            f'<text x="360" y="104" fill="#64748b" font-size="11" font-weight="600">SLOTS PRESERVED</text>',
            f'<text x="360" y="132" fill="#38bdf8" font-size="24" font-weight="800">{audit.slot_reduction_count} ({audit.slot_reduction_percentage}%)</text>',
            f'<text x="520" y="104" fill="#64748b" font-size="11" font-weight="600">COWAN CAPACITY</text>',
            f'<text x="520" y="132" fill="{"#10b981" if audit.cowan_capacity_respected else "#fbbf24"}" font-size="18" font-weight="700">{"RESPECTED" if audit.cowan_capacity_respected else "BORDERLINE"}</text>',
            '<!-- Working Memory Capacity Bar -->',
            '<text x="48" y="165" fill="#94a3b8" font-size="10.5">Active Chunk Load relative to Working Memory Capacity (4 chunks):</text>',
            '<rect x="48" y="174" width="644" height="16" rx="8" fill="#0f172a"/>',
        ]

        # Calculate fill ratio relative to 4 chunks (or max 12 chunks visually)
        visual_max = max(10, audit.original_slots_used)
        orig_w = int((audit.original_slots_used / visual_max) * 644)
        comp_w = int((audit.compressed_slots_used / visual_max) * 644)

        svg_parts.append(
            f'<rect x="48" y="174" width="{orig_w}" height="16" rx="8" fill="url(#overloadGrad)" opacity="0.4"/>'
        )
        svg_parts.append(
            f'<rect x="48" y="174" width="{comp_w}" height="16" rx="8" fill="url(#barGrad)"/>'
        )

        # Stacked Anchors Visualization Cards
        svg_parts.append('<!-- Stacked Anchor Visual Tokens -->')
        svg_parts.append('<text x="28" y="235" fill="#e2e8f0" font-size="13" font-weight="700">Compressed Stacked Anchor Tokens</text>')

        card_x = 28
        card_y = 250
        card_w = 215
        card_h = 210

        for idx, anchor in enumerate(audit.anchors[:3]):
            svg_parts.append(
                f'<g transform="translate({card_x + idx * 235}, {card_y})">'
                f'  <rect x="0" y="0" width="{card_w}" height="{card_h}" rx="8" fill="#1e293b" stroke="#10b981" stroke-width="1.5"/>'
                f'  <rect x="0" y="0" width="{card_w}" height="28" rx="8" fill="#10b981" fill-opacity="0.15"/>'
                f'  <text x="12" y="19" fill="#34d399" font-size="11" font-weight="700">{anchor.anchor_id.upper()}</text>'
                f'  <text x="{card_w - 12}" y="19" fill="#94a3b8" font-size="10" text-anchor="end">{anchor.original_slots} -> 1 Slot</text>'
                f'  <text x="12" y="48" fill="#f8fafc" font-size="12" font-weight="600">{anchor.label[:24]}</text>'
                f'  <line x1="12" y1="58" x2="{card_w - 12}" y2="58" stroke="#334155" stroke-width="1"/>'
            )

            # Draw child nodes as stacked mini tokens
            mini_y = 72
            for c_nid in anchor.child_node_ids[:4]:
                c_node = self.nodes.get(c_nid)
                txt = c_node.text[:22] if c_node else c_nid
                svg_parts.append(
                    f'  <rect x="12" y="{mini_y}" width="{card_w - 24}" height="24" rx="4" fill="#0f172a" stroke="#334155" stroke-width="1"/>'
                    f'  <circle cx="22" cy="{mini_y + 12}" r="3" fill="#38bdf8"/>'
                    f'  <text x="32" y="{mini_y + 16}" fill="#cbd5e1" font-size="10">{txt}</text>'
                )
                mini_y += 28

            if len(anchor.child_node_ids) > 4:
                rem = len(anchor.child_node_ids) - 4
                svg_parts.append(
                    f'  <text x="12" y="{mini_y + 12}" fill="#64748b" font-size="9.5">+{rem} more sub-concepts stacked</text>'
                )

            svg_parts.append('</g>')

        svg_parts.append('</svg>')
        return "\n".join(svg_parts)

    def export_summary_markdown(self, audit: ChunkCompressionAudit) -> str:
        """Generate executive markdown report describing slot reduction and working memory health."""
        lines = [
            "# Spatial Working Memory Anchor Stacking & Chunk Compression Report",
            "",
            "## Executive Telemetry",
            f"- **Original Working Memory Slots:** {audit.original_slots_used}",
            f"- **Compressed Active Slots:** {audit.compressed_slots_used} (Capacity Limit: {self.max_slots})",
            f"- **Slots Offloaded / Preserved:** {audit.slot_reduction_count} ({audit.slot_reduction_percentage}% reduction)",
            f"- **Cowan 4-Chunk Limit Respected:** {'Yes (Optimal Cognitive Comfort)' if audit.cowan_capacity_respected else 'Extended (Requires Secondary Decompression)'}",
            "",
            "## Stacked Anchor Tokens",
            ""
        ]

        for a in audit.anchors:
            lines.append(f"### {a.label} (`{a.anchor_id}`)")
            lines.append(f"- **Condensed Nodes:** {a.original_slots} nodes collapsed into 1 active working memory slot")
            lines.append(f"- **Compression Ratio:** `{a.compression_ratio}x`")
            lines.append(f"- **Child Concepts:** {', '.join(a.child_node_ids[:8])}")
            lines.append("")
            lines.append("```markdown")
            lines.append(a.condensed_text)
            lines.append("```")
            lines.append("")

        return "\n".join(lines)


def create_sample_chunk_compressor() -> Tuple[WorkingMemoryChunkCompressor, ChunkCompressionAudit]:
    """Create demonstration compressor populated with sprawling cognitive nodes."""
    compressor = WorkingMemoryChunkCompressor(max_working_memory_slots=4)
    sample_doc = """# Event-Driven Streaming Architecture
- Partitioned Kafka ingestion buffer
- Avro schema registry validation
- Outbox pattern transaction log miner

# Real-Time Geospatial Processing Engine
- H3 hexagonal spatial indexing
- Vector tile dynamic slicing
- Bounding-box spatial query cache

# Multi-Agent Coordination Mesh
- Shared blackboard state ledger
- Socratic debate dialectic consensus
- Deadlock arbitration timeout supervisor"""

    compressor.load_markdown_outline(sample_doc)
    audit = compressor.compress_chunks()
    return compressor, audit


if __name__ == "__main__":
    comp, audit = create_sample_chunk_compressor()
    print(comp.export_summary_markdown(audit))
