"""
test_semantic_anchor_distiller.py - Unit tests for SemanticAnchorDistiller (Phase 102, Cycle 98).

Tests Rosch prototype anchor distillation, spatial cluster centroid computation,
thumbnail radar SVG map generation, Obsidian Canvas export, and zero em dashes.

Strict constraint: Strictly zero em dashes (Unicode U+2014) anywhere.
"""

from pathlib import Path
import pytest
from scripts.semantic_anchor_distiller import (
    CanvasItem,
    DistillationResult,
    DistillationTelemetry,
    SemanticAnchorDistiller,
    SemanticCluster,
)


@pytest.fixture
def multi_cluster_canvas_items():
    return [
        # Cluster 1: Architecture & Systems (Coordinates around 100, 100)
        {
            "id": "node_arch_1",
            "x": 80.0,
            "y": 90.0,
            "title": "Dual-Code Memory Interleaver",
            "category": "Architecture",
            "text_content": "Phonological loop and visuospatial sketchpad dual processing system.",
            "salience_weight": 0.95,
            "tags": ["memory", "dual-code", "baddeley"],
        },
        {
            "id": "node_arch_2",
            "x": 120.0,
            "y": 140.0,
            "title": "Buffer Compactor",
            "category": "Architecture",
            "text_content": "FIFO buffer compaction maintaining strict Cowan bounds.",
            "salience_weight": 0.60,
            "tags": ["memory", "buffer"],
        },
        {
            "id": "node_arch_3",
            "x": 100.0,
            "y": 180.0,
            "title": "Working Set Pruner",
            "category": "Architecture",
            "text_content": "Dynamic working set anchor eviction for cognitive stamina.",
            "salience_weight": 0.70,
            "tags": ["memory", "pruner"],
        },
        # Cluster 2: Ocular & Reading Flow (Coordinates around 1400, 900)
        {
            "id": "node_eye_1",
            "x": 1380.0,
            "y": 880.0,
            "title": "Saccadic Fatigue Damper",
            "category": "Ocular",
            "text_content": "Carpenter main sequence peak velocity decay tracking.",
            "salience_weight": 0.92,
            "tags": ["saccade", "carpenter", "fatigue"],
        },
        {
            "id": "node_eye_2",
            "x": 1420.0,
            "y": 920.0,
            "title": "Optimal Viewing Position Calibrator",
            "category": "Ocular",
            "text_content": "Rayner OVP lexical fixation anchor placement.",
            "salience_weight": 0.85,
            "tags": ["rayner", "ovp", "lexical"],
        },
    ]


def test_empty_canvas():
    distiller = SemanticAnchorDistiller()
    result = distiller.distill_canvas([])
    assert isinstance(result, DistillationResult)
    assert result.telemetry.total_canvas_items == 0
    assert result.telemetry.total_clusters_formed == 0
    assert result.telemetry.cowan_bounded_clusters is True
    assert len(result.clusters) == 0
    assert len(result.anchor_landmarks) == 0


def test_distill_clusters_and_anchors(multi_cluster_canvas_items):
    distiller = SemanticAnchorDistiller(cluster_distance_threshold=400.0)
    result = distiller.distill_canvas(
        multi_cluster_canvas_items,
        viewport={"x": 50.0, "y": 50.0, "width": 400.0, "height": 300.0}
    )

    assert result.telemetry.total_canvas_items == 5
    assert result.telemetry.total_clusters_formed == 2
    assert result.telemetry.cowan_bounded_clusters is True
    assert result.telemetry.prototype_clarity_score > 70.0
    assert result.telemetry.working_memory_bandwidth_saved_pct >= 50.0

    # Verify prototype selection: highest salience weight in each group
    titles = [a["title"] for a in result.anchor_landmarks]
    assert "Dual-Code Memory Interleaver" in titles
    assert "Saccadic Fatigue Damper" in titles


def test_cowan_cluster_bounding():
    distiller = SemanticAnchorDistiller(cluster_distance_threshold=200.0)

    # 5 distant items -> 5 separate clusters -> exceeds Cowan 4-chunk capacity
    scattered_items = [
        {"id": f"scat_{i}", "x": i * 1000.0, "y": i * 1000.0, "title": f"Distant Node {i}", "salience_weight": 0.8}
        for i in range(5)
    ]
    res_scattered = distiller.distill_canvas(scattered_items)
    assert res_scattered.telemetry.total_clusters_formed == 5
    assert res_scattered.telemetry.cowan_bounded_clusters is False


def test_svg_radar_export(tmp_path: Path, multi_cluster_canvas_items):
    distiller = SemanticAnchorDistiller(cluster_distance_threshold=400.0)
    result = distiller.distill_canvas(multi_cluster_canvas_items)

    svg_file = tmp_path / "radar_map.svg"
    svg_content = distiller.export_svg(result, output_path=str(svg_file))

    assert "<svg" in svg_content
    assert "</svg>" in svg_content
    assert "Multi-Scale Semantic Anchor Distiller" in svg_content
    assert "CURRENT VIEWPORT" not in svg_content  # No viewport specified
    assert svg_file.exists()
    assert svg_file.stat().st_size > 500


def test_canvas_json_export(tmp_path: Path, multi_cluster_canvas_items):
    distiller = SemanticAnchorDistiller(cluster_distance_threshold=400.0)
    result = distiller.distill_canvas(multi_cluster_canvas_items)

    canvas_file = tmp_path / "distilled.canvas"
    distiller.export_canvas(result, output_path=str(canvas_file))

    assert canvas_file.exists()
    assert len(result.canvas_json["nodes"]) == 5
    assert len(result.canvas_json["edges"]) >= 1


def test_ascii_report(multi_cluster_canvas_items):
    distiller = SemanticAnchorDistiller(cluster_distance_threshold=400.0)
    result = distiller.distill_canvas(multi_cluster_canvas_items)
    report = distiller.generate_ascii_report(result)

    assert "SEMANTIC ANCHOR DISTILLER & VISUAL INDEXER" in report
    assert "Canvas Nodes Processed" in report
    assert "Distilled Clusters" in report
    assert "[HUB]" in report


def test_zero_em_dashes():
    source_files = [
        Path("scripts/semantic_anchor_distiller.py"),
        Path("tests/test_semantic_anchor_distiller.py"),
    ]
    for p in source_files:
        if p.exists():
            text = p.read_text(encoding="utf-8")
            assert "\u2014" not in text, f"Em dash found in {p}"
