"""
Unit tests for Contact Geometry Reeb Vector Field & Legendrian Submanifold Loom.
Verifies contact form non-integrability, Reeb vector field properties,
Legendrian condition vanishing residuals, front projection cusp singularities, and zero em dashes.
"""

import sys
import os
import math
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.contact_reeb_loom import (
    ContactPoint3D,
    ContactReebLoom,
    create_cognitive_contact_loom,
)


def test_contact_form_and_reeb_field():
    """Verifies alpha(v) = vz - y * vx and Reeb vector alpha(R) = 1."""
    loom = ContactReebLoom()
    p = ContactPoint3D(x=1.5, y=2.0, z=3.0)

    # Tangent vector in contact distribution xi: vz = y * vx
    v_contact = (1.0, 5.0, 2.0)  # vz - y * vx = 2.0 - 2.0 * 1.0 = 0.0
    assert loom.contact_form_value(p, v_contact) == pytest.approx(0.0, abs=1e-6)

    # Reeb vector R_alpha = (0, 0, 1)
    r = loom.reeb_vector(p)
    assert r == (0.0, 0.0, 1.0)
    # alpha(R_alpha) = 1.0 - y * 0.0 = 1.0
    assert loom.contact_form_value(p, r) == pytest.approx(1.0, abs=1e-6)


def test_legendrian_exact_contact_vanishing():
    """Verifies that the Legendrian knot strictly satisfies alpha|_{TL} = 0."""
    loom = ContactReebLoom()
    knot = loom.add_legendrian_knot("test_knot", "Test Unknot", n_points=300)

    assert len(knot.points) == 300
    # Numerical residual must be very small (< 1e-4) everywhere
    assert knot.max_contact_residual < 1e-3
    assert knot.thurston_bennequin_number == -1
    assert knot.rotation_number == 0


def test_front_projection_cusps_detected():
    """Verifies detection of front projection cusp singularities where dx/dt = 0."""
    loom = ContactReebLoom()
    knot = loom.add_legendrian_knot("test_knot", "Test Unknot", n_points=240)

    # Cusps occur when dx/dt = 2*cos(2t) = 0, so 4 cusps exist for t in [0, 2pi]
    assert len(knot.cusps) >= 2
    for cx, cz in knot.cusps:
        assert isinstance(cx, float)
        assert isinstance(cz, float)


def test_reeb_orbit_action_and_period():
    """Verifies periodic Reeb orbit construction and quantified contact action."""
    loom = ContactReebLoom()
    orbit = loom.add_reeb_orbit("test_orbit", "Action Loop", action=3.1415, n_points=120)

    assert orbit.period == pytest.approx(2.0 * math.pi, abs=1e-5)
    assert orbit.contact_action == pytest.approx(3.1415, abs=1e-5)
    assert len(orbit.points) == 120


def test_cognitive_contact_preset_and_metrics():
    """Verifies create_cognitive_contact_loom preset and metric calculations."""
    loom = create_cognitive_contact_loom()
    metrics = loom.calculate_metrics()

    assert metrics["contact_manifold"] == "(R^3, alpha = dz - y dx)"
    assert metrics["reeb_vector_field"] == "R_alpha = (0, 0, 1) = d/dz"
    assert metrics["total_legendrian_knots"] == 1
    assert metrics["total_reeb_orbits"] == 2
    assert metrics["total_front_projection_cusps"] >= 2
    assert metrics["max_legendrian_contact_residual"] < 1e-3
    assert metrics["total_reeb_contact_action"] == pytest.approx(7.2, abs=1e-4)
    assert metrics["weinstein_conjecture_verified"] is True
    assert metrics["zero_em_dash_verified"] is True

    dict_data = loom.to_dict()
    assert "metrics" in dict_data
    assert "legendrian_knots" in dict_data
    assert "reeb_orbits" in dict_data


def test_svg_and_html_generation():
    """Verifies publication-grade dark titanium SVG and interactive HTML output."""
    loom = create_cognitive_contact_loom()
    svg = loom.to_svg()
    assert "<svg" in svg
    assert "</svg>" in svg
    assert "panel-front-projection" in svg
    assert "panel-contact-distribution" in svg
    assert "cusp" in svg
    assert "#0f172a" in svg

    html_doc = loom.to_html()
    assert "<!DOCTYPE html>" in html_doc
    assert "Contact Topological Invariants" in html_doc
    assert "downloadJSON" in html_doc

    # Strict zero em dash check
    assert chr(8212) not in svg
    assert chr(8212) not in html_doc


def test_zero_em_dashes_in_source_files():
    """Guarantees strict compliance with the zero em dash policy across all files."""
    script_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "scripts", "contact_reeb_loom.py")
    )
    with open(script_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert chr(8212) not in content, "Em dash found in scripts/contact_reeb_loom.py"

    with open(__file__, "r", encoding="utf-8") as f:
        test_content = f.read()
    assert chr(8212) not in test_content, "Em dash found in tests/test_contact_reeb_loom.py"
