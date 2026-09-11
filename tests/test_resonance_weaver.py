"""Unit tests for Autonomous Cognitive Spatial Bi-Directional Hyper-Link Resonance Weaver.

Strict Quality Gate: Zero em dashes anywhere (use hyphens, commas, or parentheses).
"""

from __future__ import annotations

import json
from pathlib import Path
import pytest

from scripts.resonance_weaver import (
    HyperLinkResonanceWeaver,
    ResonanceBridge,
    ResonanceCategory,
    ResonanceWeaverTelemetry,
)


def test_empty_input_handling() -> None:
    """Ensure resonance weaver handles empty input gracefully without errors."""
    weaver = HyperLinkResonanceWeaver()
    bridges, telemetry = weaver.weave_bridges()

    assert len(bridges) == 0
    assert telemetry.total_nodes == 0
    assert telemetry.discovered_bridges_count == 0
    assert telemetry.mean_resonance_intensity == 0.0
    assert telemetry.associative_density_lift_pct == 0.0


def test_semantic_affinity_and_bridge_discovery() -> None:
    """Verify discovery of latent associative bridges based on shared semantic invariants."""
    weaver = HyperLinkResonanceWeaver(min_resonance_threshold=0.25)
    data = {
        "nodes": {
            "node_cache": {
                "title": "Redis Cache Tier",
                "text": "Distributed in-memory cache layer with TTL invalidation, eventual consistency, and eviction policies.",
            },
            "node_db": {
                "title": "Postgres Read Replica",
                "text": "Secondary database replica handling read queries with eventual consistency and cache invalidation stream.",
            },
            "node_unrelated": {
                "title": "CSS Design Tokens",
                "text": "Titanium dark mode typography variables, border radius, and box shadows.",
            },
        }
    }
    weaver.load_dict(data)
    bridges, telemetry = weaver.weave_bridges()

    assert len(bridges) >= 1
    b = bridges[0]
    pair_ids = {b.source_id, b.target_id}
    assert pair_ids == {"node_cache", "node_db"}
    assert b.resonance_score >= 0.25
    assert len(b.shared_concepts) >= 2
    assert "consistency" in b.shared_concepts or "invalidation" in b.shared_concepts
    assert telemetry.discovered_bridges_count >= 1


def test_existing_edge_filtering() -> None:
    """Verify that existing explicit edges are not redundantly rediscovered."""
    weaver = HyperLinkResonanceWeaver(min_resonance_threshold=0.20)
    data = {
        "nodes": {
            "n1": {"title": "Auth Service", "text": "OAuth2 tokens, verification, security policies."},
            "n2": {"title": "Token Vault", "text": "Cryptographic tokens, verification keys, security credentials."},
        },
        "edges": [
            {"fromNode": "n1", "toNode": "n2"},
        ],
    }
    weaver.load_dict(data)
    bridges, telemetry = weaver.weave_bridges()

    # Should not produce bridge for already-linked pair (n1, n2)
    assert len(bridges) == 0
    assert telemetry.discovered_bridges_count == 0
    assert telemetry.existing_edges_count == 1


def test_canvas_export(tmp_path: Path) -> None:
    """Verify export to Obsidian .canvas with resonance bridge edges."""
    weaver = HyperLinkResonanceWeaver(min_resonance_threshold=0.20)
    data = {
        "nodes": {
            "a": {"title": "Service A", "text": "High throughput microservice streaming metrics."},
            "b": {"title": "Service B", "text": "High throughput ingestion pipeline streaming events."},
        }
    }
    weaver.load_dict(data)

    out_file = str(tmp_path / "weaved.canvas")
    res = weaver.to_canvas(output_path=out_file, canvas_title="Associative Canvas")

    assert Path(out_file).exists()
    assert "nodes" in res
    assert "edges" in res
    assert len(res["nodes"]) == 2
    assert len(res["edges"]) == 1
    edge = res["edges"][0]
    assert "color" in edge
    assert "label" in edge


def test_svg_export(tmp_path: Path) -> None:
    """Verify publication-grade SVG generation with dark titanium styling."""
    weaver = HyperLinkResonanceWeaver(min_resonance_threshold=0.20)
    data = {
        "x": {"title": "Node X", "text": "Distributed consensus RAFT log replication protocol."},
        "y": {"title": "Node Y", "text": "Distributed transaction commit log replication Paxos."},
    }
    weaver.load_dict(data)

    out_file = str(tmp_path / "resonance_mesh.svg")
    svg_str = weaver.to_svg(output_path=out_file, width=1200, height=800)

    assert Path(out_file).exists()
    assert "<svg" in svg_str
    assert "</svg>" in svg_str
    assert "#0B0F17" in svg_str
    assert "Resonance Weaver Metrics" in svg_str
    assert "Node X" in svg_str


def test_ascii_report() -> None:
    """Verify terminal ASCII summary report output."""
    weaver = HyperLinkResonanceWeaver(min_resonance_threshold=0.20)
    data = {
        "p1": {"title": "Alpha Hub", "text": "Quantum computing simulation algorithms."},
        "p2": {"title": "Beta Hub", "text": "Quantum state vector simulation matrix."},
    }
    weaver.load_dict(data)
    bridges, telemetry = weaver.weave_bridges()
    report = weaver.render_ascii_bridges(telemetry)

    assert "Spatial Bi-Directional Hyper-Link Resonance Weaver Report" in report
    assert "Total Canvas Nodes:" in report
    assert "Alpha Hub" in report


def test_zero_em_dashes_in_module() -> None:
    """Verify neither script nor test contains em dashes."""
    root_dir = Path(__file__).parent.parent
    script_path = root_dir / "scripts" / "resonance_weaver.py"
    test_path = root_dir / "tests" / "test_resonance_weaver.py"

    for p in [script_path, test_path]:
        content = p.read_text(encoding="utf-8")
        assert "\u2014" not in content, f"Em dash found in {p.name}"
