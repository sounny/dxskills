"""Autonomous Cognitive Spatial Schema Morphing & Cross-Scale Projection Engine.

Theoretical Foundation:
- Eide & Eide M-I-N-D Framework (Material & Interconnected Reasoning):
  Dyslexic cognition excels at grasping overarching holistic system topologies (macro plane),
  yet navigating across abstraction layers down to component interactions (meso plane)
  and code contracts (micro plane) frequently triggers working memory overload and loss
  of global context.
- O'Keefe & Nadel Allocentric Coordinate Invariant Tracking:
  Unlike egocentric eye-centered coordinates that distort during zoom transformations,
  allocentric representations anchor spatial orientation relative to persistent structural
  landmarks (barycenters). The engine tracks invariant coordinates across zoom scales to
  eliminate cognitive disorientation.
- Triadic Abstraction Planes:
  - MACRO_TOPOLOGY: Strategic architecture, domain boundaries, and conceptual invariants.
  - MESO_INTERACTION: Service interfaces, state channels, and operational conduits.
  - MICRO_SPECIFICATION: Precise method signatures, parameters, and AST type contracts.
- Dark Titanium SVG & Obsidian .canvas Export:
  Generates production-grade Obsidian .canvas files with layered abstraction frames
  and dark titanium SVG diagrams featuring multi-scale concentric projection fields.

Strict Quality Gate: Zero em dashes anywhere (use hyphens, commas, or parentheses).
"""

from __future__ import annotations

import enum
import json
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


class AbstractionPlane(str, enum.Enum):
    """Hierarchical abstraction tiers for multi-scale schema projection."""

    MACRO_TOPOLOGY = "macro_topology"
    MESO_INTERACTION = "meso_interaction"
    MICRO_SPECIFICATION = "micro_specification"


@dataclass
class ProjectedEntity:
    """Represents a spatial schema node projected across multi-scale abstraction planes."""

    entity_id: str
    title: str
    plane: AbstractionPlane
    allocentric_x: float
    allocentric_y: float
    zoom_scale_factor: float
    invariant_anchor_key: str
    semantic_summary: str
    details: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert projected entity to serializable dictionary."""
        return {
            "entity_id": self.entity_id,
            "title": self.title,
            "plane": self.plane.value,
            "allocentric_x": round(self.allocentric_x, 1),
            "allocentric_y": round(self.allocentric_y, 1),
            "zoom_scale_factor": round(self.zoom_scale_factor, 2),
            "invariant_anchor_key": self.invariant_anchor_key,
            "semantic_summary": self.semantic_summary,
            "details": self.details,
        }


@dataclass
class CrossScaleProjectionTelemetry:
    """Telemetry tracking spatial schema transformations and allocentric stability."""

    total_entities: int
    macro_count: int
    meso_count: int
    micro_count: int
    allocentric_drift_variance: float
    cross_scale_coherence_pct: float
    entities: List[ProjectedEntity] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert telemetry to JSON-compatible dictionary."""
        return {
            "total_entities": self.total_entities,
            "macro_count": self.macro_count,
            "meso_count": self.meso_count,
            "micro_count": self.micro_count,
            "allocentric_drift_variance": round(self.allocentric_drift_variance, 3),
            "cross_scale_coherence_pct": round(self.cross_scale_coherence_pct, 1),
            "entities": [e.to_dict() for e in self.entities],
        }


class SchemaCrossScaleProjector:
    """Projects spatial schemas across macro, meso, and micro planes while tracking allocentric invariants."""

    def __init__(
        self,
        macro_spread_factor: float = 1.0,
        meso_spread_factor: float = 1.5,
        micro_spread_factor: float = 2.2,
    ) -> None:
        self.macro_spread_factor = macro_spread_factor
        self.meso_spread_factor = meso_spread_factor
        self.micro_spread_factor = micro_spread_factor
        self.raw_entities: Dict[str, Dict[str, Any]] = {}
        self.raw_canvas_edges: List[Dict[str, Any]] = []

    def load_dict(self, data: Dict[str, Any]) -> None:
        """Load schema specifications from dictionary."""
        self.raw_entities.clear()
        self.raw_canvas_edges.clear()

        raw_nodes = data.get("nodes", data)
        for n_id, info in raw_nodes.items():
            if isinstance(info, dict):
                title = str(info.get("title", n_id))
                text = str(info.get("text", title))
                plane_str = str(info.get("plane", "")).lower()
                x = float(info.get("x", 0.0))
                y = float(info.get("y", 0.0))
                details = list(info.get("details", []))
            else:
                title = str(info)
                text = str(info)
                plane_str = ""
                x, y = 0.0, 0.0
                details = []

            # Infer plane if not explicitly provided
            if "micro" in plane_str or "function" in text.lower() or "ast" in text.lower():
                plane = AbstractionPlane.MICRO_SPECIFICATION
            elif "meso" in plane_str or "service" in text.lower() or "broker" in text.lower():
                plane = AbstractionPlane.MESO_INTERACTION
            else:
                plane = AbstractionPlane.MACRO_TOPOLOGY

            self.raw_entities[n_id] = {
                "id": n_id,
                "title": title,
                "text": text,
                "plane": plane,
                "x": x,
                "y": y,
                "details": details,
            }

        if "edges" in data and isinstance(data["edges"], list):
            self.raw_canvas_edges = list(data["edges"])

    def load_canvas(self, canvas_data: Dict[str, Any]) -> None:
        """Extract schema entities and planes from Obsidian .canvas format."""
        self.raw_entities.clear()
        self.raw_canvas_edges = list(canvas_data.get("edges", []))

        raw_nodes = canvas_data.get("nodes", [])
        for node in raw_nodes:
            n_id = str(node.get("id", ""))
            text = str(node.get("text", "")).strip()
            lines = [l.strip() for l in text.split("\n") if l.strip()]
            title = lines[0].lstrip("#").strip() if lines else n_id

            lower_text = text.lower()
            if "micro" in lower_text or "class" in lower_text or "def " in lower_text:
                plane = AbstractionPlane.MICRO_SPECIFICATION
            elif "meso" in lower_text or "api" in lower_text or "channel" in lower_text:
                plane = AbstractionPlane.MESO_INTERACTION
            else:
                plane = AbstractionPlane.MACRO_TOPOLOGY

            self.raw_entities[n_id] = {
                "id": n_id,
                "title": title,
                "text": text,
                "plane": plane,
                "x": float(node.get("x", 0.0)),
                "y": float(node.get("y", 0.0)),
                "details": lines[1:] if len(lines) > 1 else [],
            }

    def project_schema(self) -> Tuple[List[ProjectedEntity], CrossScaleProjectionTelemetry]:
        """Project entities into multi-scale allocentric coordinates and compute stability telemetry."""
        if not self.raw_entities:
            empty_telemetry = CrossScaleProjectionTelemetry(
                total_entities=0,
                macro_count=0,
                meso_count=0,
                micro_count=0,
                allocentric_drift_variance=0.0,
                cross_scale_coherence_pct=0.0,
            )
            return [], empty_telemetry

        # Compute global barycenter of input entities to establish allocentric reference point
        mean_x = sum(e["x"] for e in self.raw_entities.values()) / len(self.raw_entities)
        mean_y = sum(e["y"] for e in self.raw_entities.values()) / len(self.raw_entities)

        projected: List[ProjectedEntity] = []
        macro_c, meso_c, micro_c = 0, 0, 0
        drift_squared_sum = 0.0

        for n_id, data in self.raw_entities.items():
            plane = data["plane"]
            rel_x = data["x"] - mean_x
            rel_y = data["y"] - mean_y

            if plane == AbstractionPlane.MACRO_TOPOLOGY:
                scale_factor = 0.60
                spread = self.macro_spread_factor
                macro_c += 1
            elif plane == AbstractionPlane.MESO_INTERACTION:
                scale_factor = 1.00
                spread = self.meso_spread_factor
                meso_c += 1
            else:
                scale_factor = 1.60
                spread = self.micro_spread_factor
                micro_c += 1

            # Transform allocentric coordinates relative to invariant barycenter
            alloc_x = mean_x + rel_x * spread
            alloc_y = mean_y + rel_y * spread

            # Drift calculation: normalized offset variance relative to pure scaling
            drift = math.hypot(alloc_x - data["x"], alloc_y - data["y"]) / max(100.0, math.hypot(rel_x, rel_y) + 1.0)
            drift_squared_sum += drift * drift

            invariant_key = f"inv_{n_id[:6]}_{plane.value[:3]}"
            summary_snippet = data["text"][:75] + ("..." if len(data["text"]) > 75 else "")

            projected.append(
                ProjectedEntity(
                    entity_id=n_id,
                    title=data["title"],
                    plane=plane,
                    allocentric_x=alloc_x,
                    allocentric_y=alloc_y,
                    zoom_scale_factor=scale_factor,
                    invariant_anchor_key=invariant_key,
                    semantic_summary=summary_snippet,
                    details=data["details"][:3],
                )
            )

        total = len(projected)
        drift_variance = (drift_squared_sum / total) if total > 0 else 0.0
        # Coherence score: high stability yields 85-98% coherence
        coherence = max(60.0, min(99.0, 100.0 - drift_variance * 8.0))

        telemetry = CrossScaleProjectionTelemetry(
            total_entities=total,
            macro_count=macro_c,
            meso_count=meso_c,
            micro_count=micro_c,
            allocentric_drift_variance=drift_variance,
            cross_scale_coherence_pct=coherence,
            entities=projected,
        )

        return projected, telemetry

    def to_canvas(
        self,
        output_path: Optional[str] = None,
        canvas_title: str = "Multi-Scale Schema Canvas",
    ) -> Dict[str, Any]:
        """Export projected entities and multi-scale visual frames to Obsidian .canvas."""
        projected, telemetry = self.project_schema()

        canvas_nodes: List[Dict[str, Any]] = []

        # Create multi-scale section frames/groups
        planes = [
            (AbstractionPlane.MACRO_TOPOLOGY, "Macro Strategic Topology", "4", -300),
            (AbstractionPlane.MESO_INTERACTION, "Meso Component Interactors", "5", 200),
            (AbstractionPlane.MICRO_SPECIFICATION, "Micro Technical AST Contracts", "6", 750),
        ]

        for p_type, p_label, p_color, y_offset in planes:
            matching = [e for e in projected if e.plane == p_type]
            if matching:
                min_x = min(e.allocentric_x for e in matching) - 40
                max_x = max(e.allocentric_x for e in matching) + 300
                min_y = min(e.allocentric_y for e in matching) - 40
                max_y = max(e.allocentric_y for e in matching) + 200

                canvas_nodes.append({
                    "id": f"group_{p_type.value}",
                    "type": "group",
                    "label": p_label,
                    "x": min_x,
                    "y": min_y,
                    "width": max(360, max_x - min_x),
                    "height": max(260, max_y - min_y),
                    "color": p_color,
                })

        # Add projected entity cards
        for entity in projected:
            detail_str = "\n".join(f"- {d}" for d in entity.details) if entity.details else ""
            card_text = f"### [{entity.plane.value.upper()}] {entity.title}\n{entity.semantic_summary}\n{detail_str}"
            canvas_nodes.append({
                "id": entity.entity_id,
                "type": "text",
                "text": card_text,
                "x": entity.allocentric_x,
                "y": entity.allocentric_y,
                "width": 260.0 * entity.zoom_scale_factor,
                "height": 140.0 * entity.zoom_scale_factor,
            })

        canvas_json = {
            "title": canvas_title,
            "nodes": canvas_nodes,
            "edges": list(self.raw_canvas_edges),
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
        """Render publication-grade SVG multi-scale projection field in dark titanium theme."""
        projected, telemetry = self.project_schema()

        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
            f'width="{width}" height="{height}" style="background-color: #0B0F17; '
            f'font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif;">',
            '<defs>',
            '  <filter id="planeShadow" x="-10%" y="-10%" width="120%" height="120%">',
            '    <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#000000" flood-opacity="0.6"/>',
            '  </filter>',
            '</defs>',
            '<!-- Header -->',
            f'<text x="60" y="45" font-size="20" font-weight="700" fill="#F8FAFC">Spatial Schema Morphing &amp; Cross-Scale Projection Engine</text>',
            f'<text x="60" y="65" font-size="12" fill="#94A3B8">Entities: {telemetry.total_entities} (Macro: {telemetry.macro_count}, Meso: {telemetry.meso_count}, Micro: {telemetry.micro_count}) | Coherence: {telemetry.cross_scale_coherence_pct:.1f}% | Allocentric Drift: {telemetry.allocentric_drift_variance:.3f}</text>',
            '<!-- Concentric Multi-Scale Guidance Grid -->',
            f'<circle cx="{width / 2:.1f}" cy="{height / 2:.1f}" r="340" fill="none" stroke="#1E293B" stroke-width="1" stroke-dasharray="6,6"/>',
            f'<circle cx="{width / 2:.1f}" cy="{height / 2:.1f}" r="220" fill="none" stroke="#334155" stroke-width="1" stroke-dasharray="4,4"/>',
            f'<circle cx="{width / 2:.1f}" cy="{height / 2:.1f}" r="110" fill="none" stroke="#475569" stroke-width="1"/>',
            f'<text x="{width / 2 + 115:.1f}" y="{height / 2 - 8:.1f}" font-size="9" fill="#64748B">Macro Zone</text>',
            f'<text x="{width / 2 + 225:.1f}" y="{height / 2 - 8:.1f}" font-size="9" fill="#64748B">Meso Zone</text>',
            f'<text x="{width / 2 + 345:.1f}" y="{height / 2 - 8:.1f}" font-size="9" fill="#64748B">Micro Zone</text>',
            '<!-- Projected Entity Cards -->',
        ]

        for e in projected:
            if e.plane == AbstractionPlane.MACRO_TOPOLOGY:
                stroke_col = "#10B981"  # Emerald
                badge_bg = "#064E3B"
            elif e.plane == AbstractionPlane.MESO_INTERACTION:
                stroke_col = "#38BDF8"  # Cyan
                badge_bg = "#0C4A6E"
            else:
                stroke_col = "#C084FC"  # Purple
                badge_bg = "#581C87"

            w = 220.0 * e.zoom_scale_factor
            h = 100.0 * e.zoom_scale_factor

            svg_parts.append(
                f'<g transform="translate({e.allocentric_x:.1f}, {e.allocentric_y:.1f})" filter="url(#planeShadow)">'
                f'  <rect width="{w:.1f}" height="{h:.1f}" rx="8" fill="#1E293B" stroke="{stroke_col}" stroke-width="1.5"/>'
                f'  <rect x="10" y="10" width="75" height="16" rx="4" fill="{badge_bg}"/>'
                f'  <text x="47" y="21" font-size="8" font-weight="700" fill="#F8FAFC" text-anchor="middle">{e.plane.value[:5].upper()}</text>'
                f'  <text x="10" y="{38 + h * 0.1:.1f}" font-size="11" font-weight="700" fill="#F8FAFC">{e.title[:18]}</text>'
                f'  <text x="10" y="{54 + h * 0.1:.1f}" font-size="9" fill="#94A3B8">Invariant: {e.invariant_anchor_key}</text>'
                f'  <text x="10" y="{68 + h * 0.1:.1f}" font-size="8" fill="#64748B">Zoom Scale: {e.zoom_scale_factor:.1f}x</text>'
                f'</g>'
            )

        # Telemetry Legend
        legend_x = width - 260
        legend_y = height - 150
        svg_parts.append('<!-- Telemetry Legend -->')
        svg_parts.append(
            f'<rect x="{legend_x}" y="{legend_y}" width="230" height="120" rx="6" '
            f'fill="#0F172A" stroke="#1E293B" stroke-width="1"/>'
        )
        svg_parts.append(
            f'<text x="{legend_x + 12}" y="{legend_y + 22}" font-size="11" font-weight="700" fill="#F8FAFC">Cross-Scale Metrics</text>'
        )
        svg_parts.append(
            f'<text x="{legend_x + 12}" y="{legend_y + 42}" font-size="10" fill="#64748B">Cross-Scale Coherence: <tspan fill="#10B981">{telemetry.cross_scale_coherence_pct:.1f}%</tspan></text>'
        )
        svg_parts.append(
            f'<text x="{legend_x + 12}" y="{legend_y + 60}" font-size="10" fill="#64748B">Allocentric Drift: <tspan fill="#38BDF8">{telemetry.allocentric_drift_variance:.3f}</tspan></text>'
        )
        svg_parts.append(
            f'<text x="{legend_x + 12}" y="{legend_y + 78}" font-size="10" fill="#64748B">Macro/Meso/Micro: <tspan fill="#F59E0B">{telemetry.macro_count}/{telemetry.meso_count}/{telemetry.micro_count}</tspan></text>'
        )
        svg_parts.append(
            f'<text x="{legend_x + 12}" y="{legend_y + 98}" font-size="9" fill="#475569">O\'Keefe Allocentric Invariants</text>'
        )

        svg_parts.append('</svg>')
        svg_content = "\n".join(svg_parts)

        if output_path:
            p = Path(output_path)
            p.parent.mkdir(parents=True, exist_ok=True)
            with open(p, "w", encoding="utf-8") as f:
                f.write(svg_content)

        return svg_content

    def render_ascii_report(self, telemetry: CrossScaleProjectionTelemetry) -> str:
        """Format an accessible ASCII summary of cross-scale projections and allocentric invariants."""
        lines = [
            "=" * 68,
            "  Spatial Schema Morphing & Cross-Scale Projection Report",
            "=" * 68,
            f"  Total Projected Entities:       {telemetry.total_entities}",
            f"  Macro Architecture Nodes:       {telemetry.macro_count}",
            f"  Meso Component Interactors:     {telemetry.meso_count}",
            f"  Micro Technical AST Contracts:  {telemetry.micro_count}",
            f"  Allocentric Drift Variance:     {telemetry.allocentric_drift_variance:.3f}",
            f"  Cross-Scale Coherence Score:    {telemetry.cross_scale_coherence_pct:.1f}%",
            "-" * 68,
            "  [PROJECTED MULTI-SCALE ENTITIES]:",
        ]

        for e in telemetry.entities:
            lines.append(
                f"    * [{e.plane.value.upper()}] {e.title} (Scale: {e.zoom_scale_factor:.1f}x)"
            )
            lines.append(
                f"      Allocentric: ({e.allocentric_x:.1f}, {e.allocentric_y:.1f}) | Invariant: {e.invariant_anchor_key}"
            )
            lines.append(f"      Summary: {e.semantic_summary[:55]}...")

        lines.append("=" * 68)
        return "\n".join(lines)
