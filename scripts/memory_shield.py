"""Autonomous Cognitive Spatial Saliency Decoupling & Working Memory Shield.

Theoretical Foundation:
- Lavie's Perceptual Load Theory & Inattentional Intrusion:
  Peripheral visual bandwidth in dyslexic and spatial thinkers captures ambient
  high-contrast visual tokens. In high-load analytical tasks, non-task tokens
  leak into working memory buffers as "semantic intrusions", inducing attentional
  fragmentation and split-attention overhead.
- Spatial Saliency Decoupling & Graduated Shielding:
  Establishes concentric radial tiers around the active analytical focus cluster:
    Tier 0 (Focus Zone): 100% opacity, full semantic and typographic resolution.
    Tier 1 (Orientation Ring): 60% opacity, structural headers and relation anchors.
    Tier 2 (Ambient Shield): 25% opacity, dampened peripheral clutter to prevent
    saccadic hijacking and working memory saturation.

Strict Quality Gate: Zero em dashes anywhere (use hyphens, commas, or parentheses).
"""

from __future__ import annotations

import enum
import json
import math
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class ShieldTier(str, enum.Enum):
    """Concentric shielding zones around active cognitive focus."""

    FOCUS = "focus"
    ORIENTATION = "orientation"
    AMBIENT_DAMPENED = "ambient_dampened"


@dataclass
class ShieldedNode:
    """Individual canvas node with saliency decoupling attributes."""

    node_id: str
    x: float
    y: float
    width: float
    height: float
    original_text: str
    shielded_text: str
    tier: ShieldTier
    opacity: float
    color_code: str
    distance_from_focus: float
    intrusion_risk_score: float


@dataclass
class MemoryShieldTelemetry:
    """Telemetry report quantifying saliency decoupling and cognitive shielding."""

    focus_node_ids: List[str]
    total_nodes: int
    focus_count: int
    orientation_count: int
    dampened_count: int
    avg_intrusion_mitigation_pct: float
    cognitive_bandwidth_reclaimed_pct: float
    shielded_nodes: List[ShieldedNode] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert telemetry to JSON-compatible dictionary."""
        return {
            "focus_node_ids": self.focus_node_ids,
            "total_nodes": self.total_nodes,
            "focus_count": self.focus_count,
            "orientation_count": self.orientation_count,
            "dampened_count": self.dampened_count,
            "avg_intrusion_mitigation_pct": round(self.avg_intrusion_mitigation_pct, 1),
            "cognitive_bandwidth_reclaimed_pct": round(self.cognitive_bandwidth_reclaimed_pct, 1),
            "shielded_nodes": [asdict(n) for n in self.shielded_nodes],
        }


class WorkingMemoryShield:
    """Decouples spatial saliency and shields working memory from peripheral intrusions."""

    def __init__(
        self,
        focus_radius_px: float = 600.0,
        orientation_radius_px: float = 1200.0,
    ) -> None:
        self.focus_radius_px = max(100.0, focus_radius_px)
        self.orientation_radius_px = max(self.focus_radius_px + 100.0, orientation_radius_px)

    @staticmethod
    def calculate_node_center(node: Dict[str, Any]) -> Tuple[float, float]:
        """Calculate geometric center of a rectangular canvas node."""
        x = float(node.get("x", 0.0))
        y = float(node.get("y", 0.0))
        w = float(node.get("width", 250.0))
        h = float(node.get("height", 150.0))
        return (x + (w / 2.0), y + (h / 2.0))

    @classmethod
    def calculate_distance(cls, node_a: Dict[str, Any], node_b: Dict[str, Any]) -> float:
        """Euclidean distance between two node centers."""
        cx1, cy1 = cls.calculate_node_center(node_a)
        cx2, cy2 = cls.calculate_node_center(node_b)
        return math.hypot(cx2 - cx1, cy2 - cy1)

    @staticmethod
    def evaluate_intrusion_risk(node: Dict[str, Any], distance: float) -> float:
        """Calculate semantic intrusion risk score (0.0 to 1.0).

        Risk increases with text density, uppercase emphasis, and high-contrast styling,
        scaled inversely by distance from focus.
        """
        text = str(node.get("text", ""))
        length = len(text)
        if length == 0:
            return 0.0

        words = text.split()
        word_count = len(words)
        caps_count = sum(1 for w in words if w.isupper() and len(w) > 1)

        density_score = min(1.0, word_count / 30.0)
        caps_penalty = min(0.3, (caps_count / max(1, word_count)) * 0.5)

        # Distant nodes with high density present severe peripheral distraction risk
        distance_factor = min(1.0, distance / 1500.0)
        risk = (0.5 * density_score) + caps_penalty + (0.2 * distance_factor)
        return max(0.05, min(1.0, risk))

    def apply_memory_shield(
        self,
        canvas_data: Dict[str, Any],
        focus_ids: Optional[List[str]] = None,
    ) -> Tuple[Dict[str, Any], MemoryShieldTelemetry]:
        """Apply saliency decoupling shield across Obsidian Canvas nodes."""
        nodes = canvas_data.get("nodes", [])
        if not nodes:
            empty_telemetry = MemoryShieldTelemetry(
                focus_node_ids=[],
                total_nodes=0,
                focus_count=0,
                orientation_count=0,
                dampened_count=0,
                avg_intrusion_mitigation_pct=0.0,
                cognitive_bandwidth_reclaimed_pct=0.0,
                shielded_nodes=[],
            )
            return canvas_data, empty_telemetry

        # If no focus nodes specified, pick the first node or central node
        if not focus_ids:
            focus_ids = [nodes[0].get("id", "")]

        focus_nodes = [n for n in nodes if n.get("id") in focus_ids]
        if not focus_nodes:
            focus_nodes = [nodes[0]]
            focus_ids = [nodes[0].get("id", "")]

        # Compute centroid of focus group
        focus_centers = [self.calculate_node_center(fn) for fn in focus_nodes]
        fc_x = sum(c[0] for c in focus_centers) / len(focus_centers)
        fc_y = sum(c[1] for c in focus_centers) / len(focus_centers)
        focus_centroid = {"x": fc_x, "y": fc_y, "width": 0, "height": 0}

        shielded_nodes: List[ShieldedNode] = []
        new_nodes: List[Dict[str, Any]] = []

        focus_count = 0
        orientation_count = 0
        dampened_count = 0
        intrusion_mitigation_sum = 0.0

        for node in nodes:
            nid = node.get("id", "")
            is_explicit_focus = nid in focus_ids
            dist = self.calculate_distance(node, focus_centroid)
            risk = self.evaluate_intrusion_risk(node, dist)
            raw_text = str(node.get("text", ""))

            new_node = dict(node)

            if is_explicit_focus or dist <= self.focus_radius_px:
                tier = ShieldTier.FOCUS
                opacity = 1.0
                color_code = "4"  # Green/Cyan focus
                shielded_text = raw_text
                focus_count += 1
                mitigation = 0.0
            elif dist <= self.orientation_radius_px:
                tier = ShieldTier.ORIENTATION
                opacity = 0.60
                color_code = "2"  # Amber/Subtle
                # Condense text to structural title or first 2 lines
                lines = raw_text.splitlines()
                header = lines[0] if lines else raw_text[:40]
                shielded_text = f"{header}\n\n*(Orientation Anchor)*"
                orientation_count += 1
                mitigation = risk * 0.50
            else:
                tier = ShieldTier.AMBIENT_DAMPENED
                opacity = 0.25
                color_code = "1"  # Dark gray / dampened
                # Collapse text to prevent peripheral reading capture
                lines = raw_text.splitlines()
                title = lines[0][:30] if lines else "Node"
                shielded_text = f"~ {title} ~ *(Shielded Ambient)*"
                dampened_count += 1
                mitigation = risk * 0.85

            intrusion_mitigation_sum += mitigation
            new_node["color"] = color_code
            new_node["text"] = shielded_text

            shielded_nodes.append(
                ShieldedNode(
                    node_id=nid,
                    x=float(node.get("x", 0.0)),
                    y=float(node.get("y", 0.0)),
                    width=float(node.get("width", 250.0)),
                    height=float(node.get("height", 150.0)),
                    original_text=raw_text,
                    shielded_text=shielded_text,
                    tier=tier,
                    opacity=opacity,
                    color_code=color_code,
                    distance_from_focus=round(dist, 1),
                    intrusion_risk_score=round(risk, 3),
                )
            )
            new_nodes.append(new_node)

        total_nodes_count = len(nodes)
        avg_mitigation = (intrusion_mitigation_sum / total_nodes_count) * 100.0 if total_nodes_count > 0 else 0.0
        # Cognitive bandwidth reclaimed proportional to dampened peripheral clutter
        reclaimed_pct = ((dampened_count * 0.75 + orientation_count * 0.40) / max(1, total_nodes_count)) * 100.0

        # Add HUD notification node to canvas
        hud_text = (
            "## Working Memory Shield Engaged\n\n"
            f"- **Focus Cluster:** {len(focus_ids)} nodes\n"
            f"- **Orientation Anchors:** {orientation_count} nodes (60% opacity)\n"
            f"- **Ambient Dampened:** {dampened_count} nodes (25% opacity)\n"
            f"- **Clutter Intrusion Blocked:** {avg_mitigation:.1f}%\n"
            f"- **Bandwidth Reclaimed:** {reclaimed_pct:.1f}%\n"
        )
        new_nodes.append({
            "id": "node-memory-shield-hud",
            "x": fc_x - 175,
            "y": fc_y - self.focus_radius_px - 260,
            "width": 350,
            "height": 210,
            "type": "text",
            "text": hud_text,
            "color": "5",
        })

        shielded_canvas = dict(canvas_data)
        shielded_canvas["nodes"] = new_nodes

        telemetry = MemoryShieldTelemetry(
            focus_node_ids=focus_ids,
            total_nodes=total_nodes_count,
            focus_count=focus_count,
            orientation_count=orientation_count,
            dampened_count=dampened_count,
            avg_intrusion_mitigation_pct=avg_mitigation,
            cognitive_bandwidth_reclaimed_pct=reclaimed_pct,
            shielded_nodes=shielded_nodes,
        )

        return shielded_canvas, telemetry

    @staticmethod
    def render_ascii_report(telemetry: MemoryShieldTelemetry) -> str:
        """Render clean ASCII report of shielded nodes and tier classifications."""
        lines: List[str] = []
        lines.append("=== DxSkills Working Memory Shield & Saliency Decoupler ===")
        lines.append(
            f"Focus Nodes: {len(telemetry.focus_node_ids)} | Total Nodes: {telemetry.total_nodes} | "
            f"Bandwidth Reclaimed: {telemetry.cognitive_bandwidth_reclaimed_pct:.1f}%"
        )
        lines.append(
            f"Tiers: Focus={telemetry.focus_count} | Orientation={telemetry.orientation_count} | "
            f"Dampened={telemetry.dampened_count} | Intrusion Mitigation: {telemetry.avg_intrusion_mitigation_pct:.1f}%"
        )
        lines.append("-" * 68)
        lines.append(f"{'Node ID':<16} {'Tier':<18} {'Dist (px)':<11} {'Risk':<7} {'Opacity'}")
        lines.append("-" * 68)

        for sn in telemetry.shielded_nodes[:14]:
            nid_str = sn.node_id[:14]
            tier_str = sn.tier.value[:16]
            opacity_bar = "#" * int(round(sn.opacity * 10))
            lines.append(f"{nid_str:<16} {tier_str:<18} {sn.distance_from_focus:>8.0f}px   {sn.intrusion_risk_score:>5.2f}  [{opacity_bar:<10}] {sn.opacity*100:.0f}%")

        if len(telemetry.shielded_nodes) > 14:
            rem = len(telemetry.shielded_nodes) - 14
            lines.append(f"... ({rem} additional peripheral nodes shielded)")

        lines.append("-" * 68)
        return "\n".join(lines)

    @staticmethod
    def export_svg_shield(telemetry: MemoryShieldTelemetry, output_path: str | Path) -> Path:
        """Export standalone SVG visualization of concentric shielding radar."""
        target = Path(output_path)
        width = 800
        height = 600
        cx = width / 2.0
        cy = height / 2.0 + 20

        svg: List[str] = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="auto">',
            '  <defs>',
            '    <radialGradient id="shield-rad" cx="50%" cy="50%" r="50%">',
            '      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.25"/>',
            '      <stop offset="45%" stop-color="#0284c7" stop-opacity="0.10"/>',
            '      <stop offset="100%" stop-color="#090d16" stop-opacity="0.0"/>',
            '    </radialGradient>',
            '  </defs>',
            f'  <rect width="{width}" height="{height}" rx="16" fill="#0b0f19" stroke="#1e293b" stroke-width="2"/>',
            f'  <text x="32" y="42" fill="#f8fafc" font-family="system-ui, sans-serif" font-size="16" font-weight="700">DxSkills Working Memory Shield &amp; Saliency Decoupler</text>',
            f'  <text x="32" y="66" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="12">Bandwidth Reclaimed: {telemetry.cognitive_bandwidth_reclaimed_pct:.1f}% | Mitigation: {telemetry.avg_intrusion_mitigation_pct:.1f}% | Focus: {telemetry.focus_count} nodes</text>',
            f'  <circle cx="{cx}" cy="{cy}" r="220" fill="#0f172a" stroke="#334155" stroke-dasharray="4 4" stroke-width="1.5"/>',
            f'  <circle cx="{cx}" cy="{cy}" r="140" fill="url(#shield-rad)" stroke="#0284c7" stroke-width="2"/>',
            f'  <circle cx="{cx}" cy="{cy}" r="65" fill="#0369a1" fill-opacity="0.4" stroke="#38bdf8" stroke-width="2.5"/>',
            f'  <text x="{cx}" y="{cy - 72}" fill="#38bdf8" font-family="system-ui, sans-serif" font-size="11" font-weight="700" text-anchor="middle">FOCUS ZONE (Tier 0)</text>',
            f'  <text x="{cx}" y="{cy - 148}" fill="#0284c7" font-family="system-ui, sans-serif" font-size="11" text-anchor="middle">ORIENTATION RING (Tier 1)</text>',
            f'  <text x="{cx}" y="{cy - 228}" fill="#64748b" font-family="system-ui, sans-serif" font-size="11" text-anchor="middle">AMBIENT SHIELD (Tier 2)</text>',
        ]

        # Draw node markers in polar layout
        num_nodes = len(telemetry.shielded_nodes)
        for idx, sn in enumerate(telemetry.shielded_nodes[:24]):
            angle = (idx / max(1, min(24, num_nodes))) * 2 * math.pi
            if sn.tier == ShieldTier.FOCUS:
                r = 35 + (idx % 2) * 18
                color = "#38bdf8"
                node_r = 7
            elif sn.tier == ShieldTier.ORIENTATION:
                r = 100 + (idx % 3) * 15
                color = "#f59e0b"
                node_r = 5
            else:
                r = 175 + (idx % 3) * 18
                color = "#64748b"
                node_r = 3

            nx = cx + (r * math.cos(angle))
            ny = cy + (r * math.sin(angle))
            svg.append(f'  <circle cx="{nx:.1f}" cy="{ny:.1f}" r="{node_r}" fill="{color}" opacity="{sn.opacity}"/>')

        svg.append('</svg>')
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("\n".join(svg), encoding="utf-8")
        return target
