"""
Unit tests for Allocentric Compass & Coordinate Anchor Compass Engine.
Verifies cardinal sector resolution, polar bearing calculations, disorientation
jump detection, fidelity metrics, dark titanium SVG rose rendering, and markdown
telemetry. Strictly zero em dashes enforced.
"""

import pytest
from scripts.allocentric_compass import (
    CanvasLandmark,
    GazeTrajectoryWaypoint,
    OrientationFix,
    AllocentricCompassTelemetry,
    AllocentricCompassTracker,
    sample_navigation_session,
)


def test_landmark_initialization():
    lm = CanvasLandmark(
        landmark_id="arch-north",
        title="Architecture Core",
        pos_x=500.0,
        pos_y=300.0,
        is_cardinal_north=True,
        importance=5.0,
    )
    assert lm.landmark_id == "arch-north"
    assert lm.pos_x == 500.0
    assert lm.pos_y == 300.0
    assert lm.is_cardinal_north is True
    assert lm.importance == 5.0


def test_resolve_cardinal_sector():
    tracker = AllocentricCompassTracker()
    assert tracker.resolve_cardinal_sector(0.0) == "N"
    assert tracker.resolve_cardinal_sector(355.0) == "N"
    assert tracker.resolve_cardinal_sector(45.0) == "NE"
    assert tracker.resolve_cardinal_sector(90.0) == "E"
    assert tracker.resolve_cardinal_sector(135.0) == "SE"
    assert tracker.resolve_cardinal_sector(180.0) == "S"
    assert tracker.resolve_cardinal_sector(225.0) == "SW"
    assert tracker.resolve_cardinal_sector(270.0) == "W"
    assert tracker.resolve_cardinal_sector(315.0) == "NW"


def test_evaluate_trajectory_empty():
    tracker = AllocentricCompassTracker()
    landmarks, _ = sample_navigation_session()
    telemetry = tracker.evaluate_trajectory(landmarks, [])

    assert telemetry.total_fixes == 0
    assert telemetry.disorientation_count == 0
    assert telemetry.orientation_fidelity_pct == 100.0
    assert len(telemetry.fixes) == 0


def test_evaluate_trajectory_cardinal_bearings():
    tracker = AllocentricCompassTracker()
    north = CanvasLandmark("origin", "Origin", 0.0, 0.0, is_cardinal_north=True)
    # Waypoints directly North (0, -100), East (100, 0), South (0, 100), West (-100, 0)
    wps = [
        GazeTrajectoryWaypoint("wp-n", 0.0, -100.0, 10.0),
        GazeTrajectoryWaypoint("wp-e", 100.0, 0.0, 20.0),
        GazeTrajectoryWaypoint("wp-s", 0.0, 100.0, 30.0),
        GazeTrajectoryWaypoint("wp-w", -100.0, 0.0, 40.0),
    ]

    telemetry = tracker.evaluate_trajectory([north], wps)
    assert telemetry.total_fixes == 4
    assert telemetry.fixes[0].cardinal_sector == "N"
    assert telemetry.fixes[1].cardinal_sector == "E"
    assert telemetry.fixes[2].cardinal_sector == "S"
    assert telemetry.fixes[3].cardinal_sector == "W"


def test_disorientation_jump_detection():
    tracker = AllocentricCompassTracker(max_allowed_heading_jump_deg=85.0)
    north = CanvasLandmark("origin", "Origin", 0.0, 0.0, is_cardinal_north=True)
    # Jump from pure North (0 deg) to South (180 deg) in one step
    wps = [
        GazeTrajectoryWaypoint("w1", 0.0, -100.0, 10.0),
        GazeTrajectoryWaypoint("w2", 0.0, 100.0, 20.0),
    ]
    telemetry = tracker.evaluate_trajectory([north], wps)
    assert telemetry.disorientation_count == 1
    assert telemetry.fixes[1].is_disoriented is True
    assert telemetry.fixes[1].heading_drift_deg == 180.0


def test_fidelity_metric_bounds():
    tracker = AllocentricCompassTracker()
    landmarks, waypoints = sample_navigation_session()
    telemetry = tracker.evaluate_trajectory(landmarks, waypoints)

    assert 0.0 <= telemetry.orientation_fidelity_pct <= 100.0
    assert 0.0 <= telemetry.angular_dispersion_deg <= 360.0


def test_generate_svg():
    tracker = AllocentricCompassTracker()
    landmarks, waypoints = sample_navigation_session()
    telemetry = tracker.evaluate_trajectory(landmarks, waypoints)

    svg_code = tracker.generate_svg(telemetry)
    assert "<svg" in svg_code
    assert "</svg>" in svg_code
    assert "compassGlow" in svg_code
    assert "ALLOCENTRIC COMPASS HUD" in svg_code
    assert chr(8212) not in svg_code


def test_generate_markdown_report():
    tracker = AllocentricCompassTracker()
    landmarks, waypoints = sample_navigation_session()
    telemetry = tracker.evaluate_trajectory(landmarks, waypoints)

    md_report = tracker.generate_markdown_report(telemetry)
    assert "# Allocentric Compass and Coordinate Navigation Telemetry" in md_report
    assert "## 1. Executive Heading Overview" in md_report
    assert "## 3. Navigation Waypoint Orientation Log" in md_report
    assert chr(8212) not in md_report
