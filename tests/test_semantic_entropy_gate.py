"""
Unit tests for Semantic Entropy Gate & Topological Density Equalizer.
Strict rule: Zero em dashes across all code, docstrings, and tests.
"""

import pytest
import math
from scripts.semantic_entropy_gate import (
    SemanticNode,
    LocalEntropyMeasurement,
    RedistributedNode,
    DensityEqualizerTelemetry,
    SemanticEntropyEqualizer,
    sample_canvas_nodes,
)


def test_semantic_node_mass():
    """Verifies weighted semantic mass calculation."""
    node = SemanticNode("n1", "Test Node", 100.0, 100.0, token_count=20, concept_count=4, edge_count=2)
    # mass = 20 * 0.2 + 4 * 1.5 + 2 * 0.8 = 4.0 + 6.0 + 1.6 = 11.6
    assert math.isclose(node.semantic_mass, 11.6, abs_tol=0.01)


def test_distance_calculation():
    """Verifies Euclidean distance calculations."""
    equalizer = SemanticEntropyEqualizer(radius=100.0)
    n1 = SemanticNode("a", "A", 0.0, 0.0)
    n2 = SemanticNode("b", "B", 30.0, 40.0)
    dist = equalizer.calculate_distance(n1, n2)
    assert math.isclose(dist, 50.0, abs_tol=0.01)

    coord_dist = equalizer.calculate_coord_distance(10.0, 20.0, 40.0, 60.0)
    assert math.isclose(coord_dist, 50.0, abs_tol=0.01)


def test_measure_local_entropy_empty():
    """Verifies graceful handling of empty node lists."""
    equalizer = SemanticEntropyEqualizer(radius=100.0)
    measurements = equalizer.measure_local_entropy([])
    assert measurements == []

    telemetry = equalizer.equalize_density([])
    assert telemetry.total_nodes == 0
    assert telemetry.global_entropy == 0.0


def test_measure_local_entropy_clustering():
    """Verifies entropy and crowding classification on crowded vs isolated nodes."""
    nodes = sample_canvas_nodes()
    equalizer = SemanticEntropyEqualizer(radius=100.0)
    measurements = equalizer.measure_local_entropy(nodes)

    assert len(measurements) == len(nodes)
    m_map = {m.node_id: m for m in measurements}

    # Core nodes are tightly clustered within radius 100
    assert m_map["core-1"].neighbor_count >= 4
    assert m_map["core-1"].crowding_level in ("moderate", "critical")

    # Satellites are isolated
    assert m_map["sat-1"].neighbor_count == 1
    assert m_map["sat-1"].crowding_level == "optimal"


def test_equalize_density_variance_reduction():
    """Verifies that density equalization disperses clusters and reduces density variance."""
    nodes = sample_canvas_nodes()
    equalizer = SemanticEntropyEqualizer(radius=120.0)
    telemetry = equalizer.equalize_density(nodes, iterations=40, repulsion_scale=600.0)

    assert telemetry.total_nodes == len(nodes)
    assert telemetry.variance_reduction_percent >= 0.0
    assert telemetry.mean_displacement > 0.0
    assert len(telemetry.redistributed_nodes) == len(nodes)

    # Verify displaced positions
    disp_map = {r.node_id: r for r in telemetry.redistributed_nodes}
    assert disp_map["core-1"].displacement > 0.5


def test_cluster_cohesion_retention():
    """Verifies that cluster cohesion maintains relative grouping."""
    nodes = sample_canvas_nodes()
    equalizer = SemanticEntropyEqualizer(radius=120.0)
    telemetry = equalizer.equalize_density(nodes, iterations=25, cluster_cohesion=0.08)

    disp_map = {r.node_id: r for r in telemetry.redistributed_nodes}
    # Nodes in cluster 'auth' should still be positioned on the left side (x < 400)
    for nid in ["core-1", "core-2", "core-3", "core-4", "core-5"]:
        assert disp_map[nid].adjusted_x < 400.0


def test_generate_svg_structure():
    """Verifies valid SVG markup generation with dark titanium styling."""
    nodes = sample_canvas_nodes()
    equalizer = SemanticEntropyEqualizer(radius=120.0)
    telemetry = equalizer.equalize_density(nodes, iterations=10)
    svg = equalizer.generate_svg(telemetry, width=800, height=500)

    assert "<svg" in svg
    assert "</svg>" in svg
    assert "#09090b" in svg  # dark titanium background
    assert "Topological Density Equalizer" in svg
    assert "Authentication Gateway" in svg


def test_generate_markdown_report():
    """Verifies publication-ready markdown compliance audit."""
    nodes = sample_canvas_nodes()
    equalizer = SemanticEntropyEqualizer(radius=120.0)
    telemetry = equalizer.equalize_density(nodes, iterations=10)
    report = equalizer.generate_markdown_report(telemetry)

    assert "# Topological Density Equalizer and Semantic Entropy Audit" in report
    assert "Shannon-Wiener Information Entropy" in report
    assert "Cowan Capacity Bounds" in report
    assert "| `core-1` |" in report
    assert chr(8212) not in report
