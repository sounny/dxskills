"""
Unit tests for Polyhedral Schema Crystallizer & Dimensionality Folder Engine.
Verifies polyhedral face mapping (tetrahedron, cube, octahedron), dihedral angles,
unfolded 2D net coordinates, SVG rendering, markdown reporting, and strict zero-em-dash compliance.
"""

import os
import pytest
from scripts.polyhedral_schema_crystallizer import (
    PolyhedralFace,
    PolyhedralNet,
    CrystallizerTelemetry,
    PolyhedralSchemaCrystallizer,
    sample_crystallizer_concepts,
)


def test_polyhedral_face_initialization():
    face = PolyhedralFace(
        face_id=1,
        title="Core Face",
        concept_summary="Summary text",
        adjacent_face_ids=[2, 3, 4],
        center_x=100.0,
        center_y=150.0,
        polygon_vertices=[(100.0, 100.0), (150.0, 200.0), (50.0, 200.0)],
        color_hex="#38bdf8",
        dihedral_angle_deg=70.53,
    )
    assert face.face_id == 1
    assert face.title == "Core Face"
    assert len(face.adjacent_face_ids) == 3
    assert len(face.polygon_vertices) == 3
    assert face.dihedral_angle_deg == 70.53


def test_polyhedral_net_initialization():
    net = PolyhedralNet(
        polyhedron_type="cube",
        face_count=6,
        faces=[],
        crystallization_coherence=0.95,
    )
    assert net.polyhedron_type == "cube"
    assert net.face_count == 6
    assert net.crystallization_coherence == 0.95


def test_crystallize_schema_tetrahedron():
    crystallizer = PolyhedralSchemaCrystallizer()
    concepts = [{"title": f"Concept {i}", "text": "desc"} for i in range(4)]
    telemetry = crystallizer.crystallize_schema(concepts, polyhedron_type="tetrahedron")

    assert telemetry.selected_polyhedron == "tetrahedron"
    assert telemetry.polyhedral_net.face_count == 4
    assert telemetry.face_coverage_ratio == 1.0
    assert telemetry.mean_dihedral_angle_deg == pytest.approx(70.53, abs=0.1)
    assert len(telemetry.polyhedral_net.faces) == 4


def test_crystallize_schema_cube():
    crystallizer = PolyhedralSchemaCrystallizer()
    concepts = sample_crystallizer_concepts()  # 6 concepts
    telemetry = crystallizer.crystallize_schema(concepts, polyhedron_type="auto")

    assert telemetry.selected_polyhedron == "cube"
    assert telemetry.polyhedral_net.face_count == 6
    assert telemetry.face_coverage_ratio == 1.0
    assert telemetry.mean_dihedral_angle_deg == 90.0
    assert len(telemetry.polyhedral_net.faces) == 6


def test_crystallize_schema_octahedron():
    crystallizer = PolyhedralSchemaCrystallizer()
    concepts = [{"title": f"Concept {i}", "text": "desc"} for i in range(8)]
    telemetry = crystallizer.crystallize_schema(concepts, polyhedron_type="octahedron")

    assert telemetry.selected_polyhedron == "octahedron"
    assert telemetry.polyhedral_net.face_count == 8
    assert telemetry.face_coverage_ratio == 1.0
    assert telemetry.mean_dihedral_angle_deg == pytest.approx(109.47, abs=0.1)


def test_crystallize_schema_empty():
    crystallizer = PolyhedralSchemaCrystallizer()
    telemetry = crystallizer.crystallize_schema([], polyhedron_type="cube")
    assert telemetry.input_concepts_count == 0
    assert telemetry.face_coverage_ratio == 0.0
    assert telemetry.polyhedral_net.face_count == 6


def test_generate_markdown_report():
    crystallizer = PolyhedralSchemaCrystallizer()
    concepts = sample_crystallizer_concepts()
    telemetry = crystallizer.crystallize_schema(concepts)
    report = crystallizer.generate_markdown_report(telemetry)

    assert "# Polyhedral Schema Crystallizer and Dimensionality Folder Report" in report
    assert "Neuro-Cognitive Theoretical Grounding (Eide & Eide S-Strengths)" in report
    assert "Polyhedral Face Allocation Blueprint" in report
    assert "Core Consensus" in report


def test_generate_svg():
    crystallizer = PolyhedralSchemaCrystallizer()
    concepts = sample_crystallizer_concepts()
    telemetry = crystallizer.crystallize_schema(concepts)
    svg = crystallizer.generate_svg(telemetry, width=900, height=540)

    assert "<svg" in svg
    assert "</svg>" in svg
    assert "polygon" in svg
    assert "POLYHEDRAL SCHEMA CRYSTALLIZER HUD" in svg
    assert "CUBE" in svg


def test_zero_em_dashes_in_source_and_outputs():
    # Verify module source file
    script_path = os.path.join(os.path.dirname(__file__), "..", "scripts", "polyhedral_schema_crystallizer.py")
    with open(script_path, "r", encoding="utf-8") as f:
        source = f.read()
    assert chr(8212) not in source

    # Verify report and svg outputs
    crystallizer = PolyhedralSchemaCrystallizer()
    concepts = sample_crystallizer_concepts()
    telemetry = crystallizer.crystallize_schema(concepts)
    report = crystallizer.generate_markdown_report(telemetry)
    svg = crystallizer.generate_svg(telemetry)

    assert chr(8212) not in report
    assert chr(8212) not in svg
