"""Autonomous Cognitive Spatial Bi-Directional Hyper-Link Resonance Weaver.

Theoretical Foundation:
- Eide & Eide M-I-N-D Framework (Interconnected "I" Reasoning):
  Dyslexic cognition thrives on discovering unexpected conceptual links, cross-domain
  metaphors, and latent structural invariants. When working with complex spatial canvases,
  valuable conceptual alignments remain disconnected because manual link-making imposes
  excessive executive function overhead.
- Semantic Proximity & Concept Extraction:
  Extracts semantic keywords, lexical terms, and structural claims across isolated
  spatial cards. Computes Jaccard affinity and thematic synergy between unlinked nodes.
- Non-Destructive Bi-Directional Resonance Bridges:
  Synthesizes associative edges across isolated clusters without mutating original
  content. Categorizes discoveries into invariant alignment, thematic synergy,
  dialectic counterparts, or cross-domain analogies with contextual bridge labels.
- Dark Titanium SVG & Obsidian .canvas Export:
  Generates production-grade Obsidian .canvas files with enhanced bi-directional
  resonance edges and dark titanium SVG diagrams with glowing bezier bridge arcs.

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


class ResonanceCategory(str, enum.Enum):
    """Classification of associative semantic resonance between spatial nodes."""

    INVARIANT_ALIGNMENT = "invariant_alignment"
    THEMATIC_SYNERGY = "thematic_synergy"
    DIALECTIC_COUNTERPART = "dialectic_counterpart"
    CROSS_DOMAIN_ANALOGY = "cross_domain_analogy"


@dataclass
class ResonanceBridge:
    """Represents a discovered bi-directional semantic bridge between spatial nodes."""

    bridge_id: str
    source_id: str
    source_title: str
    target_id: str
    target_title: str
    resonance_score: float
    category: ResonanceCategory
    shared_concepts: List[str]
    thematic_anchor_label: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert bridge to serializable dictionary."""
        return {
            "bridge_id": self.bridge_id,
            "source_id": self.source_id,
            "source_title": self.source_title,
            "target_id": self.target_id,
            "target_title": self.target_title,
            "resonance_score": round(self.resonance_score, 2),
            "category": self.category.value,
            "shared_concepts": sorted(self.shared_concepts),
            "thematic_anchor_label": self.thematic_anchor_label,
        }


@dataclass
class ResonanceWeaverTelemetry:
    """Telemetry capturing associative link discovery and network resonance."""

    total_nodes: int
    existing_edges_count: int
    discovered_bridges_count: int
    mean_resonance_intensity: float
    associative_density_lift_pct: float
    bridges: List[ResonanceBridge] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert telemetry to JSON-compatible dictionary."""
        return {
            "total_nodes": self.total_nodes,
            "existing_edges_count": self.existing_edges_count,
            "discovered_bridges_count": self.discovered_bridges_count,
            "mean_resonance_intensity": round(self.mean_resonance_intensity, 2),
            "associative_density_lift_pct": round(self.associative_density_lift_pct, 1),
            "bridges": [b.to_dict() for b in self.bridges],
        }


class HyperLinkResonanceWeaver:
    """Discovers and synthesizes bi-directional associative bridges across spatial nodes."""

    def __init__(
        self,
        min_resonance_threshold: float = 0.28,
        max_bridges_per_node: int = 3,
    ) -> None:
        self.min_resonance_threshold = min_resonance_threshold
        self.max_bridges_per_node = max_bridges_per_node
        self.nodes: Dict[str, Dict[str, Any]] = {}
        self.existing_edges: Set[Tuple[str, str]] = set()
        self.raw_canvas_edges: List[Dict[str, Any]] = []

    def load_dict(self, nodes_data: Dict[str, Any]) -> None:
        """Load nodes and existing links from dictionary structure."""
        self.nodes.clear()
        self.existing_edges.clear()
        self.raw_canvas_edges.clear()

        raw = nodes_data.get("nodes", nodes_data)
        for n_id, info in raw.items():
            if isinstance(info, dict):
                title = info.get("title", n_id)
                text = info.get("text", title)
                tags = list(info.get("tags", []))
                x = float(info.get("x", 0.0))
                y = float(info.get("y", 0.0))
                w = float(info.get("width", 260.0))
                h = float(info.get("height", 140.0))
            else:
                title = str(info)
                text = str(info)
                tags = []
                x = 0.0
                y = 0.0
                w = 260.0
                h = 140.0

            tokens = self._extract_semantic_tokens(f"{title} {text} {' '.join(tags)}")
            self.nodes[n_id] = {
                "id": n_id,
                "title": title,
                "text": text,
                "tags": tags,
                "tokens": tokens,
                "x": x,
                "y": y,
                "width": w,
                "height": h,
            }

        if "edges" in nodes_data:
            self.raw_canvas_edges = list(nodes_data.get("edges", []))
            for e in self.raw_canvas_edges:
                src = str(e.get("fromNode", ""))
                tgt = str(e.get("toNode", ""))
                if src and tgt:
                    self.existing_edges.add((src, tgt))
                    self.existing_edges.add((tgt, src))

    def load_canvas(self, canvas_data: Dict[str, Any]) -> None:
        """Extract spatial cards and existing edges from Obsidian .canvas format."""
        self.nodes.clear()
        self.existing_edges.clear()
        self.raw_canvas_edges = list(canvas_data.get("edges", []))

        for e in self.raw_canvas_edges:
            src = str(e.get("fromNode", ""))
            tgt = str(e.get("toNode", ""))
            if src and tgt:
                self.existing_edges.add((src, tgt))
                self.existing_edges.add((tgt, src))

        nodes = canvas_data.get("nodes", [])
        for node in nodes:
            n_id = str(node.get("id", ""))
            text = str(node.get("text", "")).strip()
            lines = [l.strip() for l in text.split("\n") if l.strip()]
            title = lines[0].lstrip("#").strip() if lines else n_id

            tokens = self._extract_semantic_tokens(text)
            self.nodes[n_id] = {
                "id": n_id,
                "title": title,
                "text": text,
                "tags": [],
                "tokens": tokens,
                "x": float(node.get("x", 0.0)),
                "y": float(node.get("y", 0.0)),
                "width": float(node.get("width", 260.0)),
                "height": float(node.get("height", 140.0)),
            }

    def _extract_semantic_tokens(self, text: str) -> Set[str]:
        """Extract clean lower-case semantic keywords filtered from stopwords."""
        stopwords = {
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "with",
            "by", "about", "against", "between", "into", "through", "during", "before",
            "after", "above", "below", "from", "up", "down", "of", "off", "over", "under",
            "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "do",
            "does", "did", "can", "could", "should", "would", "will", "this", "that", "these",
        }
        words = re.findall(r"[a-zA-Z0-9_\-\.]{3,}", text.lower())
        return {w for w in words if w not in stopwords and not w.isdigit()}

    def weave_bridges(self) -> Tuple[List[ResonanceBridge], ResonanceWeaverTelemetry]:
        """Discover latent conceptual connections and generate resonance bridges."""
        if not self.nodes:
            empty_telemetry = ResonanceWeaverTelemetry(
                total_nodes=0,
                existing_edges_count=0,
                discovered_bridges_count=0,
                mean_resonance_intensity=0.0,
                associative_density_lift_pct=0.0,
            )
            return [], empty_telemetry

        node_list = list(self.nodes.values())
        discovered: List[ResonanceBridge] = []
        node_bridge_counts: Dict[str, int] = {n["id"]: 0 for n in node_list}

        # Candidate pair evaluations
        candidate_pairs: List[Tuple[float, Dict[str, Any], Dict[str, Any], Set[str]]] = []

        for i in range(len(node_list)):
            for j in range(i + 1, len(node_list)):
                n1 = node_list[i]
                n2 = node_list[j]
                id1, id2 = n1["id"], n2["id"]

                # Skip existing connections
                if (id1, id2) in self.existing_edges or (id2, id1) in self.existing_edges:
                    continue

                tok1 = n1["tokens"]
                tok2 = n2["tokens"]
                if not tok1 or not tok2:
                    continue

                intersection = tok1.intersection(tok2)
                union = tok1.union(tok2)
                if not intersection or not union:
                    continue

                # Jaccard similarity augmented by shared token count
                jaccard = len(intersection) / len(union)
                raw_score = jaccard * 0.7 + min(0.3, len(intersection) * 0.08)
                score = min(1.0, raw_score)

                if score >= self.min_resonance_threshold:
                    candidate_pairs.append((score, n1, n2, intersection))

        # Sort candidate pairs by resonance intensity descending
        candidate_pairs.sort(key=lambda x: x[0], reverse=True)

        bridge_counter = 1
        for score, n1, n2, shared in candidate_pairs:
            id1, id2 = n1["id"], n2["id"]
            if node_bridge_counts[id1] >= self.max_bridges_per_node and node_bridge_counts[id2] >= self.max_bridges_per_node:
                continue

            # Determine category
            shared_list = sorted(list(shared))
            if len(shared_list) >= 3:
                cat = ResonanceCategory.INVARIANT_ALIGNMENT
                anchor_label = f"Invariant: {shared_list[0]}"
            elif any("dialectic" in w or "versus" in w or "tradeoff" in w for w in shared_list):
                cat = ResonanceCategory.DIALECTIC_COUNTERPART
                anchor_label = f"Polarity: {shared_list[0]}"
            elif score > 0.50:
                cat = ResonanceCategory.THEMATIC_SYNERGY
                anchor_label = f"Synergy: {shared_list[0]}"
            else:
                cat = ResonanceCategory.CROSS_DOMAIN_ANALOGY
                anchor_label = f"Analogy: {shared_list[0]}"

            b_id = f"bridge_{bridge_counter}"
            discovered.append(
                ResonanceBridge(
                    bridge_id=b_id,
                    source_id=id1,
                    source_title=n1["title"],
                    target_id=id2,
                    target_title=n2["title"],
                    resonance_score=score,
                    category=cat,
                    shared_concepts=shared_list[:4],
                    thematic_anchor_label=anchor_label,
                )
            )

            node_bridge_counts[id1] += 1
            node_bridge_counts[id2] += 1
            bridge_counter += 1

        existing_count = len(self.raw_canvas_edges)
        discovered_count = len(discovered)
        mean_intensity = (sum(b.resonance_score for b in discovered) / discovered_count) if discovered_count else 0.0
        lift_pct = (discovered_count / max(1, existing_count)) * 100.0 if existing_count else (discovered_count * 100.0)

        telemetry = ResonanceWeaverTelemetry(
            total_nodes=len(node_list),
            existing_edges_count=existing_count,
            discovered_bridges_count=discovered_count,
            mean_resonance_intensity=mean_intensity,
            associative_density_lift_pct=lift_pct,
            bridges=discovered,
        )

        return discovered, telemetry

    def to_canvas(
        self,
        output_path: Optional[str] = None,
        canvas_title: str = "Resonance Weaved Canvas",
    ) -> Dict[str, Any]:
        """Export weaved associative bridges and nodes to Obsidian .canvas structure."""
        bridges, telemetry = self.weave_bridges()

        canvas_nodes: List[Dict[str, Any]] = []
        for n in self.nodes.values():
            canvas_nodes.append({
                "id": n["id"],
                "x": n["x"],
                "y": n["y"],
                "width": n["width"],
                "height": n["height"],
                "type": "text",
                "text": n["text"],
            })

        combined_edges: List[Dict[str, Any]] = list(self.raw_canvas_edges)

        # Append discovered resonance edges
        for b in bridges:
            if b.category == ResonanceCategory.INVARIANT_ALIGNMENT:
                edge_color = "4"  # Green
            elif b.category == ResonanceCategory.DIALECTIC_COUNTERPART:
                edge_color = "2"  # Orange
            elif b.category == ResonanceCategory.THEMATIC_SYNERGY:
                edge_color = "5"  # Cyan
            else:
                edge_color = "6"  # Purple

            combined_edges.append({
                "id": b.bridge_id,
                "fromNode": b.source_id,
                "toNode": b.target_id,
                "label": f"[{b.thematic_anchor_label} ({b.resonance_score:.2f})]",
                "color": edge_color,
            })

        canvas_json = {
            "title": canvas_title,
            "nodes": canvas_nodes,
            "edges": combined_edges,
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
        """Render publication-grade SVG associative resonance mesh in dark titanium theme."""
        bridges, telemetry = self.weave_bridges()

        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
            f'width="{width}" height="{height}" style="background-color: #0B0F17; '
            f'font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif;">',
            '<defs>',
            '  <filter id="cardShadow" x="-10%" y="-10%" width="120%" height="120%">',
            '    <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#000000" flood-opacity="0.6"/>',
            '  </filter>',
            '</defs>',
            '<!-- Header -->',
            f'<text x="60" y="45" font-size="20" font-weight="700" fill="#F8FAFC">Spatial Bi-Directional Hyper-Link Resonance Weaver</text>',
            f'<text x="60" y="65" font-size="12" fill="#94A3B8">Discovered Bridges: {telemetry.discovered_bridges_count} | Mean Resonance: {telemetry.mean_resonance_intensity:.2f} | Connectivity Lift: +{telemetry.associative_density_lift_pct:.1f}%</text>',
            '<!-- Resonance Bridges -->',
        ]

        # Draw Resonance Bridge Arcs
        for b in bridges:
            s_node = self.nodes.get(b.source_id)
            t_node = self.nodes.get(b.target_id)
            if not s_node or not t_node:
                continue

            x1 = s_node["x"] + s_node["width"] / 2.0
            y1 = s_node["y"] + s_node["height"] / 2.0
            x2 = t_node["x"] + t_node["width"] / 2.0
            y2 = t_node["y"] + t_node["height"] / 2.0

            dx = x2 - x1
            dy = y2 - y1
            cx = (x1 + x2) / 2.0 - dy * 0.2
            cy = (y1 + y2) / 2.0 + dx * 0.2

            stroke_col = "#38BDF8" if b.category == ResonanceCategory.THEMATIC_SYNERGY else (
                "#10B981" if b.category == ResonanceCategory.INVARIANT_ALIGNMENT else "#C084FC"
            )

            svg_parts.append(
                f'<path d="M {x1:.1f} {y1:.1f} Q {cx:.1f} {cy:.1f} {x2:.1f} {y2:.1f}" '
                f'fill="none" stroke="{stroke_col}" stroke-width="2" stroke-dasharray="4,4" opacity="0.75"/>'
            )
            # Label at midpoint
            svg_parts.append(
                f'<rect x="{cx - 50:.1f}" y="{cy - 10:.1f}" width="100" height="18" rx="4" fill="#0F172A" stroke="{stroke_col}" stroke-width="1"/>'
            )
            svg_parts.append(
                f'<text x="{cx:.1f}" y="{cy + 2:.1f}" font-size="8" font-weight="700" fill="#E2E8F0" text-anchor="middle">{b.thematic_anchor_label[:14]}</text>'
            )

        # Draw Node Cards
        svg_parts.append('<!-- Spatial Node Cards -->')
        for n in self.nodes.values():
            svg_parts.append(
                f'<g transform="translate({n["x"]:.1f}, {n["y"]:.1f})" filter="url(#cardShadow)">'
                f'  <rect width="{n["width"]:.1f}" height="{n["height"]:.1f}" rx="8" fill="#1E293B" stroke="#334155" stroke-width="1.5"/>'
                f'  <text x="14" y="28" font-size="12" font-weight="700" fill="#F8FAFC">{n["title"][:18]}</text>'
                f'  <text x="14" y="48" font-size="10" fill="#94A3B8">Tokens: {len(n["tokens"])} keywords</text>'
                f'  <text x="14" y="66" font-size="9" fill="#64748B">Allocentric Hub</text>'
                f'</g>'
            )

        # Telemetry Legend
        legend_x = width - 260
        legend_y = height - 145
        svg_parts.append('<!-- Telemetry Legend -->')
        svg_parts.append(
            f'<rect x="{legend_x}" y="{legend_y}" width="230" height="115" rx="6" '
            f'fill="#0F172A" stroke="#1E293B" stroke-width="1"/>'
        )
        svg_parts.append(
            f'<text x="{legend_x + 12}" y="{legend_y + 22}" font-size="11" font-weight="700" fill="#F8FAFC">Resonance Weaver Metrics</text>'
        )
        svg_parts.append(
            f'<text x="{legend_x + 12}" y="{legend_y + 42}" font-size="10" fill="#64748B">Discovered Bridges: <tspan fill="#10B981">+{telemetry.discovered_bridges_count}</tspan></text>'
        )
        svg_parts.append(
            f'<text x="{legend_x + 12}" y="{legend_y + 60}" font-size="10" fill="#64748B">Mean Resonance: <tspan fill="#38BDF8">{telemetry.mean_resonance_intensity:.2f}</tspan></text>'
        )
        svg_parts.append(
            f'<text x="{legend_x + 12}" y="{legend_y + 78}" font-size="10" fill="#64748B">Network Density Lift: <tspan fill="#F59E0B">+{telemetry.associative_density_lift_pct:.1f}%</tspan></text>'
        )
        svg_parts.append(
            f'<text x="{legend_x + 12}" y="{legend_y + 98}" font-size="9" fill="#475569">Jaccard Semantic Affinity &amp; Invariants</text>'
        )

        svg_parts.append('</svg>')
        svg_content = "\n".join(svg_parts)

        if output_path:
            p = Path(output_path)
            p.parent.mkdir(parents=True, exist_ok=True)
            with open(p, "w", encoding="utf-8") as f:
                f.write(svg_content)

        return svg_content

    def render_ascii_bridges(self, telemetry: ResonanceWeaverTelemetry) -> str:
        """Format an accessible ASCII summary of discovered resonance bridges."""
        lines = [
            "=" * 68,
            "  Spatial Bi-Directional Hyper-Link Resonance Weaver Report",
            "=" * 68,
            f"  Total Canvas Nodes:             {telemetry.total_nodes}",
            f"  Existing Baseline Edges:        {telemetry.existing_edges_count}",
            f"  Discovered Resonance Bridges:   {telemetry.discovered_bridges_count}",
            f"  Mean Resonance Intensity:       {telemetry.mean_resonance_intensity:.2f}",
            f"  Associative Density Lift:       +{telemetry.associative_density_lift_pct:.1f}%",
            "-" * 68,
            "  [DISCOVERED ASSOCIATIVE BRIDGES]:",
        ]

        for b in telemetry.bridges:
            lines.append(f"    * [{b.category.value.upper()}] ({b.resonance_score:.2f}) {b.source_title} <---> {b.target_title}")
            lines.append(f"      Theme: {b.thematic_anchor_label} | Shared: {', '.join(b.shared_concepts)}")

        lines.append("=" * 68)
        return "\n".join(lines)
