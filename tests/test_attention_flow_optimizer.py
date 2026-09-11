"""Unit tests for Autonomous Cognitive Spatial Multi-Scale Attention Heatmap & Density Flow Optimizer.

Tests verify:
- Empty canvas handling
- Simulated gaze dwell time and crowding calculations
- Stagnation zone detection, padding expansion, and card decomposition suggestions
- Shannon visual entropy calculation
- Obsidian .canvas export with heat-adjusted geometry
- Publication-grade SVG rendering
- ASCII report formatting
- Strict zero em dash rule enforcement

Strict Quality Gate: Zero em dashes anywhere (use hyphens, commas, or parentheses).
"""

import json
import os
import pytest

from scripts.attention_flow_optimizer import (
    AttentionFlowOptimizer,
    AttentionFlowTelemetry,
    HeatZoneCategory,
    NodeAttentionProfile,
)


def test_empty_canvas_handling():
    optimizer = AttentionFlowOptimizer()
    optimizer.load_dict({})
    profiles, telemetry = optimizer.optimize_attention_flow()

    assert profiles == []
    assert telemetry.total_nodes == 0
    assert telemetry.mean_dwell_time_ms == 0.0
    assert telemetry.stagnation_risk_count == 0


def test_dwell_time_and_crowding_simulation():
    optimizer = AttentionFlowOptimizer(baseline_wpm=200.0)
    nodes = {
        "nodes": {
            "n_light": {"title": "Light Card", "text": "Quick headline anchor", "x": 100, "y": 100, "width": 300, "height": 150},
            "n_dense": {
                "title": "Dense Card",
                "text": "Extremely detailed architectural narrative containing multiple nested specifications "
                        "and explanatory sentences that require substantial cognitive fixation time to parse.",
                "x": 500,
                "y": 100,
                "width": 200,
                "height": 100,
            },
        }
    }
    optimizer.load_dict(nodes)
    profiles, telemetry = optimizer.optimize_attention_flow()

    assert len(profiles) == 2
    p_light = next(p for p in profiles if p.node_id == "n_light")
    p_dense = next(p for p in profiles if p.node_id == "n_dense")

    assert p_light.simulated_dwell_time_ms < p_dense.simulated_dwell_time_ms
    assert p_light.fixational_drift_radius_px < p_dense.fixational_drift_radius_px


def test_stagnation_detection_and_splitting():
    optimizer = AttentionFlowOptimizer(stagnation_dwell_threshold_ms=400.0)
    dense_text = "word " * 35  # 35 words on small card will yield > 400ms dwell
    nodes = {
        "nodes": {
            "n_stagnant": {"title": "Stagnant Node", "text": dense_text, "x": 100, "y": 100, "width": 150, "height": 80}
        }
    }
    optimizer.load_dict(nodes)
    profiles, telemetry = optimizer.optimize_attention_flow()

    assert len(profiles) == 1
    prof = profiles[0]
    assert prof.zone == HeatZoneCategory.STAGNATION_ALERT
    assert prof.split_recommended
    assert prof.recommended_padding_boost_px > 0
    assert telemetry.stagnation_risk_count == 1


def test_shannon_entropy_calculation():
    optimizer = AttentionFlowOptimizer()
    nodes = {
        "nodes": {
            "n1": {"title": "Entropy Test", "text": "a bb ccc dddd eeeee", "x": 100, "y": 100}
        }
    }
    optimizer.load_dict(nodes)
    profiles, _ = optimizer.optimize_attention_flow()

    assert profiles[0].entropy_bits > 1.5


def test_canvas_export(tmp_path):
    optimizer = AttentionFlowOptimizer()
    demo_canvas = {
        "nodes": [
            {"id": "c1", "text": "# Card 1\nSimple topic", "x": 100, "y": 100, "width": 260, "height": 140},
            {"id": "c2", "text": "# Card 2\nSecond balanced topic", "x": 450, "y": 100, "width": 260, "height": 140},
        ],
        "edges": []
    }
    optimizer.load_canvas(demo_canvas)
    out_file = tmp_path / "attention_flow.canvas"
    res = optimizer.to_canvas(str(out_file))

    assert out_file.exists()
    assert len(res["nodes"]) == 2
    assert "Zone:" in res["nodes"][0]["text"]


def test_svg_export(tmp_path):
    optimizer = AttentionFlowOptimizer()
    nodes = {
        "nodes": {
            "a": {"title": "Alpha", "text": "Core domain architecture", "x": 100, "y": 100, "width": 260, "height": 140},
            "b": {"title": "Beta", "text": "Secondary conduit channel", "x": 500, "y": 200, "width": 260, "height": 140},
        }
    }
    optimizer.load_dict(nodes)
    out_svg = tmp_path / "attention_heatmap.svg"
    svg_str = optimizer.to_svg(str(out_svg))

    assert out_svg.exists()
    assert "<svg" in svg_str
    assert "Spatial Attention Heatmap &amp; Density Flow Optimizer" in svg_str
    assert "heatBlur" in svg_str
    assert "Attention Density Metrics" in svg_str


def test_ascii_report():
    optimizer = AttentionFlowOptimizer()
    nodes = {
        "nodes": {
            "node_hub": {"title": "Core Hub", "text": "System overview", "x": 100, "y": 100}
        }
    }
    optimizer.load_dict(nodes)
    _, telemetry = optimizer.optimize_attention_flow()
    report = optimizer.render_ascii_report(telemetry)

    assert "Spatial Attention Heatmap & Density Flow Optimization Report" in report
    assert "Core Hub" in report
    assert "Mean Simulated Gaze Dwell:" in report


def test_zero_em_dashes_in_module():
    scripts_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "scripts", "attention_flow_optimizer.py")
    test_path = __file__

    with open(scripts_path, "r", encoding="utf-8") as f:
        src_text = f.read()
    with open(test_path, "r", encoding="utf-8") as f:
        test_text = f.read()

    assert chr(8212) not in src_text, "Found em dash in scripts/attention_flow_optimizer.py"
    assert chr(8212) not in test_text, "Found em dash in tests/test_attention_flow_optimizer.py"
