"""
Morphological Semantic Lens and Granularity Zoom Engine
Autonomous cognitive spatial module providing continuous multi-resolution semantic zoom
between macro architectural topologies and atomic code primitives.
Grounded in Lavie perceptual load theory, Cowan working memory limits (N <= 4),
and multi-tier visual LOD (Level of Detail) smoothing to eliminate cognitive jarring.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Any
import math
import html


@dataclass
class SemanticNode:
    """Represents a conceptual or structural node within a multiscale knowledge hierarchy."""
    node_id: str
    label: str
    granularity_level: str  # MACRO_ARCHITECTURAL, MESO_SUBSYSTEM, MICRO_COMPONENT, ATOMIC_PRIMITIVE
    abstraction_depth: float  # 0.0 (macro apex) to 1.0 (atomic base)
    x: float  # X coordinate in canvas space (px)
    y: float  # Y coordinate in canvas space (px)
    importance_weight: float = 1.0  # 0.1 to 1.0
    details: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_id": self.node_id,
            "label": self.label,
            "granularity_level": self.granularity_level,
            "abstraction_depth": round(self.abstraction_depth, 3),
            "x": round(self.x, 1),
            "y": round(self.y, 1),
            "importance_weight": round(self.importance_weight, 2),
            "details": self.details,
        }


@dataclass
class MorphologicalNodeView:
    """Calibrated perceptual rendering state for a semantic node under current lens focus."""
    node: SemanticNode
    distance_to_focus_px: float
    apparent_scale: float
    apparent_lod: str
    opacity: float
    is_in_foveal_focus: bool
    is_in_parafoveal_zone: bool
    visible_detail_count: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node": self.node.to_dict(),
            "distance_to_focus_px": round(self.distance_to_focus_px, 1),
            "apparent_scale": round(self.apparent_scale, 3),
            "apparent_lod": self.apparent_lod,
            "opacity": round(self.opacity, 3),
            "is_in_foveal_focus": self.is_in_foveal_focus,
            "is_in_parafoveal_zone": self.is_in_parafoveal_zone,
            "visible_detail_count": self.visible_detail_count,
        }


@dataclass
class MorphologicalLensTelemetry:
    """Synthesized telemetry summarizing multi-scale semantic zoom and cognitive load."""
    zoom_factor: float
    focus_center: Tuple[float, float]
    focal_radius_px: float
    active_primary_lod: str
    foveal_node_count: int
    parafoveal_node_count: int
    peripheral_node_count: int
    cognitive_density_score: float  # 0.0 to 100.0 (penalizes Cowan limit violations)
    perceptual_load_ratio: float    # 0.0 (sparse) to 1.0 (overload threshold)
    status_level: str               # OPTIMAL_COGNITIVE_LOAD, PERCEPTUAL_OVERLOAD, SPARSE_GRANULARITY
    views: List[MorphologicalNodeView]
    warnings: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "zoom_factor": round(self.zoom_factor, 2),
            "focus_center": [round(c, 1) for c in self.focus_center],
            "focal_radius_px": round(self.focal_radius_px, 1),
            "active_primary_lod": self.active_primary_lod,
            "foveal_node_count": self.foveal_node_count,
            "parafoveal_node_count": self.parafoveal_node_count,
            "peripheral_node_count": self.peripheral_node_count,
            "cognitive_density_score": round(self.cognitive_density_score, 1),
            "perceptual_load_ratio": round(self.perceptual_load_ratio, 3),
            "status_level": self.status_level,
            "views": [v.to_dict() for v in self.views],
            "warnings": self.warnings,
        }


class MorphologicalSemanticLens:
    """
    Computes continuous multi-resolution semantic transitions, progressive detail disclosure,
    and Cowan capacity preservation across hierarchical information topographies.
    """

    LOD_ORDER = ["MACRO_ARCHITECTURAL", "MESO_SUBSYSTEM", "MICRO_COMPONENT", "ATOMIC_PRIMITIVE"]

    def __init__(
        self,
        base_focal_radius_px: float = 140.0,
        parafoveal_expansion_ratio: float = 1.75,
        max_cowan_foveal_capacity: int = 4,
        min_zoom: float = 0.2,
        max_zoom: float = 5.0,
    ):
        self.base_focal_radius_px = max(60.0, min(300.0, base_focal_radius_px))
        self.parafoveal_expansion_ratio = max(1.2, min(3.0, parafoveal_expansion_ratio))
        self.max_cowan_foveal_capacity = max(2, min(7, max_cowan_foveal_capacity))
        self.min_zoom = min_zoom
        self.max_zoom = max_zoom

    def compute_semantic_zoom(
        self,
        nodes: List[SemanticNode],
        focus_x: float,
        focus_y: float,
        zoom_factor: float = 1.0,
    ) -> MorphologicalLensTelemetry:
        """
        Calculates apparent node scales, dynamic LOD selection, and cognitive workload
        at the specified focus point and continuous zoom factor.
        """
        clamped_zoom = max(self.min_zoom, min(self.max_zoom, zoom_factor))
        effective_foveal_r = self.base_focal_radius_px * math.sqrt(clamped_zoom)
        effective_parafoveal_r = effective_foveal_r * self.parafoveal_expansion_ratio

        views: List[MorphologicalNodeView] = []
        foveal_count = 0
        parafoveal_count = 0
        peripheral_count = 0

        # Determine primary LOD from zoom factor
        # Zoom < 0.65: Macro; 0.65 - 1.45: Meso; 1.45 - 2.85: Micro; > 2.85: Atomic
        if clamped_zoom < 0.65:
            primary_lod = "MACRO_ARCHITECTURAL"
        elif clamped_zoom < 1.45:
            primary_lod = "MESO_SUBSYSTEM"
        elif clamped_zoom < 2.85:
            primary_lod = "MICRO_COMPONENT"
        else:
            primary_lod = "ATOMIC_PRIMITIVE"

        for node in nodes:
            dx = node.x - focus_x
            dy = node.y - focus_y
            dist = math.hypot(dx, dy)

            is_foveal = dist <= effective_foveal_r
            is_parafoveal = not is_foveal and dist <= effective_parafoveal_r

            if is_foveal:
                foveal_count += 1
            elif is_parafoveal:
                parafoveal_count += 1
            else:
                peripheral_count += 1

            # Apparent scale combines zoom factor, node importance, and spatial decay
            if is_foveal:
                dist_factor = 1.0 - (dist / effective_foveal_r) * 0.25
                apparent_scale = clamped_zoom * dist_factor * node.importance_weight
                opacity = 1.0
            elif is_parafoveal:
                span = effective_parafoveal_r - effective_foveal_r
                t = (dist - effective_foveal_r) / max(1.0, span)
                dist_factor = 0.75 - t * 0.45
                apparent_scale = max(0.2, clamped_zoom * dist_factor * node.importance_weight)
                opacity = max(0.35, 1.0 - t * 0.6)
            else:
                apparent_scale = max(0.15, clamped_zoom * 0.25 * node.importance_weight)
                opacity = max(0.15, 0.40 - min(0.25, (dist - effective_parafoveal_r) / 400.0))

            # Resolve apparent LOD based on distance and depth compatibility
            if is_foveal:
                apparent_lod = primary_lod
                visible_details = len(node.details) if clamped_zoom >= 1.0 else min(1, len(node.details))
            elif is_parafoveal:
                idx = self.LOD_ORDER.index(primary_lod)
                fallback_idx = max(0, idx - 1)
                apparent_lod = self.LOD_ORDER[fallback_idx]
                visible_details = min(1, len(node.details))
            else:
                apparent_lod = "MACRO_ARCHITECTURAL"
                visible_details = 0

            views.append(
                MorphologicalNodeView(
                    node=node,
                    distance_to_focus_px=dist,
                    apparent_scale=apparent_scale,
                    apparent_lod=apparent_lod,
                    opacity=opacity,
                    is_in_foveal_focus=is_foveal,
                    is_in_parafoveal_zone=is_parafoveal,
                    visible_detail_count=visible_details,
                )
            )

        # Cognitive density score calculation
        warnings: List[str] = []
        if foveal_count == 0:
            cognitive_density = 40.0
            perceptual_load = 0.1
            status = "SPARSE_GRANULARITY"
            warnings.append("No semantic anchors located within foveal focus aperture.")
        elif foveal_count <= self.max_cowan_foveal_capacity:
            load_ratio = foveal_count / float(self.max_cowan_foveal_capacity)
            cognitive_density = 85.0 + (1.0 - abs(load_ratio - 0.75)) * 15.0
            perceptual_load = load_ratio * 0.65
            status = "OPTIMAL_COGNITIVE_LOAD"
        else:
            excess = foveal_count - self.max_cowan_foveal_capacity
            penalty = excess * 18.0
            cognitive_density = max(10.0, 75.0 - penalty)
            perceptual_load = min(1.0, 0.75 + excess * 0.12)
            status = "PERCEPTUAL_OVERLOAD"
            warnings.append(
                f"Foveal items ({foveal_count}) exceed Cowan capacity ({self.max_cowan_foveal_capacity}); visual crowding imminent."
            )

        return MorphologicalLensTelemetry(
            zoom_factor=clamped_zoom,
            focus_center=(focus_x, focus_y),
            focal_radius_px=effective_foveal_r,
            active_primary_lod=primary_lod,
            foveal_node_count=foveal_count,
            parafoveal_node_count=parafoveal_count,
            peripheral_node_count=peripheral_count,
            cognitive_density_score=min(100.0, cognitive_density),
            perceptual_load_ratio=perceptual_load,
            status_level=status,
            views=views,
            warnings=warnings,
        )

    def generate_markdown_report(self, telemetry: MorphologicalLensTelemetry) -> str:
        """Builds a structured diagnostic Markdown report on semantic zoom kinematics."""
        status_icons = {
            "OPTIMAL_COGNITIVE_LOAD": "🟢",
            "SPARSE_GRANULARITY": "🟡",
            "PERCEPTUAL_OVERLOAD": "🔴",
        }
        icon = status_icons.get(telemetry.status_level, "⚪")

        lines = [
            "# Morphological Semantic Lens & Granularity Zoom Report",
            "",
            f"**Cognitive Load Status:** {icon} `{telemetry.status_level}`",
            "",
            "## Multi-Scale Zoom Telemetry",
            "",
            "| Telemetry Parameter | Value | Reference Standard | Cognitive Impact |",
            "| :--- | :--- | :--- | :--- |",
            f"| **Current Zoom Factor** | `{telemetry.zoom_factor:.2f}x` | 0.50x to 3.00x | Continuous multi-scale magnification |",
            f"| **Active Primary LOD** | `{telemetry.active_primary_lod}` | Hierarchical Tier | Resolves abstraction granularity |",
            f"| **Focal Aperture Radius** | `{telemetry.focal_radius_px:.1f} px` | 80 - 240 px | Dynamic foveal inspection corridor |",
            f"| **Foveal Item Count** | `{telemetry.foveal_node_count} nodes` | <= {self.max_cowan_foveal_capacity} (Cowan Limit) | Immediate working memory footprint |",
            f"| **Parafoveal Buffer Count** | `{telemetry.parafoveal_node_count} nodes` | 2 - 8 nodes | Pre-attentive transition zone |",
            f"| **Peripheral Context Count** | `{telemetry.peripheral_node_count} nodes` | Broad survey | Background spatial grounding |",
            f"| **Cognitive Density Score** | `{telemetry.cognitive_density_score:.1f} / 100` | >= 75.0 | Working memory crowding resilience |",
            f"| **Perceptual Load Ratio** | `{telemetry.perceptual_load_ratio:.2f}` | < 0.70 | Lavie selective attention balance |",
            "",
            "## Calibrated Semantic Node Views",
            "",
        ]

        if not telemetry.views:
            lines.append("_No semantic nodes evaluated within lens field._")
        else:
            lines.append("| Node Label | Granularity Tier | Dist to Focus | Apparent Scale | Opacity | Focus Zone |")
            lines.append("| :--- | :--- | :--- | :--- | :--- | :--- |")
            for v in telemetry.views:
                zone = "Foveal Focus" if v.is_in_foveal_focus else ("Parafoveal" if v.is_in_parafoveal_zone else "Periphery")
                lines.append(
                    f"| **{v.node.label}** | `{v.apparent_lod}` | `{v.distance_to_focus_px:.0f} px` | `{v.apparent_scale:.2f}x` | `{v.opacity * 100:.0f}%` | {zone} |"
                )
            lines.append("")

        if telemetry.warnings:
            lines.append("## Attentional Warnings & Recommendations")
            lines.append("")
            for w in telemetry.warnings:
                lines.append(f"- ⚠️ {w}")
            lines.append("")

        lines.extend([
            "## Cognitive Principles & Multi-Scale Navigation",
            "",
            "- **Cowan Capacity Protection (N <= 4):** Restricting foveal nodes to 4 or fewer prevents working memory thrashing, preserving conceptual coherence.",
            "- **Continuous Morphological Zooming:** Smooth interpolation between macro topological maps and atomic syntax eliminates the cognitive disorientation caused by abrupt context switching.",
            "- **Concentric Focus Falloff:** Parafoveal buffers provide preview cues that guide purposeful saccades without triggering peripheral distraction.",
        ])

        return chr(10).join(lines)

    def generate_svg(
        self,
        telemetry: MorphologicalLensTelemetry,
        width: int = 880,
        height: int = 580,
    ) -> str:
        """Renders an interactive dark titanium SVG focus ring with multi-resolution node views."""
        cx, cy = telemetry.focus_center
        rf = telemetry.focal_radius_px
        rp = rf * self.parafoveal_expansion_ratio

        parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
            f'width="{width}" height="{height}" style="background-color: #0d1117; font-family: -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif;">',
            '<defs>',
            '  <!-- Concentric Focus Ring Gradients -->',
            f'  <radialGradient id="fovealGrad" cx="{cx}" cy="{cy}" r="{rf}" gradientUnits="userSpaceOnUse">',
            '    <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.18" />',
            '    <stop offset="85%" stop-color="#1f6feb" stop-opacity="0.08" />',
            '    <stop offset="100%" stop-color="#1f6feb" stop-opacity="0.0" />',
            '  </radialGradient>',
            f'  <radialGradient id="parafovealGrad" cx="{cx}" cy="{cy}" r="{rp}" gradientUnits="userSpaceOnUse">',
            '    <stop offset="0%" stop-color="#8b949e" stop-opacity="0.0" />',
            '    <stop offset="70%" stop-color="#8b949e" stop-opacity="0.04" />',
            '    <stop offset="100%" stop-color="#8b949e" stop-opacity="0.08" />',
            '  </radialGradient>',
            '  <!-- Node Glow Filter -->',
            '  <filter id="nodeGlow" x="-20%" y="-20%" width="140%" height="140%">',
            '    <feGaussianBlur stdDeviation="3" result="blur" />',
            '    <feComposite in="SourceGraphic" in2="blur" operator="over" />',
            '  </filter>',
            '</defs>',
            '<!-- Canvas Base -->',
            f'<rect width="{width}" height="{height}" fill="#0d1117" />',
        ]

        # Subtle background grid
        parts.append('<!-- Cartesian Reference Grid -->')
        for gx in range(40, width, 50):
            parts.append(f'<line x1="{gx}" y1="0" x2="{gx}" y2="{height}" stroke="#161b22" stroke-width="1" />')
        for gy in range(40, height, 50):
            parts.append(f'<line x1="0" y1="{gy}" x2="{width}" y2="{gy}" stroke="#161b22" stroke-width="1" />')

        # Concentric Focus Rings
        parts.extend([
            '<!-- Parafoveal Boundary Ring -->',
            f'<circle cx="{cx}" cy="{cy}" r="{rp}" fill="url(#parafovealGrad)" stroke="#30363d" stroke-width="1.5" stroke-dasharray="4 4" />',
            '<!-- Foveal Inspection Aperture -->',
            f'<circle cx="{cx}" cy="{cy}" r="{rf}" fill="url(#fovealGrad)" stroke="#38bdf8" stroke-width="2" />',
            '<!-- Focus Crosshair -->',
            f'<line x1="{cx - 14}" y1="{cy}" x2="{cx + 14}" y2="{cy}" stroke="#38bdf8" stroke-width="1.5" opacity="0.8" />',
            f'<line x1="{cx}" y1="{cy - 14}" x2="{cx}" y2="{cy + 14}" stroke="#38bdf8" stroke-width="1.5" opacity="0.8" />',
        ])

        # Render Nodes and Connecting Arcs
        parts.append('<!-- Semantic Graph Nodes & Interconnects -->')
        for i in range(len(telemetry.views)):
            for j in range(i + 1, min(i + 3, len(telemetry.views))):
                v1 = telemetry.views[i]
                v2 = telemetry.views[j]
                stroke_op = min(v1.opacity, v2.opacity) * 0.4
                parts.append(
                    f'<line x1="{v1.node.x}" y1="{v1.node.y}" x2="{v2.node.x}" y2="{v2.node.y}" stroke="#30363d" stroke-width="1" stroke-opacity="{stroke_op}" />'
                )

        # Draw Node Glyphs
        lod_colors = {
            "MACRO_ARCHITECTURAL": "#bc8cff",
            "MESO_SUBSYSTEM": "#38bdf8",
            "MICRO_COMPONENT": "#3fb950",
            "ATOMIC_PRIMITIVE": "#d29922",
        }

        for v in telemetry.views:
            n = v.node
            col = lod_colors.get(v.apparent_lod, "#58a6ff")
            base_r = 14.0 * v.apparent_scale
            r_clamped = max(5.0, min(32.0, base_r))

            parts.append(f'<g transform="translate({n.x}, {n.y})" opacity="{v.opacity}">')

            if v.is_in_foveal_focus:
                parts.append(f'  <circle r="{r_clamped + 5}" fill="none" stroke="{col}" stroke-width="1.5" opacity="0.4" />')

            parts.append(f'  <circle r="{r_clamped}" fill="{col}" fill-opacity="0.25" stroke="{col}" stroke-width="1.8" />')
            parts.append(f'  <circle r="{max(2.0, r_clamped * 0.35)}" fill="{col}" />')

            font_sz = max(9, min(14, int(11 * math.sqrt(v.apparent_scale))))
            label_escaped = html.escape(n.label)
            parts.append(
                f'  <text x="0" y="{r_clamped + font_sz + 2}" fill="#f0f6fc" font-size="{font_sz}" font-weight="600" text-anchor="middle">{label_escaped}</text>'
            )

            if v.visible_detail_count > 0 and n.details:
                detail_text = html.escape(n.details[0])
                parts.append(
                    f'  <text x="0" y="{r_clamped + font_sz + 16}" fill="#8b949e" font-size="9" text-anchor="middle">{detail_text}</text>'
                )

            parts.append('</g>')

        # Top Header Bar
        parts.extend([
            '<!-- Header Information -->',
            '<text x="24" y="34" fill="#f0f6fc" font-size="16" font-weight="700">Morphological Semantic Lens</text>',
            '<text x="24" y="52" fill="#8b949e" font-size="11">Continuous Multi-Resolution Granularity Zoom and Cowan Capacity Preserver</text>',
        ])

        # Status Badge (Top Right)
        status_colors = {
            "OPTIMAL_COGNITIVE_LOAD": ("#238636", "#3fb950"),
            "SPARSE_GRANULARITY": ("#9e6a03", "#d29922"),
            "PERCEPTUAL_OVERLOAD": ("#da3633", "#f85149"),
        }
        bg_col, fg_col = status_colors.get(telemetry.status_level, ("#30363d", "#8b949e"))
        badge_x = width - 210
        parts.extend([
            f'<rect x="{badge_x}" y="20" width="186" height="34" rx="6" fill="{bg_col}" fill-opacity="0.25" stroke="{fg_col}" stroke-width="1.2" />',
            f'<circle cx="{badge_x + 16}" cy="37" r="5" fill="{fg_col}" />',
            f'<text x="{badge_x + 30}" y="41" fill="#f0f6fc" font-size="11" font-weight="700">{telemetry.status_level}</text>',
        ])

        # HUD Telemetry Card (Bottom Right)
        card_w = 310
        card_h = 142
        card_x = width - card_w - 24
        card_y = height - card_h - 24
        parts.extend([
            f'<g transform="translate({card_x}, {card_y})">',
            f'  <rect width="{card_w}" height="{card_h}" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1.5" />',
            '  <text x="16" y="24" fill="#f0f6fc" font-size="12" font-weight="700">Multi-Scale Lens Telemetry</text>',
            f'  <line x1="16" y1="32" x2="{card_w - 16}" y2="32" stroke="#30363d" stroke-width="1" />',
            f'  <text x="16" y="52" fill="#8b949e" font-size="11">Active Zoom Magnification:</text>',
            f'  <text x="{card_w - 16}" y="52" fill="#38bdf8" font-size="11" font-weight="600" text-anchor="end">{telemetry.zoom_factor:.2f}x</text>',
            f'  <text x="16" y="72" fill="#8b949e" font-size="11">Primary LOD Granularity:</text>',
            f'  <text x="{card_w - 16}" y="72" fill="#bc8cff" font-size="11" font-weight="600" text-anchor="end">{telemetry.active_primary_lod}</text>',
            f'  <text x="16" y="92" fill="#8b949e" font-size="11">Foveal Capacity (N &lt;= {self.max_cowan_foveal_capacity}):</text>',
            f'  <text x="{card_w - 16}" y="92" fill="#3fb950" font-size="11" font-weight="600" text-anchor="end">{telemetry.foveal_node_count} nodes</text>',
            f'  <text x="16" y="112" fill="#8b949e" font-size="11">Cognitive Density Score:</text>',
            f'  <text x="{card_w - 16}" y="112" fill="#f0f6fc" font-size="11" font-weight="600" text-anchor="end">{telemetry.cognitive_density_score:.1f} / 100</text>',
            f'  <text x="16" y="130" fill="#8b949e" font-size="11">Perceptual Load Ratio:</text>',
            f'  <text x="{card_w - 16}" y="130" fill="#d29922" font-size="11" font-weight="600" text-anchor="end">{telemetry.perceptual_load_ratio:.2f}</text>',
            '</g>',
        ])

        # Legend Panel (Bottom Left)
        leg_w = 320
        leg_h = 108
        leg_x = 24
        leg_y = height - leg_h - 24
        parts.extend([
            f'<g transform="translate({leg_x}, {leg_y})">',
            f'  <rect width="{leg_w}" height="{leg_h}" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1.2" opacity="0.9" />',
            '  <text x="16" y="20" fill="#f0f6fc" font-size="11" font-weight="700">Granularity Tiers &amp; Focus Rings</text>',
            '  <circle cx="22" cy="38" r="6" fill="#bc8cff" />',
            '  <text x="36" y="42" fill="#8b949e" font-size="10">Macro Architectural Topology</text>',
            '  <circle cx="170" cy="38" r="6" fill="#38bdf8" />',
            '  <text x="184" y="42" fill="#8b949e" font-size="10">Meso Subsystem</text>',
            '  <circle cx="22" cy="62" r="6" fill="#3fb950" />',
            '  <text x="36" y="66" fill="#8b949e" font-size="10">Micro Component</text>',
            '  <circle cx="170" cy="62" r="6" fill="#d29922" />',
            '  <text x="184" y="66" fill="#8b949e" font-size="10">Atomic Primitive</text>',
            '  <circle cx="22" cy="88" r="6" fill="none" stroke="#38bdf8" stroke-width="1.5" />',
            '  <text x="36" y="92" fill="#8b949e" font-size="10">Foveal Aperture (Solid Blue Ring)</text>',
            '  <circle cx="170" cy="88" r="6" fill="none" stroke="#30363d" stroke-width="1.5" stroke-dasharray="2 2" />',
            '  <text x="184" y="92" fill="#8b949e" font-size="10">Parafoveal Buffer (Dashed Gray)</text>',
            '</g>',
        ])

        parts.append('</svg>')
        return "\n".join(parts)

    @classmethod
    def create_demo_telemetry(cls) -> MorphologicalLensTelemetry:
        """Constructs a realistic software architecture hierarchy for demonstration."""
        nodes = [
            SemanticNode("node-1", "Spatial Ledger Core", "MACRO_ARCHITECTURAL", 0.1, 380.0, 240.0, 1.0, ["Distributed consensus", "Merkle tree storage"]),
            SemanticNode("node-2", "Consensus Engine", "MESO_SUBSYSTEM", 0.35, 420.0, 280.0, 0.9, ["Raft state machine", "Leader election"]),
            SemanticNode("node-3", "Peer Discovery Mesh", "MESO_SUBSYSTEM", 0.4, 280.0, 190.0, 0.85, ["Kademlia DHT", "Gossip protocol"]),
            SemanticNode("node-4", "Cryptographic Verifier", "MICRO_COMPONENT", 0.65, 450.0, 230.0, 0.8, ["Ed25519 signatures", "Zero-knowledge proofs"]),
            SemanticNode("node-5", "Raft State Machine", "MICRO_COMPONENT", 0.7, 490.0, 310.0, 0.75, ["Log replication", "AppendEntries RPC"]),
            SemanticNode("node-6", "Memory Buffer Ring", "ATOMIC_PRIMITIVE", 0.9, 560.0, 340.0, 0.7, ["Atomic compare-exchange", "Zero-copy pointer"]),
            SemanticNode("node-7", "Bloom Filter Index", "ATOMIC_PRIMITIVE", 0.95, 220.0, 140.0, 0.65, ["MurmurHash3", "Bit vector arrays"]),
            SemanticNode("node-8", "Telemetry Gateway", "MESO_SUBSYSTEM", 0.45, 260.0, 360.0, 0.8, ["Prometheus metrics", "Distributed tracing"]),
            SemanticNode("node-9", "TLS Transport Layer", "MICRO_COMPONENT", 0.6, 210.0, 420.0, 0.75, ["Noise protocol", "Handshake cipher"]),
        ]

        lens = cls(base_focal_radius_px=140.0, max_cowan_foveal_capacity=4)
        return lens.compute_semantic_zoom(nodes, focus_x=430.0, focus_y=260.0, zoom_factor=1.4)
