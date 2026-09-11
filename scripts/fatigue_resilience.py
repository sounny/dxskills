"""
Spatial Dynamic Micro-Break and Fatigue Resiliency Harness for DxSkills.

Grounded in:
- Eide and Eide M-I-N-D spatial framework (ocular comfort and dynamic fatigue modulation)
- Sweller Cognitive Load Theory (preventing working memory buffer exhaustion)
- Baddeley Working Memory Model (executive control restoration and saccadic stabilization)
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional


@dataclass
class SaccadeSample:
    """Individual ocular tracking and cognitive fixation sample."""
    timestamp: float
    fixation_duration_ms: float
    jump_amplitude_deg: float
    is_regression: bool
    focal_depth: int = 1

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class FatigueTelemetry:
    """Quantitative evaluation of cognitive fatigue and ocular saturation."""
    session_duration_min: float
    total_fixations: int
    regression_rate: float
    mean_fixation_ms: float
    fatigue_score: float
    saturation_level: str
    recommended_break_type: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class BreakProtocol:
    """Structured neuro-ergonomic recovery protocol."""
    name: str
    duration_sec: int
    protocol_type: str
    guidance_steps: List[str]
    breathing_pattern: Optional[Dict[str, int]] = None
    spatial_focal_targets: Optional[List[Dict[str, Any]]] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class FatigueResilienceHarness:
    """
    Evaluates ocular fixation telemetry, calculates cognitive exhaustion thresholds,
    and synthesizes spatial micro-break protocols.
    """

    def __init__(self) -> None:
        pass

    def analyze_saccade_stream(
        self,
        samples: List[SaccadeSample],
        session_duration_min: float = 25.0,
    ) -> FatigueTelemetry:
        """
        Analyze a series of saccadic samples and session duration to assess fatigue.
        """
        if not samples:
            return FatigueTelemetry(
                session_duration_min=session_duration_min,
                total_fixations=0,
                regression_rate=0.0,
                mean_fixation_ms=200.0,
                fatigue_score=min(100.0, session_duration_min * 1.5),
                saturation_level="Optimal" if session_duration_min < 25.0 else "Mild Fatigue",
                recommended_break_type="Micro-defocus (20s)" if session_duration_min < 30.0 else "Saccadic Reset (60s)",
            )

        total_fixations = len(samples)
        regressions = sum(1 for s in samples if s.is_regression)
        regression_rate = regressions / total_fixations if total_fixations > 0 else 0.0
        mean_fixation_ms = (
            sum(s.fixation_duration_ms for s in samples) / total_fixations
        )

        # Fatigue formula weighted across ocular regressions, fixation duration, and session length
        # 1. Regression component (ideal < 0.15, severe > 0.40)
        reg_comp = min(100.0, regression_rate * 250.0)

        # 2. Fixation duration component (normal ~220ms, tired > 350ms)
        fix_comp = min(100.0, max(0.0, (mean_fixation_ms - 200.0) / 1.8))

        # 3. Session duration component (25m standard Pomodoro baseline)
        dur_comp = min(100.0, session_duration_min * 2.2)

        fatigue_score = round(
            0.35 * reg_comp + 0.35 * fix_comp + 0.30 * dur_comp, 1
        )
        fatigue_score = max(0.0, min(100.0, fatigue_score))

        if fatigue_score < 35.0:
            saturation_level = "Optimal"
            recommended_break = "Micro-defocus (20s)"
        elif fatigue_score < 55.0:
            saturation_level = "Mild Fatigue"
            recommended_break = "Saccadic Reset (60s)"
        elif fatigue_score < 75.0:
            saturation_level = "Cognitive Strain"
            recommended_break = "Spatial Breathing (3m)"
        else:
            saturation_level = "Exhaustion Threshold"
            recommended_break = "Executive Walk (10m)"

        return FatigueTelemetry(
            session_duration_min=session_duration_min,
            total_fixations=total_fixations,
            regression_rate=round(regression_rate, 3),
            mean_fixation_ms=round(mean_fixation_ms, 1),
            fatigue_score=fatigue_score,
            saturation_level=saturation_level,
            recommended_break_type=recommended_break,
        )

    def generate_break_protocol(self, telemetry: FatigueTelemetry) -> BreakProtocol:
        """
        Generate tailored spatial recovery steps based on current fatigue telemetry.
        """
        score = telemetry.fatigue_score

        if score < 35.0:
            return BreakProtocol(
                name="20-20-20 Micro-Defocus",
                duration_sec=20,
                protocol_type="micro_defocus",
                guidance_steps=[
                    "Shift gaze away from all monitors to an object at least 20 feet away.",
                    "Soften focus to engage peripheral vision across the horizon.",
                    "Blink slowly twice to lubricate cornea and release ocular tension.",
                ],
                breathing_pattern={"inhale": 4, "hold_in": 2, "exhale": 4, "hold_out": 2},
                spatial_focal_targets=[
                    {"label": "Far Horizon Anchor", "distance_meters": 6.0, "angle_deg": 0},
                ],
            )
        elif score < 55.0:
            return BreakProtocol(
                name="Saccadic Rhythm Stabilization",
                duration_sec=60,
                protocol_type="saccadic_reset",
                guidance_steps=[
                    "Close eyes and place warm palms gently over eye sockets for 15 seconds.",
                    "Open eyes and trace an imaginary infinity symbol (horizontal 8) with smooth pursuit.",
                    "Focus near on thumb at 25cm, then far on distant wall, alternating 4 times.",
                    "Take two deep diaphragmatic breaths through nose, releasing through mouth.",
                ],
                breathing_pattern={"inhale": 4, "hold_in": 4, "exhale": 4, "hold_out": 4},
                spatial_focal_targets=[
                    {"label": "Near Convergence", "distance_meters": 0.25, "angle_deg": 0},
                    {"label": "Distant Alignment", "distance_meters": 5.0, "angle_deg": 0},
                ],
            )
        elif score < 75.0:
            return BreakProtocol(
                name="Spatial Box Breathing and Core Defocus",
                duration_sec=180,
                protocol_type="spatial_breathing",
                guidance_steps=[
                    "Stand up from workstation and drop shoulders away from ears.",
                    "Inhale deeply through nose expanding belly (4 seconds).",
                    "Hold breath gently without clenching throat (4 seconds).",
                    "Exhale smoothly through parted lips (4 seconds).",
                    "Hold empty lungs in complete stillness (4 seconds).",
                    "Repeat cycle 8 times while scanning room perimeter smoothly.",
                ],
                breathing_pattern={"inhale": 4, "hold_in": 4, "exhale": 4, "hold_out": 4},
                spatial_focal_targets=[
                    {"label": "Upper Left Room Corner", "distance_meters": 3.5, "angle_deg": -30},
                    {"label": "Upper Right Room Corner", "distance_meters": 3.5, "angle_deg": 30},
                    {"label": "Lower Floor Horizon", "distance_meters": 2.0, "angle_deg": 0},
                ],
            )
        else:
            return BreakProtocol(
                name="Executive Reboot and Kinesthetic Walk",
                duration_sec=600,
                protocol_type="executive_walk",
                guidance_steps=[
                    "Step completely away from screen and device notifications.",
                    "Hydrate with 250ml cool water to restore vascular circulation.",
                    "Walk outdoors or through hallway with active arm swing for 7 minutes.",
                    "Expose eyes to natural ambient daylight (avoid direct sun stare).",
                    "Return to workstation with clear intention, avoiding immediate multi-tasking.",
                ],
                breathing_pattern={"inhale": 4, "hold_in": 7, "exhale": 8, "hold_out": 0},
                spatial_focal_targets=[
                    {"label": "Outdoor Ambient Horizon", "distance_meters": 50.0, "angle_deg": 0},
                ],
            )

    def export_spatial_canvas(self, protocol: BreakProtocol, output_path: str = "fatigue_break.canvas") -> str:
        """
        Export break protocol as an Obsidian .canvas visual layout.
        """
        nodes = []
        edges = []

        # Header card
        nodes.append({
            "id": "node-header",
            "x": 0,
            "y": 0,
            "width": 380,
            "height": 160,
            "type": "text",
            "text": (
                f"### [Break Protocol] {protocol.name}\n\n"
                f"- **Duration:** {protocol.duration_sec}s\n"
                f"- **Modality:** {protocol.protocol_type.replace('_', ' ').title()}\n"
                f"- **Focus:** Ocular and Executive Nervous System Reset"
            ),
            "color": "4",
        })

        # Guidance steps cards
        prev_id = "node-header"
        start_y = 200
        for i, step in enumerate(protocol.guidance_steps):
            step_id = f"node-step-{i + 1}"
            nodes.append({
                "id": step_id,
                "x": 0,
                "y": start_y + (i * 120),
                "width": 380,
                "height": 100,
                "type": "text",
                "text": f"**Step {i + 1}**\n\n{step}",
                "color": "5",
            })
            edges.append({
                "id": f"edge-{prev_id}-{step_id}",
                "fromNode": prev_id,
                "fromSide": "bottom",
                "toNode": step_id,
                "toSide": "top",
            })
            prev_id = step_id

        # Breathing card if available
        if protocol.breathing_pattern:
            bp = protocol.breathing_pattern
            breath_id = "node-breathing"
            nodes.append({
                "id": breath_id,
                "x": 420,
                "y": 0,
                "width": 340,
                "height": 220,
                "type": "text",
                "text": (
                    f"### Diaphragmatic Rhythm\n\n"
                    f"- Inhale: {bp.get('inhale', 4)}s\n"
                    f"- Hold (Full): {bp.get('hold_in', 4)}s\n"
                    f"- Exhale: {bp.get('exhale', 4)}s\n"
                    f"- Hold (Empty): {bp.get('hold_out', 4)}s\n\n"
                    f"*Regulates parasympathetic vagal tone.*"
                ),
                "color": "6",
            })
            edges.append({
                "id": "edge-header-breath",
                "fromNode": "node-header",
                "fromSide": "right",
                "toNode": breath_id,
                "toSide": "left",
            })

        canvas_data = {"nodes": nodes, "edges": edges}
        content = json.dumps(canvas_data, indent=2)

        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(content)

        return content

    def export_svg_breathing_visualizer(
        self,
        protocol: BreakProtocol,
        width: int = 500,
        height: int = 300,
    ) -> str:
        """
        Generate an accessible SVG vector visualizer for the breathing cadence and ocular targets.
        """
        bp = protocol.breathing_pattern or {"inhale": 4, "hold_in": 4, "exhale": 4, "hold_out": 4}
        total_cycle = bp.get("inhale", 4) + bp.get("hold_in", 4) + bp.get("exhale", 4) + bp.get("hold_out", 4)

        svg = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="auto">',
            '  <defs>',
            '    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">',
            '      <stop offset="0%" stop-color="#0f172a" />',
            '      <stop offset="100%" stop-color="#1e293b" />',
            '    </linearGradient>',
            '    <linearGradient id="circleGrad" x1="0%" y1="0%" x2="100%" y2="100%">',
            '      <stop offset="0%" stop-color="#38bdf8" />',
            '      <stop offset="100%" stop-color="#818cf8" />',
            '    </linearGradient>',
            '  </defs>',
            f'  <rect width="{width}" height="{height}" rx="12" fill="url(#bgGrad)" stroke="#334155" stroke-width="1.5" />',
            f'  <text x="25" y="36" fill="#f8fafc" font-family="system-ui, -apple-system, sans-serif" font-size="16" font-weight="bold">{protocol.name}</text>',
            f'  <text x="25" y="58" fill="#94a3b8" font-family="system-ui, -apple-system, sans-serif" font-size="12">Duration: {protocol.duration_sec}s | Cycle: {total_cycle}s rhythm</text>',
            '  <!-- Central Breathing Indicator -->',
            '  <circle cx="150" cy="175" r="75" fill="none" stroke="#334155" stroke-width="6" stroke-dasharray="6,6" />',
            '  <circle cx="150" cy="175" r="55" fill="url(#circleGrad)" opacity="0.85" />',
            '  <text x="150" y="170" fill="#0f172a" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="bold" text-anchor="middle">EXPAND</text>',
            f'  <text x="150" y="190" fill="#0f172a" font-family="system-ui, -apple-system, sans-serif" font-size="11" font-weight="600" text-anchor="middle">{bp.get("inhale", 4)}s Inhale</text>',
            '  <!-- Rhythm Cadence Labels -->',
            '  <g transform="translate(270, 95)">',
            f'    <text x="0" y="20" fill="#38bdf8" font-family="system-ui, -apple-system, sans-serif" font-size="13" font-weight="bold">1. Inhale: {bp.get("inhale", 4)}s (diaphragmatic expansion)</text>',
            f'    <text x="0" y="50" fill="#cbd5e1" font-family="system-ui, -apple-system, sans-serif" font-size="13">2. Hold: {bp.get("hold_in", 4)}s (peaceful suspension)</text>',
            f'    <text x="0" y="80" fill="#818cf8" font-family="system-ui, -apple-system, sans-serif" font-size="13" font-weight="bold">3. Exhale: {bp.get("exhale", 4)}s (smooth vocal release)</text>',
            f'    <text x="0" y="110" fill="#cbd5e1" font-family="system-ui, -apple-system, sans-serif" font-size="13">4. Stillness: {bp.get("hold_out", 4)}s (ocular softening)</text>',
            '    <line x1="0" y1="135" x2="200" y2="135" stroke="#334155" stroke-width="1" />',
            f'    <text x="0" y="155" fill="#a78bfa" font-family="system-ui, -apple-system, sans-serif" font-size="11">Goal: Parasympathetic Vagus Nerve Activation</text>',
            '  </g>',
            '</svg>',
        ]
        return "\n".join(svg)

    def generate_markdown_report(
        self,
        telemetry: FatigueTelemetry,
        protocol: BreakProtocol,
    ) -> str:
        """
        Generate a comprehensive executive recovery report in Markdown without em dashes.
        """
        lines = [
            f"# Spatial Fatigue Telemetry and Recovery Protocol",
            "",
            f"**Saturation Level:** {telemetry.saturation_level} ({telemetry.fatigue_score}/100)",
            f"**Session Duration:** {telemetry.session_duration_min} minutes",
            f"**Recommended Action:** {protocol.name} ({protocol.duration_sec}s)",
            "",
            "## 1. Ocular and Fixation Telemetry",
            "",
            f"- **Total Fixation Samples:** {telemetry.total_fixations}",
            f"- **Mean Fixation Dwell:** {telemetry.mean_fixation_ms} ms (baseline: ~220 ms)",
            f"- **Saccadic Regression Rate:** {round(telemetry.regression_rate * 100, 1)}% (ideal: < 15%)",
            f"- **Fatigue Index:** {telemetry.fatigue_score} / 100.0",
            "",
            "## 2. Prescribed Micro-Break Guidance",
            "",
            f"**Modality:** {protocol.protocol_type.replace('_', ' ').title()}",
            "",
        ]

        for i, step in enumerate(protocol.guidance_steps):
            lines.append(f"{i + 1}. {step}")

        if protocol.breathing_pattern:
            bp = protocol.breathing_pattern
            lines.extend([
                "",
                "## 3. Diaphragmatic Rhythm Pattern",
                "",
                f"- **Inhale Phase:** {bp.get('inhale', 4)} seconds (expand diaphragm and soften brow)",
                f"- **Full Suspension:** {bp.get('hold_in', 4)} seconds (stillness without tension)",
                f"- **Exhale Phase:** {bp.get('exhale', 4)} seconds (unclench jaw and drop shoulders)",
                f"- **Empty Stillness:** {bp.get('hold_out', 4)} seconds (relax ocular muscles into peripheral vision)",
            ])

        if protocol.spatial_focal_targets:
            lines.extend([
                "",
                "## 4. Spatial Focal Targets",
                "",
            ])
            for target in protocol.spatial_focal_targets:
                lines.append(
                    f"- **{target.get('label', 'Focal Point')}:** "
                    f"{target.get('distance_meters', 1.0)}m distance, {target.get('angle_deg', 0)} deg azimuth"
                )

        lines.extend([
            "",
            "---",
            "*Generated by DxSkills Fatigue Resiliency Harness. Zero phonological friction, zero em dashes.*",
        ])

        return "\n".join(lines)
