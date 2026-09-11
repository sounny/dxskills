"""
Allocentric Landmark Polar Grid & Dynamic Bearing Synthesizer Engine
Autonomous cognitive spatial module establishing world-centered polar coordinate frames,
concentric distance rings, cardinal ray bearings, and landmark relative vectors.
Grounded in Burgess allocentric spatial navigation models and O'Keefe cognitive maps
to eliminate spatial disorientation across large conceptual canvases.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Any
import math
import html


CARDINAL_SECTORS = [
    ("N", 337.5, 360.0),
    ("N", 0.0, 22.5),
    ("NE", 22.5, 67.5),
    ("E", 67.5, 112.5),
    ("SE", 112.5, 157.5),
    ("S", 157.5, 202.5),
    ("SW", 202.5, 247.5),
    ("W", 247.5, 292.5),
    ("NW", 292.5, 337.5),
]


@dataclass
class PolarLandmark:
    """Represents the primary allocentric origin hub."""
    landmark_id: str
    title: str
    x: float
    y: float
    radius_px: float = 16.0
    is_primary: bool = True


@dataclass
class TargetBearing:
    """Calculated polar bearing and radial distance of a target relative to the landmark."""
    target_id: str
    title: str
    pos_x: float
    pos_y: float
    distance_px: float
    bearing_deg: float  # 0.0 to 360.0 deg (0=North, 90=East)
    cardinal_heading: str
    range_ring_zone: str  # Inner Core, Meso Orbit, Peripheral Horizon


@dataclass
class PolarGridTelemetry:
    """Comprehensive telemetry report for allocentric polar coordinate frames."""
    primary_landmark: PolarLandmark
    target_count: int
    max_range_px: float
    ring_count: int
    target_bearings: List[TargetBearing] = field(default_factory=list)
    angular_dispersion_index: float = 0.0
    allocentric_stability_score: float = 0.0


class AllocentricPolarGridSynthesizer:
    """
    Autonomous engine that projects allocentric polar reference grids and
    synthesizes directional bearings to anchor working memory.
    """

    def __init__(self, default_ring_interval_px: float = 120.0, num_rings: int = 3):
        self.ring_interval_px = float(default_ring_interval_px)
        self.num_rings = max(1, int(num_rings))

    @staticmethod
    def resolve_cardinal_heading(bearing_deg: float) -> str:
        """Maps an angular bearing (0-360 deg, North=0, clockwise) to an 8-point compass heading."""
        b = bearing_deg % 360.0
        for name, start, end in CARDINAL_SECTORS:
            if start <= b < end:
                return name
        return "N"

    def calculate_polar_bearings(
        self,
        landmark: PolarLandmark,
        targets: List[Dict[str, Any]],
    ) -> PolarGridTelemetry:
        """
        Calculates radial distance, clockwise bearing from North, cardinal sector,
        and orbit zone for all target entities relative to the origin landmark.
        """
        if not targets:
            return PolarGridTelemetry(
                primary_landmark=landmark,
                target_count=0,
                max_range_px=self.ring_interval_px * self.num_rings,
                ring_count=self.num_rings,
                target_bearings=[],
                angular_dispersion_index=0.0,
                allocentric_stability_score=1.0,
            )

        bearings: List[TargetBearing] = []
        max_dist = self.ring_interval_px * self.num_rings

        for t in targets:
            tid = str(t.get("id", t.get("target_id", "target")))
            title = str(t.get("title", "Target"))
            tx = float(t.get("x", t.get("pos_x", 0.0)))
            ty = float(t.get("y", t.get("pos_y", 0.0)))

            dx = tx - landmark.x
            dy = ty - landmark.y
            dist = math.hypot(dx, dy)

            # Compass bearing: 0 deg = North (up, negative Y), 90 deg = East (right, positive X)
            # Standard atan2(dy, dx) has 0 at positive X (East), positive Y (Down)
            # In screen coords: dx is positive East, -dy is positive North
            # angle from North = atan2(dx, -dy)
            bearing_rad = math.atan2(dx, -dy)
            bearing_deg = (math.degrees(bearing_rad) + 360.0) % 360.0
            heading = self.resolve_cardinal_heading(bearing_deg)

            if dist <= self.ring_interval_px:
                zone = "Inner Core"
            elif dist <= self.ring_interval_px * 2:
                zone = "Meso Orbit"
            else:
                zone = "Peripheral Horizon"

            bearings.append(
                TargetBearing(
                    target_id=tid,
                    title=title,
                    pos_x=round(tx, 1),
                    pos_y=round(ty, 1),
                    distance_px=round(dist, 1),
                    bearing_deg=round(bearing_deg, 1),
                    cardinal_heading=heading,
                    range_ring_zone=zone,
                )
            )

        # Sort by distance
        bearings.sort(key=lambda b: b.distance_px)

        # Calculate angular dispersion: standard deviation of angles mapped to [0, 1]
        angles = [b.bearing_deg for b in bearings]
        mean_angle = sum(angles) / len(angles)
        variance = sum((a - mean_angle) ** 2 for a in angles) / len(angles)
        std_dev = math.sqrt(variance)
        dispersion = min(1.0, round(std_dev / 180.0, 3))

        # Stability score: higher if nodes are well-distributed across zones and sectors
        stability = round(0.6 + 0.4 * dispersion, 2)

        return PolarGridTelemetry(
            primary_landmark=landmark,
            target_count=len(bearings),
            max_range_px=round(max_dist, 1),
            ring_count=self.num_rings,
            target_bearings=bearings,
            angular_dispersion_index=dispersion,
            allocentric_stability_score=stability,
        )

    def generate_markdown_report(self, telemetry: PolarGridTelemetry) -> str:
        """Generates structured markdown audit report with zero em dashes."""
        lm = telemetry.primary_landmark
        lines = [
            "# Allocentric Landmark Polar Grid and Dynamic Bearing Report",
            "",
            "## 1. Allocentric Frame of Reference Overview",
            f"- **Primary Reference Landmark:** {lm.title} (`{lm.landmark_id}`) at ({lm.x}, {lm.y}) px",
            f"- **Monitored Spatial Targets:** {telemetry.target_count}",
            f"- **Concentric Range Rings:** {telemetry.ring_count} rings (Max Horizon: {telemetry.max_range_px} px)",
            f"- **Angular Dispersion Index:** {telemetry.angular_dispersion_index} (Scale: 0.0 to 1.0)",
            f"- **Allocentric Stability Score:** {telemetry.allocentric_stability_score} (Optimal >= 0.75)",
            "",
            "## 2. Neuro-Cognitive Theoretical Basis",
            "- **Burgess Allocentric Frame:** Anchors spatial mental maps to permanent global environment landmarks.",
            "- **O'Keefe Place/Grid Cells:** Polar distance rings mimic entorhinal grid firing fields.",
            "- **Orientation Drift Compensation:** Knowing relative compass heading prevents pan-and-scan cognitive disorientation.",
            "",
            "## 3. Target Bearing & Polar Coordinate Catalog",
            "| Target ID | Title | Distance (px) | Bearing (deg) | Heading | Zone | Position (x, y) |",
            "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |",
        ]

        for b in telemetry.target_bearings:
            lines.append(
                f"| `{b.target_id}` | {b.title} | {b.distance_px} | {b.bearing_deg} deg | `{b.cardinal_heading}` | {b.range_ring_zone} | ({b.pos_x}, {b.pos_y}) |"
            )

        lines.extend([
            "",
            "## 4. Operational Ergonomics Guidance",
            "- Use the primary landmark as a permanent visual anchor during rapid zoom-out transitions.",
            "- Cluster secondary tactical nodes within the 'Inner Core' (<= 120 px) to minimize saccadic jump fatigue.",
            "- Peripheral horizon nodes should emit subtle polar guidance rays toward the landmark hub.",
        ])

        return "\n".join(lines)

    def generate_svg(
        self,
        telemetry: PolarGridTelemetry,
        width: int = 920,
        height: int = 560,
    ) -> str:
        """Generates publication-grade dark titanium polar radar grid SVG."""
        lm = telemetry.primary_landmark
        cx, cy = lm.x, lm.y

        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" style="background:#090d18; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">',
            '<defs>',
            '  <filter id="radarGlow" x="-20%" y="-20%" width="140%" height="140%">',
            '    <feGaussianBlur stdDeviation="3" result="blur"/>',
            '    <feComposite in="SourceGraphic" in2="blur" operator="over"/>',
            '  </filter>',
            '</defs>',
            f'<rect x="0" y="0" width="{width}" height="{height}" fill="#090d18"/>',
            '<!-- Polar Range Rings -->',
        ]

        for r_idx in range(1, telemetry.ring_count + 1):
            r = self.ring_interval_px * r_idx
            svg_parts.append(
                f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#1e293b" stroke-width="1.2" stroke-dasharray="4,4"/>'
            )
            svg_parts.append(
                f'<text x="{cx + 6}" y="{cy - r + 12}" font-size="8" fill="#64748b">{int(r)} px</text>'
            )

        # Cardinal Spokes (N, S, E, W, NE, NW, SE, SW)
        max_r = telemetry.max_range_px
        spokes = [
            (0.0, "N"), (45.0, "NE"), (90.0, "E"), (135.0, "SE"),
            (180.0, "S"), (225.0, "SW"), (270.0, "W"), (315.0, "NW")
        ]
        for deg, label in spokes:
            rad = math.radians(deg)
            sx = cx + max_r * math.sin(rad)
            sy = cy - max_r * math.cos(rad)
            stroke_w = "1.2" if deg % 90 == 0 else "0.7"
            stroke_c = "#334155" if deg % 90 == 0 else "#1e293b"
            svg_parts.append(
                f'<line x1="{cx}" y1="{cy}" x2="{sx}" y2="{sy}" stroke="{stroke_c}" stroke-width="{stroke_w}"/>'
            )
            svg_parts.append(
                f'<text x="{cx + (max_r + 14) * math.sin(rad)}" y="{cy - (max_r + 14) * math.cos(rad) + 4}" font-size="9" font-weight="700" fill="#94a3b8" text-anchor="middle">{label}</text>'
            )

        # Target Bearing Vectors & Dots
        for b in telemetry.target_bearings:
            # Ray line from landmark to target
            svg_parts.append(
                f'<line x1="{cx}" y1="{cy}" x2="{b.pos_x}" y2="{b.pos_y}" stroke="#38bdf8" stroke-width="1.0" stroke-dasharray="2,2" opacity="0.4"/>'
            )
            # Target node circle
            svg_parts.append(
                f'<circle cx="{b.pos_x}" cy="{b.pos_y}" r="7" fill="#0284c7" stroke="#ffffff" stroke-width="1.5"/>'
            )
            svg_parts.append(
                f'<text x="{b.pos_x}" y="{b.pos_y + 16}" font-size="8.5" font-weight="600" fill="#ffffff" text-anchor="middle">{html.escape(b.title)}</text>'
            )
            svg_parts.append(
                f'<text x="{b.pos_x}" y="{b.pos_y + 25}" font-size="7" fill="#94a3b8" text-anchor="middle">{b.bearing_deg} deg ({int(b.distance_px)}px)</text>'
            )

        # Primary Landmark Hub (Center)
        svg_parts.append(
            f'<circle cx="{cx}" cy="{cy}" r="{lm.radius_px}" fill="#0f172a" stroke="#38bdf8" stroke-width="2.5" filter="url(#radarGlow)"/>'
        )
        svg_parts.append(
            f'<circle cx="{cx}" cy="{cy}" r="5" fill="#38bdf8"/>'
        )
        svg_parts.append(
            f'<text x="{cx}" y="{cy - lm.radius_px - 8}" font-size="10" font-weight="700" fill="#38bdf8" text-anchor="middle">{html.escape(lm.title.upper())}</text>'
        )

        # HUD Box
        svg_parts.append(
            f'<rect x="20" y="20" width="390" height="74" rx="8" fill="#0f172a" fill-opacity="0.92" stroke="#38bdf8" stroke-width="1.2"/>'
        )
        svg_parts.append(
            '<text x="32" y="38" font-size="11" font-weight="700" fill="#38bdf8">ALLOCENTRIC POLAR GRID HUD</text>'
        )
        svg_parts.append(
            f'<text x="32" y="54" font-size="9" fill="#94a3b8">Origin: ({int(cx)}, {int(cy)}) px | Targets: {telemetry.target_count} | Rings: {telemetry.ring_count}</text>'
        )
        svg_parts.append(
            f'<text x="32" y="70" font-size="9" fill="#94a3b8">Dispersion: {telemetry.angular_dispersion_index} | Allocentric Stability: {telemetry.allocentric_stability_score}</text>'
        )

        svg_parts.append('</svg>')
        return "\n".join(svg_parts)


def sample_polar_session() -> Tuple[PolarLandmark, List[Dict[str, Any]]]:
    """Generates demonstration allocentric landmark origin and surrounding target nodes."""
    landmark = PolarLandmark("lm-core", "Kernel Dispatcher Hub", 460.0, 280.0, 16.0, True)

    targets = [
        {"id": "tgt-1", "title": "Memory Allocator", "x": 460.0, "y": 180.0},     # Due North (100 px, 0 deg)
        {"id": "tgt-2", "title": "Network Socket", "x": 620.0, "y": 200.0},       # North-East (178 px, ~63 deg)
        {"id": "tgt-3", "title": "Disk I/O Controller", "x": 680.0, "y": 280.0},   # Due East (220 px, 90 deg)
        {"id": "tgt-4", "title": "IPC Pipe Queue", "x": 580.0, "y": 420.0},       # South-East (184 px, ~140 deg)
        {"id": "tgt-5", "title": "Thread Scheduler", "x": 460.0, "y": 500.0},     # Due South (220 px, 180 deg)
        {"id": "tgt-6", "title": "Telemetry Exporter", "x": 240.0, "y": 400.0},   # South-West (250 px, ~241 deg)
        {"id": "tgt-7", "title": "Security Sandbox", "x": 200.0, "y": 280.0},     # Due West (260 px, 270 deg)
        {"id": "tgt-8", "title": "Signal Handler", "x": 300.0, "y": 140.0},       # North-West (212 px, ~311 deg)
    ]

    return landmark, targets
