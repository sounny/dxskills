"""
Allocentric Compass & Coordinate Anchor Compass Engine
Autonomous cognitive spatial module for allocentric orientation tracking,
polar coordinate navigation, cardinal landmark alignment, and heading drift
stabilization across large spatial canvases. Grounded in Burgess allocentric
mapping models, Eide & Eide M-I-N-D framework, and spatial disorientation mitigation.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
import math
import html


@dataclass
class CanvasLandmark:
    """Represents a permanent spatial landmark on a wide canvas."""
    landmark_id: str
    title: str
    pos_x: float
    pos_y: float
    is_cardinal_north: bool = False
    importance: float = 1.0


@dataclass
class GazeTrajectoryWaypoint:
    """Represents an observed gaze/viewport position over time."""
    waypoint_id: str
    pos_x: float
    pos_y: float
    timestamp_ms: float


@dataclass
class OrientationFix:
    """Detailed polar orientation fix relative to the cardinal North anchor."""
    waypoint_id: str
    bearing_rad: float
    bearing_deg: float
    cardinal_sector: str  # N, NE, E, SE, S, SW, W, NW
    distance_to_north_px: float
    heading_drift_deg: float
    is_disoriented: bool


@dataclass
class AllocentricCompassTelemetry:
    """Comprehensive navigation telemetry for spatial orientation."""
    north_anchor_id: str
    north_coords: Tuple[float, float]
    total_fixes: int
    mean_bearing_deg: float
    angular_dispersion_deg: float
    disorientation_count: int
    orientation_fidelity_pct: float
    fixes: List[OrientationFix] = field(default_factory=list)


SECTORS = [
    ("N", -22.5, 22.5),
    ("NE", 22.5, 67.5),
    ("E", 67.5, 112.5),
    ("SE", 112.5, 157.5),
    ("S", 157.5, 202.5),
    ("SW", 202.5, 247.5),
    ("W", 247.5, 292.5),
    ("NW", 292.5, 337.5),
]


class AllocentricCompassTracker:
    """
    Autonomous engine that continuously measures viewport and gaze orientation
    relative to central allocentric landmarks. Prevents disorientation during
    prolonged panning across multi-megabyte canvas graphs.
    """

    def __init__(self, max_allowed_heading_jump_deg: float = 85.0):
        self.max_jump = float(max_allowed_heading_jump_deg)

    @staticmethod
    def resolve_cardinal_sector(bearing_deg: float) -> str:
        """Converts bearing degrees [0, 360) into a cardinal quadrant sector."""
        norm_deg = (bearing_deg + 360.0) % 360.0
        if norm_deg >= 337.5 or norm_deg < 22.5:
            return "N"
        for label, start, end in SECTORS[1:]:
            if start <= norm_deg < end:
                return label
        return "N"

    def evaluate_trajectory(
        self,
        landmarks: List[CanvasLandmark],
        trajectory: List[GazeTrajectoryWaypoint],
        drift_tolerance_deg: float = 45.0,
    ) -> AllocentricCompassTelemetry:
        """
        Calculates polar bearings, heading drift rates, and disorientation
        events across a sequence of navigation waypoints.
        """
        if not landmarks:
            north_anchor = CanvasLandmark("default-north", "Center Origin", 460.0, 280.0, True)
        else:
            north_anchor = next((l for l in landmarks if l.is_cardinal_north), landmarks[0])

        nx, ny = north_anchor.pos_x, north_anchor.pos_y

        if not trajectory:
            return AllocentricCompassTelemetry(
                north_anchor_id=north_anchor.landmark_id,
                north_coords=(round(nx, 2), round(ny, 2)),
                total_fixes=0,
                mean_bearing_deg=0.0,
                angular_dispersion_deg=0.0,
                disorientation_count=0,
                orientation_fidelity_pct=100.0,
                fixes=[],
            )

        fixes: List[OrientationFix] = []
        prev_bearing_deg: Optional[float] = None
        disorientation_events = 0
        all_bearings: List[float] = []

        for wp in trajectory:
            # Polar vector from North Anchor to current Waypoint
            dx = wp.pos_x - nx
            dy = wp.pos_y - ny
            dist = math.hypot(dx, dy)

            # Mathematical angle: atan2(dy, dx), convert to compass bearing: 0 deg = North (upwards, -y)
            # theta = atan2(dx, -dy)
            raw_rad = math.atan2(dx, -dy if abs(dy) > 1e-9 else 1e-9)
            bearing_deg = (math.degrees(raw_rad) + 360.0) % 360.0
            sector = self.resolve_cardinal_sector(bearing_deg)

            drift_deg = 0.0
            is_disoriented = False
            if prev_bearing_deg is not None:
                diff = abs(bearing_deg - prev_bearing_deg)
                if diff > 180.0:
                    diff = 360.0 - diff
                drift_deg = diff
                if diff > self.max_jump:
                    is_disoriented = True
                    disorientation_events += 1

            prev_bearing_deg = bearing_deg
            all_bearings.append(bearing_deg)

            fixes.append(
                OrientationFix(
                    waypoint_id=wp.waypoint_id,
                    bearing_rad=round(raw_rad, 3),
                    bearing_deg=round(bearing_deg, 2),
                    cardinal_sector=sector,
                    distance_to_north_px=round(dist, 2),
                    heading_drift_deg=round(drift_deg, 2),
                    is_disoriented=is_disoriented,
                )
            )

        # Circular mean calculation
        sin_sum = sum(math.sin(math.radians(b)) for b in all_bearings)
        cos_sum = sum(math.cos(math.radians(b)) for b in all_bearings)
        mean_deg = (math.degrees(math.atan2(sin_sum, cos_sum)) + 360.0) % 360.0

        # Angular dispersion metric
        r_length = math.hypot(sin_sum, cos_sum) / len(all_bearings)
        dispersion_deg = math.degrees(math.sqrt(max(0.0, 2.0 * (1.0 - r_length))))

        fidelity = max(
            0.0,
            min(100.0, 100.0 - (disorientation_events / len(fixes) * 100.0 * 2.0)),
        )

        return AllocentricCompassTelemetry(
            north_anchor_id=north_anchor.landmark_id,
            north_coords=(round(nx, 2), round(ny, 2)),
            total_fixes=len(fixes),
            mean_bearing_deg=round(mean_deg, 2),
            angular_dispersion_deg=round(dispersion_deg, 2),
            disorientation_count=disorientation_events,
            orientation_fidelity_pct=round(fidelity, 1),
            fixes=fixes,
        )

    def generate_markdown_report(self, telemetry: AllocentricCompassTelemetry) -> str:
        """Generates structured markdown audit report with zero em dashes."""
        lines = [
            "# Allocentric Compass and Coordinate Navigation Telemetry",
            "",
            "## 1. Executive Heading Overview",
            f"- **Cardinal North Anchor:** `{telemetry.north_anchor_id}` at ({telemetry.north_coords[0]}, {telemetry.north_coords[1]})",
            f"- **Total Navigation Fixes:** {telemetry.total_fixes}",
            f"- **Mean Allocentric Bearing:** {telemetry.mean_bearing_deg} deg",
            f"- **Angular Dispersion:** {telemetry.angular_dispersion_deg} deg",
            f"- **Disorientation Episodes:** {telemetry.disorientation_count}",
            f"- **Orientation Fidelity:** {telemetry.orientation_fidelity_pct}%",
            f"- **Navigational Status:** {'OPTIMAL ALIGNMENT' if telemetry.disorientation_count == 0 else 'DRIFT WARNING'}",
            "",
            "## 2. Theoretical Grounding",
            "- **Burgess Allocentric Mapping:** World-centered coordinates prevent cognitive vertigo during canvas pan operations.",
            "- **Cardinal Anchor Stabilizer:** Maintaining constant polar orientation to the core anchor preserves global context.",
            "- **Ocular Drift Gating:** Angular jumps above 85 degrees flag broken scanpaths requiring foveal re-centering.",
            "",
            "## 3. Navigation Waypoint Orientation Log",
            "| Waypoint ID | Bearing (deg) | Sector | Distance (px) | Drift (deg) | Status |",
            "| :--- | :--- | :--- | :--- | :--- | :--- |",
        ]

        for fix in telemetry.fixes:
            stat = "DISORIENTED" if fix.is_disoriented else "Aligned"
            lines.append(
                f"| `{fix.waypoint_id}` | {fix.bearing_deg} | `{fix.cardinal_sector}` | {fix.distance_to_north_px} | {fix.heading_drift_deg} | `{stat}` |"
            )

        lines.extend([
            "",
            "## 4. Operational Ergonomics Guidance",
            "- Anchor the main architectural module as Cardinal North to establish an intuitive spatial compass.",
            "- When orientation fidelity drops below 75%, inject smooth auto-panning restorative reticles.",
            "- Display persistent compass rose in viewport corner to anchor non-linear spatial thinkers.",
        ])

        return "\n".join(lines)

    def generate_svg(
        self,
        telemetry: AllocentricCompassTelemetry,
        width: int = 920,
        height: int = 560,
    ) -> str:
        """Generates publication-grade dark titanium polar compass rose SVG."""
        cx = width // 2
        cy = height // 2
        compass_r = 170.0

        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" style="background:#080d1a; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">',
            '<defs>',
            '  <radialGradient id="compassGlow" cx="50%" cy="50%" r="50%">',
            '    <stop offset="0%" stop-color="#0284c7" stop-opacity="0.25"/>',
            '    <stop offset="70%" stop-color="#0369a1" stop-opacity="0.06"/>',
            '    <stop offset="100%" stop-color="#080d1a" stop-opacity="0"/>',
            '  </radialGradient>',
            '  <filter id="needleGlow" x="-20%" y="-20%" width="140%" height="140%">',
            '    <feDropShadow dx="0" dy="0" stdDeviation="4" flood-color="#38bdf8" flood-opacity="0.8"/>',
            '  </filter>',
            '</defs>',
            '<!-- Polar Coordinate Reticle -->',
            f'<circle cx="{cx}" cy="{cy}" r="{compass_r + 40}" fill="url(#compassGlow)"/>',
            f'<circle cx="{cx}" cy="{cy}" r="{compass_r}" fill="#0f172a" stroke="#1e293b" stroke-width="2"/>',
            f'<circle cx="{cx}" cy="{cy}" r="{compass_r * 0.66}" fill="none" stroke="#334155" stroke-width="1" stroke-dasharray="3,3"/>',
            f'<circle cx="{cx}" cy="{cy}" r="{compass_r * 0.33}" fill="none" stroke="#334155" stroke-width="1" stroke-dasharray="2,2"/>',
        ]

        # Crosshairs
        svg_parts.append(f'<line x1="{cx}" y1="{cy - compass_r - 20}" x2="{cx}" y2="{cy + compass_r + 20}" stroke="#475569" stroke-width="1.2"/>')
        svg_parts.append(f'<line x1="{cx - compass_r - 20}" y1="{cy}" x2="{cx + compass_r + 20}" y2="{cy}" stroke="#475569" stroke-width="1.2"/>')

        # Cardinal Labels
        cardinal_positions = [
            ("N", cx, cy - compass_r - 8, "#38bdf8", 12),
            ("S", cx, cy + compass_r + 18, "#94a3b8", 11),
            ("E", cx + compass_r + 16, cy + 4, "#94a3b8", 11),
            ("W", cx - compass_r - 16, cy + 4, "#94a3b8", 11),
        ]
        for c_label, lx, ly, col, fs in cardinal_positions:
            svg_parts.append(
                f'<text x="{lx}" y="{ly}" font-size="{fs}" font-weight="700" fill="{col}" text-anchor="middle">{c_label}</text>'
            )

        # Plot Waypoint Fix Trail
        if telemetry.fixes:
            points_str = []
            for fix in telemetry.fixes:
                # Map distance into compass circle (normalized)
                norm_d = min(compass_r - 10, max(20.0, fix.distance_to_north_px * 0.35))
                rad = math.radians(fix.bearing_deg - 90.0)
                px = cx + norm_d * math.cos(rad)
                py = cy + norm_d * math.sin(rad)
                points_str.append(f"{px},{py}")

                # Draw fix node
                node_col = "#ef4444" if fix.is_disoriented else "#38bdf8"
                node_r = 5.0 if fix.is_disoriented else 3.5
                svg_parts.append(
                    f'<circle cx="{px}" cy="{py}" r="{node_r}" fill="{node_col}" stroke="#ffffff" stroke-width="1"/>'
                )

            svg_parts.append(
                f'<polyline points="{" ".join(points_str)}" fill="none" stroke="#0284c7" stroke-width="1.5" stroke-dasharray="2,3" opacity="0.7"/>'
            )

        # Primary Mean Bearing Needle
        mean_rad = math.radians(telemetry.mean_bearing_deg - 90.0)
        nx = cx + compass_r * 0.85 * math.cos(mean_rad)
        ny = cy + compass_r * 0.85 * math.sin(mean_rad)
        svg_parts.append(
            f'<line x1="{cx}" y1="{cy}" x2="{nx}" y2="{ny}" stroke="#38bdf8" stroke-width="3.0" filter="url(#needleGlow)"/>'
        )
        svg_parts.append(
            f'<circle cx="{cx}" cy="{cy}" r="6" fill="#38bdf8" stroke="#ffffff" stroke-width="2"/>'
        )

        # HUD Overlay Box
        svg_parts.append(
            f'<rect x="20" y="16" width="340" height="74" rx="8" fill="#0f172a" fill-opacity="0.88" stroke="#1e293b" stroke-width="1"/>'
        )
        svg_parts.append(
            f'<text x="32" y="36" font-size="11" font-weight="700" fill="#38bdf8">ALLOCENTRIC COMPASS HUD</text>'
        )
        svg_parts.append(
            f'<text x="32" y="52" font-size="9" fill="#94a3b8">Bearing: {telemetry.mean_bearing_deg} deg | Dispersion: {telemetry.angular_dispersion_deg} deg</text>'
        )
        svg_parts.append(
            f'<text x="32" y="68" font-size="9" fill="#94a3b8">Fidelity: {telemetry.orientation_fidelity_pct}% | Disorientation Events: {telemetry.disorientation_count}</text>'
        )

        svg_parts.append('</svg>')
        return "\n".join(svg_parts)


def sample_navigation_session() -> Tuple[List[CanvasLandmark], List[GazeTrajectoryWaypoint]]:
    """Provides demonstration landmarks and trajectory stream."""
    landmarks = [
        CanvasLandmark("core-system", "Architecture Core", 460.0, 280.0, is_cardinal_north=True, importance=5.0),
        CanvasLandmark("db-layer", "Persistence Tier", 460.0, 520.0, is_cardinal_north=False, importance=3.0),
        CanvasLandmark("ui-layer", "Frontend Surface", 200.0, 280.0, is_cardinal_north=False, importance=3.0),
        CanvasLandmark("auth-layer", "Auth Security Hub", 720.0, 280.0, is_cardinal_north=False, importance=3.0),
    ]

    waypoints = [
        GazeTrajectoryWaypoint("wp-1", 460.0, 200.0, 100.0),   # Directly North
        GazeTrajectoryWaypoint("wp-2", 580.0, 210.0, 350.0),   # North-East
        GazeTrajectoryWaypoint("wp-3", 650.0, 280.0, 600.0),   # East
        GazeTrajectoryWaypoint("wp-4", 620.0, 390.0, 850.0),   # South-East
        GazeTrajectoryWaypoint("wp-5", 460.0, 430.0, 1100.0),  # South
        GazeTrajectoryWaypoint("wp-6", 260.0, 420.0, 1350.0),  # South-West
        GazeTrajectoryWaypoint("wp-7", 220.0, 280.0, 1600.0),  # West
        GazeTrajectoryWaypoint("wp-8", 680.0, 120.0, 1900.0),  # Disorientation jump
    ]

    return landmarks, waypoints
