"""
Unit tests for WorkingMemoryHorizonVisualizer in DxSkills.

Enforces zero em dash compliance and validates multi-scale horizon mapping,
bandwidth allocation, canvas export, and SVG radar generation.
"""

import json
from pathlib import Path
import pytest

from scripts.horizon_visualizer import (
    HorizonItem,
    HorizonTelemetry,
    WorkingMemoryHorizonVisualizer,
)


def test_empty_horizon_items():
    viz = WorkingMemoryHorizonVisualizer()
    telem = viz.evaluate_horizons([])

    assert isinstance(telem, HorizonTelemetry)
    assert telem.total_items == 0
    assert telem.immediate_count == 0
    assert "Empty" in telem.balance_status


def test_balanced_horizon_items():
    viz = WorkingMemoryHorizonVisualizer()
    items = [
        HorizonItem("imm-1", "Fix compiler warning", "immediate", 0.5, 2.0),
        HorizonItem("imm-2", "Review pull request", "immediate", 1.0, 3.0),
        HorizonItem("tac-1", "Implement caching middleware", "tactical", 12.0, 6.0),
        HorizonItem("tac-2", "Refactor database adapter", "tactical", 16.0, 7.0),
        HorizonItem("str-1", "Migrate to multi-region mesh", "strategic", 120.0, 9.0),
    ]
    telem = viz.evaluate_horizons(items)

    assert telem.total_items == 5
    assert telem.immediate_count == 2
    assert telem.tactical_count == 2
    assert telem.strategic_count == 1
    assert telem.fragmentation_index < 0.5
    assert telem.balance_status == "Coherent Multi-Scale Alignment"


def test_foveal_overload_detection():
    viz = WorkingMemoryHorizonVisualizer()
    items = [
        HorizonItem(f"imm-{i}", f"Urgent task {i}", "immediate", 1.0, 4.0)
        for i in range(7)
    ]
    telem = viz.evaluate_horizons(items)

    assert telem.immediate_count == 7
    assert telem.immediate_bandwidth_pct == 100.0
    assert "Overload" in telem.balance_status or "Fragmentation" in telem.balance_status
    assert any("Foveal overload" in r for r in telem.recommendations)


def test_canvas_export(tmp_path: Path):
    viz = WorkingMemoryHorizonVisualizer()
    items = [
        HorizonItem("imm-1", "Immediate hotfix", "immediate", 0.5, 3.0),
        HorizonItem("tac-1", "Tactical milestone", "tactical", 10.0, 6.0, parent_id="str-1"),
        HorizonItem("str-1", "Strategic north star", "strategic", 80.0, 9.0),
    ]
    telem = viz.evaluate_horizons(items)
    out_file = tmp_path / "test_horizon.canvas"

    canvas_data = viz.export_canvas(items, telem, output_path=str(out_file))
    assert out_file.exists()

    assert "nodes" in canvas_data
    assert "edges" in canvas_data
    assert len(canvas_data["nodes"]) >= 4
    assert len(canvas_data["edges"]) >= 1


def test_svg_radar():
    viz = WorkingMemoryHorizonVisualizer()
    items = [
        HorizonItem("imm-1", "Immediate action", "immediate", 1.0, 3.0),
        HorizonItem("tac-1", "Tactical sprint", "tactical", 8.0, 5.0),
        HorizonItem("str-1", "Strategic horizon", "strategic", 40.0, 8.0),
    ]
    telem = viz.evaluate_horizons(items)
    svg = viz.export_svg_radar(items, telem, width=640, height=420)

    assert "<svg" in svg
    assert "</svg>" in svg
    assert "Working Memory Horizon Radar" in svg
    assert "Immediate" in svg
    assert "Tactical" in svg
    assert "Strategic" in svg


def test_markdown_summary():
    viz = WorkingMemoryHorizonVisualizer()
    items = [
        HorizonItem("imm-1", "Sprint item", "immediate", 2.0, 4.0),
        HorizonItem("tac-1", "Architecture review", "tactical", 14.0, 7.0),
    ]
    telem = viz.evaluate_horizons(items)
    md = viz.export_summary_markdown(telem, items)

    assert "# Multi-Scale Working Memory Horizon Audit" in md
    assert "Cognitive Balance Status:" in md
    assert "Immediate Horizon" in md
    assert "Zero phonological friction" in md


def test_zero_em_dash_compliance():
    """Verify that no em dashes exist anywhere in the code, tests, or generated outputs."""
    em_dash = chr(8212)

    src_path = Path("scripts/horizon_visualizer.py")
    if src_path.exists():
        content = src_path.read_text(encoding="utf-8")
        assert em_dash not in content, "Found em dash in scripts/horizon_visualizer.py"

    viz = WorkingMemoryHorizonVisualizer()
    items = [
        HorizonItem("imm-1", "Task Alpha", "immediate", 1.0, 2.0),
        HorizonItem("tac-1", "Feature Beta", "tactical", 10.0, 5.0),
        HorizonItem("str-1", "Platform Gamma", "strategic", 60.0, 8.0),
    ]
    telem = viz.evaluate_horizons(items)

    md = viz.export_summary_markdown(telem, items)
    assert em_dash not in md, "Found em dash in markdown summary"

    svg = viz.export_svg_radar(items, telem)
    assert em_dash not in svg, "Found em dash in SVG radar"

    canvas_dict = viz.export_canvas(items, telem, output_path="")
    canvas_str = json.dumps(canvas_dict)
    assert em_dash not in canvas_str, "Found em dash in canvas JSON"
