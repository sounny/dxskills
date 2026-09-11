"""
test_causal_narrative_loom.py - Unit tests for CausalNarrativeLoom (Phase 105, Cycle 101).

Tests Pearl causal DAG parsing, critical path extraction, forward and backward
narrative prose weaving, SVG export, and zero em dashes.

Strict constraint: Strictly zero em dashes (Unicode U+2014) anywhere.
"""

from pathlib import Path
import pytest
from scripts.causal_narrative_loom import (
    CausalEdge,
    CausalNarrativeLoom,
    CausalNarrativeResult,
    CausalNode,
    LoomTelemetry,
)


@pytest.fixture
def architectural_causal_dag():
    nodes = [
        {"id": "n1", "label": "Phonological Bottleneck", "node_type": "EVENT"},
        {"id": "n2", "label": "Spatial Scaffolding Harness", "node_type": "DECISION"},
        {"id": "n3", "label": "Peripheral Clutter Attenuation", "node_type": "DECISION"},
        {"id": "n4", "label": "Cognitive Stamina Restoration", "node_type": "OUTCOME"},
    ]
    edges = [
        {"source_id": "n1", "target_id": "n2", "relation": "CAUSES"},
        {"source_id": "n2", "target_id": "n3", "relation": "ENABLES"},
        {"source_id": "n3", "target_id": "n4", "relation": "RESULTS_IN"},
    ]
    return nodes, edges


def test_empty_loom():
    loom = CausalNarrativeLoom()
    result = loom.weave_narrative(raw_nodes=[])
    assert isinstance(result, CausalNarrativeResult)
    assert result.telemetry.total_nodes == 0
    assert result.telemetry.total_edges == 0
    assert result.telemetry.cowan_bounded is True
    assert len(result.nodes) == 0
    assert len(result.critical_chain) == 0


def test_causal_dag_and_critical_chain(architectural_causal_dag):
    loom = CausalNarrativeLoom()
    nodes, edges = architectural_causal_dag
    result = loom.weave_narrative(raw_nodes=nodes, raw_edges=edges)

    assert result.telemetry.total_nodes == 4
    assert result.telemetry.total_edges == 3
    assert result.telemetry.root_causes_count == 1
    assert result.telemetry.terminal_outcomes_count == 1
    assert result.telemetry.max_causal_depth == 4
    assert result.telemetry.cowan_bounded is True
    assert result.telemetry.linearization_memory_saved_pct > 40.0

    # Verify critical chain ordering
    assert result.critical_chain == ["n1", "n2", "n3", "n4"]


def test_bi_directional_prose_weaving(architectural_causal_dag):
    loom = CausalNarrativeLoom()
    nodes, edges = architectural_causal_dag
    result = loom.weave_narrative(raw_nodes=nodes, raw_edges=edges)

    # Forward chronological prose
    assert "Executive Summary: Causal Trajectory Flow" in result.forward_narrative
    assert "Primary Causal Spine" in result.forward_narrative
    assert "Phonological Bottleneck" in result.forward_narrative
    assert "causes" in result.forward_narrative.lower()

    # Backward diagnostic prose
    assert "Retrospective Diagnostic: Backward Dependency Verification" in result.backward_diagnostic
    assert "Prerequisite Ladder" in result.backward_diagnostic
    assert "Cognitive Stamina Restoration" in result.backward_diagnostic


def test_text_corpus_fallback():
    loom = CausalNarrativeLoom()
    corpus = (
        "Dense technical prose leads to cognitive fatigue.\n"
        "Cognitive fatigue causes saccadic velocity decay.\n"
        "Saccadic velocity decay enables contrast dampening intervention.\n"
    )
    result = loom.weave_narrative(raw_nodes=[], text_corpus=corpus)

    assert result.telemetry.total_nodes >= 2
    assert result.telemetry.total_edges >= 2
    assert result.telemetry.max_causal_depth >= 2


def test_cowan_depth_bounding():
    loom = CausalNarrativeLoom(max_cowan_depth=3)
    nodes = [{"id": f"node_{i}", "label": f"Step {i}"} for i in range(5)]
    edges = [{"source_id": f"node_{i}", "target_id": f"node_{i+1}", "relation": "CAUSES"} for i in range(4)]

    result = loom.weave_narrative(raw_nodes=nodes, raw_edges=edges)
    assert result.telemetry.max_causal_depth == 5
    assert result.telemetry.cowan_bounded is False


def test_svg_export(tmp_path: Path, architectural_causal_dag):
    loom = CausalNarrativeLoom()
    nodes, edges = architectural_causal_dag
    result = loom.weave_narrative(raw_nodes=nodes, raw_edges=edges)

    svg_file = tmp_path / "causal_loom.svg"
    svg_content = loom.export_svg(result, output_path=str(svg_file))

    assert "<svg" in svg_content
    assert "</svg>" in svg_content
    assert "Bi-Directional Causal Narrative Loom" in svg_content
    assert svg_file.exists()
    assert svg_file.stat().st_size > 500


def test_ascii_report(architectural_causal_dag):
    loom = CausalNarrativeLoom()
    nodes, edges = architectural_causal_dag
    result = loom.weave_narrative(raw_nodes=nodes, raw_edges=edges)
    report = loom.generate_ascii_report(result)

    assert "BI-DIRECTIONAL CAUSAL NARRATIVE LOOM" in report
    assert "Causal Topology" in report
    assert "Critical Spine Depth" in report
    assert "Step 1:" in report


def test_zero_em_dashes():
    source_files = [
        Path("scripts/causal_narrative_loom.py"),
        Path("tests/test_causal_narrative_loom.py"),
    ]
    for p in source_files:
        if p.exists():
            text = p.read_text(encoding="utf-8")
            assert "\u2014" not in text, f"Em dash found in {p}"
