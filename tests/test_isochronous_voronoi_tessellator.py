"""
Tests for Iso-Chronous Voronoi Isochrone Tessellator & Proximity Loom
Validates Voronoi territorial cell partitions, Delaunay dual triangulation graphs,
travel-time wavefront isochrones, SVG rendering, and zero em dash compliance.
"""

import os
import sys
import math
import json
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.isochronous_voronoi_tessellator import (
    IsochronousVoronoiTessellator,
    ConceptSite,
    VoronoiCell,
    DelaunayEdge,
    IsochroneRing,
    IsochronousTelemetry,
)


def test_empty_sites():
    tessellator = IsochronousVoronoiTessellator()
    telemetry = tessellator.compute_tessellation()
    assert telemetry.total_sites == 0
    assert telemetry.total_cells == 0
    assert telemetry.total_delaunay_edges == 0
    assert len(telemetry.warnings) > 0


def test_add_and_clear_sites():
    tessellator = IsochronousVoronoiTessellator()
    s1 = ConceptSite("S1", "Node A", 100.0, 100.0)
    s2 = ConceptSite("S2", "Node B", 300.0, 200.0)
    tessellator.add_site(s1)
    tessellator.add_site(s2)
    assert len(tessellator.sites) == 2

    tessellator.clear_sites()
    assert len(tessellator.sites) == 0


def test_delaunay_edge_generation():
    tessellator = IsochronousVoronoiTessellator()
    tessellator.add_site(ConceptSite("A", "Alpha", 100.0, 100.0))
    tessellator.add_site(ConceptSite("B", "Beta", 250.0, 120.0))
    tessellator.add_site(ConceptSite("C", "Gamma", 150.0, 280.0))
    edges = tessellator.compute_delaunay_edges()
    assert len(edges) >= 2
    for e in edges:
        assert e.length > 0.0
        assert e.site_a_id != e.site_b_id


def test_voronoi_tessellation_computation():
    tessellator = IsochronousVoronoiTessellator()
    telemetry = tessellator.simulate_demo_concept_territories()
    assert telemetry.total_sites == 5
    assert telemetry.total_cells == 5
    assert telemetry.mean_cell_area_px > 1000.0
    for cell in telemetry.cells:
        assert len(cell.vertices) >= 6
        assert cell.area_px > 0.0


def test_isochrone_rings_scaling():
    tessellator = IsochronousVoronoiTessellator()
    tessellator.add_site(ConceptSite("LOW", "Low Impact", 200.0, 200.0, influence_weight=0.5))
    tessellator.add_site(ConceptSite("HIGH", "High Impact", 500.0, 300.0, influence_weight=1.5))
    telemetry = tessellator.compute_tessellation(cost_step=20.0, max_cost=40.0)

    # 2 rings per site = 4 total
    assert telemetry.total_isochrone_rings == 4
    low_rings = [r for r in telemetry.rings if r.site_id == "LOW"]
    high_rings = [r for r in telemetry.rings if r.site_id == "HIGH"]
    assert len(low_rings) == 2
    assert len(high_rings) == 2
    # High weight site has larger isochrone radii for the same cost
    assert high_rings[0].radius_px > low_rings[0].radius_px


def test_svg_rendering():
    tessellator = IsochronousVoronoiTessellator()
    telemetry = tessellator.simulate_demo_concept_territories()
    svg = tessellator.render_isochronous_voronoi_svg(telemetry, width=920, height=560)
    assert "<svg" in svg
    assert "</svg>" in svg
    assert "#0b0f14" in svg
    assert "ISO-CHRONOUS VORONOI TESSELLATOR" in svg
    assert "Territory Cells" in svg
    assert "Delaunay Duals" in svg


def test_export_telemetry_json():
    tessellator = IsochronousVoronoiTessellator()
    telemetry = tessellator.simulate_demo_concept_territories()
    json_str = tessellator.export_telemetry_json(telemetry)
    data = json.loads(json_str)
    assert "total_sites" in data
    assert "total_cells" in data
    assert "mean_cell_area_px" in data
    assert len(data["cells"]) == 5


def test_zero_em_dashes():
    """Verify zero em dashes in script and test files."""
    script_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "scripts", "isochronous_voronoi_tessellator.py")
    )
    with open(script_path, "r", encoding="utf-8") as f:
        script_code = f.read()
    assert chr(8212) not in script_code, "Unicode em dash found in isochronous_voronoi_tessellator.py"

    test_path = os.path.abspath(__file__)
    with open(test_path, "r", encoding="utf-8") as f:
        test_code = f.read()
    assert chr(8212) not in test_code, "Unicode em dash found in test_isochronous_voronoi_tessellator.py"
