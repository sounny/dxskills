"""Unit tests for Autonomous Cognitive Spatial Working Memory Anchor Eviction & Dynamic Working Set Pruner.

Tests verify:
- Empty canvas handling
- Cowan 4-chunk capacity bounding
- Non-destructive peripheral ghosting and bead compaction
- Explicit focal override behavior
- Obsidian .canvas export
- Publication-grade SVG rendering
- ASCII report formatting
- Strict zero em dash rule enforcement

Strict Quality Gate: Zero em dashes anywhere (use hyphens, commas, or parentheses).
"""

import json
import os
import pytest

from scripts.working_set_pruner import (
    PrunedNodeProfile,
    PruneState,
    WorkingSetPruner,
    WorkingSetPrunerTelemetry,
)


def test_empty_canvas_handling():
    pruner = WorkingSetPruner()
    pruner.load_dict({})
    profiles, telemetry = pruner.prune_working_set()

    assert profiles == []
    assert telemetry.total_nodes == 0
    assert telemetry.active_focus_count == 0
    assert telemetry.working_memory_headroom_gain_pct == 0.0


def test_cowan_capacity_bounding():
    pruner = WorkingSetPruner(max_active_working_set=3)
    nodes = {
        f"node_{i}": {
            "title": f"Card {i}",
            "text": f"Content {i}",
            "recency": i,
            "fixations": 2,
        }
        for i in range(8)
    }
    pruner.load_dict(nodes)
    profiles, telemetry = pruner.prune_working_set()

    assert len(profiles) == 8
    assert telemetry.active_focus_count == 3

    active_nodes = [p for p in profiles if p.state == PruneState.ACTIVE_FOCUS]
    assert len(active_nodes) == 3
    for a in active_nodes:
        assert a.visual_opacity == 1.00


def test_ghosting_and_bead_compaction():
    pruner = WorkingSetPruner(max_active_working_set=2, ghost_opacity=0.35, stagnant_threshold_score=0.25)
    nodes = {
        "n_top1": {"title": "Top 1", "text": "Recent", "recency": 10, "fixations": 5},
        "n_top2": {"title": "Top 2", "text": "Recent", "recency": 9, "fixations": 4},
        "n_mid": {"title": "Mid", "text": "Moderate", "recency": 5, "fixations": 1},
        "n_stale": {"title": "Stale", "text": "Dormant", "recency": 0, "fixations": 0},
    }
    pruner.load_dict(nodes)
    profiles, telemetry = pruner.prune_working_set()

    prof_map = {p.node_id: p for p in profiles}
    assert prof_map["n_top1"].state == PruneState.ACTIVE_FOCUS
    assert prof_map["n_top2"].state == PruneState.ACTIVE_FOCUS
    assert prof_map["n_mid"].state == PruneState.PERIPHERAL_GHOST
    assert prof_map["n_mid"].visual_opacity == 0.35
    assert prof_map["n_stale"].state == PruneState.COMPACTED_BEAD
    assert prof_map["n_stale"].bead_cluster_id is not None


def test_explicit_focal_override():
    pruner = WorkingSetPruner(max_active_working_set=2)
    nodes = {
        "n1": {"title": "Older", "text": "Important node", "recency": 1, "fixations": 1},
        "n2": {"title": "Newer 1", "text": "Content", "recency": 8, "fixations": 1},
        "n3": {"title": "Newer 2", "text": "Content", "recency": 9, "fixations": 1},
    }
    pruner.load_dict(nodes)
    # Force n1 into focal set
    profiles, telemetry = pruner.prune_working_set(focal_ids=["n1"])

    prof_map = {p.node_id: p for p in profiles}
    assert prof_map["n1"].state == PruneState.ACTIVE_FOCUS


def test_canvas_export(tmp_path):
    pruner = WorkingSetPruner(max_active_working_set=2)
    demo_canvas = {
        "nodes": [
            {"id": "c1", "text": "# Card 1\nActive", "x": 100, "y": 100, "width": 260, "height": 140},
            {"id": "c2", "text": "# Card 2\nSecond", "x": 400, "y": 100, "width": 260, "height": 140},
            {"id": "c3", "text": "# Card 3\nThird", "x": 700, "y": 100, "width": 260, "height": 140},
        ],
        "edges": []
    }
    pruner.load_canvas(demo_canvas)
    out_file = tmp_path / "pruned.canvas"
    res = pruner.to_canvas(str(out_file))

    assert out_file.exists()
    assert len(res["nodes"]) == 3
    assert any("[ACTIVE FOCUS]" in n["text"] for n in res["nodes"])


def test_svg_export(tmp_path):
    pruner = WorkingSetPruner()
    nodes = {
        "nodes": {
            "a": {"title": "Card A", "text": "Core active focus", "x": 100, "y": 100, "width": 260, "height": 140},
            "b": {"title": "Card B", "text": "Distant dormant node", "x": 500, "y": 200, "width": 260, "height": 140},
        }
    }
    pruner.load_dict(nodes)
    out_svg = tmp_path / "pruned_map.svg"
    svg_str = pruner.to_svg(str(out_svg))

    assert out_svg.exists()
    assert "<svg" in svg_str
    assert "Spatial Working Memory Anchor Eviction" in svg_str
    assert "focusGlow" in svg_str
    assert "Active Focus Set:" in svg_str


def test_ascii_report():
    pruner = WorkingSetPruner()
    nodes = {
        "nodes": {
            "node_1": {"title": "Executive Gateway", "text": "Routing core", "x": 100, "y": 100}
        }
    }
    pruner.load_dict(nodes)
    _, telemetry = pruner.prune_working_set()
    report = pruner.render_ascii_report(telemetry)

    assert "Spatial Working Memory Anchor Eviction & Working Set Report" in report
    assert "Executive Gateway" in report
    assert "Active Cowan Focus Set:" in report


def test_zero_em_dashes_in_module():
    scripts_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "scripts", "working_set_pruner.py")
    test_path = __file__

    with open(scripts_path, "r", encoding="utf-8") as f:
        src_text = f.read()
    with open(test_path, "r", encoding="utf-8") as f:
        test_text = f.read()

    assert chr(8212) not in src_text, "Found em dash in scripts/working_set_pruner.py"
    assert chr(8212) not in test_text, "Found em dash in tests/test_working_set_pruner.py"
