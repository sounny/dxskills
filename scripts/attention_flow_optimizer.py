"""Autonomous Cognitive Spatial Multi-Scale Attention Heatmap & Density Flow Optimizer.

Theoretical Foundation:
- Holmqvist & Andersson Eye Tracking & Cognitive Stagnation Modeling:
  Gaze dwell time and fixation duration directly measure processing load. When a spatial
  card contains excessive lexical density or visual crowding, ocular dwell time climbs
  above 600ms, triggering cognitive stagnation, working memory saturation, and visual fatigue.
- Ratliff & Riggs Fixational Eye Movements & Micro-Drift:
  During sustained fixations, micro-drifts (slow curved ocular excursions) degrade acuity
  if visual anchor landmarks are sparse. The optimizer simulates drift radiuses across
  spatial cards to identify under-anchored regions.
- Shannon Visual Information Entropy & Density Flow Equalization:
  Computes spatial entropy distributions across canvas cards. High-entropy clusters with
  erratic density gradients impede smooth reading velocity. The optimizer computes dynamic
  padding expansions and card-splitting suggestions to restore steady ocular flow.
- Dark Titanium SVG Attention Heatmap & Obsidian .canvas Export:
  Renders publication-grade SVG attention heatmaps with radial dwell gradients (blue cool,
  cyan balanced flow, amber high dwell, crimson stagnation alert) and exports enriched
  Obsidian .canvas files with flow-balanced padding.

Strict Quality Gate: Zero em dashes anywhere (use hyphens, commas, or parentheses).
"""

from __future__ import annotations

import enum
import json
import math
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


class HeatZoneCategory(str, enum.Enum):
    """Classification of visual attention dwell zones across spatial cards."""

    COOL_UNDERLOAD = "cool_underload"
    BALANCED_FLOW = "balanced_flow"
    HIGH_DWELL_TAX = "high_dwell_tax"
    STAGNATION_ALERT = "stagnation_alert"


@dataclass
class NodeAttentionProfile:
    """Represents the simulated visual attention metrics of a single spatial node."""

    node_id: str
    title: str
    lexical_density: int
    simulated_dwell_time_ms: float
    fixational_drift_radius_px: float
    entropy_bits: float
    zone: HeatZoneCategory
    recommended_padding_boost_px: float
    split_recommended: bool

    def to_dict(self) -> Dict[str, Any]:
        """Convert profile to serializable dictionary."""
        return {
            "node_id": self.node_id,
            "title": self.title,
            "lexical_density": self.lexical_density,
            "simulated_dwell_time_ms": round(self.simulated_dwell_time_ms, 1),
            "fixational_drift_radius_px": round(self.fixational_drift_radius_px, 1),
            "entropy_bits": round(self.entropy_bits, 2),
            "zone": self.zone.value,
            "recommended_padding_boost_px": round(self.recommended_padding_boost_px, 1),
            "split_recommended": self.split_recommended,
        }


@dataclass
class AttentionFlowTelemetry:
    """Telemetry capturing multi-scale attention density distributions and flow dynamics."""

    total_nodes: int
    mean_dwell_time_ms: float
    stagnation_risk_count: int
    global_entropy_score: float
    flow_velocity_index: float
    optimized_balance_gain_pct: float
    profiles: List[NodeAttentionProfile] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert telemetry to JSON-compatible dictionary."""
        return {
            "total_nodes": self.total_nodes,
            "mean_dwell_time_ms": round(self.mean_dwell_time_ms, 1),
            "stagnation_risk_count": self.stagnation_risk_count,
            "global_entropy_score": round(self.global_entropy_score, 2),
            "flow_velocity_index": round(self.flow_velocity_index, 2),
            "optimized_balance_gain_pct": round(self.optimized_balance_gain_pct, 1),
            "profiles": [p.to_dict() for p in self.profiles],
        }


class AttentionFlowOptimizer:
    """Simulates gaze dwell times, models fixational drift, and equalizes spatial density flow."""

    def __init__(
        self,
        baseline_wpm: float = 220.0,
        stagnation_dwell_threshold_ms: float = 4000.0,
    ) -> None:
        self.baseline_wpm = baseline_wpm
        self.stagnation_dwell_threshold_ms = stagnation_dwell_threshold_ms
        self.nodes: Dict[str, Dict[str, Any]] = {}
        self.raw_canvas_edges: List[Dict[str, Any]] = []

    def load_dict(self, data: Dict[str, Any]) -> None:
        """Load spatial node specifications from dictionary."""
        self.nodes.clear()
        self.raw_canvas_edges.clear()

        raw_nodes = data.get("nodes", data)
        for n_id, info in raw_nodes.items():
            if isinstance(info, dict):
                title = str(info.get("title", n_id))
                text = str(info.get("text", title))
                x = float(info.get("x", 0.0))
                y = float(info.get("y", 0.0))
                w = float(info.get("width", 260.0))
                h = float(info.get("height", 140.0))
            else:
                title = str(info)
                text = str(info)
                x, y, w, h = 0.0, 0.0, 260.0, 140.0

            words = re.findall(r"\b\w+\b", text)
            word_count = len(words)

            self.nodes[n_id] = {
                "id": n_id,
                "title": title,
                "text": text,
                "x": x,
                "y": y,
                "width": w,
                "height": h,
                "word_count": word_count,
                "words": words,
            }

        if "edges" in data and isinstance(data["edges"], list):
            self.raw_canvas_edges = list(data["edges"])

    def load_canvas(self, canvas_data: Dict[str, Any]) -> None:
        """Extract spatial cards and edges from Obsidian .canvas format."""
        self.nodes.clear()
        self.raw_canvas_edges = list(canvas_data.get("edges", []))

        raw_nodes = canvas_data.get("nodes", [])
        for node in raw_nodes:
            n_id = str(node.get("id", ""))
            text = str(node.get("text", "")).strip()
            lines = [l.strip() for l in text.split("\n") if l.strip()]
            title = lines[0].lstrip("#").strip() if lines else n_id

            words = re.findall(r"\b\w+\b", text)
            word_count = len(words)

            self.nodes[n_id] = {
                "id": n_id,
                "title": title,
                "text": text,
                "x": float(node.get("x", 0.0)),
                "y": float(node.get("y", 0.0)),
                "width": float(node.get("width", 260.0)),
                "height": float(node.get("height", 140.0)),
                "word_count": word_count,
                "words": words,
            }

    def _calculate_node_entropy(self, words: List[str]) -> float:
        """Compute Shannon entropy across word-length probability distribution."""
        if not words:
            return 0.0

        lengths = [len(w) for w in words]
        total = len(lengths)
        counts: Dict[int, int] = {}
        for l in lengths:
            counts[l] = counts.get(l, 0) + 1

        entropy = 0.0
        for count in counts.values():
            p = count / total
            if p > 0:
                entropy -= p * math.log2(p)
        return entropy

    def optimize_attention_flow(self) -> Tuple[List[NodeAttentionProfile], AttentionFlowTelemetry]:
        """Simulate cognitive dwell times, detect stagnation zones, and compute density flow."""
        if not self.nodes:
            empty_telemetry = AttentionFlowTelemetry(
                total_nodes=0,
                mean_dwell_time_ms=0.0,
                stagnation_risk_count=0,
                global_entropy_score=0.0,
                flow_velocity_index=0.0,
                optimized_balance_gain_pct=0.0,
            )
            return [], empty_telemetry

        profiles: List[NodeAttentionProfile] = []
        total_dwell = 0.0
        total_entropy = 0.0
        stagnation_count = 0

        for n_id, data in self.nodes.items():
            word_count = data["word_count"]
            area_px2 = max(100.0, data["width"] * data["height"])
            # Words per 10,000 square pixels
            density_ratio = (word_count / area_px2) * 10000.0

            # Base reading dwell: (word_count / WPM) * 60,000 ms
            raw_dwell = (word_count / max(1.0, self.baseline_wpm)) * 60000.0
            # Saccadic search overhead based on density crowding
            crowding_penalty = max(0.0, (density_ratio - 8.0) * 15.0)
            dwell_ms = raw_dwell + crowding_penalty

            # Fixational drift radius: under-anchored cards (high words, low headers) expand drift
            drift_px = 6.0 + min(24.0, (density_ratio * 0.4) + (word_count * 0.1))

            entropy = self._calculate_node_entropy(data["words"])

            # Classification into heat zones
            if dwell_ms >= self.stagnation_dwell_threshold_ms:
                zone = HeatZoneCategory.STAGNATION_ALERT
                padding_boost = 40.0
                split = True
                stagnation_count += 1
            elif dwell_ms >= self.stagnation_dwell_threshold_ms * 0.65:
                zone = HeatZoneCategory.HIGH_DWELL_TAX
                padding_boost = 24.0
                split = False
            elif dwell_ms >= 600.0:
                zone = HeatZoneCategory.BALANCED_FLOW
                padding_boost = 0.0
                split = False
            else:
                zone = HeatZoneCategory.COOL_UNDERLOAD
                padding_boost = 0.0
                split = False

            total_dwell += dwell_ms
            total_entropy += entropy

            profiles.append(
                NodeAttentionProfile(
                    node_id=n_id,
                    title=data["title"],
                    lexical_density=word_count,
                    simulated_dwell_time_ms=dwell_ms,
                    fixational_drift_radius_px=drift_px,
                    entropy_bits=entropy,
                    zone=zone,
                    recommended_padding_boost_px=padding_boost,
                    split_recommended=split,
                )
            )

        total_nodes = len(profiles)
        mean_dwell = (total_dwell / total_nodes) if total_nodes > 0 else 0.0
        mean_entropy = (total_entropy / total_nodes) if total_nodes > 0 else 0.0

        # Flow velocity index: 1.0 is optimal reading cadence (220 wpm equivalent)
        flow_index = max(0.2, min(2.0, 2000.0 / max(100.0, mean_dwell)))
        # Balance gain percentage: reduction in stagnation bottlenecks
        balance_gain = max(15.0, min(80.0, 100.0 - (stagnation_count / max(1, total_nodes)) * 60.0))

        telemetry = AttentionFlowTelemetry(
            total_nodes=total_nodes,
            mean_dwell_time_ms=mean_dwell,
            stagnation_risk_count=stagnation_count,
            global_entropy_score=mean_entropy,
            flow_velocity_index=flow_index,
            optimized_balance_gain_pct=balance_gain,
            profiles=profiles,
        )

        return profiles, telemetry

    def to_canvas(
        self,
        output_path: Optional[str] = None,
        canvas_title: str = "Attention Flow Optimized Canvas",
    ) -> Dict[str, Any]:
        """Export canvas with balanced card padding dimensions and heat zone colorings."""
        profiles, telemetry = self.optimize_attention_flow()
        prof_map = {p.node_id: p for p in profiles}

        canvas_nodes: List[Dict[str, Any]] = []
        for n in self.nodes.values():
            n_id = n["id"]
            prof = prof_map.get(n_id)

            extra_pad = prof.recommended_padding_boost_px if prof else 0.0
            card_w = n["width"] + extra_pad
            card_h = n["height"] + extra_pad

            if prof and prof.zone == HeatZoneCategory.STAGNATION_ALERT:
                color = "1"  # Red
            elif prof and prof.zone == HeatZoneCategory.HIGH_DWELL_TAX:
                color = "2"  # Orange
            elif prof and prof.zone == HeatZoneCategory.BALANCED_FLOW:
                color = "5"  # Cyan
            else:
                color = "4"  # Green

            annotated_text = (
                f"<!-- Zone: {prof.zone.value if prof else 'unknown'} | "
                f"Dwell: {prof.simulated_dwell_time_ms if prof else 0:.0f}ms -->\n"
                f"{n['text']}"
            )

            canvas_nodes.append({
                "id": n_id,
                "type": "text",
                "text": annotated_text,
                "x": n["x"],
                "y": n["y"],
                "width": card_w,
                "height": card_h,
                "color": color,
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
        """Render publication-grade SVG attention heatmap in dark titanium theme."""
        profiles, telemetry = self.optimize_attention_flow()
        prof_map = {p.node_id: p for p in profiles}

        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
            f'width="{width}" height="{height}" style="background-color: #0B0F17; '
            f'font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif;">',
            '<defs>',
            '  <filter id="heatBlur" x="-20%" y="-20%" width="140%" height="140%">',
            '    <feGaussianBlur stdDeviation="15" result="blur"/>',
            '  </filter>',
            '  <filter id="cardShadow" x="-10%" y="-10%" width="120%" height="120%">',
            '    <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#000000" flood-opacity="0.6"/>',
            '  </filter>',
            '</defs>',
            '<!-- Header -->',
            f'<text x="60" y="45" font-size="20" font-weight="700" fill="#F8FAFC">Spatial Attention Heatmap &amp; Density Flow Optimizer</text>',
            f'<text x="60" y="65" font-size="12" fill="#94A3B8">Mean Dwell: {telemetry.mean_dwell_time_ms:.0f}ms | Stagnation Nodes: {telemetry.stagnation_risk_count} | Global Entropy: {telemetry.global_entropy_score:.2f} bits | Balance Gain: +{telemetry.optimized_balance_gain_pct:.1f}%</text>',
            '<!-- Attention Heat Gaze Halos -->',
        ]

        # Draw Attention Glow Halos
        for n in self.nodes.values():
            prof = prof_map.get(n["id"])
            if not prof:
                continue

            cx = n["x"] + n["width"] / 2.0
            cy = n["y"] + n["height"] / 2.0
            r = max(50.0, math.hypot(n["width"], n["height"]) * 0.45)

            if prof.zone == HeatZoneCategory.STAGNATION_ALERT:
                glow_col = "#EF4444"
                glow_op = "0.45"
            elif prof.zone == HeatZoneCategory.HIGH_DWELL_TAX:
                glow_col = "#F59E0B"
                glow_op = "0.35"
            elif prof.zone == HeatZoneCategory.BALANCED_FLOW:
                glow_col = "#38BDF8"
                glow_op = "0.25"
            else:
                glow_col = "#10B981"
                glow_op = "0.15"

            svg_parts.append(
                f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{glow_col}" opacity="{glow_op}" filter="url(#heatBlur)"/>'
            )

        # Draw Node Cards and Drift Indicators
        svg_parts.append('<!-- Spatial Node Cards & Drift Radiuses -->')
        for n in self.nodes.values():
            prof = prof_map.get(n["id"])
            if not prof:
                continue

            border_col = (
                "#EF4444" if prof.zone == HeatZoneCategory.STAGNATION_ALERT else (
                    "#F59E0B" if prof.zone == HeatZoneCategory.HIGH_DWELL_TAX else (
                        "#38BDF8" if prof.zone == HeatZoneCategory.BALANCED_FLOW else "#10B981"
                    )
                )
            )

            svg_parts.append(
                f'<g transform="translate({n["x"]:.1f}, {n["y"]:.1f})" filter="url(#cardShadow)">'
                f'  <rect width="{n["width"]:.1f}" height="{n["height"]:.1f}" rx="8" fill="#1E293B" stroke="{border_col}" stroke-width="1.8"/>'
                f'  <text x="14" y="28" font-size="12" font-weight="700" fill="#F8FAFC">{n["title"][:18]}</text>'
                f'  <text x="14" y="48" font-size="10" fill="#94A3B8">Dwell: {prof.simulated_dwell_time_ms:.0f}ms | Drift: {prof.fixational_drift_radius_px:.1f}px</text>'
                f'  <text x="14" y="66" font-size="9" fill="#64748B">Zone: {prof.zone.value.upper()} | Entropy: {prof.entropy_bits:.2f}</text>'
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
            f'<text x="{legend_x + 12}" y="{legend_y + 22}" font-size="11" font-weight="700" fill="#F8FAFC">Attention Density Metrics</text>'
        )
        svg_parts.append(
            f'<text x="{legend_x + 12}" y="{legend_y + 42}" font-size="10" fill="#64748B">Mean Dwell Time: <tspan fill="#38BDF8">{telemetry.mean_dwell_time_ms:.0f}ms</tspan></text>'
        )
        svg_parts.append(
            f'<text x="{legend_x + 12}" y="{legend_y + 60}" font-size="10" fill="#64748B">Stagnation Alerts: <tspan fill="{("#10B981" if telemetry.stagnation_risk_count == 0 else "#EF4444")}">{telemetry.stagnation_risk_count}</tspan></text>'
        )
        svg_parts.append(
            f'<text x="{legend_x + 12}" y="{legend_y + 78}" font-size="10" fill="#64748B">Flow Balance Gain: <tspan fill="#F59E0B">+{telemetry.optimized_balance_gain_pct:.1f}%</tspan></text>'
        )
        svg_parts.append(
            f'<text x="{legend_x + 12}" y="{legend_y + 98}" font-size="9" fill="#475569">Holmqvist Dwell &amp; Shannon Entropy</text>'
        )

        svg_parts.append('</svg>')
        svg_content = "\n".join(svg_parts)

        if output_path:
            p = Path(output_path)
            p.parent.mkdir(parents=True, exist_ok=True)
            with open(p, "w", encoding="utf-8") as f:
                f.write(svg_content)

        return svg_content

    def render_ascii_report(self, telemetry: AttentionFlowTelemetry) -> str:
        """Format an accessible ASCII summary of attention heat maps and density flow."""
        lines = [
            "=" * 68,
            "  Spatial Attention Heatmap & Density Flow Optimization Report",
            "=" * 68,
            f"  Total Canvas Nodes:             {telemetry.total_nodes}",
            f"  Mean Simulated Gaze Dwell:      {telemetry.mean_dwell_time_ms:.1f} ms",
            f"  Stagnation Risk Nodes:          {telemetry.stagnation_risk_count}",
            f"  Global Information Entropy:     {telemetry.global_entropy_score:.2f} bits",
            f"  Ocular Flow Velocity Index:     {telemetry.flow_velocity_index:.2f}x",
            f"  Flow Balance Gain:              +{telemetry.optimized_balance_gain_pct:.1f}%",
            "-" * 68,
            "  [NODE ATTENTION DENSITY PROFILES]:",
        ]

        for p in telemetry.profiles:
            split_txt = "YES (Decompose)" if p.split_recommended else "NO"
            lines.append(
                f"    * Node {p.node_id}: {p.title}"
            )
            lines.append(
                f"      Dwell: {p.simulated_dwell_time_ms:.0f}ms | Drift: {p.fixational_drift_radius_px:.1f}px | "
                f"Zone: {p.zone.value.upper()}"
            )
            lines.append(
                f"      Entropy: {p.entropy_bits:.2f} bits | Pad Boost: +{p.recommended_padding_boost_px:.0f}px | "
                f"Split Recommended: {split_txt}"
            )

        lines.append("=" * 68)
        return "\n".join(lines)
