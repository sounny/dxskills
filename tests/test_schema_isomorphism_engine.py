"""
test_schema_isomorphism_engine.py - Unit tests for SchemaIsomorphismEngine (Phase 108, Cycle 104).

Tests Gentner structure-mapping graph homomorphisms, systematicity calculation,
cross-domain analogy transfer inferences, SVG export, and zero em dashes.

Strict constraint: Strictly zero em dashes (Unicode U+2014) anywhere.
"""

from pathlib import Path
import pytest
from scripts.schema_isomorphism_engine import (
    AnalogyTransferProjection,
    DomainSchema,
    IsomorphismResult,
    IsomorphismTelemetry,
    NodeMapping,
    SchemaIsomorphismEngine,
    SchemaNode,
    SchemaRelation,
)


@pytest.fixture
def hydraulic_schema():
    return DomainSchema.from_dict({
        "domain_name": "Hydraulic Power System",
        "nodes": [
            {"id": "pump", "name": "Centrifugal Pump", "role": "SOURCE"},
            {"id": "pipe", "name": "Conduit Pipe", "role": "TRANSPORT"},
            {"id": "valve", "name": "Flow Constrictor Valve", "role": "REGULATOR"},
            {"id": "basin", "name": "Reservoir Basin", "role": "SINK"},
        ],
        "relations": [
            {"source": "pump", "target": "pipe", "relation": "DRIVES"},
            {"source": "pipe", "target": "valve", "relation": "CIRCULATES"},
            {"source": "valve", "target": "basin", "relation": "REGULATES"},
        ],
    })


@pytest.fixture
def electrical_schema():
    return DomainSchema.from_dict({
        "domain_name": "Electrical Direct Current Circuit",
        "nodes": [
            {"id": "battery", "name": "Chemical Battery", "role": "SOURCE"},
            {"id": "wire", "name": "Copper Wire", "role": "TRANSPORT"},
            {"id": "resistor", "name": "Ceramic Resistor", "role": "REGULATOR"},
            {"id": "ground", "name": "Chassis Ground", "role": "SINK"},
        ],
        "relations": [
            {"source": "battery", "target": "wire", "relation": "DRIVES"},
            {"source": "wire", "target": "resistor", "relation": "CIRCULATES"},
            {"source": "resistor", "target": "ground", "relation": "REGULATES"},
        ],
    })


def test_empty_schemas():
    engine = SchemaIsomorphismEngine()
    empty_a = DomainSchema(domain_name="Empty A", nodes=[], relations=[])
    empty_b = DomainSchema(domain_name="Empty B", nodes=[], relations=[])
    res = engine.evaluate_isomorphism(empty_a, empty_b)

    assert isinstance(res, IsomorphismResult)
    assert res.isomorphism_score == 0.0
    assert res.systematicity_index == 0.0
    assert len(res.node_mappings) == 0
    assert res.is_valid_homomorphism is False


def test_isomorphism_evaluation(hydraulic_schema, electrical_schema):
    engine = SchemaIsomorphismEngine(min_alignment_threshold=0.60)
    res = engine.evaluate_isomorphism(hydraulic_schema, electrical_schema)

    assert res.isomorphism_score >= 0.80
    assert res.systematicity_index >= 0.80
    assert res.preserved_relations_count == 3
    assert res.unmapped_relations_count == 0
    assert res.is_valid_homomorphism is True
    assert len(res.node_mappings) == 4

    # Verify structural correspondences
    mapping_dict = {m.source_label: m.target_label for m in res.node_mappings}
    assert mapping_dict["Centrifugal Pump"] == "Chemical Battery"
    assert mapping_dict["Conduit Pipe"] == "Copper Wire"
    assert mapping_dict["Flow Constrictor Valve"] == "Ceramic Resistor"
    assert mapping_dict["Reservoir Basin"] == "Chassis Ground"


def test_analogy_transfer_synthesis(hydraulic_schema, electrical_schema):
    engine = SchemaIsomorphismEngine()
    proj = engine.synthesize_analogy_transfer(hydraulic_schema, electrical_schema)

    assert isinstance(proj, AnalogyTransferProjection)
    assert proj.source_domain == "Hydraulic Power System"
    assert proj.target_domain == "Electrical Direct Current Circuit"
    assert proj.telemetry.isomorphism_score >= 0.80
    assert proj.telemetry.cowan_bounded is True
    assert len(proj.transferred_inferences) >= 1
    assert "Cross-Domain Schema Isomorphism & Analogy Transfer Report" in proj.transfer_report_md
    assert "| `Centrifugal Pump` | `Chemical Battery` |" in proj.transfer_report_md


def test_unmapped_relation_generates_hypotheses(hydraulic_schema, electrical_schema):
    # Add a feedback relation in source that has no counterpart in target
    hydraulic_schema.relations.append(
        SchemaRelation(source_id="basin", target_id="pump", relation_type="CIRCULATES")
    )
    engine = SchemaIsomorphismEngine()
    proj = engine.synthesize_analogy_transfer(hydraulic_schema, electrical_schema)

    assert any("Projected Relational Hypothesis" in inf for inf in proj.transferred_inferences)
    assert any("Chassis Ground" in inf and "Chemical Battery" in inf for inf in proj.transferred_inferences)


def test_cowan_bounding_exceeded():
    engine = SchemaIsomorphismEngine()
    src_nodes = [{"id": f"s{i}", "name": f"Source {i}", "role": "TRANSFORMER"} for i in range(6)]
    tgt_nodes = [{"id": f"t{i}", "name": f"Target {i}", "role": "TRANSFORMER"} for i in range(6)]
    src = DomainSchema.from_dict({"domain_name": "Src6", "nodes": src_nodes, "relations": []})
    tgt = DomainSchema.from_dict({"domain_name": "Tgt6", "nodes": tgt_nodes, "relations": []})

    proj = engine.synthesize_analogy_transfer(src, tgt)
    assert proj.telemetry.mapped_nodes_count == 6
    assert proj.telemetry.cowan_bounded is False


def test_svg_export(tmp_path: Path, hydraulic_schema, electrical_schema):
    engine = SchemaIsomorphismEngine()
    proj = engine.synthesize_analogy_transfer(hydraulic_schema, electrical_schema)

    svg_file = tmp_path / "schema_projection.svg"
    svg_str = engine.export_svg(proj, output_path=str(svg_file))

    assert "<svg" in svg_str
    assert "</svg>" in svg_str
    assert "Schema Isomorphism &amp; Analogy Transfer Engine" in svg_str
    assert svg_file.exists()
    assert svg_file.stat().st_size > 500


def test_ascii_report(hydraulic_schema, electrical_schema):
    engine = SchemaIsomorphismEngine()
    proj = engine.synthesize_analogy_transfer(hydraulic_schema, electrical_schema)
    report = engine.generate_ascii_report(proj)

    assert "SCHEMA ISOMORPHISM & ANALOGY TRANSFER ENGINE" in report
    assert "Isomorphism Score" in report
    assert "[MAP]" in report
    assert "Centrifugal Pump" in report


def test_zero_em_dashes():
    source_files = [
        Path("scripts/schema_isomorphism_engine.py"),
        Path("tests/test_schema_isomorphism_engine.py"),
    ]
    for p in source_files:
        if p.exists():
            text = p.read_text(encoding="utf-8")
            assert "\u2014" not in text, f"Em dash found in {p}"
