"""
Unit tests for Hyper-Dimensional Grassmannian Manifold Projector & Subspace Angle Loom.
Verifies Gram-Schmidt orthonormalization, canonical principal angle bounds,
Riemannian geodesic and chordal metrics, geodesic interpolation, and zero em dashes.
"""

import sys
import os
import math
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.grassmannian_subspace_loom import (
    gram_schmidt_orthonormalize,
    compute_principal_angles,
    GrassmannianManifoldLoom,
    create_cognitive_subspace_loom,
)


def test_gram_schmidt_orthonormalization():
    """Verifies that Gram-Schmidt yields unit-length and mutually orthogonal vectors."""
    raw = [
        [1.0, 2.0, 0.0, 1.0],
        [0.0, 1.0, 1.0, 0.0],
        [1.0, 0.0, 1.0, 1.0],
    ]
    basis = gram_schmidt_orthonormalize(raw)
    assert len(basis) == 3

    # Check unit norms
    for v in basis:
        norm = math.sqrt(sum(x * x for x in v))
        assert norm == pytest.approx(1.0, abs=1e-6)

    # Check mutual orthogonality
    for i in range(len(basis)):
        for j in range(i + 1, len(basis)):
            dot = sum(basis[i][d] * basis[j][d] for d in range(len(basis[0])))
            assert dot == pytest.approx(0.0, abs=1e-6)


def test_principal_angles_bounds_and_extremes():
    """Verifies principal angles for identical and mutually orthogonal subspaces."""
    # Identical subspaces: angles must be 0, singular values 1.0
    sub_ident = [
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0],
    ]
    angles_id, sigmas_id = compute_principal_angles(sub_ident, sub_ident)
    for a in angles_id:
        assert a == pytest.approx(0.0, abs=1e-5)
    for s in sigmas_id:
        assert s == pytest.approx(1.0, abs=1e-5)

    # Mutually orthogonal subspaces: angles must be pi/2, singular values 0.0
    sub_ortho = [
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0],
    ]
    angles_ortho, sigmas_ortho = compute_principal_angles(sub_ident, sub_ortho)
    for a in angles_ortho:
        assert a == pytest.approx(math.pi / 2.0, abs=1e-5)
    for s in sigmas_ortho:
        assert s == pytest.approx(0.0, abs=1e-5)


def test_grassmannian_metrics_axioms():
    """Verifies Riemannian geodesic, chordal, Asimov, and Binet-Cauchy metric properties."""
    loom = GrassmannianManifoldLoom(ambient_dim=4, subspace_dim=2)
    loom.add_subspace("A", "Subspace A", [[1, 0, 0, 0], [0, 1, 0, 0]])
    loom.add_subspace("B", "Subspace B", [[0.7071, 0.7071, 0, 0], [0, 0, 1, 0]])

    comp_ab = loom.compare_pair("A", "B")
    comp_ba = loom.compare_pair("B", "A")

    assert comp_ab is not None
    assert comp_ba is not None

    # Symmetry
    assert comp_ab.geodesic_distance == pytest.approx(comp_ba.geodesic_distance, rel=1e-5)
    assert comp_ab.chordal_distance == pytest.approx(comp_ba.chordal_distance, rel=1e-5)

    # Chordal distance is strictly <= Geodesic distance (since sin(x) <= x for x >= 0)
    assert comp_ab.chordal_distance <= comp_ab.geodesic_distance + 1e-6

    # Asimov distance <= Geodesic distance
    assert comp_ab.asimov_distance <= comp_ab.geodesic_distance + 1e-6

    # Binet-Cauchy is in [0, 1]
    assert 0.0 <= comp_ab.binet_cauchy_metric <= 1.0


def test_geodesic_interpolation_orthonormality():
    """Verifies that intermediate points along geodesic path are orthonormal."""
    loom = GrassmannianManifoldLoom(ambient_dim=6, subspace_dim=2)
    loom.add_subspace("S1", "Subspace 1", [[1, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0]])
    loom.add_subspace("S2", "Subspace 2", [[0, 0, 1, 0, 0, 0], [0, 0, 0, 1, 0, 0]])

    for t in [0.0, 0.25, 0.5, 0.75, 1.0]:
        interp_basis = loom.geodesic_interpolate("S1", "S2", t=t)
        assert len(interp_basis) == 2

        # Check unit norm
        for v in interp_basis:
            norm = math.sqrt(sum(x * x for x in v))
            assert norm == pytest.approx(1.0, abs=1e-5)

        # Check orthogonality
        dot = sum(interp_basis[0][d] * interp_basis[1][d] for d in range(len(interp_basis[0])))
        assert dot == pytest.approx(0.0, abs=1e-5)


def test_cognitive_subspace_preset_and_metrics():
    """Verifies create_cognitive_subspace_loom preset and comprehensive metrics summary."""
    loom = create_cognitive_subspace_loom()
    metrics = loom.calculate_metrics()

    assert metrics["ambient_dimension"] == 8
    assert metrics["subspace_dimension"] == 2
    assert metrics["grassmannian_manifold"] == "Gr(2, 8)"
    assert metrics["total_subspaces"] == 4
    assert metrics["total_pairwise_comparisons"] == 6

    assert metrics["mean_geodesic_distance"] > 0.0
    assert metrics["mean_chordal_distance"] > 0.0
    assert 0.0 <= metrics["mean_subspace_affinity"] <= 1.0
    assert metrics["riemannian_metric_verified"] is True
    assert metrics["zero_em_dash_verified"] is True


def test_svg_and_html_generation():
    """Verifies publication-grade SVG and HTML output without rendering anomalies."""
    loom = create_cognitive_subspace_loom()
    svg = loom.to_svg()
    assert "<svg" in svg
    assert "</svg>" in svg
    assert "panel-angle-radar" in svg
    assert "panel-subspace-projection" in svg
    assert "Gr(2, 8)" in svg
    assert "#0f172a" in svg

    html_doc = loom.to_html()
    assert "<!DOCTYPE html>" in html_doc
    assert "Grassmannian Invariant Telemetry" in html_doc
    assert "downloadJSON" in html_doc

    # Strict zero em dash check
    assert chr(8212) not in svg
    assert chr(8212) not in html_doc


def test_zero_em_dashes_in_source_files():
    """Guarantees strict compliance with the zero em dash policy across all files."""
    script_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "scripts", "grassmannian_subspace_loom.py")
    )
    with open(script_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert chr(8212) not in content, "Em dash found in scripts/grassmannian_subspace_loom.py"

    with open(__file__, "r", encoding="utf-8") as f:
        test_content = f.read()
    assert chr(8212) not in test_content, "Em dash found in tests/test_grassmannian_subspace_loom.py"
