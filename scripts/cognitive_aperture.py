"""Autonomous Cognitive Spatial Dynamic Cognitive Aperture & Scope Bounding Harness.

Theoretical Foundation:
- Cowan's Working Memory Capacity Limit (The Magical Number 4 Chunks):
  Contemporary cognitive neuroscience demonstrates that human focal working memory
  is strictly bounded to 3-5 discrete active chunks (Cowan, 2001). Complex spatial
  canvases containing 15-30 unmanaged nodes saturate cognitive bandwidth, causing
  inattention, visual disorientation, and severe executive fatigue.
- Progressive Semantic Attenuation & Allocentric Mental Maps:
  Instead of hard-filtering or deleting peripheral context (which triggers spatial
  amnesia), dynamic cognitive aperture scaling dims non-focal nodes across concentric
  attenuation tiers. This preserves the global mental model without overloading
  the visuospatial sketchpad.
- Spatial Horizon Compass & Scope Bounding:
  Disentangles immediate tactical execution (runway tasks) from distant strategic
  ambitions, calculating a real-time Scope Drift Index to prevent cognitive sprawl.
- Spatial Canvas Lens & Dark Titanium SVG Export:
  Enriches Obsidian .canvas workspaces with focal aperture boundaries and generates
  publication-grade SVG concentric working memory radar visualizations.

Strict Quality Gate: Zero em dashes anywhere (use hyphens, commas, or parentheses).
"""

from __future__ import annotations

import enum
import json
import math
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


class ApertureTier(str, enum.Enum):
    """Concentric working memory attention tier for a spatial entity."""

    FOCAL = "focal"
    PERIPHERAL = "peripheral"
    HORIZON = "horizon"
    DORMANT = "dormant"


@dataclass
class SpatialEntity:
    """Cognitive entity situated within the spatial working memory field."""

    entity_id: str
    title: str
    description: str
    cognitive_weight: float  # 1.0 to 10.0 scale
    urgency_score: float  # 0.0 to 1.0
    strategic_alignment: float  # 0.0 to 1.0
    aperture_tier: ApertureTier = ApertureTier.PERIPHERAL
    attenuation_factor: float = 0.0  # 0.0 = full focus, 1.0 = maximum visual dimming
    aperture_rank: int = 0
    x: float = 0.0
    y: float = 0.0
    width: float = 280.0
    height: float = 160.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert entity to serializable dictionary."""
        return {
            "entity_id": self.entity_id,
            "title": self.title,
            "description": self.description,
            "cognitive_weight": round(self.cognitive_weight, 2),
            "urgency_score": round(self.urgency_score, 2),
            "strategic_alignment": round(self.strategic_alignment, 2),
            "aperture_tier": self.aperture_tier.value,
            "attenuation_factor": round(self.attenuation_factor, 2),
            "aperture_rank": self.aperture_rank,
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
        }


@dataclass
class ApertureTelemetry:
    """Telemetry metrics quantifying working memory load and scope bounding."""

    total_entities: int
    focal_count: int
    peripheral_count: int
    horizon_count: int
    dormant_count: int
    capacity_limit: int
    working_memory_strain_index: float
    scope_drift_index: float
    aperture_focus_efficiency_pct: float
    focal_entities: List[str] = field(default_factory=list)
    entities: List[SpatialEntity] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert telemetry to JSON-compatible dictionary."""
        return {
            "total_entities": self.total_entities,
            "focal_count": self.focal_count,
            "peripheral_count": self.peripheral_count,
            "horizon_count": self.horizon_count,
            "dormant_count": self.dormant_count,
            "capacity_limit": self.capacity_limit,
            "working_memory_strain_index": round(self.working_memory_strain_index, 3),
            "scope_drift_index": round(self.scope_drift_index, 3),
            "aperture_focus_efficiency_pct": round(self.aperture_focus_efficiency_pct, 1),
            "focal_entities": self.focal_entities,
            "entities": [e.to_dict() for e in self.entities],
        }


class CognitiveApertureHarness:
    """Engine calibrating dynamic cognitive aperture and semantic attenuation."""

    def __init__(
        self,
        capacity_limit: int = 4,
        max_peripheral_count: int = 6,
    ) -> None:
        self.capacity_limit = capacity_limit
        self.max_peripheral_count = max_peripheral_count
        self.entities: Dict[str, SpatialEntity] = {}
        self.raw_edges: List[Dict[str, Any]] = []

    def load_dict(self, entity_data: Dict[str, Any]) -> None:
        """Load entities from structured dictionary."""
        self.entities.clear()
        for e_id, info in entity_data.items():
            if isinstance(info, dict):
                title = info.get("title", e_id)
                desc = info.get("description", "")
                weight = float(info.get("cognitive_weight", 5.0))
                urgency = float(info.get("urgency_score", 0.5))
                strat = float(info.get("strategic_alignment", 0.5))
                x = float(info.get("x", 0.0))
                y = float(info.get("y", 0.0))
            else:
                title = str(info)
                desc = ""
                weight = 5.0
                urgency = 0.5
                strat = 0.5
                x = 0.0
                y = 0.0

            self.entities[e_id] = SpatialEntity(
                entity_id=e_id,
                title=title,
                description=desc,
                cognitive_weight=max(1.0, min(10.0, weight)),
                urgency_score=max(0.0, min(1.0, urgency)),
                strategic_alignment=max(0.0, min(1.0, strat)),
                x=x,
                y=y,
            )

    def load_canvas(self, canvas_data: Dict[str, Any]) -> None:
        """Extract spatial nodes and positions from an Obsidian .canvas structure."""
        self.entities.clear()
        self.raw_edges = list(canvas_data.get("edges", []))
        nodes = canvas_data.get("nodes", [])

        for node in nodes:
            n_id = str(node.get("id", ""))
            text = str(node.get("text", "")).strip()
            lines = [l.strip() for l in text.split("\n") if l.strip()]
            title = lines[0].lstrip("#").strip() if lines else n_id
            desc = "\n".join(lines[1:]) if len(lines) > 1 else ""

            # Infer weights and urgency from keywords or tags
            weight = 5.0
            urgency = 0.5
            strat = 0.5

            if "#urgent" in text or "urgent" in text.lower() or "critical" in text.lower():
                urgency = 0.9
            if "#strategic" in text or "architecture" in text.lower() or "milestone" in text.lower():
                strat = 0.9
            if "#heavy" in text or len(text) > 200:
                weight = 8.0
            elif len(text) < 50:
                weight = 3.0

            self.entities[n_id] = SpatialEntity(
                entity_id=n_id,
                title=title,
                description=desc,
                cognitive_weight=weight,
                urgency_score=urgency,
                strategic_alignment=strat,
                x=float(node.get("x", 0.0)),
                y=float(node.get("y", 0.0)),
                width=float(node.get("width", 280.0)),
                height=float(node.get("height", 160.0)),
            )

    def calibrate_aperture(
        self,
        manual_focal_ids: Optional[List[str]] = None,
    ) -> Tuple[List[SpatialEntity], ApertureTelemetry]:
        """Calibrate cognitive aperture rings and compute semantic attenuation factors."""
        if not self.entities:
            empty_telemetry = ApertureTelemetry(
                total_entities=0,
                focal_count=0,
                peripheral_count=0,
                horizon_count=0,
                dormant_count=0,
                capacity_limit=self.capacity_limit,
                working_memory_strain_index=0.0,
                scope_drift_index=0.0,
                aperture_focus_efficiency_pct=100.0,
            )
            return [], empty_telemetry

        # Calculate composite tactical salience
        # Prioritizes immediate execution while honoring strategic anchors
        scored_items: List[Tuple[float, SpatialEntity]] = []
        for e in self.entities.values():
            if manual_focal_ids and e.entity_id in manual_focal_ids:
                score = 999.0  # Force focal inclusion
            else:
                score = (e.urgency_score * 0.55) + ((e.cognitive_weight / 10.0) * 0.25) + (e.strategic_alignment * 0.20)
            scored_items.append((score, e))

        # Sort descending by priority score
        scored_items.sort(key=lambda item: item[0], reverse=True)

        focal_entities: List[str] = []
        focal_count = 0
        peripheral_count = 0
        horizon_count = 0
        dormant_count = 0

        for rank, (score, entity) in enumerate(scored_items, 1):
            entity.aperture_rank = rank
            if rank <= self.capacity_limit:
                entity.aperture_tier = ApertureTier.FOCAL
                entity.attenuation_factor = 0.0  # zero attenuation (crisp focus)
                focal_entities.append(entity.entity_id)
                focal_count += 1
            elif rank <= (self.capacity_limit + self.max_peripheral_count):
                if entity.strategic_alignment >= 0.75 and entity.urgency_score < 0.4:
                    entity.aperture_tier = ApertureTier.HORIZON
                    entity.attenuation_factor = 0.45  # subtle dimming, distinct landmark
                    horizon_count += 1
                else:
                    entity.aperture_tier = ApertureTier.PERIPHERAL
                    # Progressive attenuation gradient (0.35 to 0.65)
                    step = (rank - self.capacity_limit) / float(self.max_peripheral_count)
                    entity.attenuation_factor = 0.35 + (step * 0.30)
                    peripheral_count += 1
            else:
                if entity.strategic_alignment >= 0.8:
                    entity.aperture_tier = ApertureTier.HORIZON
                    entity.attenuation_factor = 0.50
                    horizon_count += 1
                else:
                    entity.aperture_tier = ApertureTier.DORMANT
                    entity.attenuation_factor = 0.85  # heavy attenuation
                    dormant_count += 1

        # Working Memory Strain Index
        # Evaluates load vs Cowan's 4-chunk threshold
        unbounded_active = focal_count + (peripheral_count * 0.35)
        raw_strain = max(0.0, (unbounded_active - self.capacity_limit) / float(self.capacity_limit))
        strain_index = min(1.0, raw_strain)

        # Scope Drift Index: measures high-urgency or high-weight items pushed outside focal aperture
        outside_focal = [e for e in self.entities.values() if e.aperture_tier != ApertureTier.FOCAL]
        if outside_focal:
            drift_numerator = sum(e.urgency_score for e in outside_focal)
            drift_index = min(1.0, drift_numerator / float(len(outside_focal)))
        else:
            drift_index = 0.0

        focus_efficiency = max(0.0, (1.0 - (strain_index * 0.5 + drift_index * 0.5))) * 100.0

        telemetry = ApertureTelemetry(
            total_entities=len(self.entities),
            focal_count=focal_count,
            peripheral_count=peripheral_count,
            horizon_count=horizon_count,
            dormant_count=dormant_count,
            capacity_limit=self.capacity_limit,
            working_memory_strain_index=strain_index,
            scope_drift_index=drift_index,
            aperture_focus_efficiency_pct=focus_efficiency,
            focal_entities=focal_entities,
            entities=list(self.entities.values()),
        )

        return list(self.entities.values()), telemetry

    def to_canvas(
        self,
        output_path: Optional[str] = None,
        canvas_title: str = "Bounded Cognitive Aperture",
    ) -> Dict[str, Any]:
        """Export aperture-scaled entities to Obsidian .canvas format with visual tier tags."""
        entities_list, telemetry = self.calibrate_aperture()

        canvas_nodes: List[Dict[str, Any]] = []

        for e in entities_list:
            # Color assignment: 4 (green) for focal, 2 (orange) for peripheral, 6 (purple) for horizon, 1 (dimmed red) for dormant
            if e.aperture_tier == ApertureTier.FOCAL:
                color = "4"
                tier_badge = f"[IN-APERTURE FOCAL #{e.aperture_rank}/{telemetry.capacity_limit}]"
            elif e.aperture_tier == ApertureTier.PERIPHERAL:
                color = "2"
                tier_badge = f"[PERIPHERAL ATTENUATED: {e.attenuation_factor:.0%}]"
            elif e.aperture_tier == ApertureTier.HORIZON:
                color = "6"
                tier_badge = f"[STRATEGIC HORIZON ANCHOR]"
            else:
                color = "1"
                tier_badge = f"[DORMANT STOWED: {e.attenuation_factor:.0%}]"

            content = (
                f"### {e.title}\n"
                f"**Aperture:** `{tier_badge}`\n"
                f"**Metrics:** Weight: {e.cognitive_weight}/10 | Urgency: {e.urgency_score:.0%} | Strategic: {e.strategic_alignment:.0%}\n\n"
                f"{e.description}"
            )

            canvas_nodes.append({
                "id": e.entity_id,
                "x": e.x,
                "y": e.y,
                "width": e.width,
                "height": e.height,
                "type": "text",
                "text": content,
                "color": color,
            })

        canvas_json = {
            "title": canvas_title,
            "nodes": canvas_nodes,
            "edges": self.raw_edges,
        }

        if output_path:
            p = Path(output_path)
            p.parent.mkdir(parents=True, exist_ok=True)
            with open(p, "w", encoding="utf-8") as f:
                json.dump(canvas_json, f, indent=2)

        return canvas_json

    def to_svg(
        self,
        output_path: Optional[str] = None,
        width: int = 1200,
        height: int = 800,
    ) -> str:
        """Render publication-grade SVG concentric cognitive aperture radar diagram."""
        entities_list, telemetry = self.calibrate_aperture()

        cx = width / 2.0 - 100.0
        cy = height / 2.0 + 30.0

        r_focal = 160.0
        r_peripheral = 270.0
        r_horizon = 360.0

        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
            f'width="{width}" height="{height}" style="background-color: #0B0F17; '
            f'font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif;">',
            '<defs>',
            '  <radialGradient id="focalGlow" cx="50%" cy="50%" r="50%">',
            '    <stop offset="0%" stop-color="#10B981" stop-opacity="0.25"/>',
            '    <stop offset="100%" stop-color="#10B981" stop-opacity="0.0"/>',
            '  </radialGradient>',
            '  <filter id="cardShadow" x="-15%" y="-15%" width="130%" height="130%">',
            '    <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#000000" flood-opacity="0.6"/>',
            '  </filter>',
            '</defs>',
            '<!-- Header -->',
            f'<text x="60" y="45" font-size="20" font-weight="700" fill="#F8FAFC">Dynamic Cognitive Aperture &amp; Scope Bounding Radar</text>',
            f'<text x="60" y="65" font-size="12" fill="#94A3B8">Cowan 4-Slot Boundary: {telemetry.focal_count}/{telemetry.capacity_limit} Focal | {telemetry.peripheral_count} Attenuated | {telemetry.horizon_count} Strategic Anchors</text>',
            '<!-- Concentric Working Memory Rings -->',
            # Horizon Ring
            f'<circle cx="{cx}" cy="{cy}" r="{r_horizon}" fill="none" stroke="#334155" stroke-width="1.5" stroke-dasharray="6,6"/>',
            f'<text x="{cx + r_horizon - 10}" y="{cy - 8}" font-size="10" font-weight="600" fill="#64748B" text-anchor="end">Strategic Horizon Ring</text>',
            # Peripheral Ring
            f'<circle cx="{cx}" cy="{cy}" r="{r_peripheral}" fill="none" stroke="#F59E0B" stroke-width="1.5" stroke-dasharray="4,4" stroke-opacity="0.6"/>',
            f'<text x="{cx + r_peripheral - 10}" y="{cy - 8}" font-size="10" font-weight="600" fill="#D97706" text-anchor="end">Peripheral Attenuation Ring</text>',
            # Focal Ring
            f'<circle cx="{cx}" cy="{cy}" r="{r_focal}" fill="url(#focalGlow)" stroke="#10B981" stroke-width="2.5"/>',
            f'<text x="{cx + r_focal - 10}" y="{cy - 8}" font-size="10" font-weight="700" fill="#10B981" text-anchor="end">Focal Aperture (Cowan Limit: {telemetry.capacity_limit})</text>',
            '<!-- Entity Nodes -->',
        ]

        # Place entities radially by tier
        focal_nodes = [e for e in entities_list if e.aperture_tier == ApertureTier.FOCAL]
        peripheral_nodes = [e for e in entities_list if e.aperture_tier == ApertureTier.PERIPHERAL]
        horizon_nodes = [e for e in entities_list if e.aperture_tier == ApertureTier.HORIZON]

        # Draw focal nodes inside inner circle
        for idx, node in enumerate(focal_nodes):
            angle = (2.0 * math.pi / max(1, len(focal_nodes))) * idx - (math.pi / 2.0)
            dist = r_focal * 0.55
            nx = cx + math.cos(angle) * dist
            ny = cy + math.sin(angle) * dist

            svg_parts.append(
                f'<g transform="translate({nx - 60}, {ny - 25})" filter="url(#cardShadow)">'
                f'  <rect width="120" height="50" rx="6" fill="#064E3B" stroke="#10B981" stroke-width="2"/>'
                f'  <text x="60" y="20" font-size="10" font-weight="700" fill="#ECFDF5" text-anchor="middle">{node.title[:14]}</text>'
                f'  <text x="60" y="36" font-size="9" fill="#A7F3D0" text-anchor="middle">Rank #{node.aperture_rank} [FOCAL]</text>'
                f'</g>'
            )

        # Draw peripheral nodes in middle band
        for idx, node in enumerate(peripheral_nodes):
            angle = (2.0 * math.pi / max(1, len(peripheral_nodes))) * idx
            dist = (r_focal + r_peripheral) / 2.0
            nx = cx + math.cos(angle) * dist
            ny = cy + math.sin(angle) * dist
            opacity = 1.0 - node.attenuation_factor

            svg_parts.append(
                f'<g transform="translate({nx - 55}, {ny - 22})" opacity="{opacity:.2f}">'
                f'  <rect width="110" height="44" rx="6" fill="#1E293B" stroke="#F59E0B" stroke-width="1.5"/>'
                f'  <text x="55" y="18" font-size="10" font-weight="600" fill="#FDE68A" text-anchor="middle">{node.title[:13]}</text>'
                f'  <text x="55" y="32" font-size="8" fill="#94A3B8" text-anchor="middle">Atten: {node.attenuation_factor:.0%}</text>'
                f'</g>'
            )

        # Draw horizon anchors in outer band
        for idx, node in enumerate(horizon_nodes):
            angle = (2.0 * math.pi / max(1, len(horizon_nodes))) * idx + 0.35
            dist = (r_peripheral + r_horizon) / 2.0
            nx = cx + math.cos(angle) * dist
            ny = cy + math.sin(angle) * dist

            svg_parts.append(
                f'<g transform="translate({nx - 55}, {ny - 22})">'
                f'  <rect width="110" height="44" rx="6" fill="#2E1065" stroke="#A855F7" stroke-width="1.5"/>'
                f'  <text x="55" y="18" font-size="10" font-weight="600" fill="#E9D5FF" text-anchor="middle">{node.title[:13]}</text>'
                f'  <text x="55" y="32" font-size="8" fill="#C084FC" text-anchor="middle">Strategic Landmark</text>'
                f'</g>'
            )

        # Telemetry Legend
        legend_x = width - 260
        legend_y = height - 145
        svg_parts.append('<!-- Telemetry Legend -->')
        svg_parts.append(
            f'<rect x="{legend_x}" y="{legend_y}" width="230" height="115" rx="6" '
            f'fill="#0F172A" stroke="#1E293B" stroke-width="1"/>'
        )
        svg_parts.append(
            f'<text x="{legend_x + 12}" y="{legend_y + 22}" font-size="11" font-weight="700" fill="#F8FAFC">Aperture Scaffolding Metrics</text>'
        )
        svg_parts.append(
            f'<text x="{legend_x + 12}" y="{legend_y + 42}" font-size="10" fill="#64748B">WM Strain Index: <tspan fill="{"#EF4444" if telemetry.working_memory_strain_index > 0.4 else "#10B981"}">{telemetry.working_memory_strain_index:.2f}</tspan></text>'
        )
        svg_parts.append(
            f'<text x="{legend_x + 12}" y="{legend_y + 60}" font-size="10" fill="#64748B">Scope Drift Index: <tspan fill="#F59E0B">{telemetry.scope_drift_index:.2f}</tspan></text>'
        )
        svg_parts.append(
            f'<text x="{legend_x + 12}" y="{legend_y + 78}" font-size="10" fill="#64748B">Focus Efficiency: <tspan fill="#38BDF8">{telemetry.aperture_focus_efficiency_pct:.1f}%</tspan></text>'
        )
        svg_parts.append(
            f'<text x="{legend_x + 12}" y="{legend_y + 98}" font-size="9" fill="#475569">Cowan 4-Slot Working Memory Bounds</text>'
        )

        svg_parts.append('</svg>')
        svg_content = "\n".join(svg_parts)

        if output_path:
            p = Path(output_path)
            p.parent.mkdir(parents=True, exist_ok=True)
            with open(p, "w", encoding="utf-8") as f:
                f.write(svg_content)

        return svg_content

    def render_ascii_lens(self, telemetry: ApertureTelemetry) -> str:
        """Format an accessible ASCII aperture lens report for the terminal."""
        lines = [
            "=" * 68,
            "  Dynamic Cognitive Aperture & Scope Bounding Lens",
            "=" * 68,
            f"  Total Entities:             {telemetry.total_entities}",
            f"  Focal Aperture Slots:       {telemetry.focal_count} / {telemetry.capacity_limit} (Cowan Limit)",
            f"  Peripheral Attenuated:      {telemetry.peripheral_count}",
            f"  Strategic Horizon Anchors:  {telemetry.horizon_count}",
            f"  Dormant Stowed:             {telemetry.dormant_count}",
            f"  Working Memory Strain:      {telemetry.working_memory_strain_index:.2f} (0.0 = relaxed, 1.0 = saturated)",
            f"  Scope Drift Index:          {telemetry.scope_drift_index:.2f}",
            f"  Focus Efficiency:           {telemetry.aperture_focus_efficiency_pct:.1f}%",
            "-" * 68,
            "  [ACTIVE COGNITIVE APERTURE (FOCAL INTAKE)]:",
        ]

        focal_nodes = [e for e in telemetry.entities if e.aperture_tier == ApertureTier.FOCAL]
        for node in focal_nodes:
            lines.append(f"    #{node.aperture_rank} [FOCAL] {node.title} (Weight: {node.cognitive_weight}/10, Urgency: {node.urgency_score:.0%})")

        peripheral_nodes = [e for e in telemetry.entities if e.aperture_tier == ApertureTier.PERIPHERAL]
        if peripheral_nodes:
            lines.append("-" * 68)
            lines.append("  [PERIPHERAL ATTENUATED ZONE]:")
            for node in peripheral_nodes[:4]:
                lines.append(f"    #{node.aperture_rank} [PERIPHERAL -{node.attenuation_factor:.0%}] {node.title}")

        horizon_nodes = [e for e in telemetry.entities if e.aperture_tier == ApertureTier.HORIZON]
        if horizon_nodes:
            lines.append("-" * 68)
            lines.append("  [STRATEGIC HORIZON ANCHORS]:")
            for node in horizon_nodes[:3]:
                lines.append(f"    * [HORIZON LANDMARK] {node.title} (Strategic: {node.strategic_alignment:.0%})")

        lines.append("=" * 68)
        return "\n".join(lines)
