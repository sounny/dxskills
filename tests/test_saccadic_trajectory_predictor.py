"""
Unit tests for Saccadic Trajectory Predictor & Predictive Pre-Fetcher Engine.
Verifies Carpenter LATER trajectory extrapolation, candidate priority scoring,
tier classification, SVG rendering, markdown reporting, and strict zero-em-dash compliance.
"""

import os
import pytest
from scripts.saccadic_trajectory_predictor import (
    FixationPoint,
    TrajectoryVector,
    PreFetchCandidate,
    SaccadicPredictionTelemetry,
    SaccadicTrajectoryPredictor,
    sample_saccadic_session,
)


def test_fixation_point_initialization():
    p = FixationPoint(
        node_id="fix-1",
        title="Primary Logic Hub",
        x=200.0,
        y=150.0,
        timestamp_ms=500.0,
        dwell_duration_ms=220.0,
    )
    assert p.node_id == "fix-1"
    assert p.title == "Primary Logic Hub"
    assert p.x == 200.0
    assert p.y == 150.0
    assert p.timestamp_ms == 500.0
    assert p.dwell_duration_ms == 220.0


def test_trajectory_vector_initialization():
    vec = TrajectoryVector(
        origin_x=100.0,
        origin_y=150.0,
        heading_deg=45.0,
        velocity_px_per_ms=1.2,
        confidence=0.85,
        cone_angle_deg=35.0,
    )
    assert vec.origin_x == 100.0
    assert vec.origin_y == 150.0
    assert vec.heading_deg == 45.0
    assert vec.velocity_px_per_ms == 1.2
    assert vec.confidence == 0.85
    assert vec.cone_angle_deg == 35.0


def test_predict_trajectory_insufficient_points():
    predictor = SaccadicTrajectoryPredictor()
    assert predictor.predict_trajectory([]) is None
    single_point = [FixationPoint("f0", "Single", 100.0, 100.0, 0.0)]
    assert predictor.predict_trajectory(single_point) is None


def test_predict_trajectory_heading_and_velocity():
    predictor = SaccadicTrajectoryPredictor()
    points = [
        FixationPoint("p1", "Start", 100.0, 100.0, 0.0, 100.0),
        FixationPoint("p2", "Mid", 200.0, 100.0, 200.0, 100.0),  # moved right 100px in 100ms -> vel ~ 1.0, heading ~ 0.0 deg
    ]
    traj = predictor.predict_trajectory(points)
    assert traj is not None
    assert traj.origin_x == 200.0
    assert traj.origin_y == 100.0
    assert traj.heading_deg == pytest.approx(0.0, abs=1.0)
    assert traj.velocity_px_per_ms > 0.5
    assert traj.confidence >= 0.70


def test_evaluate_pre_fetch_candidates_empty():
    predictor = SaccadicTrajectoryPredictor()
    telemetry = predictor.evaluate_pre_fetch_candidates([], [])
    assert telemetry.recent_fixations_count == 0
    assert telemetry.current_trajectory is None
    assert telemetry.candidate_count == 0
    assert len(telemetry.pre_fetch_candidates) == 0


def test_evaluate_pre_fetch_candidates_priorities():
    predictor = SaccadicTrajectoryPredictor()
    fixations, candidates = sample_saccadic_session()
    telemetry = predictor.evaluate_pre_fetch_candidates(fixations, candidates)

    assert telemetry.recent_fixations_count == 3
    assert telemetry.current_trajectory is not None
    assert telemetry.candidate_count > 0
    assert len(telemetry.pre_fetch_candidates) > 0

    # Top candidate should be the one directly ahead (cand-1: Session Cache)
    top_cand = telemetry.pre_fetch_candidates[0]
    assert top_cand.node_id == "cand-1"
    assert top_cand.pre_fetch_tier == "focal"
    assert top_cand.priority_score >= 0.70

    # Backward candidate should have low priority
    cand_6 = [c for c in telemetry.pre_fetch_candidates if c.node_id == "cand-6"]
    if cand_6:
        assert cand_6[0].priority_score < 0.40


def test_generate_markdown_report():
    predictor = SaccadicTrajectoryPredictor()
    fixations, candidates = sample_saccadic_session()
    telemetry = predictor.evaluate_pre_fetch_candidates(fixations, candidates)
    report = predictor.generate_markdown_report(telemetry)

    assert "# Saccadic Trajectory Predictor and Predictive Pre-Fetcher Report" in report
    assert "Carpenter LATER Model" in report
    assert "Rayner Parafoveal Preview" in report
    assert "Prioritized Pre-Fetch Candidate Hierarchy" in report
    assert "Session Cache" in report


def test_generate_svg():
    predictor = SaccadicTrajectoryPredictor()
    fixations, candidates = sample_saccadic_session()
    telemetry = predictor.evaluate_pre_fetch_candidates(fixations, candidates)
    svg = predictor.generate_svg(telemetry, width=900, height=540)

    assert "<svg" in svg
    assert "</svg>" in svg
    assert "coneGrad" in svg
    assert "ACTIVE FOVEAL FIXATION" in svg
    assert "SACCADIC TRAJECTORY PREDICTOR HUD" in svg
    assert "Session Cache" in svg


def test_zero_em_dashes_in_source_and_outputs():
    # Verify module source file
    script_path = os.path.join(os.path.dirname(__file__), "..", "scripts", "saccadic_trajectory_predictor.py")
    with open(script_path, "r", encoding="utf-8") as f:
        source = f.read()
    assert chr(8212) not in source

    # Verify report and svg
    predictor = SaccadicTrajectoryPredictor()
    fixations, candidates = sample_saccadic_session()
    telemetry = predictor.evaluate_pre_fetch_candidates(fixations, candidates)
    report = predictor.generate_markdown_report(telemetry)
    svg = predictor.generate_svg(telemetry)

    assert chr(8212) not in report
    assert chr(8212) not in svg
