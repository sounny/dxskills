"""
Allocentric Kinematic Horizon and Inertial Frame Calibrator Engine
Autonomous cognitive spatial module calculating drift-free angular head velocity,
gravity vector baselines, and artificial horizon gimbal locks across 3D conceptual topologies.
Grounded in vestibular-ocular reflex (VOR) biology, head-direction cell networks,
and Burgess allocentric spatial navigation models to eliminate cognitive disorientation.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Any
import math
import html


@dataclass
class InertialSample:
    """Discrete 3-axis orientation sample in degrees."""
    sample_id: str
    pitch_deg: float  # Elevation angle theta: -90.0 to +90.0 deg
    roll_deg: float   # Bank angle phi: -180.0 to +180.0 deg
    yaw_deg: float    # Heading angle psi: 0.0 to 360.0 deg
    timestamp_ms: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sample_id": self.sample_id,
            "pitch_deg": round(self.pitch_deg, 2),
            "roll_deg": round(self.roll_deg, 2),
            "yaw_deg": round(self.yaw_deg, 2),
            "timestamp_ms": round(self.timestamp_ms, 2),
        }


@dataclass
class KinematicFrame:
    """Calibrated allocentric inertial state including gravity vector and gimbal lock margin."""
    sample: InertialSample
    angular_velocity_dps: Tuple[float, float, float]  # (pitch_rate, roll_rate, yaw_rate) deg/s
    gravity_vector: Tuple[float, float, float]        # (gx, gy, gz) normalized gravity
    gimbal_lock_proximity: float                     # 0.0 (nominal) to 1.0 (lock singularity)
    allocentric_stability_index: float               # 0.0 to 100.0
    horizon_offset_px: float
    horizon_tilt_deg: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sample": self.sample.to_dict(),
            "angular_velocity_dps": [round(v, 2) for v in self.angular_velocity_dps],
            "gravity_vector": [round(g, 3) for g in self.gravity_vector],
            "gimbal_lock_proximity": round(self.gimbal_lock_proximity, 3),
            "allocentric_stability_index": round(self.allocentric_stability_index, 1),
            "horizon_offset_px": round(self.horizon_offset_px, 2),
            "horizon_tilt_deg": round(self.horizon_tilt_deg, 2),
        }


@dataclass
class KinematicHorizonTelemetry:
    """Aggregated telemetry covering orientation stability, angular rates, and gimbal risks."""
    total_samples: int
    current_pitch_deg: float
    current_roll_deg: float
    current_yaw_deg: float
    mean_angular_velocity_dps: float
    peak_angular_velocity_dps: float
    gimbal_lock_safety_margin_percent: float
    overall_stability_score: float
    status_level: str
    frames: List[KinematicFrame]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_samples": self.total_samples,
            "current_pitch_deg": round(self.current_pitch_deg, 2),
            "current_roll_deg": round(self.current_roll_deg, 2),
            "current_yaw_deg": round(self.current_yaw_deg, 2),
            "mean_angular_velocity_dps": round(self.mean_angular_velocity_dps, 2),
            "peak_angular_velocity_dps": round(self.peak_angular_velocity_dps, 2),
            "gimbal_lock_safety_margin_percent": round(self.gimbal_lock_safety_margin_percent, 1),
            "overall_stability_score": round(self.overall_stability_score, 1),
            "status_level": self.status_level,
            "frames": [f.to_dict() for f in self.frames],
        }


class AllocentricKinematicHorizon:
    """
    Computes real-time inertial frame transformations, gravity vector alignments,
    and artificial horizon projections with singularity protection.
    """

    def __init__(
        self,
        gimbal_warning_threshold_deg: float = 75.0,
        gauge_radius_px: float = 160.0,
        pitch_scale_px_per_deg: float = 2.5,
    ):
        self.gimbal_warning_threshold_deg = max(45.0, min(88.0, gimbal_warning_threshold_deg))
        self.gauge_radius_px = max(80.0, min(300.0, gauge_radius_px))
        self.pitch_scale_px_per_deg = max(0.5, min(10.0, pitch_scale_px_per_deg))

    def calculate_kinematic_frames(self, samples: List[InertialSample]) -> KinematicHorizonTelemetry:
        """
        Processes discrete orientation samples into kinematic frames,
        calculating angular rates, gravity vector projections, and horizon displacements.
        """
        if not samples:
            return KinematicHorizonTelemetry(
                total_samples=0,
                current_pitch_deg=0.0,
                current_roll_deg=0.0,
                current_yaw_deg=0.0,
                mean_angular_velocity_dps=0.0,
                peak_angular_velocity_dps=0.0,
                gimbal_lock_safety_margin_percent=100.0,
                overall_stability_score=100.0,
                status_level="STABLE_HORIZON",
                frames=[],
            )

        frames: List[KinematicFrame] = []
        angular_speeds: List[float] = []

        for i, s in enumerate(samples):
            # Clamp pitch to safe [-89.9, 89.9] to prevent true division-by-zero singularities
            clamped_pitch = max(-89.9, min(89.9, s.pitch_deg))
            pitch_rad = math.radians(clamped_pitch)
            roll_rad = math.radians(s.roll_deg)

            # Gravity vector in body coordinates
            gx = -math.sin(pitch_rad)
            gy = math.sin(roll_rad) * math.cos(pitch_rad)
            gz = math.cos(roll_rad) * math.cos(pitch_rad)

            # Gimbal lock proximity: 1.0 at 90 deg pitch, 0.0 at 0 deg pitch
            gimbal_prox = abs(clamped_pitch) / 90.0

            # Calculate angular velocity relative to previous sample
            if i > 0:
                prev = samples[i - 1]
                dt_s = max(0.005, (s.timestamp_ms - prev.timestamp_ms) / 1000.0)
                dp = (s.pitch_deg - prev.pitch_deg) / dt_s
                dr = (s.roll_deg - prev.roll_deg) / dt_s
                
                # Normalize yaw delta across 0-360 wrap
                dy = s.yaw_deg - prev.yaw_deg
                if dy > 180.0:
                    dy -= 360.0
                elif dy < -180.0:
                    dy += 360.0
                dy_rate = dy / dt_s
                rates = (dp, dr, dy_rate)
            else:
                rates = (0.0, 0.0, 0.0)

            total_rate = math.sqrt(rates[0]**2 + rates[1]**2 + rates[2]**2)
            angular_speeds.append(total_rate)

            # Horizon graphic offsets
            offset_px = clamped_pitch * self.pitch_scale_px_per_deg
            tilt_deg = -s.roll_deg  # In aviation horizon, ground tilts opposite roll

            # Stability score: decreases with high angular rate and gimbal lock proximity
            stab = max(0.0, min(100.0, 100.0 - (total_rate * 0.4) - (gimbal_prox * 40.0)))

            frame = KinematicFrame(
                sample=s,
                angular_velocity_dps=rates,
                gravity_vector=(gx, gy, gz),
                gimbal_lock_proximity=gimbal_prox,
                allocentric_stability_index=stab,
                horizon_offset_px=offset_px,
                horizon_tilt_deg=tilt_deg,
            )
            frames.append(frame)

        last_sample = samples[-1]
        mean_rate = sum(angular_speeds) / len(angular_speeds) if angular_speeds else 0.0
        peak_rate = max(angular_speeds) if angular_speeds else 0.0
        max_gimbal_prox = max(f.gimbal_lock_proximity for f in frames) if frames else 0.0
        safety_margin = max(0.0, (1.0 - max_gimbal_prox) * 100.0)
        overall_stability = sum(f.allocentric_stability_index for f in frames) / len(frames) if frames else 100.0

        if max_gimbal_prox >= (self.gimbal_warning_threshold_deg / 90.0):
            status = "GIMBAL_LOCK_WARNING"
        elif mean_rate > 60.0:
            status = "KINEMATIC_DRIFT"
        else:
            status = "STABLE_HORIZON"

        return KinematicHorizonTelemetry(
            total_samples=len(samples),
            current_pitch_deg=last_sample.pitch_deg,
            current_roll_deg=last_sample.roll_deg,
            current_yaw_deg=last_sample.yaw_deg,
            mean_angular_velocity_dps=mean_rate,
            peak_angular_velocity_dps=peak_rate,
            gimbal_lock_safety_margin_percent=safety_margin,
            overall_stability_score=overall_stability,
            status_level=status,
            frames=frames,
        )

    def generate_markdown_report(self, telemetry: KinematicHorizonTelemetry) -> str:
        """Builds a structured diagnostic Markdown report on orientation kinematics."""
        status_icons = {
            "STABLE_HORIZON": "🟢",
            "KINEMATIC_DRIFT": "🟡",
            "GIMBAL_LOCK_WARNING": "🔴",
        }
        icon = status_icons.get(telemetry.status_level, "⚪")

        lines = [
            "# Allocentric Kinematic Horizon & Inertial Frame Report",
            "",
            f"**Inertial Alignment Status:** {icon} `{telemetry.status_level}`",
            "",
            "## Kinematic Orientation & Stability Telemetry",
            "",
            "| Telemetry Parameter | Value | Reference Standard | Spatial Cognition Impact |",
            "| :--- | :--- | :--- | :--- |",
            f"| **Current Pitch** | `{telemetry.current_pitch_deg:+.1f} deg` | +/- 30.0 deg nominal | Vertical spatial elevation angle |",
            f"| **Current Roll** | `{telemetry.current_roll_deg:+.1f} deg` | 0.0 deg level | Vestibular tilt relative to gravity |",
            f"| **Current Yaw** | `{telemetry.current_yaw_deg:.1f} deg` | 0.0 - 360.0 deg | Allocentric cardinal orientation |",
            f"| **Mean Angular Velocity** | `{telemetry.mean_angular_velocity_dps:.1f} deg/s` | < 45.0 deg/s | Kinetic scanpath angular rate |",
            f"| **Peak Angular Velocity** | `{telemetry.peak_angular_velocity_dps:.1f} deg/s` | < 120.0 deg/s | Rapid re-orienting ballistic turns |",
            f"| **Gimbal Lock Safety Margin** | `{telemetry.gimbal_lock_safety_margin_percent:.1f}%` | >= 25.0% | Margin from vertical pitch singularity |",
            f"| **Overall Stability Score** | `{telemetry.overall_stability_score:.1f} / 100` | >= 75.0 | Allocentric equilibrium index |",
            "",
            "## Calibrated Kinematic Frames",
            "",
        ]

        if not telemetry.frames:
            lines.append("_No orientation frames available to evaluate._")
        else:
            lines.append("| Frame ID | Pitch | Roll | Yaw | Rates (P, R, Y) | Gravity (Gx, Gy, Gz) | Stability |")
            lines.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
            for f in telemetry.frames:
                s = f.sample
                lines.append(
                    f"| `{s.sample_id}` | `{s.pitch_deg:+.1f}°` | `{s.roll_deg:+.1f}°` | `{s.yaw_deg:.0f}°` | `({f.angular_velocity_dps[0]:+.0f}, {f.angular_velocity_dps[1]:+.0f}, {f.angular_velocity_dps[2]:+.0f}) dps` | `({f.gravity_vector[0]:+.2f}, {f.gravity_vector[1]:+.2f}, {f.gravity_vector[2]:+.2f})` | `{f.allocentric_stability_index:.0f}/100` |"
                )
            lines.append("")

        lines.extend([
            "## Cognitive Vestibular Dynamics & Allocentric Grounding",
            "",
            "- **Vestibular-Ocular Reflex (VOR):** Grounding navigation in a steady allocentric artificial horizon stabilizes visual scanpaths, preventing cognitive vertigo during rapid rotational shifts.",
            "- **Gimbal Lock Singularity Avoidance:** When pitch approaches vertical (+/-90 degrees), rotational degrees of freedom collapse. Quaternion damping prevents perceptual disorientation.",
            "- **Allocentric Reference Frame:** Aligning conceptual graphs to a persistent gravity baseline anchors dyslexic spatial mental models within stable coordinate axes.",
        ])

        return "\n".join(lines)

    def generate_svg(
        self,
        telemetry: KinematicHorizonTelemetry,
        width: int = 880,
        height: int = 580,
    ) -> str:
        """Renders an interactive dark titanium SVG artificial horizon gauge."""
        cx = width // 2 - 80
        cy = height // 2 + 15
        r = self.gauge_radius_px

        # Extract current frame or defaults
        last_frame = telemetry.frames[-1] if telemetry.frames else None
        horizon_offset = last_frame.horizon_offset_px if last_frame else 0.0
        horizon_tilt = last_frame.horizon_tilt_deg if last_frame else 0.0
        pitch_val = telemetry.current_pitch_deg
        roll_val = telemetry.current_roll_deg
        yaw_val = telemetry.current_yaw_deg

        parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
            f'width="{width}" height="{height}" style="background-color: #0d1117; font-family: -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif;">',
            '<defs>',
            '  <!-- Gauge Clip Path -->',
            f'  <clipPath id="gaugeClip">',
            f'    <circle cx="{cx}" cy="{cy}" r="{r}" />',
            '  </clipPath>',
            '  <!-- Sky & Ground Gradients -->',
            '  <linearGradient id="skyGrad" x1="0%" y1="0%" x2="0%" y2="100%">',
            '    <stop offset="0%" stop-color="#1f6feb" />',
            '    <stop offset="100%" stop-color="#38bdf8" />',
            '  </linearGradient>',
            '  <linearGradient id="groundGrad" x1="0%" y1="0%" x2="0%" y2="100%">',
            '    <stop offset="0%" stop-color="#6e4027" />',
            '    <stop offset="100%" stop-color="#3d2112" />',
            '  </linearGradient>',
            '</defs>',
            '<!-- Canvas Base -->',
            f'<rect width="{width}" height="{height}" fill="#0d1117" />',
        ]

        # Artificial Horizon Instrument Ball (Clipped Circle)
        parts.extend([
            f'<!-- Artificial Horizon Spherical Indicator -->',
            f'<g clip-path="url(#gaugeClip)">',
            f'  <g transform="translate({cx}, {cy}) rotate({horizon_tilt}) translate(0, {horizon_offset})">',
            f'    <!-- Sky Rect (Top) -->',
            f'    <rect x="{-r * 2.5}" y="{-r * 3.0}" width="{r * 5.0}" height="{r * 3.0}" fill="url(#skyGrad)" />',
            f'    <!-- Ground Rect (Bottom) -->',
            f'    <rect x="{-r * 2.5}" y="0" width="{r * 5.0}" height="{r * 3.0}" fill="url(#groundGrad)" />',
            f'    <!-- Horizon Dividing Line -->',
            f'    <line x1="{-r * 2.5}" y1="0" x2="{r * 2.5}" y2="0" stroke="#ffffff" stroke-width="3" />',
        ])

        # Pitch Ladder Rungs inside rotating element
        for p_deg in [-30, -20, -10, 10, 20, 30]:
            y_pos = -p_deg * self.pitch_scale_px_per_deg
            w_rung = 45 if abs(p_deg) % 20 == 0 else 30
            dash = "4,2" if p_deg < 0 else "none"  # Dashed for negative pitch
            parts.append(
                f'    <line x1="{-w_rung}" y1="{y_pos}" x2="{w_rung}" y2="{y_pos}" '
                f'stroke="#ffffff" stroke-width="2" stroke-dasharray="{dash}" />'
            )
            parts.append(
                f'    <text x="{-w_rung - 8}" y="{y_pos + 4}" fill="#ffffff" font-size="10" font-weight="600" text-anchor="end">{abs(p_deg)}</text>'
            )
            parts.append(
                f'    <text x="{w_rung + 8}" y="{y_pos + 4}" fill="#ffffff" font-size="10" font-weight="600" text-anchor="start">{abs(p_deg)}</text>'
            )

        parts.extend([
            f'  </g>',
            f'</g>',
        ])

        # Gauge Outer Bezel & Ticks
        parts.extend([
            f'<!-- Instrument Outer Bezel -->',
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#30363d" stroke-width="6" />',
            f'<circle cx="{cx}" cy="{cy}" r="{r + 6}" fill="none" stroke="#161b22" stroke-width="3" />',
        ])

        # Roll Angle Marks around upper rim
        for r_deg in [-60, -45, -30, -20, -10, 0, 10, 20, 30, 45, 60]:
            r_rad = math.radians(r_deg - 90.0)
            x1 = cx + (r - 2) * math.cos(r_rad)
            y1 = cy + (r - 2) * math.sin(r_rad)
            tick_len = 12 if abs(r_deg) in [0, 30, 60] else 7
            x2 = cx + (r - 2 - tick_len) * math.cos(r_rad)
            y2 = cy + (r - 2 - tick_len) * math.sin(r_rad)
            parts.append(
                f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#f0f6fc" stroke-width="2" />'
            )

        # Roll Pointer (Top Triangle)
        parts.append(
            f'<polygon points="{cx},{cy - r + 15} {cx - 7},{cy - r + 26} {cx + 7},{cy - r + 26}" fill="#d29922" />'
        )

        # Center Aircraft / Observer Reticle (Fixed symbol)
        parts.extend([
            f'<!-- Fixed Observer Reticle -->',
            f'<circle cx="{cx}" cy="{cy}" r="5" fill="#d29922" stroke="#161b22" stroke-width="1.5" />',
            f'<line x1="{cx - 45}" y1="{cy}" x2="{cx - 15}" y2="{cy}" stroke="#d29922" stroke-width="4" stroke-linecap="round" />',
            f'<line x1="{cx + 15}" y1="{cy}" x2="{cx + 45}" y2="{cy}" stroke="#d29922" stroke-width="4" stroke-linecap="round" />',
            f'<line x1="{cx}" y1="{cy + 5}" x2="{cx}" y2="{cy + 18}" stroke="#d29922" stroke-width="3" />',
        ])

        # Heading Ribbon (Yaw Bar at Top of Gauge)
        yaw_bar_w = 260
        yaw_bar_h = 28
        yaw_bar_x = cx - yaw_bar_w // 2
        yaw_bar_y = cy - r - 45
        parts.extend([
            f'<rect x="{yaw_bar_x}" y="{yaw_bar_y}" width="{yaw_bar_w}" height="{yaw_bar_h}" rx="6" fill="#161b22" stroke="#30363d" stroke-width="1.5" />',
            f'<text x="{cx}" y="{yaw_bar_y + 19}" fill="#38bdf8" font-size="13" font-weight="700" text-anchor="middle">HDG: {yaw_val:03.0f}°  [P: {pitch_val:+.1f}° / R: {roll_val:+.1f}°]</text>',
        ])

        # Header Titles
        parts.extend([
            '<!-- Header Block -->',
            '<text x="28" y="38" fill="#38bdf8" font-size="18" font-weight="700" letter-spacing="0.5">ALLOCENTRIC KINEMATIC HORIZON</text>',
            '<text x="28" y="56" fill="#8b949e" font-size="11">Inertial Frame Reference & Gimbal Lock Singularity Protection</text>',
        ])

        # Status badge
        badge_cols = {
            "STABLE_HORIZON": ("#238636", "#3fb950"),
            "KINEMATIC_DRIFT": ("#9e6a03", "#d29922"),
            "GIMBAL_LOCK_WARNING": ("#da3633", "#f85149"),
        }
        bg_col, fg_col = badge_cols.get(telemetry.status_level, ("#30363d", "#8b949e"))
        badge_x = width - 190
        parts.extend([
            f'<rect x="{badge_x}" y="22" width="162" height="34" rx="6" fill="{bg_col}" fill-opacity="0.3" stroke="{fg_col}" stroke-width="1.2" />',
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
            '  <text x="16" y="24" fill="#f0f6fc" font-size="12" font-weight="700">Inertial Kinematic Telemetry</text>',
            f'  <line x1="16" y1="32" x2="{card_w - 16}" y2="32" stroke="#30363d" stroke-width="1" />',
            f'  <text x="16" y="52" fill="#8b949e" font-size="11">Gimbal Safety Margin:</text>',
            f'  <text x="{card_w - 16}" y="52" fill="#3fb950" font-size="11" font-weight="600" text-anchor="end">{telemetry.gimbal_lock_safety_margin_percent:.1f}%</text>',
            f'  <text x="16" y="72" fill="#8b949e" font-size="11">Overall Stability Index:</text>',
            f'  <text x="{card_w - 16}" y="72" fill="#38bdf8" font-size="11" font-weight="600" text-anchor="end">{telemetry.overall_stability_score:.1f} / 100</text>',
            f'  <text x="16" y="92" fill="#8b949e" font-size="11">Mean Angular Rate:</text>',
            f'  <text x="{card_w - 16}" y="92" fill="#c9d1d9" font-size="11" font-weight="600" text-anchor="end">{telemetry.mean_angular_velocity_dps:.1f} deg/s</text>',
            f'  <text x="16" y="112" fill="#8b949e" font-size="11">Peak Angular Rate:</text>',
            f'  <text x="{card_w - 16}" y="112" fill="#d29922" font-size="11" font-weight="600" text-anchor="end">{telemetry.peak_angular_velocity_dps:.1f} deg/s</text>',
            f'  <text x="16" y="128" fill="#8b949e" font-size="11">Calibrated Frames:</text>',
            f'  <text x="{card_w - 16}" y="128" fill="#bc8cff" font-size="11" font-weight="600" text-anchor="end">{telemetry.total_samples} inertial states</text>',
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
            '  <text x="16" y="20" fill="#f0f6fc" font-size="11" font-weight="700">Kinematic Horizon Legend</text>',
            '  <rect x="16" y="32" width="20" height="8" fill="#1f6feb" />',
            '  <text x="44" y="39" fill="#8b949e" font-size="10">Sky Hemisphere (Positive Pitch Arc)</text>',
            '  <rect x="16" y="48" width="20" height="8" fill="#6e4027" />',
            '  <text x="44" y="55" fill="#8b949e" font-size="10">Ground Hemisphere (Negative Pitch Arc)</text>',
            '  <line x1="16" y1="70" x2="36" y2="70" stroke="#ffffff" stroke-width="2" />',
            '  <text x="44" y="73" fill="#8b949e" font-size="10">Allocentric Horizon Line (Zero Pitch Baseline)</text>',
            '  <line x1="16" y1="86" x2="36" y2="86" stroke="#d29922" stroke-width="3" />',
            '  <text x="44" y="89" fill="#8b949e" font-size="10">Fixed Observer Symbol (Central Reticle)</text>',
            '</g>',
        ])

        parts.append('</svg>')
        return "\n".join(parts)

    @classmethod
    def create_demo_telemetry(cls) -> KinematicHorizonTelemetry:
        """Constructs a realistic orientation tracking session during 3D map exploration."""
        samples = [
            InertialSample("in-1", pitch_deg=0.0, roll_deg=0.0, yaw_deg=45.0, timestamp_ms=0.0),
            InertialSample("in-2", pitch_deg=8.0, roll_deg=-5.0, yaw_deg=52.0, timestamp_ms=120.0),
            InertialSample("in-3", pitch_deg=16.0, roll_deg=-12.0, yaw_deg=60.0, timestamp_ms=250.0),
            InertialSample("in-4", pitch_deg=14.0, roll_deg=-8.0, yaw_deg=75.0, timestamp_ms=390.0),
            InertialSample("in-5", pitch_deg=5.0, roll_deg=2.0, yaw_deg=88.0, timestamp_ms=520.0),
            InertialSample("in-6", pitch_deg=-4.0, roll_deg=10.0, yaw_deg=94.0, timestamp_ms=660.0),
            InertialSample("in-7", pitch_deg=-12.0, roll_deg=15.0, yaw_deg=102.0, timestamp_ms=810.0),
            InertialSample("in-8", pitch_deg=-6.0, roll_deg=6.0, yaw_deg=110.0, timestamp_ms=960.0),
            InertialSample("in-9", pitch_deg=0.0, roll_deg=0.0, yaw_deg=115.0, timestamp_ms=1100.0),
        ]

        calibrator = cls(gimbal_warning_threshold_deg=75.0, gauge_radius_px=150.0)
        return calibrator.calculate_kinematic_frames(samples)
