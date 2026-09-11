"""
test_dialectic_loom.py - Unit tests for DialecticLoom (Phase 97, Cycle 93).

Tests structural tension mapping, Aufhebung bridge synthesis, Cowan 4-chunk
bounding, Obsidian Canvas export, SVG generation, and zero em dashes.

Strict constraint: Strictly zero em dashes (Unicode U+2014) anywhere.
"""

import json
from pathlib import Path
import pytest
from scripts.dialectic_loom import (
    ArgumentCard,
    AufhebungBridge,
    DialecticLoom,
    DialecticLoomResult,
    LoomTelemetry,
    TensionVector,
)


@pytest.fixture
def sample_architectural_cards():
    return [
        {
            "id": "node_01",
            "title": "Decoupled Autonomous Microservices",
            "statement": "Each domain service manages its own local datastore with independent deployment pipelines and eventual consistency.",
            "perspective": "thesis",
            "core_values": ["Autonomy", "Velocity", "Fault Isolation"],
            "failure_modes": ["Cascading latency", "Data drift", "Complex distributed sagas"],
        },
        {
            "id": "node_02",
            "title": "Strict Centralized Monolithic Ledger",
            "statement": "All transactions commit synchronously to a single ACID relational database with global governance and total order.",
            "perspective": "antithesis",
            "core_values": ["Coherence", "ACID Guarantees", "Auditability"],
            "failure_modes": ["Single point of failure", "Deployment lock-step", "Throughput bottleneck"],
        },
    ]


def test_empty_cards():
    loom = DialecticLoom()
    result = loom.analyze([])
    assert isinstance(result, DialecticLoomResult)
    assert len(result.cards) == 0
    assert len(result.tensions) == 0
    assert len(result.bridges) == 0
    assert result.telemetry.total_cards_processed == 0
    assert result.telemetry.cowan_bounded is True


def test_load_cards_formats():
    loom = DialecticLoom()

    # List format
    list_data = [
        {"id": "c1", "title": "Card 1", "statement": "Statement 1"},
        {"id": "c2", "title": "Card 2", "statement": "Statement 2"},
    ]
    cards = loom.load_cards(list_data)
    assert len(cards) == 2
    assert cards[0].card_id == "c1"

    # Obsidian canvas format
    canvas_data = {
        "nodes": [
            {"id": "n1", "type": "text", "text": "### Microservice Autonomy\nFast isolated deploys."},
            {"id": "n2", "type": "text", "text": "### Monolith Coherence\nSingle global ACID schema."},
        ],
        "edges": [],
    }
    cards_canvas = loom.load_cards(canvas_data)
    assert len(cards_canvas) == 2
    assert cards_canvas[0].title == "Microservice Autonomy"
    assert "Fast isolated deploys" in cards_canvas[0].statement


def test_perspective_classification():
    loom = DialecticLoom()
    cards_data = [
        {"id": "c1", "title": "Local-First Eventual Consistency", "statement": "Distributed speed and dynamic asynchronous updates"},
        {"id": "c2", "title": "Strict Global Governance", "statement": "Centralized linearizable auditability and formal stability"},
    ]
    result = loom.analyze(cards_data)
    assert result.cards[0].perspective == "thesis"
    assert result.cards[1].perspective == "antithesis"


def test_structural_tension_mapping(sample_architectural_cards):
    loom = DialecticLoom()
    result = loom.analyze(sample_architectural_cards)

    assert len(result.tensions) >= 1
    primary_tension = result.tensions[0]
    assert isinstance(primary_tension, TensionVector)
    assert primary_tension.intensity > 0.5
    assert primary_tension.thesis_card_id == "node_01"
    assert primary_tension.antithesis_card_id == "node_02"
    assert "vs" in primary_tension.axis_name or "Coupling" in primary_tension.axis_name


def test_aufhebung_bridge_synthesis(sample_architectural_cards):
    loom = DialecticLoom()
    result = loom.analyze(sample_architectural_cards)

    assert len(result.bridges) >= 1
    bridge = result.bridges[0]
    assert isinstance(bridge, AufhebungBridge)
    assert bridge.reification_fidelity > 0.8
    assert len(bridge.eliminated_failure_modes) >= 2
    assert len(bridge.invariant_guarantees) >= 2
    assert result.telemetry.cowan_bounded is True
    assert result.telemetry.cognitive_load_saved_pct > 0.0


def test_canvas_export(sample_architectural_cards, tmp_path):
    loom = DialecticLoom()
    result = loom.analyze(sample_architectural_cards)

    out_file = tmp_path / "dialectic_output.canvas"
    canvas_dict = loom.export_canvas(result, str(out_file))

    assert out_file.exists()
    assert "nodes" in canvas_dict
    assert "edges" in canvas_dict
    # At least 2 argument cards + 1 Aufhebung bridge = 3 nodes
    assert len(canvas_dict["nodes"]) >= 3
    # Check that edges exist with tension and synthesis labels
    assert len(canvas_dict["edges"]) >= 1


def test_svg_export(sample_architectural_cards, tmp_path):
    loom = DialecticLoom()
    result = loom.analyze(sample_architectural_cards)

    svg_file = tmp_path / "dialectic_diagram.svg"
    svg_content = loom.export_svg(result, str(svg_file))

    assert svg_file.exists()
    assert "<svg" in svg_content
    assert "</svg>" in svg_content
    assert "AUFHEBUNG SYNTHESIS" in svg_content
    assert "THESIS" in svg_content
    assert "ANTITHESIS" in svg_content


def test_ascii_report(sample_architectural_cards):
    loom = DialecticLoom()
    result = loom.analyze(sample_architectural_cards)
    report = loom.generate_ascii_report(result)

    assert "DIALECTIC REIFICATION" in report
    assert "AUFHEBUNG BRIDGES" in report
    assert "STRUCTURAL TENSIONS" in report
    assert "Cowan Bounded" in report


def test_zero_em_dashes():
    """Verify strictly zero em dashes in code and test files."""
    files_to_check = [
        Path("scripts/dialectic_loom.py"),
        Path("tests/test_dialectic_loom.py"),
    ]
    em_dash = chr(8212)
    for fpath in files_to_check:
        if fpath.exists():
            text = fpath.read_text(encoding="utf-8")
            assert em_dash not in text, f"Em dash found in {fpath}"
