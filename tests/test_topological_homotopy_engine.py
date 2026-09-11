"""
test_topological_homotopy_engine.py - Unit tests for TopologicalHomotopyEngine (Phase 110, Cycle 106).

Tests continuous algebraic topological invariant evaluation (Betti numbers, Euler characteristic),
Hermite smoothstep homotopic path deformation, SVG export, and zero em dashes.

Strict constraint: Strictly zero em dashes (Unicode U+2014) anywhere.
"""

from pathlib import Path
import pytest
from scripts.topological_homotopy_engine import (
    HomotopyResult,
    HomotopyStep,
    HomotopyTelemetry,
    TopologicalEdge,
    TopologicalHomotopyEngine,
    TopologicalInvariants,
    TopologicalNode,
)


@pytest.fixture
def triangle_cyclic_topology():
    nodes = [
        {"id": "n1", "label": "Perceptual Anchor", "start_x": 100.0, "start_y": 100.0, "end_x": 600.0, "end_y": 100.0},
        {"id": "n2", "label": "Epistemic Node", "start_x": 200.0, "start_y": 250.0, "end_x": 700.0, "end_y": 250.0},
        {"id": "n3", "label": "Action Horizon", "start_x": 100.0, "start_y": 250.0, "end_x": 600.0, "end_y": 250.0},
    ]
    edges = [
        {"source": "n1", "target": "n2"},
        {"source": "n2", "target": "n3"},
        {"source": "n3", "target": "n1"},
    ]
    return nodes, edges


def test_empty_engine():
    engine = TopologicalHomotopyEngine()
    res = engine.evaluate_and_deform(nodes=[])

    assert isinstance(res, HomotopyResult)
    assert res.telemetry.nodes_count == 0
    assert res.telemetry.edges_count == 0
    assert res.telemetry.betti_0 == 0
    assert res.telemetry.betti_1 == 0
    assert res.telemetry.cowan_bounded is True
    assert len(res.homotopy_steps) == 0
    assert res.svg_homotopy_diagram == ""
    assert res.invariant_audit_md == ""


def test_topological_invariants_triangle_cycle(triangle_cyclic_topology):
    nodes, edges = triangle_cyclic_topology
    engine = TopologicalHomotopyEngine(steps_count=5)
    res = engine.evaluate_and_deform(nodes=nodes, edges=edges)

    assert res.telemetry.nodes_count == 3
    assert res.telemetry.edges_count == 3
    assert res.telemetry.betti_0 == 1  # Single connected component
    assert res.telemetry.betti_1 == 1  # Single cyclic 1D hole/loop (3 - 3 + 1 = 1)
    assert res.telemetry.euler_characteristic == 0  # V - E = 3 - 3 = 0
    assert res.telemetry.structural_preservation_score == 1.0
    assert res.telemetry.cowan_bounded is True

    # Validate homotopy steps
    assert len(res.homotopy_steps) == 5
    assert res.homotopy_steps[0].t_value == 0.0
    assert res.homotopy_steps[-1].t_value == 1.0

    # Start position check
    assert res.homotopy_steps[0].interpolated_positions["n1"] == (100.0, 100.0)
    # End position check
    assert res.homotopy_steps[-1].interpolated_positions["n1"] == (600.0, 100.0)


def test_two_component_disconnected_topology():
    nodes = [
        {"id": "a1", "label": "Cluster A1", "start_x": 50.0, "start_y": 50.0, "end_x": 500.0, "end_y": 50.0},
        {"id": "a2", "label": "Cluster A2", "start_x": 100.0, "start_y": 50.0, "end_x": 550.0, "end_y": 50.0},
        {"id": "b1", "label": "Cluster B1", "start_x": 50.0, "start_y": 200.0, "end_x": 500.0, "end_y": 200.0},
        {"id": "b2", "label": "Cluster B2", "start_x": 100.0, "start_y": 200.0, "end_x": 550.0, "end_y": 200.0},
    ]
    edges = [
        {"source": "a1", "target": "a2"},
        {"source": "b1", "target": "b2"},
    ]
    engine = TopologicalHomotopyEngine()
    res = engine.evaluate_and_deform(nodes=nodes, edges=edges)

    assert res.telemetry.betti_0 == 2  # Two disjoint components
    assert res.telemetry.betti_1 == 0  # No cycles
    assert res.telemetry.euler_characteristic == 2  # 4 - 2 = 2


def test_cowan_bounding_exceeded():
    engine = TopologicalHomotopyEngine(max_cowan_nodes=4)
    nodes = [{"id": f"node_{i}", "label": f"Node {i}"} for i in range(7)]
    res = engine.evaluate_and_deform(nodes=nodes)

    assert res.telemetry.nodes_count == 7
    assert res.telemetry.cowan_bounded is False


def test_svg_export(tmp_path: Path, triangle_cyclic_topology):
    nodes, edges = triangle_cyclic_topology
    engine = TopologicalHomotopyEngine()
    res = engine.evaluate_and_deform(nodes=nodes, edges=edges)

    svg_file = tmp_path / "homotopy.svg"
    svg_str = engine.export_svg(res, output_path=str(svg_file))

    assert "<svg" in svg_str
    assert "</svg>" in svg_str
    assert "Topological Invariant &amp; Homotopy Visualizer" in svg_str
    assert svg_file.exists()
    assert svg_file.stat().st_size > 500


def test_ascii_report(triangle_cyclic_topology):
    nodes, edges = triangle_cyclic_topology
    engine = TopologicalHomotopyEngine()
    res = engine.evaluate_and_deform(nodes=nodes, edges=edges)
    report = engine.generate_ascii_report(res)

    assert "TOPOLOGICAL INVARIANT & HOMOTOPY VISUALIZER" in report
    assert "Entities Evaluated" in report
    assert "Betti 0" in report
    assert "[KEYFRAME]" in report


def test_invariant_audit_markdown(triangle_cyclic_topology):
    nodes, edges = triangle_cyclic_topology
    engine = TopologicalHomotopyEngine()
    res = engine.evaluate_and_deform(nodes=nodes, edges=edges)

    md = res.invariant_audit_md
    assert "# Topological Invariant & Homotopy Audit Report" in md
    assert "Connected Components (Betti 0):** 1" in md
    assert "Cyclic Holes (Betti 1):** 1" in md
    assert "| Keyframe (t) |" in md


def test_zero_em_dashes():
    source_files = [
        Path("scripts/topological_homotopy_engine.py"),
        Path("tests/test_topological_homotopy_engine.py"),
    ]
    for p in source_files:
        if p.exists():
            text = p.read_text(encoding="utf-8")
            assert "\u2014" not in text, f"Em dash found in {p}"
