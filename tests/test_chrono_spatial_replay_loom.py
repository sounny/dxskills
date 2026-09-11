"""
Tests for Chrono-Spatial Replay Loom & Episodic Trajectory Synthesizer
Validates forward mental planning sweeps, reverse credit assignment,
theta phase precession, temporal compression ratios, SVG rendering, and zero em dash compliance.
"""

import os
import sys
import math
import json
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.chrono_spatial_replay_loom import (
    ChronoSpatialReplayLoom,
    EpisodicWaypoint,
    ChronoReplayTelemetry,
)


def test_empty_trajectory():
    loom = ChronoSpatialReplayLoom()
    telemetry = loom.synthesize_forward_replay([])
    assert telemetry.total_waypoints == 0
    assert telemetry.total_path_length_px == 0.0
    assert telemetry.status == "EMPTY_TRAJECTORY"
    assert len(telemetry.warnings) > 0

    rev_telemetry = loom.synthesize_reverse_replay([])
    assert rev_telemetry.total_waypoints == 0
    assert rev_telemetry.status == "EMPTY_TRAJECTORY"


def test_single_waypoint():
    loom = ChronoSpatialReplayLoom()
    wp = EpisodicWaypoint("START", "Origin", 100.0, 100.0, valence=0.0, dwell_time_ms=200.0)
    telemetry = loom.synthesize_forward_replay([wp])
    assert telemetry.total_waypoints == 1
    assert telemetry.total_path_length_px == 0.0
    assert telemetry.realtime_duration_ms == 200.0
    assert telemetry.status == "REPLAY_SYNTHESIZED"


def test_forward_replay_synthesis():
    loom = ChronoSpatialReplayLoom()
    wps = [
        EpisodicWaypoint("W1", "Initial Clue", 100.0, 100.0, valence=0.1, dwell_time_ms=200.0),
        EpisodicWaypoint("W2", "Hypothesis", 200.0, 150.0, valence=0.4, dwell_time_ms=250.0),
        EpisodicWaypoint("W3", "Verification", 350.0, 200.0, valence=0.8, dwell_time_ms=300.0),
        EpisodicWaypoint("W4", "Goal State", 500.0, 250.0, valence=1.0, dwell_time_ms=350.0),
    ]
    telemetry = loom.synthesize_forward_replay(wps, compression_factor=15.0)
    assert telemetry.total_waypoints == 4
    assert telemetry.replay_mode == "FORWARD_PLANNING"
    assert telemetry.total_path_length_px > 400.0
    assert telemetry.compression_factor == 15.0
    assert telemetry.compressed_duration_ms < telemetry.realtime_duration_ms
    assert telemetry.fidelity_score > 80.0

    # Phase precession: early node has high phase (~320 deg), late node has low phase (~40 deg)
    assert telemetry.waypoints[0].theta_phase_deg > telemetry.waypoints[-1].theta_phase_deg
    assert telemetry.waypoints[0].theta_phase_deg == 320.0
    assert telemetry.waypoints[-1].theta_phase_deg == 40.0


def test_reverse_replay_synthesis():
    loom = ChronoSpatialReplayLoom()
    wps = [
        EpisodicWaypoint("N1", "Antecedent", 50.0, 50.0),
        EpisodicWaypoint("N2", "Action", 150.0, 100.0),
        EpisodicWaypoint("N3", "Consequence", 250.0, 150.0),
    ]
    telemetry = loom.synthesize_reverse_replay(wps)
    assert telemetry.replay_mode == "REVERSE_CREDIT"
    assert telemetry.total_waypoints == 3
    # First waypoint in reverse replay is the last node of the forward sequence
    assert telemetry.waypoints[0].node_id == "N3"
    assert telemetry.waypoints[-1].node_id == "N1"
    # Reverse phase precession: starts low, ends high
    assert telemetry.waypoints[0].theta_phase_deg < telemetry.waypoints[-1].theta_phase_deg


def test_choice_point_rollout_simulation():
    loom = ChronoSpatialReplayLoom()
    telemetry = loom.simulate_choice_point_rollout(depth=5, step_len_px=100.0)
    assert telemetry.total_waypoints == 6  # ROOT + 5 steps
    assert telemetry.total_path_length_px > 450.0
    assert telemetry.fidelity_score > 0.0
    assert telemetry.status == "REPLAY_SYNTHESIZED"


def test_svg_rendering():
    loom = ChronoSpatialReplayLoom()
    telemetry = loom.simulate_choice_point_rollout(depth=4)
    svg = loom.render_chrono_replay_svg(telemetry, width=920, height=560)
    assert "<svg" in svg
    assert "</svg>" in svg
    assert "#0b0f14" in svg
    assert "CHRONO-SPATIAL REPLAY LOOM" in svg
    assert "Compression Ratio" in svg
    assert "Fidelity Score" in svg


def test_export_telemetry_json():
    loom = ChronoSpatialReplayLoom()
    telemetry = loom.simulate_choice_point_rollout(depth=3)
    json_str = loom.export_telemetry_json(telemetry)
    data = json.loads(json_str)
    assert "replay_mode" in data
    assert "total_waypoints" in data
    assert "compression_factor" in data
    assert len(data["waypoints"]) == 4


def test_zero_em_dashes():
    """Verify zero em dashes in script and test files."""
    script_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "scripts", "chrono_spatial_replay_loom.py")
    )
    with open(script_path, "r", encoding="utf-8") as f:
        script_code = f.read()
    assert chr(8212) not in script_code, "Unicode em dash found in chrono_spatial_replay_loom.py"

    test_path = os.path.abspath(__file__)
    with open(test_path, "r", encoding="utf-8") as f:
        test_code = f.read()
    assert chr(8212) not in test_code, "Unicode em dash found in test_chrono_spatial_replay_loom.py"
