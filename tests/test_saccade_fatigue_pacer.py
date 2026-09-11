"""
Unit tests for Autonomous Cognitive Spatial Working Memory Saccade Fatigue Predictor & Kinetic Pacer.
Strictly NO em dashes (\u2014) anywhere.
"""

import pytest
from scripts.saccade_fatigue_pacer import (
    SaccadeKineticEvent,
    KineticPacerTelemetry,
    SaccadeFatiguePacerResult,
    SaccadeKineticPacer
)

SAMPLE_SACCADES = [
    {"amplitude_px": 100.0, "duration_ms": 30.0, "peak_velocity_px_s": 420.0},
    {"amplitude_px": 150.0, "duration_ms": 35.0, "peak_velocity_px_s": 510.0},
    {"amplitude_px": 250.0, "duration_ms": 80.0, "peak_velocity_px_s": 320.0},  # Fatigued
    {"amplitude_px": 350.0, "duration_ms": 110.0, "peak_velocity_px_s": 340.0}, # Fatigued
]

def test_expected_velocity_curve():
    pacer = SaccadeKineticPacer()
    v1 = pacer.expected_velocity(50.0)
    v2 = pacer.expected_velocity(200.0)
    v3 = pacer.expected_velocity(600.0)
    assert v1 < v2 < v3
    assert v3 < pacer.V_MAX

def test_kinetic_evaluation_optimal():
    pacer = SaccadeKineticPacer()
    optimal_saccades = [
        {"amplitude_px": 100.0, "duration_ms": 30.0, "peak_velocity_px_s": 450.0},
        {"amplitude_px": 150.0, "duration_ms": 35.0, "peak_velocity_px_s": 550.0},
    ]
    res = pacer.evaluate_kinetics(optimal_saccades)
    assert res.telemetry.fatigued_saccades == 0
    assert res.telemetry.fatigue_risk_index == 0.0

def test_kinetic_evaluation_fatigued():
    pacer = SaccadeKineticPacer(fatigue_threshold_ratio=0.80)
    res = pacer.evaluate_kinetics(SAMPLE_SACCADES)
    assert res.telemetry.fatigued_saccades >= 2
    assert res.telemetry.fatigue_risk_index > 0.0
    assert res.telemetry.velocity_drop_percent > 0.0

def test_telemetry_metrics():
    pacer = SaccadeKineticPacer()
    res = pacer.evaluate_kinetics(SAMPLE_SACCADES)
    tel = res.telemetry
    assert tel.total_saccades == len(SAMPLE_SACCADES)
    assert tel.mean_peak_velocity > 0.0
    assert tel.recommended_rest_interval_s >= 5.0
    assert 0.8 <= tel.pacing_cadence_hz <= 2.0

def test_to_dict_serialization():
    pacer = SaccadeKineticPacer()
    res = pacer.evaluate_kinetics(SAMPLE_SACCADES)
    d = res.to_dict()
    assert "events" in d
    assert "telemetry" in d
    assert len(d["events"]) == len(SAMPLE_SACCADES)

def test_svg_rendering_elements():
    pacer = SaccadeKineticPacer()
    res = pacer.evaluate_kinetics(SAMPLE_SACCADES)
    svg = res.kinetic_pacer_svg
    assert "<svg" in svg
    assert "</svg>" in svg
    assert "titaniumPacerBg" in svg
    assert "Main Sequence" in svg

def test_markdown_report_zero_em_dashes():
    pacer = SaccadeKineticPacer()
    res = pacer.evaluate_kinetics(SAMPLE_SACCADES)
    md = res.audit_report_md
    assert "# Saccade Kinetic Fatigue & Adaptive Pacer Report" in md
    assert "Ocular Kinetic Metrics" in md
    assert "Saccade Event Classification" in md
    assert chr(8212) not in md

def test_empty_saccades_handling():
    pacer = SaccadeKineticPacer()
    res = pacer.evaluate_kinetics([])
    assert res.telemetry.total_saccades == 0
    assert len(res.events) == 0
