"""
Topographic Contour Morph & Iso-Semantic Isocline Tracer
Autonomous cognitive spatial module mapping conceptual density into continuous elevation models,
tracing equal semantic density isoclines, and rendering cartographic relief terrains.
Grounded in Eduard Imhof relief cartography, Tobler spatial interpolation,
and marching squares isocontour algorithms for spatial-relational cognitive navigation.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Any
import math
import html
import json


@dataclass
class ElevationSummit:
    """Represents a primary conceptual peak or focal idea in semantic space."""
    summit_id: str
    label: str
    x: float
    y: float
    elevation: float               # Altitude in arbitrary elevation units (e.g. 100 to 1000m)
    spread_sigma: float = 65.0      # Spatial Gaussian dispersion radius in px

    def to_dict(self) -> Dict[str, Any]:
        return {
            "summit_id": self.summit_id,
            "label": self.label,
            "x": round(self.x, 1),
            "y": round(self.y, 1),
            "elevation": round(self.elevation, 1),
            "spread_sigma": round(self.spread_sigma, 1),
        }


@dataclass
class IsoclineLevel:
    """Represents an elevation slice containing traced isocontour line segments."""
    elevation: float
    is_index_contour: bool          # True if major fifth or tenth index contour
    contour_segments: List[List[Tuple[float, float]]]
    stroke_color: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "elevation": round(self.elevation, 1),
            "is_index_contour": self.is_index_contour,
            "segment_count": len(self.contour_segments),
            "stroke_color": self.stroke_color,
        }


@dataclass
class TopographicTelemetry:
    """Comprehensive telemetry summarizing topographic terrain relief and isocline structure."""
    total_summits: int
    min_elevation: float
    max_elevation: float
    contour_interval: float
    total_isocline_levels: int
    total_segments: int
    terrain_ruggedness_index: float
    grid_size: Tuple[int, int]
    summits: List[ElevationSummit]
    levels: List[IsoclineLevel]
    warnings: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_summits": self.total_summits,
            "min_elevation": round(self.min_elevation, 1),
            "max_elevation": round(self.max_elevation, 1),
            "contour_interval": round(self.contour_interval, 1),
            "total_isocline_levels": self.total_isocline_levels,
            "total_segments": self.total_segments,
            "terrain_ruggedness_index": round(self.terrain_ruggedness_index, 2),
            "grid_size": list(self.grid_size),
            "summits": [s.to_dict() for s in self.summits],
            "levels": [lvl.to_dict() for lvl in self.levels],
            "warnings": self.warnings,
        }


class TopographicContourMorph:
    """
    Synthesizes continuous digital elevation fields from discrete conceptual nodes,
    traces iso-semantic contours via marching squares, and produces cartographic relief visualizations.
    """

    def __init__(self, base_contour_interval: float = 100.0):
        self.base_contour_interval = base_contour_interval
        self.summits: List[ElevationSummit] = []

    def add_summit(self, summit: ElevationSummit) -> None:
        """Add a semantic elevation peak to the terrain."""
        self.summits.append(summit)

    def clear_summits(self) -> None:
        """Clear all registered summits."""
        self.summits.clear()

    def evaluate_field_at(self, x: float, y: float, baseline: float = 50.0) -> float:
        """Evaluate continuous elevation at point (x, y) using Gaussian superposition."""
        elev = baseline
        for s in self.summits:
            dx = x - s.x
            dy = y - s.y
            dist_sq = dx * dx + dy * dy
            elev += s.elevation * math.exp(-dist_sq / (2.0 * s.spread_sigma * s.spread_sigma))
        return elev

    def trace_isoclines(
        self,
        grid_w: int = 52,
        grid_h: int = 34,
        min_x: float = 40.0,
        min_y: float = 120.0,
        max_x: float = 880.0,
        max_y: float = 480.0,
        contour_interval: Optional[float] = None,
    ) -> TopographicTelemetry:
        """
        Trace isoclines across regular scalar grid using 2D marching squares algorithm.
        """
        interval = contour_interval or self.base_contour_interval

        if not self.summits:
            return TopographicTelemetry(
                total_summits=0,
                min_elevation=0.0,
                max_elevation=0.0,
                contour_interval=interval,
                total_isocline_levels=0,
                total_segments=0,
                terrain_ruggedness_index=0.0,
                grid_size=(grid_w, grid_h),
                summits=[],
                levels=[],
                warnings=["No semantic summits registered to construct elevation model."],
            )

        # Build scalar elevation grid
        step_x = (max_x - min_x) / float(grid_w - 1)
        step_y = (max_y - min_y) / float(grid_h - 1)

        grid: List[List[float]] = []
        all_elevs = []
        for gy in range(grid_h):
            row = []
            cy = min_y + gy * step_y
            for gx in range(grid_w):
                cx = min_x + gx * step_x
                val = self.evaluate_field_at(cx, cy)
                row.append(val)
                all_elevs.append(val)
            grid.append(row)

        min_val = min(all_elevs)
        max_val = max(all_elevs)

        # Determine isocline threshold levels
        start_level = math.ceil(min_val / interval) * interval
        end_level = math.floor(max_val / interval) * interval

        levels_list: List[IsoclineLevel] = []
        total_segments_count = 0

        # Colors for hypsometric progression
        palette = ["#00e5ff", "#26c6da", "#00e676", "#ffb300", "#ff7043", "#ffffff"]

        current_val = start_level
        lvl_idx = 0
        while current_val <= end_level:
            is_index = (round(current_val / interval) % 5 == 0)
            segments: List[List[Tuple[float, float]]] = []

            color_idx = min(len(palette) - 1, int(((current_val - min_val) / max(1.0, max_val - min_val)) * len(palette)))
            stroke_col = palette[color_idx]

            # Marching squares cell evaluation
            for r in range(grid_h - 1):
                for c in range(grid_w - 1):
                    # Four corners of the cell
                    v_tl = grid[r][c]
                    v_tr = grid[r][c + 1]
                    v_br = grid[r + 1][c + 1]
                    v_bl = grid[r + 1][c]

                    x_l = min_x + c * step_x
                    x_r = min_x + (c + 1) * step_x
                    y_t = min_y + r * step_y
                    y_b = min_y + (r + 1) * step_y

                    # Binary classification
                    code = 0
                    if v_tl >= current_val: code |= 8
                    if v_tr >= current_val: code |= 4
                    if v_br >= current_val: code |= 2
                    if v_bl >= current_val: code |= 1

                    if code in (0, 15):
                        continue

                    # Linear interpolation helper
                    def interp(v1: float, v2: float, p1: float, p2: float) -> float:
                        if abs(v2 - v1) < 1e-6:
                            return (p1 + p2) * 0.5
                        mu = (current_val - v1) / (v2 - v1)
                        return p1 + mu * (p2 - p1)

                    top_pt = (interp(v_tl, v_tr, x_l, x_r), y_t)
                    right_pt = (x_r, interp(v_tr, v_br, y_t, y_b))
                    bottom_pt = (interp(v_bl, v_br, x_l, x_r), y_b)
                    left_pt = (x_l, interp(v_tl, v_bl, y_t, y_b))

                    if code in (1, 14):
                        segments.append([left_pt, bottom_pt])
                    elif code in (2, 13):
                        segments.append([bottom_pt, right_pt])
                    elif code in (3, 12):
                        segments.append([left_pt, right_pt])
                    elif code in (4, 11):
                        segments.append([top_pt, right_pt])
                    elif code in (5, 10):
                        segments.append([left_pt, top_pt])
                        segments.append([bottom_pt, right_pt])
                    elif code in (6, 9):
                        segments.append([top_pt, bottom_pt])
                    elif code in (7, 8):
                        segments.append([left_pt, top_pt])

            if segments:
                levels_list.append(
                    IsoclineLevel(
                        elevation=current_val,
                        is_index_contour=is_index,
                        contour_segments=segments,
                        stroke_color=stroke_col,
                    )
                )
                total_segments_count += len(segments)

            current_val += interval
            lvl_idx += 1

        # Calculate terrain ruggedness index (elevation standard deviation / mean)
        mean_elev = sum(all_elevs) / len(all_elevs) if all_elevs else 1.0
        var_elev = sum((e - mean_elev) ** 2 for e in all_elevs) / len(all_elevs) if all_elevs else 0.0
        tri = (math.sqrt(var_elev) / mean_elev) * 100.0

        warnings = []
        if total_segments_count == 0:
            warnings.append("No isoclines traced at specified interval. Adjust contour interval spacing.")

        return TopographicTelemetry(
            total_summits=len(self.summits),
            min_elevation=min_val,
            max_elevation=max_val,
            contour_interval=interval,
            total_isocline_levels=len(levels_list),
            total_segments=total_segments_count,
            terrain_ruggedness_index=tri,
            grid_size=(grid_w, grid_h),
            summits=[s for s in self.summits],
            levels=levels_list,
            warnings=warnings,
        )

    def simulate_demo_semantic_terrain(self) -> TopographicTelemetry:
        """
        Generate a multi-peak demonstration conceptual landscape
        representing a rich intellectual problem domain.
        """
        self.clear_summits()
        summits_data = [
            ("SUMMIT_CORE", "Spatial Reasoning Core", 450.0, 290.0, 820.0, 75.0),
            ("SUMMIT_PERC", "Attentional Gaze Peak", 260.0, 220.0, 640.0, 60.0),
            ("SUMMIT_WM", "Working Memory Ridge", 650.0, 240.0, 710.0, 68.0),
            ("SUMMIT_SYN", "Dialectical Valley Pass", 520.0, 410.0, 480.0, 52.0),
        ]
        for sid, lbl, sx, sy, elev, sig in summits_data:
            self.add_summit(ElevationSummit(summit_id=sid, label=lbl, x=sx, y=sy, elevation=elev, spread_sigma=sig))

        return self.trace_isoclines(contour_interval=80.0)

    def render_topographic_svg(
        self,
        telemetry: TopographicTelemetry,
        width: int = 920,
        height: int = 560,
    ) -> str:
        """
        Render a publication-grade dark titanium cartographic relief SVG diagram
        with isoclines, hypsometric gradients, spot heights, and ruggedness telemetry.
        """
        bg_color = "#0b0f14"
        card_color = "#121820"
        border_color = "#1f2937"
        text_primary = "#f3f4f6"
        text_muted = "#9ca3af"
        accent_cyan = "#00e5ff"
        accent_purple = "#7c4dff"
        accent_green = "#00e676"
        accent_amber = "#ffab00"

        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
            f'width="{width}" height="{height}" style="background-color: {bg_color}; '
            'font-family: -apple-system, BlinkMacSystemFont, sans-serif;">',
            '<defs>',
            '  <linearGradient id="reliefGrad" x1="0%" y1="0%" x2="100%" y2="0%">',
            '    <stop offset="0%" stop-color="#00e5ff" stop-opacity="0.95"/>',
            '    <stop offset="50%" stop-color="#00e676" stop-opacity="0.95"/>',
            '    <stop offset="100%" stop-color="#ffab00" stop-opacity="0.95"/>',
            '  </linearGradient>',
            '  <filter id="glowSummit" x="-20%" y="-20%" width="140%" height="140%">',
            '    <feGaussianBlur stdDeviation="3" result="blur" />',
            '    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>',
            '  </filter>',
            '</defs>',
            '<!-- Subtle coordinate grid -->',
            '<g opacity="0.06" stroke="#ffffff" stroke-width="1">',
        ]

        for gx in range(0, width, 40):
            svg_parts.append(f'<line x1="{gx}" y1="0" x2="{gx}" y2="{height}" />')
        for gy in range(0, height, 40):
            svg_parts.append(f'<line x1="0" y1="{gy}" x2="{width}" y2="{gy}" />')
        svg_parts.append('</g>')

        # Top Header Bar
        svg_parts.extend([
            f'<rect x="24" y="20" width="{width - 48}" height="70" rx="8" fill="{card_color}" stroke="{border_color}" stroke-width="1.2"/>',
            '<text x="44" y="50" fill="url(#reliefGrad)" font-size="18" font-weight="700" letter-spacing="0.5">TOPOGRAPHIC CONTOUR MORPH &amp; ISOCLINE TRACER</text>',
            '<text x="44" y="72" fill="#9ca3af" font-size="12">Cartographic Relief Elevation Model &amp; Iso-Semantic Contour Terrain</text>',
            f'<rect x="{width - 240}" y="36" width="196" height="36" rx="6" fill="#1e293b" stroke="{accent_cyan}" stroke-width="1.2"/>',
            f'<circle cx="{width - 222}" cy="54" r="5" fill="{accent_cyan}"/>',
            f'<text x="{width - 208}" y="59" fill="{text_primary}" font-size="12" font-weight="600">RELIEF: {telemetry.terrain_ruggedness_index:.1f}%</text>',
        ])

        # Main Terrain Viewport
        view_y = 105
        view_h = height - view_y - 85
        svg_parts.extend([
            f'<rect x="24" y="{view_y}" width="{width - 48}" height="{view_h}" rx="8" fill="#0c1219" stroke="{border_color}" stroke-width="1.2"/>',
            f'<text x="44" y="{view_y + 24}" fill="{text_muted}" font-size="11" font-weight="600" letter-spacing="1">SEMANTIC ELEVATION ISOCLINES (INTERVAL: {telemetry.contour_interval:.0f}m)</text>',
        ])

        # Draw Isoclines
        for lvl in telemetry.levels:
            sw = "2.2" if lvl.is_index_contour else "1.1"
            op = "0.9" if lvl.is_index_contour else "0.55"
            dash = "" if lvl.is_index_contour else ""
            for seg in lvl.contour_segments:
                if len(seg) >= 2:
                    p1, p2 = seg[0], seg[1]
                    svg_parts.append(
                        f'<line x1="{p1[0]:.1f}" y1="{p1[1]:.1f}" x2="{p2[0]:.1f}" y2="{p2[1]:.1f}" '
                        f'stroke="{lvl.stroke_color}" stroke-width="{sw}" opacity="{op}" />'
                    )

        # Draw Summits (Triangles and spot heights)
        for s in telemetry.summits:
            # Triangle marker
            tx, ty = s.x, s.y
            tri_pts = f"{tx:.1f},{ty-8:.1f} {tx-6:.1f},{ty+6:.1f} {tx+6:.1f},{ty+6:.1f}"
            svg_parts.extend([
                f'<polygon points="{tri_pts}" fill="#ffffff" filter="url(#glowSummit)"/>',
                f'<circle cx="{tx:.1f}" cy="{ty:.1f}" r="2" fill="#ff5252"/>',
                f'<text x="{tx + 12:.1f}" y="{ty - 2:.1f}" fill="{text_primary}" font-size="11" font-weight="700">{html.escape(s.label)}</text>',
                f'<text x="{tx + 12:.1f}" y="{ty + 11:.1f}" fill="{accent_amber}" font-size="9.5">{s.elevation:.0f}m | s={s.spread_sigma:.0f}px</text>',
            ])

        # Bottom Metrics Cards
        bottom_y = height - 72
        card_w = (width - 48 - 36) / 4

        metrics = [
            ("Peak Elevation", f"{telemetry.max_elevation:.0f} m", accent_cyan),
            ("Base Baseline", f"{telemetry.min_elevation:.0f} m", accent_purple),
            ("Isocline Levels", f"{telemetry.total_isocline_levels} slices", accent_green),
            ("Terrain Ruggedness", f"{telemetry.terrain_ruggedness_index:.1f}%", accent_amber),
        ]

        for i, (m_label, m_val, m_col) in enumerate(metrics):
            cx = 24 + i * (card_w + 12)
            svg_parts.extend([
                f'<rect x="{cx:.1f}" y="{bottom_y}" width="{card_w:.1f}" height="56" rx="6" fill="{card_color}" stroke="{border_color}" stroke-width="1.2"/>',
                f'<text x="{cx + 12:.1f}" y="{bottom_y + 20}" fill="{text_muted}" font-size="10.5">{m_label}</text>',
                f'<text x="{cx + 12:.1f}" y="{bottom_y + 44}" fill="{m_col}" font-size="16" font-weight="700">{m_val}</text>',
            ])

        svg_parts.append('</svg>')
        return "\n".join(svg_parts)

    def export_telemetry_json(self, telemetry: TopographicTelemetry) -> str:
        """Export serialized telemetry to JSON format."""
        return json.dumps(telemetry.to_dict(), indent=2)
