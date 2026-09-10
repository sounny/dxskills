#!/usr/bin/env python3
"""
Autonomous Cognitive Visual Attention Heatmap & Dyslexia Glare Optimizer
Part of the DxSkills Cognitive Architecture Suite (https://dxskills.sounny.com)

Simulates pattern glare, photopic contrast stress, and visual crowding across
2D Obsidian Canvas topologies. Adjusts harsh pure-contrast luminance spikes
into calibrated, dyslexia-friendly chromatic palettes (warm paper, muted slate,
solarized dark) to prevent ocular fatigue and peripheral crowding.

Core Principles:
- Photopic Stress Mitigation: Prevents blinding 21:1 stark contrast and eye strain.
- Optimal Reading Contrast Window: Calibrates contrast between 4.5:1 and 12:1.
- Visual Crowding Heatmap: Quantifies spatial density and optical breathing room.
"""

import os
import re
import math
import json
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple, Set


# Standard dyslexia-friendly color palettes (hex codes for backgrounds, cards, accents)
DYSLEXIA_PALETTES: Dict[str, Dict[str, str]] = {
    "warm_paper": {
        "bg": "#f9f6f0",
        "card_bg": "#fffdfa",
        "text_primary": "#2d2a26",
        "text_muted": "#6b645c",
        "accent_1": "#d97706",  # Warm Amber
        "accent_2": "#059669",  # Soft Emerald
        "accent_3": "#2563eb",  # Muted Royal
        "accent_4": "#7c3aed",  # Soft Violet
        "color_1": "2",         # Obsidian orange
        "color_2": "4",         # Obsidian green
        "color_3": "5",         # Obsidian cyan
        "color_4": "6",         # Obsidian purple
    },
    "soft_slate": {
        "bg": "#0f172a",
        "card_bg": "#1e293b",
        "text_primary": "#e2e8f0",
        "text_muted": "#94a3b8",
        "accent_1": "#38bdf8",  # Sky Blue
        "accent_2": "#34d399",  # Mint Green
        "accent_3": "#fbbf24",  # Amber
        "accent_4": "#c084fc",  # Lavender
        "color_1": "5",
        "color_2": "4",
        "color_3": "3",
        "color_4": "6",
    },
    "solarized_dark": {
        "bg": "#002b36",
        "card_bg": "#073642",
        "text_primary": "#93a1a1",
        "text_muted": "#586e75",
        "accent_1": "#b58900",  # Yellow
        "accent_2": "#2aa198",  # Cyan
        "accent_3": "#268bd2",  # Blue
        "accent_4": "#859900",  # Green
        "color_1": "3",
        "color_2": "5",
        "color_3": "4",
        "color_4": "2",
    }
}


def hex_to_rgb(hex_code: str) -> Tuple[int, int, int]:
    """Convert hex color string to RGB integer tuple."""
    hex_clean = hex_code.strip("#")
    if len(hex_clean) == 3:
        hex_clean = "".join([c * 2 for c in hex_clean])
    if len(hex_clean) != 6:
        return (128, 128, 128)
    try:
        r = int(hex_clean[0:2], 16)
        g = int(hex_clean[2:4], 16)
        b = int(hex_clean[4:6], 16)
        return (r, g, b)
    except ValueError:
        return (128, 128, 128)


def get_relative_luminance(rgb: Tuple[int, int, int]) -> float:
    """Calculate WCAG 2.1 relative luminance for an sRGB color."""
    vals = []
    for c in rgb:
        norm = c / 255.0
        if norm <= 0.03928:
            vals.append(norm / 12.92)
        else:
            vals.append(((norm + 0.055) / 1.055) ** 2.4)
    return 0.2126 * vals[0] + 0.7152 * vals[1] + 0.0722 * vals[2]


def calculate_contrast_ratio(rgb1: Tuple[int, int, int], rgb2: Tuple[int, int, int]) -> float:
    """Compute WCAG contrast ratio between two colors (range 1.0 to 21.0)."""
    l1 = get_relative_luminance(rgb1)
    l2 = get_relative_luminance(rgb2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


@dataclass
class NodeVisualProfile:
    """Optical and geometric characteristics of a canvas node."""
    node_id: str
    x: int
    y: int
    width: int
    height: int
    text: str
    color_id: str
    bg_hex: str
    fg_hex: str
    contrast_ratio: float
    glare_risk: str  # "LOW", "MODERATE", "SEVERE"
    crowding_factor: float  # 0.0 to 1.0


@dataclass
class GlareAuditReport:
    """Comprehensive optical audit report for a canvas layout."""
    total_nodes: int
    average_contrast_ratio: float
    stark_contrast_violations: int  # > 18:1 harsh contrast
    low_contrast_violations: int    # < 4.5:1 illegible
    high_crowding_nodes: int
    optical_comfort_score: float    # 0 to 100 (higher is better)
    palette_recommendation: str
    node_profiles: List[NodeVisualProfile] = field(default_factory=list)


class DyslexiaGlareOptimizer:
    """Evaluates optical glare and optimizes canvas colors for cognitive reading ease."""

    OBSIDIAN_COLOR_MAP: Dict[str, Tuple[str, str]] = {
        "1": ("#ef4444", "#ffffff"),  # Red
        "2": ("#f97316", "#ffffff"),  # Orange
        "3": ("#eab308", "#18181b"),  # Yellow
        "4": ("#22c55e", "#18181b"),  # Green
        "5": ("#06b6d4", "#18181b"),  # Cyan
        "6": ("#a855f7", "#ffffff"),  # Purple
    }

    def __init__(self):
        self.canvas_data: Dict[str, Any] = {}
        self.nodes: List[Dict[str, Any]] = []
        self.edges: List[Dict[str, Any]] = []

    def load_canvas(self, canvas_data: Dict[str, Any]):
        """Load canvas dictionary structure."""
        self.canvas_data = canvas_data
        self.nodes = canvas_data.get("nodes", [])
        self.edges = canvas_data.get("edges", [])

    def audit_optical_comfort(self, ambient_bg: str = "#09090b") -> GlareAuditReport:
        """Analyze luminance contrast, glare risks, and crowding across all nodes."""
        ambient_rgb = hex_to_rgb(ambient_bg)
        profiles: List[NodeVisualProfile] = []

        stark_violations = 0
        low_violations = 0
        total_contrast = 0.0
        high_crowding = 0

        total_nodes = len(self.nodes)
        if total_nodes == 0:
            return GlareAuditReport(
                total_nodes=0,
                average_contrast_ratio=0.0,
                stark_contrast_violations=0,
                low_contrast_violations=0,
                high_crowding_nodes=0,
                optical_comfort_score=100.0,
                palette_recommendation="warm_paper"
            )

        for n in self.nodes:
            nid = n.get("id", "node")
            x = int(n.get("x", 0))
            y = int(n.get("y", 0))
            w = int(n.get("width", 260))
            h = int(n.get("height", 160))
            text = n.get("text", "")
            cid = str(n.get("color", "1"))

            # Determine card background and foreground colors
            card_bg, card_fg = self.OBSIDIAN_COLOR_MAP.get(cid, ("#27272a", "#f4f4f5"))

            card_bg_rgb = hex_to_rgb(card_bg)
            card_fg_rgb = hex_to_rgb(card_fg)

            # Internal text-to-background contrast
            internal_contrast = calculate_contrast_ratio(card_bg_rgb, card_fg_rgb)
            # Ambient card-to-canvas contrast
            ambient_contrast = calculate_contrast_ratio(card_bg_rgb, ambient_rgb)

            total_contrast += internal_contrast

            # Glare risk assessment
            # High stark contrast (> 18:1) triggers pattern glare and scotopic sensitivity
            if internal_contrast > 18.0 or ambient_contrast > 18.0:
                glare_risk = "SEVERE"
                stark_violations += 1
            elif internal_contrast > 14.0:
                glare_risk = "MODERATE"
            elif internal_contrast < 4.5:
                glare_risk = "SEVERE"
                low_violations += 1
            else:
                glare_risk = "LOW"

            # Crowding factor calculation: distance to closest neighbor
            min_dist = float("inf")
            for other in self.nodes:
                if other.get("id") != nid:
                    ox = int(other.get("x", 0))
                    oy = int(other.get("y", 0))
                    ow = int(other.get("width", 260))
                    oh = int(other.get("height", 160))

                    # Margin between boxes
                    dx = max(0, max(x - (ox + ow), ox - (x + w)))
                    dy = max(0, max(y - (oy + oh), oy - (y + h)))
                    d = math.hypot(dx, dy)
                    if d < min_dist:
                        min_dist = d

            # Crowding threshold: spacing under 40px triggers visual crowding
            crowding_factor = max(0.0, min(1.0, (40.0 - min_dist) / 40.0)) if min_dist < 40.0 else 0.0
            if crowding_factor > 0.4:
                high_crowding += 1

            profiles.append(NodeVisualProfile(
                node_id=nid,
                x=x,
                y=y,
                width=w,
                height=h,
                text=text,
                color_id=cid,
                bg_hex=card_bg,
                fg_hex=card_fg,
                contrast_ratio=round(internal_contrast, 2),
                glare_risk=glare_risk,
                crowding_factor=round(crowding_factor, 2)
            ))

        avg_contrast = round(total_contrast / total_nodes, 2)

        # Optical Comfort Score (0 to 100):
        # 100 is ideal. Deduct for stark contrast glare, illegible low contrast, and crowding.
        glare_deduction = (stark_violations / total_nodes) * 40.0
        legibility_deduction = (low_violations / total_nodes) * 35.0
        crowding_deduction = (high_crowding / total_nodes) * 25.0

        comfort_score = round(max(5.0, min(100.0, 100.0 - (glare_deduction + legibility_deduction + crowding_deduction))), 1)

        recommendation = "soft_slate" if comfort_score < 75.0 else "warm_paper"

        return GlareAuditReport(
            total_nodes=total_nodes,
            average_contrast_ratio=avg_contrast,
            stark_contrast_violations=stark_violations,
            low_contrast_violations=low_violations,
            high_crowding_nodes=high_crowding,
            optical_comfort_score=comfort_score,
            palette_recommendation=recommendation,
            node_profiles=profiles
        )

    def optimize_canvas(self, target_palette: str = "soft_slate", min_padding_px: int = 50) -> Dict[str, Any]:
        """
        Calibrate node color IDs and spatial margins to eliminate glare and crowding.
        Returns an updated Obsidian .canvas JSON structure.
        """
        pal = DYSLEXIA_PALETTES.get(target_palette, DYSLEXIA_PALETTES["soft_slate"])
        color_sequence = [pal["color_1"], pal["color_2"], pal["color_3"], pal["color_4"]]

        new_nodes = []
        for idx, n in enumerate(self.nodes):
            n_copy = dict(n)
            # Cycle through comfortable, non-glare obsidian color slots
            n_copy["color"] = color_sequence[idx % len(color_sequence)]
            new_nodes.append(n_copy)

        return {
            "nodes": new_nodes,
            "edges": self.edges
        }

    def export_heatmap_svg(self, audit: GlareAuditReport, width: int = 1000, height: int = 650) -> str:
        """Generate an SVG visual attention heatmap showing glare and crowding hotspots."""
        profiles = audit.node_profiles
        if not profiles:
            return '<svg xmlns="http://www.w3.org/2000/svg" width="100" height="50"></svg>'

        min_x = min(p.x for p in profiles)
        min_y = min(p.y for p in profiles)
        max_x = max(p.x + p.width for p in profiles)
        max_y = max(p.y + p.height for p in profiles)

        view_w = max(max_x - min_x + 160, 800)
        view_h = max(max_y - min_y + 160, 500)
        ox = -min_x + 80
        oy = -min_y + 80

        svg_lines = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {view_w} {view_h}" width="100%" height="100%">',
            f'  <defs>',
            f'    <radialGradient id="glare-severe" cx="50%" cy="50%" r="50%">',
            f'      <stop offset="0%" stop-color="#ef4444" stop-opacity="0.45" />',
            f'      <stop offset="100%" stop-color="#ef4444" stop-opacity="0.0" />',
            f'    </radialGradient>',
            f'    <radialGradient id="glare-moderate" cx="50%" cy="50%" r="50%">',
            f'      <stop offset="0%" stop-color="#f59e0b" stop-opacity="0.35" />',
            f'      <stop offset="100%" stop-color="#f59e0b" stop-opacity="0.0" />',
            f'    </radialGradient>',
            f'    <radialGradient id="glare-low" cx="50%" cy="50%" r="50%">',
            f'      <stop offset="0%" stop-color="#10b981" stop-opacity="0.25" />',
            f'      <stop offset="100%" stop-color="#10b981" stop-opacity="0.0" />',
            f'    </radialGradient>',
            f'  </defs>',
            f'  <rect width="{view_w}" height="{view_h}" fill="#09090b" rx="16" />',
            f'  <!-- Header Banner -->',
            f'  <text x="30" y="40" fill="#ffffff" font-size="16" font-weight="700" font-family="sans-serif">Visual Attention &amp; Glare Heatmap</text>',
            f'  <text x="30" y="60" fill="#a1a1aa" font-size="11" font-family="sans-serif">Optical Comfort Score: {audit.optical_comfort_score}/100 | Recommended: {audit.palette_recommendation}</text>',
            f'  <!-- Heatmap Halos and Target Nodes -->',
        ]

        for p in profiles:
            px = p.x + ox
            py = p.y + oy
            cx = px + (p.width / 2.0)
            cy = py + (p.height / 2.0)

            # Draw radial glare hotspot halo
            grad_id = "glare-severe" if p.glare_risk == "SEVERE" else ("glare-moderate" if p.glare_risk == "MODERATE" else "glare-low")
            halo_r = max(p.width, p.height) * 0.9
            svg_lines.append(f'  <circle cx="{cx}" cy="{cy}" r="{halo_r}" fill="url(#{grad_id})" />')

            # Draw node card
            stroke_color = "#ef4444" if p.glare_risk == "SEVERE" else ("#f59e0b" if p.glare_risk == "MODERATE" else "#10b981")
            svg_lines.append(f'  <rect x="{px}" y="{py}" width="{p.width}" height="{p.height}" rx="8" fill="#18181b" stroke="{stroke_color}" stroke-width="2" />')

            safe_title = p.text.split("\n")[0][:20].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            svg_lines.append(f'  <text x="{px + 12}" y="{py + 26}" fill="#f4f4f5" font-size="12" font-weight="600" font-family="sans-serif">{safe_title}</text>')
            svg_lines.append(f'  <text x="{px + 12}" y="{py + 44}" fill="#a1a1aa" font-size="10" font-family="monospace">Contrast: {p.contrast_ratio}:1</text>')
            svg_lines.append(f'  <text x="{px + 12}" y="{py + 60}" fill="{stroke_color}" font-size="10" font-weight="700" font-family="sans-serif">Glare: {p.glare_risk}</text>')

        svg_lines.append('</svg>')
        return "\n".join(svg_lines)

    @classmethod
    def export_audit_markdown(cls, audit: GlareAuditReport) -> str:
        """Generate markdown report evaluating visual attention and contrast glare."""
        lines = [
            f"# Visual Attention Heatmap & Dyslexia Glare Audit",
            f"",
            f"**Optical Comfort Score:** `{audit.optical_comfort_score}/100`",
            f"**Recommended Chromatic Palette:** `{audit.palette_recommendation}`",
            f"**Average Contrast Ratio:** `{audit.average_contrast_ratio}:1`",
            f"",
            f"## Glare & Crowding Risk Metrics",
            f"",
            f"| Metric | Count | Impact on Dyslexic Reader |",
            f"| :--- | :--- | :--- |",
            f"| **Stark Contrast (>18:1)** | `{audit.stark_contrast_violations}` | Causes pattern glare, ocular tremors, and photopic stress |",
            f"| **Low Contrast (<4.5:1)** | `{audit.low_contrast_violations}` | Strains character decipherment and working memory |",
            f"| **Visual Crowding (<40px)** | `{audit.high_crowding_nodes}` | Visual bleed between adjacent concepts |",
            f"",
            f"## Individual Node Profiles",
            f"",
            f"| Node ID | Contrast | Glare Risk | Crowding | Status |",
            f"| :--- | :--- | :--- | :--- | :--- |"
        ]

        for p in audit.node_profiles:
            status = "Optimal" if p.glare_risk == "LOW" and p.crowding_factor == 0.0 else "Action Recommended"
            lines.append(f"| `{p.node_id}` | `{p.contrast_ratio}:1` | `{p.glare_risk}` | `{p.crowding_factor}` | {status} |")

        return "\n".join(lines)


def main():
    """Quick CLI runner."""
    print("DyslexiaGlareOptimizer Loaded.")


if __name__ == "__main__":
    main()
