"""Unit tests for Autonomous Cognitive Spatial Working Memory Saccade Velocity & Gaze Path Calibrator.

Tests verify:
- Empty canvas handling
- Rayner Optimal Viewing Position (OVP) anchor calculations
- Carpenter saccadic velocity and duration scaling
- Optical overshoot detection and intermediate damping guides
- Obsidian .canvas export
- Publication-grade SVG rendering
- ASCII report formatting
- Strict zero em dash rule enforcement

Strict Quality Gate: Zero em dashes anywhere (use hyphens, commas, or parentheses).
"""

import json
import os
import pytest

from scripts.saccade_calibrator import (
    GazeAnchor,
    SaccadeCalibratorTelemetry,
    SaccadeRegime,
    SaccadeStep,
    SaccadeVelocityGazeCalibrator,
)


def test_empty_canvas_handling():
    calibrator = SaccadeVelocityGazeCalibrator()
    calibrator.load_dict({})
    steps, telemetry = calibrator.calibrate_gaze_paths()

    assert steps == []
    assert telemetry.total_nodes == 0
    assert telemetry.total_steps == 0
    assert telemetry.mean_jump_distance_px == 0.0
    assert telemetry.overshoot_risk_count == 0


def test_ovp_anchor_calculation():
    calibrator = SaccadeVelocityGazeCalibrator()
    nodes = {
        "nodes": {
            "n1": {"title": "Executive Gateway", "text": "Central architectural routing hub", "x": 100, "y": 200, "width": 300, "height": 100}
        }
    }
    calibrator.load_dict(nodes)
    node = calibrator.nodes["n1"]

    # 100 + 300 * 0.35 = 205.0
    assert node["ovp_x"] == pytest.approx(205.0, 0.1)
    # 200 + 100 * 0.30 = 230.0
    assert node["ovp_y"] == pytest.approx(230.0, 0.1)
    assert node["lexical_length"] == 4


def test_saccadic_velocity_and_duration_scaling():
    calibrator = SaccadeVelocityGazeCalibrator(screen_dpi=96.0, viewing_distance_cm=60.0)
    nodes = {
        "nodes": {
            "n1": {"title": "Card Alpha", "text": "Near node", "x": 100, "y": 100, "width": 200, "height": 100},
            "n2": {"title": "Card Beta", "text": "Adjacent node", "x": 180, "y": 100, "width": 200, "height": 100},
            "n3": {"title": "Card Gamma", "text": "Distant node", "x": 1200, "y": 800, "width": 200, "height": 100},
        }
    }
    calibrator.load_dict(nodes)
    steps, telemetry = calibrator.calibrate_gaze_paths(reading_sequence=["n1", "n2", "n3"])

    assert len(steps) == 2
    step1 = steps[0]  # n1 -> n2 (short jump)
    step2 = steps[1]  # n2 -> n3 (large ballistic jump)

    assert step1.distance_px < step2.distance_px
    assert step1.estimated_duration_ms < step2.estimated_duration_ms
    assert step1.peak_velocity_deg_s < step2.peak_velocity_deg_s


def test_overshoot_detection_and_damping_guides():
    calibrator = SaccadeVelocityGazeCalibrator(max_comfortable_jump_px=400.0)
    nodes = {
        "nodes": {
            "n_local": {"title": "Local Focus", "text": "Active foveal anchor", "x": 100, "y": 100, "width": 200, "height": 100},
            "n_mid": {"title": "Meso Scope", "text": "Intermediate node", "x": 350, "y": 120, "width": 200, "height": 100},
            "n_far": {"title": "Peripheral Far", "text": "Distant cluster node", "x": 1100, "y": 150, "width": 200, "height": 100},
        }
    }
    calibrator.load_dict(nodes)
    steps, telemetry = calibrator.calibrate_gaze_paths(reading_sequence=["n_local", "n_mid", "n_far"])

    assert len(steps) == 2
    step_short = steps[0]
    step_far = steps[1]

    assert step_short.regime in [SaccadeRegime.MICRO_ADJACENT, SaccadeRegime.BALLISTIC_OPTIMAL]
    assert not step_short.damping_guide_required
    assert step_short.intermediate_anchor_coords is None

    assert step_far.regime in [SaccadeRegime.CORRECTIVE_OVERSHOOT, SaccadeRegime.EXCESSIVE_SPAN]
    assert step_far.damping_guide_required
    assert step_far.intermediate_anchor_coords is not None
    assert telemetry.overshoot_risk_count == 1


def test_canvas_export(tmp_path):
    calibrator = SaccadeVelocityGazeCalibrator()
    demo_canvas = {
        "nodes": [
            {"id": "c1", "text": "# Header\nFirst spatial anchor", "x": 100, "y": 100, "width": 260, "height": 140},
            {"id": "c2", "text": "# Detail\nSecond spatial anchor", "x": 650, "y": 120, "width": 260, "height": 140},
        ],
        "edges": []
    }
    calibrator.load_canvas(demo_canvas)
    out_file = tmp_path / "gaze_calibrated.canvas"
    res = calibrator.to_canvas(str(out_file))

    assert out_file.exists()
    assert len(res["nodes"]) == 2
    assert len(res["edges"]) == 1
    assert "gaze_step_1" == res["edges"][0]["id"]


def test_svg_export(tmp_path):
    calibrator = SaccadeVelocityGazeCalibrator()
    nodes = {
        "nodes": {
            "a": {"title": "Node A", "text": "Content A", "x": 100, "y": 100, "width": 200, "height": 100},
            "b": {"title": "Node B", "text": "Content B", "x": 700, "y": 300, "width": 200, "height": 100},
        }
    }
    calibrator.load_dict(nodes)
    out_svg = tmp_path / "gaze_mesh.svg"
    svg_str = calibrator.to_svg(str(out_svg))

    assert out_svg.exists()
    assert "<svg" in svg_str
    assert "Spatial Working Memory Saccade Velocity" in svg_str
    assert "OVP (35% L)" in svg_str
    assert "marker-end=\"url(#arrow)\"" in svg_str


def test_ascii_report():
    calibrator = SaccadeVelocityGazeCalibrator()
    nodes = {
        "nodes": {
            "node_1": {"title": "Input Gateway", "text": "Lexical parsing", "x": 100, "y": 100, "width": 200, "height": 100},
            "node_2": {"title": "Transform Core", "text": "AST compilation", "x": 500, "y": 400, "width": 200, "height": 100},
        }
    }
    calibrator.load_dict(nodes)
    _, telemetry = calibrator.calibrate_gaze_paths()
    report = calibrator.render_ascii_report(telemetry)

    assert "Spatial Working Memory Saccade Velocity & Gaze Path Report" in report
    assert "Input Gateway" in report or "node_1" in report
    assert "Mean Saccade Jump Distance:" in report


def test_zero_em_dashes_in_module():
    scripts_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "scripts", "saccade_calibrator.py")
    test_path = __file__

    with open(scripts_path, "r", encoding="utf-8") as f:
        src_text = f.read()
    with open(test_path, "r", encoding="utf-8") as f:
        test_text = f.read()

    assert chr(8212) not in src_text, "Found em dash in scripts/saccade_calibrator.py"
    assert chr(8212) not in test_text, "Found em dash in tests/test_saccade_calibrator.py"
