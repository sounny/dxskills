"""
Unit tests for Autonomous Cognitive Spatial Working Memory Drift Compensator & Re-Centering Harness.
Strictly NO em dashes (\u2014) anywhere.
"""

import pytest
from scripts.drift_compensator import (
    EpistemicAnchor,
    DriftWaypoint,
    DriftTelemetry,
    DriftCompensatorResult,
    WorkingMemoryDriftCompensator
)

SAMPLE_ANCHORS = [
    {"id": "root", "label": "Core Problem Definition", "x": 400.0, "y": 300.0, "mass": 6.0, "type": "root"},
    {"id": "synthesis", "label": "Architectural Nexus", "x": 700.0, "y": 300.0, "mass": 4.0, "type": "synthesis_nexus"}
]

SAMPLE_WAYPOINTS = [
    {"x": 420.0, "y": 310.0, "duration_ms": 400.0},
    {"x": 480.0, "y": 350.0, "duration_ms": 500.0},
    {"x": 580.0, "y": 420.0, "duration_ms": 600.0},
    {"x": 750.0, "y": 550.0, "duration_ms": 700.0},
    {"x": 900.0, "y": 680.0, "duration_ms": 800.0},
]

def test_anchor_initialization():
    compensator = WorkingMemoryDriftCompensator()
    res = compensator.compute_drift([], SAMPLE_ANCHORS)
    assert len(res.anchors) == 2
    assert res.anchors[0].anchor_id == "root"
    assert res.anchors[0].mass == 6.0

def test_waypoint_tracking_and_displacement():
    compensator = WorkingMemoryDriftCompensator()
    res = compensator.compute_drift(SAMPLE_WAYPOINTS, SAMPLE_ANCHORS)
    assert len(res.waypoints) == len(SAMPLE_WAYPOINTS)
    assert res.telemetry.cumulative_drift_distance > 0.0
    assert res.telemetry.max_drift_displacement > 0.0
    assert res.telemetry.drift_entropy > 0.0

def test_drift_within_threshold_stable():
    compensator = WorkingMemoryDriftCompensator(drift_threshold=1000.0)
    res = compensator.compute_drift(SAMPLE_WAYPOINTS[:2], SAMPLE_ANCHORS)
    assert res.telemetry.requires_recentering is False

def test_drift_exceeding_threshold_triggers_restore():
    compensator = WorkingMemoryDriftCompensator(drift_threshold=250.0)
    res = compensator.compute_drift(SAMPLE_WAYPOINTS, SAMPLE_ANCHORS)
    assert res.telemetry.requires_recentering is True
    assert res.telemetry.restore_magnitude > 0.0

def test_magnetic_restore_vector():
    compensator = WorkingMemoryDriftCompensator(spring_constant=0.1)
    res = compensator.compute_drift(SAMPLE_WAYPOINTS, SAMPLE_ANCHORS)
    tel = res.telemetry
    # Head at (900, 680). Nearest anchor is synthesis at (700, 300).
    assert tel.nearest_anchor_id in ("root", "synthesis")
    assert tel.restore_magnitude > 0.0
    # Restoring vector components should pull backwards towards (700, 300)
    assert tel.restore_vector_x != 0.0
    assert tel.restore_vector_y != 0.0

def test_to_dict_serialization():
    compensator = WorkingMemoryDriftCompensator()
    res = compensator.compute_drift(SAMPLE_WAYPOINTS, SAMPLE_ANCHORS)
    d = res.to_dict()
    assert "anchors" in d
    assert "waypoints" in d
    assert "telemetry" in d
    assert len(d["waypoints"]) == len(SAMPLE_WAYPOINTS)

def test_svg_rendering_elements():
    compensator = WorkingMemoryDriftCompensator()
    res = compensator.compute_drift(SAMPLE_WAYPOINTS, SAMPLE_ANCHORS)
    svg = res.drift_field_svg
    assert "<svg" in svg
    assert "</svg>" in svg
    assert "titaniumDriftBg" in svg
    assert "polyline" in svg
    assert "Working Memory Allocentric Drift" in svg

def test_markdown_report_zero_em_dashes():
    compensator = WorkingMemoryDriftCompensator()
    res = compensator.compute_drift(SAMPLE_WAYPOINTS, SAMPLE_ANCHORS)
    md = res.audit_report_md
    assert "# Working Memory Drift & Allocentric Re-Centering Report" in md
    assert "Navigational Displacement Metrics" in md
    assert "Primary Epistemic Anchors" in md
    assert chr(8212) not in md
