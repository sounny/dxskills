"""
Unit tests for Anchor Stacking & Hierarchical Zoom Lens.
Verifies multi-tier level-of-detail resolution, micro-anchor collapse into hulls,
crowding index computation, Cowan bound compliance, dark titanium SVG rendering,
and markdown audit reports. Strictly zero em dashes enforced.
"""

import pytest
from scripts.anchor_stacking_zoom_lens import (
    SemanticAnchor,
    CollapsedClusterHull,
    ZoomLensTelemetry,
    AnchorStackingZoomLens,
    sample_knowledge_hierarchy,
)


def test_semantic_anchor_initialization():
    anchor = SemanticAnchor(
        anchor_id="anc-1",
        title="Dialectic Resolution Core",
        x=250.0,
        y=180.0,
        lod_level=0,
        saliency=4.2,
        tags=["core", "dialectic"],
    )
    assert anchor.anchor_id == "anc-1"
    assert anchor.lod_level == 0
    assert anchor.parent_id is None
    assert anchor.saliency == 4.2
    assert "core" in anchor.tags


def test_determine_lod_tier():
    lens = AnchorStackingZoomLens(macro_zoom_threshold=0.55, meso_zoom_threshold=1.15)
    assert lens.determine_lod_tier(0.3) == (0, "Macro")
    assert lens.determine_lod_tier(0.54) == (0, "Macro")
    assert lens.determine_lod_tier(0.55) == (1, "Meso")
    assert lens.determine_lod_tier(1.0) == (1, "Meso")
    assert lens.determine_lod_tier(1.15) == (2, "Micro")
    assert lens.determine_lod_tier(2.0) == (2, "Micro")


def test_evaluate_zoom_macro_collapse():
    lens = AnchorStackingZoomLens()
    anchors = sample_knowledge_hierarchy()  # 3 macro, 4 meso, 4 micro = 11 total

    telemetry = lens.evaluate_zoom(anchors, zoom_factor=0.4)
    assert telemetry.active_lod_tier == "Macro"
    assert telemetry.visible_anchor_count == 3
    assert len(telemetry.visible_anchors) == 3
    # Check all visible are lod 0
    for a in telemetry.visible_anchors:
        assert a.lod_level == 0

    assert telemetry.collapsed_cluster_count > 0
    assert len(telemetry.collapsed_hulls) > 0


def test_evaluate_zoom_meso():
    lens = AnchorStackingZoomLens()
    anchors = sample_knowledge_hierarchy()

    telemetry = lens.evaluate_zoom(anchors, zoom_factor=0.85)
    assert telemetry.active_lod_tier == "Meso"
    # Macro (3) + Meso (4) = 7 visible anchors
    assert telemetry.visible_anchor_count == 7
    for a in telemetry.visible_anchors:
        assert a.lod_level in [0, 1]

    # Micro anchors (4) should be stacked into hulls
    assert telemetry.collapsed_cluster_count > 0


def test_evaluate_zoom_micro_full():
    lens = AnchorStackingZoomLens()
    anchors = sample_knowledge_hierarchy()

    telemetry = lens.evaluate_zoom(anchors, zoom_factor=1.5)
    assert telemetry.active_lod_tier == "Micro"
    assert telemetry.visible_anchor_count == len(anchors)
    assert telemetry.collapsed_cluster_count == 0
    assert len(telemetry.collapsed_hulls) == 0


def test_crowding_index_and_cowan_compliance():
    lens = AnchorStackingZoomLens()
    anchors = sample_knowledge_hierarchy()

    macro_telemetry = lens.evaluate_zoom(anchors, zoom_factor=0.4)
    assert macro_telemetry.cowan_compliant is True
    assert 0.0 <= macro_telemetry.cognitive_load_score <= 1.0

    micro_telemetry = lens.evaluate_zoom(anchors, zoom_factor=1.8)
    assert 0.0 <= micro_telemetry.cognitive_load_score <= 1.0


def test_generate_svg():
    lens = AnchorStackingZoomLens()
    anchors = sample_knowledge_hierarchy()
    telemetry = lens.evaluate_zoom(anchors, zoom_factor=0.75)

    svg_code = lens.generate_svg(telemetry)
    assert "<svg" in svg_code
    assert "</svg>" in svg_code
    assert "lensGlow" in svg_code
    assert "HIERARCHICAL ZOOM LENS HUD" in svg_code
    assert chr(8212) not in svg_code


def test_generate_markdown_report():
    lens = AnchorStackingZoomLens()
    anchors = sample_knowledge_hierarchy()
    telemetry = lens.evaluate_zoom(anchors, zoom_factor=0.75)

    md_report = lens.generate_markdown_report(telemetry)
    assert "# Anchor Stacking and Hierarchical Zoom Lens Telemetry" in md_report
    assert "## 1. Executive Zoom State Overview" in md_report
    assert "## 3. Visible Spatial Anchors" in md_report
    assert "## 4. Collapsed Cluster Envelopes" in md_report
    assert chr(8212) not in md_report
