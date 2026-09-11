"""
Tests for Topographic Contour Morph & Iso-Semantic Isocline Tracer
Validates continuous digital elevation model interpolation, marching squares isocline tracing,
index contour classification, SVG relief rendering, and zero em dash compliance.
"""

import os
import sys
import math
import json
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.topographic_contour_morph import (
    TopographicContourMorph,
    ElevationSummit,
    IsoclineLevel,
    TopographicTelemetry,
)


def test_empty_summits():
    morph = TopographicContourMorph()
    telemetry = morph.trace_isoclines()
    assert telemetry.total_summits == 0
    assert telemetry.total_isocline_levels == 0
    assert telemetry.total_segments == 0
    assert len(telemetry.warnings) > 0


def test_add_and_clear_summits():
    morph = TopographicContourMorph()
    s1 = ElevationSummit("S1", "Concept Alpha", 200.0, 200.0, 500.0)
    s2 = ElevationSummit("S2", "Concept Beta", 400.0, 300.0, 750.0)
    morph.add_summit(s1)
    morph.add_summit(s2)
    assert len(morph.summits) == 2

    morph.clear_summits()
    assert len(morph.summits) == 0


def test_scalar_field_evaluation():
    morph = TopographicContourMorph()
    s = ElevationSummit("PEAK", "Summit Peak", 300.0, 300.0, elevation=600.0, spread_sigma=50.0)
    morph.add_summit(s)

    at_peak = morph.evaluate_field_at(300.0, 300.0)
    distant = morph.evaluate_field_at(600.0, 600.0)
    assert at_peak > distant
    assert at_peak >= 650.0  # 600 peak + 50 baseline
    assert distant < 100.0


def test_isocline_tracing_marching_squares():
    morph = TopographicContourMorph()
    telemetry = morph.simulate_demo_semantic_terrain()
    assert telemetry.total_summits == 4
    assert telemetry.max_elevation > 700.0
    assert telemetry.min_elevation >= 50.0
    assert telemetry.total_isocline_levels > 3
    assert telemetry.total_segments > 20
    assert telemetry.terrain_ruggedness_index > 0.0


def test_index_contour_flagging():
    morph = TopographicContourMorph(base_contour_interval=50.0)
    s = ElevationSummit("HIGH", "Highland", 400.0, 300.0, elevation=800.0, spread_sigma=80.0)
    morph.add_summit(s)
    telemetry = morph.trace_isoclines(contour_interval=50.0)

    # Check that some levels are flagged as index contours (multiples of 5 * 50 = 250)
    has_index = any(lvl.is_index_contour for lvl in telemetry.levels)
    assert has_index is True


def test_svg_rendering():
    morph = TopographicContourMorph()
    telemetry = morph.simulate_demo_semantic_terrain()
    svg = morph.render_topographic_svg(telemetry, width=920, height=560)
    assert "<svg" in svg
    assert "</svg>" in svg
    assert "#0b0f14" in svg
    assert "TOPOGRAPHIC CONTOUR MORPH" in svg
    assert "Peak Elevation" in svg
    assert "Terrain Ruggedness" in svg


def test_export_telemetry_json():
    morph = TopographicContourMorph()
    telemetry = morph.simulate_demo_semantic_terrain()
    json_str = morph.export_telemetry_json(telemetry)
    data = json.loads(json_str)
    assert "total_summits" in data
    assert "contour_interval" in data
    assert "total_isocline_levels" in data
    assert len(data["summits"]) == 4


def test_zero_em_dashes():
    """Verify zero em dashes in script and test files."""
    script_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "scripts", "topographic_contour_morph.py")
    )
    with open(script_path, "r", encoding="utf-8") as f:
        script_code = f.read()
    assert chr(8212) not in script_code, "Unicode em dash found in topographic_contour_morph.py"

    test_path = os.path.abspath(__file__)
    with open(test_path, "r", encoding="utf-8") as f:
        test_code = f.read()
    assert chr(8212) not in test_code, "Unicode em dash found in test_topographic_contour_morph.py"
