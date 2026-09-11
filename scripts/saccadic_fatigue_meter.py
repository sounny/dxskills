"""
saccadic_fatigue_meter.py - Autonomous Cognitive Spatial Working Memory Saccadic Fatigue Meter & Dynamic Contrast Damper

Part of the DxSkills cognitive scaffolding suite (Phase 100, Cycle 96).
Grounded in Carpenter (1988) saccadic main sequence dynamics, Raymond et al.
attentional blink physiology, and Bouma window photopic visual ergonomics.

Strict constraint: Strictly zero em dashes (Unicode U+2014) anywhere.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class GazeSessionSample:
    """Individual ocular tracking sample measuring saccade kinematics."""
    sample_id: str
    timestamp_ms: float
    saccade_amplitude_deg: float
    peak_velocity_deg_s: float
    fixation_duration_ms: float
    blink_interval_sec: float
    target_card_id: str


@dataclass
class ContrastDampingProfile:
    """Luminance and contrast attenuation profile for an individual spatial card."""
    card_id: str
    original_contrast_ratio: float
    damped_contrast_ratio: float
    luminance_level: float  # 0.0 to 1.0
    border_opacity: float  # 0.2 to 1.0
    recommended_kelvin: int
    restorative_action: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class FatigueMeterTelemetry:
    """Cognitive telemetry measuring ocular fatigue, velocity decay, and stamina."""
    total_samples_analyzed: int
    session_duration_minutes: float
    mean_peak_velocity_deg_s: float
    velocity_decay_pct: float
    ocular_fatigue_index: float  # 0.0 (fresh) to 1.0 (exhausted)
    attentional_blink_risk: str  # LOW, MODERATE, ELEVATED, CRITICAL
    recommended_break_sec: int
    contrast_attenuation_factor: float
    cowan_bounded: bool

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class FatigueMeterResult:
    """Master result bundle containing fatigue telemetry and damping profiles."""
    telemetry: FatigueMeterTelemetry
    card_profiles: List[ContrastDampingProfile]
    restorative_css_tokens: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "telemetry": self.telemetry.to_dict(),
            "card_profiles": [p.to_dict() for p in self.card_profiles],
            "restorative_css_tokens": self.restorative_css_tokens,
        }


class SaccadicFatigueMeter:
    """
    Autonomous Cognitive Spatial Working Memory Saccadic Fatigue Meter & Dynamic Contrast Damper.

    Tracks ocular velocity degradation, computes attentional blink risk, and dynamically
    dampens peripheral contrast and screen luminance to restore cognitive stamina.
    """

    def __init__(
        self,
        baseline_velocity_deg_s: float = 420.0,
        max_session_minutes: float = 45.0,
        target_contrast_ratio: float = 7.0,
    ) -> None:
        self.baseline_velocity = baseline_velocity_deg_s
        self.max_session_minutes = max_session_minutes
        self.target_contrast_ratio = target_contrast_ratio

    def evaluate_gaze_samples(
        self,
        samples: List[Any],
        cards: Optional[List[Dict[str, Any]]] = None,
    ) -> FatigueMeterResult:
        """
        Task 100.1: Continuous reading fatigue model predicting foveal velocity decay
        and attentional blink frequency.
        """
        parsed_samples: List[GazeSessionSample] = []

        if isinstance(samples, list):
            for idx, item in enumerate(samples):
                if isinstance(item, dict):
                    sid = str(item.get("sample_id") or f"sample_{idx+1}")
                    t_ms = float(item.get("timestamp_ms") or (idx * 500.0))
                    amp = float(item.get("saccade_amplitude_deg") or 8.0)
                    vel = float(item.get("peak_velocity_deg_s") or 380.0)
                    fix = float(item.get("fixation_duration_ms") or 220.0)
                    blink = float(item.get("blink_interval_sec") or 4.5)
                    cid = str(item.get("target_card_id") or f"card_{(idx % 4) + 1}")
                    parsed_samples.append(
                        GazeSessionSample(
                            sample_id=sid,
                            timestamp_ms=t_ms,
                            saccade_amplitude_deg=amp,
                            peak_velocity_deg_s=vel,
                            fixation_duration_ms=fix,
                            blink_interval_sec=blink,
                            target_card_id=cid,
                        )
                    )
                elif isinstance(item, GazeSessionSample):
                    parsed_samples.append(item)

        if not parsed_samples:
            empty_telemetry = FatigueMeterTelemetry(
                total_samples_analyzed=0,
                session_duration_minutes=0.0,
                mean_peak_velocity_deg_s=self.baseline_velocity,
                velocity_decay_pct=0.0,
                ocular_fatigue_index=0.0,
                attentional_blink_risk="LOW",
                recommended_break_sec=0,
                contrast_attenuation_factor=1.0,
                cowan_bounded=True,
            )
            return FatigueMeterResult(
                telemetry=empty_telemetry,
                card_profiles=[],
                restorative_css_tokens="",
            )

        # 1. Compute kinematics and decay metrics
        total_samples = len(parsed_samples)
        duration_ms = (
            parsed_samples[-1].timestamp_ms - parsed_samples[0].timestamp_ms
            if total_samples > 1
            else 60000.0
        )
        duration_min = max(0.5, duration_ms / 60000.0)

        # Early window vs Late window velocity comparison
        split_point = max(1, total_samples // 3)
        early_samples = parsed_samples[:split_point]
        late_samples = parsed_samples[-split_point:]

        early_vel = sum(s.peak_velocity_deg_s for s in early_samples) / len(early_samples)
        late_vel = sum(s.peak_velocity_deg_s for s in late_samples) / len(late_samples)
        mean_vel = sum(s.peak_velocity_deg_s for s in parsed_samples) / total_samples

        # Velocity decay calculation
        velocity_drop = max(0.0, early_vel - late_vel)
        decay_pct = (velocity_drop / early_vel * 100.0) if early_vel > 0 else 0.0

        # Mean blink interval: lower interval (< 2.5s) or excessive interval (> 8s) signals strain
        mean_blink = sum(s.blink_interval_sec for s in parsed_samples) / total_samples
        blink_strain = 0.0
        if mean_blink < 2.5:
            blink_strain = 0.3  # Rapid compensatory blinking
        elif mean_blink > 7.0:
            blink_strain = 0.4  # Fixational staring causing tear film breakup

        # Ocular Fatigue Index (OFI): combination of duration, velocity decay, and blink strain
        duration_factor = min(1.0, duration_min / self.max_session_minutes)
        velocity_factor = min(1.0, decay_pct / 30.0)
        ofi = round(min(1.0, (0.45 * duration_factor) + (0.40 * velocity_factor) + (0.15 * blink_strain)), 2)

        # Attentional blink risk classification
        if ofi < 0.25:
            risk = "LOW"
            rec_break = 0
            attenuation = 1.0
        elif ofi < 0.50:
            risk = "MODERATE"
            rec_break = 60
            attenuation = 0.85
        elif ofi < 0.75:
            risk = "ELEVATED"
            rec_break = 180
            attenuation = 0.65
        else:
            risk = "CRITICAL"
            rec_break = 300
            attenuation = 0.45

        telemetry = FatigueMeterTelemetry(
            total_samples_analyzed=total_samples,
            session_duration_minutes=round(duration_min, 1),
            mean_peak_velocity_deg_s=round(mean_vel, 1),
            velocity_decay_pct=round(decay_pct, 1),
            ocular_fatigue_index=ofi,
            attentional_blink_risk=risk,
            recommended_break_sec=rec_break,
            contrast_attenuation_factor=attenuation,
            cowan_bounded=True,
        )

        # 2. Task 100.2: Compute adaptive contrast damping profiles
        target_cards = cards or [
            {"id": cid} for cid in {s.target_card_id for s in parsed_samples}
        ]
        card_profiles = self.compute_contrast_damping(target_cards, ofi)

        # 3. Generate CSS tokens
        kelvin = 3400 if ofi > 0.6 else (4200 if ofi > 0.3 else 5500)
        css_tokens = (
            f":root {{\n"
            f"  --dx-ocular-fatigue: {ofi:.2f};\n"
            f"  --dx-contrast-attenuation: {attenuation:.2f};\n"
            f"  --dx-color-temperature: {kelvin}K;\n"
            f"  --dx-ambient-luminance: {round(max(0.3, 1.0 - (ofi * 0.5)), 2)};\n"
            f"  --dx-border-softening: {round(min(1.0, 0.4 + ofi * 0.5), 2)}px;\n"
            f"}}"
        )

        return FatigueMeterResult(
            telemetry=telemetry,
            card_profiles=card_profiles,
            restorative_css_tokens=css_tokens,
        )

    def compute_contrast_damping(
        self, cards: List[Dict[str, Any]], fatigue_index: float
    ) -> List[ContrastDampingProfile]:
        """Task 100.2: Applies adaptive luminance and contrast ramp dampener across cards."""
        profiles: List[ContrastDampingProfile] = []

        for idx, card in enumerate(cards):
            cid = str(card.get("id") or f"card_{idx+1}")
            is_focal = card.get("is_focal", idx == 0)

            # High fatigue lowers overall contrast to protect rod/cone photoreceptors
            orig_contrast = 14.5
            if is_focal:
                # Keep focal card readable with warm contrast
                damped_contrast = round(max(7.0, orig_contrast * (1.0 - (fatigue_index * 0.25))), 1)
                luminance = round(max(0.70, 1.0 - (fatigue_index * 0.20)), 2)
                border_op = round(max(0.60, 1.0 - (fatigue_index * 0.20)), 2)
                action = "Photopic soft focus preserved"
            else:
                # Peripheral cards dampened aggressively
                damped_contrast = round(max(3.5, orig_contrast * (1.0 - (fatigue_index * 0.60))), 1)
                luminance = round(max(0.35, 0.85 - (fatigue_index * 0.45)), 2)
                border_op = round(max(0.20, 0.60 - (fatigue_index * 0.40)), 2)
                action = "Peripheral glare attenuated"

            kelvin = 3200 if fatigue_index > 0.6 else (4000 if fatigue_index > 0.3 else 5200)

            profiles.append(
                ContrastDampingProfile(
                    card_id=cid,
                    original_contrast_ratio=orig_contrast,
                    damped_contrast_ratio=damped_contrast,
                    luminance_level=luminance,
                    border_opacity=border_op,
                    recommended_kelvin=kelvin,
                    restorative_action=action,
                )
            )

        return profiles

    def export_svg(self, result: FatigueMeterResult, output_path: Optional[str] = None) -> str:
        """
        Exports a dark titanium visual SVG diagram showing the Carpenter Main Sequence
        saccadic velocity decay curve and the adaptive contrast damping ramp.
        """
        w, h = 900, 520
        t = result.telemetry

        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">',
            '  <defs>',
            '    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">',
            '      <stop offset="0%" stop-color="#090d16"/>',
            '      <stop offset="100%" stop-color="#0f172a"/>',
            '    </linearGradient>',
            '    <linearGradient id="curveFill" x1="0%" y1="0%" x2="0%" y2="100%">',
            '      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.35"/>',
            '      <stop offset="100%" stop-color="#38bdf8" stop-opacity="0.0"/>',
            '    </linearGradient>',
            '    <linearGradient id="decayFill" x1="0%" y1="0%" x2="0%" y2="100%">',
            '      <stop offset="0%" stop-color="#f43f5e" stop-opacity="0.25"/>',
            '      <stop offset="100%" stop-color="#f43f5e" stop-opacity="0.0"/>',
            '    </linearGradient>',
            '  </defs>',
            '  <rect width="100%" height="100%" fill="url(#bg)"/>',
            '  <!-- Header -->',
            '  <text x="40" y="44" font-family="system-ui, -apple-system, sans-serif" font-size="18" font-weight="700" fill="#f8fafc">Saccadic Fatigue Meter &amp; Dynamic Contrast Damper</text>',
            f'  <text x="40" y="68" font-family="system-ui, -apple-system, sans-serif" font-size="12" fill="#94a3b8">Carpenter Main Sequence &bull; Velocity Decay: -{t.velocity_decay_pct}% &bull; Attentional Blink Risk: {t.attentional_blink_risk} &bull; OFI: {t.ocular_fatigue_index}</text>',
            '  <!-- Kinematic Chart Viewport -->',
            '  <g transform="translate(60, 95)">',
            '    <rect width="780" height="260" rx="12" fill="#0b1120" stroke="#1e293b" stroke-width="1.5"/>',
            '    <!-- Axes -->',
            '    <line x1="60" y1="210" x2="720" y2="210" stroke="#334155" stroke-width="1.5"/>',
            '    <line x1="60" y1="40" x2="60" y2="210" stroke="#334155" stroke-width="1.5"/>',
            '    <text x="60" y="30" font-family="system-ui, -apple-system, sans-serif" font-size="10" fill="#94a3b8">Velocity (deg/s)</text>',
            '    <text x="720" y="228" font-family="system-ui, -apple-system, sans-serif" font-size="10" fill="#94a3b8" text-anchor="end">Session Time &rarr;</text>',
            '    <!-- Baseline Curve (Cyan Dashed) -->',
            '    <path d="M 60 70 Q 300 75 720 85" fill="none" stroke="#38bdf8" stroke-width="2" stroke-dasharray="4,4"/>',
            '    <text x="680" y="75" font-family="system-ui, -apple-system, sans-serif" font-size="10" fill="#7dd3fc">Baseline Velocity</text>',
            '    <!-- Actual Decaying Velocity Curve (Red/Amber) -->',
            '    <path d="M 60 70 Q 250 85 450 135 T 720 170" fill="none" stroke="#f43f5e" stroke-width="3"/>',
            '    <text x="680" y="160" font-family="system-ui, -apple-system, sans-serif" font-size="10" font-weight="700" fill="#fb7185">Fatigue Decay Curve</text>',
            '    <!-- Restorative Contrast Ramp Zone -->',
            '    <rect x="420" y="45" width="280" height="160" fill="#10b981" fill-opacity="0.08" stroke="#10b981" stroke-width="1" stroke-dasharray="3,3"/>',
            '    <text x="435" y="65" font-family="system-ui, -apple-system, sans-serif" font-size="11" font-weight="700" fill="#34d399">Dynamic Contrast Damping Active</text>',
            '    <text x="435" y="85" font-family="system-ui, -apple-system, sans-serif" font-size="10" fill="#6ee7b7">&bull; Attenuation: {int(t.contrast_attenuation_factor*100)}%</text>',
            '    <text x="435" y="103" font-family="system-ui, -apple-system, sans-serif" font-size="10" fill="#6ee7b7">&bull; Ambient Kelvin: 3400K</text>',
            '    <text x="435" y="121" font-family="system-ui, -apple-system, sans-serif" font-size="10" fill="#6ee7b7">&bull; Peripheral Glare: -55%</text>',
            '  </g>',
            '  <!-- Bottom Cards: Telemetry Badges -->',
            '  <g transform="translate(60, 380)">',
            '    <rect x="0" y="0" width="240" height="90" rx="10" fill="#0b1120" stroke="#1e293b" stroke-width="1.5"/>',
            '    <text x="20" y="28" font-family="system-ui, -apple-system, sans-serif" font-size="11" fill="#94a3b8">Ocular Fatigue Index (OFI)</text>',
            f'    <text x="20" y="60" font-family="system-ui, -apple-system, sans-serif" font-size="26" font-weight="800" fill="#f43f5e">{t.ocular_fatigue_index}</text>',
            f'    <text x="20" y="80" font-family="system-ui, -apple-system, sans-serif" font-size="10" fill="#64748b">Session: {t.session_duration_minutes} min</text>',
            '    <rect x="270" y="0" width="240" height="90" rx="10" fill="#0b1120" stroke="#1e293b" stroke-width="1.5"/>',
            '    <text x="290" y="28" font-family="system-ui, -apple-system, sans-serif" font-size="11" fill="#94a3b8">Attentional Blink Risk</text>',
            f'    <text x="290" y="60" font-family="system-ui, -apple-system, sans-serif" font-size="24" font-weight="800" fill="#f59e0b">{t.attentional_blink_risk}</text>',
            f'    <text x="290" y="80" font-family="system-ui, -apple-system, sans-serif" font-size="10" fill="#64748b">Velocity drop: -{t.velocity_decay_pct}%</text>',
            '    <rect x="540" y="0" width="240" height="90" rx="10" fill="#0b1120" stroke="#1e293b" stroke-width="1.5"/>',
            '    <text x="560" y="28" font-family="system-ui, -apple-system, sans-serif" font-size="11" fill="#94a3b8">Recommended Pause</text>',
            f'    <text x="560" y="60" font-family="system-ui, -apple-system, sans-serif" font-size="26" font-weight="800" fill="#10b981">{t.recommended_break_sec}s</text>',
            '    <text x="560" y="80" font-family="system-ui, -apple-system, sans-serif" font-size="10" fill="#64748b">Micro-break resets tear film</text>',
            '  </g>',
            '</svg>',
        ]

        svg_content = "\n".join(svg_parts)

        if output_path:
            p = Path(output_path)
            p.parent.mkdir(parents=True, exist_ok=True)
            with open(p, "w", encoding="utf-8") as f:
                f.write(svg_content)

        return svg_content

    def generate_ascii_report(self, result: FatigueMeterResult) -> str:
        """Generates a clean terminal ASCII table summarizing the fatigue telemetry."""
        t = result.telemetry
        lines = [
            "================================================================================",
            "   SACCADIC FATIGUE METER & DYNAMIC CONTRAST DAMPER (PHASE 100 / CYCLE 96)",
            "================================================================================",
            f" Samples Processed     : {t.total_samples_analyzed} gaze events across {t.session_duration_minutes:.1f} minutes",
            f" Mean Peak Velocity    : {t.mean_peak_velocity_deg_s:.1f} deg/s (Baseline: {self.baseline_velocity:.1f} deg/s)",
            f" Velocity Decay Rate   : -{t.velocity_decay_pct:.1f}%",
            f" Ocular Fatigue Index  : {t.ocular_fatigue_index:.2f} (0.0=Optimal, 1.0=Exhaustion)",
            f" Attentional Blink     : [{t.attentional_blink_risk}] Risk",
            f" Recommended Pause     : {t.recommended_break_sec} seconds (Restorative ocular reset)",
            f" Contrast Attenuation  : {int(t.contrast_attenuation_factor * 100)}% (Glaring peripheral cards dimmed)",
            "--------------------------------------------------------------------------------",
            " CARD CONTRAST DAMPING PROFILES (FIRST 4 CARDS)",
            "--------------------------------------------------------------------------------",
        ]

        if not result.card_profiles:
            lines.append(" (No card profiles evaluated)")
        else:
            for p in result.card_profiles[:4]:
                lines.append(f" CARD [{p.card_id}]: Contrast {p.original_contrast_ratio}:1 ==> {p.damped_contrast_ratio}:1 (Lum: {p.luminance_level:.2f})")
                lines.append(f"   Action : {p.restorative_action} | Temp: {p.recommended_kelvin}K | Border Opacity: {p.border_opacity:.2f}")

        lines.append("================================================================================")
        return "\n".join(lines)
