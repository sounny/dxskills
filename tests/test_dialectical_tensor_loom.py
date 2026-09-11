"""
Unit tests for Dialectical Tensor Lattice & Hegelian Synthesis Loom Engine.
Verifies multi-pole semantic tensor opposition evaluation, Aufhebung resolution mechanics,
harmonic convergence metrics, SVG rendering, and diagnostic reporting.
Strictly zero em dash compliance.
"""

import pytest
import math
from scripts.dialectical_tensor_loom import (
    DialecticalPole,
    DialecticalTensionEdge,
    AufhebungResolution,
    DialecticalLatticeTelemetry,
    DialecticalTensorLoom,
)


def test_dialectical_pole_and_edge_creation():
    p = DialecticalPole(
        pole_id="p-1",
        title="Centralization",
        dimension_vector=[1.0, 0.0, -1.0],
        core_axiom="Axiom of central control",
        pole_type="THESIS",
        pos_x=100.0,
        pos_y=200.0,
    )
    assert p.pole_id == "p-1"
    d = p.to_dict()
    assert d["pole_id"] == "p-1"
    assert d["pole_type"] == "THESIS"
    assert len(d["dimension_vector"]) == 3

    edge = DialecticalTensionEdge(
        source_id="p-1",
        target_id="p-2",
        cosine_similarity=-0.9,
        antithesis_friction=0.95,
        tension_level="PARADOX",
    )
    ed = edge.to_dict()
    assert ed["tension_level"] == "PARADOX"
    assert ed["antithesis_friction"] == 0.95


def test_cosine_sim_and_vector_norm():
    loom = DialecticalTensorLoom()
    # Parallel vectors -> sim = 1.0
    v1 = [1.0, 2.0, 3.0]
    v2 = [2.0, 4.0, 6.0]
    assert math.isclose(loom.cosine_sim(v1, v2), 1.0, abs_tol=1e-5)

    # Orthogonal vectors -> sim = 0.0
    v_orth1 = [1.0, 0.0]
    v_orth2 = [0.0, 1.0]
    assert math.isclose(loom.cosine_sim(v_orth1, v_orth2), 0.0, abs_tol=1e-5)

    # Opposing vectors -> sim = -1.0
    v_opp1 = [1.0, -1.0]
    v_opp2 = [-2.0, 2.0]
    assert math.isclose(loom.cosine_sim(v_opp1, v_opp2), -1.0, abs_tol=1e-5)


def test_calculate_tension_edge():
    loom = DialecticalTensorLoom(acute_friction_threshold=0.65)
    p_thesis = DialecticalPole("t", "Thesis", [1.0, 0.0], "Axiom T", "THESIS")
    p_antithesis = DialecticalPole("a", "Antithesis", [-1.0, 0.0], "Axiom A", "ANTITHESIS")
    
    edge = loom.calculate_tension_edge(p_thesis, p_antithesis)
    assert edge.cosine_similarity == pytest.approx(-1.0, 0.01)
    assert edge.antithesis_friction == pytest.approx(1.0, 0.01)
    assert edge.tension_level == "PARADOX"


def test_evaluate_lattice_empty():
    loom = DialecticalTensorLoom()
    telemetry = loom.evaluate_lattice([])
    assert len(telemetry.poles) == 0
    assert len(telemetry.tension_edges) == 0
    assert telemetry.status_level == "SYNTHESIZED"
    assert telemetry.overall_harmony_score == 100.0


def test_evaluate_lattice_with_triad():
    loom = DialecticalTensorLoom()
    p1 = DialecticalPole("p1", "A", [1.0, 0.0], "A", "THESIS", 100.0, 100.0)
    p2 = DialecticalPole("p2", "B", [-0.8, 0.2], "B", "ANTITHESIS", 200.0, 100.0)
    p3 = DialecticalPole("p3", "C", [0.5, 0.5], "C", "SYNTHESIS", 150.0, 50.0)

    res = AufhebungResolution(
        resolution_id="r1",
        thesis_id="p1",
        antithesis_id="p2",
        synthesis_title="Integration of A and B",
        preserved_tenets=["Strength of A", "Flexibility of B"],
        negated_biases=["Rigidity of A", "Fragility of B"],
        emergent_axiom="Harmonic dynamic",
        resolution_ratio=0.85,
        cognitive_harmony_index=88.0,
    )

    telemetry = loom.evaluate_lattice([p1, p2, p3], [res])
    assert len(telemetry.poles) == 3
    assert len(telemetry.tension_edges) == 3
    assert len(telemetry.resolutions) == 1
    assert telemetry.resolution_coverage == 1.0


def test_auto_weave_resolutions():
    loom = DialecticalTensorLoom(acute_friction_threshold=0.60)
    p1 = DialecticalPole("p1", "Local Optimization", [1.0, -1.0], "Local", "THESIS")
    p2 = DialecticalPole("p2", "Global Coordination", [-1.0, 1.0], "Global", "ANTITHESIS")
    
    # Do not provide custom resolutions, engine should auto-weave Aufhebung
    telemetry = loom.evaluate_lattice([p1, p2])
    assert len(telemetry.resolutions) == 1
    assert telemetry.resolutions[0].thesis_id == "p1"
    assert telemetry.resolutions[0].antithesis_id == "p2"
    assert telemetry.resolutions[0].resolution_ratio > 0.0


def test_demo_telemetry_generation():
    demo = DialecticalTensorLoom.create_demo_telemetry()
    assert len(demo.poles) == 3
    assert len(demo.tension_edges) == 3
    assert len(demo.resolutions) == 1
    assert demo.status_level in ["HARMONIZED", "SYNTHESIZED"]
    assert demo.overall_harmony_score > 80.0

    d = demo.to_dict()
    assert "mean_lattice_friction" in d
    assert "overall_harmony_score" in d


def test_markdown_report_formatting():
    loom = DialecticalTensorLoom()
    demo = loom.create_demo_telemetry()
    report = loom.generate_markdown_report(demo)

    assert "# Dialectical Tensor Lattice" in report
    assert "Monolithic Cohesion" in report
    assert "Microservice Isolation" in report
    assert "Modular Microkernel" in report
    assert "| Telemetry Dimension |" in report
    assert chr(8212) not in report, "Em dash found in markdown report!"


def test_svg_rendering_integrity():
    loom = DialecticalTensorLoom()
    demo = loom.create_demo_telemetry()
    svg = loom.generate_svg(demo, width=880, height=580)

    assert '<svg xmlns="http://www.w3.org/2000/svg"' in svg
    assert 'viewBox="0 0 880 580"' in svg
    assert 'HEGELIAN DIALECTICAL TENSOR LOOM' in svg
    assert 'Dialectical Tensor Telemetry' in svg
    assert 'Dialectical Loom Legend' in svg
    assert chr(8212) not in svg, "Em dash found in SVG output!"


def test_zero_em_dashes_enforcement():
    with open("scripts/dialectical_tensor_loom.py", "r", encoding="utf-8") as f:
        src = f.read()
    assert chr(8212) not in src, "Em dash found in dialectical_tensor_loom.py!"
