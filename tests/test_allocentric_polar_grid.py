"""
Unit tests for Allocentric Landmark Polar Grid & Dynamic Bearing Synthesizer Engine.
Verifies polar coordinates, cardinal ray bearings, concentric distance zones,
dispersion metrics, SVG rendering, markdown reporting, and strict zero-em-dash compliance.
"""

import os
import pytest
from scripts.allocentric_polar_grid import (
    PolarLandmark,
    TargetBearing,
    PolarGridTelemetry,
    AllocentricPolarGridSynthesizer,
    sample_polar_session,
)


def test_polar_landmark_initialization():
    lm = PolarLandmark(
        landmark_id="lm-01",
        title="Primary System Kernel",
        x=400.0,
        y=300.0,
        radius_px=20.0,
        is_primary=True,
    )
    assert lm.landmark_id == "lm-01"
    assert lm.title == "Primary System Kernel"
    assert lm.x == 400.0
    assert lm.y == 300.0
    assert lm.radius_px == 20.0
    assert lm.is_primary is True


def test_target_bearing_initialization():
    bearing = TargetBearing(
        target_id="tgt-1",
        title="Cache Layer",
        pos_x=400.0,
        pos_y=200.0,
        distance_px=100.0,
        bearing_deg=0.0,
        cardinal_heading="N",
        range_ring_zone="Inner Core",
    )
    assert bearing.target_id == "tgt-1"
    assert bearing.title == "Cache Layer"
    assert bearing.distance_px == 100.0
    assert bearing.bearing_deg == 0.0
    assert bearing.cardinal_heading == "N"
    assert bearing.range_ring_zone == "Inner Core"


def test_resolve_cardinal_heading():
    resolve = AllocentricPolarGridSynthesizer.resolve_cardinal_heading
    assert resolve(0.0) == "N"
    assert resolve(45.0) == "NE"
    assert resolve(90.0) == "E"
    assert resolve(135.0) == "SE"
    assert resolve(180.0) == "S"
    assert resolve(225.0) == "SW"
    assert resolve(270.0) == "W"
    assert resolve(315.0) == "NW"
    assert resolve(359.0) == "N"


def test_calculate_polar_bearings_empty():
    synthesizer = AllocentricPolarGridSynthesizer()
    lm = PolarLandmark("lm", "Hub", 100.0, 100.0)
    telemetry = synthesizer.calculate_polar_bearings(lm, [])

    assert telemetry.target_count == 0
    assert len(telemetry.target_bearings) == 0
    assert telemetry.allocentric_stability_score == 1.0


def test_calculate_polar_bearings_cardinal_alignment():
    synthesizer = AllocentricPolarGridSynthesizer()
    lm, targets = sample_polar_session()
    telemetry = synthesizer.calculate_polar_bearings(lm, targets)

    assert telemetry.target_count == 8
    assert len(telemetry.target_bearings) == 8

    # Find tgt-1 (North: x=460, y=180 -> dy=-100, dx=0 -> bearing 0.0 deg)
    t1 = next(b for b in telemetry.target_bearings if b.target_id == "tgt-1")
    assert t1.bearing_deg == pytest.approx(0.0, abs=0.1)
    assert t1.cardinal_heading == "N"
    assert t1.distance_px == pytest.approx(100.0, abs=0.1)

    # Find tgt-3 (East: x=680, y=280 -> dy=0, dx=220 -> bearing 90.0 deg)
    t3 = next(b for b in telemetry.target_bearings if b.target_id == "tgt-3")
    assert t3.bearing_deg == pytest.approx(90.0, abs=0.1)
    assert t3.cardinal_heading == "E"

    # Find tgt-5 (South: x=460, y=500 -> dy=220, dx=0 -> bearing 180.0 deg)
    t5 = next(b for b in telemetry.target_bearings if b.target_id == "tgt-5")
    assert t5.bearing_deg == pytest.approx(180.0, abs=0.1)
    assert t5.cardinal_heading == "S"

    # Find tgt-7 (West: x=200, y=280 -> dy=0, dx=-260 -> bearing 270.0 deg)
    t7 = next(b for b in telemetry.target_bearings if b.target_id == "tgt-7")
    assert t7.bearing_deg == pytest.approx(270.0, abs=0.1)
    assert t7.cardinal_heading == "W"


def test_range_ring_zones():
    synthesizer = AllocentricPolarGridSynthesizer(default_ring_interval_px=100.0)
    lm = PolarLandmark("lm", "Hub", 0.0, 0.0)
    targets = [
        {"id": "near", "title": "Near", "x": 0.0, "y": -50.0},     # 50px -> Inner Core
        {"id": "mid", "title": "Mid", "x": 150.0, "y": 0.0},       # 150px -> Meso Orbit
        {"id": "far", "title": "Far", "x": 0.0, "y": 250.0},       # 250px -> Peripheral Horizon
    ]
    telemetry = synthesizer.calculate_polar_bearings(lm, targets)
    zones = {b.target_id: b.range_ring_zone for b in telemetry.target_bearings}
    assert zones["near"] == "Inner Core"
    assert zones["mid"] == "Meso Orbit"
    assert zones["far"] == "Peripheral Horizon"


def test_generate_markdown_report():
    synthesizer = AllocentricPolarGridSynthesizer()
    lm, targets = sample_polar_session()
    telemetry = synthesizer.calculate_polar_bearings(lm, targets)
    report = synthesizer.generate_markdown_report(telemetry)

    assert "# Allocentric Landmark Polar Grid and Dynamic Bearing Report" in report
    assert "Burgess Allocentric Frame" in report
    assert "Kernel Dispatcher Hub" in report
    assert "Memory Allocator" in report


def test_generate_svg():
    synthesizer = AllocentricPolarGridSynthesizer()
    lm, targets = sample_polar_session()
    telemetry = synthesizer.calculate_polar_bearings(lm, targets)
    svg = synthesizer.generate_svg(telemetry, width=900, height=540)

    assert "<svg" in svg
    assert "</svg>" in svg
    assert "radarGlow" in svg
    assert "ALLOCENTRIC POLAR GRID HUD" in svg
    assert "KERNEL DISPATCHER HUB" in svg


def test_zero_em_dashes_in_source_and_outputs():
    # Verify module source file
    script_path = os.path.join(os.path.dirname(__file__), "..", "scripts", "allocentric_polar_grid.py")
    with open(script_path, "r", encoding="utf-8") as f:
        source = f.read()
    assert chr(8212) not in source

    # Verify report and svg outputs
    synthesizer = AllocentricPolarGridSynthesizer()
    lm, targets = sample_polar_session()
    telemetry = synthesizer.calculate_polar_bearings(lm, targets)
    report = synthesizer.generate_markdown_report(telemetry)
    svg = synthesizer.generate_svg(telemetry)

    assert chr(8212) not in report
    assert chr(8212) not in svg
