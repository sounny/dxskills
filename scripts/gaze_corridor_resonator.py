"""
Gaze Corridor Resonator and Dynamic Attentional Funnel Engine
Autonomous cognitive spatial module synchronizing parafoveal preview envelopes
with ocular scanpath velocities across technical diagrams and code layouts.
Grounded in Keith Rayner eye-movement reading science, Carpenter LATER saccade dynamics,
and Eide Interconnected Reasoning to eliminate fixation latency and visual crowding.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Any
import math
import html


@dataclass
class GazeSample:
    """Discrete ocular fixation or saccadic tracking sample."""
    sample_id: str
    x: float
    y: float
    timestamp_ms: float
    dwell_ms: float = 120.0
    modality: str = "TEXT"  # TEXT, CODE, SCHEMATIC, DIAGRAM

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sample_id": self.sample_id,
            "x": round(self.x, 2),
            "y": round(self.y, 2),
            "timestamp_ms": round(self.timestamp_ms, 2),
            "dwell_ms": round(self.dwell_ms, 2),
            "modality": self.modality,
        }


@dataclass
class ResonantCorridorSegment:
    """Dynamic conduit segment calibrated to local scanpath velocity and lookahead."""
    segment_id: str
    start_x: float
    start_y: float
    target_x: float
    target_y: float
    velocity_px_ms: float
    lookahead_px: float
    funnel_radius_px: float
    preview_cone_angle_deg: float
    resonance_efficiency: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "segment_id": self.segment_id,
            "start_x": round(self.start_x, 2),
            "start_y": round(self.start_y, 2),
            "target_x": round(self.target_x, 2),
            "target_y": round(self.target_y, 2),
            "velocity_px_ms": round(self.velocity_px_ms, 3),
            "lookahead_px": round(self.lookahead_px, 2),
            "funnel_radius_px": round(self.funnel_radius_px, 2),
            "preview_cone_angle_deg": round(self.preview_cone_angle_deg, 1),
            "resonance_efficiency": round(self.resonance_efficiency, 3),
        }


@dataclass
class GazeCorridorTelemetry:
    """Comprehensive telemetry describing parafoveal synchronization and conduit dynamics."""
    total_samples: int
    segments: List[ResonantCorridorSegment]
    mean_scanpath_velocity: float
    peak_saccade_velocity: float
    mean_funnel_aperture_px: float
    parafoveal_synchrony_rate: float
    overdrive_events_count: int
    status_level: str
    samples: List[GazeSample]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_samples": self.total_samples,
            "mean_scanpath_velocity": round(self.mean_scanpath_velocity, 3),
            "peak_saccade_velocity": round(self.peak_saccade_velocity, 3),
            "mean_funnel_aperture_px": round(self.mean_funnel_aperture_px, 2),
            "parafoveal_synchrony_rate": round(self.parafoveal_synchrony_rate, 3),
            "overdrive_events_count": self.overdrive_events_count,
            "status_level": self.status_level,
            "samples": [s.to_dict() for s in self.samples],
            "segments": [seg.to_dict() for seg in self.segments],
        }


class GazeCorridorResonator:
    """
    Dynamically adjusts parafoveal preview spans and focal aperture widths
    in real time according to ballistic ocular velocities.
    """

    def __init__(
        self,
        saccadic_latency_ms: float = 180.0,
        base_aperture_px: float = 45.0,
        velocity_scale: float = 65.0,
    ):
        self.saccadic_latency_ms = max(50.0, min(400.0, saccadic_latency_ms))
        self.base_aperture_px = max(15.0, min(120.0, base_aperture_px))
        self.velocity_scale = max(10.0, min(200.0, velocity_scale))

    def synchronize_corridor(self, samples: List[GazeSample]) -> GazeCorridorTelemetry:
        """
        Calculates velocity vectors, forward lookahead projections,
        and adaptive conduit bounds across sequential gaze waypoints.
        """
        if not samples or len(samples) < 2:
            return GazeCorridorTelemetry(
                total_samples=len(samples) if samples else 0,
                segments=[],
                mean_scanpath_velocity=0.0,
                peak_saccade_velocity=0.0,
                mean_funnel_aperture_px=self.base_aperture_px,
                parafoveal_synchrony_rate=1.0,
                overdrive_events_count=0,
                status_level="SYNCHRONIZED",
                samples=samples or [],
            )

        segments: List[ResonantCorridorSegment] = []
        velocities: List[float] = []
        apertures: List[float] = []
        overdrive_count = 0
        synchronous_segments = 0

        for i in range(len(samples) - 1):
            s1 = samples[i]
            s2 = samples[i + 1]

            dist_px = math.hypot(s2.x - s1.x, s2.y - s1.y)
            delta_t = max(10.0, s2.timestamp_ms - s1.timestamp_ms)
            v = dist_px / delta_t  # px/ms
            velocities.append(v)

            # Predictive lookahead D = v * latency
            lookahead = v * self.saccadic_latency_ms

            # Dynamic focal aperture widens during ballistic saccades to prime parafoveal targets
            # and contracts during fixations to shield fovea from crowding
            aperture = self.base_aperture_px + (v * self.velocity_scale)
            apertures.append(aperture)

            # Lookahead cone angle (narrower at high speeds, wider at low speeds)
            cone_angle = max(20.0, min(65.0, 50.0 - (v * 15.0)))

            # Resonance efficiency: how well the lookahead aligns with the actual target distance
            if dist_px > 1e-3:
                ratio = min(lookahead / dist_px, dist_px / (lookahead + 1e-6))
                res_eff = max(0.2, min(1.0, ratio))
            else:
                res_eff = 1.0

            if res_eff >= 0.50:
                synchronous_segments += 1
            if v > 1.8:  # Extremely rapid ballistic jump
                overdrive_count += 1

            seg = ResonantCorridorSegment(
                segment_id=f"seg-{i+1}",
                start_x=s1.x,
                start_y=s1.y,
                target_x=s2.x,
                target_y=s2.y,
                velocity_px_ms=v,
                lookahead_px=lookahead,
                funnel_radius_px=aperture,
                preview_cone_angle_deg=cone_angle,
                resonance_efficiency=res_eff,
            )
            segments.append(seg)

        mean_v = sum(velocities) / len(velocities) if velocities else 0.0
        peak_v = max(velocities) if velocities else 0.0
        mean_aperture = sum(apertures) / len(apertures) if apertures else self.base_aperture_px
        sync_rate = synchronous_segments / len(segments) if segments else 1.0

        if sync_rate >= 0.80 and overdrive_count <= 1:
            status = "SYNCHRONIZED"
        elif sync_rate >= 0.55:
            status = "CALIBRATED"
        else:
            status = "ASYNC_LAG"

        return GazeCorridorTelemetry(
            total_samples=len(samples),
            segments=segments,
            mean_scanpath_velocity=mean_v,
            peak_saccade_velocity=peak_v,
            mean_funnel_aperture_px=mean_aperture,
            parafoveal_synchrony_rate=sync_rate,
            overdrive_events_count=overdrive_count,
            status_level=status,
            samples=samples,
        )

    def generate_markdown_report(self, telemetry: GazeCorridorTelemetry) -> str:
        """Builds a structured diagnostic Markdown report analyzing gaze corridor resonance."""
        status_icons = {
            "SYNCHRONIZED": "🟢",
            "CALIBRATED": "🟡",
            "ASYNC_LAG": "🔴",
        }
        icon = status_icons.get(telemetry.status_level, "⚪")

        lines = [
            "# Gaze Corridor Resonator & Attentional Funnel Report",
            "",
            f"**Synchronization Status:** {icon} `{telemetry.status_level}`",
            "",
            "## Ocular Pacing & Parafoveal Resonance Telemetry",
            "",
            "| Telemetry Metric | Measured Value | Optimal Pacing Threshold | Clinical Significance |",
            "| :--- | :--- | :--- | :--- |",
            f"| **Total Gaze Samples** | `{telemetry.total_samples}` | >= 4 samples | Density of eye scanpath trajectory |",
            f"| **Mean Scanpath Velocity** | `{telemetry.mean_scanpath_velocity:.3f} px/ms` | 0.2 - 0.8 px/ms | Baseline reading movement pace |",
            f"| **Peak Saccade Velocity** | `{telemetry.peak_saccade_velocity:.3f} px/ms` | < 2.0 px/ms | Ballistic trans-modular leaps |",
            f"| **Mean Funnel Aperture** | `{telemetry.mean_funnel_aperture_px:.1f} px` | 40 - 75 px | Dynamic foveal corridor comfort width |",
            f"| **Parafoveal Synchrony Rate** | `{telemetry.parafoveal_synchrony_rate * 100:.1f}%` | >= 80.0% | Lookahead target pre-fetch matching |",
            f"| **Velocity Overdrive Events** | `{telemetry.overdrive_events_count}` | <= 1 event | Saccadic overshoots risking disorientation |",
            "",
            "## Resonant Corridor Segments",
            "",
        ]

        if not telemetry.segments:
            lines.append("_No multi-point trajectory segments available to calibrate._")
        else:
            lines.append("| Segment | Start -> Target | Velocity | Lookahead | Funnel Radius | Efficiency |")
            lines.append("| :--- | :--- | :--- | :--- | :--- | :--- |")
            for s in telemetry.segments:
                lines.append(
                    f"| `{s.segment_id}` | ({s.start_x:.0f}, {s.start_y:.0f}) -> ({s.target_x:.0f}, {s.target_y:.0f}) | `{s.velocity_px_ms:.2f} px/ms` | `{s.lookahead_px:.1f} px` | `{s.funnel_radius_px:.1f} px` | `{s.resonance_efficiency * 100:.1f}%` |"
                )
            lines.append("")

        lines.extend([
            "## Cognitive Architecture & Parafoveal Pre-Fetching Mechanics",
            "",
            "- **Keith Rayner Reading Paradigm:** The parafoveal window pre-processes downstream word lengths and visual anchors before fixation lands. Dynamic velocity funnels expand this preview zone proactively.",
            "- **Carpenter LATER Dynamics:** Eliminating landing latency via predictive lookahead prevents hesitation pauses and maintains rhythmic reading momentum.",
            "- **Visual Crowding Protection:** Narrowing focal aperture during slow fixations shields dyslexic working memory from extraneous peripheral interference.",
        ])

        return "\n".join(lines)

    def generate_svg(
        self,
        telemetry: GazeCorridorTelemetry,
        width: int = 880,
        height: int = 580,
    ) -> str:
        """Renders an interactive dark titanium SVG visualization of the resonant gaze corridor."""
        parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
            f'width="{width}" height="{height}" style="background-color: #0d1117; font-family: -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif;">',
            '<defs>',
            '  <pattern id="dotGrid" width="30" height="30" patternUnits="userSpaceOnUse">',
            '    <circle cx="2" cy="2" r="1" fill="#21262d" />',
            '  </pattern>',
            '  <linearGradient id="conduitGrad" x1="0%" y1="0%" x2="100%" y2="100%">',
            '    <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.22" />',
            '    <stop offset="100%" stop-color="#58a6ff" stop-opacity="0.08" />',
            '  </linearGradient>',
            '  <filter id="pGlow" x="-30%" y="-30%" width="160%" height="160%">',
            '    <feGaussianBlur stdDeviation="3" result="blur" />',
            '    <feComposite in="SourceGraphic" in2="blur" operator="over" />',
            '  </filter>',
            '</defs>',
            '<!-- Canvas Base -->',
            f'<rect width="{width}" height="{height}" fill="#0d1117" />',
            f'<rect width="{width}" height="{height}" fill="url(#dotGrid)" />',
        ]

        # Draw Adaptive Conduit Bands along segments
        for seg in telemetry.segments:
            # Thick conduit ribbon
            parts.append(
                f'<line x1="{seg.start_x}" y1="{seg.start_y}" x2="{seg.target_x}" y2="{seg.target_y}" '
                f'stroke="#58a6ff" stroke-width="{seg.funnel_radius_px * 1.8}" stroke-opacity="0.10" '
                f'stroke-linecap="round" />'
            )
            # Outer conduit border dashed
            parts.append(
                f'<line x1="{seg.start_x}" y1="{seg.start_y}" x2="{seg.target_x}" y2="{seg.target_y}" '
                f'stroke="#58a6ff" stroke-width="{seg.funnel_radius_px * 1.8}" stroke-opacity="0.28" '
                f'stroke-dasharray="6,6" stroke-linecap="round" />'
            )

            # Forward Parafoveal Lookahead Projection Cone
            dx = seg.target_x - seg.start_x
            dy = seg.target_y - seg.start_y
            seg_len = math.hypot(dx, dy)
            if seg_len > 1e-3:
                nx = dx / seg_len
                ny = dy / seg_len
                # Projected lookahead apex
                proj_x = seg.target_x + nx * seg.lookahead_px * 0.6
                proj_y = seg.target_y + ny * seg.lookahead_px * 0.6
                parts.append(
                    f'<line x1="{seg.target_x}" y1="{seg.target_y}" x2="{proj_x}" y2="{proj_y}" '
                    f'stroke="#38bdf8" stroke-width="2" stroke-dasharray="3,3" stroke-opacity="0.85" />'
                )
                parts.append(
                    f'<circle cx="{proj_x}" cy="{proj_y}" r="3.5" fill="#38bdf8" opacity="0.8" />'
                )

        # Draw Core Scanpath Trajectory Line
        if len(telemetry.samples) >= 2:
            pts_str = " ".join(f"{s.x},{s.y}" for s in telemetry.samples)
            parts.append(
                f'<polyline points="{pts_str}" fill="none" stroke="#3fb950" stroke-width="2.8" '
                f'stroke-linejoin="round" stroke-linecap="round" filter="url(#pGlow)" stroke-opacity="0.9" />'
            )

        # Draw Gaze Sample Nodes
        for idx, s in enumerate(telemetry.samples):
            # Velocity coloring: look at following segment velocity if available
            v_val = 0.0
            if idx < len(telemetry.segments):
                v_val = telemetry.segments[idx].velocity_px_ms
            elif telemetry.segments:
                v_val = telemetry.segments[-1].velocity_px_ms

            if v_val > 1.2:
                node_col = "#38bdf8"  # High velocity cyan
            elif v_val > 0.4:
                node_col = "#3fb950"  # Calibrated emerald
            else:
                node_col = "#d29922"  # Dwell fixation amber

            # Dwell circle
            dwell_r = min(14.0, max(5.0, math.sqrt(s.dwell_ms) * 0.75))
            parts.append(
                f'<circle cx="{s.x}" cy="{s.y}" r="{dwell_r}" fill="{node_col}" fill-opacity="0.25" '
                f'stroke="{node_col}" stroke-width="2" />'
            )
            parts.append(
                f'<circle cx="{s.x}" cy="{s.y}" r="2.5" fill="#ffffff" />'
            )
            # Label
            parts.append(
                f'<text x="{s.x + 10}" y="{s.y + 4}" fill="#f0f6fc" font-size="10" font-weight="600">{idx + 1}</text>'
            )

        # Header Titles
        parts.extend([
            '<!-- Header Block -->',
            '<text x="28" y="38" fill="#38bdf8" font-size="18" font-weight="700" letter-spacing="0.5">GAZE CORRIDOR RESONATOR & ATTENTIONAL FUNNEL</text>',
            '<text x="28" y="56" fill="#8b949e" font-size="11">Rayner Parafoveal Preview Synchronization & Dynamic Velocity Conduits</text>',
        ])

        # Status badge
        badge_cols = {
            "SYNCHRONIZED": ("#238636", "#3fb950"),
            "CALIBRATED": ("#9e6a03", "#d29922"),
            "ASYNC_LAG": ("#da3633", "#f85149"),
        }
        bg_col, fg_col = badge_cols.get(telemetry.status_level, ("#30363d", "#8b949e"))
        badge_x = width - 180
        parts.extend([
            f'<rect x="{badge_x}" y="22" width="152" height="34" rx="6" fill="{bg_col}" fill-opacity="0.3" stroke="{fg_col}" stroke-width="1.2" />',
            f'<circle cx="{badge_x + 18}" cy="39" r="5" fill="{fg_col}" />',
            f'<text x="{badge_x + 32}" y="43" fill="#f0f6fc" font-size="11" font-weight="700">{telemetry.status_level}</text>',
        ])

        # Telemetry HUD Card (Bottom Right)
        card_w = 320
        card_h = 138
        card_x = width - card_w - 24
        card_y = height - card_h - 24
        parts.extend([
            f'<g transform="translate({card_x}, {card_y})">',
            f'  <rect width="{card_w}" height="{card_h}" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1.5" />',
            '  <text x="16" y="24" fill="#f0f6fc" font-size="12" font-weight="700">Corridor Resonance Telemetry</text>',
            f'  <line x1="16" y1="32" x2="{card_w - 16}" y2="32" stroke="#30363d" stroke-width="1" />',
            f'  <text x="16" y="52" fill="#8b949e" font-size="11">Parafoveal Synchrony:</text>',
            f'  <text x="{card_w - 16}" y="52" fill="#3fb950" font-size="11" font-weight="600" text-anchor="end">{telemetry.parafoveal_synchrony_rate * 100:.1f}%</text>',
            f'  <text x="16" y="72" fill="#8b949e" font-size="11">Mean Gaze Velocity:</text>',
            f'  <text x="{card_w - 16}" y="72" fill="#38bdf8" font-size="11" font-weight="600" text-anchor="end">{telemetry.mean_scanpath_velocity:.3f} px/ms</text>',
            f'  <text x="16" y="92" fill="#8b949e" font-size="11">Peak Saccade Speed:</text>',
            f'  <text x="{card_w - 16}" y="92" fill="#bc8cff" font-size="11" font-weight="600" text-anchor="end">{telemetry.peak_saccade_velocity:.3f} px/ms</text>',
            f'  <text x="16" y="112" fill="#8b949e" font-size="11">Mean Conduit Aperture:</text>',
            f'  <text x="{card_w - 16}" y="112" fill="#c9d1d9" font-size="11" font-weight="600" text-anchor="end">{telemetry.mean_funnel_aperture_px:.1f} px</text>',
            f'  <text x="16" y="128" fill="#8b949e" font-size="11">Velocity Overdrive Events:</text>',
            f'  <text x="{card_w - 16}" y="128" fill="{"#f85149" if telemetry.overdrive_events_count > 0 else "#3fb950"}" font-size="11" font-weight="600" text-anchor="end">{telemetry.overdrive_events_count} events</text>',
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
            '  <text x="16" y="20" fill="#f0f6fc" font-size="11" font-weight="700">Gaze Corridor Legend</text>',
            '  <line x1="16" y1="36" x2="36" y2="36" stroke="#3fb950" stroke-width="2.5" />',
            '  <text x="44" y="39" fill="#8b949e" font-size="10">Scanpath Waypoint Track (Foveal Path)</text>',
            '  <rect x="16" y="50" width="20" height="10" fill="#58a6ff" fill-opacity="0.25" stroke="#58a6ff" stroke-width="1" stroke-dasharray="2,2" />',
            '  <text x="44" y="59" fill="#8b949e" font-size="10">Adaptive Conduit Aperture (Velocity Tuned)</text>',
            '  <line x1="16" y1="76" x2="36" y2="76" stroke="#38bdf8" stroke-width="2" stroke-dasharray="3,3" />',
            '  <circle cx="36" cy="76" r="3" fill="#38bdf8" />',
            '  <text x="44" y="79" fill="#8b949e" font-size="10">Parafoveal Lookahead Ray (Rayner Preview)</text>',
            '  <circle cx="26" cy="94" r="5" fill="#d29922" fill-opacity="0.3" stroke="#d29922" stroke-width="1.5" />',
            '  <text x="44" y="97" fill="#8b949e" font-size="10">Fixation Dwell Anchor (Ocular Station)</text>',
            '</g>',
        ])

        parts.append('</svg>')
        return "\n".join(parts)

    @classmethod
    def create_demo_telemetry(cls) -> GazeCorridorTelemetry:
        """Constructs a realistic technical scanpath across complex architecture."""
        samples = [
            GazeSample("gs-1", 100.0, 180.0, timestamp_ms=0.0, dwell_ms=180.0, modality="TEXT"),
            GazeSample("gs-2", 220.0, 185.0, timestamp_ms=210.0, dwell_ms=160.0, modality="TEXT"),
            GazeSample("gs-3", 380.0, 190.0, timestamp_ms=440.0, dwell_ms=140.0, modality="CODE"),
            GazeSample("gs-4", 560.0, 240.0, timestamp_ms=680.0, dwell_ms=190.0, modality="CODE"),
            GazeSample("gs-5", 680.0, 360.0, timestamp_ms=990.0, dwell_ms=220.0, modality="SCHEMATIC"),
            GazeSample("gs-6", 480.0, 420.0, timestamp_ms=1320.0, dwell_ms=150.0, modality="SCHEMATIC"),
            GazeSample("gs-7", 260.0, 430.0, timestamp_ms=1640.0, dwell_ms=170.0, modality="DIAGRAM"),
            GazeSample("gs-8", 120.0, 440.0, timestamp_ms=1890.0, dwell_ms=200.0, modality="DIAGRAM"),
        ]

        resonator = cls(saccadic_latency_ms=175.0, base_aperture_px=45.0, velocity_scale=60.0)
        return resonator.synchronize_corridor(samples)
