"""
Tests for Tensegrity Cable-Strut Lattice & Dynamic Equilibrium Balancer
Validates 3-strut Simplex prism geometry, 6-strut icosahedral sphere,
self-stress stability, strain energy calculations, isometric projection, SVG rendering, and zero em dash compliance.
"""

import os
import sys
import math
import json
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.tensegrity_equilibrium_lattice import (
    TensegrityEquilibriumLattice,
    TensegrityNode,
    TensegrityStrut,
    TensegrityCable,
    TensegrityTelemetry,
)


def test_3strut_prism_geometry():
    lattice = TensegrityEquilibriumLattice()
    telemetry = lattice.build_3strut_prism(radius=150.0, height=200.0, prestress_level=100.0)
    assert telemetry.structure_type == "3_STRUT_PRISM"
    assert telemetry.total_nodes == 6
    assert telemetry.total_struts == 3
    assert telemetry.total_cables == 9
    assert telemetry.is_self_stressed_stable is True
    assert telemetry.mean_prestress_tension == 100.0
    assert telemetry.max_compression_force > 150.0
    assert telemetry.total_strain_energy > 0.0


def test_6strut_icosahedron_geometry():
    lattice = TensegrityEquilibriumLattice()
    telemetry = lattice.build_6strut_icosahedron(radius=180.0, prestress_level=120.0)
    assert telemetry.structure_type == "6_STRUT_ICOSAHEDRON"
    assert telemetry.total_nodes == 12
    assert telemetry.total_struts == 6
    assert telemetry.total_cables == 24
    assert telemetry.is_self_stressed_stable is True
    assert telemetry.total_strain_energy > 0.0


def test_non_touching_struts():
    lattice = TensegrityEquilibriumLattice()
    telemetry = lattice.build_3strut_prism()
    # In a true tensegrity prism, struts never share a node
    strut_nodes = set()
    for s in telemetry.struts:
        assert s.node_a_id not in strut_nodes
        assert s.node_b_id not in strut_nodes
        strut_nodes.add(s.node_a_id)
        strut_nodes.add(s.node_b_id)
    assert len(strut_nodes) == 6


def test_isometric_projection():
    lattice = TensegrityEquilibriumLattice()
    sx, sy = lattice.project_isometric(100.0, 50.0, 80.0, center_x=450.0, center_y=270.0)
    assert isinstance(sx, float)
    assert isinstance(sy, float)
    assert 200.0 < sx < 700.0
    assert 100.0 < sy < 450.0


def test_strain_energy_calculation():
    lattice = TensegrityEquilibriumLattice()
    low_prestress = lattice.build_3strut_prism(prestress_level=50.0)
    high_prestress = lattice.build_3strut_prism(prestress_level=150.0)
    assert high_prestress.total_strain_energy > low_prestress.total_strain_energy
    assert high_prestress.mean_prestress_tension == 150.0


def test_svg_rendering():
    lattice = TensegrityEquilibriumLattice()
    telemetry = lattice.build_3strut_prism()
    svg = lattice.render_tensegrity_svg(telemetry, width=920, height=560)
    assert "<svg" in svg
    assert "</svg>" in svg
    assert "#0b0f14" in svg
    assert "TENSEGRITY CABLE-STRUT LATTICE" in svg
    assert "Compression Struts" in svg
    assert "Tension Cables" in svg
    assert "3_STRUT_PRISM" in svg


def test_export_telemetry_json():
    lattice = TensegrityEquilibriumLattice()
    telemetry = lattice.build_6strut_icosahedron()
    json_str = lattice.export_telemetry_json(telemetry)
    data = json.loads(json_str)
    assert "structure_type" in data
    assert "total_nodes" in data
    assert "total_struts" in data
    assert "total_cables" in data
    assert len(data["struts"]) == 6
    assert len(data["cables"]) == 24


def test_zero_em_dashes():
    """Verify zero em dashes in script and test files."""
    script_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "scripts", "tensegrity_equilibrium_lattice.py")
    )
    with open(script_path, "r", encoding="utf-8") as f:
        script_code = f.read()
    assert chr(8212) not in script_code, "Unicode em dash found in tensegrity_equilibrium_lattice.py"

    test_path = os.path.abspath(__file__)
    with open(test_path, "r", encoding="utf-8") as f:
        test_code = f.read()
    assert chr(8212) not in test_code, "Unicode em dash found in test_tensegrity_equilibrium_lattice.py"
