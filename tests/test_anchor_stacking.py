"""Unit tests for Autonomous Cognitive Spatial Working Memory Anchor Stacking & Compaction Harness.

Strict Quality Gate: Zero em dashes anywhere (use hyphens, commas, or parentheses).
"""

from __future__ import annotations

import json
from pathlib import Path
import pytest

from scripts.anchor_stacking import (
    AnchorStackCompactor,
    AnchorStackTelemetry,
    MemoryToken,
    SpatialBreadcrumb,
    StackStatus,
)


def test_empty_input_handling() -> None:
    """Ensure anchor stack compactor handles empty input gracefully without errors."""
    compactor = AnchorStackCompactor()
    tokens, breadcrumbs, telemetry = compactor.compact_stack()

    assert len(tokens) == 0
    assert len(breadcrumbs) == 0
    assert telemetry.total_input_nodes == 0
    assert telemetry.compacted_tokens_count == 0
    assert telemetry.memory_load_reduction_pct == 0.0


def test_subgraph_compaction() -> None:
    """Verify multiple nodes within resolved subgraphs are condensed into single tokens."""
    compactor = AnchorStackCompactor(max_working_memory_capacity=4)
    data = {
        "subgraphs": {
            "sg_auth": {
                "title": "Authentication Sub-System",
                "status": "resolved",
                "nodes": ["JWT Issuer", "OAuth Client", "Token Revocation Store", "Rate Limiter"],
                "depth": 1,
            },
            "sg_storage": {
                "title": "LSM Storage Engine",
                "status": "active",
                "nodes": ["MemTable", "Write-Ahead Log", "SSTable Flusher"],
                "depth": 2,
            },
            "sg_network": {
                "title": "gRPC Network Gateway",
                "status": "suspended",
                "nodes": ["TLS Handler", "Protobuf Codec"],
                "depth": 1,
            },
        }
    }
    compactor.load_dict(data)
    tokens, breadcrumbs, telemetry = compactor.compact_stack()

    assert len(tokens) == 3
    assert telemetry.total_input_nodes == 9
    assert telemetry.compacted_tokens_count == 3
    # Reduction: (9 - 3) / 9 = 66.7%
    assert telemetry.memory_load_reduction_pct > 60.0

    token_map = {t.token_id: t for t in tokens}
    auth_tok = token_map["sg_auth"]
    assert auth_tok.status == StackStatus.RESOLVED
    assert auth_tok.original_node_count == 4
    assert auth_tok.compaction_ratio == 4.0


def test_breadcrumb_trail_generation() -> None:
    """Verify hierarchical breadcrumb trail preserves depth and spatial coordinates."""
    compactor = AnchorStackCompactor()
    data = {
        "root": {"title": "Root Architecture", "depth": 0, "nodes": ["Main System"]},
        "sub_core": {"title": "Core Pipeline", "depth": 1, "nodes": ["Ingestion"]},
        "leaf_filter": {"title": "Bloom Filter", "depth": 2, "nodes": ["Bit Array"]},
    }
    compactor.load_dict(data)
    tokens, breadcrumbs, telemetry = compactor.compact_stack()

    assert len(breadcrumbs) == 3
    # Check monotonic depth ordering
    assert breadcrumbs[0].depth == 0
    assert breadcrumbs[1].depth == 1
    assert breadcrumbs[2].depth == 2

    # Check zoom levels decrease with depth
    assert breadcrumbs[0].zoom_scale > breadcrumbs[2].zoom_scale


def test_canvas_export(tmp_path: Path) -> None:
    """Verify export to Obsidian .canvas with breadcrumb banner and color badges."""
    compactor = AnchorStackCompactor()
    data = {
        "subgraphs": {
            "cluster_a": {"title": "Cluster A", "status": "resolved", "nodes": ["N1", "N2"]},
            "cluster_b": {"title": "Cluster B", "status": "active", "nodes": ["N3"]},
        }
    }
    compactor.load_dict(data)

    out_file = str(tmp_path / "compacted_stack.canvas")
    res = compactor.to_canvas(out_file, canvas_title="Anchor Stack Map")

    assert Path(out_file).exists()
    assert "nodes" in res
    assert len(res["nodes"]) == 3  # 2 tokens + 1 breadcrumb ribbon card

    # Verify ribbon card
    ribbon = next(n for n in res["nodes"] if n["id"] == "breadcrumb_ribbon")
    assert "Spatial Navigation Breadcrumb" in ribbon["text"]
    assert ribbon["color"] == "6"


def test_svg_export(tmp_path: Path) -> None:
    """Verify publication-grade SVG generation with dark titanium styling."""
    compactor = AnchorStackCompactor()
    data = {
        "m1": {"title": "Memory Hub 1", "status": "resolved", "nodes": ["A", "B", "C"]},
        "m2": {"title": "Memory Hub 2", "status": "active", "nodes": ["D"]},
    }
    compactor.load_dict(data)

    out_file = str(tmp_path / "compacted_stack.svg")
    svg_str = compactor.to_svg(out_file, width=1200, height=800)

    assert Path(out_file).exists()
    assert "<svg" in svg_str
    assert "</svg>" in svg_str
    assert "#0B0F17" in svg_str
    assert "Anchor Stack Telemetry" in svg_str
    assert "Working Memory Relief" in svg_str


def test_ascii_report() -> None:
    """Verify terminal ASCII summary report output."""
    compactor = AnchorStackCompactor()
    data = {
        "task_1": {"title": "Database Optimization", "status": "resolved", "nodes": ["Indexes", "Queries"]},
    }
    compactor.load_dict(data)
    tokens, breadcrumbs, telemetry = compactor.compact_stack()
    report = compactor.render_ascii_stack(telemetry)

    assert "Spatial Working Memory Anchor Stacking & Compaction Report" in report
    assert "Total Subgraph Items:" in report
    assert "SPATIAL BREADCRUMB TRAIL" in report


def test_zero_em_dashes_in_module() -> None:
    """Verify neither script nor test contains em dashes."""
    root_dir = Path(__file__).parent.parent
    script_path = root_dir / "scripts" / "anchor_stacking.py"
    test_path = root_dir / "tests" / "test_anchor_stacking.py"

    for p in [script_path, test_path]:
        content = p.read_text(encoding="utf-8")
        assert "\u2014" not in content, f"Em dash found in {p.name}"
