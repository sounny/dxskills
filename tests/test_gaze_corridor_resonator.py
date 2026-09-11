"""
Unit tests for Gaze Corridor Resonator & Dynamic Attentional Funnel Engine.
Verifies velocity calculation, lookahead distance estimation, adaptive conduit aperture,
SVG rendering, and diagnostic reporting.
Strictly zero em dash compliance.
"""

import pytest
import math
from scripts.gaze_corridor_resonator import (
    GazeSample,
    ResonantCorridorSegment,
    GazeCorridorTelemetry,
    GazeCorridorResonator,
)


def test_gaze_sample_and_segment_creation():
    s = GazeSample(
        sample_id="s-1",
        x=120.0,
        y=240.0,
        timestamp_ms=150.0,
        dwell_ms=130.0,
        modality="CODE",
    )
    assert s.sample_id == "s-1"
    d = s.to_dict()
    assert d["sample_id"] == "s-1"
    assert d["modality"] == "CODE"

    seg = ResonantCorridorSegment(
        segment_id="seg-1",
        start_x=100.0,
        start_y=100.0,
        target_x=200.0,
        target_y=100.0,
        velocity_px_ms=0.5,
        lookahead_px=45.0,
        funnel_radius_px=60.0,
        preview_cone_angle_deg=40.0,
        resonance_efficiency=0.88,
    )
    assert seg.segment_id == "seg-1"
    sd = seg.to_dict()
    assert sd["velocity_px_ms"] == 0.5
    assert sd["resonance_efficiency"] == 0.88


def test_synchronize_corridor_empty():
    resonator = GazeCorridorResonator()
    telemetry = resonator.synchronize_corridor([])
    assert telemetry.total_samples == 0
    assert len(telemetry.segments) == 0
    assert telemetry.mean_scanpath_velocity == 0.0
    assert telemetry.status_level == "SYNCHRONIZED"


def test_synchronize_corridor_single_sample():
    resonator = GazeCorridorResonator()
    s = GazeSample("s-0", 50.0, 50.0, 0.0)
    telemetry = resonator.synchronize_corridor([s])
    assert telemetry.total_samples == 1
    assert len(telemetry.segments) == 0


def test_synchronize_corridor_velocity_and_lookahead():
    resonator = GazeCorridorResonator(saccadic_latency_ms=200.0, base_aperture_px=40.0, velocity_scale=50.0)
    # Distance = 100 px, delta_t = 100 ms -> v = 1.0 px/ms
    s1 = GazeSample("s1", 100.0, 100.0, timestamp_ms=0.0)
    s2 = GazeSample("s2", 200.0, 100.0, timestamp_ms=100.0)

    telemetry = resonator.synchronize_corridor([s1, s2])
    assert len(telemetry.segments) == 1
    seg = telemetry.segments[0]
    assert math.isclose(seg.velocity_px_ms, 1.0, abs_tol=1e-3)
    # lookahead = 1.0 * (200 * 0.5) = 100.0
    assert math.isclose(seg.lookahead_px, 200.0, abs_tol=1e-3)
    # aperture = 40.0 + 1.0 * 50.0 = 90.0
    assert math.isclose(seg.funnel_radius_px, 90.0, abs_tol=1e-3)


def test_synchronize_corridor_overdrive_detection():
    resonator = GazeCorridorResonator()
    # Distance = 400 px in 50 ms -> v = 8.0 px/ms (> 1.8 px/ms overdrive)
    s1 = GazeSample("s1", 0.0, 0.0, timestamp_ms=0.0)
    s2 = GazeSample("s2", 400.0, 0.0, timestamp_ms=50.0)

    telemetry = resonator.synchronize_corridor([s1, s2])
    assert telemetry.overdrive_events_count == 1
    assert telemetry.peak_saccade_velocity > 1.8


def test_demo_telemetry_generation():
    demo = GazeCorridorResonator.create_demo_telemetry()
    assert demo.total_samples == 8
    assert len(demo.segments) == 7
    assert demo.mean_scanpath_velocity > 0.0
    assert demo.parafoveal_synchrony_rate > 0.60
    assert demo.status_level in ["SYNCHRONIZED", "CALIBRATED"]

    d = demo.to_dict()
    assert "mean_scanpath_velocity" in d
    assert "parafoveal_synchrony_rate" in d


def test_markdown_report_formatting():
    resonator = GazeCorridorResonator()
    demo = resonator.create_demo_telemetry()
    report = resonator.generate_markdown_report(demo)

    assert "# Gaze Corridor Resonator" in report
    assert "Keith Rayner Reading Paradigm" in report
    assert "| Telemetry Metric |" in report
    assert "| Segment |" in report
    assert chr(8212) not in report, "Em dash found in markdown report!"


def test_svg_rendering_integrity():
    resonator = GazeCorridorResonator()
    demo = resonator.create_demo_telemetry()
    svg = resonator.generate_svg(demo, width=880, height=580)

    assert '<svg xmlns="http://www.w3.org/2000/svg"' in svg
    assert 'viewBox="0 0 880 580"' in svg
    assert 'GAZE CORRIDOR RESONATOR' in svg
    assert 'Corridor Resonance Telemetry' in svg
    assert 'Gaze Corridor Legend' in svg
    assert chr(8212) not in svg, "Em dash found in SVG output!"


def test_zero_em_dashes_enforcement():
    with open("scripts/gaze_corridor_resonator.py", "r", encoding="utf-8") as f:
        src = f.read()
    assert chr(8212) not in src, "Em dash found in gaze_corridor_resonator.py!"
