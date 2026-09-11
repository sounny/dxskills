"""
Unit tests for Knowledge Mesh Consolidator & Semantic Hyper-Graph Weaver Engine.
Verifies cross-domain primitive mapping, hyper-edge formation, domain bridge calculation,
IRI scoring, SVG rendering, markdown reporting, and strict zero-em-dash compliance.
"""

import os
import pytest
from scripts.knowledge_mesh_weaver import (
    MeshNode,
    HyperEdge,
    DomainBridge,
    KnowledgeMeshTelemetry,
    KnowledgeMeshWeaver,
    sample_knowledge_mesh,
)


def test_mesh_node_initialization():
    node = MeshNode(
        node_id="n1",
        title="Cell Respiration",
        domain="Biology",
        semantic_primitives=["combustion", "energy-transfer", "buffering"],
        pos_x=120.0,
        pos_y=240.0,
        weight=1.5,
    )
    assert node.node_id == "n1"
    assert node.title == "Cell Respiration"
    assert node.domain == "Biology"
    assert len(node.semantic_primitives) == 3
    assert node.pos_x == 120.0
    assert node.pos_y == 240.0
    assert node.weight == 1.5


def test_hyper_edge_initialization():
    edge = HyperEdge(
        edge_id="he-01",
        title="Primitive: Buffering",
        shared_primitive="buffering",
        member_node_ids=["n1", "n2", "n3"],
        domains_spanned=["Biology", "Distributed Systems", "Urbanism"],
        coherence_score=0.92,
        color_hex="#38bdf8",
    )
    assert edge.edge_id == "he-01"
    assert edge.shared_primitive == "buffering"
    assert len(edge.member_node_ids) == 3
    assert len(edge.domains_spanned) == 3
    assert edge.coherence_score == 0.92


def test_weave_mesh_empty():
    weaver = KnowledgeMeshWeaver()
    telemetry = weaver.weave_mesh([])
    assert telemetry.total_nodes == 0
    assert telemetry.domain_count == 0
    assert telemetry.hyper_edges_count == 0
    assert telemetry.cross_domain_bridges_count == 0
    assert telemetry.interconnected_reasoning_index == 0.0


def test_weave_mesh_hyper_edges():
    weaver = KnowledgeMeshWeaver(min_cluster_size=2)
    nodes = sample_knowledge_mesh()
    telemetry = weaver.weave_mesh(nodes)

    assert telemetry.total_nodes == 6
    assert telemetry.domain_count == 3
    assert telemetry.hyper_edges_count > 0

    # Verify "buffering" hyper-edge includes bio-1, sys-1, and urb-1
    buffering_edges = [he for he in telemetry.hyper_edges if he.shared_primitive == "buffering"]
    assert len(buffering_edges) == 1
    he_buff = buffering_edges[0]
    assert "bio-1" in he_buff.member_node_ids
    assert "sys-1" in he_buff.member_node_ids
    assert "urb-1" in he_buff.member_node_ids
    assert len(he_buff.domains_spanned) == 3


def test_weave_mesh_domain_bridges():
    weaver = KnowledgeMeshWeaver()
    nodes = sample_knowledge_mesh()
    telemetry = weaver.weave_mesh(nodes)

    assert telemetry.cross_domain_bridges_count > 0
    bridges = telemetry.domain_bridges

    # There should be a bridge between Biology and Distributed Systems
    bio_sys = [
        b for b in bridges
        if (b.domain_a == "Biology" and b.domain_b == "Distributed Systems")
        or (b.domain_a == "Distributed Systems" and b.domain_b == "Biology")
    ]
    assert len(bio_sys) == 1
    assert bio_sys[0].resonance_strength > 0.0
    assert "semi-permeable" in bio_sys[0].bridging_primitives or "pattern-matching" in bio_sys[0].bridging_primitives


def test_interconnected_reasoning_index():
    weaver = KnowledgeMeshWeaver()
    nodes = sample_knowledge_mesh()
    telemetry = weaver.weave_mesh(nodes)

    assert 0.0 <= telemetry.interconnected_reasoning_index <= 1.0
    assert telemetry.mesh_density > 0.0


def test_generate_markdown_report():
    weaver = KnowledgeMeshWeaver()
    nodes = sample_knowledge_mesh()
    telemetry = weaver.weave_mesh(nodes)
    report = weaver.generate_markdown_report(telemetry)

    assert "# Knowledge Mesh Consolidator and Semantic Hyper-Graph Weaver Report" in report
    assert "Neuro-Cognitive Grounding (Eide & Eide I-Strengths)" in report
    assert "Discovered Hyper-Edge Envelopes" in report
    assert "Cross-Domain Resonance Bridges" in report


def test_generate_svg():
    weaver = KnowledgeMeshWeaver()
    nodes = sample_knowledge_mesh()
    telemetry = weaver.weave_mesh(nodes)
    svg = weaver.generate_svg(nodes, telemetry, width=900, height=540)

    assert "<svg" in svg
    assert "</svg>" in svg
    assert "meshGlow" in svg
    assert "KNOWLEDGE MESH HYPER-GRAPH HUD" in svg
    assert "Cell Membrane Osmosis" in svg
    assert "polygon" in svg or "line" in svg


def test_zero_em_dashes_in_source_and_outputs():
    # Verify module source file
    script_path = os.path.join(os.path.dirname(__file__), "..", "scripts", "knowledge_mesh_weaver.py")
    with open(script_path, "r", encoding="utf-8") as f:
        source = f.read()
    assert chr(8212) not in source

    # Verify report and svg outputs
    weaver = KnowledgeMeshWeaver()
    nodes = sample_knowledge_mesh()
    telemetry = weaver.weave_mesh(nodes)
    report = weaver.generate_markdown_report(telemetry)
    svg = weaver.generate_svg(nodes, telemetry)

    assert chr(8212) not in report
    assert chr(8212) not in svg
