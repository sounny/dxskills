"""
test_saccadic_fatigue_meter.py - Unit tests for SaccadicFatigueMeter (Phase 100, Cycle 96).

Tests Carpenter saccadic velocity decay, attentional blink risk estimation,
dynamic contrast ramp dampening, SVG export, and zero em dashes.

Strict constraint: Strictly zero em dashes (Unicode U+2014) anywhere.
"""

from pathlib import Path
import pytest
from scripts.saccadic_fatigue_meter import (
    ContrastDampingProfile,
    FatigueMeterResult,
    FatigueMeterTelemetry,
    GazeSessionSample,
    SaccadicFatigueMeter,
)


@pytest.fixture
def fatigued_gaze_samples():
    samples = []
    # 20 samples over 35 minutes showing gradual velocity decay from 440 down to 310 deg/s
    for i in range(20):
        t_ms = i * 105000.0  # ~35 mins total
        vel = 440.0 - (i * 6.5)  # Drop of ~130 deg/s
        blink = 5.0 if i < 10 else 1.8  # Strain blinking later
        samples.append({
            "sample_id": f"s_{i+1:02d}",
            "timestamp_ms": t_ms,
            "saccade_amplitude_deg": 9.0,
            "peak_velocity_deg_s": vel,
            "fixation_duration_ms": 210.0 + (i * 8.0),
            "blink_interval_sec": blink,
            "target_card_id": f"card_{(i % 4) + 1}",
        })
    return samples


def test_empty_samples():
    meter = SaccadicFatigueMeter()
    result = meter.evaluate_gaze_samples([])
    assert isinstance(result, FatigueMeterResult)
    assert result.telemetry.total_samples_analyzed == 0
    assert result.telemetry.ocular_fatigue_index == 0.0
    assert result.telemetry.attentional_blink_risk == "LOW"


def test_velocity_decay_calculation(fatigued_gaze_samples):
    meter = SaccadicFatigueMeter()
    result = meter.evaluate_gaze_samples(fatigued_gaze_samples)

    assert result.telemetry.total_samples_analyzed == 20
    assert result.telemetry.velocity_decay_pct > 15.0
    assert result.telemetry.ocular_fatigue_index > 0.4
    assert result.telemetry.attentional_blink_risk in ("MODERATE", "ELEVATED", "CRITICAL")
    assert result.telemetry.recommended_break_sec >= 60


def test_contrast_damping_profiles(fatigued_gaze_samples):
    meter = SaccadicFatigueMeter()
    cards = [
        {"id": "card_focal", "is_focal": True},
        {"id": "card_peripheral_1", "is_focal": False},
        {"id": "card_peripheral_2", "is_focal": False},
    ]
    result = meter.evaluate_gaze_samples(fatigued_gaze_samples, cards=cards)

    assert len(result.card_profiles) == 3
    focal_p = result.card_profiles[0]
    periph_p = result.card_profiles[1]

    # Focal card preserves higher contrast than peripheral
    assert focal_p.damped_contrast_ratio > periph_p.damped_contrast_ratio
    assert focal_p.luminance_level > periph_p.luminance_level
    assert focal_p.border_opacity > periph_p.border_opacity
    assert focal_p.recommended_kelvin <= 4500


def test_restorative_css_tokens(fatigued_gaze_samples):
    meter = SaccadicFatigueMeter()
    result = meter.evaluate_gaze_samples(fatigued_gaze_samples)

    css = result.restorative_css_tokens
    assert ":root" in css
    assert "--dx-ocular-fatigue" in css
    assert "--dx-contrast-attenuation" in css
    assert "--dx-color-temperature" in css


def test_svg_export(fatigued_gaze_samples, tmp_path):
    meter = SaccadicFatigueMeter()
    result = meter.evaluate_gaze_samples(fatigued_gaze_samples)

    svg_file = tmp_path / "fatigue.svg"
    svg_content = meter.export_svg(result, str(svg_file))

    assert svg_file.exists()
    assert "<svg" in svg_content
    assert "</svg>" in svg_content
    assert "Saccadic Fatigue Meter" in svg_content
    assert "Carpenter Main Sequence" in svg_content


def test_ascii_report(fatigued_gaze_samples):
    meter = SaccadicFatigueMeter()
    result = meter.evaluate_gaze_samples(fatigued_gaze_samples)
    report = meter.generate_ascii_report(result)

    assert "SACCADIC FATIGUE METER" in report
    assert "Mean Peak Velocity" in report
    assert "Velocity Decay Rate" in report
    assert "CARD CONTRAST DAMPING" in report


def test_zero_em_dashes():
    """Verify strictly zero em dashes in code and test files."""
    files_to_check = [
        Path("scripts/saccadic_fatigue_meter.py"),
        Path("tests/test_saccadic_fatigue_meter.py"),
    ]
    em_dash = chr(8212)
    for fpath in files_to_check:
        if fpath.exists():
            text = fpath.read_text(encoding="utf-8")
            assert em_dash not in text, f"Em dash found in {fpath}"
