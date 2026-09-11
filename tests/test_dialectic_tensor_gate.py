"""
Unit tests for Dialectic Tensor & Semantic Orthogonality Gate.
Verifies cosine similarity calculations, orthogonality scoring, thesis-antithesis
tension detection, synthesis resultant vector generation, dark titanium SVG
rendering, and markdown telemetry. Strictly zero em dashes enforced.
"""

import pytest
from scripts.dialectic_tensor_gate import (
    DialecticVector,
    TensorPairTension,
    SynthesisResultant,
    DialecticTensorTelemetry,
    DialecticTensorGate,
    sample_dialectic_vectors,
)


def test_dialectic_vector_initialization():
    v = DialecticVector(
        vector_id="v-core",
        title="Pure Immutability",
        components=[1.0, 0.5, -0.5],
        domain="core_architecture",
        magnitude=1.5,
    )
    assert v.vector_id == "v-core"
    assert v.title == "Pure Immutability"
    assert len(v.components) == 3
    assert v.domain == "core_architecture"
    assert v.magnitude == 1.5


def test_cosine_similarity_edge_cases():
    gate = DialecticTensorGate()
    # Parallel
    assert abs(gate.calculate_cosine_similarity([1.0, 0.0], [2.0, 0.0]) - 1.0) < 1e-6
    # Anti-parallel
    assert abs(gate.calculate_cosine_similarity([1.0, 0.0], [-1.0, 0.0]) - (-1.0)) < 1e-6
    # Orthogonal
    assert abs(gate.calculate_cosine_similarity([1.0, 0.0], [0.0, 1.0]) - 0.0) < 1e-6
    # Empty / zero vector
    assert gate.calculate_cosine_similarity([], []) == 0.0
    assert gate.calculate_cosine_similarity([0.0, 0.0], [1.0, 1.0]) == 0.0


def test_evaluate_manifold_empty():
    gate = DialecticTensorGate()
    telemetry = gate.evaluate_manifold([])
    assert telemetry.total_vectors == 0
    assert telemetry.evaluated_pairs_count == 0
    assert telemetry.mean_orthogonality == 1.0
    assert telemetry.peak_tension_pair is None
    assert len(telemetry.synthesis_candidates) == 0
    assert len(telemetry.pair_tensions) == 0


def test_evaluate_manifold_polar_opposition():
    gate = DialecticTensorGate()
    v_thesis = DialecticVector("t1", "Thesis", [1.0, 0.0, 0.0], "theory")
    v_antithesis = DialecticVector("t2", "Antithesis", [-0.95, 0.05, 0.0], "theory")

    telemetry = gate.evaluate_manifold([v_thesis, v_antithesis])
    assert telemetry.evaluated_pairs_count == 1
    pair = telemetry.pair_tensions[0]
    assert pair.synthesis_opportunity == "polarized"
    assert pair.tension_energy > 0.8
    assert len(telemetry.synthesis_candidates) == 1


def test_evaluate_manifold_orthogonality():
    gate = DialecticTensorGate()
    v1 = DialecticVector("v1", "Data Tier", [1.0, 0.0, 0.0], "backend")
    v2 = DialecticVector("v2", "UI Tier", [0.0, 1.0, 0.0], "frontend")

    telemetry = gate.evaluate_manifold([v1, v2])
    pair = telemetry.pair_tensions[0]
    assert pair.orthogonality_score > 0.95
    assert pair.synthesis_opportunity == "orthogonal"


def test_synthesis_resultant_generation():
    gate = DialecticTensorGate()
    vectors = sample_dialectic_vectors()
    telemetry = gate.evaluate_manifold(vectors)

    assert len(telemetry.synthesis_candidates) > 0
    for sc in telemetry.synthesis_candidates:
        assert sc.synthesis_power > 0.0
        assert 0.0 <= sc.resolution_angle_deg <= 180.0
        assert len(sc.components) > 0


def test_generate_svg():
    gate = DialecticTensorGate()
    vectors = sample_dialectic_vectors()
    telemetry = gate.evaluate_manifold(vectors)

    svg_code = gate.generate_svg(telemetry)
    assert "<svg" in svg_code
    assert "</svg>" in svg_code
    assert "tensorGlow" in svg_code
    assert "DIALECTIC TENSOR HUD" in svg_code
    assert chr(8212) not in svg_code


def test_generate_markdown_report():
    gate = DialecticTensorGate()
    vectors = sample_dialectic_vectors()
    telemetry = gate.evaluate_manifold(vectors)

    md_report = gate.generate_markdown_report(telemetry)
    assert "# Dialectic Tensor and Semantic Orthogonality Telemetry" in md_report
    assert "## 1. Manifold Orthogonality Overview" in md_report
    assert "## 3. Pair Tension and Orthogonality Catalog" in md_report
    assert chr(8212) not in md_report
