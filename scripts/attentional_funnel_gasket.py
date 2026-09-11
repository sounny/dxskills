"""
Attentional Funnel & Saccadic Boundary Gasket
Grounding: Cowan working memory bounds (N <= 4), Bouma law of visual crowding,
Lavie perceptual load theory, and vignetted foveal conduits for noise suppression.
Strict rule: Zero em dashes across all code, comments, docstrings, and outputs.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
import math
import json


@dataclass
class CanvasEntity:
    """Represents a spatial canvas node or visual card."""
    entity_id: str
    label: str
    x: float
    y: float
    width: float = 120.0
    height: float = 60.0
    saliency_weight: float = 5.0
    is_active_focus: bool = False

    @property
    def center(self) -> Tuple[float, float]:
        """Calculates center point of entity."""
        return (self.x + self.width * 0.5, self.y + self.height * 0.5)


@dataclass
class FunnelConduit:
    """Represents the active foveal aperture and surrounding boundary gasket geometry."""
    center_x: float
    center_y: float
    foveal_radius: float
    gasket_radius: float
    focal_label: str = "Active Workspace"


@dataclass
class BoundaryLeakageMeasurement:
    """Telemetry measuring peripheral visual interference from a single entity."""
    entity_id: str
    label: str
    distance_px: float
    raw_saliency: float
    transparency_factor: float
    attenuated_saliency: float
    leakage_risk: str  # "contained", "parafoveal_leak", "peripheral_chatter"


@dataclass
class AttentionalFunnelTelemetry:
    """Aggregated metrics across the attentional funnel and boundary gasket."""
    total_entities: int
    active_entities_count: int
    peripheral_entities_count: int
    raw_leakage_index: float
    attenuated_leakage_index: float
    noise_suppression_pct: float
    gasket_status: str  # "optimal", "tightened", "diffuse"
    focal_center: Tuple[float, float]
    foveal_radius: float
    gasket_radius: float
    measurements: List[BoundaryLeakageMeasurement] = field(default_factory=list)


class AttentionalFunnelGasket:
    """
    Analyzes visual boundary leakage across dense spatial canvases and constructs
    adaptive vignetted foveal conduits to protect Cowan working memory bounds.
    """

    def __init__(self, foveal_radius: float = 180.0, gasket_radius: float = 380.0, min_transparency: float = 0.15):
        self.foveal_radius = max(20.0, float(foveal_radius))
        self.gasket_radius = max(self.foveal_radius + 20.0, float(gasket_radius))
        self.min_transparency = max(0.05, min(0.95, float(min_transparency)))

    def calculate_transparency(self, distance: float) -> float:
        """
        Computes the gasket transparency factor T(d) based on distance from focal center.
        Inside foveal radius: 1.0. Outside gasket radius: min_transparency.
        Between radii: smooth polynomial falloff.
        """
        if distance <= self.foveal_radius:
            return 1.0
        if distance >= self.gasket_radius:
            return self.min_transparency

        # Normalized position in gasket zone [0, 1]
        norm = (distance - self.foveal_radius) / (self.gasket_radius - self.foveal_radius)
        # Smoothstep falloff
        falloff = norm * norm * (3.0 - 2.0 * norm)
        return round(1.0 - (1.0 - self.min_transparency) * falloff, 3)

    def evaluate_canvas(
        self,
        entities: List[CanvasEntity],
        focal_entity_id: Optional[str] = None
    ) -> Tuple[AttentionalFunnelTelemetry, FunnelConduit]:
        """
        Evaluates peripheral visual leakage and generates attentional funnel telemetry.
        """
        if not entities:
            conduit = FunnelConduit(0.0, 0.0, self.foveal_radius, self.gasket_radius, "Empty")
            telemetry = AttentionalFunnelTelemetry(
                total_entities=0,
                active_entities_count=0,
                peripheral_entities_count=0,
                raw_leakage_index=0.0,
                attenuated_leakage_index=0.0,
                noise_suppression_pct=0.0,
                gasket_status="optimal",
                focal_center=(0.0, 0.0),
                foveal_radius=self.foveal_radius,
                gasket_radius=self.gasket_radius,
                measurements=[]
            )
            return telemetry, conduit

        # Determine focal center
        focal_entity = None
        if focal_entity_id:
            for e in entities:
                if e.entity_id == focal_entity_id:
                    focal_entity = e
                    break

        if not focal_entity:
            # Look for active focus flag
            actives = [e for e in entities if e.is_active_focus]
            if actives:
                focal_entity = actives[0]
            else:
                # Default to entity with highest saliency weight
                focal_entity = max(entities, key=lambda e: e.saliency_weight)

        cx, cy = focal_entity.center
        focal_entity.is_active_focus = True

        conduit = FunnelConduit(
            center_x=round(cx, 2),
            center_y=round(cy, 2),
            foveal_radius=self.foveal_radius,
            gasket_radius=self.gasket_radius,
            focal_label=focal_entity.label
        )

        measurements: List[BoundaryLeakageMeasurement] = []
        raw_leakage = 0.0
        attenuated_leakage = 0.0
        active_cnt = 0
        peripheral_cnt = 0

        for e in entities:
            ex, ey = e.center
            dx = ex - cx
            dy = ey - cy
            dist = math.sqrt(dx * dx + dy * dy)

            t_factor = self.calculate_transparency(dist)
            att_sal = e.saliency_weight * t_factor

            if dist <= self.foveal_radius:
                active_cnt += 1
                risk = "contained"
            elif dist <= self.gasket_radius:
                peripheral_cnt += 1
                raw_leakage += e.saliency_weight
                attenuated_leakage += att_sal
                risk = "parafoveal_leak"
            else:
                peripheral_cnt += 1
                raw_leakage += e.saliency_weight
                attenuated_leakage += att_sal
                risk = "peripheral_chatter"

            measurements.append(BoundaryLeakageMeasurement(
                entity_id=e.entity_id,
                label=e.label,
                distance_px=round(dist, 2),
                raw_saliency=round(e.saliency_weight, 2),
                transparency_factor=round(t_factor, 3),
                attenuated_saliency=round(att_sal, 2),
                leakage_risk=risk
            ))

        suppression_pct = 0.0
        if raw_leakage > 0.0:
            suppression_pct = max(0.0, ((raw_leakage - attenuated_leakage) / raw_leakage) * 100.0)

        # Gasket status classification
        if raw_leakage > 35.0:
            g_status = "tightened"
        elif raw_leakage < 15.0:
            g_status = "diffuse"
        else:
            g_status = "optimal"

        telemetry = AttentionalFunnelTelemetry(
            total_entities=len(entities),
            active_entities_count=active_cnt,
            peripheral_entities_count=peripheral_cnt,
            raw_leakage_index=round(raw_leakage, 2),
            attenuated_leakage_index=round(attenuated_leakage, 2),
            noise_suppression_pct=round(suppression_pct, 1),
            gasket_status=g_status,
            focal_center=(round(cx, 2), round(cy, 2)),
            foveal_radius=self.foveal_radius,
            gasket_radius=self.gasket_radius,
            measurements=measurements
        )

        return telemetry, conduit

    def generate_svg(
        self,
        telemetry: AttentionalFunnelTelemetry,
        conduit: FunnelConduit,
        entities: List[CanvasEntity],
        width: int = 920,
        height: int = 560
    ) -> str:
        """
        Renders a dark titanium SVG diagram visualizing the vignetted foveal aperture,
        the boundary gasket transition zone, and attenuated peripheral card chatter.
        """
        if not entities:
            return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <rect width="100%" height="100%" fill="#09090b"/>
  <text x="50%" y="50%" fill="#71717a" font-family="system-ui, sans-serif" font-size="14" text-anchor="middle">No entities to visualize</text>
</svg>'''

        min_x = min(e.x for e in entities)
        max_x = max(e.x + e.width for e in entities)
        min_y = min(e.y for e in entities)
        max_y = max(e.y + e.height for e in entities)

        pad = 60.0
        data_w = max(1.0, max_x - min_x)
        data_h = max(1.0, max_y - min_y)
        draw_w = float(width) - pad * 2.0
        draw_h = float(height) - pad * 2.0 - 50.0

        def sx(val: float) -> float:
            return pad + ((val - min_x) / data_w) * draw_w

        def sy(val: float) -> float:
            return 80.0 + ((val - min_y) / data_h) * draw_h

        fcx = sx(conduit.center_x)
        fcy = sy(conduit.center_y)
        scale_avg = (draw_w / data_w + draw_h / data_h) * 0.5
        rf_scaled = conduit.foveal_radius * scale_avg
        rg_scaled = conduit.gasket_radius * scale_avg

        m_map = {m.entity_id: m for m in telemetry.measurements}

        svg_parts: List[str] = [
            f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <defs>
    <radialGradient id="fovealAperture" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.18"/>
      <stop offset="70%" stop-color="#38bdf8" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#09090b" stop-opacity="0.75"/>
    </radialGradient>
    <radialGradient id="gasketVignette" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#09090b" stop-opacity="0.0"/>
      <stop offset="60%" stop-color="#09090b" stop-opacity="0.4"/>
      <stop offset="100%" stop-color="#09090b" stop-opacity="0.88"/>
    </radialGradient>
  </defs>

  <!-- Canvas Background -->
  <rect width="100%" height="100%" fill="#09090b" rx="14"/>
  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" fill="none" stroke="#27272a" stroke-width="1.5" rx="13"/>

  <!-- Header -->
  <text x="32" y="38" fill="#fafafa" font-family="system-ui, sans-serif" font-size="16" font-weight="700">Attentional Funnel and Saccadic Boundary Gasket</text>
  <text x="32" y="58" fill="#71717a" font-family="system-ui, sans-serif" font-size="12">Noise Suppression: {telemetry.noise_suppression_pct}% | Raw Leakage: {telemetry.raw_leakage_index} -> Attenuated: {telemetry.attenuated_leakage_index} | Status: {telemetry.gasket_status.upper()}</text>

  <!-- Legend -->
  <g transform="translate({width - 320}, 22)">
    <rect width="90" height="24" rx="6" fill="#18181b" stroke="#27272a"/>
    <circle cx="12" cy="12" r="4" fill="#38bdf8"/>
    <text x="22" y="16" fill="#a1a1aa" font-family="system-ui, sans-serif" font-size="10">Foveal Locus</text>

    <rect x="98" width="100" height="24" rx="6" fill="#18181b" stroke="#27272a"/>
    <circle cx="110" cy="12" r="4" fill="#10b981"/>
    <text x="120" y="16" fill="#a1a1aa" font-family="system-ui, sans-serif" font-size="10">Active Card</text>

    <rect x="206" width="100" height="24" rx="6" fill="#18181b" stroke="#27272a"/>
    <circle cx="218" cy="12" r="4" fill="#71717a"/>
    <text x="228" y="16" fill="#a1a1aa" font-family="system-ui, sans-serif" font-size="10">Gasketed</text>
  </g>

  <!-- Attentional Gasket Rings -->
  <circle cx="{fcx:.1f}" cy="{fcy:.1f}" r="{rg_scaled:.1f}" fill="none" stroke="#27272a" stroke-width="1.5" stroke-dasharray="4,4"/>
  <circle cx="{fcx:.1f}" cy="{fcy:.1f}" r="{rf_scaled:.1f}" fill="url(#fovealAperture)" stroke="#38bdf8" stroke-width="2"/>
'''
        ]

        # Draw entities
        for e in entities:
            m = m_map.get(e.entity_id)
            op = m.transparency_factor if m else 1.0
            x_pos = sx(e.x)
            y_pos = sy(e.y)
            w_box = max(20.0, (e.width / data_w) * draw_w)
            h_box = max(16.0, (e.height / data_h) * draw_h)

            stroke_col = "#38bdf8" if e.is_active_focus else ("#10b981" if op > 0.8 else "#71717a")
            fill_col = "#18181b"

            svg_parts.append(f'''  <!-- Entity: {e.label} -->
  <g opacity="{op:.2f}">
    <rect x="{x_pos:.1f}" y="{y_pos:.1f}" width="{w_box:.1f}" height="{h_box:.1f}" rx="6" fill="{fill_col}" stroke="{stroke_col}" stroke-width="1.5"/>
    <text x="{x_pos + 8:.1f}" y="{y_pos + 16:.1f}" fill="#fafafa" font-family="system-ui, sans-serif" font-size="10" font-weight="500">{e.label}</text>
  </g>''')

        svg_parts.append('</svg>')
        return "\n".join(svg_parts)

    def generate_markdown_report(self, telemetry: AttentionalFunnelTelemetry) -> str:
        """
        Synthesizes a publication-ready markdown compliance audit report.
        """
        lines: List[str] = [
            "# Attentional Funnel and Saccadic Boundary Gasket Audit",
            "",
            "## 1. Executive Telemetry Overview",
            f"- **Total Workspace Entities:** {telemetry.total_entities}",
            f"- **Active Foveal Entities:** {telemetry.active_entities_count}",
            f"- **Attenuated Peripheral Entities:** {telemetry.peripheral_entities_count}",
            f"- **Foveal Focus Aperture Radius:** {telemetry.foveal_radius} px",
            f"- **Boundary Gasket Perimeter Radius:** {telemetry.gasket_radius} px",
            f"- **Raw Boundary Leakage Index:** {telemetry.raw_leakage_index}",
            f"- **Attenuated Leakage Index:** {telemetry.attenuated_leakage_index}",
            f"- **Visual Noise Suppression:** {telemetry.noise_suppression_pct}%",
            f"- **Attentional Gasket Status:** {telemetry.gasket_status.upper()}",
            "",
            "## 2. Theoretical Grounding",
            "- **Bouma Law of Visual Crowding:** Peripheral clutter encroaches on foveal clarity when spacing is less than half eccentricity.",
            "- **Lavie Perceptual Load Theory:** High perceptual load requires selective boundary suppression to prevent attentional diversion.",
            "- **Cowan Capacity Bounds (N <= 4):** Restricting active foveal targets preserves working memory bandwidth for synthesis.",
            "",
            "## 3. Entity Leakage Telemetry Breakdown",
            "| Entity ID | Label | Distance (px) | Raw Saliency | Transparency | Attenuated Saliency | Leakage Risk |",
            "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |"
        ]

        for m in telemetry.measurements:
            lines.append(
                f"| `{m.entity_id}` | {m.label} | {m.distance_px} | {m.raw_saliency} | {m.transparency_factor} | {m.attenuated_saliency} | `{m.leakage_risk}` |"
            )

        lines.extend([
            "",
            "## 4. Operational Ergonomics Guidance",
            "- Entities flagged as Parafoveal Leak should be pushed outward or grouped into hierarchical sub-canvas portals.",
            "- When Raw Leakage exceeds 35.0, activate tightened gasket mode with steeper opacity falloff curves.",
            "- Maintain negative whitespace around focal cluster to preserve immediate foveal access."
        ])

        return "\n".join(lines)


def sample_canvas_entities() -> List[CanvasEntity]:
    """Generates an illustrative spatial canvas with active cluster and peripheral distractions."""
    return [
        # Active focal cluster (center ~ 300, 250)
        CanvasEntity("core-1", "Executive Core Model", 250.0, 220.0, width=140.0, height=60.0, saliency_weight=8.0, is_active_focus=True),
        CanvasEntity("core-2", "State Machine Harness", 220.0, 310.0, width=130.0, height=55.0, saliency_weight=6.5),
        CanvasEntity("core-3", "Telemetry Aggregator", 380.0, 230.0, width=135.0, height=55.0, saliency_weight=6.0),

        # Parafoveal entities (dist ~ 200 - 350)
        CanvasEntity("para-1", "Authentication Broker", 120.0, 100.0, width=120.0, height=50.0, saliency_weight=5.0),
        CanvasEntity("para-2", "Query Cache Index", 480.0, 400.0, width=125.0, height=50.0, saliency_weight=5.5),

        # Peripheral chatter (dist > 400)
        CanvasEntity("periph-1", "Legacy Log Collector", 750.0, 120.0, width=130.0, height=50.0, saliency_weight=4.0),
        CanvasEntity("periph-2", "Billing Stripe Webhook", 80.0, 520.0, width=130.0, height=50.0, saliency_weight=4.5),
        CanvasEntity("periph-3", "Email Notification Queue", 780.0, 480.0, width=140.0, height=50.0, saliency_weight=4.0),
    ]
