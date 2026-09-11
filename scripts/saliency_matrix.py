"""Autonomous Cognitive Spatial Working Memory Saliency Decoupler & Attenuation Matrix.

Theoretical Foundation:
- Posner's Spatial Cueing & Eriksen Flanker Paradigms (Posner, 1980; Eriksen & St. James, 1986):
  In dyslexic and ADHD neurodivergent cognition, involuntary attentional capture by
  peripheral visual clutter severely degrades focal reasoning throughput.
  Unattenuated neighboring cards compete for foveal visual processing capacity.
- Multi-Tier Concentric Saliency Attenuation:
  Partitions canvas topologies into continuous visual saliency tiers centered around
  the active focal locus:
  - Tier 0: Focal Locus (100% luminance, high contrast, active anchor spotlight)
  - Tier 1: Context Neighbors (75% opacity, immediate topological dependencies)
  - Tier 2: Peripheral References (45% opacity, desaturated background cards)
  - Tier 3: Background Chatter (20% opacity, deeply muted ambient context)
- Exponential Spatial Decay Contrast Ramp:
  Applies smooth exponential decay based on Euclidean canvas distance and topological
  graph hop count, eliminating abrupt visual disconnections that cause allocentric
  disorientation while wiping out distracting cognitive noise.
- Dark Titanium SVG & Obsidian .canvas Export:
  Generates production-grade Obsidian .canvas files with color-tiered attenuation
  properties and dark titanium SVG diagrams with concentric spotlight illumination halos.

Strict Quality Gate: Zero em dashes anywhere (use hyphens, commas, or parentheses).
"""

from __future__ import annotations

import enum
import json
import math
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


class AttenuationTier(str, enum.Enum):
    """Concentric visual saliency and attenuation tier."""

    FOCAL_LOCUS = "focal_locus"
    CONTEXT_NEIGHBOR = "context_neighbor"
    PERIPHERAL_REF = "peripheral_ref"
    BACKGROUND_CHATTER = "background_chatter"


@dataclass
class SaliencyNode:
    """Represents a spatial canvas node evaluated for visual saliency attenuation."""

    node_id: str
    title: str
    x: float
    y: float
    width: float
    height: float
    distance_from_focus: float = 0.0
    hop_distance: int = 0
    opacity: float = 1.0
    contrast_ratio: float = 1.0
    tier: AttenuationTier = AttenuationTier.FOCAL_LOCUS

    def to_dict(self) -> Dict[str, Any]:
        """Convert node to serializable dictionary."""
        return {
            "node_id": self.node_id,
            "title": self.title,
            "x": round(self.x, 1),
            "y": round(self.y, 1),
            "width": round(self.width, 1),
            "height": round(self.height, 1),
            "distance_from_focus": round(self.distance_from_focus, 1),
            "hop_distance": self.hop_distance,
            "opacity": round(self.opacity, 2),
            "contrast_ratio": round(self.contrast_ratio, 2),
            "tier": self.tier.value,
        }


@dataclass
class SaliencyMatrixTelemetry:
    """Telemetry capturing visual attenuation and cognitive clutter suppression."""

    total_nodes: int
    focal_nodes_count: int
    attenuated_nodes_count: int
    peripheral_noise_reduction_pct: float
    focal_saliency_boost: float
    focal_node_id: str
    nodes: List[SaliencyNode] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert telemetry to JSON-compatible dictionary."""
        return {
            "total_nodes": self.total_nodes,
            "focal_nodes_count": self.focal_nodes_count,
            "attenuated_nodes_count": self.attenuated_nodes_count,
            "peripheral_noise_reduction_pct": round(self.peripheral_noise_reduction_pct, 1),
            "focal_saliency_boost": round(self.focal_saliency_boost, 2),
            "focal_node_id": self.focal_node_id,
            "nodes": [n.to_dict() for n in self.nodes],
        }


class SaliencyDecouplerMatrix:
    """Computes concentric saliency attenuation fields across spatial canvas layouts."""

    def __init__(self, decay_rate: float = 0.0018, hop_penalty: float = 0.22) -> None:
        self.decay_rate = decay_rate
        self.hop_penalty = hop_penalty
        self.nodes: Dict[str, SaliencyNode] = {}
        self.adjacency: Dict[str, Set[str]] = {}
        self.raw_edges: List[Dict[str, Any]] = []

    def load_dict(self, layout_data: Dict[str, Any]) -> None:
        """Load nodes and adjacency relationships from dictionary structure."""
        self.nodes.clear()
        self.adjacency.clear()
        self.raw_edges.clear()

        raw_nodes = layout_data.get("nodes", layout_data)
        for n_id, info in raw_nodes.items():
            if isinstance(info, dict):
                title = info.get("title", n_id)
                x = float(info.get("x", 0.0))
                y = float(info.get("y", 0.0))
                w = float(info.get("width", 260.0))
                h = float(info.get("height", 140.0))
                deps = list(info.get("dependencies", []))
            else:
                title = str(info)
                x = 0.0
                y = 0.0
                w = 260.0
                h = 140.0
                deps = []

            self.nodes[n_id] = SaliencyNode(
                node_id=n_id,
                title=title,
                x=x,
                y=y,
                width=w,
                height=h,
            )
            self.adjacency[n_id] = set(deps)

        if "edges" in layout_data:
            self.raw_edges = list(layout_data.get("edges", []))
            for e in self.raw_edges:
                src = e.get("fromNode")
                tgt = e.get("toNode")
                if src in self.adjacency and tgt:
                    self.adjacency[src].add(tgt)
                if tgt in self.adjacency and src:
                    self.adjacency[tgt].add(src)

    def load_canvas(self, canvas_data: Dict[str, Any]) -> None:
        """Extract nodes and edges from Obsidian .canvas format."""
        self.nodes.clear()
        self.adjacency.clear()
        self.raw_edges = list(canvas_data.get("edges", []))

        nodes = canvas_data.get("nodes", [])
        for node in nodes:
            n_id = str(node.get("id", ""))
            text = str(node.get("text", "")).strip()
            lines = [l.strip() for l in text.split("\n") if l.strip()]
            title = lines[0].lstrip("#").strip() if lines else n_id

            self.nodes[n_id] = SaliencyNode(
                node_id=n_id,
                title=title,
                x=float(node.get("x", 0.0)),
                y=float(node.get("y", 0.0)),
                width=float(node.get("width", 260.0)),
                height=float(node.get("height", 140.0)),
            )
            self.adjacency[n_id] = set()

        for e in self.raw_edges:
            src = str(e.get("fromNode", ""))
            tgt = str(e.get("toNode", ""))
            if src in self.adjacency and tgt in self.nodes:
                self.adjacency[src].add(tgt)
            if tgt in self.adjacency and src in self.nodes:
                self.adjacency[tgt].add(src)

    def attenuate(self, focal_node_id: Optional[str] = None) -> Tuple[List[SaliencyNode], SaliencyMatrixTelemetry]:
        """Compute multi-tier attenuation gradient radiating from designated focal node."""
        if not self.nodes:
            empty_telemetry = SaliencyMatrixTelemetry(
                total_nodes=0,
                focal_nodes_count=0,
                attenuated_nodes_count=0,
                peripheral_noise_reduction_pct=0.0,
                focal_saliency_boost=1.0,
                focal_node_id="",
            )
            return [], empty_telemetry

        # Choose primary focal node if not specified
        if not focal_node_id or focal_node_id not in self.nodes:
            focal_node_id = next(iter(self.nodes.keys()))

        focal = self.nodes[focal_node_id]
        focal_cx = focal.x + focal.width / 2.0
        focal_cy = focal.y + focal.height / 2.0

        # Breadth-first search for topological hop distance
        hop_distances: Dict[str, int] = {focal_node_id: 0}
        queue: List[str] = [focal_node_id]
        while queue:
            curr = queue.pop(0)
            curr_dist = hop_distances[curr]
            for neighbor in self.adjacency.get(curr, []):
                if neighbor in self.nodes and neighbor not in hop_distances:
                    hop_distances[neighbor] = curr_dist + 1
                    queue.append(neighbor)

        node_list: List[SaliencyNode] = list(self.nodes.values())
        attenuated_count = 0
        total_opacity_pre = len(node_list) * 1.0
        total_opacity_post = 0.0

        for n in node_list:
            if n.node_id == focal_node_id:
                n.distance_from_focus = 0.0
                n.hop_distance = 0
                n.opacity = 1.0
                n.contrast_ratio = 1.0
                n.tier = AttenuationTier.FOCAL_LOCUS
                total_opacity_post += 1.0
                continue

            # Compute Euclidean spatial distance
            cx = n.x + n.width / 2.0
            cy = n.y + n.height / 2.0
            euc_dist = math.sqrt((cx - focal_cx) ** 2 + (cy - focal_cy) ** 2)
            n.distance_from_focus = euc_dist

            hops = hop_distances.get(n.node_id, 3)
            n.hop_distance = hops

            # Smooth exponential decay: opacity decreases with Euclidean distance and hop count
            decay_factor = math.exp(-self.decay_rate * euc_dist)
            hop_factor = max(0.2, 1.0 - (hops * self.hop_penalty))
            calculated_opacity = max(0.18, min(0.95, decay_factor * hop_factor))
            n.opacity = calculated_opacity
            n.contrast_ratio = max(0.25, calculated_opacity * 1.1)
            total_opacity_post += calculated_opacity

            # Assign categorical tier
            if calculated_opacity >= 0.70:
                n.tier = AttenuationTier.CONTEXT_NEIGHBOR
            elif calculated_opacity >= 0.40:
                n.tier = AttenuationTier.PERIPHERAL_REF
            else:
                n.tier = AttenuationTier.BACKGROUND_CHATTER
                attenuated_count += 1

        noise_reduction_pct = max(0.0, ((total_opacity_pre - total_opacity_post) / total_opacity_pre)) * 100.0
        saliency_boost = round(min(3.5, 1.0 / max(0.2, (total_opacity_post / total_opacity_pre))), 2)

        telemetry = SaliencyMatrixTelemetry(
            total_nodes=len(node_list),
            focal_nodes_count=1,
            attenuated_nodes_count=attenuated_count,
            peripheral_noise_reduction_pct=noise_reduction_pct,
            focal_saliency_boost=saliency_boost,
            focal_node_id=focal_node_id,
            nodes=node_list,
        )

        return node_list, telemetry

    def to_canvas(
        self,
        focal_node_id: Optional[str] = None,
        output_path: Optional[str] = None,
        canvas_title: str = "Saliency Attenuation Canvas",
    ) -> Dict[str, Any]:
        """Export attenuated nodes to Obsidian .canvas with opacity tiers and badges."""
        nodes, telemetry = self.attenuate(focal_node_id)

        canvas_nodes: List[Dict[str, Any]] = []

        for n in nodes:
            if n.tier == AttenuationTier.FOCAL_LOCUS:
                color = "5"  # Cyan / Bright
                badge = "[ACTIVE FOCAL LOCUS]"
            elif n.tier == AttenuationTier.CONTEXT_NEIGHBOR:
                color = "4"  # Green
                badge = "[CONTEXT NEIGHBOR]"
            elif n.tier == AttenuationTier.PERIPHERAL_REF:
                color = "3"  # Yellow / Amber
                badge = "[PERIPHERAL REF]"
            else:
                color = "0"  # Dim Gray
                badge = "[BACKGROUND CHATTER]"

            content = (
                f"### {n.title} {badge}\n"
                f"**Opacity:** {n.opacity:.2f} | **Contrast:** {n.contrast_ratio:.2f}\n"
                f"**Distance:** {n.distance_from_focus:.0f}px (Hops: {n.hop_distance})\n"
                f"**Saliency Tier:** `{n.tier.value}`"
            )

            canvas_nodes.append({
                "id": n.node_id,
                "x": n.x,
                "y": n.y,
                "width": n.width,
                "height": n.height,
                "type": "text",
                "text": content,
                "color": color,
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
        focal_node_id: Optional[str] = None,
        output_path: Optional[str] = None,
        width: int = 1200,
        height: int = 800,
    ) -> str:
        """Render publication-grade SVG attenuation matrix in dark titanium theme."""
        nodes, telemetry = self.attenuate(focal_node_id)
        focal = next((n for n in nodes if n.node_id == telemetry.focal_node_id), nodes[0] if nodes else None)
        fcx = (focal.x + focal.width / 2.0) if focal else width / 2.0
        fcy = (focal.y + focal.height / 2.0) if focal else height / 2.0

        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
            f'width="{width}" height="{height}" style="background-color: #0B0F17; '
            f'font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif;">',
            '<defs>',
            '  <radialGradient id="focalSpotlight" cx="50%" cy="50%" r="50%">',
            '    <stop offset="0%" stop-color="#38BDF8" stop-opacity="0.25"/>',
            '    <stop offset="50%" stop-color="#38BDF8" stop-opacity="0.08"/>',
            '    <stop offset="100%" stop-color="#38BDF8" stop-opacity="0.0"/>',
            '  </radialGradient>',
            '  <filter id="focalGlow" x="-15%" y="-15%" width="130%" height="130%">',
            '    <feDropShadow dx="0" dy="0" stdDeviation="12" flood-color="#38BDF8" flood-opacity="0.6"/>',
            '  </filter>',
            '</defs>',
            '<!-- Header -->',
            f'<text x="60" y="45" font-size="20" font-weight="700" fill="#F8FAFC">Spatial Working Memory Saliency Decoupler &amp; Attenuation Matrix</text>',
            f'<text x="60" y="65" font-size="12" fill="#94A3B8">Focal Locus: {focal.title if focal else ""} | Chatter Suppression: -{telemetry.peripheral_noise_reduction_pct:.1f}% | Saliency Boost: {telemetry.focal_saliency_boost:.2f}x</text>',
            '<!-- Concentric Attenuation Spotlights -->',
            f'<circle cx="{fcx:.1f}" cy="{fcy:.1f}" r="450" fill="url(#focalSpotlight)"/>',
            f'<circle cx="{fcx:.1f}" cy="{fcy:.1f}" r="220" fill="none" stroke="#38BDF8" stroke-width="1" stroke-dasharray="4,4" opacity="0.4"/>',
            f'<circle cx="{fcx:.1f}" cy="{fcy:.1f}" r="420" fill="none" stroke="#64748B" stroke-width="1" stroke-dasharray="3,3" opacity="0.25"/>',
            '<!-- Node Cards -->',
        ]

        for n in nodes:
            is_focal = (n.tier == AttenuationTier.FOCAL_LOCUS)
            filter_attr = 'filter="url(#focalGlow)"' if is_focal else ""
            stroke_col = "#38BDF8" if is_focal else ("#10B981" if n.tier == AttenuationTier.CONTEXT_NEIGHBOR else "#475569")
            stroke_w = "2.5" if is_focal else "1.5"

            svg_parts.append(
                f'<g transform="translate({n.x:.1f}, {n.y:.1f})" opacity="{n.opacity:.2f}" {filter_attr}>'
                f'  <rect width="{n.width:.1f}" height="{n.height:.1f}" rx="8" fill="#1E293B" stroke="{stroke_col}" stroke-width="{stroke_w}"/>'
                f'  <text x="14" y="28" font-size="12" font-weight="700" fill="#F8FAFC">{n.title[:18]}</text>'
                f'  <text x="14" y="48" font-size="10" fill="#94A3B8">Opacity: <tspan fill="{stroke_col}">{n.opacity:.2f}</tspan> | Dist: {n.distance_from_focus:.0f}px</text>'
                f'  <text x="14" y="66" font-size="9" fill="#64748B">Tier: {n.tier.value}</text>'
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
            f'<text x="{legend_x + 12}" y="{legend_y + 22}" font-size="11" font-weight="700" fill="#F8FAFC">Saliency Decoupler Metrics</text>'
        )
        svg_parts.append(
            f'<text x="{legend_x + 12}" y="{legend_y + 42}" font-size="10" fill="#64748B">Total Cards: <tspan fill="#F8FAFC">{telemetry.total_nodes}</tspan></text>'
        )
        svg_parts.append(
            f'<text x="{legend_x + 12}" y="{legend_y + 60}" font-size="10" fill="#64748B">Chatter Relief: <tspan fill="#10B981">-{telemetry.peripheral_noise_reduction_pct:.1f}%</tspan></text>'
        )
        svg_parts.append(
            f'<text x="{legend_x + 12}" y="{legend_y + 78}" font-size="10" fill="#64748B">Saliency Ratio: <tspan fill="#38BDF8">{telemetry.focal_saliency_boost:.2f}x</tspan></text>'
        )
        svg_parts.append(
            f'<text x="{legend_x + 12}" y="{legend_y + 98}" font-size="9" fill="#475569">Concentric Exponential Attenuation</text>'
        )

        svg_parts.append('</svg>')
        svg_content = "\n".join(svg_parts)

        if output_path:
            p = Path(output_path)
            p.parent.mkdir(parents=True, exist_ok=True)
            with open(p, "w", encoding="utf-8") as f:
                f.write(svg_content)

        return svg_content

    def render_ascii_matrix(self, telemetry: SaliencyMatrixTelemetry) -> str:
        """Format an accessible ASCII summary of visual attenuation tiers."""
        lines = [
            "=" * 68,
            "  Spatial Working Memory Saliency Decoupler & Attenuation Matrix",
            "=" * 68,
            f"  Total Canvas Nodes:           {telemetry.total_nodes}",
            f"  Active Focal Node ID:         {telemetry.focal_node_id}",
            f"  Muted Chatter Nodes:          {telemetry.attenuated_nodes_count}",
            f"  Peripheral Noise Reduction:   -{telemetry.peripheral_noise_reduction_pct:.1f}%",
            f"  Focal Saliency Boost:         {telemetry.focal_saliency_boost:.2f}x",
            "-" * 68,
            "  [CONCENTRIC ATTENUATION TIERS]:",
        ]

        for n in telemetry.nodes:
            lines.append(f"    * [{n.tier.value.upper()}] {n.title}")
            lines.append(f"      Opacity: {n.opacity:.2f} | Contrast: {n.contrast_ratio:.2f} | Dist: {n.distance_from_focus:.0f}px (Hops: {n.hop_distance})")

        lines.append("=" * 68)
        return "\n".join(lines)
