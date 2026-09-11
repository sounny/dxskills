"""Autonomous Cognitive Spatial Dual-Code Working Memory Interleaver.

Theoretical Foundation:
- Paivio's Dual-Coding Theory (DCT):
  Cognitive architecture processes verbal representations (Phonological Loop)
  and non-verbal representations (Visuospatial Sketchpad) through distinct,
  independent channels. Learning and working memory retention compound exponentially
  when semantic information is dual-encoded via associative referential connections.
- Sweller's Split-Attention & Modality Effects:
  When verbal text and visual diagrams are presented disjointedly, cognitive bandwidth
  is consumed by search and match operations. Interleaving visual spatial cards
  directly with corresponding verbal explanations eliminates split-attention tax.
- Cross-Modal Referential Bridging:
  Extracts conceptual entities across spatial canvas nodes and linear prose,
  generating bidirectional anchor tags that ground abstract verbal tokens in
  stable visual topology.

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


class InterleaveMode(str, enum.Enum):
    """Layout format for dual-coded representation."""

    SIDE_BY_SIDE = "side_by_side"
    INTERLEAVED_STREAM = "interleaved_stream"
    VISUAL_ANCHORED = "visual_anchored"


@dataclass
class CrossReferenceLink:
    """Bidirectional semantic link between a spatial node and a verbal clause."""

    node_id: str
    node_title: str
    verbal_phrase: str
    match_confidence: float
    channel_balance_score: float


@dataclass
class DualCodeBlock:
    """Interleaved paired block comprising spatial node and verbal explanation."""

    block_id: int
    node_id: str
    spatial_title: str
    spatial_summary: str
    verbal_text: str
    cross_refs: List[str]
    visuospatial_load: float
    phonological_load: float


@dataclass
class DualCodeTelemetry:
    """Telemetry quantifying cross-modal synchronization and channel balance."""

    total_nodes: int
    total_verbal_sentences: int
    mapped_associations_count: int
    unmapped_verbal_count: int
    dual_code_balance_ratio: float
    cognitive_friction_reduction_pct: float
    blocks: List[DualCodeBlock] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert telemetry to JSON-compatible dictionary."""
        return {
            "total_nodes": self.total_nodes,
            "total_verbal_sentences": self.total_verbal_sentences,
            "mapped_associations_count": self.mapped_associations_count,
            "unmapped_verbal_count": self.unmapped_verbal_count,
            "dual_code_balance_ratio": round(self.dual_code_balance_ratio, 3),
            "cognitive_friction_reduction_pct": round(self.cognitive_friction_reduction_pct, 1),
            "blocks": [asdict(b) for b in self.blocks],
        }


class DualCodeInterleaver:
    """Synchronizes spatial canvas representations with verbal explanatory scripts."""

    def __init__(self, mode: InterleaveMode = InterleaveMode.INTERLEAVED_STREAM) -> None:
        self.mode = mode

    @staticmethod
    def extract_keywords(text: str) -> Set[str]:
        """Extract significant semantic keywords from a text snippet."""
        stopwords = {
            "the", "and", "a", "an", "in", "on", "at", "to", "for", "with", "from",
            "by", "of", "as", "is", "are", "was", "were", "be", "been", "this", "that",
            "these", "those", "it", "its", "or", "but", "into", "across", "over", "all"
        }
        tokens = re.findall(r"[a-zA-Z0-9]+", text.lower())
        return {t for t in tokens if len(t) > 3 and t not in stopwords}

    def align_channels(
        self,
        canvas_data: Dict[str, Any],
        prose_text: str,
    ) -> Tuple[List[DualCodeBlock], DualCodeTelemetry]:
        """Align spatial canvas nodes with verbal prose sentences into dual-code blocks."""
        nodes = canvas_data.get("nodes", [])
        if not nodes and not prose_text.strip():
            empty_telemetry = DualCodeTelemetry(
                total_nodes=0,
                total_verbal_sentences=0,
                mapped_associations_count=0,
                unmapped_verbal_count=0,
                dual_code_balance_ratio=1.0,
                cognitive_friction_reduction_pct=0.0,
                blocks=[],
            )
            return [], empty_telemetry

        # Split prose into sentences
        raw_sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", prose_text) if s.strip()]
        if not raw_sentences and prose_text.strip():
            raw_sentences = [prose_text.strip()]

        total_nodes = len(nodes)
        total_sentences = len(raw_sentences)

        # Build node semantic index
        node_records: List[Dict[str, Any]] = []
        for n in nodes:
            nid = str(n.get("id", ""))
            text = str(n.get("text", ""))
            lines = text.splitlines()
            title = lines[0].replace("#", "").strip() if lines else nid
            summary = "\n".join(lines[1:]).strip() if len(lines) > 1 else text
            keywords = self.extract_keywords(text)
            node_records.append({
                "id": nid,
                "title": title,
                "summary": summary,
                "keywords": keywords,
                "raw": n,
            })

        blocks: List[DualCodeBlock] = []
        mapped_sentences: Set[int] = set()

        for idx, nr in enumerate(node_records):
            matching_sentences: List[str] = []
            node_kw = nr["keywords"]

            for s_idx, sent in enumerate(raw_sentences):
                sent_kw = self.extract_keywords(sent)
                overlap = len(node_kw.intersection(sent_kw))
                if overlap > 0:
                    matching_sentences.append(sent)
                    mapped_sentences.add(s_idx)

            verbal_text = " ".join(matching_sentences) if matching_sentences else "No direct verbal accompaniment specified."
            spatial_words = len(nr["summary"].split())
            verbal_words = len(verbal_text.split())

            # Load scores (0.0 to 1.0)
            spatial_load = min(1.0, spatial_words / 25.0)
            phonological_load = min(1.0, verbal_words / 35.0)

            # Detect cross references
            cross_refs = [f"[Node: {nr['id']}]"]
            for kw in sorted(node_kw):
                if kw in verbal_text.lower():
                    cross_refs.append(f"@{kw}")

            blocks.append(
                DualCodeBlock(
                    block_id=idx + 1,
                    node_id=nr["id"],
                    spatial_title=nr["title"],
                    spatial_summary=nr["summary"],
                    verbal_text=verbal_text,
                    cross_refs=cross_refs[:5],
                    visuospatial_load=round(spatial_load, 2),
                    phonological_load=round(phonological_load, 2),
                )
            )

        # Append residual unmapped sentences into general synthesis block
        unmapped_indices = [i for i in range(total_sentences) if i not in mapped_sentences]
        if unmapped_indices:
            unmapped_text = " ".join([raw_sentences[i] for i in unmapped_indices])
            blocks.append(
                DualCodeBlock(
                    block_id=len(blocks) + 1,
                    node_id="node-general-verbal",
                    spatial_title="Macro System Synthesis",
                    spatial_summary="Global system context connecting modular components.",
                    verbal_text=unmapped_text,
                    cross_refs=["[Global Context]"],
                    visuospatial_load=0.2,
                    phonological_load=min(1.0, len(unmapped_text.split()) / 35.0),
                )
            )

        mapped_count = len(mapped_sentences)
        unmapped_count = len(unmapped_indices)

        # Dual-coding balance ratio: balance between visuospatial load and phonological load
        avg_spatial = sum(b.visuospatial_load for b in blocks) / len(blocks) if blocks else 0.0
        avg_phono = sum(b.phonological_load for b in blocks) / len(blocks) if blocks else 0.0

        if (avg_spatial + avg_phono) > 0:
            diff = abs(avg_spatial - avg_phono)
            balance_ratio = max(0.2, min(1.0, 1.0 - (diff * 0.8)))
        else:
            balance_ratio = 1.0

        # Cognitive friction reduction: higher when most sentences are successfully mapped
        mapping_rate = mapped_count / max(1, total_sentences)
        friction_reduction = (mapping_rate * 0.70 + balance_ratio * 0.30) * 100.0

        telemetry = DualCodeTelemetry(
            total_nodes=total_nodes,
            total_verbal_sentences=total_sentences,
            mapped_associations_count=mapped_count,
            unmapped_verbal_count=unmapped_count,
            dual_code_balance_ratio=balance_ratio,
            cognitive_friction_reduction_pct=friction_reduction,
            blocks=blocks,
        )

        return blocks, telemetry

    @staticmethod
    def render_ascii_dual_stream(telemetry: DualCodeTelemetry) -> str:
        """Render clean ASCII dual-coding stream safe for all terminals."""
        lines: List[str] = []
        lines.append("=== DxSkills Dual-Code Working Memory Interleaver ===")
        lines.append(
            f"Nodes: {telemetry.total_nodes} | Sentences: {telemetry.total_verbal_sentences} | "
            f"Mapped: {telemetry.mapped_associations_count} | Unmapped: {telemetry.unmapped_verbal_count}"
        )
        lines.append(
            f"Dual-Code Balance: {telemetry.dual_code_balance_ratio * 100:.1f}% | "
            f"Cognitive Friction Reduction: {telemetry.cognitive_friction_reduction_pct:.1f}%"
        )
        lines.append("=" * 70)

        for block in telemetry.blocks[:8]:
            s_bar = "#" * int(round(block.visuospatial_load * 8))
            p_bar = "*" * int(round(block.phonological_load * 8))

            lines.append(f"BLOCK #{block.block_id}: {block.spatial_title.upper()}")
            lines.append(f"  [Spatial Canvas]   [{s_bar:<8}] {block.spatial_summary[:48]}")
            lines.append(f"  [Verbal Script]    [{p_bar:<8}] {block.verbal_text[:48]}")
            lines.append(f"  [Bridges]          {', '.join(block.cross_refs)}")
            lines.append("-" * 70)

        if len(telemetry.blocks) > 8:
            rem = len(telemetry.blocks) - 8
            lines.append(f"... ({rem} additional dual-coded blocks queued)")
            lines.append("-" * 70)

        return "\n".join(lines)

    @staticmethod
    def export_interleaved_markdown(telemetry: DualCodeTelemetry, filepath: str | Path) -> Path:
        """Export dual-coded interleaved representation to structured markdown."""
        target = Path(filepath)
        md: List[str] = []
        md.append("# Dual-Coded Working Memory Specification\n")
        md.append(f"> **Dual-Code Balance:** {telemetry.dual_code_balance_ratio * 100:.1f}% | "
                  f"**Friction Reduction:** {telemetry.cognitive_friction_reduction_pct:.1f}%\n")
        md.append("---\n")

        for b in telemetry.blocks:
            md.append(f"## Section {b.block_id}: {b.spatial_title}\n")
            md.append("```\n+-------------------------------------------------------------+")
            md.append(f"| VISUAL SPATIAL ANCHOR: {b.spatial_title[:38]:<38} |")
            md.append("+-------------------------------------------------------------+")
            md.append(f"| {b.spatial_summary[:59]:<59} |")
            md.append("+-------------------------------------------------------------+\n```\n")
            md.append(f"**Verbal Script:**\n\n{b.verbal_text}\n")
            md.append(f"*Referential Bridges:* {', '.join(b.cross_refs)}\n")
            md.append("---\n")

        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("\n".join(md), encoding="utf-8")
        return target

    @staticmethod
    def export_canvas(telemetry: DualCodeTelemetry, filepath: str | Path) -> Path:
        """Export synchronized dual-track cards to Obsidian Canvas (.canvas) JSON."""
        target = Path(filepath)
        nodes: List[Dict[str, Any]] = []
        edges: List[Dict[str, Any]] = []

        header_text = (
            f"## Dual-Code Working Memory Stream\n\n"
            f"- **Dual-Code Balance:** {telemetry.dual_code_balance_ratio * 100:.1f}%\n"
            f"- **Friction Reduction:** {telemetry.cognitive_friction_reduction_pct:.1f}%\n"
            f"- **Mapped Associations:** {telemetry.mapped_associations_count} of {telemetry.total_verbal_sentences}\n"
            f"- **Total Dual Blocks:** {len(telemetry.blocks)}\n"
        )
        nodes.append({
            "id": "node-dual-header",
            "x": 0,
            "y": 0,
            "width": 360,
            "height": 200,
            "type": "text",
            "text": header_text,
            "color": "6",
        })

        card_w = 260
        card_h = 160
        y_offset = 260

        for idx, b in enumerate(telemetry.blocks[:16]):
            by = y_offset + (idx * (card_h + 40))

            # Spatial card (Left track)
            spatial_id = f"node-spatial-{b.block_id}"
            nodes.append({
                "id": spatial_id,
                "x": 0,
                "y": by,
                "width": card_w,
                "height": card_h,
                "type": "text",
                "text": f"### [Spatial] {b.spatial_title}\n\n{b.spatial_summary}\n\n*Load:* {b.visuospatial_load}",
                "color": "4",
            })

            # Verbal card (Right track)
            verbal_id = f"node-verbal-{b.block_id}"
            nodes.append({
                "id": verbal_id,
                "x": card_w + 80,
                "y": by,
                "width": card_w + 60,
                "height": card_h,
                "type": "text",
                "text": f"### [Verbal] Explanation\n\n{b.verbal_text[:140]}...\n\n*Refs:* {', '.join(b.cross_refs[:3])}",
                "color": "2",
            })

            # Dual-coding associative bridge edge
            edges.append({
                "id": f"edge-bridge-{b.block_id}",
                "fromNode": spatial_id,
                "fromSide": "right",
                "toNode": verbal_id,
                "toSide": "left",
                "label": "Dual-Code Bridge",
            })

        canvas_data = {"nodes": nodes, "edges": edges}
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(canvas_data, indent=2), encoding="utf-8")
        return target

    @staticmethod
    def export_svg_dual_track(telemetry: DualCodeTelemetry, filepath: str | Path) -> Path:
        """Export standalone SVG showing parallel Spatial and Verbal tracks with bridges."""
        target = Path(filepath)
        items = telemetry.blocks[:6]
        width = 860
        height = 140 + (len(items) * 90)

        svg: List[str] = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="auto">',
            '  <defs>',
            '    <linearGradient id="dc-bg" x1="0%" y1="0%" x2="100%" y2="100%">',
            '      <stop offset="0%" stop-color="#090d16"/>',
            '      <stop offset="100%" stop-color="#141c2e"/>',
            '    </linearGradient>',
            '  </defs>',
            f'  <rect width="{width}" height="{height}" rx="16" fill="url(#dc-bg)" stroke="#1e293b" stroke-width="2"/>',
            f'  <text x="32" y="40" fill="#f8fafc" font-family="system-ui, sans-serif" font-size="16" font-weight="700">DxSkills Dual-Code Working Memory Interleaver</text>',
            f'  <text x="32" y="64" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="12">Dual Balance: {telemetry.dual_code_balance_ratio*100:.1f}% | Friction Reduction: {telemetry.cognitive_friction_reduction_pct:.1f}% | Mapped: {telemetry.mapped_associations_count} sentences</text>',
            '  <text x="140" y="100" fill="#38bdf8" font-family="system-ui, sans-serif" font-size="12" font-weight="700" text-anchor="middle">SPATIAL TRACK (Visuospatial)</text>',
            '  <text x="660" y="100" fill="#34d399" font-family="system-ui, sans-serif" font-size="12" font-weight="700" text-anchor="middle">VERBAL TRACK (Phonological)</text>',
        ]

        sy = 120
        for idx, b in enumerate(items):
            cur_y = sy + (idx * 85)
            s_title = b.spatial_title[:20]
            v_snippet = b.verbal_text[:28]

            # Spatial block
            svg.append(f'  <rect x="40" y="{cur_y}" width="220" height="65" rx="8" fill="#0369a1" fill-opacity="0.3" stroke="#38bdf8" stroke-width="1"/>')
            svg.append(f'  <text x="150" y="{cur_y + 36}" fill="#f0f9ff" font-family="system-ui, sans-serif" font-size="12" font-weight="700" text-anchor="middle">{s_title}</text>')

            # Verbal block
            svg.append(f'  <rect x="540" y="{cur_y}" width="280" height="65" rx="8" fill="#065f46" fill-opacity="0.3" stroke="#34d399" stroke-width="1"/>')
            svg.append(f'  <text x="680" y="{cur_y + 36}" fill="#ecfdf5" font-family="system-ui, sans-serif" font-size="11" text-anchor="middle">{v_snippet}...</text>')

            # Connecting dual-code bridge line
            svg.append(f'  <line x1="260" y1="{cur_y + 32}" x2="540" y2="{cur_y + 32}" stroke="#818cf8" stroke-width="2" stroke-dasharray="4 4"/>')
            svg.append(f'  <circle cx="400" cy="{cur_y + 32}" r="5" fill="#818cf8"/>')

        svg.append('</svg>')
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("\n".join(svg), encoding="utf-8")
        return target
