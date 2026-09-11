"""
Unit tests for Calabi-Yau Compactification & Multi-Dimensional Flux Vacuum Loom.
Verifies Hodge diamond symmetries, Euler characteristic calculations,
quintic threefold cross-section sheet generation, flux vacua stabilization, and zero em dashes.
"""

import sys
import os
import math
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.calabi_yau_compactification import (
    HodgeDiamond,
    FluxVacuum,
    CalabiYauLoom,
    create_cognitive_calabi_yau_loom,
)


def test_hodge_diamond_symmetries_and_euler_characteristic():
    """Verifies Calabi-Yau 3-fold Hodge numbers and topological Euler characteristic."""
    hd = HodgeDiamond()
    assert hd.h00 == 1
    assert hd.h30 == 1
    assert hd.h11 == 1    # 1 Kaehler modulus
    assert hd.h21 == 101  # 101 complex structure moduli

    # Topological Euler characteristic: chi = 2 * (h11 - h21) = 2 * (1 - 101) = -200
    assert hd.euler_characteristic == -200
    assert (hd.h11 + hd.h21) == 102

    dict_data = hd.to_dict()
    assert dict_data["euler_characteristic"] == -200
    assert dict_data["total_moduli_degrees_of_freedom"] == 102


def test_quintic_cross_section_sheets():
    """Verifies 5-sheeted cross-section curves with closed loop topology."""
    loom = CalabiYauLoom(psi_deformation=0.4)
    sheets = loom.cross_section_sheets

    # Must produce 5 sheets corresponding to 5th roots of unity
    assert len(sheets) == 5

    for sheet in sheets:
        assert len(sheet) == 121
        # First and last point must coincide to form a closed loop
        p_first = sheet[0]
        p_last = sheet[-1]
        assert p_first[0] == pytest.approx(p_last[0], abs=1e-4)
        assert p_first[1] == pytest.approx(p_last[1], abs=1e-4)


def test_flux_vacua_registration():
    """Verifies stabilized flux vacua registration and moduli coordinates."""
    loom = CalabiYauLoom()
    vac = loom.add_flux_vacuum(
        "test_vac",
        "Test Vacuum",
        psi_real=0.5,
        psi_imag=-0.3,
        flux_f3=[1, 2, 3, 4],
        flux_h3=[0, 1, 0, -1],
        vacuum_energy=0.02
    )

    assert vac.vacuum_id == "test_vac"
    assert vac.moduli_psi_real == 0.5
    assert vac.moduli_psi_imag == -0.3
    assert vac.vacuum_energy == pytest.approx(0.02, abs=1e-5)
    assert len(loom.flux_vacua) == 1


def test_calabi_yau_metrics_summary():
    """Verifies comprehensive metric dictionary and Calabi-Yau invariants."""
    loom = create_cognitive_calabi_yau_loom()
    metrics = loom.calculate_metrics()

    assert metrics["compactified_real_dimensions"] == 6
    assert metrics["complex_dimensions"] == 3
    assert metrics["first_chern_class"] == "c1(X) = 0"
    assert metrics["ricci_flat_condition"] == "R_ij = 0 (Kaehler-Einstein)"
    assert metrics["euler_characteristic"] == -200
    assert metrics["kaehler_moduli_h11"] == 1
    assert metrics["complex_structure_moduli_h21"] == 101
    assert metrics["cross_section_sheets"] == 5
    assert metrics["stabilized_flux_vacua"] == 3
    assert metrics["yau_metric_verified"] is True
    assert metrics["zero_em_dash_verified"] is True

    dict_data = loom.to_dict()
    assert "metrics" in dict_data
    assert "hodge_diamond" in dict_data
    assert len(dict_data["flux_vacua"]) == 3


def test_svg_and_html_generation():
    """Verifies publication-grade dark titanium SVG and interactive HTML output."""
    loom = create_cognitive_calabi_yau_loom()
    svg = loom.to_svg()
    assert "<svg" in svg
    assert "</svg>" in svg
    assert "panel-quintic-slice" in svg
    assert "panel-hodge-moduli" in svg
    assert "chi = 2*(1 - 101) = -200" in svg
    assert "#0f172a" in svg

    html_doc = loom.to_html()
    assert "<!DOCTYPE html>" in html_doc
    assert "Calabi-Yau Topological Invariants" in html_doc
    assert "downloadJSON" in html_doc

    # Strict zero em dash check
    assert chr(8212) not in svg
    assert chr(8212) not in html_doc


def test_zero_em_dashes_in_source_files():
    """Guarantees strict compliance with the zero em dash policy across all files."""
    script_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "scripts", "calabi_yau_compactification.py")
    )
    with open(script_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert chr(8212) not in content, "Em dash found in scripts/calabi_yau_compactification.py"

    with open(__file__, "r", encoding="utf-8") as f:
        test_content = f.read()
    assert chr(8212) not in test_content, "Em dash found in tests/test_calabi_yau_compactification.py"
