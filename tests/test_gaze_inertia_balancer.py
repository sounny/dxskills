"""Unit tests for Autonomous Cognitive Spatial Working Memory Saccade Velocity & Gaze Inertia Balancer.

Strict Quality Gate: Zero em dashes anywhere.
"""

import json
from pathlib import Path
import pytest

from scripts.gaze_inertia_balancer import (
    GazeInertiaBalancer,
    GazeInertiaTelemetry,
    GazeWaypoint,
    SaccadeTransition,
)


def test_compute_saccade_kinematics():
    balancer = GazeInertiaBalancer(px_per_deg=38.0)

    # Short hop (114px = 3 degrees)
    ang_short, vel_short, dur_short = balancer.compute_saccade_kinematics(114.0)
    assert 2.8 <= ang_short <= 3.2
    assert 120.0 <= vel_short <= 160.0
    assert dur_short >= 25.0

    # Long hop (760px = 20 degrees)
    ang_long, vel_long, dur_long = balancer.compute_saccade_kinematics(760.0)
    assert 19.5 <= ang_long <= 20.5
    assert 420.0 <= vel_long <= 480.0
    assert dur_long > dur_short


def test_analyze_scanpath_empty():
    balancer = GazeInertiaBalancer()
    telemetry = balancer.analyze_scanpath({"nodes": []})
    assert telemetry.total_nodes == 0
    assert telemetry.total_transitions == 0
    assert telemetry.ocular_comfort_score == 1.0


def test_analyze_scanpath_transitions():
    balancer = GazeInertiaBalancer(px_per_deg=38.0, max_comfortable_velocity_deg_per_sec=400.0)

    sample_canvas = {
        "nodes": [
            {"id": "n1", "x": 0, "y": 0, "width": 200, "height": 100, "text": "### Step 1\nInitialization"},
            {"id": "n2", "x": 100, "y": 80, "width": 200, "height": 100, "text": "### Step 2\nLocal validation"},
            {"id": "n3", "x": 1200, "y": 1000, "width": 200, "height": 100, "text": "### Step 3\nDistant replication cluster"},
        ],
        "edges": [],
    }

    telemetry = balancer.analyze_scanpath(sample_canvas, reading_sequence=["n1", "n2", "n3"])
    assert telemetry.total_nodes == 3
    assert telemetry.total_transitions == 2
    assert telemetry.strain_transitions_count == 1  # n2 -> n3 jump is over 1200px
    assert telemetry.transitions[1].is_strain_risk is True
    assert telemetry.transitions[0].is_strain_risk is False


def test_balance_gaze_inertia_waypoints():
    balancer = GazeInertiaBalancer(max_unbuffered_jump_px=500.0)

    sample_canvas = {
        "nodes": [
            {"id": "start", "x": 0, "y": 0, "width": 200, "height": 100, "text": "### Entry Hub\nMain dispatch."},
            {"id": "far_dest", "x": 900, "y": 600, "width": 200, "height": 100, "text": "### Far Cluster\nStorage sink."},
        ],
        "edges": [],
    }

    stabilized_canvas, telemetry = balancer.balance_gaze_inertia(sample_canvas, reading_sequence=["start", "far_dest"])

    assert telemetry.inserted_waypoints_count == 1
    assert telemetry.velocity_smoothness_boost_pct > 10.0
    assert len(stabilized_canvas["nodes"]) == 3  # original 2 + 1 stepping stone
    assert len(stabilized_canvas["edges"]) == 2

    # Verify stepping stone exists in canvas
    wp_nodes = [n for n in stabilized_canvas["nodes"] if "gaze_wp_" in n.get("id", "")]
    assert len(wp_nodes) == 1
    assert "Stepping Stone" in wp_nodes[0]["text"]


def test_export_svg_velocity_profile(tmp_path):
    balancer = GazeInertiaBalancer()
    telemetry = GazeInertiaTelemetry(
        total_nodes=4,
        total_transitions=3,
        average_jump_distance_px=380.0,
        max_peak_velocity_deg_per_sec=460.0,
        mean_gaze_inertia_index=320.0,
        strain_transitions_count=1,
        inserted_waypoints_count=1,
        velocity_smoothness_boost_pct=24.5,
        ocular_comfort_score=0.88,
        transitions=[
            SaccadeTransition("n1", "n2", "Hop 1", "Hop 2", 150.0, 3.9, 160.0, 32.5, 78.0, False),
            SaccadeTransition("n2", "n3", "Hop 2", "Hop 3", 750.0, 19.7, 440.0, 75.0, 2580.0, True),
            SaccadeTransition("n3", "n4", "Hop 3", "Hop 4", 240.0, 6.3, 230.0, 39.0, 1350.0, False),
        ],
    )

    svg_file = tmp_path / "velocity_profile.svg"
    svg_str = balancer.export_svg_velocity_profile(telemetry, str(svg_file))

    assert svg_file.exists()
    assert "<svg" in svg_str
    assert "</svg>" in svg_str
    assert "Strain Threshold" in svg_str
    assert "Saccade Velocity" in svg_str


def test_zero_em_dashes_enforcement():
    balancer = GazeInertiaBalancer()
    sample_canvas = {
        "nodes": [
            {"id": "n1", "x": 0, "y": 0, "width": 200, "height": 100, "text": "### Alpha\nTask 1"},
            {"id": "n2", "x": 800, "y": 600, "width": 200, "height": 100, "text": "### Beta\nTask 2"},
        ],
        "edges": [],
    }

    stabilized_canvas, telemetry = balancer.balance_gaze_inertia(sample_canvas)
    md_report = balancer.generate_markdown_report(telemetry)
    svg_str = balancer.export_svg_velocity_profile(telemetry)

    full_text = md_report + svg_str + json.dumps(stabilized_canvas) + json.dumps(telemetry.to_dict())
    assert chr(8212) not in full_text
    assert "\u2014" not in full_text
