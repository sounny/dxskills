"""
Unit tests for Saccadic Drift Compensator & Foveal Re-Centering Loom.
Strict rule: Zero em dashes across all code, docstrings, and tests.
"""

import pytest
import math
from scripts.foveal_recentering_loom import (
    GazeFixationPoint,
    DriftMeasurement,
    RestorativeGuide,
    FovealReCenteringTelemetry,
    FovealReCenteringLoom,
    sample_gaze_fixations,
)


def test_gaze_displacement_calculation():
    """Verifies Euclidean distance between anchor target and observed gaze."""
    p = GazeFixationPoint("p1", "Anchor A", 100.0, 100.0, 130.0, 140.0)
    # sqrt(30^2 + 40^2) = 50.0
    assert math.isclose(p.displacement_px, 50.0, abs_tol=0.01)


def test_evaluate_fixations_empty():
    """Verifies graceful handling of empty fixation list."""
    loom = FovealReCenteringLoom()
    telemetry = loom.evaluate_fixations([])

    assert telemetry.total_fixations == 0
    assert telemetry.mean_displacement_px == 0.0
    assert telemetry.locked_count == 0
    assert telemetry.disoriented_count == 0


def test_fixations_state_classification():
    """Verifies state classification into locked, drifting, and disoriented."""
    loom = FovealReCenteringLoom(drift_threshold=45.0)
    fixations = [
        GazeFixationPoint("p1", "Target 1", 100.0, 100.0, 110.0, 105.0),   # disp ~ 11.18 -> locked (<=25)
        GazeFixationPoint("p2", "Target 2", 200.0, 200.0, 230.0, 210.0),   # disp ~ 31.62 -> drifting (<=45)
        GazeFixationPoint("p3", "Target 3", 300.0, 300.0, 360.0, 370.0),   # disp ~ 92.19 -> disoriented (>45)
    ]
    telemetry = loom.evaluate_fixations(fixations)

    assert telemetry.total_fixations == 3
    assert telemetry.locked_count == 1
    assert telemetry.drifting_count == 1
    assert telemetry.disoriented_count == 1
    assert math.isclose(telemetry.disorientation_rate_pct, 33.3, abs_tol=0.1)


def test_magnetic_restore_vector_direction():
    """Verifies restore vector pulls from gaze coordinate towards intended anchor target."""
    loom = FovealReCenteringLoom(magnetic_gain=0.50)
    p = GazeFixationPoint("p1", "Center Hub", 200.0, 200.0, 240.0, 260.0)
    telemetry = loom.evaluate_fixations([p])

    m = telemetry.measurements[0]
    # dx = target_x - gaze_x = 200 - 240 = -40; rx = -40 * 0.5 = -20
    # dy = target_y - gaze_y = 200 - 260 = -60; ry = -60 * 0.5 = -30
    assert math.isclose(m.restore_vector_x, -20.0, abs_tol=0.01)
    assert math.isclose(m.restore_vector_y, -30.0, abs_tol=0.01)


def test_restorative_guide_generation():
    """Verifies that bezier restorative guides are synthesized for drifting/disoriented fixations."""
    loom = FovealReCenteringLoom(drift_threshold=40.0)
    fixations = [
        GazeFixationPoint("p1", "Anchor A", 100.0, 100.0, 105.0, 105.0),  # locked (no guide)
        GazeFixationPoint("p2", "Anchor B", 300.0, 300.0, 370.0, 370.0),  # disoriented (guide generated)
    ]
    telemetry = loom.evaluate_fixations(fixations)

    assert len(telemetry.guides) == 1
    guide = telemetry.guides[0]
    assert guide.label == "Anchor B"
    assert math.isclose(guide.source_x, 370.0, abs_tol=0.01)
    assert math.isclose(guide.target_x, 300.0, abs_tol=0.01)
    assert guide.strength > 0.0


def test_drift_velocity_calculation():
    """Verifies drift velocity computation between consecutive fixation timestamps."""
    loom = FovealReCenteringLoom()
    fixations = [
        GazeFixationPoint("p1", "Target 1", 100.0, 100.0, 100.0, 100.0, timestamp_ms=0.0),    # disp = 0
        GazeFixationPoint("p2", "Target 2", 200.0, 200.0, 250.0, 200.0, timestamp_ms=500.0),  # disp = 50, dt = 0.5s -> v = 100 px/s
    ]
    telemetry = loom.evaluate_fixations(fixations)

    assert telemetry.measurements[0].drift_velocity_px_s == 0.0
    assert math.isclose(telemetry.measurements[1].drift_velocity_px_s, 100.0, abs_tol=0.1)


def test_generate_svg_structure():
    """Verifies valid SVG markup generation with dark titanium styling."""
    loom = FovealReCenteringLoom()
    fixations = sample_gaze_fixations()
    telemetry = loom.evaluate_fixations(fixations)
    svg = loom.generate_svg(telemetry, width=900, height=540)

    assert "<svg" in svg
    assert "</svg>" in svg
    assert "#09090b" in svg
    assert "Saccadic Drift Compensator" in svg
    assert "Restore Vector" in svg


def test_generate_markdown_report():
    """Verifies publication-ready markdown compliance audit."""
    loom = FovealReCenteringLoom()
    fixations = sample_gaze_fixations()
    telemetry = loom.evaluate_fixations(fixations)
    report = loom.generate_markdown_report(telemetry)

    assert "# Saccadic Drift Compensator and Foveal Re-Centering Audit" in report
    assert "Fixational Ocular Drift" in report
    assert "Cowan Capacity Bounds" in report
    assert "| `fix-1` |" in report
    assert chr(8212) not in report
