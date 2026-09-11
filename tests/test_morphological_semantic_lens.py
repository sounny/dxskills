"""
Unit tests for Morphological Semantic Lens and Granularity Zoom Engine.
Strict zero em dash policy enforced.
"""

import pytest
import math
from scripts.morphological_semantic_lens import (
    SemanticNode,
    MorphologicalNodeView,
    MorphologicalLensTelemetry,
    MorphologicalSemanticLens,
)


def test_semantic_node_creation_and_dict():
    node = SemanticNode(
        node_id="n-1",
        label="Root Architecture",
        granularity_level="MACRO_ARCHITECTURAL",
        abstraction_depth=0.1,
        x=200.0,
        y=300.0,
        importance_weight=0.9,
        details=["High level topology", "Module boundary"],
    )
    d = node.to_dict()
    assert d["node_id"] == "n-1"
    assert d["label"] == "Root Architecture"
    assert d["granularity_level"] == "MACRO_ARCHITECTURAL"
    assert d["abstraction_depth"] == 0.1
    assert d["x"] == 200.0
    assert d["y"] == 300.0
    assert len(d["details"]) == 2


def test_compute_semantic_zoom_macro_lod():
    lens = MorphologicalSemanticLens()
    nodes = [
        SemanticNode("n-1", "System Root", "MACRO_ARCHITECTURAL", 0.05, 100.0, 100.0),
    ]
    telemetry = lens.compute_semantic_zoom(nodes, focus_x=100.0, focus_y=100.0, zoom_factor=0.4)
    assert telemetry.zoom_factor == 0.4
    assert telemetry.active_primary_lod == "MACRO_ARCHITECTURAL"
    assert telemetry.foveal_node_count == 1
    assert telemetry.views[0].is_in_foveal_focus is True
    assert telemetry.views[0].apparent_lod == "MACRO_ARCHITECTURAL"


def test_compute_semantic_zoom_meso_lod():
    lens = MorphologicalSemanticLens()
    nodes = [
        SemanticNode("n-1", "Cache Cluster", "MESO_SUBSYSTEM", 0.3, 100.0, 100.0),
    ]
    telemetry = lens.compute_semantic_zoom(nodes, focus_x=100.0, focus_y=100.0, zoom_factor=1.0)
    assert telemetry.active_primary_lod == "MESO_SUBSYSTEM"
    assert telemetry.foveal_node_count == 1


def test_compute_semantic_zoom_micro_and_atomic_lod():
    lens = MorphologicalSemanticLens()
    nodes = [
        SemanticNode("n-1", "Hasher", "MICRO_COMPONENT", 0.6, 100.0, 100.0),
        SemanticNode("n-2", "Register Pointer", "ATOMIC_PRIMITIVE", 0.95, 100.0, 100.0),
    ]
    telemetry_micro = lens.compute_semantic_zoom(nodes, focus_x=100.0, focus_y=100.0, zoom_factor=2.0)
    assert telemetry_micro.active_primary_lod == "MICRO_COMPONENT"

    telemetry_atomic = lens.compute_semantic_zoom(nodes, focus_x=100.0, focus_y=100.0, zoom_factor=3.5)
    assert telemetry_atomic.active_primary_lod == "ATOMIC_PRIMITIVE"


def test_cowan_capacity_optimal_vs_overload():
    lens = MorphologicalSemanticLens(base_focal_radius_px=100.0, max_cowan_foveal_capacity=4)
    # Create 3 nodes inside fovea
    nodes_optimal = [
        SemanticNode(f"opt-{i}", f"Node {i}", "MESO_SUBSYSTEM", 0.3, 100.0 + i * 10.0, 100.0)
        for i in range(3)
    ]
    telemetry_opt = lens.compute_semantic_zoom(nodes_optimal, focus_x=100.0, focus_y=100.0, zoom_factor=1.0)
    assert telemetry_opt.foveal_node_count == 3
    assert telemetry_opt.status_level == "OPTIMAL_COGNITIVE_LOAD"
    assert len(telemetry_opt.warnings) == 0
    assert telemetry_opt.cognitive_density_score >= 80.0

    # Create 7 nodes inside fovea (exceeds Cowan limit of 4)
    nodes_overload = [
        SemanticNode(f"ovr-{i}", f"Dense Node {i}", "MICRO_COMPONENT", 0.7, 100.0 + (i % 3) * 15.0, 100.0 + (i // 3) * 15.0)
        for i in range(7)
    ]
    telemetry_ovr = lens.compute_semantic_zoom(nodes_overload, focus_x=100.0, focus_y=100.0, zoom_factor=1.0)
    assert telemetry_ovr.foveal_node_count == 7
    assert telemetry_ovr.status_level == "PERCEPTUAL_OVERLOAD"
    assert len(telemetry_ovr.warnings) > 0
    assert "exceed Cowan capacity" in telemetry_ovr.warnings[0]
    assert telemetry_ovr.cognitive_density_score < 75.0


def test_sparse_granularity_status():
    lens = MorphologicalSemanticLens(base_focal_radius_px=50.0)
    nodes = [
        SemanticNode("far-1", "Distant Star", "MACRO_ARCHITECTURAL", 0.1, 500.0, 500.0),
    ]
    telemetry = lens.compute_semantic_zoom(nodes, focus_x=100.0, focus_y=100.0, zoom_factor=1.0)
    assert telemetry.foveal_node_count == 0
    assert telemetry.status_level == "SPARSE_GRANULARITY"
    assert telemetry.peripheral_node_count == 1
    assert "No semantic anchors located" in telemetry.warnings[0]


def test_parafoveal_and_peripheral_decay():
    lens = MorphologicalSemanticLens(base_focal_radius_px=100.0, parafoveal_expansion_ratio=2.0)
    nodes = [
        SemanticNode("fov-1", "Center Node", "MESO_SUBSYSTEM", 0.3, 100.0, 100.0),
        SemanticNode("para-1", "Midway Node", "MESO_SUBSYSTEM", 0.3, 100.0, 250.0),  # dist = 150 (parafoveal)
        SemanticNode("peri-1", "Outer Node", "MESO_SUBSYSTEM", 0.3, 100.0, 450.0),   # dist = 350 (peripheral)
    ]
    telemetry = lens.compute_semantic_zoom(nodes, focus_x=100.0, focus_y=100.0, zoom_factor=1.0)
    v_fov = telemetry.views[0]
    v_para = telemetry.views[1]
    v_peri = telemetry.views[2]

    assert v_fov.is_in_foveal_focus is True
    assert v_para.is_in_parafoveal_zone is True
    assert v_peri.is_in_foveal_focus is False
    assert v_peri.is_in_parafoveal_zone is False

    assert v_fov.opacity > v_para.opacity
    assert v_para.opacity > v_peri.opacity
    assert v_fov.apparent_scale > v_para.apparent_scale


def test_demo_telemetry_generation():
    telemetry = MorphologicalSemanticLens.create_demo_telemetry()
    assert telemetry.zoom_factor == 1.4
    assert telemetry.active_primary_lod in ["MESO_SUBSYSTEM", "MICRO_COMPONENT"]
    assert len(telemetry.views) == 9
    assert telemetry.foveal_node_count > 0
    d = telemetry.to_dict()
    assert "cognitive_density_score" in d
    assert "views" in d


def test_markdown_report_formatting():
    telemetry = MorphologicalSemanticLens.create_demo_telemetry()
    lens = MorphologicalSemanticLens()
    report = lens.generate_markdown_report(telemetry)
    assert "# Morphological Semantic Lens & Granularity Zoom Report" in report
    assert "Cognitive Load Status:" in report
    assert "| **Current Zoom Factor** |" in report
    assert "| **Active Primary LOD** |" in report
    assert "| Node Label | Granularity Tier |" in report
    assert "Cowan Capacity Protection (N <= 4)" in report


def test_svg_rendering_integrity():
    telemetry = MorphologicalSemanticLens.create_demo_telemetry()
    lens = MorphologicalSemanticLens()
    svg = lens.generate_svg(telemetry)
    assert svg.startswith("<svg")
    assert svg.endswith("</svg>")
    assert 'id="fovealGrad"' in svg
    assert 'id="parafovealGrad"' in svg
    assert "Morphological Semantic Lens" in svg
    assert "Foveal Inspection Aperture" in svg


def test_zero_em_dashes_enforcement():
    with open("scripts/morphological_semantic_lens.py", "r", encoding="utf-8") as f:
        script_content = f.read()
    assert chr(8212) not in script_content, "Em dash detected in scripts/morphological_semantic_lens.py!"

    with open("tests/test_morphological_semantic_lens.py", "r", encoding="utf-8") as f:
        test_content = f.read()
    assert chr(8212) not in test_content, "Em dash detected in tests/test_morphological_semantic_lens.py!"
