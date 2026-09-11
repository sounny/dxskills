"""
Autonomous Cognitive Spatial Working Memory Drift Compensator & Re-Centering Harness
===================================================================================
Theoretical Framework:
- Burgess & O'Keefe Allocentric Cognitive Mapping: Continuous spatial navigation
  across unbounded canvas environments accumulates path-integration drift errors.
- Virtual Magnetic Attractor Dynamics: Epistemic anchors act as gravitational potential
  wells exerting restoring forces (F = -k * Delta_r) to pull wandered attention back
  to the primary conceptual nexus.
- Cowan Capacity Bounds (N <= 4): Mitigates cognitive disorientation and working memory
  fragmentation caused by unconstrained navigational wandering.
- Strictly NO em dashes (\u2014) anywhere in code, docstrings, or outputs.
"""

import math
import json
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple

@dataclass
class EpistemicAnchor:
    """A primary cognitive reference point anchoring the spatial mental model."""
    anchor_id: str
    label: str
    x: float
    y: float
    mass: float  # Attractor gravitational strength (1.0 to 10.0)
    anchor_type: str  # root, synthesis_nexus, checkpoint

@dataclass
class DriftWaypoint:
    """A spatial gaze or navigation waypoint recorded along the search path."""
    step_idx: int
    x: float
    y: float
    duration_ms: float
    displacement_from_origin: float

@dataclass
class DriftTelemetry:
    """Telemetry measuring cumulative navigational displacement and restore force."""
    cumulative_drift_distance: float
    max_drift_displacement: float
    net_displacement_x: float
    net_displacement_y: float
    drift_entropy: float
    requires_recentering: bool
    restore_vector_x: float
    restore_vector_y: float
    restore_magnitude: float
    nearest_anchor_id: str

@dataclass
class DriftCompensatorResult:
    """Result containing anchors, waypoints, telemetry, SVG map, and audit report."""
    anchors: List[EpistemicAnchor]
    waypoints: List[DriftWaypoint]
    telemetry: DriftTelemetry
    drift_field_svg: str
    audit_report_md: str

    def to_dict(self) -> Dict[str, Any]:
        import dataclasses
        return {
            "anchors": [dataclasses.asdict(a) for a in self.anchors],
            "waypoints": [dataclasses.asdict(w) for w in self.waypoints],
            "telemetry": dataclasses.asdict(self.telemetry)
        }

class WorkingMemoryDriftCompensator:
    """
    Tracks navigational displacement across spatial mental models, detects
    allocentric drift beyond working memory bounds, and synthesizes magnetic
    re-centering vectors to restore equilibrium.
    """

    def __init__(self, drift_threshold: float = 350.0, spring_constant: float = 0.05):
        self.drift_threshold = drift_threshold
        self.spring_constant = spring_constant

    def compute_drift(
        self,
        waypoints_raw: List[Dict[str, Any]],
        anchors_raw: List[Dict[str, Any]],
        drift_threshold: Optional[float] = None
    ) -> DriftCompensatorResult:
        """Evaluates navigational waypoints against epistemic anchors."""
        threshold = drift_threshold if drift_threshold is not None else self.drift_threshold

        anchors: List[EpistemicAnchor] = []
        for idx, a in enumerate(anchors_raw):
            anchors.append(EpistemicAnchor(
                anchor_id=str(a.get("id", f"anchor_{idx+1}")),
                label=str(a.get("label", a.get("id", f"Anchor {idx+1}"))),
                x=float(a.get("x", 400.0)),
                y=float(a.get("y", 300.0)),
                mass=float(a.get("mass", 5.0)),
                anchor_type=str(a.get("type", "root"))
            ))

        if not anchors:
            anchors.append(EpistemicAnchor("root_nexus", "Primary Origin", 400.0, 300.0, 5.0, "root"))

        primary_anchor = anchors[0]
        origin_x = primary_anchor.x
        origin_y = primary_anchor.y

        waypoints: List[DriftWaypoint] = []
        cumulative_dist = 0.0
        max_displacement = 0.0
        prev_x, prev_y = origin_x, origin_y

        for idx, wp in enumerate(waypoints_raw):
            wx = float(wp.get("x", origin_x))
            wy = float(wp.get("y", origin_y))
            duration = float(wp.get("duration_ms", 500.0))

            step_dist = math.hypot(wx - prev_x, wy - prev_y)
            cumulative_dist += step_dist

            disp = math.hypot(wx - origin_x, wy - origin_y)
            if disp > max_displacement:
                max_displacement = disp

            waypoints.append(DriftWaypoint(
                step_idx=idx + 1,
                x=wx,
                y=wy,
                duration_ms=duration,
                displacement_from_origin=round(disp, 2)
            ))
            prev_x, prev_y = wx, wy

        # Current head position
        curr_x = waypoints[-1].x if waypoints else origin_x
        curr_y = waypoints[-1].y if waypoints else origin_y

        net_dx = curr_x - origin_x
        net_dy = curr_y - origin_y
        current_displacement = math.hypot(net_dx, net_dy)

        requires_recentering = current_displacement > threshold

        # Find nearest anchor
        nearest_anchor = anchors[0]
        min_anchor_dist = float("inf")
        for a in anchors:
            d = math.hypot(curr_x - a.x, curr_y - a.y)
            if d < min_anchor_dist:
                min_anchor_dist = d
                nearest_anchor = a

        # Compute magnetic restoring force vector toward nearest attractor
        rx = nearest_anchor.x - curr_x
        ry = nearest_anchor.y - curr_y
        restore_dist = math.hypot(rx, ry)

        # Scale force by mass and spring constant
        if restore_dist > 0.001:
            force_mag = round(self.spring_constant * restore_dist * (nearest_anchor.mass / 5.0), 3)
            unit_rx = rx / restore_dist
            unit_ry = ry / restore_dist
            restore_vx = round(unit_rx * force_mag, 3)
            restore_vy = round(unit_ry * force_mag, 3)
        else:
            force_mag = 0.0
            restore_vx = 0.0
            restore_vy = 0.0

        # Drift entropy: ratio of cumulative exploration path to direct displacement
        drift_entropy = round(cumulative_dist / max(1.0, current_displacement), 3)

        telemetry = DriftTelemetry(
            cumulative_drift_distance=round(cumulative_dist, 2),
            max_drift_displacement=round(max_displacement, 2),
            net_displacement_x=round(net_dx, 2),
            net_displacement_y=round(net_dy, 2),
            drift_entropy=drift_entropy,
            requires_recentering=requires_recentering,
            restore_vector_x=restore_vx,
            restore_vector_y=restore_vy,
            restore_magnitude=force_mag,
            nearest_anchor_id=nearest_anchor.anchor_id
        )

        svg = self.generate_svg(anchors, waypoints, telemetry, origin_x, origin_y, threshold)
        md = self.generate_markdown_report(anchors, waypoints, telemetry)

        return DriftCompensatorResult(
            anchors=anchors,
            waypoints=waypoints,
            telemetry=telemetry,
            drift_field_svg=svg,
            audit_report_md=md
        )

    def generate_svg(
        self,
        anchors: List[EpistemicAnchor],
        waypoints: List[DriftWaypoint],
        telemetry: DriftTelemetry,
        origin_x: float,
        origin_y: float,
        threshold: float,
        width: int = 800,
        height: int = 600
    ) -> str:
        """Renders dark titanium SVG showing anchor potential wells and restore vectors."""
        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">',
            '<defs>',
            '  <linearGradient id="titaniumDriftBg" x1="0%" y1="0%" x2="100%" y2="100%">',
            '    <stop offset="0%" stop-color="#141820" />',
            '    <stop offset="100%" stop-color="#0b0e14" />',
            '  </linearGradient>',
            '  <radialGradient id="anchorGlow" cx="50%" cy="50%" r="50%">',
            '    <stop offset="0%" stop-color="#58a6ff" stop-opacity="0.3" />',
            '    <stop offset="100%" stop-color="#58a6ff" stop-opacity="0.0" />',
            '  </radialGradient>',
            '  <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">',
            '    <path d="M 0 1 L 10 5 L 0 9 z" fill="#7ee787" />',
            '  </marker>',
            '</defs>',
            f'<rect width="{width}" height="{height}" rx="12" fill="url(#titaniumDriftBg)" stroke="#30363d" stroke-width="1.5" />',
            '<!-- Header -->',
            '<text x="24" y="36" fill="#58a6ff" font-family="sans-serif" font-size="16" font-weight="bold">Working Memory Allocentric Drift &amp; Re-Centering Field</text>',
            f'<text x="{width - 24}" y="36" fill="#8b949e" font-family="sans-serif" font-size="12" text-anchor="end">Status: {"RE-CENTERING NEEDED" if telemetry.requires_recentering else "EQUILIBRIUM STABLE"}</text>',
            f'<line x1="24" y1="48" x2="{width - 24}" y2="48" stroke="#30363d" stroke-width="1" />',
            '<!-- Drift Threshold Ring -->',
            f'<circle cx="{origin_x}" cy="{origin_y}" r="{threshold}" fill="none" stroke="#f85149" stroke-dasharray="6,6" stroke-width="1.2" opacity="0.6" />',
            f'<text x="{origin_x + 10}" y="{origin_y - threshold + 16}" fill="#f85149" font-family="sans-serif" font-size="10">Drift Boundary ({threshold}px)</text>'
        ]

        # Draw Anchors
        for a in anchors:
            glow_r = 25.0 * (a.mass / 5.0)
            svg_parts.append(f'<circle cx="{a.x}" cy="{a.y}" r="{glow_r}" fill="url(#anchorGlow)" />')
            svg_parts.append(f'<circle cx="{a.x}" cy="{a.y}" r="8" fill="#58a6ff" stroke="#c9d1d9" stroke-width="1.5" />')
            escaped_a_label = a.label.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            svg_parts.append(f'<text x="{a.x + 12}" y="{a.y + 4}" fill="#58a6ff" font-family="sans-serif" font-size="12" font-weight="bold">{escaped_a_label}</text>')

        # Draw Drift Path
        if len(waypoints) > 1:
            points_str = " ".join(f"{wp.x},{wp.y}" for wp in waypoints)
            svg_parts.append(f'<polyline points="{points_str}" fill="none" stroke="#ffa657" stroke-width="2" stroke-linejoin="round" opacity="0.8" />')

        # Draw Waypoints
        for wp in waypoints:
            svg_parts.append(f'<circle cx="{wp.x}" cy="{wp.y}" r="3.5" fill="#ffa657" />')

        # Draw Magnetic Restore Vector from final waypoint
        if waypoints:
            head = waypoints[-1]
            svg_parts.append(f'<circle cx="{head.x}" cy="{head.y}" r="6" fill="#f85149" stroke="#fff" stroke-width="1.5" />')
            svg_parts.append(f'<text x="{head.x + 10}" y="{head.y - 10}" fill="#f85149" font-family="sans-serif" font-size="11" font-weight="bold">Gaze Head</text>')

            if telemetry.requires_recentering:
                target_anchor = next((a for a in anchors if a.anchor_id == telemetry.nearest_anchor_id), anchors[0])
                svg_parts.append(f'<line x1="{head.x}" y1="{head.y}" x2="{target_anchor.x}" y2="{target_anchor.y}" stroke="#7ee787" stroke-width="2.5" stroke-dasharray="4,4" marker-end="url(#arrow)" />')
                mid_x = (head.x + target_anchor.x) / 2.0
                mid_y = (head.y + target_anchor.y) / 2.0
                svg_parts.append(f'<text x="{mid_x + 10}" y="{mid_y - 10}" fill="#7ee787" font-family="sans-serif" font-size="11" font-weight="bold">Restore Vector (F={telemetry.restore_magnitude:.2f})</text>')

        # Footer
        svg_parts.append(f'<line x1="24" y1="{height - 35}" x2="{width - 24}" y2="{height - 35}" stroke="#30363d" stroke-width="1" />')
        svg_parts.append(f'<text x="24" y="{height - 15}" fill="#8b949e" font-family="sans-serif" font-size="11">Cumulative Path: {telemetry.cumulative_drift_distance:.1f}px | Net Displacement: ({telemetry.net_displacement_x:.1f}, {telemetry.net_displacement_y:.1f}) | Entropy: {telemetry.drift_entropy:.2f}</text>')
        target_name = telemetry.nearest_anchor_id
        svg_parts.append(f'<text x="{width - 24}" y="{height - 15}" fill="#7ee787" font-family="sans-serif" font-size="11" text-anchor="end">Nearest Attractor: {target_name}</text>')
        svg_parts.append('</svg>')

        return "\n".join(svg_parts)

    def generate_markdown_report(
        self,
        anchors: List[EpistemicAnchor],
        waypoints: List[DriftWaypoint],
        telemetry: DriftTelemetry
    ) -> str:
        """Generates an audit report with strictly zero em dashes."""
        status_badge = "RE-CENTERING REQUIRED" if telemetry.requires_recentering else "EQUILIBRIUM NORMAL"
        lines = [
            "# Working Memory Drift & Allocentric Re-Centering Report",
            "",
            "## Navigational Displacement Metrics",
            f"- **System Equilibrium State:** {status_badge}",
            f"- **Cumulative Path Distance:** {telemetry.cumulative_drift_distance:.2f} px",
            f"- **Max Drift Displacement:** {telemetry.max_drift_displacement:.2f} px",
            f"- **Net Displacement Vector:** ({telemetry.net_displacement_x:.2f}, {telemetry.net_displacement_y:.2f}) px",
            f"- **Path Entropy Ratio:** {telemetry.drift_entropy:.3f}",
            f"- **Nearest Epistemic Attractor:** `{telemetry.nearest_anchor_id}`",
            f"- **Magnetic Restore Force Magnitude:** {telemetry.restore_magnitude:.3f}",
            "",
            "## Primary Epistemic Anchors",
            "",
            "| Anchor ID | Label | Coordinates (x, y) | Mass Strength | Type |",
            "| :--- | :--- | :--- | :--- | :--- |"
        ]

        for a in anchors:
            lines.append(f"| **{a.anchor_id}** | {a.label} | ({a.x:.1f}, {a.y:.1f}) | {a.mass:.1f} | {a.anchor_type} |")

        lines.extend([
            "",
            "## Navigational Trajectory Waypoints",
            "",
            "| Step | Coordinate (x, y) | Step Dwell (ms) | Distance from Origin (px) |",
            "| :--- | :--- | :--- | :--- |"
        ])

        for wp in waypoints:
            lines.append(f"| {wp.step_idx:02d} | ({wp.x:.1f}, {wp.y:.1f}) | {wp.duration_ms:.0f} | {wp.displacement_from_origin:.1f} |")

        lines.extend([
            "",
            "## Theoretical Grounding",
            "- **Burgess Allocentric Grid System:** Path integration errors are bounded before spatial representation collapses.",
            "- **Magnetic Attractor Physics:** Virtual restoring potential wells return wanderers along the path of least cognitive resistance.",
            "- **Cowan Buffer Preservation:** Prevents working memory fragmentation by anchoring sub-canvases to immutable reference nodes.",
            ""
        ])

        return "\n".join(lines)
