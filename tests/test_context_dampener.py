"""
Unit tests for ContextSwitchDampener in DxSkills.

Enforces zero em dash compliance and validates attention residue modeling,
cognitive bookmark creation, canvas export, and SVG gauge rendering.
"""

import json
from pathlib import Path
import pytest

from scripts.context_dampener import (
    ContextState,
    ContextSwitchDampener,
    InterleavingTelemetry,
)


def test_clean_switch_low_residue():
    dampener = ContextSwitchDampener()
    state = ContextState(
        project_name="Docsite Minor Fix",
        active_thread="Correct typo in README",
        depth_of_focus=3.0,
        completion_ratio=0.95,
        time_in_flow_min=10.0,
        unresolved_tensions=[],
        immediate_next_step="Push commit to main",
    )
    telem = dampener.evaluate_switch(state)

    assert isinstance(telem, InterleavingTelemetry)
    assert telem.attention_residue_score < 35.0
    assert telem.interleaving_readiness == "Safe to Switch"
    assert telem.open_loops_count == 0
    assert telem.estimated_recovery_minutes < 10.0


def test_high_residue_severe_bleed():
    dampener = ContextSwitchDampener()
    state = ContextState(
        project_name="Core Consensus Engine",
        active_thread="Debugging Raft split-brain partition race",
        depth_of_focus=9.5,
        completion_ratio=0.48,  # Near 0.5 peak Zeigarnik effect
        time_in_flow_min=65.0,
        unresolved_tensions=[
            "Term index desynchronization on worker node 3",
            "Fsync barrier timeout under high IOPS",
            "Uncommitted log entries during master handover",
        ],
        immediate_next_step="Inspect tcpdump pcap log around term 14 switch",
    )
    telem = dampener.evaluate_switch(state)

    assert telem.attention_residue_score > 60.0
    assert telem.interleaving_readiness in ["Moderate Residue", "Critical Cognitive Bleed"]
    assert telem.open_loops_count == 3
    assert telem.estimated_recovery_minutes > 12.0


def test_canvas_export(tmp_path: Path):
    dampener = ContextSwitchDampener()
    state = ContextState(
        project_name="Search Mesh",
        active_thread="Vector clustering indexing",
        depth_of_focus=7.0,
        completion_ratio=0.5,
        time_in_flow_min=30.0,
        unresolved_tensions=["Cosine distance threshold test failing"],
        immediate_next_step="Update HNSW index build parameter M=16",
    )
    telem = dampener.evaluate_switch(state)
    out_file = tmp_path / "test_bookmark.canvas"

    canvas_data = dampener.export_canvas(state, telem, output_path=str(out_file))
    assert out_file.exists()

    assert "nodes" in canvas_data
    assert "edges" in canvas_data
    assert len(canvas_data["nodes"]) >= 3
    assert len(canvas_data["edges"]) >= 2


def test_svg_gauge():
    dampener = ContextSwitchDampener()
    state = ContextState(
        project_name="UI Kit",
        active_thread="Typography token sync",
        depth_of_focus=5.0,
        completion_ratio=0.7,
        time_in_flow_min=20.0,
        unresolved_tensions=[],
        immediate_next_step="Verify mobile font scale",
    )
    telem = dampener.evaluate_switch(state)
    svg = dampener.export_svg_gauge(telem, width=600, height=360)

    assert "<svg" in svg
    assert "</svg>" in svg
    assert "Context Switch Dampener" in svg
    assert "UI Kit" in svg
    assert "Attention Residue Load" in svg


def test_markdown_summary():
    dampener = ContextSwitchDampener()
    state = ContextState(
        project_name="Data Pipeline",
        active_thread="Kafka partition consumer loop",
        depth_of_focus=6.5,
        completion_ratio=0.6,
        time_in_flow_min=25.0,
        unresolved_tensions=["Offset commit retry logic"],
        immediate_next_step="Add exponential backoff wrapper",
    )
    telem = dampener.evaluate_switch(state)
    md = dampener.export_summary_markdown(state, telem)

    assert "# Context Switch Dampener and Cognitive Bookmark" in md
    assert "Data Pipeline" in md
    assert "Immediate Re-entry Vector" in md
    assert "Zero phonological friction" in md


def test_zero_em_dash_compliance():
    """Verify that no em dashes exist anywhere in the code, tests, or generated outputs."""
    em_dash = chr(8212)

    src_path = Path("scripts/context_dampener.py")
    if src_path.exists():
        content = src_path.read_text(encoding="utf-8")
        assert em_dash not in content, "Found em dash in scripts/context_dampener.py"

    dampener = ContextSwitchDampener()
    state = ContextState(
        project_name="Mission Critical Core",
        active_thread="Hypergraph sync",
        depth_of_focus=8.0,
        completion_ratio=0.5,
        time_in_flow_min=45.0,
        unresolved_tensions=["Edge weight decay", "Ring buffer overflow"],
        immediate_next_step="Re-run benchmark suite",
    )
    telem = dampener.evaluate_switch(state)

    md = dampener.export_summary_markdown(state, telem)
    assert em_dash not in md, "Found em dash in markdown report"

    svg = dampener.export_svg_gauge(telem)
    assert em_dash not in svg, "Found em dash in SVG gauge"

    canvas_dict = dampener.export_canvas(state, telem, output_path="")
    canvas_str = json.dumps(canvas_dict)
    assert em_dash not in canvas_str, "Found em dash in canvas JSON"
