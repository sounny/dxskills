"""Unit tests for Autonomous Cognitive Multi-Agent Workspace Consensus & Semantic Conflict Synthesizer.

Strict Quality Gate: Zero em dashes anywhere.
"""

import json
from pathlib import Path
import pytest

from scripts.workspace_consensus import (
    ConflictRecord,
    ConflictType,
    ConsensusMergeScorecard,
    WorkspaceConsensusSynthesizer,
)


def test_clean_concurrency_merge():
    synth = WorkspaceConsensusSynthesizer()

    base_canvas = {
        "nodes": [
            {"id": "n1", "x": 0, "y": 0, "text": "### Common Root\nBase architectural foundation."},
        ],
        "edges": [],
    }

    canvas_a = {
        "nodes": [
            {"id": "n1", "x": 0, "y": 0, "text": "### Common Root\nBase architectural foundation."},
            {"id": "n_a", "x": 200, "y": 0, "text": "### Feature A\nAgent A telemetry extension."},
        ],
        "edges": [{"id": "e_a", "fromNode": "n1", "toNode": "n_a"}],
    }

    canvas_b = {
        "nodes": [
            {"id": "n1", "x": 0, "y": 0, "text": "### Common Root\nBase architectural foundation."},
            {"id": "n_b", "x": 0, "y": 200, "text": "### Feature B\nAgent B cache extension."},
        ],
        "edges": [{"id": "e_b", "fromNode": "n1", "toNode": "n_b"}],
    }

    merged, scorecard = synth.synthesize_visual_merge(base_canvas, canvas_a, canvas_b)

    assert scorecard.semantic_divergences_count == 0
    assert scorecard.spatial_collisions_count == 0
    assert scorecard.clean_merges_count >= 2
    assert scorecard.consensus_stability_score >= 0.90
    assert len(merged["nodes"]) == 3
    assert len(merged["edges"]) == 2


def test_semantic_divergence_synthesis():
    synth = WorkspaceConsensusSynthesizer()

    base_canvas = {
        "nodes": [
            {"id": "n_shared", "x": 100, "y": 100, "text": "### Consensus Protocol\nDefault Raft consensus."},
        ],
        "edges": [],
    }

    # Branch A modifies consensus claim
    canvas_a = {
        "nodes": [
            {"id": "n_shared", "x": 100, "y": 100, "text": "### Consensus Protocol\nPaxos distributed consensus with multi-decree leases."},
        ],
        "edges": [],
    }

    # Branch B modifies consensus claim differently
    canvas_b = {
        "nodes": [
            {"id": "n_shared", "x": 100, "y": 100, "text": "### Consensus Protocol\nRaft consensus with zero-copy WAL replication."},
        ],
        "edges": [],
    }

    merged, scorecard = synth.synthesize_visual_merge(base_canvas, canvas_a, canvas_b)

    assert scorecard.semantic_divergences_count == 1
    assert len(scorecard.conflicts) == 1
    assert scorecard.conflicts[0].conflict_type == ConflictType.SEMANTIC_DIVERGENCE

    # Merged canvas must contain Branch A, Branch B, and Consensus Synthesis Bridge
    node_ids = [n["id"] for n in merged["nodes"]]
    assert "n_shared_agent_a" in node_ids
    assert "n_shared_agent_b" in node_ids
    assert "n_shared_consensus_bridge" in node_ids


def test_spatial_collision_detection():
    synth = WorkspaceConsensusSynthesizer(proximity_collision_threshold_px=50.0)

    base_canvas = {
        "nodes": [
            {"id": "n_pos", "x": 0, "y": 0, "text": "### Memory Ring\nCircular buffer."},
        ],
        "edges": [],
    }

    canvas_a = {
        "nodes": [
            {"id": "n_pos", "x": 200, "y": 300, "text": "### Memory Ring\nCircular buffer."},
        ],
        "edges": [],
    }

    canvas_b = {
        "nodes": [
            {"id": "n_pos", "x": -200, "y": -150, "text": "### Memory Ring\nCircular buffer."},
        ],
        "edges": [],
    }

    scorecard = synth.audit_concurrency(base_canvas, canvas_a, canvas_b)
    assert scorecard.spatial_collisions_count == 1
    assert any(c.conflict_type == ConflictType.SPATIAL_COLLISION for c in scorecard.conflicts)


def test_structural_edge_fork():
    synth = WorkspaceConsensusSynthesizer()

    base_canvas = {
        "nodes": [
            {"id": "src", "x": 0, "y": 0, "text": "### Source Node"},
            {"id": "dst1", "x": 100, "y": 0, "text": "### Destination 1"},
            {"id": "dst2", "x": 200, "y": 0, "text": "### Destination 2"},
        ],
        "edges": [{"id": "edge_1", "fromNode": "src", "toNode": "dst1"}],
    }

    canvas_a = {
        "nodes": base_canvas["nodes"],
        "edges": [{"id": "edge_1", "fromNode": "src", "toNode": "dst1"}],
    }

    # Branch B redirects edge_1 to dst2
    canvas_b = {
        "nodes": base_canvas["nodes"],
        "edges": [{"id": "edge_1", "fromNode": "src", "toNode": "dst2"}],
    }

    scorecard = synth.audit_concurrency(base_canvas, canvas_a, canvas_b)
    assert scorecard.structural_forks_count == 1
    assert any(c.conflict_type == ConflictType.STRUCTURAL_FORK for c in scorecard.conflicts)


def test_export_svg_radar(tmp_path):
    synth = WorkspaceConsensusSynthesizer()
    scorecard = ConsensusMergeScorecard(
        total_nodes_base=5,
        total_nodes_a=6,
        total_nodes_b=7,
        merged_nodes_count=8,
        clean_merges_count=6,
        semantic_divergences_count=1,
        spatial_collisions_count=1,
        structural_forks_count=0,
        consensus_stability_score=0.76,
    )

    out_file = tmp_path / "consensus_radar.svg"
    svg_str = synth.export_svg_consensus_radar(scorecard, str(out_file))

    assert out_file.exists()
    assert "<svg" in svg_str
    assert "</svg>" in svg_str
    assert "Workspace Consensus" in svg_str
    assert "Semantic Unity" in svg_str


def test_zero_em_dashes_enforcement():
    synth = WorkspaceConsensusSynthesizer()

    base = {"nodes": [{"id": "root", "text": "### Root Node\nFoundation"}], "edges": []}
    fork_a = {"nodes": [{"id": "root", "text": "### Root Node\nRefined by Agent A"}], "edges": []}
    fork_b = {"nodes": [{"id": "root", "text": "### Root Node\nRefined by Agent B"}], "edges": []}

    merged, scorecard = synth.synthesize_visual_merge(base, fork_a, fork_b)
    md_report = synth.generate_markdown_report(scorecard)
    svg_str = synth.export_svg_consensus_radar(scorecard)

    full_text = md_report + svg_str + json.dumps(merged) + json.dumps(scorecard.to_dict())
    assert chr(8212) not in full_text
    assert "\u2014" not in full_text
