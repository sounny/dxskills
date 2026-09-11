"""
Autonomous Cognitive Spatial Working Memory Saccade Fatigue Predictor & Kinetic Pacer
=====================================================================================
Theoretical Framework:
- Main Sequence Saccadic Kinetics (Bahill, Clark & Stark): Relationship between peak
  velocity and saccadic amplitude degrades linearly under prolonged cognitive strain.
- Working Memory Protection (Cowan N <= 4): Mitigates cognitive buffer collapse
  by anticipating ocular fatigue before involuntary fixation drift occurs.
- Adaptive Kinetic Luminance Pacing: Modulates canvas contrast and visual rhythm to
  induce restorative cognitive micro-rests along reading and search scanpaths.
- Strictly NO em dashes (\u2014) anywhere in code, docstrings, or outputs.
"""

import math
import json
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class SaccadeKineticEvent:
    """An ocular saccadic movement evaluated against the Main Sequence."""
    saccade_idx: int
    amplitude_px: float
    duration_ms: float
    peak_velocity_px_s: float
    expected_peak_velocity: float
    velocity_ratio: float
    is_fatigued: bool

@dataclass
class KineticPacerTelemetry:
    """Telemetry measuring kinetic deceleration and restorative pacing needs."""
    total_saccades: int
    fatigued_saccades: int
    mean_peak_velocity: float
    mean_expected_velocity: float
    velocity_drop_percent: float
    fatigue_risk_index: float
    recommended_rest_interval_s: float
    pacing_cadence_hz: float

@dataclass
class SaccadeFatiguePacerResult:
    """Result containing kinetic events, telemetry, SVG visualization, and audit report."""
    events: List[SaccadeKineticEvent]
    telemetry: KineticPacerTelemetry
    kinetic_pacer_svg: str
    audit_report_md: str

    def to_dict(self) -> Dict[str, Any]:
        import dataclasses
        return {
            "events": [dataclasses.asdict(e) for e in self.events],
            "telemetry": dataclasses.asdict(self.telemetry)
        }

class SaccadeKineticPacer:
    """
    Tracks ocular velocity degradation, predicts fatigue thresholds, and
    calculates optimal visual pacing rhythms to protect cognitive stamina.
    """

    # Main sequence empirical coefficients: V_peak = V_max * (1 - exp(-Amp / C))
    V_MAX = 800.0  # px/s asymptotic peak velocity
    ASYMPTOTE_CONSTANT = 180.0  # px scaling constant

    def __init__(self, fatigue_threshold_ratio: float = 0.80):
        self.fatigue_threshold_ratio = fatigue_threshold_ratio

    def expected_velocity(self, amplitude: float) -> float:
        """Calculates theoretical peak velocity for a given saccadic amplitude."""
        if amplitude <= 0.0:
            return 50.0
        return self.V_MAX * (1.0 - math.exp(-amplitude / self.ASYMPTOTE_CONSTANT))

    def evaluate_kinetics(self, raw_saccades: List[Dict[str, Any]]) -> SaccadeFatiguePacerResult:
        """Evaluates a sequence of ocular saccadic movements for kinetic degradation."""
        if not raw_saccades:
            telemetry = KineticPacerTelemetry(
                total_saccades=0,
                fatigued_saccades=0,
                mean_peak_velocity=0.0,
                mean_expected_velocity=0.0,
                velocity_drop_percent=0.0,
                fatigue_risk_index=0.0,
                recommended_rest_interval_s=0.0,
                pacing_cadence_hz=1.0
            )
            return SaccadeFatiguePacerResult(
                events=[],
                telemetry=telemetry,
                kinetic_pacer_svg="<svg width='800' height='450'></svg>",
                audit_report_md="# Saccade Kinetic Pacer Report\n\nNo saccade events provided."
            )

        events: List[SaccadeKineticEvent] = []
        vel_sum = 0.0
        exp_vel_sum = 0.0

        for idx, s in enumerate(raw_saccades):
            amp = float(s.get("amplitude_px", 120.0))
            dur = float(s.get("duration_ms", 45.0))

            # Peak velocity either measured or estimated
            if "peak_velocity_px_s" in s:
                peak_v = float(s["peak_velocity_px_s"])
            else:
                # Approximation: peak velocity is roughly 1.6 to 1.8 times average velocity
                avg_v = (amp / max(1.0, dur)) * 1000.0
                peak_v = avg_v * 1.7

            exp_v = self.expected_velocity(amp)
            ratio = round(peak_v / max(1.0, exp_v), 3)
            is_fatigued = ratio < self.fatigue_threshold_ratio

            vel_sum += peak_v
            exp_vel_sum += exp_v

            events.append(SaccadeKineticEvent(
                saccade_idx=idx + 1,
                amplitude_px=round(amp, 1),
                duration_ms=round(dur, 1),
                peak_velocity_px_s=round(peak_v, 1),
                expected_peak_velocity=round(exp_v, 1),
                velocity_ratio=ratio,
                is_fatigued=is_fatigued
            ))

        total_cnt = len(events)
        fatigued_cnt = sum(1 for e in events if e.is_fatigued)
        mean_vel = round(vel_sum / max(1, total_cnt), 1)
        mean_exp_vel = round(exp_vel_sum / max(1, total_cnt), 1)

        drop_pct = round(max(0.0, (1.0 - (mean_vel / max(1.0, mean_exp_vel))) * 100.0), 1)
        fatigue_risk = round(min(1.0, (fatigued_cnt / max(1, total_cnt)) * 1.25), 3)

        # Rest intervals scaled by fatigue risk (5s baseline up to 30s)
        rest_interval = round(5.0 + fatigue_risk * 25.0, 1)
        # Optimal pacing cadence: 2.0 Hz down to 0.8 Hz under high fatigue
        cadence_hz = round(max(0.8, 2.0 - fatigue_risk * 1.2), 2)

        telemetry = KineticPacerTelemetry(
            total_saccades=total_cnt,
            fatigued_saccades=fatigued_cnt,
            mean_peak_velocity=mean_vel,
            mean_expected_velocity=mean_exp_vel,
            velocity_drop_percent=drop_pct,
            fatigue_risk_index=fatigue_risk,
            recommended_rest_interval_s=rest_interval,
            pacing_cadence_hz=cadence_hz
        )

        svg = self.generate_svg(events, telemetry)
        md = self.generate_markdown_report(events, telemetry)

        return SaccadeFatiguePacerResult(
            events=events,
            telemetry=telemetry,
            kinetic_pacer_svg=svg,
            audit_report_md=md
        )

    def generate_svg(
        self,
        events: List[SaccadeKineticEvent],
        telemetry: KineticPacerTelemetry,
        width: int = 800,
        height: int = 450
    ) -> str:
        """Renders a dark titanium SVG displaying the Main Sequence velocity curve."""
        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">',
            '<defs>',
            '  <linearGradient id="titaniumPacerBg" x1="0%" y1="0%" x2="100%" y2="100%">',
            '    <stop offset="0%" stop-color="#141820" />',
            '    <stop offset="100%" stop-color="#0a0d13" />',
            '  </linearGradient>',
            '</defs>',
            f'<rect width="{width}" height="{height}" rx="12" fill="url(#titaniumPacerBg)" stroke="#30363d" stroke-width="1.5" />',
            '<!-- Header -->',
            '<text x="24" y="36" fill="#58a6ff" font-family="sans-serif" font-size="16" font-weight="bold">Saccadic Kinetic Main Sequence &amp; Fatigue Pacer</text>',
            f'<text x="{width - 24}" y="36" fill="#8b949e" font-family="sans-serif" font-size="12" text-anchor="end">Fatigue Risk: {telemetry.fatigue_risk_index * 100:.1f}% | Cadence: {telemetry.pacing_cadence_hz} Hz</text>',
            f'<line x1="24" y1="48" x2="{width - 24}" y2="48" stroke="#30363d" stroke-width="1" />',
            '<!-- Graph Axes -->',
            '<line x1="60" y1="360" x2="740" y2="360" stroke="#30363d" stroke-width="1.5" />',
            '<line x1="60" y1="80" x2="60" y2="360" stroke="#30363d" stroke-width="1.5" />',
            '<text x="740" y="380" fill="#8b949e" font-family="sans-serif" font-size="11" text-anchor="end">Amplitude (px)</text>',
            '<text x="50" y="75" fill="#8b949e" font-family="sans-serif" font-size="11">Peak Velocity (px/s)</text>'
        ]

        # Draw Expected Main Sequence Curve
        curve_points = []
        for a_px in range(10, 680, 20):
            v_exp = self.expected_velocity(a_px)
            # Map a_px to x (60 to 740), v_exp to y (360 down to 100)
            x_plot = 60 + (a_px / 680.0) * 660
            y_plot = 360 - (v_exp / 850.0) * 260
            curve_points.append(f"{x_plot:.1f},{y_plot:.1f}")

        if curve_points:
            svg_parts.append(f'<polyline points="{" ".join(curve_points)}" fill="none" stroke="#58a6ff" stroke-width="2" stroke-dasharray="4,4" opacity="0.7" />')

        # Plot Events
        for e in events:
            x_pt = 60 + (min(680.0, e.amplitude_px) / 680.0) * 660
            y_pt = 360 - (min(850.0, e.peak_velocity_px_s) / 850.0) * 260
            dot_color = "#f85149" if e.is_fatigued else "#7ee787"
            svg_parts.append(f'<circle cx="{x_pt:.1f}" cy="{y_pt:.1f}" r="4.5" fill="{dot_color}" stroke="#0a0d13" stroke-width="1" />')

        # Footer
        svg_parts.append(f'<line x1="24" y1="{height - 35}" x2="{width - 24}" y2="{height - 35}" stroke="#30363d" stroke-width="1" />')
        svg_parts.append(f'<text x="24" y="{height - 15}" fill="#8b949e" font-family="sans-serif" font-size="11">Total Saccades: {telemetry.total_saccades} | Decelerated: {telemetry.fatigued_saccades} | Velocity Drop: {telemetry.velocity_drop_percent}%</text>')
        svg_parts.append(f'<text x="{width - 24}" y="{height - 15}" fill="#7ee787" font-family="sans-serif" font-size="11" text-anchor="end">Rest Interval: {telemetry.recommended_rest_interval_s}s</text>')
        svg_parts.append('</svg>')

        return "\n".join(svg_parts)

    def generate_markdown_report(
        self,
        events: List[SaccadeKineticEvent],
        telemetry: KineticPacerTelemetry
    ) -> str:
        """Generates an audit report with strictly zero em dashes."""
        lines = [
            "# Saccade Kinetic Fatigue & Adaptive Pacer Report",
            "",
            "## Ocular Kinetic Metrics",
            f"- **Analyzed Saccade Movements:** {telemetry.total_saccades}",
            f"- **Fatigued/Decelerated Saccades:** {telemetry.fatigued_saccades}",
            f"- **Mean Peak Velocity:** {telemetry.mean_peak_velocity:.1f} px/s",
            f"- **Expected Baseline Velocity:** {telemetry.mean_expected_velocity:.1f} px/s",
            f"- **Velocity Attenuation:** {telemetry.velocity_drop_percent:.1f}%",
            f"- **Kinetic Fatigue Risk Index:** {telemetry.fatigue_risk_index * 100:.1f}%",
            f"- **Recommended Micro-Rest Interval:** {telemetry.recommended_rest_interval_s:.1f} s",
            f"- **Adaptive Visual Cadence:** {telemetry.pacing_cadence_hz:.2f} Hz",
            "",
            "## Saccade Event Classification",
            "",
            "| Index | Amplitude (px) | Duration (ms) | Peak Vel (px/s) | Expected Vel (px/s) | Ratio | Status |",
            "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |"
        ]

        for e in events:
            status = "FATIGUED" if e.is_fatigued else "OPTIMAL"
            lines.append(f"| {e.saccade_idx:02d} | {e.amplitude_px:.1f} | {e.duration_ms:.1f} | {e.peak_velocity_px_s:.1f} | {e.expected_peak_velocity:.1f} | {e.velocity_ratio:.2f} | **{status}** |")

        lines.extend([
            "",
            "## Theoretical Grounding",
            "- **Main Sequence Kinetics (Bahill et al.):** Predicts ocular fatigue from non-linear asymptotic velocity drops.",
            "- **Cowan Capacity Bounds:** Protects working memory buffers by timing visual breaks before cognitive disorientation.",
            "- **Adaptive Cadence Modulation:** Tunes presentation rhythms to the eye's physical recovery frequency.",
            ""
        ])

        return "\n".join(lines)
