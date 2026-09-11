"""
Unit tests for Hyperbolic Poincare Disk Projector & Non-Euclidean Concept Loom.
Verifies conformal metric properties, geodesic circle calculations,
Mobius isometric translations, tree layout wedge distributions, and zero em dashes.
"""

import sys
import os
import math
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.hyperbolic_poincare_projector import (
    HyperbolicPoint,
    hyperbolic_distance,
    mobius_transform,
    compute_geodesic_arc,
    PoincareDiskProjector,
    create_cognitive_taxonomy_disk,
)


def test_hyperbolic_point_properties():
    """Verifies Euclidean radius, hyperbolic radius, and boundary clamping."""
    origin = HyperbolicPoint(0.0, 0.0)
    assert origin.euclidean_radius == pytest.approx(0.0, abs=1e-6)
    assert origin.hyperbolic_radius == pytest.approx(0.0, abs=1e-6)

    p1 = HyperbolicPoint(0.3, 0.4)
    assert p1.euclidean_radius == pytest.approx(0.5, abs=1e-6)
    # r_hyp = 2 * artanh(0.5) = ln(1.5 / 0.5) = ln(3) = 1.098612...
    expected_rhyp = math.log(3.0)
    assert p1.hyperbolic_radius == pytest.approx(expected_rhyp, rel=1e-4)

    # Point outside unit disk is clamped inside
    p_out = HyperbolicPoint(1.2, 1.6)
    assert p_out.euclidean_radius < 1.0
    assert p_out.euclidean_radius > 0.999


def test_hyperbolic_distance_metric_invariance():
    """Verifies metric axioms and Mobius isometry invariance."""
    p1 = HyperbolicPoint(0.1, 0.2)
    p2 = HyperbolicPoint(-0.3, 0.4)
    p3 = HyperbolicPoint(0.5, -0.1)

    # Axiom: d(x, x) = 0
    assert hyperbolic_distance(p1, p1) == pytest.approx(0.0, abs=1e-6)

    # Axiom: Symmetry d(x, y) = d(y, x)
    d12 = hyperbolic_distance(p1, p2)
    d21 = hyperbolic_distance(p2, p1)
    assert d12 == pytest.approx(d21, rel=1e-5)
    assert d12 > 0.0

    # Axiom: Triangle inequality d(x, z) <= d(x, y) + d(y, z)
    d13 = hyperbolic_distance(p1, p3)
    d23 = hyperbolic_distance(p2, p3)
    assert d13 <= (d12 + d23 + 1e-6)

    # Mobius Isometry Invariance: d(T_w(z1), T_w(z2)) == d(z1, z2)
    w = complex(0.2, -0.3)
    z1_sh = mobius_transform(p1.to_complex(), w)
    z2_sh = mobius_transform(p2.to_complex(), w)
    p1_sh = HyperbolicPoint(z1_sh.real, z1_sh.imag)
    p2_sh = HyperbolicPoint(z2_sh.real, z2_sh.imag)

    d_shifted = hyperbolic_distance(p1_sh, p2_sh)
    assert d_shifted == pytest.approx(d12, rel=1e-4)


def test_geodesic_arc_computation():
    """Tests orthogonal circle center and radius math for hyperbolic straight lines."""
    # Collinear points with origin
    p_origin = HyperbolicPoint(0.0, 0.0)
    p_radial = HyperbolicPoint(0.4, 0.4)
    arc_type, center, radius = compute_geodesic_arc(p_origin, p_radial)
    assert arc_type == "line"
    assert center is None
    assert radius is None

    # Non-collinear points
    p1 = HyperbolicPoint(0.2, 0.1)
    p2 = HyperbolicPoint(-0.3, 0.4)
    arc_type, center, radius = compute_geodesic_arc(p1, p2)
    assert arc_type == "arc"
    assert center is not None
    assert radius is not None

    cx, cy = center
    # Orthogonality relation to unit circle: R^2 = cx^2 + cy^2 - 1
    expected_r_sq = cx**2 + cy**2 - 1.0
    assert (radius**2) == pytest.approx(expected_r_sq, rel=1e-5)

    # Both points must lie on the circle: distance to center equals radius
    dist_p1_c = math.sqrt((p1.u - cx)**2 + (p1.v - cy)**2)
    dist_p2_c = math.sqrt((p2.u - cx)**2 + (p2.v - cy)**2)
    assert dist_p1_c == pytest.approx(radius, rel=1e-4)
    assert dist_p2_c == pytest.approx(radius, rel=1e-4)


def test_poincare_disk_projector_tree_layout():
    """Verifies hierarchical tree construction and wedge angle assignment."""
    proj = PoincareDiskProjector()
    proj.add_node("r", "Root", weight=4.0)
    proj.add_node("c1", "Child 1", parent_id="r", weight=2.0)
    proj.add_node("c2", "Child 2", parent_id="r", weight=2.0)
    proj.add_node("g1", "Grandchild 1", parent_id="c1", weight=1.0)

    proj.build_tree_layout(root_id="r", radial_step=0.6)

    # Root is at origin
    assert proj.nodes["r"].point.euclidean_radius == pytest.approx(0.0, abs=1e-6)

    # All nodes must be within open unit disk
    for nid, node in proj.nodes.items():
        assert node.point.euclidean_radius < 1.0

    # Children must have depth 1
    assert proj.nodes["c1"].depth == 1
    assert proj.nodes["c2"].depth == 1
    assert proj.nodes["g1"].depth == 2

    # Geodesics must exist for all parent-child connections
    assert len(proj.geodesics) == 3


def test_mobius_focus_re_centering():
    """Verifies that applying Mobius focus on a target node shifts it to origin."""
    proj = create_cognitive_taxonomy_disk()
    target_id = "spatial"
    orig_spatial_radius = proj.nodes[target_id].point.euclidean_radius
    assert orig_spatial_radius > 0.1

    # Shift focus to "spatial"
    focused_proj = proj.apply_mobius_focus(target_id)
    assert focused_proj.focus_node_id == target_id

    # The focused node is now at the origin
    new_point = focused_proj.nodes[target_id].point
    assert new_point.euclidean_radius == pytest.approx(0.0, abs=1e-4)

    # All nodes are still strictly inside the unit disk
    for nid, node in focused_proj.nodes.items():
        assert node.point.euclidean_radius < 1.0

    # Hyperbolic distance between two arbitrary nodes remains strictly invariant
    d_before = hyperbolic_distance(proj.nodes["memory"].point, proj.nodes["topology"].point)
    d_after = hyperbolic_distance(focused_proj.nodes["memory"].point, focused_proj.nodes["topology"].point)
    assert d_after == pytest.approx(d_before, rel=1e-4)


def test_cross_links_and_metrics():
    """Verifies cross-links across branches and non-Euclidean metrics."""
    proj = create_cognitive_taxonomy_disk()
    metrics = proj.calculate_metrics()

    assert metrics["total_nodes"] >= 15
    assert metrics["total_geodesics"] >= 16
    assert metrics["max_depth"] >= 2
    assert metrics["average_branching_factor"] > 1.0
    assert metrics["hyperbolic_diameter"] > 0.5
    assert metrics["mean_edge_length"] > 0.1
    assert metrics["constant_negative_curvature"] == -1.0
    assert metrics["hyperbolic_area_expansion"] > 1.0
    assert metrics["zero_em_dash_verified"] is True


def test_svg_and_html_generation():
    """Verifies SVG and HTML generation without rendering anomalies."""
    proj = create_cognitive_taxonomy_disk()
    svg = proj.to_svg(width=800, height=800, disk_radius=340.0)
    assert "<svg" in svg
    assert "</svg>" in svg
    assert "r_hyp=" in svg
    assert "#0f172a" in svg
    assert "Hyperbolic Poincare Disk Projector" in svg

    html_doc = proj.to_html()
    assert "<!DOCTYPE html>" in html_doc
    assert "Hyperbolic Space Metrics" in html_doc
    assert "poincare_disk_metrics.json" in html_doc

    # Strict zero em dash check
    assert chr(8212) not in svg
    assert chr(8212) not in html_doc


def test_zero_em_dashes_in_source_files():
    """Guarantees strict compliance with the zero em dash policy across all files."""
    script_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "scripts", "hyperbolic_poincare_projector.py")
    )
    with open(script_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert chr(8212) not in content, "Em dash found in scripts/hyperbolic_poincare_projector.py"

    with open(__file__, "r", encoding="utf-8") as f:
        test_content = f.read()
    assert chr(8212) not in test_content, "Em dash found in tests/test_hyperbolic_poincare_projector.py"
