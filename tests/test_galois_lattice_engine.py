"""
test_galois_lattice_engine.py - Unit tests for GaloisLatticeEngine (Phase 99, Cycle 95).

Tests Formal Concept Analysis Galois lattice, derivation operators,
cross-cluster associative bridge synthesis, Obsidian Canvas export, SVG generation, and zero em dashes.

Strict constraint: Strictly zero em dashes (Unicode U+2014) anywhere.
"""

from pathlib import Path
import pytest
from scripts.galois_lattice_engine import (
    AssociativeBridgePath,
    FormalConcept,
    FormalObject,
    GaloisLatticeEngine,
    GaloisLatticeResult,
    GaloisLatticeTelemetry,
)


@pytest.fixture
def sample_entities():
    return [
        {
            "id": "card_01",
            "name": "Local Spatial Canvas",
            "cluster": "spatial_ui",
            "attributes": ["local-first", "crdt", "reactive", "spatial"],
        },
        {
            "id": "card_02",
            "name": "Reactive Event Bus",
            "cluster": "spatial_ui",
            "attributes": ["reactive", "async", "decoupled"],
        },
        {
            "id": "card_03",
            "name": "Distributed Storage Ledger",
            "cluster": "backend_storage",
            "attributes": ["crdt", "local-first", "audit", "distributed"],
        },
        {
            "id": "card_04",
            "name": "Audit Log Aggregator",
            "cluster": "backend_storage",
            "attributes": ["audit", "distributed", "linearizable"],
        },
    ]


def test_empty_objects():
    engine = GaloisLatticeEngine()
    result = engine.analyze([])
    assert isinstance(result, GaloisLatticeResult)
    assert len(result.objects) == 0
    assert len(result.concepts) == 0
    assert len(result.bridges) == 0
    assert result.telemetry.total_objects == 0
    assert result.telemetry.cowan_bounded is True


def test_load_objects_formats():
    engine = GaloisLatticeEngine()

    # List format
    list_input = [
        {"id": "o1", "name": "Node A", "cluster": "c1", "attributes": ["alpha", "beta"]},
        {"id": "o2", "name": "Node B", "cluster": "c2", "attributes": ["beta", "gamma"]},
    ]
    objs = engine.load_objects(list_input)
    assert len(objs) == 2
    assert objs[0].object_id == "o1"
    assert "alpha" in objs[0].attributes

    # Obsidian Canvas format
    canvas_dict = {
        "nodes": [
            {"id": "n1", "text": "### Spatial Node\n#reactive #crdt details", "color": "4"},
            {"id": "n2", "text": "### Ledger Node\n#distributed #crdt details", "color": "1"},
        ]
    }
    objs_canvas = engine.load_objects(canvas_dict)
    assert len(objs_canvas) == 2
    assert "crdt" in objs_canvas[0].attributes
    assert objs_canvas[0].cluster == "cyan_domain"


def test_derivation_operators(sample_entities):
    engine = GaloisLatticeEngine()
    objs = engine.load_objects(sample_entities)

    # Derivation B' (objects containing attributes)
    extent = engine.derive_extent({"local-first", "crdt"}, objs)
    assert "card_01" in extent
    assert "card_03" in extent
    assert "card_02" not in extent

    # Derivation A' (attributes shared by objects)
    intent = engine.derive_intent({"card_01", "card_03"}, objs)
    assert "local-first" in intent
    assert "crdt" in intent
    assert "reactive" not in intent


def test_build_concept_lattice(sample_entities):
    engine = GaloisLatticeEngine()
    objs = engine.load_objects(sample_entities)
    concepts = engine.build_concept_lattice(objs)

    assert len(concepts) >= 3
    # Verify top concept exists
    top = next((c for c in concepts if c.is_lattice_top), None)
    assert top is not None
    assert len(top.extent) == len(objs)


def test_synthesize_associative_bridges(sample_entities):
    engine = GaloisLatticeEngine(min_resonance_threshold=0.2)
    result = engine.analyze(sample_entities)

    assert len(result.bridges) >= 1
    primary_bridge = result.bridges[0]
    assert isinstance(primary_bridge, AssociativeBridgePath)
    assert primary_bridge.source_cluster != primary_bridge.target_cluster
    assert "crdt" in primary_bridge.shared_intent or "local-first" in primary_bridge.shared_intent
    assert primary_bridge.resonance_score > 0.3
    assert result.telemetry.cognitive_load_saved_pct > 0.0


def test_canvas_export(sample_entities, tmp_path):
    engine = GaloisLatticeEngine()
    result = engine.analyze(sample_entities)

    out_file = tmp_path / "galois.canvas"
    canvas_dict = engine.export_canvas(result, str(out_file))

    assert out_file.exists()
    assert "nodes" in canvas_dict
    assert "edges" in canvas_dict
    assert len(canvas_dict["nodes"]) >= 4
    assert len(canvas_dict["edges"]) >= 1


def test_svg_export(sample_entities, tmp_path):
    engine = GaloisLatticeEngine()
    result = engine.analyze(sample_entities)

    svg_file = tmp_path / "galois.svg"
    svg_content = engine.export_svg(result, str(svg_file))

    assert svg_file.exists()
    assert "<svg" in svg_content
    assert "</svg>" in svg_content
    assert "Galois Lattice" in svg_content
    assert "TOP LATTICE CONCEPT" in svg_content


def test_ascii_report(sample_entities):
    engine = GaloisLatticeEngine()
    result = engine.analyze(sample_entities)
    report = engine.generate_ascii_report(result)

    assert "GALOIS CONCEPT LATTICE" in report
    assert "FORMAL CONCEPTS" in report
    assert "DISCOVERED CROSS-CLUSTER" in report
    assert "Cowan Bounded" in report


def test_zero_em_dashes():
    """Verify strictly zero em dashes in code and test files."""
    files_to_check = [
        Path("scripts/galois_lattice_engine.py"),
        Path("tests/test_galois_lattice_engine.py"),
    ]
    em_dash = chr(8212)
    for fpath in files_to_check:
        if fpath.exists():
            text = fpath.read_text(encoding="utf-8")
            assert em_dash not in text, f"Em dash found in {fpath}"
