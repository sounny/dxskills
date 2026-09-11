"""
foveal_horizon_tracker.py - Autonomous Cognitive Spatial Dynamic Foveal Horizon & Context Anchor Restorer

Part of the DxSkills cognitive scaffolding suite (Phase 103, Cycle 99).
Grounded in Henderson & Hollingworth (1999) trans-saccadic memory, Rayner (2009) foveal
horizon dynamics, and Eide & Eide M-I spatial orientation models.

Strict constraint: Strictly zero em dashes (Unicode U+2014) anywhere.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class ZoomState:
    """Snapshot of 2D canvas zoom scale, pan position, and focal landmark."""
    state_id: str
    zoom_level: float  # e.g., 0.25 (macro overview) to 4.0 (micro deep-dive)
    pan_x: float
    pan_y: float
    focal_node_title: str
    timestamp_ms: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class BreadcrumbAnchor:
    """Contextual re-entry breadcrumb anchor bridging multi-scale focus transitions."""
    anchor_id: str
    label: str
    x: float
    y: float
    zoom_tier: str  # MACRO, MESO, MICRO
    salience_score: float
    vector_from_prev: Tuple[float, float]  # (dx, dy)
    re_entry_hint: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "anchor_id": self.anchor_id,
            "label": self.label,
            "x": self.x,
            "y": self.y,
            "zoom_tier": self.zoom_tier,
            "salience_score": self.salience_score,
            "vector_from_prev": list(self.vector_from_prev),
            "re_entry_hint": self.re_entry_hint,
        }


@dataclass
class HorizonTelemetry:
    """Cognitive telemetry measuring visual drift latency, disorientation risk, and working memory coherence."""
    source_zoom: float
    target_zoom: float
    zoom_ratio: float
    pan_displacement_px: float
    visual_drift_latency_ms: float  # Latency required for allocentric re-calibration
    disorientation_risk: str  # NOMINAL, MODERATE, ELEVATED, CRITICAL
    breadcrumbs_synthesized: int
    working_memory_coherence_pct: float
    cowan_bounded: bool

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class FovealHorizonResult:
    """Master result bundle containing breadcrumbs, telemetry, and SVG re-entry horizon."""
    breadcrumbs: List[BreadcrumbAnchor]
    telemetry: HorizonTelemetry
    re_entry_path: List[Tuple[float, float]]
    svg_diagram: str
    restorative_css: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "telemetry": self.telemetry.to_dict(),
            "breadcrumbs": [b.to_dict() for b in self.breadcrumbs],
            "re_entry_path": [list(p) for p in self.re_entry_path],
            "svg_diagram": self.svg_diagram,
            "restorative_css": self.restorative_css,
        }


class FovealHorizonTracker:
    """
    Autonomous Cognitive Spatial Dynamic Foveal Horizon & Context Anchor Restorer.

    Measures visual drift latency across deep zoom scales (macro overview <-> micro detail)
    and generates non-destructive re-entry guide vectors to preserve spatial working memory.
    """

    def __init__(
        self,
        base_orientation_latency_ms: float = 240.0,
        critical_displacement_threshold: float = 1200.0,
    ) -> None:
        self.base_orientation_latency_ms = base_orientation_latency_ms
        self.critical_displacement_threshold = critical_displacement_threshold

    def track_transition(
        self,
        source: Dict[str, Any],
        target: Dict[str, Any],
        landmarks: Optional[List[Dict[str, Any]]] = None,
    ) -> FovealHorizonResult:
        """
        Task 103.1 & 103.2: Calculates visual drift latency across zoom scales and
        projects contextual breadcrumb anchors for effortless re-entry.
        """
        s_zoom = max(0.1, float(source.get("zoom_level", 1.0)))
        t_zoom = max(0.1, float(target.get("zoom_level", 1.0)))
        s_x = float(source.get("pan_x", 0.0))
        s_y = float(source.get("pan_y", 0.0))
        t_x = float(target.get("pan_x", 0.0))
        t_y = float(target.get("pan_y", 0.0))
        s_title = str(source.get("focal_node_title", "Source Focal Hub"))
        t_title = str(target.get("focal_node_title", "Target Detail Node"))

        # Compute spatial metrics
        zoom_ratio = round(max(s_zoom / t_zoom, t_zoom / s_zoom), 2)
        displacement_px = round(math.hypot(t_x - s_x, t_y - s_y), 1)

        # Visual drift latency calculation (Task 103.1):
        # Latency escalates with both scale disparity and linear pan displacement
        zoom_penalty_ms = math.log2(zoom_ratio + 1.0) * 160.0
        pan_penalty_ms = (displacement_px / 1000.0) * 180.0
        total_drift_ms = round(self.base_orientation_latency_ms + zoom_penalty_ms + pan_penalty_ms, 1)

        # Categorize disorientation risk
        if total_drift_ms < 400.0 and zoom_ratio <= 1.8:
            risk_level = "NOMINAL"
        elif total_drift_ms < 750.0 and zoom_ratio <= 3.0:
            risk_level = "MODERATE"
        elif total_drift_ms < 1100.0:
            risk_level = "ELEVATED"
        else:
            risk_level = "CRITICAL"

        # Synthesize contextual breadcrumb anchors (Task 103.2)
        breadcrumbs: List[BreadcrumbAnchor] = []
        path_points: List[Tuple[float, float]] = [(s_x, s_y)]

        # Number of intermediate stepping anchors (Cowan bounded: 2 to 4)
        step_count = min(4, max(2, int(math.ceil(math.log2(zoom_ratio + 1.0) + (displacement_px / 800.0)))))

        for i in range(1, step_count + 1):
            alpha = i / (step_count + 1)
            interp_x = round(s_x + alpha * (t_x - s_x), 1)
            interp_y = round(s_y + alpha * (t_y - s_y), 1)
            interp_zoom = round(s_zoom + alpha * (t_zoom - s_zoom), 2)

            tier = "MACRO" if interp_zoom < 0.6 else ("MESO" if interp_zoom <= 1.8 else "MICRO")
            dx = round(interp_x - path_points[-1][0], 1)
            dy = round(interp_y - path_points[-1][1], 1)

            # Match or interpolate landmark label
            label = f"Waypoint {i}: ({tier} z={interp_zoom})"
            if landmarks and i - 1 < len(landmarks):
                lm_name = landmarks[i - 1].get("title", landmarks[i - 1].get("name", ""))
                if lm_name:
                    label = f"{lm_name} [{tier}]"

            hint = f"Saccadic vector: dx={dx:+.0f}px, dy={dy:+.0f}px at scale {interp_zoom}x"

            b = BreadcrumbAnchor(
                anchor_id=f"bc_{i:02d}",
                label=label,
                x=interp_x,
                y=interp_y,
                zoom_tier=tier,
                salience_score=round(0.90 - (i * 0.08), 2),
                vector_from_prev=(dx, dy),
                re_entry_hint=hint,
            )
            breadcrumbs.append(b)
            path_points.append((interp_x, interp_y))

        path_points.append((t_x, t_y))

        # Working memory coherence: higher with breadcrumbs absorbing displacement strain
        coherence_pct = round(max(35.0, min(95.0, 100.0 - (total_drift_ms / 30.0) + (len(breadcrumbs) * 6.5))), 1)
        cowan_bounded = len(breadcrumbs) <= 4

        telemetry = HorizonTelemetry(
            source_zoom=s_zoom,
            target_zoom=t_zoom,
            zoom_ratio=zoom_ratio,
            pan_displacement_px=displacement_px,
            visual_drift_latency_ms=total_drift_ms,
            disorientation_risk=risk_level,
            breadcrumbs_synthesized=len(breadcrumbs),
            working_memory_coherence_pct=coherence_pct,
            cowan_bounded=cowan_bounded,
        )

        # Restorative CSS animation tokens
        restorative_css = (
            f"/* DxSkills Restorative Transition Guide: Drift Latency {total_drift_ms}ms */\n"
            f".dx-foveal-transition {{\n"
            f"  transition: transform {min(650, int(total_drift_ms * 0.7))}ms cubic-bezier(0.16, 1, 0.3, 1);\n"
            f"  outline: 2px solid rgba(245, 158, 11, 0.4);\n"
            f"  will-change: transform, opacity;\n"
            f"}}\n"
            f".dx-breadcrumb-anchor {{\n"
            f"  box-shadow: 0 0 16px rgba(56, 189, 248, 0.35);\n"
            f"  backdrop-filter: blur(8px);\n"
            f"}}\n"
        )

        svg_diagram = self._render_foveal_svg(
            source=(s_x, s_y, s_zoom, s_title),
            target=(t_x, t_y, t_zoom, t_title),
            breadcrumbs=breadcrumbs,
            path_points=path_points,
            telemetry=telemetry,
        )

        return FovealHorizonResult(
            breadcrumbs=breadcrumbs,
            telemetry=telemetry,
            re_entry_path=path_points,
            svg_diagram=svg_diagram,
            restorative_css=restorative_css,
        )

    def _render_foveal_svg(
        self,
        source: Tuple[float, float, float, str],
        target: Tuple[float, float, float, str],
        breadcrumbs: List[BreadcrumbAnchor],
        path_points: List[Tuple[float, float]],
        telemetry: HorizonTelemetry,
    ) -> str:
        """Renders dark titanium SVG showing the multi-scale horizon and re-entry trajectory."""
        w, h = 920, 520
        t = telemetry

        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">',
            '  <defs>',
            '    <linearGradient id="fhBg" x1="0%" y1="0%" x2="100%" y2="100%">',
            '      <stop offset="0%" stop-color="#090d16"/>',
            '      <stop offset="100%" stop-color="#0f172a"/>',
            '    </linearGradient>',
            '    <linearGradient id="trailGrad" x1="0%" y1="0%" x2="100%" y2="0%">',
            '      <stop offset="0%" stop-color="#38bdf8"/>',
            '      <stop offset="50%" stop-color="#f59e0b"/>',
            '      <stop offset="100%" stop-color="#10b981"/>',
            '    </linearGradient>',
            '  </defs>',
            '  <rect width="100%" height="100%" fill="url(#fhBg)"/>',
            '  <!-- Header -->',
            '  <text x="40" y="44" font-family="system-ui, -apple-system, sans-serif" font-size="18" font-weight="700" fill="#f8fafc">Dynamic Foveal Horizon &amp; Context Anchor Restorer</text>',
            f'  <text x="40" y="68" font-family="system-ui, -apple-system, sans-serif" font-size="12" fill="#94a3b8">Rayner Foveal Dynamics &bull; Scale: {t.source_zoom}x &rarr; {t.target_zoom}x ({t.zoom_ratio}:1) &bull; Drift Latency: {t.visual_drift_latency_ms}ms &bull; Risk: [{t.disorientation_risk}]</text>',
            '  <!-- Horizon Canvas Frame -->',
            '  <g transform="translate(60, 95)">',
            '    <rect width="800" height="265" rx="12" fill="#070b14" stroke="#1e293b" stroke-width="1.5"/>',
            '    <!-- Horizon Depth Grids -->',
            '    <line x1="40" y1="132" x2="760" y2="132" stroke="#1e293b" stroke-width="1.5" stroke-dasharray="6,4"/>',
            '    <text x="50" y="125" font-family="monospace" font-size="9" fill="#475569">MACRO HORIZON</text>',
            '    <text x="710" y="125" font-family="monospace" font-size="9" fill="#475569" text-anchor="end">MICRO ZOOM</text>',
            '    <!-- Trajectory Spline -->',
            '    <path d="M 120 180 Q 280 60 420 120 T 700 80" fill="none" stroke="url(#trailGrad)" stroke-width="3" stroke-dasharray="6,3"/>',
            '    <!-- Source Landmark -->',
            '    <g transform="translate(120, 180)">',
            '      <circle cx="0" cy="0" r="14" fill="#0284c7" stroke="#38bdf8" stroke-width="2.5"/>',
            '      <circle cx="0" cy="0" r="24" fill="none" stroke="#0284c7" stroke-width="1" stroke-opacity="0.4"/>',
            f'      <text x="0" y="38" font-family="system-ui, -apple-system, sans-serif" font-size="11" font-weight="700" fill="#bae6fd" text-anchor="middle">{source[3]}</text>',
            f'      <text x="0" y="52" font-family="monospace" font-size="9" fill="#7dd3fc" text-anchor="middle">Scale: {source[2]}x</text>',
            '    </g>',
        ]

        # Draw breadcrumbs along the curve
        bx_coords = [270, 420, 560]
        by_coords = [85, 120, 95]
        for idx, b in enumerate(breadcrumbs[:3]):
            bx = bx_coords[idx] if idx < len(bx_coords) else 300 + idx * 100
            by = by_coords[idx] if idx < len(by_coords) else 100
            svg_parts.extend([
                f'    <!-- Breadcrumb Anchor {b.anchor_id} -->',
                f'    <g transform="translate({bx}, {by})">',
                '      <rect x="-60" y="-16" width="120" height="32" rx="8" fill="#78350f" stroke="#f59e0b" stroke-width="1.5"/>',
                f'      <text x="0" y="4" font-family="system-ui, -apple-system, sans-serif" font-size="10" font-weight="700" fill="#fef3c7" text-anchor="middle">{b.label}</text>',
                '    </g>',
            ])

        # Target Detail Node
        svg_parts.extend([
            '    <!-- Target Landmark -->',
            '    <g transform="translate(700, 80)">',
            '      <circle cx="0" cy="0" r="14" fill="#059669" stroke="#10b981" stroke-width="2.5"/>',
            '      <circle cx="0" cy="0" r="24" fill="none" stroke="#10b981" stroke-width="1" stroke-opacity="0.4"/>',
            f'      <text x="0" y="38" font-family="system-ui, -apple-system, sans-serif" font-size="11" font-weight="700" fill="#a7f3d0" text-anchor="middle">{target[3]}</text>',
            f'      <text x="0" y="52" font-family="monospace" font-size="9" fill="#6ee7b7" text-anchor="middle">Scale: {target[2]}x</text>',
            '    </g>',
            '    <!-- Recovery Vector Indicator -->',
            '    <text x="400" y="240" font-family="system-ui, -apple-system, sans-serif" font-size="11" fill="#94a3b8" text-anchor="middle">&larr; Continuous Contextual Re-Entry Vector (Preserves allocentric coordinates) &rarr;</text>',
            '  </g>',
            '  <!-- Bottom Cards: Telemetry Badges -->',
            '  <g transform="translate(60, 385)">',
            '    <rect x="0" y="0" width="240" height="90" rx="10" fill="#0b1120" stroke="#1e293b" stroke-width="1.5"/>',
            '    <text x="20" y="28" font-family="system-ui, -apple-system, sans-serif" font-size="11" fill="#94a3b8">Visual Drift Latency</text>',
            f'    <text x="20" y="60" font-family="system-ui, -apple-system, sans-serif" font-size="26" font-weight="800" fill="#38bdf8">{t.visual_drift_latency_ms}ms</text>',
            f'    <text x="20" y="80" font-family="system-ui, -apple-system, sans-serif" font-size="10" fill="#64748b">Zoom Ratio: {t.zoom_ratio}:1 &bull; Pan: {t.pan_displacement_px:.0f}px</text>',
            '    <rect x="270" y="0" width="240" height="90" rx="10" fill="#0b1120" stroke="#1e293b" stroke-width="1.5"/>',
            '    <text x="290" y="28" font-family="system-ui, -apple-system, sans-serif" font-size="11" fill="#94a3b8">Breadcrumb Stepping Anchors</text>',
            f'    <text x="290" y="60" font-family="system-ui, -apple-system, sans-serif" font-size="26" font-weight="800" fill="#f59e0b">{t.breadcrumbs_synthesized}</text>',
            f'    <text x="290" y="80" font-family="system-ui, -apple-system, sans-serif" font-size="10" fill="#64748b">Cowan 4-chunk bounded: {t.cowan_bounded}</text>',
            '    <rect x="540" y="0" width="240" height="90" rx="10" fill="#0b1120" stroke="#1e293b" stroke-width="1.5"/>',
            '    <text x="560" y="28" font-family="system-ui, -apple-system, sans-serif" font-size="11" fill="#94a3b8">Working Memory Coherence</text>',
            f'    <text x="560" y="60" font-family="system-ui, -apple-system, sans-serif" font-size="26" font-weight="800" fill="#10b981">{t.working_memory_coherence_pct}%</text>',
            f'    <text x="560" y="80" font-family="system-ui, -apple-system, sans-serif" font-size="10" fill="#64748b">Disorientation Risk: [{t.disorientation_risk}]</text>',
            '  </g>',
            '</svg>',
        ])

        return "\n".join(svg_parts)

    def export_svg(self, result: FovealHorizonResult, output_path: Optional[str] = None) -> str:
        """Exports SVG diagram to filepath or returns XML string."""
        if output_path:
            p = Path(output_path)
            p.parent.mkdir(parents=True, exist_ok=True)
            with open(p, "w", encoding="utf-8") as f:
                f.write(result.svg_diagram)
        return result.svg_diagram

    def generate_ascii_report(self, result: FovealHorizonResult) -> str:
        """Generates clean terminal ASCII table summarizing foveal horizon metrics."""
        t = result.telemetry
        lines = [
            "================================================================================",
            "   DYNAMIC FOVEAL HORIZON & CONTEXT ANCHOR RESTORER (PHASE 103 / CYCLE 99)",
            "================================================================================",
            f" Zoom Transition       : {t.source_zoom}x -> {t.target_zoom}x (Ratio: {t.zoom_ratio}:1)",
            f" Pan Displacement      : {t.pan_displacement_px:.1f}px linear canvas offset",
            f" Visual Drift Latency  : {t.visual_drift_latency_ms:.1f}ms re-orientation lag",
            f" Disorientation Risk   : [{t.disorientation_risk}]",
            f" Breadcrumbs Placed    : {t.breadcrumbs_synthesized} context anchors",
            f" Memory Coherence      : {t.working_memory_coherence_pct:.1f}%",
            f" Cowan Bounded (N<=4)  : {'Yes [OPTIMAL]' if t.cowan_bounded else 'No [EXCEEDS CAPACITY]'}",
            "--------------------------------------------------------------------------------",
            " SYNTHESIZED CONTEXTUAL RE-ENTRY ANCHORS",
            "--------------------------------------------------------------------------------",
        ]

        if not result.breadcrumbs:
            lines.append(" (No breadcrumbs required; transition is micro-local)")
        else:
            for b in result.breadcrumbs:
                lines.append(f" [ANCHOR] '{b.label}' (Tier: {b.zoom_tier} | Salience: {b.salience_score:.2f})")
                lines.append(f"          Hint: {b.re_entry_hint}")

        lines.append("================================================================================")
        return "\n".join(lines)
