"""
Unit tests for Allocentric Kinematic Horizon & Inertial Frame Calibrator Engine.
Verifies 3-axis orientation frame calculations, gravity vector baselines,
gimbal lock singularity protection, SVG gauge rendering, and diagnostic reporting.
Strictly zero em dash compliance.
"""

import pytest
import math
from scripts.allocentric_kinematic_horizon import (
    InertialSample,
    KinematicFrame,
    KinematicHorizonTelemetry,
    AllocentricKinematicHorizon,
)


def test_inertial_sample_and_frame_creation():
    s = InertialSample("in-1", pitch_deg=10.0, roll_deg=-5.0, yaw_deg=180.0, timestamp_ms=100.0)
    assert s.sample_id == "in-1"
    d = s.to_dict()
    assert d["pitch_deg"] == 10.0
    assert d["roll_deg"] == -5.0

    frame = KinematicFrame(
        sample=s,
        angular_velocity_dps=(5.0, -2.0, 10.0),
        gravity_vector=(0.174, -0.086, 0.981),
        gimbal_lock_proximity=0.111,
        allocentric_stability_index=92.5,
        horizon_offset_px=25.0,
        horizon_tilt_deg=5.0,
    )
    assert frame.sample.sample_id == "in-1"
    fd = frame.to_dict()
    assert fd["gimbal_lock_proximity"] == 0.111
    assert fd["horizon_tilt_deg"] == 5.0


def test_calculate_kinematic_frames_empty():
    calibrator = AllocentricKinematicHorizon()
    telemetry = calibrator.calculate_kinematic_frames([])
    assert telemetry.total_samples == 0
    assert len(telemetry.frames) == 0
    assert telemetry.gimbal_lock_safety_margin_percent == 100.0
    assert telemetry.status_level == "STABLE_HORIZON"


def test_calculate_kinematic_frames_nominal_level():
    calibrator = AllocentricKinematicHorizon(pitch_scale_px_per_deg=2.0)
    s = InertialSample("level", pitch_deg=0.0, roll_deg=0.0, yaw_deg=0.0)
    telemetry = calibrator.calculate_kinematic_frames([s])

    assert telemetry.total_samples == 1
    f = telemetry.frames[0]
    assert math.isclose(f.gravity_vector[0], 0.0, abs_tol=1e-3)
    assert math.isclose(f.gravity_vector[1], 0.0, abs_tol=1e-3)
    assert math.isclose(f.gravity_vector[2], 1.0, abs_tol=1e-3)
    assert math.isclose(f.horizon_offset_px, 0.0, abs_tol=1e-3)
    assert f.gimbal_lock_proximity == 0.0
    assert telemetry.status_level == "STABLE_HORIZON"


def test_gimbal_lock_proximity_and_warning():
    calibrator = AllocentricKinematicHorizon(gimbal_warning_threshold_deg=75.0)
    # Pitch near vertical (85 degrees)
    s1 = InertialSample("in-safe", pitch_deg=20.0, roll_deg=0.0, yaw_deg=0.0, timestamp_ms=0.0)
    s2 = InertialSample("in-steep", pitch_deg=85.0, roll_deg=0.0, yaw_deg=0.0, timestamp_ms=100.0)

    telemetry = calibrator.calculate_kinematic_frames([s1, s2])
    assert telemetry.status_level == "GIMBAL_LOCK_WARNING"
    assert telemetry.frames[1].gimbal_lock_proximity > (75.0 / 90.0)
    assert telemetry.gimbal_lock_safety_margin_percent < 15.0


def test_angular_velocity_and_wrap_around():
    calibrator = AllocentricKinematicHorizon()
    # Yaw changes from 355 deg to 5 deg in 100 ms (delta = +10 deg across 360 wrap)
    s1 = InertialSample("y1", pitch_deg=0.0, roll_deg=0.0, yaw_deg=355.0, timestamp_ms=0.0)
    s2 = InertialSample("y2", pitch_deg=0.0, roll_deg=0.0, yaw_deg=5.0, timestamp_ms=100.0)

    telemetry = calibrator.calculate_kinematic_frames([s1, s2])
    yaw_rate = telemetry.frames[1].angular_velocity_dps[2]
    # 10 deg / 0.1 s = 100 deg/s
    assert math.isclose(yaw_rate, 100.0, abs_tol=1.0)


def test_demo_telemetry_generation():
    demo = AllocentricKinematicHorizon.create_demo_telemetry()
    assert demo.total_samples == 9
    assert len(demo.frames) == 9
    assert demo.overall_stability_score > 60.0
    assert demo.status_level in ["STABLE_HORIZON", "KINEMATIC_DRIFT"]

    d = demo.to_dict()
    assert "gimbal_lock_safety_margin_percent" in d
    assert "mean_angular_velocity_dps" in d


def test_markdown_report_formatting():
    calibrator = AllocentricKinematicHorizon()
    demo = calibrator.create_demo_telemetry()
    report = calibrator.generate_markdown_report(demo)

    assert "# Allocentric Kinematic Horizon" in report
    assert "Vestibular-Ocular Reflex" in report
    assert "| Telemetry Parameter |" in report
    assert "| Frame ID |" in report
    assert chr(8212) not in report, "Em dash found in markdown report!"


def test_svg_rendering_integrity():
    calibrator = AllocentricKinematicHorizon()
    demo = calibrator.create_demo_telemetry()
    svg = calibrator.generate_svg(demo, width=880, height=580)

    assert '<svg xmlns="http://www.w3.org/2000/svg"' in svg
    assert 'viewBox="0 0 880 580"' in svg
    assert 'ALLOCENTRIC KINEMATIC HORIZON' in svg
    assert 'Inertial Kinematic Telemetry' in svg
    assert 'Kinematic Horizon Legend' in svg
    assert 'gaugeClip' in svg
    assert chr(8212) not in svg, "Em dash found in SVG output!"


def test_zero_em_dashes_enforcement():
    with open("scripts/allocentric_kinematic_horizon.py", "r", encoding="utf-8") as f:
        src = f.read()
    assert chr(8212) not in src, "Em dash found in allocentric_kinematic_horizon.py!"
