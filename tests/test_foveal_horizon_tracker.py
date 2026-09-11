"""
test_foveal_horizon_tracker.py - Unit tests for FovealHorizonTracker (Phase 103, Cycle 99).

Tests Rayner foveal dynamics, visual drift latency estimation,
contextual breadcrumb anchor synthesis, SVG horizon rendering, and zero em dashes.

Strict constraint: Strictly zero em dashes (Unicode U+2014) anywhere.
"""

from pathlib import Path
import pytest
from scripts.foveal_horizon_tracker import (
    BreadcrumbAnchor,
    FovealHorizonResult,
    FovealHorizonTracker,
    HorizonTelemetry,
)


@pytest.fixture
def macro_to_micro_transition():
    source = {
        "zoom_level": 0.35,
        "pan_x": 100.0,
        "pan_y": 150.0,
        "focal_node_title": "Global System Architecture Overview",
    }
    target = {
        "zoom_level": 3.20,
        "pan_x": 1600.0,
        "pan_y": 1400.0,
        "focal_node_title": "Register Cache Line Pipeline Spec",
    }
    landmarks = [
        {"title": "Core Domain Cluster"},
        {"title": "Execution Unit Interface"},
        {"title": "Microcode Memory Bank"},
    ]
    return source, target, landmarks


def test_nominal_transition():
    tracker = FovealHorizonTracker()
    source = {"zoom_level": 1.0, "pan_x": 200.0, "pan_y": 200.0, "focal_node_title": "A"}
    target = {"zoom_level": 1.2, "pan_x": 260.0, "pan_y": 240.0, "focal_node_title": "B"}

    result = tracker.track_transition(source, target)
    assert isinstance(result, FovealHorizonResult)
    assert result.telemetry.visual_drift_latency_ms < 500.0
    assert result.telemetry.disorientation_risk in ("NOMINAL", "MODERATE")
    assert result.telemetry.cowan_bounded is True
    assert len(result.breadcrumbs) >= 2


def test_deep_macro_micro_transition(macro_to_micro_transition):
    tracker = FovealHorizonTracker()
    source, target, landmarks = macro_to_micro_transition

    result = tracker.track_transition(source, target, landmarks=landmarks)

    assert result.telemetry.zoom_ratio > 8.0
    assert result.telemetry.pan_displacement_px > 1500.0
    assert result.telemetry.visual_drift_latency_ms > 700.0
    assert result.telemetry.disorientation_risk in ("ELEVATED", "CRITICAL")
    assert result.telemetry.cowan_bounded is True
    assert len(result.breadcrumbs) <= 4

    # Verify landmark integration into breadcrumbs
    labels = [b.label for b in result.breadcrumbs]
    assert any("Core Domain Cluster" in l for l in labels)


def test_svg_export(tmp_path: Path, macro_to_micro_transition):
    tracker = FovealHorizonTracker()
    source, target, landmarks = macro_to_micro_transition
    result = tracker.track_transition(source, target, landmarks=landmarks)

    svg_file = tmp_path / "foveal_horizon.svg"
    svg_content = tracker.export_svg(result, output_path=str(svg_file))

    assert "<svg" in svg_content
    assert "</svg>" in svg_content
    assert "Dynamic Foveal Horizon" in svg_content
    assert svg_file.exists()
    assert svg_file.stat().st_size > 500


def test_ascii_report(macro_to_micro_transition):
    tracker = FovealHorizonTracker()
    source, target, landmarks = macro_to_micro_transition
    result = tracker.track_transition(source, target, landmarks=landmarks)
    report = tracker.generate_ascii_report(result)

    assert "DYNAMIC FOVEAL HORIZON & CONTEXT ANCHOR RESTORER" in report
    assert "Zoom Transition" in report
    assert "Visual Drift Latency" in report
    assert "[ANCHOR]" in report


def test_restorative_css(macro_to_micro_transition):
    tracker = FovealHorizonTracker()
    source, target, _ = macro_to_micro_transition
    result = tracker.track_transition(source, target)

    assert ".dx-foveal-transition" in result.restorative_css
    assert "cubic-bezier" in result.restorative_css
    assert "will-change" in result.restorative_css


def test_zero_em_dashes():
    source_files = [
        Path("scripts/foveal_horizon_tracker.py"),
        Path("tests/test_foveal_horizon_tracker.py"),
    ]
    for p in source_files:
        if p.exists():
            text = p.read_text(encoding="utf-8")
            assert "\u2014" not in text, f"Em dash found in {p}"
