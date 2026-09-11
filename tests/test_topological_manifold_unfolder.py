"""
Unit tests for Topological Manifold Unfolder and Polytope Net Weaver.
Strict zero em dash policy enforced.
"""

import pytest
import math
from scripts.topological_manifold_unfolder import (
    PolytopeVertex,
    PolytopeCell,
    TopologicalManifoldNet,
    TopologicalManifoldUnfolder,
)


def test_polytope_vertex_and_cell_creation():
    v = PolytopeVertex("v-1", (1.0, -1.0, 1.0, -1.0), "Corner Alpha")
    d_v = v.to_dict()
    assert d_v["vertex_id"] == "v-1"
    assert d_v["coords_4d"] == [1.0, -1.0, 1.0, -1.0]

    c = PolytopeCell(
        cell_id="c-1",
        label="Test Cube",
        cell_type="CUBE",
        center_4d=(0.0, 0.0, 0.0, 0.0),
        unfolded_position_3d=(0.0, 100.0, 0.0),
        hinge_parent_id=None,
        hinge_rotation_deg=0.0,
        color_hex="#38bdf8",
        volume=1.0,
    )
    d_c = c.to_dict()
    assert d_c["cell_id"] == "c-1"
    assert d_c["cell_type"] == "CUBE"
    assert d_c["unfolded_position_3d"] == [0.0, 100.0, 0.0]


def test_unfold_tesseract_invariants():
    unfolder = TopologicalManifoldUnfolder()
    net = unfolder.unfold_polytope("TESSERACT_8_CELL", unfolding_factor=1.0)
    assert net.polytope_type == "TESSERACT_8_CELL"
    assert net.total_cells == 8
    assert net.total_faces == 24
    assert net.total_edges == 32
    assert net.total_vertices == 16
    assert net.euler_poincare_characteristic == 0
    assert len(net.cells) == 8
    assert net.status_level == "MANIFOLD_ISOMETRIC"
    assert net.stability_score >= 80.0


def test_unfold_hypersimplex_invariants():
    unfolder = TopologicalManifoldUnfolder()
    net = unfolder.unfold_polytope("HYPERSIMPLEX_5_CELL", unfolding_factor=1.0)
    assert net.polytope_type == "HYPERSIMPLEX_5_CELL"
    assert net.total_cells == 5
    assert net.total_faces == 10
    assert net.total_edges == 10
    assert net.total_vertices == 5
    assert net.euler_poincare_characteristic == 0
    assert len(net.cells) == 5


def test_unfold_orthoplex_invariants():
    unfolder = TopologicalManifoldUnfolder()
    net = unfolder.unfold_polytope("ORTHOPLEX_16_CELL", unfolding_factor=1.0)
    assert net.polytope_type == "ORTHOPLEX_16_CELL"
    assert net.total_cells == 16
    assert net.total_faces == 32
    assert net.total_edges == 24
    assert net.total_vertices == 8
    assert net.euler_poincare_characteristic == 0
    assert len(net.cells) == 16


def test_unfolding_factor_progression():
    unfolder = TopologicalManifoldUnfolder(cell_spacing_px=100.0)
    net_folded = unfolder.unfold_polytope("TESSERACT_8_CELL", unfolding_factor=0.1)
    assert net_folded.unfolding_progress == 0.1
    assert net_folded.status_level == "SINGULAR_COLLAPSE"
    assert len(net_folded.warnings) > 0

    net_unfolded = unfolder.unfold_polytope("TESSERACT_8_CELL", unfolding_factor=1.0)
    assert net_unfolded.unfolding_progress == 1.0
    assert net_unfolded.status_level == "MANIFOLD_ISOMETRIC"
    assert net_unfolded.metric_distortion_index < net_folded.metric_distortion_index
    assert net_unfolded.stability_score > net_folded.stability_score


def test_demo_telemetry_generation():
    net = TopologicalManifoldUnfolder.create_demo_telemetry()
    assert net.polytope_type == "TESSERACT_8_CELL"
    assert net.total_cells == 8
    d = net.to_dict()
    assert "cells" in d
    assert "metric_distortion_index" in d
    assert "stability_score" in d


def test_markdown_report_formatting():
    net = TopologicalManifoldUnfolder.create_demo_telemetry()
    unfolder = TopologicalManifoldUnfolder()
    report = unfolder.generate_markdown_report(net)
    assert "# Topological Manifold Unfolder & Polytope Net Report" in report
    assert "Manifold Topological State:" in report
    assert "| **Polytope Geometry** |" in report
    assert "| **Euler-Poincare (Chi)** |" in report
    assert "Salvador Dali Hypercube Unfolding" in report


def test_svg_rendering_integrity():
    net = TopologicalManifoldUnfolder.create_demo_telemetry()
    unfolder = TopologicalManifoldUnfolder()
    svg = unfolder.generate_svg(net)
    assert svg.startswith("<svg")
    assert svg.endswith("</svg>")
    assert "Topological Manifold Unfolder" in svg
    assert "<polygon points=" in svg
    assert "Isometric Background Matrix" in svg
    assert "Euler Characteristic Chi = 0" in svg


def test_zero_em_dashes_enforcement():
    with open("scripts/topological_manifold_unfolder.py", "r", encoding="utf-8") as f:
        script_content = f.read()
    assert chr(8212) not in script_content, "Em dash detected in scripts/topological_manifold_unfolder.py!"

    with open("tests/test_topological_manifold_unfolder.py", "r", encoding="utf-8") as f:
        test_content = f.read()
    assert chr(8212) not in test_content, "Em dash detected in tests/test_topological_manifold_unfolder.py!"
