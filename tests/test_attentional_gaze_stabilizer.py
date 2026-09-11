"""
Unit tests for Attentional Gaze Stabilizer & Scanpath Limiter Engine.
Verifies Carpenter LATER drift limitation, Bouma visual crowding corridor containment,
jitter dampening mathematics, SVG rendering, and diagnostic reporting.
Strictly zero em dash compliance.
"""

import pytest
import math
from scripts.attentional_gaze_stabilizer import (
    GazePoint,
    AttentionalChannel,
    StabilizedPoint,
    GazeStabilizationTelemetry,
    AttentionalGazeStabilizer,
)


def test_gaze_point_and_channel_creation():
    gp = GazePoint("gp-1", 120.5, 240.2, timestamp_ms=500.0, fixation_dwell_ms=180.0, is_fixation=True)
    assert gp.point_id == "gp-1"
    assert gp.x == 120.5
    assert gp.y == 240.2
    d = gp.to_dict()
    assert d["point_id"] == "gp-1"
    assert d["fixation_dwell_ms"] == 180.0

    ch = AttentionalChannel("ch-1", "Spine A", [(0.0, 0.0), (100.0, 0.0)], envelope_width_px=60.0)
    assert ch.channel_id == "ch-1"
    assert len(ch.points) == 2
    cd = ch.to_dict()
    assert cd["envelope_width_px"] == 60.0


def test_distance_point_to_segment():
    # Segment (0, 0) to (100, 0)
    # Point at (50, 20) -> distance is 20, projection is (50, 0)
    dist, proj = AttentionalGazeStabilizer.distance_point_to_segment(50.0, 20.0, 0.0, 0.0, 100.0, 0.0)
    assert math.isclose(dist, 20.0, abs_tol=1e-5)
    assert math.isclose(proj[0], 50.0, abs_tol=1e-5)
    assert math.isclose(proj[1], 0.0, abs_tol=1e-5)

    # Point at (-20, 0) -> clamped to (0, 0), distance 20
    dist, proj = AttentionalGazeStabilizer.distance_point_to_segment(-20.0, 0.0, 0.0, 0.0, 100.0, 0.0)
    assert math.isclose(dist, 20.0, abs_tol=1e-5)
    assert math.isclose(proj[0], 0.0, abs_tol=1e-5)


def test_stabilize_scanpath_empty():
    stabilizer = AttentionalGazeStabilizer()
    telemetry = stabilizer.stabilize_scanpath([], [])
    assert telemetry.total_gaze_points == 0
    assert telemetry.envelope_containment_rate == 1.0
    assert telemetry.mean_drift_px == 0.0
    assert telemetry.status_level == "OPTIMAL"


def test_stabilize_scanpath_no_channels():
    pts = [
        GazePoint("p1", 10.0, 10.0, 0.0, 100.0, True),
        GazePoint("p2", 20.0, 20.0, 100.0, 100.0, True),
    ]
    stabilizer = AttentionalGazeStabilizer()
    telemetry = stabilizer.stabilize_scanpath(pts, [])
    assert telemetry.total_gaze_points == 2
    assert telemetry.envelope_containment_rate == 1.0
    assert telemetry.drift_alerts_count == 0


def test_stabilize_scanpath_strictly_within_envelope():
    channel = AttentionalChannel("ch-1", "Straight Spine", [(0.0, 50.0), (200.0, 50.0)], envelope_width_px=40.0)
    # Points exactly on the spine
    pts = [
        GazePoint("p1", 10.0, 50.0, 0.0, 150.0, True),
        GazePoint("p2", 50.0, 50.0, 150.0, 150.0, True),
        GazePoint("p3", 100.0, 50.0, 300.0, 150.0, True),
        GazePoint("p4", 150.0, 50.0, 450.0, 150.0, True),
    ]
    stabilizer = AttentionalGazeStabilizer(default_envelope_width_px=40.0)
    telemetry = stabilizer.stabilize_scanpath(pts, [channel])
    assert telemetry.total_gaze_points == 4
    assert telemetry.envelope_containment_rate == 1.0
    assert telemetry.drift_alerts_count == 0
    assert math.isclose(telemetry.mean_drift_px, 0.0, abs_tol=1e-5)
    assert telemetry.status_level == "OPTIMAL"


def test_stabilize_scanpath_with_drift_damping():
    channel = AttentionalChannel("ch-1", "Horizontal Corridor", [(0.0, 100.0), (300.0, 100.0)], envelope_width_px=50.0)
    # Half width is 25.0
    # Point at y=110 (drift 10 <= 25, inside)
    # Point at y=160 (drift 60 > 25, outside alert)
    pts = [
        GazePoint("p1", 50.0, 110.0, 0.0, 150.0, True),
        GazePoint("p2", 100.0, 160.0, 150.0, 150.0, True),
        GazePoint("p3", 150.0, 95.0, 300.0, 150.0, True),
    ]
    stabilizer = AttentionalGazeStabilizer(default_envelope_width_px=50.0, jitter_damping_factor=0.6)
    telemetry = stabilizer.stabilize_scanpath(pts, [channel])

    assert telemetry.total_gaze_points == 3
    assert telemetry.drift_alerts_count == 1
    assert telemetry.envelope_containment_rate == pytest.approx(2.0 / 3.0, 0.01)
    
    # Check that p2 was pulled toward y=100
    p2_stab = telemetry.stabilized_points[1]
    assert p2_stab.stabilized_y < 160.0
    assert p2_stab.is_within_envelope is False
    assert p2_stab.jitter_dampened_px > 0.0


def test_demo_telemetry_generation():
    demo = AttentionalGazeStabilizer.create_demo_telemetry()
    assert demo.total_gaze_points == 14
    assert demo.fixation_count >= 10
    assert len(demo.channels) == 3
    assert demo.envelope_containment_rate > 0.70
    assert demo.jitter_reduction_percent > 0.0

    d = demo.to_dict()
    assert "status_level" in d
    assert "envelope_containment_rate" in d


def test_markdown_report_formatting():
    stabilizer = AttentionalGazeStabilizer()
    demo = stabilizer.create_demo_telemetry()
    report = stabilizer.generate_markdown_report(demo)

    assert "# Attentional Gaze Stabilizer" in report
    assert "Carpenter LATER" in report
    assert "Bouma Visual Crowding" in report
    assert "| Telemetry Parameter |" in report
    assert chr(8212) not in report, "Em dash found in markdown report!"


def test_svg_rendering_integrity():
    stabilizer = AttentionalGazeStabilizer()
    demo = stabilizer.create_demo_telemetry()
    svg = stabilizer.generate_svg(demo, width=860, height=560)

    assert '<svg xmlns="http://www.w3.org/2000/svg"' in svg
    assert 'viewBox="0 0 860 560"' in svg
    assert 'polyline' in svg
    assert 'Gaze Stabilization Telemetry' in svg
    assert 'Scanpath Legend' in svg
    assert chr(8212) not in svg, "Em dash found in SVG output!"


def test_zero_em_dashes_enforcement():
    with open("scripts/attentional_gaze_stabilizer.py", "r", encoding="utf-8") as f:
        src = f.read()
    assert chr(8212) not in src, "Em dash found in attentional_gaze_stabilizer.py!"
