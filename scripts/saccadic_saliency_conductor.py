"""
Saccadic Saliency Conductor Engine
Autonomous cognitive spatial module guiding ballistic eye movements along optimal semantic gradients.
Grounded in Itti-Koch-Niebur visual saliency, Carpenter LATER saccade dynamics,
and Henderson cognitive guidance models to eliminate ocular regression and visual crowding.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Any
import math
import html


@dataclass
class SaliencyWaypoint:
    """Represents a visual fixation target with spatial and semantic coordinates."""
    waypoint_id: str
    label: str
    x: float
    y: float
    raw_saliency: float      # 0.0 to 1.0 (visual prominence)
    semantic_weight: float   # 0.0 to 1.0 (conceptual importance)
    order_index: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "waypoint_id": self.waypoint_id,
            "label": self.label,
            "x": round(self.x, 1),
            "y": round(self.y, 1),
            "raw_saliency": round(self.raw_saliency, 2),
            "semantic_weight": round(self.semantic_weight, 2),
            "order_index": self.order_index,
        }


@dataclass
class SaccadicTransition:
    """Represents a ballistic ocular leap between consecutive fixation waypoints."""
    from_waypoint_id: str
    to_waypoint_id: str
    distance_px: float
    ballistic_velocity_dps: float  # Degrees per second
    latency_ms: float
    is_regression: bool            # True if saccade moves counter to primary reading axis

    def to_dict(self) -> Dict[str, Any]:
        return {
            "from_waypoint_id": self.from_waypoint_id,
            "to_waypoint_id": self.to_waypoint_id,
            "distance_px": round(self.distance_px, 1),
            "ballistic_velocity_dps": round(self.ballistic_velocity_dps, 1),
            "latency_ms": round(self.latency_ms, 1),
            "is_regression": self.is_regression,
        }


@dataclass
class SaccadicConductorTelemetry:
    """Synthesized telemetry summarizing gaze trajectory guidance and ocular efficiency."""
    total_waypoints: int
    total_path_length_px: float
    mean_transition_latency_ms: float
    peak_velocity_dps: float
    regression_count: int
    saccadic_efficiency_score: float  # 0.0 to 100.0
    entropy_gradient_smoothness: float # 0.0 to 1.0
    status_level: str                 # OPTIMAL_SACCADIC_GUIDANCE, ELEVATED_REGRESSION_FATIGUE, ERRATIC_SALIENCY_CHAOS
    waypoints: List[SaliencyWaypoint]
    transitions: List[SaccadicTransition]
    warnings: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_waypoints": self.total_waypoints,
            "total_path_length_px": round(self.total_path_length_px, 1),
            "mean_transition_latency_ms": round(self.mean_transition_latency_ms, 1),
            "peak_velocity_dps": round(self.peak_velocity_dps, 1),
            "regression_count": self.regression_count,
            "saccadic_efficiency_score": round(self.saccadic_efficiency_score, 1),
            "entropy_gradient_smoothness": round(self.entropy_gradient_smoothness, 2),
            "status_level": self.status_level,
            "waypoints": [w.to_dict() for w in self.waypoints],
            "transitions": [t.to_dict() for t in self.transitions],
            "warnings": self.warnings,
        }


class SaccadicSaliencyConductor:
    """
    Computes optimal ocular scanpaths across semantic visual anchors,
    minimizing regressive saccades and visual search friction for dyslexic readers.
    """

    def __init__(
        self,
        px_per_degree: float = 35.0,
        base_saccade_latency_ms: float = 190.0,
        regression_penalty_weight: float = 1.4,
    ):
        self.px_per_degree = max(10.0, min(100.0, px_per_degree))
        self.base_saccade_latency_ms = max(120.0, min(350.0, base_saccade_latency_ms))
        self.regression_penalty_weight = max(1.0, min(3.0, regression_penalty_weight))

    def conduct_saliency_path(self, waypoints: List[SaliencyWaypoint]) -> SaccadicConductorTelemetry:
        """
        Calculates the ballistic trajectory across waypoints, assessing saccade velocity,
        regressive movements, and perceptual energy consumption.
        """
        if not waypoints:
            return SaccadicConductorTelemetry(
                total_waypoints=0,
                total_path_length_px=0.0,
                mean_transition_latency_ms=0.0,
                peak_velocity_dps=0.0,
                regression_count=0,
                saccadic_efficiency_score=100.0,
                entropy_gradient_smoothness=1.0,
                status_level="OPTIMAL_SACCADIC_GUIDANCE",
                waypoints=[],
                transitions=[],
                warnings=["No waypoints provided for saliency path conduction."],
            )

        # Ensure ordered waypoints
        ordered = sorted(waypoints, key=lambda w: w.order_index)
        transitions: List[SaccadicTransition] = []
        total_dist = 0.0
        latencies: List[float] = []
        velocities: List[float] = []
        regression_count = 0
        warnings: List[str] = []

        for i in range(len(ordered) - 1):
            w1 = ordered[i]
            w2 = ordered[i + 1]

            dx = w2.x - w1.x
            dy = w2.y - w1.y
            dist_px = math.hypot(dx, dy)
            total_dist += dist_px

            # Convert distance to visual degrees
            dist_deg = dist_px / self.px_per_degree

            # Saccadic main sequence velocity: v ~ 400 * (1 - exp(-d / 10)) + 50
            # saturates around 500-600 deg/s for large saccades
            velocity = 450.0 * (1.0 - math.exp(-max(0.1, dist_deg) / 8.0)) + 60.0
            velocities.append(velocity)

            # Latency incorporates Carpenter LATER decision delay + distance factor
            latency = self.base_saccade_latency_ms + math.sqrt(dist_deg) * 18.0
            latencies.append(latency)

            # Detect regression: right-to-left or upward jump against forward flow
            is_reg = dx < -20.0 or dy < -30.0
            if is_reg:
                regression_count += 1

            transitions.append(
                SaccadicTransition(
                    from_waypoint_id=w1.waypoint_id,
                    to_waypoint_id=w2.waypoint_id,
                    distance_px=dist_px,
                    ballistic_velocity_dps=velocity,
                    latency_ms=latency,
                    is_regression=is_reg,
                )
            )

        mean_lat = sum(latencies) / max(1, len(latencies))
        peak_vel = max(velocities) if velocities else 0.0

        # Calculate efficiency score based on regressions and path linearity
        direct_dist = math.hypot(ordered[-1].x - ordered[0].x, ordered[-1].y - ordered[0].y) if len(ordered) > 1 else total_dist
        efficiency_ratio = direct_dist / max(1.0, total_dist)
        reg_penalty = regression_count * 15.0 * self.regression_penalty_weight
        efficiency_score = max(10.0, min(100.0, 95.0 * efficiency_ratio - reg_penalty + 10.0))

        # Smoothness of saliency gradient along path
        saliency_diffs = [
            abs(ordered[j + 1].raw_saliency - ordered[j].raw_saliency)
            for j in range(len(ordered) - 1)
        ]
        mean_diff = sum(saliency_diffs) / max(1, len(saliency_diffs))
        smoothness = max(0.0, min(1.0, 1.0 - mean_diff))

        if regression_count >= 3 or efficiency_score < 50.0:
            status = "ERRATIC_SALIENCY_CHAOS"
            warnings.append(
                f"Elevated regressive saccades ({regression_count}) indicate visual disorientation and high cognitive drag."
            )
        elif regression_count >= 1 or efficiency_score < 75.0:
            status = "ELEVATED_REGRESSION_FATIGUE"
            warnings.append(
                f"Detected {regression_count} backward saccadic adjustments during scanpath execution."
            )
        else:
            status = "OPTIMAL_SACCADIC_GUIDANCE"

        return SaccadicConductorTelemetry(
            total_waypoints=len(ordered),
            total_path_length_px=total_dist,
            mean_transition_latency_ms=mean_lat,
            peak_velocity_dps=peak_vel,
            regression_count=regression_count,
            saccadic_efficiency_score=efficiency_score,
            entropy_gradient_smoothness=smoothness,
            status_level=status,
            waypoints=ordered,
            transitions=transitions,
            warnings=warnings,
        )

    def generate_markdown_report(self, telemetry: SaccadicConductorTelemetry) -> str:
        """Builds a structured diagnostic Markdown report on saccadic trajectory efficiency."""
        status_icons = {
            "OPTIMAL_SACCADIC_GUIDANCE": "🟢",
            "ELEVATED_REGRESSION_FATIGUE": "🟡",
            "ERRATIC_SALIENCY_CHAOS": "🔴",
        }
        icon = status_icons.get(telemetry.status_level, "⚪")

        lines = [
            "# Saccadic Saliency Conductor & Attentional Trajectory Report",
            "",
            f"**Scanpath Conduction Status:** {icon} `{telemetry.status_level}`",
            "",
            "## Ocular Kinematic & Saccadic Telemetry",
            "",
            "| Telemetry Parameter | Value | Reference Standard | Cognitive Guidance Impact |",
            "| :--- | :--- | :--- | :--- |",
            f"| **Total Fixation Waypoints** | `{telemetry.total_waypoints} points` | 4 - 8 semantic anchors | Working memory chunking bounds |",
            f"| **Cumulative Path Length** | `{telemetry.total_path_length_px:.1f} px` | Minimal Euclidean | Trajectory spatial efficiency |",
            f"| **Mean Transition Latency** | `{telemetry.mean_transition_latency_ms:.1f} ms` | 180 - 240 ms | Carpenter LATER ballistic decision delay |",
            f"| **Peak Saccadic Velocity** | `{telemetry.peak_velocity_dps:.1f} deg/s` | 300 - 550 deg/s | Rapid ballistic scanpath phase |",
            f"| **Regressive Saccades** | `{telemetry.regression_count} regressions` | 0 - 1 nominal | Back-tracking visual fatigue index |",
            f"| **Saccadic Efficiency Score** | `{telemetry.saccadic_efficiency_score:.1f} / 100` | >= 75.0 | Scanpath fluid alignment index |",
            f"| **Saliency Gradient Smoothness** | `{telemetry.entropy_gradient_smoothness * 100:.0f}%` | >= 70% | Continuous perceptual guidance |",
            "",
            "## Ballistic Saccade Transitions",
            "",
        ]

        if not telemetry.transitions:
            lines.append("_No ballistic transitions evaluated._")
        else:
            lines.append("| Step | From -> To | Distance | Ballistic Velocity | Latency | Movement Type |")
            lines.append("| :--- | :--- | :--- | :--- | :--- | :--- |")
            for i, t in enumerate(telemetry.transitions):
                m_type = "⚠️ Regression" if t.is_regression else "Forward Leap"
                lines.append(
                    f"| `{i+1}` | `{t.from_waypoint_id}` -> `{t.to_waypoint_id}` | `{t.distance_px:.0f} px` | `{t.ballistic_velocity_dps:.0f} deg/s` | `{t.latency_ms:.0f} ms` | {m_type} |"
                )
            lines.append("")

        if telemetry.warnings:
            lines.append("## Attentional Warnings & Recommendations")
            lines.append("")
            for w in telemetry.warnings:
                lines.append(f"- ⚠️ {w}")
            lines.append("")

        lines.extend([
            "## Cognitive Principles & Visual Trajectory Optimization",
            "",
            "- **Itti-Koch Saliency Guidance:** Structuring interface anchors along predictable visual gradients prevents involuntary attentional capture by peripheral clutter.",
            "- **Minimizing Regressive Backtracking:** For dyslexic readers, regressive saccades frequently result from phonological hesitation or line-jumping; linear guidance vectors reduce working memory re-encoding.",
            "- **Carpenter Ballistic Dynamics:** Saccades are ballistic and cannot be redirected mid-flight. Providing clear parafoveal previews ensures each landing point accurately targets meaningful semantic tokens.",
        ])

        return chr(10).join(lines)

    def generate_svg(
        self,
        telemetry: SaccadicConductorTelemetry,
        width: int = 880,
        height: int = 580,
    ) -> str:
        """Renders an interactive dark titanium SVG visual trajectory map with saliency contours."""
        parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
            f'width="{width}" height="{height}" style="background-color: #0d1117; font-family: -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif;">',
            '<defs>',
            '  <!-- Marker Arrow for Saccade Vectors -->',
            '  <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">',
            '    <path d="M 0 1 L 10 5 L 0 9 z" fill="#38bdf8" />',
            '  </marker>',
            '  <marker id="arrow-reg" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">',
            '    <path d="M 0 1 L 10 5 L 0 9 z" fill="#f85149" />',
            '  </marker>',
            '  <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">',
            '    <feGaussianBlur stdDeviation="3" result="blur" />',
            '    <feComposite in="SourceGraphic" in2="blur" operator="over" />',
            '  </filter>',
            '</defs>',
            '<!-- Canvas Base -->',
            f'<rect width="{width}" height="{height}" fill="#0d1117" />',
        ]

        # Cartesian Background Grid
        parts.append('<!-- Cartesian Grid Matrix -->')
        for gx in range(40, width, 50):
            parts.append(f'<line x1="{gx}" y1="0" x2="{gx}" y2="{height}" stroke="#161b22" stroke-width="1" />')
        for gy in range(40, height, 50):
            parts.append(f'<line x1="0" y1="{gy}" x2="{width}" y2="{gy}" stroke="#161b22" stroke-width="1" />')

        # Saliency Density Contours around Waypoints
        parts.append('<!-- Saliency Density Heat Fields -->')
        for w in telemetry.waypoints:
            r1 = max(15.0, w.raw_saliency * 55.0)
            r2 = r1 * 1.6
            parts.append(
                f'<circle cx="{w.x}" cy="{w.y}" r="{r2:.1f}" fill="#38bdf8" fill-opacity="0.04" />'
            )
            parts.append(
                f'<circle cx="{w.x}" cy="{w.y}" r="{r1:.1f}" fill="#38bdf8" fill-opacity="0.09" />'
            )

        # Draw Saccade Ballistic Vectors
        parts.append('<!-- Saccadic Ballistic Transitions -->')
        wp_map = {w.waypoint_id: w for w in telemetry.waypoints}
        for t in telemetry.transitions:
            if t.from_waypoint_id in wp_map and t.to_waypoint_id in wp_map:
                w1 = wp_map[t.from_waypoint_id]
                w2 = wp_map[t.to_waypoint_id]

                col = "#f85149" if t.is_regression else "#38bdf8"
                mkr = "url(#arrow-reg)" if t.is_regression else "url(#arrow)"
                dash = 'stroke-dasharray="4 4"' if t.is_regression else ""

                # Compute shortened line so arrow does not overlap waypoint halo
                dx = w2.x - w1.x
                dy = w2.y - w1.y
                d = max(1.0, math.hypot(dx, dy))
                ux = dx / d
                uy = dy / d
                x1 = w1.x + ux * 16.0
                y1 = w1.y + uy * 16.0
                x2 = w2.x - ux * 18.0
                y2 = w2.y - uy * 18.0

                parts.append(
                    f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="2" {dash} marker-end="{mkr}" />'
                )

                # Velocity pill mid-point
                mx = (x1 + x2) / 2.0
                my = (y1 + y2) / 2.0 - 8.0
                parts.append(
                    f'<text x="{mx:.1f}" y="{my:.1f}" fill="{col}" font-size="9" font-weight="600" text-anchor="middle">{t.ballistic_velocity_dps:.0f} dps</text>'
                )

        # Draw Fixation Waypoints
        parts.append('<!-- Fixation Halos & Anchors -->')
        for i, w in enumerate(telemetry.waypoints):
            node_col = "#58a6ff" if w.semantic_weight >= 0.7 else "#79c0ff"
            halo_r = 16.0

            # Outer ring
            parts.append(
                f'<circle cx="{w.x}" cy="{w.y}" r="{halo_r}" fill="#161b22" stroke="{node_col}" stroke-width="2" />'
            )
            # Center index number
            parts.append(
                f'<text x="{w.x}" y="{w.y + 4}" fill="#f0f6fc" font-size="11" font-weight="700" text-anchor="middle">{i + 1}</text>'
            )

            # Label text
            lbl_escaped = html.escape(w.label)
            parts.append(
                f'<text x="{w.x}" y="{w.y + halo_r + 14}" fill="#f0f6fc" font-size="10" font-weight="600" text-anchor="middle">{lbl_escaped}</text>'
            )

        # Top Header Bar
        parts.extend([
            '<!-- Header Block -->',
            '<text x="24" y="34" fill="#f0f6fc" font-size="16" font-weight="700">Saccadic Saliency Conductor</text>',
            '<text x="24" y="52" fill="#8b949e" font-size="11">Predictive Visual Saliency Gradients &amp; Ballistic Eye Movement Conductor</text>',
        ])

        # Status Badge (Top Right)
        status_colors = {
            "OPTIMAL_SACCADIC_GUIDANCE": ("#238636", "#3fb950"),
            "ELEVATED_REGRESSION_FATIGUE": ("#9e6a03", "#d29922"),
            "ERRATIC_SALIENCY_CHAOS": ("#da3633", "#f85149"),
        }
        bg_col, fg_col = status_colors.get(telemetry.status_level, ("#30363d", "#8b949e"))
        badge_x = width - 230
        parts.extend([
            f'<rect x="{badge_x}" y="20" width="206" height="34" rx="6" fill="{bg_col}" fill-opacity="0.25" stroke="{fg_col}" stroke-width="1.2" />',
            f'<circle cx="{badge_x + 16}" cy="37" r="5" fill="{fg_col}" />',
            f'<text x="{badge_x + 28}" y="41" fill="#f0f6fc" font-size="10" font-weight="700">{telemetry.status_level}</text>',
        ])

        # HUD Telemetry Card (Bottom Right)
        card_w = 320
        card_h = 146
        card_x = width - card_w - 24
        card_y = height - card_h - 24
        parts.extend([
            f'<g transform="translate({card_x}, {card_y})">',
            f'  <rect width="{card_w}" height="{card_h}" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1.5" />',
            '  <text x="16" y="24" fill="#f0f6fc" font-size="12" font-weight="700">Saccadic Scanpath Telemetry</text>',
            f'  <line x1="16" y1="32" x2="{card_w - 16}" y2="32" stroke="#30363d" stroke-width="1" />',
            f'  <text x="16" y="52" fill="#8b949e" font-size="11">Saccadic Efficiency Score:</text>',
            f'  <text x="{card_w - 16}" y="52" fill="#3fb950" font-size="11" font-weight="600" text-anchor="end">{telemetry.saccadic_efficiency_score:.1f} / 100</text>',
            f'  <text x="16" y="72" fill="#8b949e" font-size="11">Mean Saccade Latency:</text>',
            f'  <text x="{card_w - 16}" y="72" fill="#38bdf8" font-size="11" font-weight="600" text-anchor="end">{telemetry.mean_transition_latency_ms:.0f} ms</text>',
            f'  <text x="16" y="92" fill="#8b949e" font-size="11">Peak Ballistic Velocity:</text>',
            f'  <text x="{card_w - 16}" y="92" fill="#bc8cff" font-size="11" font-weight="600" text-anchor="end">{telemetry.peak_velocity_dps:.0f} deg/s</text>',
            f'  <text x="16" y="112" fill="#8b949e" font-size="11">Cumulative Path Distance:</text>',
            f'  <text x="{card_w - 16}" y="112" fill="#f0f6fc" font-size="11" font-weight="600" text-anchor="end">{telemetry.total_path_length_px:.0f} px</text>',
            f'  <text x="16" y="132" fill="#8b949e" font-size="11">Regressive Saccades:</text>',
            f'  <text x="{card_w - 16}" y="132" fill="#d29922" font-size="11" font-weight="600" text-anchor="end">{telemetry.regression_count} detected</text>',
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
            '  <text x="16" y="20" fill="#f0f6fc" font-size="11" font-weight="700">Trajectory Legend</text>',
            '  <line x1="16" y1="36" x2="36" y2="36" stroke="#38bdf8" stroke-width="2" marker-end="url(#arrow)" />',
            '  <text x="44" y="40" fill="#8b949e" font-size="10">Forward Ballistic Saccade Vector</text>',
            '  <line x1="16" y1="56" x2="36" y2="56" stroke="#f85149" stroke-width="2" stroke-dasharray="3 3" marker-end="url(#arrow-reg)" />',
            '  <text x="44" y="60" fill="#8b949e" font-size="10">Regressive Saccade (Backtracking)</text>',
            '  <circle cx="26" cy="82" r="7" fill="#161b22" stroke="#58a6ff" stroke-width="1.5" />',
            '  <text x="44" y="86" fill="#8b949e" font-size="10">Fixation Anchor (Sequential Halos 1..N)</text>',
            '</g>',
        ])

        parts.append('</svg>')
        return chr(10).join(parts)

    @classmethod
    def create_demo_telemetry(cls) -> SaccadicConductorTelemetry:
        """Constructs a realistic visual reading scanpath across documentation layout."""
        waypoints = [
            SaliencyWaypoint("wp-1", "Executive Header", 120.0, 140.0, 0.95, 0.9, order_index=0),
            SaliencyWaypoint("wp-2", "Architecture Diagram", 280.0, 170.0, 0.85, 0.85, order_index=1),
            SaliencyWaypoint("wp-3", "Core Pipeline Flow", 440.0, 210.0, 0.9, 0.95, order_index=2),
            SaliencyWaypoint("wp-4", "API Endpoint Specs", 580.0, 260.0, 0.75, 0.8, order_index=3),
            SaliencyWaypoint("wp-5", "Performance Metrics", 400.0, 340.0, 0.7, 0.75, order_index=4),  # Slight regression
            SaliencyWaypoint("wp-6", "Deployment Checklist", 550.0, 410.0, 0.8, 0.85, order_index=5),
        ]

        conductor = cls(px_per_degree=35.0, base_saccade_latency_ms=190.0)
        return conductor.conduct_saliency_path(waypoints)
