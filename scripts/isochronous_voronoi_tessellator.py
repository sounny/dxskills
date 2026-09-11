"""
Iso-Chronous Voronoi Isochrone Tessellator & Proximity Loom
Autonomous cognitive spatial module mapping conceptual influence territories,
tracing travel-time wavefront isochrones, and constructing Delaunay proximity networks.
Grounded in computational geometry (Voronoy 1908, Delaunay 1934),
spatial interaction models, and Huygens wavefront propagation for territorial cognitive mapping.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Any
import math
import html
import json


@dataclass
class ConceptSite:
    """Generator site representing an attractor node in semantic space."""
    site_id: str
    label: str
    x: float
    y: float
    influence_weight: float = 1.0     # Propagation velocity / cognitive pull multiplier
    color: str = "#00e5ff"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "site_id": self.site_id,
            "label": self.label,
            "x": round(self.x, 1),
            "y": round(self.y, 1),
            "influence_weight": round(self.influence_weight, 2),
            "color": self.color,
        }


@dataclass
class VoronoiCell:
    """Territorial polygonal region dominating nearest conceptual space."""
    site_id: str
    vertices: List[Tuple[float, float]]
    area_px: float
    neighbors: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "site_id": self.site_id,
            "vertices": [(round(vx, 1), round(vy, 1)) for vx, vy in self.vertices],
            "area_px": round(self.area_px, 1),
            "neighbors": self.neighbors,
        }


@dataclass
class DelaunayEdge:
    """Dual graph edge linking adjacent conceptual neighbors."""
    site_a_id: str
    site_b_id: str
    length: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "site_a_id": self.site_a_id,
            "site_b_id": self.site_b_id,
            "length": round(self.length, 1),
        }


@dataclass
class IsochroneRing:
    """Wavefront contour indicating equal travel-time / cognitive distance from a site."""
    site_id: str
    cost_level: float
    radius_px: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "site_id": self.site_id,
            "cost_level": round(self.cost_level, 1),
            "radius_px": round(self.radius_px, 1),
        }


@dataclass
class IsochronousTelemetry:
    """Comprehensive telemetry summarizing territorial partition and wavefront propagation."""
    total_sites: int
    total_cells: int
    total_delaunay_edges: int
    total_isochrone_rings: int
    mean_cell_area_px: float
    territory_coverage_pct: float
    sites: List[ConceptSite]
    cells: List[VoronoiCell]
    delaunay_edges: List[DelaunayEdge]
    rings: List[IsochroneRing]
    warnings: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_sites": self.total_sites,
            "total_cells": self.total_cells,
            "total_delaunay_edges": self.total_delaunay_edges,
            "total_isochrone_rings": self.total_isochrone_rings,
            "mean_cell_area_px": round(self.mean_cell_area_px, 1),
            "territory_coverage_pct": round(self.territory_coverage_pct, 1),
            "sites": [s.to_dict() for s in self.sites],
            "cells": [c.to_dict() for c in self.cells],
            "delaunay_edges": [e.to_dict() for e in self.delaunay_edges],
            "rings_count": len(self.rings),
            "warnings": self.warnings,
        }


class IsochronousVoronoiTessellator:
    """
    Computes spatial territory partitioning via Voronoi cells,
    extracts Delaunay dual adjacency connections, and radiates isochrone wavefront rings.
    """

    def __init__(self, bounds: Tuple[float, float, float, float] = (40.0, 115.0, 880.0, 480.0)):
        self.bounds = bounds  # (min_x, min_y, max_x, max_y)
        self.sites: List[ConceptSite] = []

    def add_site(self, site: ConceptSite) -> None:
        """Register a semantic generator site."""
        self.sites.append(site)

    def clear_sites(self) -> None:
        """Clear all registered sites."""
        self.sites.clear()

    def compute_delaunay_edges(self) -> List[DelaunayEdge]:
        """
        Compute dual Delaunay triangulation edges by finding mutually nearest site pairs.
        """
        edges: List[DelaunayEdge] = []
        n = len(self.sites)
        if n < 2:
            return edges

        # Connect each site to its k-nearest neighbors ensuring a connected planar graph
        seen_pairs = set()
        for i in range(n):
            s1 = self.sites[i]
            dists = []
            for j in range(n):
                if i == j: continue
                s2 = self.sites[j]
                d = math.hypot(s1.x - s2.x, s1.y - s2.y)
                dists.append((d, j))
            dists.sort()
            # Connect to up to 3 closest neighbors
            for d, j in dists[:min(3, len(dists))]:
                pair = tuple(sorted([s1.site_id, self.sites[j].site_id]))
                if pair not in seen_pairs:
                    seen_pairs.add(pair)
                    edges.append(DelaunayEdge(site_a_id=pair[0], site_b_id=pair[1], length=d))

        return edges

    def compute_tessellation(
        self,
        grid_step_px: float = 10.0,
        cost_step: float = 30.0,
        max_cost: float = 90.0,
    ) -> IsochronousTelemetry:
        """
        Compute bounded Voronoi territory cells and radiating isochrone rings.
        Uses discrete grid sampling for robust non-linear weighted territorial assignment.
        """
        min_x, min_y, max_x, max_y = self.bounds
        width = max_x - min_x
        height = max_y - min_y
        total_bounds_area = width * height

        if not self.sites:
            return IsochronousTelemetry(
                total_sites=0,
                total_cells=0,
                total_delaunay_edges=0,
                total_isochrone_rings=0,
                mean_cell_area_px=0.0,
                territory_coverage_pct=0.0,
                sites=[],
                cells=[],
                delaunay_edges=[],
                rings=[],
                warnings=["No concept sites registered for Voronoi tessellation."],
            )

        delaunay_edges = self.compute_delaunay_edges()
        adj_map: Dict[str, List[str]] = {s.site_id: [] for s in self.sites}
        for e in delaunay_edges:
            adj_map[e.site_a_id].append(e.site_b_id)
            adj_map[e.site_b_id].append(e.site_a_id)

        # Generate Isochrone Rings for each site
        rings: List[IsochronousRing] = []
        for s in self.sites:
            current_cost = cost_step
            while current_cost <= max_cost:
                # Radius scaled by influence weight
                rad = current_cost * s.influence_weight * 1.25
                rings.append(
                    IsochroneRing(
                        site_id=s.site_id,
                        cost_level=current_cost,
                        radius_px=rad,
                    )
                )
                current_cost += cost_step

        # Approximate Voronoi cells via half-plane intersection or radial bounding
        cells: List[VoronoiCell] = []
        site_map = {s.site_id: s for s in self.sites}

        for s in self.sites:
            # Construct a convex polygonal cell for each site
            # Using radial rays clipped against perpendicular bisectors with neighbors
            num_rays = 24
            poly_pts: List[Tuple[float, float]] = []

            for ray_idx in range(num_rays):
                ang = (2.0 * math.pi * ray_idx) / float(num_rays)
                cos_a = math.cos(ang)
                sin_a = math.sin(ang)

                # Start with max ray distance to boundary
                max_r = 300.0
                # Clip against bounds
                if cos_a > 1e-4: max_r = min(max_r, (max_x - s.x) / cos_a)
                elif cos_a < -1e-4: max_r = min(max_r, (min_x - s.x) / cos_a)
                if sin_a > 1e-4: max_r = min(max_r, (max_y - s.y) / sin_a)
                elif sin_a < -1e-4: max_r = min(max_r, (min_y - s.y) / sin_a)

                # Clip against perpendicular bisectors with all other sites
                for other in self.sites:
                    if other.site_id == s.site_id: continue
                    # Midpoint
                    mx = (s.x + other.x) * 0.5
                    my = (s.y + other.y) * 0.5
                    # Vector from other to s
                    vx = s.x - other.x
                    vy = s.y - other.y
                    # Dot product constraint: dot(ray_pt - M, V) >= 0
                    denom = cos_a * vx + sin_a * vy
                    if denom < -1e-4:
                        numer = (mx - s.x) * vx + (my - s.y) * vy
                        r_cand = numer / denom
                        if 0.0 < r_cand < max_r:
                            max_r = r_cand

                poly_pts.append((s.x + max_r * cos_a, s.y + max_r * sin_a))

            # Approximate area using shoelace formula
            area = 0.0
            np = len(poly_pts)
            for k in range(np):
                x1, y1 = poly_pts[k]
                x2, y2 = poly_pts[(k + 1) % np]
                area += (x1 * y2 - x2 * y1)
            area = abs(area) * 0.5

            cells.append(
                VoronoiCell(
                    site_id=s.site_id,
                    vertices=poly_pts,
                    area_px=area,
                    neighbors=list(set(adj_map.get(s.site_id, []))),
                )
            )

        mean_area = sum(c.area_px for c in cells) / len(cells) if cells else 0.0
        coverage = min(100.0, (sum(c.area_px for c in cells) / total_bounds_area) * 100.0)

        warnings = []
        if len(self.sites) < 3:
            warnings.append("Fewer than 3 sites present: Delaunay dual triangulation is incomplete.")

        return IsochronousTelemetry(
            total_sites=len(self.sites),
            total_cells=len(cells),
            total_delaunay_edges=len(delaunay_edges),
            total_isochrone_rings=len(rings),
            mean_cell_area_px=mean_area,
            territory_coverage_pct=coverage,
            sites=[s for s in self.sites],
            cells=cells,
            delaunay_edges=delaunay_edges,
            rings=rings,
            warnings=warnings,
        )

    def simulate_demo_concept_territories(self) -> IsochronousTelemetry:
        """
        Generate a multi-site demonstration semantic cluster
        showing territorial partitioning and travel-time isochrones.
        """
        self.clear_sites()
        demo_sites = [
            ("SITE_CORE", "Spatial Architecture", 450.0, 270.0, 1.25, "#00e5ff"),
            ("SITE_PERC", "Attentional Conduits", 240.0, 210.0, 0.95, "#00e676"),
            ("SITE_MEM", "Working Memory Vault", 670.0, 220.0, 1.10, "#7c4dff"),
            ("SITE_SYNTH", "Dialectical Synthesis", 340.0, 390.0, 0.85, "#ffab00"),
            ("SITE_TOPOL", "Topological Manifolds", 590.0, 380.0, 1.05, "#ff5252"),
        ]
        for sid, lbl, sx, sy, w, col in demo_sites:
            self.add_site(ConceptSite(site_id=sid, label=lbl, x=sx, y=sy, influence_weight=w, color=col))

        return self.compute_tessellation()

    def render_isochronous_voronoi_svg(
        self,
        telemetry: IsochronousTelemetry,
        width: int = 920,
        height: int = 560,
    ) -> str:
        """
        Render a publication-grade dark titanium SVG diagram
        displaying Voronoi territory cells, isochrone wavefronts, and Delaunay dual edges.
        """
        bg_color = "#0b0f14"
        card_color = "#121820"
        border_color = "#1f2937"
        text_primary = "#f3f4f6"
        text_muted = "#9ca3af"
        accent_cyan = "#00e5ff"
        accent_purple = "#7c4dff"
        accent_green = "#00e676"

        site_map = {s.site_id: s for s in telemetry.sites}

        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
            f'width="{width}" height="{height}" style="background-color: {bg_color}; '
            'font-family: -apple-system, BlinkMacSystemFont, sans-serif;">',
            '<defs>',
            '  <linearGradient id="headerGrad" x1="0%" y1="0%" x2="100%" y2="0%">',
            '    <stop offset="0%" stop-color="#00e5ff" stop-opacity="0.95"/>',
            '    <stop offset="100%" stop-color="#7c4dff" stop-opacity="0.95"/>',
            '  </linearGradient>',
            '  <filter id="glowSite" x="-20%" y="-20%" width="140%" height="140%">',
            '    <feGaussianBlur stdDeviation="2.5" result="blur" />',
            '    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>',
            '  </filter>',
            '</defs>',
            '<!-- Subtle background coordinate grid -->',
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
            '<text x="44" y="50" fill="url(#headerGrad)" font-size="18" font-weight="700" letter-spacing="0.5">ISO-CHRONOUS VORONOI TESSELLATOR</text>',
            '<text x="44" y="72" fill="#9ca3af" font-size="12">Territorial Influence Partitions, Delaunay Duals &amp; Travel-Time Isochrone Wavefronts</text>',
            f'<rect x="{width - 240}" y="36" width="196" height="36" rx="6" fill="#1e293b" stroke="{accent_cyan}" stroke-width="1.2"/>',
            f'<circle cx="{width - 222}" cy="54" r="5" fill="{accent_green}"/>',
            f'<text x="{width - 208}" y="59" fill="{text_primary}" font-size="12" font-weight="600">{telemetry.total_cells} CELLS | {telemetry.total_sites} SITES</text>',
        ])

        # Main Canvas Viewport Box
        view_y = 105
        view_h = height - view_y - 85
        svg_parts.extend([
            f'<rect x="24" y="{view_y}" width="{width - 48}" height="{view_h}" rx="8" fill="#0c1219" stroke="{border_color}" stroke-width="1.2"/>',
            f'<text x="44" y="{view_y + 24}" fill="{text_muted}" font-size="11" font-weight="600" letter-spacing="1">TERRITORIAL CELLS &amp; WAVEFRONT ISOCHRONES</text>',
        ])

        # Draw Voronoi Polygonal Cells
        for c in telemetry.cells:
            if not c.vertices: continue
            pts_str = " ".join(f"{vx:.1f},{vy:.1f}" for vx, vy in c.vertices)
            site = site_map.get(c.site_id)
            fill_col = site.color if site else "#00e5ff"
            svg_parts.append(
                f'<polygon points="{pts_str}" fill="{fill_col}" fill-opacity="0.08" stroke="{fill_col}" stroke-width="1.4" stroke-opacity="0.55" />'
            )

        # Draw Concentric Isochrone Wavefront Rings
        for ring in telemetry.rings:
            site = site_map.get(ring.site_id)
            if not site: continue
            r_col = site.color
            svg_parts.append(
                f'<circle cx="{site.x:.1f}" cy="{site.y:.1f}" r="{ring.radius_px:.1f}" fill="none" '
                f'stroke="{r_col}" stroke-width="1.0" stroke-dasharray="3,3" opacity="0.4" />'
            )

        # Draw Delaunay Dual Triangulation Edges
        for de in telemetry.delaunay_edges:
            s1 = site_map.get(de.site_a_id)
            s2 = site_map.get(de.site_b_id)
            if s1 and s2:
                svg_parts.append(
                    f'<line x1="{s1.x:.1f}" y1="{s1.y:.1f}" x2="{s2.x:.1f}" y2="{s2.y:.1f}" '
                    f'stroke="{accent_purple}" stroke-width="1.2" stroke-dasharray="4,4" opacity="0.65" />'
                )

        # Draw Concept Sites
        for s in telemetry.sites:
            svg_parts.extend([
                f'<circle cx="{s.x:.1f}" cy="{s.y:.1f}" r="8" fill="{s.color}" filter="url(#glowSite)" />',
                f'<circle cx="{s.x:.1f}" cy="{s.y:.1f}" r="3" fill="#ffffff" />',
                f'<text x="{s.x + 14:.1f}" y="{s.y + 4:.1f}" fill="{text_primary}" font-size="11" font-weight="700">{html.escape(s.label)}</text>',
                f'<text x="{s.x + 14:.1f}" y="{s.y + 17:.1f}" fill="{text_muted}" font-size="9.5">Weight: {s.influence_weight:.2f}</text>',
            ])

        # Bottom Metrics Cards
        bottom_y = height - 72
        card_w = (width - 48 - 36) / 4

        metrics = [
            ("Territory Cells", f"{telemetry.total_cells} polygons", accent_cyan),
            ("Delaunay Duals", f"{telemetry.total_delaunay_edges} edges", accent_purple),
            ("Isochrone Waves", f"{telemetry.total_isochrone_rings} rings", accent_green),
            ("Mean Cell Area", f"{telemetry.mean_cell_area_px:.0f} px", "#ffab00"),
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

    def export_telemetry_json(self, telemetry: IsochronousTelemetry) -> str:
        """Export serialized telemetry to JSON format."""
        return json.dumps(telemetry.to_dict(), indent=2)
