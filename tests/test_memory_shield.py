"""Unit tests for Autonomous Cognitive Spatial Saliency Decoupling & Working Memory Shield.

Strict Quality Gate: Zero em dashes anywhere.
"""

import json
from pathlib import Path
import pytest

from scripts.memory_shield import (
    MemoryShieldTelemetry,
    ShieldedNode,
    ShieldTier,
    WorkingMemoryShield,
)


def test_geometry_calculations():
    shield = WorkingMemoryShield()
    node_a = {"x": 0, "y": 0, "width": 100, "height": 100}
    node_b = {"x": 300, "y": 400, "width": 100, "height": 100}

    assert shield.calculate_node_center(node_a) == (50.0, 50.0)
    assert shield.calculate_node_center(node_b) == (350.0, 450.0)
    dist = shield.calculate_distance(node_a, node_b)
    assert pytest.approx(dist, rel=1e-2) == 500.0


def test_intrusion_risk_evaluation():
    shield = WorkingMemoryShield()
    sparse_node = {"text": "simple note"}
    dense_node = {"text": "CRITICAL ALERT DENSE MULTI-SYSTEM DISTRIBUTED FAILURE PROTOCOL WITH IMMEDIATE ATTENTION REQUIRED"}

    risk_sparse = shield.evaluate_intrusion_risk(sparse_node, distance=100.0)
    risk_dense = shield.evaluate_intrusion_risk(dense_node, distance=800.0)

    assert risk_sparse < risk_dense
    assert 0.05 <= risk_sparse <= 1.0
    assert 0.05 <= risk_dense <= 1.0


def test_empty_canvas():
    shield = WorkingMemoryShield()
    canvas, telemetry = shield.apply_memory_shield({"nodes": []})
    assert telemetry.total_nodes == 0
    assert telemetry.focus_count == 0
    assert telemetry.dampened_count == 0


def test_concentric_tiers_and_exports(tmp_path: Path):
    shield = WorkingMemoryShield(focus_radius_px=400.0, orientation_radius_px=900.0)

    canvas_data = {
        "nodes": [
            {"id": "node-focus", "x": 0, "y": 0, "width": 200, "height": 100, "text": "Active Architecture Focus"},
            {"id": "node-near", "x": 250, "y": 0, "width": 200, "height": 100, "text": "Sub-component relation"},
            {"id": "node-mid", "x": 650, "y": 0, "width": 200, "height": 100, "text": "Related cluster context header"},
            {"id": "node-far", "x": 1400, "y": 0, "width": 200, "height": 100, "text": "Distant legacy archive notes and backlog items"},
        ]
    }

    shielded_canvas, telemetry = shield.apply_memory_shield(canvas_data, focus_ids=["node-focus"])

    assert telemetry.total_nodes == 4
    assert telemetry.focus_count >= 1
    assert telemetry.orientation_count >= 1
    assert telemetry.dampened_count >= 1
    assert telemetry.avg_intrusion_mitigation_pct > 0.0
    assert telemetry.cognitive_bandwidth_reclaimed_pct > 0.0

    # Verify HUD node was appended to canvas
    hud_nodes = [n for n in shielded_canvas["nodes"] if n.get("id") == "node-memory-shield-hud"]
    assert len(hud_nodes) == 1
    assert "Working Memory Shield Engaged" in hud_nodes[0]["text"]

    # Verify text dampening on far node
    far_node = next(n for n in shielded_canvas["nodes"] if n.get("id") == "node-far")
    assert "Shielded Ambient" in far_node["text"]

    # ASCII report
    ascii_rep = shield.render_ascii_report(telemetry)
    assert "Working Memory Shield & Saliency Decoupler" in ascii_rep
    assert "node-focus" in ascii_rep

    # SVG export
    svg_path = tmp_path / "test_shield.svg"
    shield.export_svg_shield(telemetry, svg_path)
    assert svg_path.exists()
    svg_data = svg_path.read_text(encoding="utf-8")
    assert "<svg" in svg_data
    assert "FOCUS ZONE" in svg_data


def test_zero_em_dashes():
    script_file = Path(__file__).resolve().parent.parent / "scripts" / "memory_shield.py"
    test_file = Path(__file__).resolve()

    em_dash = chr(8212)
    assert em_dash not in script_file.read_text(encoding="utf-8")
    assert em_dash not in test_file.read_text(encoding="utf-8")
