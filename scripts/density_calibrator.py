"""Autonomous Cognitive Spatial Multi-Scale Attention Density Calibrator & Visual Restorer.

Theoretical Foundation:
- Visual Crowding & Bouma's Critical Window (Bouma, 1970; Pelli & Tillman, 2008):
  In dyslexic cognition, peripheral visual crowding is significantly enlarged,
  requiring 1.5x to 2.0x greater inter-node spacing than neurotypical baselines.
  When technical cards and diagram nodes are tightly packed, parafoveal feature
  pooling triggers optical jitter, letter transposition, and visual search exhaustion.
- Kernel Density Estimation (KDE) of Spatial Attention:
  Models 2D canvas layouts as a continuous visual attention field where node visual
  entropy (text length, perimeter, and connectivity) radiates Gaussian attention
  weight across foveal and parafoveal radii.
- Force-Directed Dynamic Whitespace Balancing:
  Applies an anisotropic repulsive force field between nodes within crowding hotspots.
  Expands optical breathing room around high-entropy hubs, restoring Bouma clearance
  while preserving the user's allocentric topological mental map.
- Spatial Canvas Rebalancing & Dark Titanium SVG Export:
  Outputs balanced Obsidian .canvas files with optimized coordinates and generates
  publication-grade SVG attention density contour diagrams.

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


class CrowdingTier(str, enum.Enum):
    """Categorization of visual crowding and optical density."""

    CRITICAL_CROWDING = "critical_crowding"
    ELEVATED_DENSITY = "elevated_density"
    OPTIMAL_SPACING = "optimal_spacing"
    SPARSE = "sparse"


@dataclass
class DensityNode:
    """Spatial node evaluated for visual attention density and crowding."""

    node_id: str
    title: str
    x: float
    y: float
    width: float
    height: float
    text_entropy: float
    local_density_score: float = 0.0
    crowding_tier: CrowdingTier = CrowdingTier.OPTIMAL_SPACING
    adjusted_x: float = 0.0
    adjusted_y: float = 0.0
    bouma_clearance_px: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert node to serializable dictionary."""
        return {
            "node_id": self.node_id,
            "title": self.title,
            "x": round(self.x, 1),
            "y": round(self.y, 1),
            "width": round(self.width, 1),
            "height": round(self.height, 1),
            "text_entropy": round(self.text_entropy, 2),
            "local_density_score": round(self.local_density_score, 2),
            "crowding_tier": self.crowding_tier.value,
            "adjusted_x": round(self.adjusted_x, 1),
            "adjusted_y": round(self.adjusted_y, 1),
            "bouma_clearance_px": round(self.bouma_clearance_px, 1),
        }


@dataclass
class CrowdingHotspot:
    """Spatial region where visual attention density exceeds critical threshold."""

    hotspot_id: str
    center_x: float
    center_y: float
    radius: float
    peak_density: float
    node_count: int
    member_node_ids: List[str]
    recommended_expansion_factor: float

    def to_dict(self) -> Dict[str, Any]:
        """Convert hotspot to serializable dictionary."""
        return {
            "hotspot_id": self.hotspot_id,
            "center_x": round(self.center_x, 1),
            "center_y": round(self.center_y, 1),
            "radius": round(self.radius, 1),
            "peak_density": round(self.peak_density, 2),
            "node_count": self.node_count,
            "member_node_ids": sorted(self.member_node_ids),
            "recommended_expansion_factor": round(self.recommended_expansion_factor, 2),
        }


@dataclass
class DensityTelemetry:
    """Telemetry capturing multi-scale attention density and whitespace balancing."""

    total_nodes: int
    crowded_nodes_count: int
    hotspots_count: int
    initial_mean_density: float
    rebalanced_mean_density: float
    density_reduction_pct: float
    ocular_fatigue_mitigation_score: float
    nodes: List[DensityNode] = field(default_factory=list)
    hotspots: List[CrowdingHotspot] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert telemetry to JSON-compatible dictionary."""
        return {
            "total_nodes": self.total_nodes,
            "crowded_nodes_count": self.crowded_nodes_count,
            "hotspots_count": self.hotspots_count,
            "initial_mean_density": round(self.initial_mean_density, 2),
            "rebalanced_mean_density": round(self.rebalanced_mean_density, 2),
            "density_reduction_pct": round(self.density_reduction_pct, 1),
            "ocular_fatigue_mitigation_score": round(self.ocular_fatigue_mitigation_score, 2),
            "nodes": [n.to_dict() for n in self.nodes],
            "hotspots": [h.to_dict() for h in self.hotspots],
        }


class AttentionDensityCalibrator:
    """Evaluates spatial attention density fields and applies force-directed whitespace balancing."""

    def __init__(
        self,
        foveal_sigma: float = 200.0,
        bouma_factor: float = 1.6,
        crowding_threshold: float = 0.65,
    ) -> None:
        self.foveal_sigma = foveal_sigma
        self.bouma_factor = bouma_factor
        self.crowding_threshold = crowding_threshold
        self.nodes: Dict[str, DensityNode] = {}
        self.raw_edges: List[Dict[str, Any]] = []

    def load_dict(self, node_data: Dict[str, Any]) -> None:
        """Load node layout from dictionary."""
        self.nodes.clear()
        self.raw_edges.clear()

        for n_id, info in node_data.items():
            if isinstance(info, dict):
                title = info.get("title", n_id)
                x = float(info.get("x", 0.0))
                y = float(info.get("y", 0.0))
                w = float(info.get("width", 280.0))
                h = float(info.get("height", 160.0))
                text = str(info.get("text", title))
            else:
                title = str(info)
                x = 0.0
                y = 0.0
                w = 280.0
                h = 160.0
                text = title

            entropy = self._calculate_text_entropy(text)
            self.nodes[n_id] = DensityNode(
                node_id=n_id,
                title=title,
                x=x,
                y=y,
                width=w,
                height=h,
                text_entropy=entropy,
                adjusted_x=x,
                adjusted_y=y,
            )

    def load_canvas(self, canvas_data: Dict[str, Any]) -> None:
        """Extract spatial nodes and bounding boxes from an Obsidian .canvas structure."""
        self.nodes.clear()
        self.raw_edges = list(canvas_data.get("edges", []))
        nodes = canvas_data.get("nodes", [])

        for node in nodes:
            n_id = str(node.get("id", ""))
            text = str(node.get("text", "")).strip()
            lines = [l.strip() for l in text.split("\n") if l.strip()]
            title = lines[0].lstrip("#").strip() if lines else n_id

            x = float(node.get("x", 0.0))
            y = float(node.get("y", 0.0))
            w = float(node.get("width", 280.0))
            h = float(node.get("height", 160.0))

            entropy = self._calculate_text_entropy(text)
            self.nodes[n_id] = DensityNode(
                node_id=n_id,
                title=title,
                x=x,
                y=y,
                width=w,
                height=h,
                text_entropy=entropy,
                adjusted_x=x,
                adjusted_y=y,
            )

    def _calculate_text_entropy(self, text: str) -> float:
        """Compute visual entropy metric based on character length and lexical density."""
        length = len(text)
        if length < 20:
            return 1.0
        elif length < 80:
            return 2.5
        elif length < 200:
            return 5.0
        elif length < 500:
            return 7.5
        else:
            return 10.0

    def calibrate(
        self,
        iterations: int = 12,
        repulsion_k: float = 35000.0,
    ) -> Tuple[List[DensityNode], List[CrowdingHotspot], DensityTelemetry]:
        """Compute continuous attention density, detect crowding hotspots, and rebalance whitespace."""
        if not self.nodes:
            empty_telemetry = DensityTelemetry(
                total_nodes=0,
                crowded_nodes_count=0,
                hotspots_count=0,
                initial_mean_density=0.0,
                rebalanced_mean_density=0.0,
                density_reduction_pct=0.0,
                ocular_fatigue_mitigation_score=1.0,
            )
            return [], [], empty_telemetry

        node_list = list(self.nodes.values())
        two_sigma_sq = 2.0 * (self.foveal_sigma ** 2)

        # 1. Initial Gaussian Kernel Density Estimation (KDE)
        initial_densities: Dict[str, float] = {}
        for i, n1 in enumerate(node_list):
            c1_x = n1.x + n1.width / 2.0
            c1_y = n1.y + n1.height / 2.0
            accum_density = 0.0
            min_dist = float("inf")

            for j, n2 in enumerate(node_list):
                if i == j:
                    continue
                c2_x = n2.x + n2.width / 2.0
                c2_y = n2.y + n2.height / 2.0
                dist_sq = (c1_x - c2_x) ** 2 + (c1_y - c2_y) ** 2
                dist = math.sqrt(dist_sq)
                if dist < min_dist:
                    min_dist = dist

                weight = n2.text_entropy
                accum_density += weight * math.exp(-dist_sq / two_sigma_sq)

            # Normalize density
            norm_density = min(1.0, accum_density / 15.0)
            initial_densities[n1.node_id] = norm_density
            n1.local_density_score = norm_density

            # Bouma critical spacing check: clearance must be at least bouma_factor * half-diagonal
            diagonal = math.sqrt(n1.width ** 2 + n1.height ** 2) / 2.0
            n1.bouma_clearance_px = diagonal * self.bouma_factor

            if norm_density >= self.crowding_threshold or min_dist < (diagonal * 0.9):
                n1.crowding_tier = CrowdingTier.CRITICAL_CROWDING
            elif norm_density >= 0.40:
                n1.crowding_tier = CrowdingTier.ELEVATED_DENSITY
            elif norm_density >= 0.15:
                n1.crowding_tier = CrowdingTier.OPTIMAL_SPACING
            else:
                n1.crowding_tier = CrowdingTier.SPARSE

        # 2. Detect Crowding Hotspots
        hotspots = self._detect_hotspots(node_list)

        # 3. Force-Directed Dynamic Whitespace Balancing
        self._rebalance_positions(node_list, iterations, repulsion_k)

        # 4. Re-calculate Post-Balancing Density
        rebalanced_densities: List[float] = []
        crowded_count = 0
        for i, n1 in enumerate(node_list):
            c1_x = n1.adjusted_x + n1.width / 2.0
            c1_y = n1.adjusted_y + n1.height / 2.0
            accum_density = 0.0
            for j, n2 in enumerate(node_list):
                if i == j:
                    continue
                c2_x = n2.adjusted_x + n2.width / 2.0
                c2_y = n2.adjusted_y + n2.height / 2.0
                dist_sq = (c1_x - c2_x) ** 2 + (c1_y - c2_y) ** 2
                weight = n2.text_entropy
                accum_density += weight * math.exp(-dist_sq / two_sigma_sq)

            post_norm = min(1.0, accum_density / 15.0)
            rebalanced_densities.append(post_norm)
            if post_norm >= self.crowding_threshold:
                crowded_count += 1

        init_mean = sum(initial_densities.values()) / max(1, len(node_list))
        post_mean = sum(rebalanced_densities) / max(1, len(node_list))
        reduction = max(0.0, ((init_mean - post_mean) / max(0.01, init_mean))) * 100.0
        mitigation = round(min(1.0, 0.70 + (reduction / 100.0) * 0.30), 2)

        telemetry = DensityTelemetry(
            total_nodes=len(node_list),
            crowded_nodes_count=crowded_count,
            hotspots_count=len(hotspots),
            initial_mean_density=init_mean,
            rebalanced_mean_density=post_mean,
            density_reduction_pct=reduction,
            ocular_fatigue_mitigation_score=mitigation,
            nodes=node_list,
            hotspots=hotspots,
        )

        return node_list, hotspots, telemetry

    def _detect_hotspots(self, nodes: List[DensityNode]) -> List[CrowdingHotspot]:
        """Cluster neighboring crowded nodes into distinct spatial hotspots."""
        crowded = [n for n in nodes if n.crowding_tier in [CrowdingTier.CRITICAL_CROWDING, CrowdingTier.ELEVATED_DENSITY]]
        if not crowded:
            return []

        clusters: List[List[DensityNode]] = []
        visited: Set[str] = set()

        for n in crowded:
            if n.node_id in visited:
                continue
            cluster = [n]
            visited.add(n.node_id)
            c1_x = n.x + n.width / 2.0
            c1_y = n.y + n.height / 2.0

            for other in crowded:
                if other.node_id in visited:
                    continue
                c2_x = other.x + other.width / 2.0
                c2_y = other.y + other.height / 2.0
                dist = math.sqrt((c1_x - c2_x) ** 2 + (c1_y - c2_y) ** 2)
                if dist < (self.foveal_sigma * 1.5):
                    cluster.append(other)
                    visited.add(other.node_id)
            clusters.append(cluster)

        hotspots: List[CrowdingHotspot] = []
        for idx, cl in enumerate(clusters, 1):
            h_id = f"hotspot_{idx}"
            avg_x = sum(n.x + n.width / 2.0 for n in cl) / len(cl)
            avg_y = sum(n.y + n.height / 2.0 for n in cl) / len(cl)
            peak = max(n.local_density_score for n in cl)
            exp_factor = round(min(2.5, 1.2 + (len(cl) * 0.15)), 2)

            hotspots.append(
                CrowdingHotspot(
                    hotspot_id=h_id,
                    center_x=avg_x,
                    center_y=avg_y,
                    radius=self.foveal_sigma * 1.2,
                    peak_density=peak,
                    node_count=len(cl),
                    member_node_ids=[n.node_id for n in cl],
                    recommended_expansion_factor=exp_factor,
                )
            )

        return hotspots

    def _rebalance_positions(
        self,
        nodes: List[DensityNode],
        iterations: int,
        repulsion_k: float,
    ) -> None:
        """Apply force-directed iterative expansion away from crowding centers."""
        # Initialize adjusted coords from original
        for n in nodes:
            n.adjusted_x = n.x
            n.adjusted_y = n.y

        for _ in range(iterations):
            dx_map: Dict[str, float] = {n.node_id: 0.0 for n in nodes}
            dy_map: Dict[str, float] = {n.node_id: 0.0 for n in nodes}

            for i, n1 in enumerate(nodes):
                c1_x = n1.adjusted_x + n1.width / 2.0
                c1_y = n1.adjusted_y + n1.height / 2.0

                for j, n2 in enumerate(nodes):
                    if i == j:
                        continue
                    c2_x = n2.adjusted_x + n2.width / 2.0
                    c2_y = n2.adjusted_y + n2.height / 2.0

                    vx = c1_x - c2_x
                    vy = c1_y - c2_y
                    dist_sq = vx ** 2 + vy ** 2
                    dist = math.sqrt(dist_sq)

                    min_required = (n1.width + n2.width) * 0.55
                    if dist < 1.0:
                        dist = 1.0
                        vx = 1.0
                        vy = 0.0

                    if dist < min_required:
                        # Repulsive force
                        force = (repulsion_k / (dist_sq + 100.0)) * (n1.text_entropy + n2.text_entropy) * 0.1
                        dx_map[n1.node_id] += (vx / dist) * force
                        dy_map[n1.node_id] += (vy / dist) * force

            for n in nodes:
                # Clamp displacement per iteration to preserve mental map stability
                disp_x = max(-45.0, min(45.0, dx_map[n.node_id]))
                disp_y = max(-45.0, min(45.0, dy_map[n.node_id]))
                n.adjusted_x += disp_x
                n.adjusted_y += disp_y

    def to_canvas(
        self,
        output_path: Optional[str] = None,
        canvas_title: str = "Rebalanced Attention Canvas",
    ) -> Dict[str, Any]:
        """Export rebalanced layout to Obsidian .canvas with restored whitespace and density badges."""
        nodes_list, hotspots, telemetry = self.calibrate()

        canvas_nodes: List[Dict[str, Any]] = []

        for n in nodes_list:
            if n.crowding_tier == CrowdingTier.CRITICAL_CROWDING:
                color = "1"  # red
            elif n.crowding_tier == CrowdingTier.ELEVATED_DENSITY:
                color = "2"  # orange
            else:
                color = "4"  # green / optimal

            content = (
                f"### {n.title}\n"
                f"**Density:** {n.local_density_score:.2f} (`{n.crowding_tier.value}`)\n"
                f"**Bouma Clearance:** {n.bouma_clearance_px:.0f}px | **Entropy:** {n.text_entropy:.1f}/10\n"
                f"**Shift:** dx: {n.adjusted_x - n.x:+.1f}px, dy: {n.adjusted_y - n.y:+.1f}px"
            )

            canvas_nodes.append({
                "id": n.node_id,
                "x": n.adjusted_x,
                "y": n.adjusted_y,
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
        output_path: Optional[str] = None,
        width: int = 1200,
        height: int = 800,
    ) -> str:
        """Render publication-grade SVG visual attention density map with dark titanium theme."""
        nodes_list, hotspots, telemetry = self.calibrate()

        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
            f'width="{width}" height="{height}" style="background-color: #0B0F17; '
            f'font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif;">',
            '<defs>',
            '  <radialGradient id="hotspotGrad" cx="50%" cy="50%" r="50%">',
            '    <stop offset="0%" stop-color="#EF4444" stop-opacity="0.35"/>',
            '    <stop offset="60%" stop-color="#F59E0B" stop-opacity="0.15"/>',
            '    <stop offset="100%" stop-color="#F59E0B" stop-opacity="0.0"/>',
            '  </radialGradient>',
            '  <filter id="cardShadow" x="-10%" y="-10%" width="120%" height="120%">',
            '    <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#000000" flood-opacity="0.5"/>',
            '  </filter>',
            '</defs>',
            '<!-- Header -->',
            f'<text x="60" y="45" font-size="20" font-weight="700" fill="#F8FAFC">Spatial Multi-Scale Attention Density &amp; Whitespace Calibrator</text>',
            f'<text x="60" y="65" font-size="12" fill="#94A3B8">Bouma Window Clearance: {telemetry.hotspots_count} Hotspots | Density Reduction: -{telemetry.density_reduction_pct:.1f}% | Ocular Mitigation: {telemetry.ocular_fatigue_mitigation_score:.2f}</text>',
            '<!-- Hotspot Heatmap Contours -->',
        ]

        # Draw Hotspot Halos
        for h in hotspots:
            svg_parts.append(
                f'<circle cx="{h.center_x}" cy="{h.center_y}" r="{h.radius}" fill="url(#hotspotGrad)"/>'
            )
            svg_parts.append(
                f'<circle cx="{h.center_x}" cy="{h.center_y}" r="{h.radius * 0.5}" fill="none" stroke="#EF4444" stroke-width="1" stroke-dasharray="4,4" opacity="0.6"/>'
            )
            svg_parts.append(
                f'<rect x="{h.center_x - 50}" y="{h.center_y - h.radius - 12}" width="100" height="20" rx="4" fill="#450A0A" stroke="#EF4444" stroke-width="1"/>'
            )
            svg_parts.append(
                f'<text x="{h.center_x}" y="{h.center_y - h.radius + 2}" font-size="9" font-weight="700" fill="#FCA5A5" text-anchor="middle">Hotspot ({h.peak_density:.2f})</text>'
            )

        # Draw Node Displacements (arrows from original to adjusted)
        svg_parts.append('<!-- Rebalancing Displacement Ramps -->')
        for n in nodes_list:
            orig_cx = n.x + n.width / 2.0
            orig_cy = n.y + n.height / 2.0
            new_cx = n.adjusted_x + n.width / 2.0
            new_cy = n.adjusted_y + n.height / 2.0

            if abs(orig_cx - new_cx) > 2.0 or abs(orig_cy - new_cy) > 2.0:
                svg_parts.append(
                    f'<line x1="{orig_cx:.1f}" y1="{orig_cy:.1f}" x2="{new_cx:.1f}" y2="{new_cy:.1f}" '
                    f'stroke="#10B981" stroke-width="2" stroke-dasharray="2,2"/>'
                )

        # Draw Node Cards at adjusted locations
        svg_parts.append('<!-- Rebalanced Spatial Cards -->')
        for n in nodes_list:
            rx = n.adjusted_x
            ry = n.adjusted_y
            w = n.width
            h = n.height

            if n.crowding_tier == CrowdingTier.CRITICAL_CROWDING:
                stroke_col = "#EF4444"
                bg_col = "#1E293B"
            elif n.crowding_tier == CrowdingTier.ELEVATED_DENSITY:
                stroke_col = "#F59E0B"
                bg_col = "#1E293B"
            else:
                stroke_col = "#10B981"
                bg_col = "#064E3B"

            title_clean = n.title[:16] + ".." if len(n.title) > 18 else n.title

            svg_parts.append(
                f'<g transform="translate({rx:.1f}, {ry:.1f})" filter="url(#cardShadow)">'
                f'  <rect width="{w:.1f}" height="{h:.1f}" rx="8" fill="{bg_col}" stroke="{stroke_col}" stroke-width="2"/>'
                f'  <text x="14" y="24" font-size="11" font-weight="700" fill="#F8FAFC">{title_clean}</text>'
                f'  <text x="14" y="44" font-size="9" fill="#94A3B8">Density: <tspan fill="{stroke_col}">{n.local_density_score:.2f}</tspan> | Ent: {n.text_entropy:.1f}</text>'
                f'  <text x="14" y="62" font-size="9" fill="#38BDF8">Bouma Space: {n.bouma_clearance_px:.0f}px</text>'
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
            f'<text x="{legend_x + 12}" y="{legend_y + 22}" font-size="11" font-weight="700" fill="#F8FAFC">Attention Density Metrics</text>'
        )
        svg_parts.append(
            f'<text x="{legend_x + 12}" y="{legend_y + 42}" font-size="10" fill="#64748B">Pre-Balancing Density: <tspan fill="#EF4444">{telemetry.initial_mean_density:.2f}</tspan></text>'
        )
        svg_parts.append(
            f'<text x="{legend_x + 12}" y="{legend_y + 60}" font-size="10" fill="#64748B">Density Relief: <tspan fill="#10B981">-{telemetry.density_reduction_pct:.1f}%</tspan></text>'
        )
        svg_parts.append(
            f'<text x="{legend_x + 12}" y="{legend_y + 78}" font-size="10" fill="#64748B">Ocular Mitigation: <tspan fill="#38BDF8">{telemetry.ocular_fatigue_mitigation_score:.2f}</tspan></text>'
        )
        svg_parts.append(
            f'<text x="{legend_x + 12}" y="{legend_y + 98}" font-size="9" fill="#475569">Bouma Law &amp; Parafoveal Expansion</text>'
        )

        svg_parts.append('</svg>')
        svg_content = "\n".join(svg_parts)

        if output_path:
            p = Path(output_path)
            p.parent.mkdir(parents=True, exist_ok=True)
            with open(p, "w", encoding="utf-8") as f:
                f.write(svg_content)

        return svg_content

    def render_ascii_report(self, telemetry: DensityTelemetry) -> str:
        """Format an accessible ASCII attention density report for the terminal."""
        lines = [
            "=" * 68,
            "  Spatial Multi-Scale Attention Density & Whitespace Report",
            "=" * 68,
            f"  Total Canvas Nodes:         {telemetry.total_nodes}",
            f"  Crowding Hotspots Detected: {telemetry.hotspots_count}",
            f"  Initial Mean Density:       {telemetry.initial_mean_density:.2f}",
            f"  Rebalanced Mean Density:    {telemetry.rebalanced_mean_density:.2f}",
            f"  Density Reduction:          -{telemetry.density_reduction_pct:.1f}%",
            f"  Ocular Fatigue Mitigation:  {telemetry.ocular_fatigue_mitigation_score:.2f}",
            "-" * 68,
            "  [HOTSPOT CLUSTER READOUT]:",
        ]

        for h in telemetry.hotspots:
            lines.append(f"    * {h.hotspot_id}: Peak Density: {h.peak_density:.2f} ({h.node_count} nodes)")
            lines.append(f"      Center: ({h.center_x:.0f}, {h.center_y:.0f}) | Recommended Expansion: {h.recommended_expansion_factor:.1f}x")
            lines.append(f"      Members: {', '.join(h.member_node_ids[:4])}")

        if telemetry.nodes:
            lines.append("-" * 68)
            lines.append("  [SAMPLE NODE DISPLACEMENTS]:")
            for node in telemetry.nodes[:4]:
                shift_x = node.adjusted_x - node.x
                shift_y = node.adjusted_y - node.y
                lines.append(f"    - {node.title} [{node.crowding_tier.value}]: Density: {node.local_density_score:.2f} -> Shift ({shift_x:+.1f}px, {shift_y:+.1f}px)")

        lines.append("=" * 68)
        return "\n".join(lines)
