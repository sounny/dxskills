"""
attention_gradient_shaper.py - Autonomous Cognitive Spatial Dynamic Attention Gradient & Peripheral Saccade Shaper

Part of the DxSkills cognitive scaffolding suite (Phase 104, Cycle 100).
Grounded in Anstis (1974) eccentricity acuity decay, Bouma (1970) visual crowding window,
and Findlay & Gilchrist (2003) active vision dynamics.

Strict constraint: Strictly zero em dashes (Unicode U+2014) anywhere.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class CardAcuityProfile:
    """Card-level peripheral acuity decay and high-frequency edge attenuation profile."""
    card_id: str
    title: str
    center_x: float
    center_y: float
    eccentricity_deg: float  # Visual angle in degrees from focal gaze center
    eccentricity_px: float
    visual_acuity_factor: float  # 1.0 (foveal 20/20) down to 0.05 (far periphery)
    bouma_crowding_radius_px: float  # Bouma's law: critical spacing ~ 0.5 * eccentricity
    attenuation_pct: float  # High-frequency clutter dampening percentage (0% to 85%)
    blur_radius_px: float  # Softening blur applied to peripheral distractors
    opacity_multiplier: float  # Contrast/opacity scaling (1.0 focal down to 0.35 periphery)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class GradientTelemetry:
    """Cognitive telemetry measuring peripheral clutter suppression and saccadic momentum."""
    total_cards_evaluated: int
    focal_card_id: str
    focal_gaze_coords: Tuple[float, float]
    max_eccentricity_deg: float
    mean_attenuation_pct: float
    peripheral_drag_reduction_pct: float
    momentum_clarity_score: float  # 0 to 100 rating of corridor channel clarity
    cowan_bounded: bool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_cards_evaluated": self.total_cards_evaluated,
            "focal_card_id": self.focal_card_id,
            "focal_gaze_coords": list(self.focal_gaze_coords),
            "max_eccentricity_deg": self.max_eccentricity_deg,
            "mean_attenuation_pct": self.mean_attenuation_pct,
            "peripheral_drag_reduction_pct": self.peripheral_drag_reduction_pct,
            "momentum_clarity_score": self.momentum_clarity_score,
            "cowan_bounded": self.cowan_bounded,
        }


@dataclass
class GradientShaperResult:
    """Master result bundle containing card profiles, corridor trajectory, telemetry, and SVG."""
    card_profiles: List[CardAcuityProfile]
    telemetry: GradientTelemetry
    saccade_corridor: List[Tuple[float, float]]
    svg_diagram: str
    attenuation_css: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "telemetry": self.telemetry.to_dict(),
            "card_profiles": [p.to_dict() for p in self.card_profiles],
            "saccade_corridor": [list(pt) for pt in self.saccade_corridor],
            "svg_diagram": self.svg_diagram,
            "attenuation_css": self.attenuation_css,
        }


class AttentionGradientShaper:
    """
    Autonomous Cognitive Spatial Dynamic Attention Gradient & Peripheral Saccade Shaper.

    Models retinal eccentricity acuity decay (Anstis 1974) and Bouma crowding zones across
    2D spatial workspaces, muting peripheral visual clutter to carve clean ballistic saccade corridors.
    """

    def __init__(
        self,
        px_per_deg: float = 45.0,  # ~45 pixels per degree at standard 60cm monitor distance
        foveal_radius_deg: float = 2.0,  # Fovea centralis (~2 degrees visual angle)
        parafoveal_radius_deg: float = 5.0,  # Parafovea (~5 degrees visual angle)
    ) -> None:
        self.px_per_deg = px_per_deg
        self.foveal_radius_deg = foveal_radius_deg
        self.parafoveal_radius_deg = parafoveal_radius_deg

    def calculate_gradient(
        self,
        gaze_x: float,
        gaze_y: float,
        cards: List[Dict[str, Any]],
        saccade_target: Optional[Dict[str, float]] = None,
    ) -> GradientShaperResult:
        """
        Task 104.1 & 104.2: Computes eccentric visual acuity decay across cards,
        attenuates peripheral edge clutter, and shapes a non-linear saccade momentum corridor.
        """
        if not cards:
            empty_telemetry = GradientTelemetry(
                total_cards_evaluated=0,
                focal_card_id="",
                focal_gaze_coords=(gaze_x, gaze_y),
                max_eccentricity_deg=0.0,
                mean_attenuation_pct=0.0,
                peripheral_drag_reduction_pct=0.0,
                momentum_clarity_score=0.0,
                cowan_bounded=True,
            )
            return GradientShaperResult(
                card_profiles=[],
                telemetry=empty_telemetry,
                saccade_corridor=[],
                svg_diagram="",
                attenuation_css="",
            )

        profiles: List[CardAcuityProfile] = []
        max_ecc_deg = 0.0
        total_att = 0.0

        # Identify focal card closest to gaze center
        cards_with_dist = []
        for c in cards:
            cx = float(c.get("x", 0.0)) + float(c.get("width", 280.0)) / 2.0
            cy = float(c.get("y", 0.0)) + float(c.get("height", 180.0)) / 2.0
            dist_px = math.hypot(cx - gaze_x, cy - gaze_y)
            cards_with_dist.append((dist_px, cx, cy, c))

        cards_with_dist.sort(key=lambda item: item[0])
        focal_card_id = str(cards_with_dist[0][3].get("id", "card_focal"))

        # Saccade corridor calculation (Task 104.2)
        corridor_points: List[Tuple[float, float]] = [(gaze_x, gaze_y)]
        t_x = float(saccade_target.get("x", gaze_x + 600.0)) if saccade_target else (gaze_x + 500.0)
        t_y = float(saccade_target.get("y", gaze_y + 200.0)) if saccade_target else (gaze_y + 150.0)

        # Generate parabolic ballistic curve points
        for step in (0.25, 0.50, 0.75, 1.0):
            # Parabolic sag for natural ocular ballistic trajectory
            sag = math.sin(step * math.pi) * 60.0
            px = round(gaze_x + step * (t_x - gaze_x), 1)
            py = round(gaze_y + step * (t_y - gaze_y) - sag, 1)
            corridor_points.append((px, py))

        # Evaluate each card against Anstis acuity formula and Bouma window
        for dist_px, cx, cy, c in cards_with_dist:
            cid = str(c.get("id", f"c_{len(profiles)+1}"))
            title = str(c.get("title", f"Card {len(profiles)+1}"))
            ecc_deg = round(dist_px / self.px_per_deg, 2)
            max_ecc_deg = max(max_ecc_deg, ecc_deg)

            # Anstis (1974) relative acuity formula: A = 1 / (1 + 0.3 * E)
            acuity = round(1.0 / (1.0 + 0.30 * ecc_deg), 3)

            # Bouma's law: critical crowding spacing = 0.5 * eccentricity in pixels
            bouma_px = round(0.50 * dist_px, 1)

            # Corridor proximity bonus: if card lies close to planned saccade path, spare attenuation
            min_corridor_dist = min(math.hypot(cx - cpx, cy - cpy) for cpx, cpy in corridor_points)
            corridor_shield = max(0.0, 1.0 - (min_corridor_dist / 350.0))

            # Calculate clutter attenuation percentage (Task 104.2)
            if ecc_deg <= self.foveal_radius_deg:
                att_pct = 0.0
                blur_px = 0.0
                opacity = 1.0
            elif ecc_deg <= self.parafoveal_radius_deg:
                att_pct = round(max(0.0, (ecc_deg - self.foveal_radius_deg) * 8.0 * (1.0 - corridor_shield * 0.5)), 1)
                blur_px = round(att_pct * 0.03, 1)
                opacity = round(1.0 - (att_pct * 0.003), 2)
            else:
                base_att = min(85.0, 25.0 + (ecc_deg - self.parafoveal_radius_deg) * 4.5)
                att_pct = round(max(10.0, base_att * (1.0 - corridor_shield * 0.6)), 1)
                blur_px = round(min(5.0, 0.8 + (att_pct * 0.05)), 1)
                opacity = round(max(0.35, 1.0 - (att_pct * 0.007)), 2)

            total_att += att_pct

            profiles.append(CardAcuityProfile(
                card_id=cid,
                title=title,
                center_x=round(cx, 1),
                center_y=round(cy, 1),
                eccentricity_deg=ecc_deg,
                eccentricity_px=round(dist_px, 1),
                visual_acuity_factor=acuity,
                bouma_crowding_radius_px=bouma_px,
                attenuation_pct=att_pct,
                blur_radius_px=blur_px,
                opacity_multiplier=opacity,
            ))

        mean_att = round(total_att / max(1, len(profiles)), 1)
        drag_reduction = round(min(80.0, mean_att * 0.95), 1)
        momentum_clarity = round(min(98.0, 50.0 + (drag_reduction * 0.55)), 1)
        cowan_bounded = len([p for p in profiles if p.attenuation_pct < 20.0]) <= 4

        telemetry = GradientTelemetry(
            total_cards_evaluated=len(profiles),
            focal_card_id=focal_card_id,
            focal_gaze_coords=(round(gaze_x, 1), round(gaze_y, 1)),
            max_eccentricity_deg=max_ecc_deg,
            mean_attenuation_pct=mean_att,
            peripheral_drag_reduction_pct=drag_reduction,
            momentum_clarity_score=momentum_clarity,
            cowan_bounded=cowan_bounded,
        )

        # Generate CSS rules for peripheral card attenuation
        css_rules = [
            "/* DxSkills Attention Gradient & Saccade Shaper Tokens */",
            f".dx-focal-gaze {{ outline: 2.5px solid #0284c7; box-shadow: 0 0 24px rgba(2, 132, 199, 0.4); }}",
            f".dx-saccade-corridor {{ transition: filter 240ms ease, opacity 240ms ease; }}",
        ]
        for p in profiles:
            css_rules.append(
                f"[data-node-id=\"{p.card_id}\"] {{ "
                f"filter: blur({p.blur_radius_px}px); "
                f"opacity: {p.opacity_multiplier}; "
                f"}}"
            )
        attenuation_css = "\n".join(css_rules) + "\n"

        svg_diagram = self._render_gradient_svg(
            gaze=(gaze_x, gaze_y),
            corridor=corridor_points,
            profiles=profiles,
            telemetry=telemetry,
        )

        return GradientShaperResult(
            card_profiles=profiles,
            telemetry=telemetry,
            saccade_corridor=corridor_points,
            svg_diagram=svg_diagram,
            attenuation_css=attenuation_css,
        )

    def _render_gradient_svg(
        self,
        gaze: Tuple[float, float],
        corridor: List[Tuple[float, float]],
        profiles: List[CardAcuityProfile],
        telemetry: GradientTelemetry,
    ) -> str:
        """Renders dark titanium SVG showing eccentric acuity rings, corridor, and card nodes."""
        w, h = 920, 520
        t = telemetry

        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">',
            '  <defs>',
            '    <linearGradient id="agBg" x1="0%" y1="0%" x2="100%" y2="100%">',
            '      <stop offset="0%" stop-color="#090d16"/>',
            '      <stop offset="100%" stop-color="#0f172a"/>',
            '    </linearGradient>',
            '    <radialGradient id="foveaSpot" cx="50%" cy="50%" r="50%">',
            '      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.35"/>',
            '      <stop offset="40%" stop-color="#0284c7" stop-opacity="0.15"/>',
            '      <stop offset="100%" stop-color="#0284c7" stop-opacity="0.0"/>',
            '    </radialGradient>',
            '  </defs>',
            '  <rect width="100%" height="100%" fill="url(#agBg)"/>',
            '  <!-- Header -->',
            '  <text x="40" y="44" font-family="system-ui, -apple-system, sans-serif" font-size="18" font-weight="700" fill="#f8fafc">Attention Gradient &amp; Peripheral Saccade Shaper</text>',
            f'  <text x="40" y="68" font-family="system-ui, -apple-system, sans-serif" font-size="12" fill="#94a3b8">Anstis Retinal Acuity &bull; Drag Reduction: {t.peripheral_drag_reduction_pct}% &bull; Corridor Clarity: {t.momentum_clarity_score}/100 &bull; Max Ecc: {t.max_eccentricity_deg}&deg;</text>',
            '  <!-- Viewport Canvas Frame -->',
            '  <g transform="translate(60, 95)">',
            '    <rect width="800" height="265" rx="12" fill="#070b14" stroke="#1e293b" stroke-width="1.5"/>',
            '    <!-- Concentric Acuity Decay Zones (Center at x=180, y=130) -->',
            '    <!-- Fovea (0-2 deg) -->',
            '    <circle cx="180" cy="130" r="45" fill="url(#foveaSpot)" stroke="#38bdf8" stroke-width="1.5"/>',
            '    <!-- Parafovea (2-5 deg) -->',
            '    <circle cx="180" cy="130" r="110" fill="none" stroke="#0284c7" stroke-width="1" stroke-dasharray="4,4" stroke-opacity="0.6"/>',
            '    <!-- Periphery (>5 deg) -->',
            '    <circle cx="180" cy="130" r="190" fill="none" stroke="#475569" stroke-width="1" stroke-dasharray="2,4" stroke-opacity="0.4"/>',
            '    <!-- Zone Labels -->',
            '    <text x="180" y="75" font-family="monospace" font-size="9" fill="#38bdf8" text-anchor="middle">FOVEA (100% Acuity)</text>',
            '    <text x="180" y="15" font-family="monospace" font-size="9" fill="#0284c7" text-anchor="middle">PARAFOVEA (Bouma Zone)</text>',
            '    <text x="180" y="-45" font-family="monospace" font-size="9" fill="#64748b" text-anchor="middle">PERIPHERAL ATTENUATION</text>',
            '    <!-- Ballistic Saccade Momentum Corridor -->',
            '    <path d="M 180 130 Q 380 40 650 110" fill="none" stroke="#10b981" stroke-width="3" stroke-dasharray="6,4"/>',
            '    <!-- Target Fixation Point -->',
            '    <circle cx="650" cy="110" r="10" fill="#059669" stroke="#34d399" stroke-width="2"/>',
            '    <text x="650" y="135" font-family="system-ui, -apple-system, sans-serif" font-size="10" font-weight="700" fill="#a7f3d0" text-anchor="middle">Saccadic Target</text>',
            '    <!-- Focal Gaze Point -->',
            '    <circle cx="180" cy="130" r="10" fill="#0284c7" stroke="#f8fafc" stroke-width="2.5"/>',
            '    <text x="180" y="155" font-family="system-ui, -apple-system, sans-serif" font-size="10" font-weight="700" fill="#bae6fd" text-anchor="middle">Gaze Center</text>',
            '    <!-- Peripheral Distractor Cards (Attenuated) -->',
            '    <g transform="translate(420, 185)">',
            '      <rect x="-60" y="-18" width="120" height="36" rx="6" fill="#1e293b" fill-opacity="0.4" stroke="#334155" stroke-dasharray="3,3"/>',
            '      <text x="0" y="4" font-family="system-ui, -apple-system, sans-serif" font-size="9" fill="#64748b" text-anchor="middle">[Damped Distractor]</text>',
            '    </g>',
            '    <g transform="translate(620, 205)">',
            '      <rect x="-60" y="-18" width="120" height="36" rx="6" fill="#1e293b" fill-opacity="0.3" stroke="#334155" stroke-dasharray="3,3"/>',
            '      <text x="0" y="4" font-family="system-ui, -apple-system, sans-serif" font-size="9" fill="#475569" text-anchor="middle">[Edge Clutter -75%]</text>',
            '    </g>',
            '  </g>',
            '  <!-- Bottom Cards: Telemetry Badges -->',
            '  <g transform="translate(60, 385)">',
            '    <rect x="0" y="0" width="240" height="90" rx="10" fill="#0b1120" stroke="#1e293b" stroke-width="1.5"/>',
            '    <text x="20" y="28" font-family="system-ui, -apple-system, sans-serif" font-size="11" fill="#94a3b8">Peripheral Drag Reduction</text>',
            f'    <text x="20" y="60" font-family="system-ui, -apple-system, sans-serif" font-size="26" font-weight="800" fill="#38bdf8">{t.peripheral_drag_reduction_pct}%</text>',
            f'    <text x="20" y="80" font-family="system-ui, -apple-system, sans-serif" font-size="10" fill="#64748b">Mean attenuation across {t.total_cards_evaluated} nodes</text>',
            '    <rect x="270" y="0" width="240" height="90" rx="10" fill="#0b1120" stroke="#1e293b" stroke-width="1.5"/>',
            '    <text x="290" y="28" font-family="system-ui, -apple-system, sans-serif" font-size="11" fill="#94a3b8">Momentum Corridor Clarity</text>',
            f'    <text x="290" y="60" font-family="system-ui, -apple-system, sans-serif" font-size="26" font-weight="800" fill="#10b981">{t.momentum_clarity_score}/100</text>',
            f'    <text x="290" y="80" font-family="system-ui, -apple-system, sans-serif" font-size="10" fill="#64748b">Shielded ballistic trajectory path</text>',
            '    <rect x="540" y="0" width="240" height="90" rx="10" fill="#0b1120" stroke="#1e293b" stroke-width="1.5"/>',
            '    <text x="560" y="28" font-family="system-ui, -apple-system, sans-serif" font-size="11" fill="#94a3b8">Cowan Uncluttered Bounds</text>',
            f'    <text x="560" y="60" font-family="system-ui, -apple-system, sans-serif" font-size="26" font-weight="800" fill="#f59e0b">{"&lt;= 4 Cards" if t.cowan_bounded else "&gt; 4 Cards"}</text>',
            f'    <text x="560" y="80" font-family="system-ui, -apple-system, sans-serif" font-size="10" fill="#64748b">Cowan bounded: {t.cowan_bounded}</text>',
            '  </g>',
            '</svg>',
        ]

        return "\n".join(svg_parts)

    def export_svg(self, result: GradientShaperResult, output_path: Optional[str] = None) -> str:
        """Exports SVG diagram to file or returns XML string."""
        if output_path:
            p = Path(output_path)
            p.parent.mkdir(parents=True, exist_ok=True)
            with open(p, "w", encoding="utf-8") as f:
                f.write(result.svg_diagram)
        return result.svg_diagram

    def generate_ascii_report(self, result: GradientShaperResult) -> str:
        """Generates clean terminal ASCII table summarizing attention gradient metrics."""
        t = result.telemetry
        lines = [
            "================================================================================",
            "   ATTENTION GRADIENT & PERIPHERAL SACCADE SHAPER (PHASE 104 / CYCLE 100)",
            "================================================================================",
            f" Cards Evaluated       : {t.total_cards_evaluated} workspace nodes",
            f" Focal Gaze Center     : ({t.focal_gaze_coords[0]}, {t.focal_gaze_coords[1]}) [Focal Card: {t.focal_card_id}]",
            f" Max Eccentricity      : {t.max_eccentricity_deg:.2f} deg visual angle",
            f" Mean Attenuation      : {t.mean_attenuation_pct:.1f}% edge clutter suppression",
            f" Drag Reduction        : {t.peripheral_drag_reduction_pct:.1f}% cognitive load relief",
            f" Momentum Clarity      : {t.momentum_clarity_score:.1f}/100 corridor channel rating",
            f" Cowan Bounded (N<=4)  : {'Yes [OPTIMAL]' if t.cowan_bounded else 'No [EXCEEDS CAPACITY]'}",
            "--------------------------------------------------------------------------------",
            " EVALUATED CARD ECCENTRICITY & ATTENUATION PROFILES",
            "--------------------------------------------------------------------------------",
        ]

        if not result.card_profiles:
            lines.append(" (No cards evaluated; empty workspace input)")
        else:
            for p in result.card_profiles[:5]:
                lines.append(f" [CARD] '{p.title}' (Ecc: {p.eccentricity_deg:.1f} deg | Acuity: {p.visual_acuity_factor:.2f})")
                lines.append(f"        Dampening: {p.attenuation_pct:.1f}% | Blur: {p.blur_radius_px}px | Opacity: {p.opacity_multiplier:.2f}")

        lines.append("================================================================================")
        return "\n".join(lines)
