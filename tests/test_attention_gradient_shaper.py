"""
test_attention_gradient_shaper.py - Unit tests for AttentionGradientShaper (Phase 104, Cycle 100).

Tests Anstis visual acuity decay, Bouma crowding window calculation,
peripheral edge clutter attenuation, saccade corridor shielding, SVG export,
and zero em dashes.

Strict constraint: Strictly zero em dashes (Unicode U+2014) anywhere.
"""

from pathlib import Path
import pytest
from scripts.attention_gradient_shaper import (
    AttentionGradientShaper,
    CardAcuityProfile,
    GradientShaperResult,
    GradientTelemetry,
)


@pytest.fixture
def workspace_cards():
    return [
        # Focal card (at gaze center ~200, 200)
        {"id": "card_focal", "x": 100.0, "y": 100.0, "width": 200.0, "height": 200.0, "title": "Focal Anchor"},
        # Parafoveal card (~450px away)
        {"id": "card_para", "x": 550.0, "y": 150.0, "width": 200.0, "height": 160.0, "title": "Parafoveal Node"},
        # Peripheral card along corridor (target ~900, 300)
        {"id": "card_target", "x": 800.0, "y": 250.0, "width": 220.0, "height": 180.0, "title": "Saccade Target"},
        # Far peripheral off-axis distractor (~1200px away)
        {"id": "card_distract", "x": 1200.0, "y": 800.0, "width": 200.0, "height": 160.0, "title": "Distractor Note"},
    ]


def test_empty_cards():
    shaper = AttentionGradientShaper()
    result = shaper.calculate_gradient(gaze_x=200.0, gaze_y=200.0, cards=[])
    assert isinstance(result, GradientShaperResult)
    assert result.telemetry.total_cards_evaluated == 0
    assert result.telemetry.max_eccentricity_deg == 0.0
    assert result.telemetry.cowan_bounded is True
    assert len(result.card_profiles) == 0


def test_gradient_and_acuity_decay(workspace_cards):
    shaper = AttentionGradientShaper(px_per_deg=45.0)
    result = shaper.calculate_gradient(
        gaze_x=200.0,
        gaze_y=200.0,
        cards=workspace_cards,
        saccade_target={"x": 910.0, "y": 340.0},
    )

    assert result.telemetry.total_cards_evaluated == 4
    assert result.telemetry.focal_card_id == "card_focal"
    assert result.telemetry.max_eccentricity_deg > 15.0
    assert result.telemetry.peripheral_drag_reduction_pct > 15.0
    assert result.telemetry.momentum_clarity_score > 60.0

    # Focal card has 0% attenuation and 1.0 opacity
    focal = next(p for p in result.card_profiles if p.card_id == "card_focal")
    assert focal.attenuation_pct == 0.0
    assert focal.opacity_multiplier == 1.0
    assert focal.blur_radius_px == 0.0

    # Distractor card has heavy attenuation and softening blur
    distract = next(p for p in result.card_profiles if p.card_id == "card_distract")
    assert distract.attenuation_pct > 30.0
    assert distract.blur_radius_px > 1.0
    assert distract.opacity_multiplier < 0.85


def test_saccade_corridor_shield():
    shaper = AttentionGradientShaper(px_per_deg=45.0)
    cards = [
        # Focal center
        {"id": "c_center", "x": 100.0, "y": 100.0, "width": 100.0, "height": 100.0, "title": "Center"},
        # Card A: directly in the path of the saccade corridor (x=500, y=180)
        {"id": "c_on_path", "x": 450.0, "y": 130.0, "width": 100.0, "height": 100.0, "title": "On Path"},
        # Card B: equidistant from center but far orthogonal to corridor (x=150, y=550)
        {"id": "c_off_path", "x": 100.0, "y": 500.0, "width": 100.0, "height": 100.0, "title": "Off Path"},
    ]

    res = shaper.calculate_gradient(
        gaze_x=150.0,
        gaze_y=150.0,
        cards=cards,
        saccade_target={"x": 750.0, "y": 180.0},
    )

    on_path = next(p for p in res.card_profiles if p.card_id == "c_on_path")
    off_path = next(p for p in res.card_profiles if p.card_id == "c_off_path")

    # The card along the momentum corridor receives a corridor shield and is less attenuated
    assert on_path.attenuation_pct < off_path.attenuation_pct


def test_svg_export(tmp_path: Path, workspace_cards):
    shaper = AttentionGradientShaper()
    result = shaper.calculate_gradient(200.0, 200.0, workspace_cards)

    svg_file = tmp_path / "attention_gradient.svg"
    svg_content = shaper.export_svg(result, output_path=str(svg_file))

    assert "<svg" in svg_content
    assert "</svg>" in svg_content
    assert "Attention Gradient" in svg_content
    assert svg_file.exists()
    assert svg_file.stat().st_size > 500


def test_ascii_report(workspace_cards):
    shaper = AttentionGradientShaper()
    result = shaper.calculate_gradient(200.0, 200.0, workspace_cards)
    report = shaper.generate_ascii_report(result)

    assert "ATTENTION GRADIENT & PERIPHERAL SACCADE SHAPER" in report
    assert "Cards Evaluated" in report
    assert "Drag Reduction" in report
    assert "[CARD]" in report


def test_attenuation_css(workspace_cards):
    shaper = AttentionGradientShaper()
    result = shaper.calculate_gradient(200.0, 200.0, workspace_cards)

    assert ".dx-focal-gaze" in result.attenuation_css
    assert "filter: blur(" in result.attenuation_css
    assert "opacity:" in result.attenuation_css


def test_zero_em_dashes():
    source_files = [
        Path("scripts/attention_gradient_shaper.py"),
        Path("tests/test_attention_gradient_shaper.py"),
    ]
    for p in source_files:
        if p.exists():
            text = p.read_text(encoding="utf-8")
            assert "\u2014" not in text, f"Em dash found in {p}"
