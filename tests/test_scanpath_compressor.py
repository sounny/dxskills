"""Unit tests for Autonomous Cognitive Spatial Saccadic Scanpath Compressor & Reading Flow Harness.

Strict Quality Gate: Zero em dashes anywhere.
"""

import json
from pathlib import Path
import pytest

from scripts.scanpath_compressor import (
    GuidanceMode,
    SaccadicScanpathCompressor,
    ScanpathTelemetry,
)


def test_audit_scanpath_empty():
    compressor = SaccadicScanpathCompressor()
    telemetry = compressor.audit_scanpath("")
    assert telemetry.total_words == 0
    assert telemetry.regression_rate_pct == 0.0
    assert telemetry.scanpath_efficiency_ratio == 1.0


def test_audit_scanpath_metrics():
    compressor = SaccadicScanpathCompressor()
    sample_text = (
        "Distributed asynchronous state machines coordinate deterministic state across multiple geographic regions. "
        "Consensus protocols eliminate split-brain synchronization anomalies during partition degradation."
    )
    telemetry = compressor.audit_scanpath(sample_text, baseline_wpm=175.0)

    assert telemetry.total_words > 15
    assert telemetry.estimated_regressions_count > 0
    assert 0.40 <= telemetry.scanpath_efficiency_ratio <= 0.95
    assert telemetry.projected_wpm > telemetry.baseline_wpm
    assert telemetry.wpm_speedup_pct > 10.0


def test_apply_bionic_ramp():
    compressor = SaccadicScanpathCompressor()
    assert compressor.apply_bionic_ramp("a") == "a"
    assert compressor.apply_bionic_ramp("cat") == "**c**at"
    assert compressor.apply_bionic_ramp("engine") == "**en**gine"
    assert compressor.apply_bionic_ramp("protocol") == "**pro**tocol"
    assert compressor.apply_bionic_ramp("deterministic") == "**dete**rministic"


def test_compress_and_guide_modes():
    compressor = SaccadicScanpathCompressor(target_line_chars=40)
    sample_text = (
        "Distributed database systems require continuous validation of synchronization boundaries "
        "to prevent catastrophic transactional degradation."
    )

    # Test Bionic Ramp mode
    guided_bionic, tel_bionic = compressor.compress_and_guide(sample_text, mode=GuidanceMode.BIONIC_RAMP)
    assert "**" in guided_bionic
    assert len(guided_bionic.split("\n")) >= 2

    # Test Return Beacon mode
    guided_beacon, tel_beacon = compressor.compress_and_guide(sample_text, mode=GuidanceMode.RETURN_BEACON)
    assert "> " in guided_beacon


def test_export_canvas_and_svg(tmp_path):
    compressor = SaccadicScanpathCompressor()
    sample_text = "Spatial cognition offloads working memory by mapping conceptual structures to 2D geometric space."
    guided_text, telemetry = compressor.compress_and_guide(sample_text)

    canvas_file = tmp_path / "scanpath.canvas"
    canvas_data = compressor.export_canvas(guided_text, telemetry, str(canvas_file))
    assert canvas_file.exists()
    assert len(canvas_data["nodes"]) >= 2
    assert "Scanpath Compressor" in canvas_data["nodes"][0]["text"]

    svg_file = tmp_path / "scanpath.svg"
    svg_str = compressor.export_svg_scanpath(telemetry, str(svg_file))
    assert svg_file.exists()
    assert "<svg" in svg_str
    assert "</svg>" in svg_str
    assert "Saccadic Scanpath" in svg_str
    assert "Guided Saccadic Corridor" in svg_str


def test_zero_em_dashes_enforcement():
    compressor = SaccadicScanpathCompressor()
    sample_text = "Cognitive reading harnesses restructure linear sentences into balanced visual corridors."
    guided_text, telemetry = compressor.compress_and_guide(sample_text)
    md_report = compressor.generate_markdown_report(telemetry)
    svg_str = compressor.export_svg_scanpath(telemetry)
    canvas_data = compressor.export_canvas(guided_text, telemetry)

    full_text = md_report + svg_str + guided_text + json.dumps(canvas_data) + json.dumps(telemetry.to_dict())
    assert chr(8212) not in full_text
    assert "\u2014" not in full_text
