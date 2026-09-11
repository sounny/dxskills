"""
Attentional Gaze Stabilizer and Scanpath Limiter Engine
Autonomous cognitive spatial module confining eye scanpaths to bounded thematic visual channels,
dampening peripheral saccadic jitter across high-density technical canvases.
Grounded in Carpenter LATER saccade dynamics, Bouma visual crowding law,
and Lavie perceptual load theory to protect dyslexic working memory from cognitive overload.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Any
import math
import html


@dataclass
class GazePoint:
    """Represents a discrete raw ocular gaze fixation or saccade sample."""
    point_id: str
    x: float
    y: float
    timestamp_ms: float
    fixation_dwell_ms: float = 120.0
    is_fixation: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "point_id": self.point_id,
            "x": round(self.x, 2),
            "y": round(self.y, 2),
            "timestamp_ms": round(self.timestamp_ms, 2),
            "fixation_dwell_ms": round(self.fixation_dwell_ms, 2),
            "is_fixation": self.is_fixation,
        }


@dataclass
class AttentionalChannel:
    """Bounded thematic corridor guiding eye movements along structured visual paths."""
    channel_id: str
    title: str
    points: List[Tuple[float, float]]
    envelope_width_px: float = 90.0
    priority: int = 1
    color: str = "#58a6ff"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "channel_id": self.channel_id,
            "title": self.title,
            "points": self.points,
            "envelope_width_px": round(self.envelope_width_px, 2),
            "priority": self.priority,
            "color": self.color,
        }


@dataclass
class StabilizedPoint:
    """Stabilized gaze coordinate after drift limitation and jitter dampening."""
    raw_point: GazePoint
    stabilized_x: float
    stabilized_y: float
    drift_distance_px: float
    is_within_envelope: bool
    jitter_dampened_px: float
    assigned_channel_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "raw_point": self.raw_point.to_dict(),
            "stabilized_x": round(self.stabilized_x, 2),
            "stabilized_y": round(self.stabilized_y, 2),
            "drift_distance_px": round(self.drift_distance_px, 2),
            "is_within_envelope": self.is_within_envelope,
            "jitter_dampened_px": round(self.jitter_dampened_px, 2),
            "assigned_channel_id": self.assigned_channel_id,
        }


@dataclass
class GazeStabilizationTelemetry:
    """Comprehensive telemetry describing gaze containment, jitter reduction, and stability."""
    total_gaze_points: int
    fixation_count: int
    saccade_count: int
    mean_drift_px: float
    max_drift_px: float
    envelope_containment_rate: float
    jitter_reduction_percent: float
    drift_alerts_count: int
    channels: List[AttentionalChannel]
    stabilized_points: List[StabilizedPoint]
    status_level: str = "OPTIMAL"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_gaze_points": self.total_gaze_points,
            "fixation_count": self.fixation_count,
            "saccade_count": self.saccade_count,
            "mean_drift_px": round(self.mean_drift_px, 2),
            "max_drift_px": round(self.max_drift_px, 2),
            "envelope_containment_rate": round(self.envelope_containment_rate, 4),
            "jitter_reduction_percent": round(self.jitter_reduction_percent, 2),
            "drift_alerts_count": self.drift_alerts_count,
            "status_level": self.status_level,
            "channels": [c.to_dict() for c in self.channels],
            "stabilized_points": [p.to_dict() for p in self.stabilized_points],
        }


class AttentionalGazeStabilizer:
    """
    Engine executing attentional funneling and gaze envelope stabilization.
    Projects raw scanpaths onto designated thematic channels, attenuating
    involuntary peripheral ocular drift while respecting purposeful saccadic jumps.
    """

    def __init__(self, default_envelope_width_px: float = 90.0, jitter_damping_factor: float = 0.65):
        self.default_envelope_width_px = max(10.0, default_envelope_width_px)
        self.jitter_damping_factor = max(0.0, min(1.0, jitter_damping_factor))

    @staticmethod
    def distance_point_to_segment(
        px: float, py: float, ax: float, ay: float, bx: float, by: float
    ) -> Tuple[float, Tuple[float, float]]:
        """Computes Euclidean distance and nearest projection point from P onto segment AB."""
        dx = bx - ax
        dy = by - ay
        seg_len_sq = dx * dx + dy * dy
        if seg_len_sq < 1e-9:
            dist = math.hypot(px - ax, py - ay)
            return dist, (ax, ay)
        
        t = ((px - ax) * dx + (py - ay) * dy) / seg_len_sq
        t_clamped = max(0.0, min(1.0, t))
        proj_x = ax + t_clamped * dx
        proj_y = ay + t_clamped * dy
        dist = math.hypot(px - proj_x, py - proj_y)
        return dist, (proj_x, proj_y)

    def find_nearest_channel_projection(
        self, px: float, py: float, channels: List[AttentionalChannel]
    ) -> Tuple[Optional[AttentionalChannel], float, Tuple[float, float]]:
        """Finds closest point on any channel centerline ribbon and the corresponding distance."""
        if not channels:
            return None, 0.0, (px, py)
        
        best_channel: Optional[AttentionalChannel] = None
        best_dist = float("inf")
        best_proj = (px, py)

        for channel in channels:
            pts = channel.points
            if len(pts) == 1:
                dist = math.hypot(px - pts[0][0], py - pts[0][1])
                if dist < best_dist:
                    best_dist = dist
                    best_channel = channel
                    best_proj = pts[0]
            else:
                for i in range(len(pts) - 1):
                    ax, ay = pts[i]
                    bx, by = pts[i + 1]
                    dist, proj = self.distance_point_to_segment(px, py, ax, ay, bx, by)
                    if dist < best_dist:
                        best_dist = dist
                        best_channel = channel
                        best_proj = proj

        return best_channel, best_dist, best_proj

    def stabilize_scanpath(
        self,
        raw_points: List[GazePoint],
        channels: Optional[List[AttentionalChannel]] = None,
    ) -> GazeStabilizationTelemetry:
        """
        Stabilizes raw eye scanpath points against bounded attentional channels.
        Calculates drift metrics, dampens jitter outside envelope limits,
        and derives stabilization telemetry.
        """
        active_channels = channels or []
        if not raw_points:
            return GazeStabilizationTelemetry(
                total_gaze_points=0,
                fixation_count=0,
                saccade_count=0,
                mean_drift_px=0.0,
                max_drift_px=0.0,
                envelope_containment_rate=1.0,
                jitter_reduction_percent=0.0,
                drift_alerts_count=0,
                channels=active_channels,
                stabilized_points=[],
                status_level="OPTIMAL",
            )

        stabilized_list: List[StabilizedPoint] = []
        drift_values: List[float] = []
        raw_jitters: List[float] = []
        stab_jitters: List[float] = []
        contained_count = 0
        alerts_count = 0
        fix_count = 0
        sac_count = 0

        for pt in raw_points:
            if pt.is_fixation:
                fix_count += 1
            else:
                sac_count += 1

            if not active_channels:
                stab_pt = StabilizedPoint(
                    raw_point=pt,
                    stabilized_x=pt.x,
                    stabilized_y=pt.y,
                    drift_distance_px=0.0,
                    is_within_envelope=True,
                    jitter_dampened_px=0.0,
                    assigned_channel_id=None,
                )
                stabilized_list.append(stab_pt)
                contained_count += 1
                continue

            channel, drift_dist, proj_pt = self.find_nearest_channel_projection(pt.x, pt.y, active_channels)
            envelope_half_width = (channel.envelope_width_px if channel else self.default_envelope_width_px) / 2.0
            is_inside = drift_dist <= envelope_half_width
            drift_values.append(drift_dist)

            if is_inside:
                contained_count += 1
                # Small drift inside comfort zone: light dampening to preserve organic gaze
                damping = self.jitter_damping_factor * 0.4
            else:
                alerts_count += 1
                # Exceeded envelope: strong dampening pulling toward channel boundary
                damping = self.jitter_damping_factor

            # Vector from raw point toward spine projection
            pull_x = proj_pt[0] - pt.x
            pull_y = proj_pt[1] - pt.y

            # Stabilized point moves fractionally along pull vector
            stab_x = pt.x + pull_x * damping
            stab_y = pt.y + pull_y * damping
            dampened_px = math.hypot(stab_x - pt.x, stab_y - pt.y)

            stab_pt = StabilizedPoint(
                raw_point=pt,
                stabilized_x=stab_x,
                stabilized_y=stab_y,
                drift_distance_px=drift_dist,
                is_within_envelope=is_inside,
                jitter_dampened_px=dampened_px,
                assigned_channel_id=channel.channel_id if channel else None,
            )
            stabilized_list.append(stab_pt)

        # Calculate high-frequency trajectory jitter comparison (step-to-step directional variance)
        if len(raw_points) >= 3:
            for i in range(len(raw_points) - 2):
                # Raw acceleration vector
                r_ax = raw_points[i + 2].x - 2 * raw_points[i + 1].x + raw_points[i].x
                r_ay = raw_points[i + 2].y - 2 * raw_points[i + 1].y + raw_points[i].y
                raw_jitters.append(math.hypot(r_ax, r_ay))

                # Stabilized acceleration vector
                s_ax = stabilized_list[i + 2].stabilized_x - 2 * stabilized_list[i + 1].stabilized_x + stabilized_list[i].stabilized_x
                s_ay = stabilized_list[i + 2].stabilized_y - 2 * stabilized_list[i + 1].stabilized_y + stabilized_list[i].stabilized_y
                stab_jitters.append(math.hypot(s_ax, s_ay))

            mean_raw_j = sum(raw_jitters) / len(raw_jitters) if raw_jitters else 1.0
            mean_stab_j = sum(stab_jitters) / len(stab_jitters) if stab_jitters else 1.0
            jitter_reduc = max(0.0, min(100.0, (1.0 - (mean_stab_j / (mean_raw_j + 1e-6))) * 100.0))
        else:
            jitter_reduc = 0.0

        mean_drift = sum(drift_values) / len(drift_values) if drift_values else 0.0
        max_drift = max(drift_values) if drift_values else 0.0
        containment_rate = contained_count / len(raw_points) if raw_points else 1.0

        # Assess status level
        if containment_rate >= 0.85 and alerts_count <= 2:
            status = "OPTIMAL"
        elif containment_rate >= 0.60:
            status = "STABILIZED"
        else:
            status = "CRITICAL_DRIFT"

        return GazeStabilizationTelemetry(
            total_gaze_points=len(raw_points),
            fixation_count=fix_count,
            saccade_count=sac_count,
            mean_drift_px=mean_drift,
            max_drift_px=max_drift,
            envelope_containment_rate=containment_rate,
            jitter_reduction_percent=jitter_reduc,
            drift_alerts_count=alerts_count,
            channels=active_channels,
            stabilized_points=stabilized_list,
            status_level=status,
        )

    def generate_markdown_report(self, telemetry: GazeStabilizationTelemetry) -> str:
        """Builds a comprehensive diagnostic Markdown report on gaze stabilization telemetry."""
        status_icons = {
            "OPTIMAL": "🟢",
            "STABILIZED": "🟡",
            "CRITICAL_DRIFT": "🔴",
        }
        icon = status_icons.get(telemetry.status_level, "⚪")

        lines = [
            "# Attentional Gaze Stabilizer & Scanpath Diagnostic Report",
            "",
            f"**Overall Status:** {icon} `{telemetry.status_level}`",
            "",
            "## Gaze Envelope Executive Metrics",
            "",
            "| Telemetry Parameter | Value | Theoretical Standard | Clinical Relevance |",
            "| :--- | :--- | :--- | :--- |",
            f"| **Total Gaze Points** | `{telemetry.total_gaze_points}` | N/A | Total ocular samples evaluated |",
            f"| **Fixation Count** | `{telemetry.fixation_count}` | > 70% of points | Primary reading dwell phases |",
            f"| **Saccade Count** | `{telemetry.saccade_count}` | < 30% of points | Rapid ballistic target transitions |",
            f"| **Envelope Containment** | `{telemetry.envelope_containment_rate * 100:.1f}%` | >= 85.0% | Bouma visual corridor safety index |",
            f"| **Mean Drift** | `{telemetry.mean_drift_px:.1f} px` | < 35.0 px | Average deviation from channel spine |",
            f"| **Peak Drift** | `{telemetry.max_drift_px:.1f} px` | < 75.0 px | Extreme outlier peripheral excursion |",
            f"| **Jitter Reduction** | `{telemetry.jitter_reduction_percent:.1f}%` | >= 25.0% | Damped high-frequency ocular tremor |",
            f"| **Drift Alerts** | `{telemetry.drift_alerts_count}` | <= 2 incidents | Visual crowding boundary violations |",
            "",
            "## Active Attentional Channels",
            "",
        ]

        if not telemetry.channels:
            lines.append("_No designated attentional channels defined; raw scanpath unconstrained._")
        else:
            lines.append("| Channel ID | Thematic Title | Waypoints | Envelope Width | Priority |")
            lines.append("| :--- | :--- | :--- | :--- | :--- |")
            for ch in telemetry.channels:
                lines.append(
                    f"| `{ch.channel_id}` | {ch.title} | {len(ch.points)} nodes | `{ch.envelope_width_px:.0f} px` | Priority {ch.priority} |"
                )
            lines.append("")

        lines.extend([
            "## Cognitive Architecture & Dyslexic Load Analysis",
            "",
            "- **Carpenter LATER Model:** Ballistic saccades that stray into high-density peripheral regions prolong decision latencies. Limiting drift bounds scanpaths to primary thematic axes.",
            "- **Bouma Visual Crowding:** Lateral interference collapses grapheme recognition when flanking noise sits within half an eccentricity radius. Stabilized envelopes enforce foveal isolation.",
            "- **Working Memory Preservation:** Mitigating involuntary saccadic wander eliminates disorientation, maintaining spatial mental models within Cowan four-chunk constraints.",
            "",
            "## Actionable Recommendations",
            "",
        ])

        if telemetry.status_level == "OPTIMAL":
            lines.append("1. **Maintain Current Density:** Thematic corridors are properly calibrated with excellent gaze containment.")
            lines.append("2. **Fluid Transition Continuity:** Scanpaths glide seamlessly across channel waypoints without abrupt visual breaks.")
        elif telemetry.status_level == "STABILIZED":
            lines.append("1. **Expand Envelope Padding:** Moderate drift detected; increase corridor width by 15-20 px to prevent premature border alerts.")
            lines.append("2. **Add Visual Waypoint Anchors:** Introduce subtle contrast beacons along channel spines to draw fixation.")
        else:
            lines.append("1. **Partition High-Density Zones:** Extreme ocular drift indicates severe visual crowding; segment the layout into distinct stepped stages.")
            lines.append("2. **Amplify Gaze Guidance Gaskets:** Enforce explicit high-contrast guide rails and suppress adjacent background stimuli.")

        return "\n".join(lines)

    def generate_svg(
        self,
        telemetry: GazeStabilizationTelemetry,
        width: int = 860,
        height: int = 560,
    ) -> str:
        """Renders an interactive dark titanium SVG visualization of the stabilized gaze envelope."""
        parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
            f'width="{width}" height="{height}" style="background-color: #0d1117; font-family: -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif;">',
            '<defs>',
            '  <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">',
            '    <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#21262d" stroke-width="0.75" />',
            '  </pattern>',
            '  <linearGradient id="envelopeGrad" x1="0%" y1="0%" x2="100%" y2="100%">',
            '    <stop offset="0%" stop-color="#58a6ff" stop-opacity="0.16" />',
            '    <stop offset="100%" stop-color="#38bdf8" stop-opacity="0.04" />',
            '  </linearGradient>',
            '  <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">',
            '    <feGaussianBlur stdDeviation="3" result="blur" />',
            '    <feComposite in="SourceGraphic" in2="blur" operator="over" />',
            '  </filter>',
            '</defs>',
            '<!-- Canvas Background & Grid -->',
            f'<rect width="{width}" height="{height}" fill="#0d1117" />',
            f'<rect width="{width}" height="{height}" fill="url(#grid)" opacity="0.65" />',
        ]

        # Draw Channels (Envelope corridors & spines)
        for ch in telemetry.channels:
            if len(ch.points) >= 2:
                # Envelope corridor (thick semi-transparent line)
                pts_str = " ".join(f"{x},{y}" for x, y in ch.points)
                parts.append(
                    f'<polyline points="{pts_str}" fill="none" stroke="{ch.color}" '
                    f'stroke-width="{ch.envelope_width_px}" stroke-opacity="0.12" stroke-linecap="round" stroke-linejoin="round" />'
                )
                # Outer envelope boundary lines (offset visualization via dashed line)
                parts.append(
                    f'<polyline points="{pts_str}" fill="none" stroke="{ch.color}" '
                    f'stroke-width="{ch.envelope_width_px}" stroke-opacity="0.30" stroke-dasharray="6,6" stroke-linecap="round" stroke-linejoin="round" />'
                )
                # Centerline spine
                parts.append(
                    f'<polyline points="{pts_str}" fill="none" stroke="{ch.color}" '
                    f'stroke-width="2.5" stroke-dasharray="4,4" stroke-opacity="0.85" />'
                )
                # Channel waypoint anchors
                for i, (wx, wy) in enumerate(ch.points):
                    parts.append(
                        f'<circle cx="{wx}" cy="{wy}" r="4.5" fill="#161b22" stroke="{ch.color}" stroke-width="2" />'
                    )
                    parts.append(
                        f'<text x="{wx}" y="{wy - 10}" fill="{ch.color}" font-size="10" font-weight="600" text-anchor="middle">{html.escape(ch.title)} #{i+1}</text>'
                    )

        # Draw Raw Scanpath (Muted red / gray dashed line with jitter markers)
        if len(telemetry.stabilized_points) >= 2:
            raw_pts_str = " ".join(f"{p.raw_point.x},{p.raw_point.y}" for p in telemetry.stabilized_points)
            parts.append(
                f'<polyline points="{raw_pts_str}" fill="none" stroke="#f85149" stroke-width="1.25" '
                f'stroke-dasharray="3,3" stroke-opacity="0.55" />'
            )

        # Draw Stabilization Correction Vectors (dashed lines linking raw to stabilized points)
        for p in telemetry.stabilized_points:
            if p.jitter_dampened_px > 1.5:
                stroke_col = "#d29922" if p.is_within_envelope else "#f85149"
                parts.append(
                    f'<line x1="{p.raw_point.x}" y1="{p.raw_point.y}" x2="{p.stabilized_x}" y2="{p.stabilized_y}" '
                    f'stroke="{stroke_col}" stroke-width="1" stroke-dasharray="2,2" stroke-opacity="0.75" />'
                )

        # Draw Stabilized Scanpath (Solid vibrant emerald path)
        if len(telemetry.stabilized_points) >= 2:
            stab_pts_str = " ".join(f"{p.stabilized_x},{p.stabilized_y}" for p in telemetry.stabilized_points)
            parts.append(
                f'<polyline points="{stab_pts_str}" fill="none" stroke="#3fb950" stroke-width="3" '
                f'stroke-linejoin="round" stroke-linecap="round" filter="url(#glow)" stroke-opacity="0.9" />'
            )

        # Draw Gaze Nodes
        for idx, p in enumerate(telemetry.stabilized_points):
            # Raw point marker
            r_col = "#f85149" if not p.is_within_envelope else "#8b949e"
            parts.append(
                f'<circle cx="{p.raw_point.x}" cy="{p.raw_point.y}" r="2.5" fill="{r_col}" opacity="0.6" />'
            )

            # Stabilized point marker (dwell size proportional to fixation duration)
            dwell_r = min(12.0, max(4.0, math.sqrt(p.raw_point.fixation_dwell_ms) * 0.7))
            s_col = "#3fb950" if p.is_within_envelope else "#d29922"
            parts.append(
                f'<circle cx="{p.stabilized_x}" cy="{p.stabilized_y}" r="{dwell_r}" fill="{s_col}" '
                f'fill-opacity="0.25" stroke="{s_col}" stroke-width="1.8" />'
            )
            # Center core
            parts.append(
                f'<circle cx="{p.stabilized_x}" cy="{p.stabilized_y}" r="2" fill="#ffffff" />'
            )
            # Index label
            parts.append(
                f'<text x="{p.stabilized_x + 8}" y="{p.stabilized_y + 4}" fill="#c9d1d9" font-size="9" font-family="monospace">{idx + 1}</text>'
            )

        # Header HUD
        parts.extend([
            '<!-- Header Titles -->',
            '<text x="28" y="38" fill="#58a6ff" font-size="18" font-weight="700" letter-spacing="0.5">ATTENTIONAL GAZE ENVELOPE STABILIZER</text>',
            '<text x="28" y="56" fill="#8b949e" font-size="11">Carpenter LATER Scanpath Confinement and Visual Jitter Dampener</text>',
        ])

        # Status badge
        badge_cols = {
            "OPTIMAL": ("#238636", "#3fb950"),
            "STABILIZED": ("#9e6a03", "#d29922"),
            "CRITICAL_DRIFT": ("#da3633", "#f85149"),
        }
        bg_col, fg_col = badge_cols.get(telemetry.status_level, ("#30363d", "#8b949e"))
        badge_x = width - 180
        parts.extend([
            f'<rect x="{badge_x}" y="22" width="152" height="34" rx="6" fill="{bg_col}" fill-opacity="0.3" stroke="{fg_col}" stroke-width="1.2" />',
            f'<circle cx="{badge_x + 18}" cy="39" r="5" fill="{fg_col}" />',
            f'<text x="{badge_x + 32}" y="43" fill="#f0f6fc" font-size="12" font-weight="700">{telemetry.status_level}</text>',
        ])

        # Telemetry HUD Card (Bottom Right)
        card_w = 320
        card_h = 138
        card_x = width - card_w - 24
        card_y = height - card_h - 24
        parts.extend([
            f'<g transform="translate({card_x}, {card_y})">',
            f'  <rect width="{card_w}" height="{card_h}" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1.5" />',
            '  <text x="16" y="24" fill="#f0f6fc" font-size="12" font-weight="700">Gaze Stabilization Telemetry</text>',
            f'  <line x1="16" y1="32" x2="{card_w - 16}" y2="32" stroke="#30363d" stroke-width="1" />',
            f'  <text x="16" y="52" fill="#8b949e" font-size="11">Envelope Containment:</text>',
            f'  <text x="{card_w - 16}" y="52" fill="#58a6ff" font-size="11" font-weight="600" text-anchor="end">{telemetry.envelope_containment_rate * 100:.1f}%</text>',
            f'  <text x="16" y="72" fill="#8b949e" font-size="11">Mean Gaze Drift:</text>',
            f'  <text x="{card_w - 16}" y="72" fill="#c9d1d9" font-size="11" font-weight="600" text-anchor="end">{telemetry.mean_drift_px:.1f} px</text>',
            f'  <text x="16" y="92" fill="#8b949e" font-size="11">Jitter Reduction:</text>',
            f'  <text x="{card_w - 16}" y="92" fill="#3fb950" font-size="11" font-weight="600" text-anchor="end">+{telemetry.jitter_reduction_percent:.1f}%</text>',
            f'  <text x="16" y="112" fill="#8b949e" font-size="11">Fixations / Saccades:</text>',
            f'  <text x="{card_w - 16}" y="112" fill="#e6edf3" font-size="11" font-weight="600" text-anchor="end">{telemetry.fixation_count} / {telemetry.saccade_count}</text>',
            '  <text x="16" y="128" fill="#8b949e" font-size="11">Peripheral Drift Alerts:</text>',
            f'  <text x="{card_w - 16}" y="128" fill="{"#f85149" if telemetry.drift_alerts_count > 0 else "#3fb950"}" font-size="11" font-weight="600" text-anchor="end">{telemetry.drift_alerts_count} events</text>',
            '</g>',
        ])

        # Legend (Bottom Left)
        leg_w = 340
        leg_h = 105
        leg_x = 24
        leg_y = height - leg_h - 24
        parts.extend([
            f'<g transform="translate({leg_x}, {leg_y})">',
            f'  <rect width="{leg_w}" height="{leg_h}" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1.2" opacity="0.9" />',
            '  <text x="16" y="20" fill="#f0f6fc" font-size="11" font-weight="700">Scanpath Legend</text>',
            '  <line x1="16" y1="36" x2="36" y2="36" stroke="#f85149" stroke-width="1.5" stroke-dasharray="3,3" />',
            '  <circle cx="26" cy="36" r="2.5" fill="#f85149" />',
            '  <text x="46" y="39" fill="#8b949e" font-size="10">Raw Gaze Scanpath (Peripheral Jitter)</text>',
            '  <line x1="16" y1="56" x2="36" y2="56" stroke="#3fb950" stroke-width="3" />',
            '  <circle cx="26" cy="56" r="4" fill="#3fb950" fill-opacity="0.3" stroke="#3fb950" stroke-width="1.5" />',
            '  <text x="46" y="59" fill="#8b949e" font-size="10">Stabilized Scanpath (LATER Optimized)</text>',
            '  <rect x="16" y="72" width="20" height="12" fill="#58a6ff" fill-opacity="0.25" stroke="#58a6ff" stroke-width="1" stroke-dasharray="2,2" />',
            '  <text x="46" y="82" fill="#8b949e" font-size="10">Attentional Corridor Envelope (Bouma Limit)</text>',
            '  <line x1="16" y1="94" x2="36" y2="94" stroke="#d29922" stroke-width="1" stroke-dasharray="2,2" />',
            '  <text x="46" y="97" fill="#8b949e" font-size="10">Jitter Dampening Correction Vector</text>',
            '</g>',
        ])

        parts.append('</svg>')
        return "\n".join(parts)

    @classmethod
    def create_demo_telemetry(cls) -> GazeStabilizationTelemetry:
        """Generates realistic demonstration scanpath telemetry for technical architecture viewing."""
        channels = [
            AttentionalChannel(
                channel_id="ch-data-stream",
                title="Telemetry Ingestion Flow",
                points=[(90.0, 140.0), (280.0, 160.0), (460.0, 150.0)],
                envelope_width_px=80.0,
                priority=1,
                color="#58a6ff",
            ),
            AttentionalChannel(
                channel_id="ch-transform-mesh",
                title="Cognitive Transform Matrix",
                points=[(460.0, 150.0), (520.0, 280.0), (380.0, 360.0)],
                envelope_width_px=85.0,
                priority=2,
                color="#38bdf8",
            ),
            AttentionalChannel(
                channel_id="ch-allocentric-output",
                title="Allocentric Projection Spine",
                points=[(380.0, 360.0), (220.0, 380.0), (120.0, 440.0)],
                envelope_width_px=90.0,
                priority=3,
                color="#a371f7",
            ),
        ]

        # Raw scanpath simulating natural jitter and a few peripheral excursions
        raw_points = [
            GazePoint("gp-1", 88.0, 138.0, 0.0, 180.0, True),
            GazePoint("gp-2", 145.0, 158.0, 210.0, 140.0, True),
            GazePoint("gp-3", 195.0, 132.0, 380.0, 110.0, True),  # slight upward jitter
            GazePoint("gp-4", 275.0, 162.0, 520.0, 240.0, True),
            GazePoint("gp-5", 340.0, 210.0, 780.0, 90.0, False),  # excursion outward
            GazePoint("gp-6", 455.0, 155.0, 900.0, 220.0, True),
            GazePoint("gp-7", 490.0, 210.0, 1140.0, 130.0, True),
            GazePoint("gp-8", 535.0, 285.0, 1300.0, 190.0, True),
            GazePoint("gp-9", 480.0, 310.0, 1510.0, 110.0, True),
            GazePoint("gp-10", 415.0, 420.0, 1650.0, 80.0, False), # peripheral drift outlier
            GazePoint("gp-11", 385.0, 355.0, 1760.0, 250.0, True),
            GazePoint("gp-12", 290.0, 375.0, 2030.0, 160.0, True),
            GazePoint("gp-13", 215.0, 382.0, 2220.0, 170.0, True),
            GazePoint("gp-14", 125.0, 438.0, 2410.0, 210.0, True),
        ]

        stabilizer = cls(default_envelope_width_px=85.0, jitter_damping_factor=0.7)
        return stabilizer.stabilize_scanpath(raw_points, channels)
