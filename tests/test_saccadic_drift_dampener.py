"""
Tests for Saccadic Drift Dampener & Retinal Latch Engine
Validates ocular jitter reduction, anchor latching mechanics, hysteresis thresholds,
mental rotation drift suppression, and zero em dash compliance.
"""

import os
import sys
import math
import json
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.saccadic_drift_dampener import (
    SaccadicDriftDampener,
    RetinalAnchor,
    DriftDampeningConfig,
    RetinalLatchTelemetry,
    DriftCorrectionStep,
)


def test_empty_stream():
    dampener = SaccadicDriftDampener()
    telemetry = dampener.process_stream([])
    assert telemetry.total_samples == 0
    assert telemetry.total_raw_path_length_px == 0.0
    assert telemetry.total_damped_path_length_px == 0.0
    assert telemetry.drift_reduction_pct == 0.0
    assert telemetry.stability_status == "EMPTY_STREAM"
    assert len(telemetry.corrections) == 0
    assert len(telemetry.warnings) > 0


def test_single_sample():
    dampener = SaccadicDriftDampener()
    telemetry = dampener.process_stream([(0.0, 100.0, 200.0)])
    assert telemetry.total_samples == 1
    assert telemetry.total_raw_path_length_px == 0.0
    assert len(telemetry.corrections) == 1
    c = telemetry.corrections[0]
    assert c.raw_x == 100.0
    assert c.raw_y == 200.0
    assert c.filtered_x == 100.0
    assert c.filtered_y == 200.0


def test_add_and_clear_anchors():
    dampener = SaccadicDriftDampener()
    anc1 = RetinalAnchor(anchor_id="A1", label="Anchor 1", x=150.0, y=150.0)
    anc2 = RetinalAnchor(anchor_id="A2", label="Anchor 2", x=300.0, y=300.0)
    dampener.add_anchor(anc1)
    dampener.add_anchor(anc2)
    assert len(dampener.anchors) == 2

    nearest = dampener.find_nearest_anchor(155.0, 152.0)
    assert nearest is not None
    anchor, dist = nearest
    assert anchor.anchor_id == "A1"
    assert dist < 10.0

    dampener.clear_anchors()
    assert len(dampener.anchors) == 0
    assert dampener.find_nearest_anchor(100.0, 100.0) is None


def test_retinal_latching_capture():
    dampener = SaccadicDriftDampener()
    anc = RetinalAnchor(
        anchor_id="LATCH_1",
        label="Focal Target",
        x=200.0,
        y=200.0,
        capture_radius_px=30.0,
        latch_strength=0.9,
    )
    dampener.add_anchor(anc)

    # Sample within capture radius (distance = 10 px)
    samples = [
        (0.0, 208.0, 206.0),
        (50.0, 206.0, 204.0),
    ]
    telemetry = dampener.process_stream(samples)
    assert telemetry.total_samples == 2
    assert telemetry.latch_event_count >= 1

    first_step = telemetry.corrections[0]
    assert first_step.is_latched is True
    assert first_step.latched_anchor_id == "LATCH_1"
    # Latched coordinate pulled closer to (200.0, 200.0)
    assert abs(first_step.filtered_x - 200.0) < abs(first_step.raw_x - 200.0)
    assert abs(first_step.filtered_y - 200.0) < abs(first_step.raw_y - 200.0)


def test_hysteresis_unlatching():
    config = DriftDampeningConfig(hysteresis_threshold_px=25.0)
    dampener = SaccadicDriftDampener(config=config)
    anc = RetinalAnchor(
        anchor_id="HYST_1",
        label="Hysteresis Target",
        x=100.0,
        y=100.0,
        capture_radius_px=20.0,
    )
    dampener.add_anchor(anc)

    samples = [
        (0.0, 105.0, 105.0),    # Dist ~7.07 -> Latches
        (50.0, 115.0, 115.0),   # Dist ~21.2 -> Stays latched (below hysteresis 25.0)
        (100.0, 130.0, 130.0),  # Dist ~42.4 -> Unlatches (exceeds hysteresis)
    ]
    telemetry = dampener.process_stream(samples)
    assert len(telemetry.corrections) == 3
    assert telemetry.corrections[0].is_latched is True
    assert telemetry.corrections[1].is_latched is True
    assert telemetry.corrections[2].is_latched is False


def test_lowpass_deadband_suppression():
    config = DriftDampeningConfig(deadband_radius_px=8.0, damping_factor=0.7)
    dampener = SaccadicDriftDampener(config=config)

    # Initial anchor-less sample
    # Next sample has tiny jitter (3px) below deadband
    samples = [
        (0.0, 50.0, 50.0),
        (50.0, 52.0, 51.0),
    ]
    telemetry = dampener.process_stream(samples)
    second_step = telemetry.corrections[1]
    # Deadband clamps tiny tremor to previous filtered position
    assert second_step.filtered_x == 50.0
    assert second_step.filtered_y == 50.0


def test_drift_reduction_percentage():
    dampener = SaccadicDriftDampener()
    anc = RetinalAnchor(anchor_id="A", label="Anchor", x=300.0, y=300.0, capture_radius_px=45.0)
    dampener.add_anchor(anc)

    # Oscillating noisy tremor around the anchor
    samples = []
    for i in range(20):
        t = i * 50.0
        rx = 300.0 + (12.0 if i % 2 == 0 else -12.0)
        ry = 300.0 + (8.0 if i % 2 == 0 else -8.0)
        samples.append((t, rx, ry))

    telemetry = dampener.process_stream(samples)
    assert telemetry.drift_reduction_pct > 20.0
    assert telemetry.mean_jitter_amplitude_px > 0.0
    assert telemetry.stability_status in ["LATCHED_STABLE", "DRIFT_DAMPED"]


def test_mental_rotation_simulation():
    dampener = SaccadicDriftDampener()
    telemetry = dampener.simulate_mental_rotation_drift(
        rotation_angle_deg=180.0,
        noise_std=8.0,
        duration_ms=1200.0,
        step_ms=50.0,
    )
    assert telemetry.total_samples == 24
    assert len(telemetry.corrections) == 24
    assert len(telemetry.anchors) == 3
    assert telemetry.working_memory_coherence_score > 0.0
    assert telemetry.total_raw_path_length_px > telemetry.total_damped_path_length_px


def test_svg_rendering():
    dampener = SaccadicDriftDampener()
    telemetry = dampener.simulate_mental_rotation_drift(
        rotation_angle_deg=90.0,
        duration_ms=600.0,
        step_ms=50.0,
    )
    svg = dampener.render_retinal_latch_svg(telemetry, width=900, height=550)
    assert "<svg" in svg
    assert "</svg>" in svg
    assert "#0b0f14" in svg
    assert "SACCADIC DRIFT DAMPENER" in svg
    assert "Drift Suppression" in svg
    assert "WM Coherence Index" in svg


def test_export_telemetry_json():
    dampener = SaccadicDriftDampener()
    telemetry = dampener.simulate_mental_rotation_drift(duration_ms=400.0, step_ms=100.0)
    json_str = dampener.export_telemetry_json(telemetry)
    data = json.loads(json_str)
    assert "total_samples" in data
    assert "drift_reduction_pct" in data
    assert "working_memory_coherence_score" in data
    assert "anchors" in data
    assert len(data["anchors"]) == 3


def test_zero_em_dashes():
    """Verify zero em dashes in script and test files."""
    script_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "scripts", "saccadic_drift_dampener.py")
    )
    with open(script_path, "r", encoding="utf-8") as f:
        script_code = f.read()
    assert chr(8212) not in script_code, "Unicode em dash found in saccadic_drift_dampener.py"

    with open(__file__, "r", encoding="utf-8") as f:
        test_code = f.read()
    assert chr(8212) not in test_code, "Unicode em dash found in test_saccadic_drift_dampener.py"
