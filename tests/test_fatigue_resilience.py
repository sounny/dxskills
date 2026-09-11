"""
Unit tests for FatigueResilienceHarness in DxSkills.

Enforces zero em dash compliance and validates ocular fatigue calculations,
protocol generation, canvas export, and SVG rendering.
"""

import json
from pathlib import Path
import pytest

from scripts.fatigue_resilience import (
    BreakProtocol,
    FatigueResilienceHarness,
    FatigueTelemetry,
    SaccadeSample,
)


def test_empty_saccade_stream():
    harness = FatigueResilienceHarness()
    telemetry = harness.analyze_saccade_stream([], session_duration_min=10.0)

    assert isinstance(telemetry, FatigueTelemetry)
    assert telemetry.total_fixations == 0
    assert telemetry.saturation_level == "Optimal"
    assert telemetry.fatigue_score < 35.0


def test_saccade_stream_mild_and_strain():
    harness = FatigueResilienceHarness()

    # Mild scenario: normal fixations, 10% regressions, 20m session
    mild_samples = [
        SaccadeSample(timestamp=i * 0.3, fixation_duration_ms=220.0, jump_amplitude_deg=3.5, is_regression=(i % 10 == 0))
        for i in range(50)
    ]
    mild_telem = harness.analyze_saccade_stream(mild_samples, session_duration_min=20.0)
    assert mild_telem.total_fixations == 50
    assert mild_telem.regression_rate == 0.1
    assert mild_telem.saturation_level in ["Optimal", "Mild Fatigue"]

    # Severe scenario: long fixations, 50% regressions, 60m session
    strain_samples = [
        SaccadeSample(timestamp=i * 0.4, fixation_duration_ms=380.0, jump_amplitude_deg=1.5, is_regression=(i % 2 == 0))
        for i in range(50)
    ]
    strain_telem = harness.analyze_saccade_stream(strain_samples, session_duration_min=60.0)
    assert strain_telem.regression_rate == 0.5
    assert strain_telem.fatigue_score > 60.0
    assert strain_telem.saturation_level in ["Cognitive Strain", "Exhaustion Threshold"]


def test_generate_break_protocol_levels():
    harness = FatigueResilienceHarness()

    levels = [
        (20.0, "micro_defocus"),
        (45.0, "saccadic_reset"),
        (65.0, "spatial_breathing"),
        (85.0, "executive_walk"),
    ]

    for score, expected_type in levels:
        telem = FatigueTelemetry(
            session_duration_min=30.0,
            total_fixations=100,
            regression_rate=0.2,
            mean_fixation_ms=250.0,
            fatigue_score=score,
            saturation_level="Test",
            recommended_break_type="Test Break",
        )
        proto = harness.generate_break_protocol(telem)
        assert proto.protocol_type == expected_type
        assert len(proto.guidance_steps) >= 3
        assert proto.duration_sec > 0


def test_canvas_export(tmp_path: Path):
    harness = FatigueResilienceHarness()
    telem = FatigueTelemetry(
        session_duration_min=45.0,
        total_fixations=80,
        regression_rate=0.3,
        mean_fixation_ms=320.0,
        fatigue_score=68.0,
        saturation_level="Cognitive Strain",
        recommended_break_type="Spatial Breathing (3m)",
    )
    proto = harness.generate_break_protocol(telem)
    out_file = tmp_path / "test_break.canvas"

    canvas_str = harness.export_spatial_canvas(proto, output_path=str(out_file))
    assert out_file.exists()

    data = json.loads(canvas_str)
    assert "nodes" in data
    assert "edges" in data
    assert len(data["nodes"]) >= 4
    assert len(data["edges"]) >= 3


def test_svg_visualizer():
    harness = FatigueResilienceHarness()
    proto = BreakProtocol(
        name="Test Dynamic Defocus",
        duration_sec=30,
        protocol_type="micro_defocus",
        guidance_steps=["Step 1", "Step 2"],
        breathing_pattern={"inhale": 4, "hold_in": 4, "exhale": 4, "hold_out": 4},
    )
    svg = harness.export_svg_breathing_visualizer(proto, width=600, height=350)

    assert "<svg" in svg
    assert "</svg>" in svg
    assert "Test Dynamic Defocus" in svg
    assert "EXPAND" in svg


def test_markdown_report():
    harness = FatigueResilienceHarness()
    telem = FatigueTelemetry(
        session_duration_min=25.0,
        total_fixations=60,
        regression_rate=0.15,
        mean_fixation_ms=230.0,
        fatigue_score=38.0,
        saturation_level="Mild Fatigue",
        recommended_break_type="Saccadic Reset (60s)",
    )
    proto = harness.generate_break_protocol(telem)
    md = harness.generate_markdown_report(telem, proto)

    assert "# Spatial Fatigue Telemetry" in md
    assert "Mild Fatigue" in md
    assert "Saccadic Reset" in md
    assert "Zero phonological friction" in md


def test_zero_em_dash_compliance():
    """Verify that no em dashes exist anywhere in the code, tests, or generated outputs."""
    em_dash = chr(8212)

    # Check source file
    src_path = Path("scripts/fatigue_resilience.py")
    if src_path.exists():
        content = src_path.read_text(encoding="utf-8")
        assert em_dash not in content, "Found em dash in scripts/fatigue_resilience.py"

    # Check generated reports and visualizers
    harness = FatigueResilienceHarness()
    for score in [20.0, 50.0, 70.0, 90.0]:
        telem = FatigueTelemetry(
            session_duration_min=30.0,
            total_fixations=100,
            regression_rate=0.25,
            mean_fixation_ms=280.0,
            fatigue_score=score,
            saturation_level="Level",
            recommended_break_type="Break",
        )
        proto = harness.generate_break_protocol(telem)
        md = harness.generate_markdown_report(telem, proto)
        assert em_dash not in md, f"Found em dash in markdown report for score {score}"

        svg = harness.export_svg_breathing_visualizer(proto)
        assert em_dash not in svg, f"Found em dash in SVG for score {score}"

        canvas = harness.export_spatial_canvas(proto, output_path="")
        assert em_dash not in canvas, f"Found em dash in canvas for score {score}"
