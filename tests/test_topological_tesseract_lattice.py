"""
Unit tests for Topological Tesseract Lattice & 4D Schema Morphing Engine.
Verifies 4D coordinate representation, dual isoclinic rotations, perspective
projection to 2D screen coordinates, canonical 16-vertex/32-edge topology,
dark titanium SVG rendering, and markdown telemetry. Strictly zero em dashes enforced.
"""

import pytest
import math
from scripts.topological_tesseract_lattice import (
    HyperVertex,
    HyperEdge,
    TesseractProjection,
    TesseractTelemetry,
    TopologicalTesseractLattice,
    sample_4d_schema_hypercube,
)


def test_hyper_vertex_initialization():
    v = HyperVertex(
        vertex_id="v-test",
        coords_4d=(1.0, -1.0, 1.0, -1.0),
        title="Test Node",
        axis_labels={"X": "Macro", "Y": "Static"},
    )
    assert v.vertex_id == "v-test"
    assert v.coords_4d == (1.0, -1.0, 1.0, -1.0)
    assert v.title == "Test Node"
    assert v.active is True
    assert v.axis_labels["X"] == "Macro"


def test_canonical_hypercube_topology():
    vertices, edges = sample_4d_schema_hypercube()
    # 4D hypercube has 16 vertices and 32 edges
    assert len(vertices) == 16
    assert len(edges) == 32

    # Each vertex must connect to exactly 4 orthogonal neighbors
    vertex_degree = {}
    for edge in edges:
        vertex_degree[edge.source_id] = vertex_degree.get(edge.source_id, 0) + 1
        vertex_degree[edge.target_id] = vertex_degree.get(edge.target_id, 0) + 1

    for v_id, deg in vertex_degree.items():
        assert deg == 4


def test_rotation_4d_invariance():
    lattice = TopologicalTesseractLattice()
    # At theta=0, phi=0, rotated coords should equal original
    rx, ry, rz, rw = lattice.rotate_4d(1.0, 2.0, 3.0, 4.0, 0.0, 0.0)
    assert abs(rx - 1.0) < 1e-6
    assert abs(ry - 2.0) < 1e-6
    assert abs(rz - 3.0) < 1e-6
    assert abs(rw - 4.0) < 1e-6

    # 4D distance from origin must be preserved under rotation
    dist_orig = math.sqrt(1.0**2 + 2.0**2 + 3.0**2 + 4.0**2)
    rx2, ry2, rz2, rw2 = lattice.rotate_4d(1.0, 2.0, 3.0, 4.0, 0.8, 1.2)
    dist_rot = math.sqrt(rx2**2 + ry2**2 + rz2**2 + rw2**2)
    assert abs(dist_orig - dist_rot) < 1e-6


def test_project_vertex_centering():
    lattice = TopologicalTesseractLattice()
    cx, cy = 460.0, 280.0
    px, py, z3, rw = lattice.project_vertex(0.0, 0.0, 0.0, 0.0, cx, cy)
    assert px == cx
    assert py == cy


def test_solve_lattice_telemetry():
    lattice = TopologicalTesseractLattice()
    vertices, edges = sample_4d_schema_hypercube()
    telemetry = lattice.solve_lattice(vertices, edges, theta_deg=45.0, phi_deg=30.0)

    assert telemetry.total_vertices == 16
    assert telemetry.total_edges == 32
    assert telemetry.cell_count == 8
    assert len(telemetry.projected_vertices) == 16
    assert 0.0 <= telemetry.symmetry_metric <= 1.0


def test_perspective_w_depth_layering():
    lattice = TopologicalTesseractLattice()
    vertices, edges = sample_4d_schema_hypercube()
    telemetry = lattice.solve_lattice(vertices, edges, theta_deg=0.0, phi_deg=0.0)

    # At 0 rotation, inner cube (w=-1) must have different scale/depth from outer cube (w=+1)
    w_depths = set(p.w_depth for p in telemetry.projected_vertices)
    assert len(w_depths) >= 2


def test_generate_svg():
    lattice = TopologicalTesseractLattice()
    vertices, edges = sample_4d_schema_hypercube()
    telemetry = lattice.solve_lattice(vertices, edges)

    svg_code = lattice.generate_svg(telemetry)
    assert "<svg" in svg_code
    assert "</svg>" in svg_code
    assert "hyperGlow" in svg_code
    assert "TOPOLOGICAL TESSERACT HUD" in svg_code
    assert chr(8212) not in svg_code


def test_generate_markdown_report():
    lattice = TopologicalTesseractLattice()
    vertices, edges = sample_4d_schema_hypercube()
    telemetry = lattice.solve_lattice(vertices, edges)

    md_report = lattice.generate_markdown_report(telemetry)
    assert "# Topological Tesseract Lattice and 4D Schema Telemetry" in md_report
    assert "## 1. Hyper-Dimensional Projection Overview" in md_report
    assert "## 3. Projected Hyper-Vertex Coordinates" in md_report
    assert chr(8212) not in md_report
