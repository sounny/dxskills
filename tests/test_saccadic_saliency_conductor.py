"""
Unit tests for Saccadic Saliency Conductor Engine.
Strict zero em dash policy enforced.
"""

import pytest
import math
from scripts.saccadic_saliency_conductor import (
    SaliencyWaypoint,
    SaccadicTransition,
    SaccadicConductorTelemetry,
    SaccadicSaliencyConductor,
)


def test_waypoint_and_transition_creation():
    wp = SaliencyWaypoint("wp-1", "Hero Banner", 100.0, 150.0, 0.9, 0.85, 0)
    d = wp.to_dict()
    assert d["waypoint_id"] == "wp-1"
    assert d["x"] == 100.0
    assert d["y"] == 150.0
    assert d["raw_saliency"] == 0.9

    tr = SaccadicTransition("wp-1", "wp-2", 150.0, 420.0, 210.0, False)
    d_tr = tr.to_dict()
    assert d_tr["from_waypoint_id"] == "wp-1"
    assert d_tr["to_waypoint_id"] == "wp-2"
    assert d_tr["is_regression"] is False


def test_empty_waypoints_handling():
    conductor = SaccadicSaliencyConductor()
    telemetry = conductor.conduct_saliency_path([])
    assert telemetry.total_waypoints == 0
    assert telemetry.total_path_length_px == 0.0
    assert len(telemetry.warnings) > 0


def test_linear_forward_scanpath():
    conductor = SaccadicSaliencyConductor()
    waypoints = [
        SaliencyWaypoint("wp-1", "Title", 100.0, 100.0, 0.9, 0.9, order_index=0),
        SaliencyWaypoint("wp-2", "Subtitle", 200.0, 120.0, 0.8, 0.8, order_index=1),
        SaliencyWaypoint("wp-3", "Paragraph", 350.0, 150.0, 0.7, 0.7, order_index=2),
        SaliencyWaypoint("wp-4", "Call to Action", 500.0, 180.0, 0.85, 0.9, order_index=3),
    ]
    telemetry = conductor.conduct_saliency_path(waypoints)
    assert telemetry.total_waypoints == 4
    assert telemetry.regression_count == 0
    assert telemetry.status_level == "OPTIMAL_SACCADIC_GUIDANCE"
    assert telemetry.saccadic_efficiency_score >= 80.0
    assert len(telemetry.transitions) == 3


def test_regressive_saccade_detection_and_penalty():
    conductor = SaccadicSaliencyConductor()
    # Step 2 jumps back to the left
    waypoints = [
        SaliencyWaypoint("wp-1", "A", 100.0, 100.0, 0.9, 0.9, order_index=0),
        SaliencyWaypoint("wp-2", "B", 400.0, 100.0, 0.8, 0.8, order_index=1),
        SaliencyWaypoint("wp-3", "C (Regress)", 150.0, 100.0, 0.7, 0.7, order_index=2),
    ]
    telemetry = conductor.conduct_saliency_path(waypoints)
    assert telemetry.regression_count == 1
    assert telemetry.transitions[1].is_regression is True
    assert telemetry.status_level in ["ELEVATED_REGRESSION_FATIGUE", "ERRATIC_SALIENCY_CHAOS"]


def test_erratic_saliency_chaos_trigger():
    conductor = SaccadicSaliencyConductor()
    # Path with 3 regressions back and forth
    waypoints = [
        SaliencyWaypoint("wp-1", "A", 100.0, 100.0, 0.9, 0.9, order_index=0),
        SaliencyWaypoint("wp-2", "B", 400.0, 100.0, 0.8, 0.8, order_index=1),
        SaliencyWaypoint("wp-3", "C", 120.0, 100.0, 0.7, 0.7, order_index=2),  # Regress 1
        SaliencyWaypoint("wp-4", "D", 420.0, 100.0, 0.8, 0.8, order_index=3),
        SaliencyWaypoint("wp-5", "E", 130.0, 100.0, 0.7, 0.7, order_index=4),  # Regress 2
        SaliencyWaypoint("wp-6", "F", 430.0, 100.0, 0.8, 0.8, order_index=5),
        SaliencyWaypoint("wp-7", "G", 140.0, 100.0, 0.7, 0.7, order_index=6),  # Regress 3
    ]
    telemetry = conductor.conduct_saliency_path(waypoints)
    assert telemetry.regression_count == 3
    assert telemetry.status_level == "ERRATIC_SALIENCY_CHAOS"
    assert len(telemetry.warnings) > 0


def test_demo_telemetry_generation():
    telemetry = SaccadicSaliencyConductor.create_demo_telemetry()
    assert telemetry.total_waypoints == 6
    assert len(telemetry.transitions) == 5
    d = telemetry.to_dict()
    assert "saccadic_efficiency_score" in d
    assert "peak_velocity_dps" in d


def test_markdown_report_formatting():
    telemetry = SaccadicSaliencyConductor.create_demo_telemetry()
    conductor = SaccadicSaliencyConductor()
    report = conductor.generate_markdown_report(telemetry)
    assert "# Saccadic Saliency Conductor & Attentional Trajectory Report" in report
    assert "Scanpath Conduction Status:" in report
    assert "| **Total Fixation Waypoints** |" in report
    assert "| **Saccadic Efficiency Score** |" in report
    assert "Itti-Koch Saliency Guidance" in report


def test_svg_rendering_integrity():
    telemetry = SaccadicSaliencyConductor.create_demo_telemetry()
    conductor = SaccadicSaliencyConductor()
    svg = conductor.generate_svg(telemetry)
    assert svg.startswith("<svg")
    assert svg.endswith("</svg>")
    assert "Saccadic Saliency Conductor" in svg
    assert 'id="arrow"' in svg
    assert "Cartesian Grid Matrix" in svg


def test_zero_em_dashes_enforcement():
    with open("scripts/saccadic_saliency_conductor.py", "r", encoding="utf-8") as f:
        script_content = f.read()
    assert chr(8212) not in script_content, "Em dash detected in scripts/saccadic_saliency_conductor.py!"

    with open("tests/test_saccadic_saliency_conductor.py", "r", encoding="utf-8") as f:
        test_content = f.read()
    assert chr(8212) not in test_content, "Em dash detected in tests/test_saccadic_saliency_conductor.py!"
