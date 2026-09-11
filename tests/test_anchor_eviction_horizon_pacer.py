"""
Unit tests for Anchor Eviction & Graceful Horizon Pacer Engine.
Verifies Ebbinghaus decay, lifecycle state transitions, memory pressure,
SVG generation, report output, and strict zero-em-dash compliance.
"""

import os
import pytest
from scripts.anchor_eviction_horizon_pacer import (
    DecayingAnchor,
    EvictionState,
    AnchorEvictionTelemetry,
    AnchorEvictionHorizonPacer,
)


def test_decaying_anchor_initialization():
    anchor = DecayingAnchor(
        anchor_id="anc_01",
        title="Primary Research Node",
        created_at_s=100.0,
        last_accessed_s=150.0,
        base_saliency=1.5,
        half_life_s=300.0,
        pos_x=120.0,
        pos_y=80.0,
    )
    assert anchor.anchor_id == "anc_01"
    assert anchor.title == "Primary Research Node"
    assert anchor.base_saliency == 1.5
    assert anchor.half_life_s == 300.0
    assert anchor.pos_x == 120.0
    assert anchor.pos_y == 80.0


def test_calculate_retention_ebbinghaus():
    pacer = AnchorEvictionHorizonPacer()
    anchor = DecayingAnchor(
        anchor_id="anc_calc",
        title="Decay Math Test",
        created_at_s=0.0,
        last_accessed_s=100.0,
        base_saliency=1.0,
        half_life_s=200.0,
    )

    # At exact access time, retention is 1.0
    ret_now = pacer.calculate_retention(anchor, current_time_s=100.0)
    assert ret_now == pytest.approx(1.0, abs=1e-3)

    # Future access calculation
    ret_elapsed = pacer.calculate_retention(anchor, current_time_s=300.0)
    assert 0.45 <= ret_elapsed <= 0.55

    # Very distant future
    ret_distant = pacer.calculate_retention(anchor, current_time_s=5000.0)
    assert ret_distant < 0.01


def test_evaluate_session_empty():
    pacer = AnchorEvictionHorizonPacer()
    telemetry = pacer.evaluate_session([], current_time_s=500.0)
    assert telemetry.total_anchors == 0
    assert telemetry.working_memory_pressure == 0.0
    assert not telemetry.overload_warning
    assert len(telemetry.anchor_states) == 0


def test_lifecycle_state_transitions():
    pacer = AnchorEvictionHorizonPacer()
    now = 1000.0

    # Create anchors with controlled last_accessed_s
    # base half life = 300s, base_saliency = 1.0 -> effective half-life = 300s
    a_fresh = DecayingAnchor("a1", "Fresh Node", 0.0, now - 10.0)      # ret > 0.95
    a_maturing = DecayingAnchor("a2", "Maturing Node", 0.0, now - 200.0) # ret ~ 0.63
    a_sunset = DecayingAnchor("a3", "Sunset Node", 0.0, now - 500.0)   # ret ~ 0.31
    a_breadcrumb = DecayingAnchor("a4", "Breadcrumb Node", 0.0, now - 1000.0) # ret ~ 0.09
    a_evicted = DecayingAnchor("a5", "Evicted Node", 0.0, now - 2000.0) # ret ~ 0.009

    telemetry = pacer.evaluate_session(
        [a_fresh, a_maturing, a_sunset, a_breadcrumb, a_evicted],
        current_time_s=now,
    )

    assert telemetry.total_anchors == 5
    assert telemetry.fresh_count == 1
    assert telemetry.maturing_count == 1
    assert telemetry.sunset_count == 1
    assert telemetry.breadcrumb_count == 1
    assert telemetry.evicted_count == 1

    states_by_id = {s.anchor_id: s for s in telemetry.anchor_states}
    assert states_by_id["a1"].lifecycle_state == "fresh"
    assert states_by_id["a1"].opacity == 1.0
    assert states_by_id["a2"].lifecycle_state == "maturing"
    assert states_by_id["a2"].opacity == 0.85
    assert states_by_id["a3"].lifecycle_state == "sunset"
    assert states_by_id["a3"].opacity == 0.55
    assert states_by_id["a4"].lifecycle_state == "breadcrumb"
    assert states_by_id["a4"].opacity == 0.25
    assert states_by_id["a5"].lifecycle_state == "evicted"
    assert states_by_id["a5"].opacity == 0.0


def test_working_memory_pressure_overload():
    pacer = AnchorEvictionHorizonPacer(pressure_threshold=3.0)
    now = 500.0

    # 4 high saliency fresh anchors -> pressure = 4 * 1.5 = 6.0 > 3.0
    anchors = [
        DecayingAnchor(f"high_{i}", f"Important Node {i}", 0.0, now - 5.0, base_saliency=1.5)
        for i in range(4)
    ]
    telemetry = pacer.evaluate_session(anchors, current_time_s=now)
    assert telemetry.working_memory_pressure > 3.0
    assert telemetry.overload_warning is True


def test_generate_svg():
    pacer = AnchorEvictionHorizonPacer()
    now = 600.0
    anchors = [
        DecayingAnchor("a1", "Fresh Node", 0.0, now - 5.0, pos_x=100.0, pos_y=150.0),
        DecayingAnchor("a2", "Sunset Node", 0.0, now - 400.0, pos_x=300.0, pos_y=250.0),
        DecayingAnchor("a3", "Evicted Node", 0.0, now - 2000.0, pos_x=500.0, pos_y=350.0),
    ]
    telemetry = pacer.evaluate_session(anchors, current_time_s=now)
    svg = pacer.generate_svg(telemetry, width=800, height=500)

    assert "<svg" in svg
    assert "</svg>" in svg
    assert "sunsetSky" in svg
    assert "Fresh Node" in svg
    assert "Sunset Node" in svg
    assert "Evicted Node" not in svg  # Evicted anchors are not rendered in SVG


def test_generate_markdown_report():
    pacer = AnchorEvictionHorizonPacer()
    now = 800.0
    anchors = [
        DecayingAnchor("a1", "Core Synthesis", 0.0, now - 20.0, pos_x=100.0, pos_y=120.0),
        DecayingAnchor("a2", "Secondary Schema", 0.0, now - 350.0, pos_x=220.0, pos_y=180.0),
    ]
    telemetry = pacer.evaluate_session(anchors, current_time_s=now)
    report = pacer.generate_markdown_report(telemetry)

    assert "# Working Memory Anchor Eviction and Horizon Pacer Telemetry" in report
    assert "Core Synthesis" in report
    assert "Secondary Schema" in report
    assert "Cowan Capacity Bound Status" in report


def test_zero_em_dashes_in_source_and_outputs():
    # Verify module source file
    script_path = os.path.join(os.path.dirname(__file__), "..", "scripts", "anchor_eviction_horizon_pacer.py")
    with open(script_path, "r", encoding="utf-8") as f:
        source = f.read()
    assert chr(8212) not in source

    # Verify report and svg outputs
    pacer = AnchorEvictionHorizonPacer()
    anchors = [DecayingAnchor("a1", "Zero Dash Anchor", 0.0, 50.0)]
    telemetry = pacer.evaluate_session(anchors, current_time_s=100.0)
    report = pacer.generate_markdown_report(telemetry)
    svg = pacer.generate_svg(telemetry)

    assert chr(8212) not in report
    assert chr(8212) not in svg
