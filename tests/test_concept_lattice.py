"""Unit tests for Autonomous Cognitive Spatial Associative Resonance & Concept Lattice Compiler.

Strict Quality Gate: Zero em dashes anywhere (use hyphens, commas, or parentheses).
"""

from __future__ import annotations

import json
from pathlib import Path
import pytest

from scripts.concept_lattice import (
    ConceptLatticeCompiler,
    FormalConcept,
    LatticeEdge,
    AssociativeLeap,
    LeapCategory,
)


def test_empty_context() -> None:
    """Ensure compiler handles empty formal contexts gracefully."""
    compiler = ConceptLatticeCompiler()
    concepts, edges, leaps, telemetry = compiler.compute_lattice()

    assert len(concepts) == 0
    assert len(edges) == 0
    assert len(leaps) == 0
    assert telemetry.total_concepts == 0
    assert telemetry.max_lattice_depth == 0


def test_galois_derivation_and_lattice_structure() -> None:
    """Verify FCA derivation operators and closed concept hierarchy."""
    compiler = ConceptLatticeCompiler(min_resonance=0.3)
    context = {
        "mechanical_damper": ["energy_dissipation", "resilience", "hardware"],
        "viscoelastic_mount": ["energy_dissipation", "resilience", "hardware", "isolation"],
        "rate_limiter": ["energy_dissipation", "resilience", "software", "backpressure"],
        "circuit_breaker": ["resilience", "software", "fault_tolerance"],
    }
    compiler.load_context(context)

    # Test Galois derivation
    common_attrs = compiler._prime_objects({"mechanical_damper", "rate_limiter"})
    assert "energy_dissipation" in common_attrs
    assert "resilience" in common_attrs

    matching_objs = compiler._prime_attributes({"energy_dissipation", "resilience"})
    assert "mechanical_damper" in matching_objs
    assert "viscoelastic_mount" in matching_objs
    assert "rate_limiter" in matching_objs

    concepts, edges, leaps, telemetry = compiler.compute_lattice()

    assert len(concepts) >= 4
    assert len(edges) >= 3
    assert telemetry.total_objects == 4
    assert telemetry.total_attributes == 7
    assert telemetry.max_lattice_depth >= 1

    # Verify Hasse cover property: no edge should jump over an intermediate concept
    concept_map = {c.concept_id: set(c.extent) for c in concepts}
    for edge in edges:
        sub_ext = concept_map[edge.child_id]
        sup_ext = concept_map[edge.parent_id]
        assert sub_ext < sup_ext
        for mid_c in concepts:
            mid_ext = set(mid_c.extent)
            assert not (sub_ext < mid_ext and mid_ext < sup_ext)


def test_associative_resonance_intuitive_leaps() -> None:
    """Verify detection of cross-domain analogical bridges and resonance scoring."""
    compiler = ConceptLatticeCompiler(min_resonance=0.35, max_overlap_for_leap=0.5)
    context = {
        "lymphatic_drainage": ["fluid_transport", "waste_clearance", "biological", "circulatory"],
        "vascular_tree": ["fluid_transport", "distribution", "biological", "circulatory"],
        "urban_stormwater_grid": ["fluid_transport", "waste_clearance", "infrastructure", "civil"],
        "data_pipeline_drain": ["waste_clearance", "infrastructure", "software"],
    }
    compiler.load_context(context)
    concepts, edges, leaps, telemetry = compiler.compute_lattice()

    assert len(leaps) > 0
    top_leap = leaps[0]
    assert top_leap.resonance_score >= 0.35
    assert len(top_leap.shared_intent) > 0
    assert top_leap.category in [
        LeapCategory.CROSS_DOMAIN_ISOMORPHISM,
        LeapCategory.ANALOGICAL_BRIDGE,
        LeapCategory.EMERGENT_INTEGRATION,
        LeapCategory.METAPHORIC_SYNTHESIS,
    ]
    assert telemetry.associative_leaps_count == len(leaps)


def test_canvas_export(tmp_path: Path) -> None:
    """Verify Obsidian .canvas structure and properties."""
    compiler = ConceptLatticeCompiler()
    context = {
        "neural_net": ["learning", "adaptation", "weights"],
        "decision_tree": ["interpretable", "rules", "classification"],
        "expert_system": ["rules", "classification", "knowledge_base"],
    }
    compiler.load_context(context)

    canvas_file = str(tmp_path / "test_lattice.canvas")
    canvas_dict = compiler.to_canvas(canvas_file, canvas_title="ML Architecture Lattice")

    assert Path(canvas_file).exists()
    assert "nodes" in canvas_dict
    assert "edges" in canvas_dict
    assert len(canvas_dict["nodes"]) >= 3

    # Check node formatting
    first_node = canvas_dict["nodes"][0]
    assert "id" in first_node
    assert "x" in first_node
    assert "y" in first_node
    assert "color" in first_node
    assert "text" in first_node


def test_svg_export(tmp_path: Path) -> None:
    """Verify SVG generation with publication styling and telemetry legend."""
    compiler = ConceptLatticeCompiler()
    context = {
        "alpha": ["shared_one", "shared_two", "feat_a"],
        "beta": ["shared_one", "shared_two", "feat_b"],
        "gamma": ["shared_one", "feat_c"],
    }
    compiler.load_context(context)

    svg_file = str(tmp_path / "test_lattice.svg")
    svg_str = compiler.to_svg(svg_file, width=1000, height=700)

    assert Path(svg_file).exists()
    assert "<svg" in svg_str
    assert "</svg>" in svg_str
    assert "Formal Concept Lattice" in svg_str
    assert "M-I-N-D Lattice Metrics" in svg_str
    assert "#0B0F17" in svg_str  # Dark titanium background


def test_zero_em_dashes_in_module() -> None:
    """Verify that neither the script nor test files contain em dashes."""
    root_dir = Path(__file__).parent.parent
    script_path = root_dir / "scripts" / "concept_lattice.py"
    test_path = root_dir / "tests" / "test_concept_lattice.py"

    for p in [script_path, test_path]:
        content = p.read_text(encoding="utf-8")
        assert "\u2014" not in content, f"Em dash found in {p.name}"
