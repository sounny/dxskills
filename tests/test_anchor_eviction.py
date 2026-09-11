"""
Unit tests for MemoryBufferCompactor in DxSkills.

Enforces zero em dash compliance and validates FIFO decay,
saliency compaction, canvas export, and SVG buffer rendering.
"""

import json
from pathlib import Path
import pytest

from scripts.anchor_eviction import (
    CompactionAudit,
    MemoryBufferCompactor,
    WorkingMemoryNode,
)


def test_saliency_decay_and_reference_boost():
    # Fresh node with references
    node_fresh = WorkingMemoryNode("n1", "Active Thread", base_importance=8.0, idle_minutes=0.0, reference_count=2)
    s_fresh = node_fresh.calculate_saliency()
    assert s_fresh >= 8.0

    # Stale node with zero references
    node_stale = WorkingMemoryNode("n2", "Dormant Thread", base_importance=8.0, idle_minutes=30.0, reference_count=0)
    s_stale = node_stale.calculate_saliency()
    assert s_stale < s_fresh


def test_empty_buffer_compaction():
    compactor = MemoryBufferCompactor(capacity_limit=5)
    audit = compactor.compact_buffer([])

    assert isinstance(audit, CompactionAudit)
    assert audit.initial_node_count == 0
    assert audit.retained_node_count == 0
    assert audit.compacted_node_count == 0
    assert audit.headroom_gain_pct == 0.0


def test_buffer_compaction_within_and_exceeding_capacity():
    compactor = MemoryBufferCompactor(capacity_limit=3)

    nodes = [
        WorkingMemoryNode("n1", "Top Task", base_importance=9.0, idle_minutes=2.0, reference_count=3),
        WorkingMemoryNode("n2", "Medium Task", base_importance=7.0, idle_minutes=5.0, reference_count=1),
        WorkingMemoryNode("n3", "Low Task", base_importance=5.0, idle_minutes=10.0, reference_count=0),
        WorkingMemoryNode("n4", "Old Task", base_importance=4.0, idle_minutes=25.0, reference_count=0),
        WorkingMemoryNode("n5", "Ancient Task", base_importance=3.0, idle_minutes=45.0, reference_count=0),
    ]

    audit = compactor.compact_buffer(nodes)

    assert audit.initial_node_count == 5
    assert audit.retained_node_count == 3
    assert audit.compacted_node_count == 2
    assert audit.headroom_gain_pct > 0.0
    assert audit.retained_nodes[0].id == "n1"
    assert audit.compacted_nodes[-1].id == "n5"


def test_canvas_export(tmp_path: Path):
    compactor = MemoryBufferCompactor(capacity_limit=2)
    nodes = [
        WorkingMemoryNode("n1", "Critical Thread", base_importance=9.0, idle_minutes=1.0),
        WorkingMemoryNode("n2", "Active Thread", base_importance=7.0, idle_minutes=3.0),
        WorkingMemoryNode("n3", "Dormant Thread", base_importance=4.0, idle_minutes=20.0),
    ]
    audit = compactor.compact_buffer(nodes)
    out_file = tmp_path / "test_compact.canvas"

    canvas_data = compactor.export_canvas(audit, output_path=str(out_file))
    assert out_file.exists()

    assert "nodes" in canvas_data
    assert "edges" in canvas_data
    assert len(canvas_data["nodes"]) >= 3
    assert len(canvas_data["edges"]) >= 1


def test_svg_telemetry():
    compactor = MemoryBufferCompactor(capacity_limit=4)
    nodes = [
        WorkingMemoryNode("n1", "Task 1", base_importance=8.0, idle_minutes=2.0),
        WorkingMemoryNode("n2", "Task 2", base_importance=6.0, idle_minutes=5.0),
    ]
    audit = compactor.compact_buffer(nodes)
    svg = compactor.export_svg_telemetry(audit, width=600, height=360)

    assert "<svg" in svg
    assert "</svg>" in svg
    assert "Working Memory FIFO Buffer Compactor" in svg
    assert "Active Buffer Slots" in svg


def test_markdown_summary():
    compactor = MemoryBufferCompactor(capacity_limit=3)
    nodes = [
        WorkingMemoryNode("n1", "Sprint Item", base_importance=8.0, idle_minutes=1.0),
        WorkingMemoryNode("n2", "Old Bug", base_importance=3.0, idle_minutes=40.0),
    ]
    audit = compactor.compact_buffer(nodes)
    md = compactor.export_summary_markdown(audit)

    assert "# Working Memory Anchor Eviction" in md
    assert "Sprint Item" in md
    assert "Zero phonological friction" in md


def test_zero_em_dash_compliance():
    """Verify that no em dashes exist anywhere in the code, tests, or generated outputs."""
    em_dash = chr(8212)

    src_path = Path("scripts/anchor_eviction.py")
    if src_path.exists():
        content = src_path.read_text(encoding="utf-8")
        assert em_dash not in content, "Found em dash in scripts/anchor_eviction.py"

    compactor = MemoryBufferCompactor(capacity_limit=2)
    nodes = [
        WorkingMemoryNode("n1", "Task Alpha", base_importance=8.0, idle_minutes=1.0),
        WorkingMemoryNode("n2", "Task Beta", base_importance=5.0, idle_minutes=15.0),
        WorkingMemoryNode("n3", "Task Gamma", base_importance=3.0, idle_minutes=35.0),
    ]
    audit = compactor.compact_buffer(nodes)

    md = compactor.export_summary_markdown(audit)
    assert em_dash not in md, "Found em dash in markdown summary"

    svg = compactor.export_svg_telemetry(audit)
    assert em_dash not in svg, "Found em dash in SVG telemetry"

    canvas_dict = compactor.export_canvas(audit, output_path="")
    canvas_str = json.dumps(canvas_dict)
    assert em_dash not in canvas_str, "Found em dash in canvas JSON"
