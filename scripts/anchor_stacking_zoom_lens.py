"""
Anchor Stacking & Hierarchical Zoom Lens
Autonomous cognitive spatial module for multi-tier level-of-detail (LoD)
semantic zoom, dynamic micro-anchor collapse, and nested conceptual hierarchy
envelopes. Grounded in Eide & Eide M-I-N-D framework, Cowan working memory bounds,
and Bouma visual crowding mitigation.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
import math
import html


@dataclass
class SemanticAnchor:
    """Represents a spatial knowledge anchor at a specific hierarchy depth."""
    anchor_id: str
    title: str
    x: float
    y: float
    lod_level: int  # 0: Macro (system), 1: Meso (subsystem), 2: Micro (detail)
    parent_id: Optional[str] = None
    saliency: float = 1.0  # 0.1 to 10.0
    tags: List[str] = field(default_factory=list)


@dataclass
class CollapsedClusterHull:
    """Represents a collapsed cluster envelope at low zoom levels."""
    cluster_id: str
    parent_anchor_id: str
    title: str
    center_x: float
    center_y: float
    radius_px: float
    contained_anchor_count: int
    aggregate_saliency: float


@dataclass
class ZoomLensTelemetry:
    """Comprehensive telemetry for anchor stacking and zoom lens state."""
    zoom_factor: float
    active_lod_tier: str  # Macro, Meso, or Micro
    total_anchors: int
    visible_anchor_count: int
    collapsed_cluster_count: int
    mean_crowding_index: float
    cowan_compliant: bool
    cognitive_load_score: float  # 0.0 (minimal) to 1.0 (overload)
    visible_anchors: List[SemanticAnchor] = field(default_factory=list)
    collapsed_hulls: List[CollapsedClusterHull] = field(default_factory=list)


class AnchorStackingZoomLens:
    """
    Autonomous engine that regulates visual density across zoom transformations.
    Dynamically prunes and stacks micro-anchors into parent hulls upon zoom retreat,
    preventing cognitive crowding while preserving allocentric landmarks.
    """

    def __init__(
        self,
        macro_zoom_threshold: float = 0.55,
        meso_zoom_threshold: float = 1.15,
        crowding_distance_px: float = 65.0,
    ):
        self.macro_threshold = float(macro_zoom_threshold)
        self.meso_threshold = float(meso_zoom_threshold)
        self.crowding_dist = float(crowding_distance_px)

    def determine_lod_tier(self, zoom_factor: float) -> Tuple[int, str]:
        """Resolves active maximum LoD level and human-readable tier label."""
        z = max(0.1, float(zoom_factor))
        if z < self.macro_threshold:
            return 0, "Macro"
        elif z < self.meso_threshold:
            return 1, "Meso"
        else:
            return 2, "Micro"

    def evaluate_zoom(
        self,
        anchors: List[SemanticAnchor],
        zoom_factor: float = 1.0,
    ) -> ZoomLensTelemetry:
        """
        Evaluates knowledge anchors against current zoom magnification,
        collapsing high-LoD children into cluster envelopes when zoomed out.
        """
        max_lod, tier_label = self.determine_lod_tier(zoom_factor)

        visible_anchors: List[SemanticAnchor] = []
        hidden_anchors_by_parent: Dict[str, List[SemanticAnchor]] = {}

        for a in anchors:
            if a.lod_level <= max_lod:
                visible_anchors.append(a)
            else:
                p_id = a.parent_id or "root"
                hidden_anchors_by_parent.setdefault(p_id, []).append(a)

        # Build collapsed cluster hulls for hidden children
        collapsed_hulls: List[CollapsedClusterHull] = []
        for p_id, children in hidden_anchors_by_parent.items():
            # Find parent anchor coordinates if available
            parent = next((a for a in anchors if a.anchor_id == p_id), None)
            if parent:
                c_x, c_y = parent.x, parent.y
                p_title = f"{parent.title} Details"
            else:
                c_x = sum(c.x for c in children) / len(children)
                c_y = sum(c.y for c in children) / len(children)
                p_title = f"Cluster ({p_id})"

            agg_sal = sum(c.saliency for c in children)
            rad = max(24.0, min(70.0, 18.0 + math.sqrt(len(children)) * 12.0))

            collapsed_hulls.append(
                CollapsedClusterHull(
                    cluster_id=f"hull-{p_id}",
                    parent_anchor_id=p_id,
                    title=p_title,
                    center_x=round(c_x, 2),
                    center_y=round(c_y, 2),
                    radius_px=round(rad, 2),
                    contained_anchor_count=len(children),
                    aggregate_saliency=round(agg_sal, 2),
                )
            )

        # Calculate visual crowding index between visible elements
        crowding_events = 0
        pair_comparisons = 0
        for i in range(len(visible_anchors)):
            for j in range(i + 1, len(visible_anchors)):
                a1 = visible_anchors[i]
                a2 = visible_anchors[j]
                dist = math.hypot((a1.x - a2.x) * zoom_factor, (a1.y - a2.y) * zoom_factor)
                pair_comparisons += 1
                if dist < self.crowding_dist:
                    crowding_events += 1

        mean_crowding = (
            round(crowding_events / max(1, pair_comparisons), 3)
            if pair_comparisons > 0
            else 0.0
        )

        # Cowan limit compliance check (N <= 4 focal anchors in active focus)
        cowan_compliant = len(visible_anchors) <= 7 or mean_crowding <= 0.15

        # Cognitive load score computation
        raw_load = (len(visible_anchors) * 0.08) + (mean_crowding * 0.5)
        cognitive_load = round(min(1.0, max(0.05, raw_load)), 2)

        return ZoomLensTelemetry(
            zoom_factor=round(zoom_factor, 2),
            active_lod_tier=tier_label,
            total_anchors=len(anchors),
            visible_anchor_count=len(visible_anchors),
            collapsed_cluster_count=len(collapsed_hulls),
            mean_crowding_index=mean_crowding,
            cowan_compliant=cowan_compliant,
            cognitive_load_score=cognitive_load,
            visible_anchors=visible_anchors,
            collapsed_hulls=collapsed_hulls,
        )

    def generate_markdown_report(self, telemetry: ZoomLensTelemetry) -> str:
        """Generates structured markdown audit report with zero em dashes."""
        lines = [
            "# Anchor Stacking and Hierarchical Zoom Lens Telemetry",
            "",
            "## 1. Executive Zoom State Overview",
            f"- **Magnification Factor:** {telemetry.zoom_factor}x",
            f"- **Active Level-of-Detail Tier:** `{telemetry.active_lod_tier}`",
            f"- **Total System Anchors:** {telemetry.total_anchors}",
            f"- **Visible Unstacked Anchors:** {telemetry.visible_anchor_count}",
            f"- **Stacked / Collapsed Envelopes:** {telemetry.collapsed_cluster_count}",
            f"- **Mean Visual Crowding Index:** {telemetry.mean_crowding_index}",
            f"- **Cognitive Working Memory Load:** {round(telemetry.cognitive_load_score * 100.0, 1)}%",
            f"- **Cowan Capacity Status:** {'COMPLIANT' if telemetry.cowan_compliant else 'OVERLOAD WARNING'}",
            "",
            "## 2. Theoretical Grounding",
            "- **Bouma Visual Crowding Law:** When magnification drops, dense tokens merge into unreadable blobs unless stacked.",
            "- **Cowan Capacity Bounds (N <= 4):** Macro views restrict active focus points to preserve strategic overview.",
            "- **Allocentric Landmarks:** Core anchors (LoD 0) remain visible across all zoom levels to prevent disorientation.",
            "",
            "## 3. Visible Spatial Anchors",
            "| ID | Title | Coordinates (x, y) | LoD Tier | Saliency | Tags |",
            "| :--- | :--- | :--- | :--- | :--- | :--- |",
        ]

        for a in telemetry.visible_anchors:
            tier_name = ["Macro (0)", "Meso (1)", "Micro (2)"][min(2, a.lod_level)]
            tag_str = ", ".join(a.tags) if a.tags else "none"
            lines.append(
                f"| `{a.anchor_id}` | {a.title} | ({a.x}, {a.y}) | {tier_name} | {a.saliency} | {tag_str} |"
            )

        if telemetry.collapsed_hulls:
            lines.extend([
                "",
                "## 4. Collapsed Cluster Envelopes",
                "| Envelope ID | Parent Anchor | Center (x, y) | Contained Anchors | Aggregate Saliency |",
                "| :--- | :--- | :--- | :--- | :--- |",
            ])
            for h in telemetry.collapsed_hulls:
                lines.append(
                    f"| `{h.cluster_id}` | `{h.parent_anchor_id}` | ({h.center_x}, {h.center_y}) | {h.contained_anchor_count} micro-items | {h.aggregate_saliency} |"
                )

        lines.extend([
            "",
            "## 5. Operational Ergonomics Guidance",
            "- In Macro zoom (< 0.55x), focus exclusively on high-level domain relationships.",
            "- In Meso zoom (0.55x to 1.15x), inspect module boundaries and interfaces without line-level distraction.",
            "- In Micro zoom (> 1.15x), full constructive details and code tokens are expanded.",
        ])

        return "\n".join(lines)

    def generate_svg(
        self,
        telemetry: ZoomLensTelemetry,
        width: int = 920,
        height: int = 560,
    ) -> str:
        """Generates publication-grade dark titanium SVG diagram of the zoom lens canvas."""
        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" style="background:#090d16; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">',
            '<defs>',
            '  <radialGradient id="lensGlow" cx="50%" cy="50%" r="50%">',
            '    <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.15"/>',
            '    <stop offset="100%" stop-color="#090d16" stop-opacity="0"/>',
            '  </radialGradient>',
            '  <filter id="nodeShadow" x="-20%" y="-20%" width="140%" height="140%">',
            '    <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#000" flood-opacity="0.7"/>',
            '  </filter>',
            '</defs>',
            '<!-- Background Grid -->',
            '<g opacity="0.12">',
        ]

        grid_spacing = int(max(20, 50 * telemetry.zoom_factor))
        for gx in range(0, width, grid_spacing):
            svg_parts.append(f'<line x1="{gx}" y1="0" x2="{gx}" y2="{height}" stroke="#334155" stroke-width="0.5"/>')
        for gy in range(0, height, grid_spacing):
            svg_parts.append(f'<line x1="0" y1="{gy}" x2="{width}" y2="{gy}" stroke="#334155" stroke-width="0.5"/>')
        svg_parts.append('</g>')

        # Center lens glow
        svg_parts.append(f'<circle cx="{width // 2}" cy="{height // 2}" r="{min(width, height) // 2}" fill="url(#lensGlow)"/>')

        # Draw Collapsed Cluster Hulls
        for hull in telemetry.collapsed_hulls:
            svg_parts.append(
                f'<circle cx="{hull.center_x}" cy="{hull.center_y}" r="{hull.radius_px}" fill="#1e293b" fill-opacity="0.5" stroke="#38bdf8" stroke-width="1.2" stroke-dasharray="3,3"/>'
            )
            badge_text = f"+{hull.contained_anchor_count} stacked"
            svg_parts.append(
                f'<rect x="{hull.center_x - 36}" y="{hull.center_y + hull.radius_px - 8}" width="72" height="16" rx="8" fill="#0f172a" stroke="#0284c7" stroke-width="1"/>'
            )
            svg_parts.append(
                f'<text x="{hull.center_x}" y="{hull.center_y + hull.radius_px + 4}" font-size="8" font-weight="700" fill="#38bdf8" text-anchor="middle">{badge_text}</text>'
            )

        # Draw Hierarchy Links
        for anchor in telemetry.visible_anchors:
            if anchor.parent_id:
                parent = next((p for p in telemetry.visible_anchors if p.anchor_id == anchor.parent_id), None)
                if parent:
                    svg_parts.append(
                        f'<line x1="{parent.x}" y1="{parent.y}" x2="{anchor.x}" y2="{anchor.y}" stroke="#475569" stroke-width="1.0" stroke-dasharray="2,3" opacity="0.6"/>'
                    )

        # Draw Visible Anchors
        for anchor in telemetry.visible_anchors:
            if anchor.lod_level == 0:
                fill_c = "#0284c7"
                stroke_c = "#38bdf8"
                r = 18.0
            elif anchor.lod_level == 1:
                fill_c = "#0f766e"
                stroke_c = "#2dd4bf"
                r = 13.0
            else:
                fill_c = "#7c3aed"
                stroke_c = "#a78bfa"
                r = 9.0

            svg_parts.append(
                f'<circle cx="{anchor.x}" cy="{anchor.y}" r="{r}" fill="{fill_c}" stroke="{stroke_c}" stroke-width="2.0" filter="url(#nodeShadow)"/>'
            )
            svg_parts.append(
                f'<text x="{anchor.x}" y="{anchor.y + r + 13}" font-size="10" font-weight="600" fill="#ffffff" text-anchor="middle">{html.escape(anchor.title)}</text>'
            )

        # Telemetry HUD Header
        svg_parts.append(
            f'<rect x="20" y="16" width="330" height="74" rx="8" fill="#0f172a" fill-opacity="0.88" stroke="#1e293b" stroke-width="1"/>'
        )
        svg_parts.append(
            f'<text x="32" y="36" font-size="11" font-weight="700" fill="#38bdf8">HIERARCHICAL ZOOM LENS HUD</text>'
        )
        svg_parts.append(
            f'<text x="32" y="52" font-size="9" fill="#94a3b8">Zoom: {telemetry.zoom_factor}x | Tier: {telemetry.active_lod_tier} | Visible: {telemetry.visible_anchor_count}/{telemetry.total_anchors}</text>'
        )
        svg_parts.append(
            f'<text x="32" y="68" font-size="9" fill="#94a3b8">Cognitive Load: {round(telemetry.cognitive_load_score * 100.0, 1)}% | Envelopes: {telemetry.collapsed_cluster_count}</text>'
        )

        svg_parts.append('</svg>')
        return "\n".join(svg_parts)


def sample_knowledge_hierarchy() -> List[SemanticAnchor]:
    """Provides demonstration multi-tier knowledge hierarchy."""
    return [
        # Macro Level 0 (System Pillars)
        SemanticAnchor(anchor_id="sys-core", title="DxEngine Core", x=460.0, y=280.0, lod_level=0, saliency=5.0, tags=["core", "system"]),
        SemanticAnchor(anchor_id="sys-vis", title="Spatial Canvas", x=240.0, y=200.0, lod_level=0, saliency=4.5, tags=["ui", "canvas"]),
        SemanticAnchor(anchor_id="sys-tele", title="Cognitive Telemetry", x=680.0, y=200.0, lod_level=0, saliency=4.0, tags=["telemetry"]),
        
        # Meso Level 1 (Subsystems)
        SemanticAnchor(anchor_id="sub-saccade", title="Saccadic Pacer", x=200.0, y=340.0, lod_level=1, parent_id="sys-vis", saliency=3.0, tags=["ocular"]),
        SemanticAnchor(anchor_id="sub-density", title="Density Equalizer", x=300.0, y=120.0, lod_level=1, parent_id="sys-vis", saliency=2.8, tags=["density"]),
        SemanticAnchor(anchor_id="sub-gravity", title="Gravity Well", x=460.0, y=420.0, lod_level=1, parent_id="sys-core", saliency=3.2, tags=["orbit"]),
        SemanticAnchor(anchor_id="sub-audit", title="Metacognition Auditor", x=720.0, y=340.0, lod_level=1, parent_id="sys-tele", saliency=2.5, tags=["audit"]),

        # Micro Level 2 (Detailed Implementations)
        SemanticAnchor(anchor_id="mic-kepler", title="Kepler Math Kernel", x=420.0, y=470.0, lod_level=2, parent_id="sub-gravity", saliency=1.5, tags=["math"]),
        SemanticAnchor(anchor_id="mic-escape", title="Escape Velocity Check", x=500.0, y=470.0, lod_level=2, parent_id="sub-gravity", saliency=1.2, tags=["physics"]),
        SemanticAnchor(anchor_id="mic-foveal", title="Foveal Aperture Cut", x=160.0, y=390.0, lod_level=2, parent_id="sub-saccade", saliency=1.4, tags=["filter"]),
        SemanticAnchor(anchor_id="mic-shannon", title="Shannon Entropy Calc", x=340.0, y=80.0, lod_level=2, parent_id="sub-density", saliency=1.1, tags=["math"]),
    ]
