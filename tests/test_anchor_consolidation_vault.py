"""
test_anchor_consolidation_vault.py - Unit tests for AnchorConsolidationVault (Phase 107, Cycle 103).

Tests Burgess allocentric spatial clustering, immutable SHA-256 snapshot creation,
working memory headroom recovery, sub-canvas rehydration, SVG export, and zero em dashes.

Strict constraint: Strictly zero em dashes (Unicode U+2014) anywhere.
"""

from pathlib import Path
import pytest
from scripts.anchor_consolidation_vault import (
    AnchorConsolidationVault,
    CanvasAnchor,
    SemanticSnapshot,
    SubCanvasCluster,
    VaultResult,
    VaultTelemetry,
)


@pytest.fixture
def architectural_canvas_anchors():
    return [
        # Sub-canvas A: High coherence layout engine
        {"id": "a1", "label": "Affine Viewport Matrix", "x": 100.0, "y": 120.0, "coherence_score": 0.88},
        {"id": "a2", "label": "Pinch-Zoom Transform", "x": 140.0, "y": 150.0, "coherence_score": 0.92},
        {"id": "a3", "label": "Foveal Focus Reticle", "x": 180.0, "y": 130.0, "coherence_score": 0.85},

        # Sub-canvas B: Saccadic contrast dampener
        {"id": "b1", "label": "Attentional Blink Detector", "x": 600.0, "y": 100.0, "coherence_score": 0.78},
        {"id": "b2", "label": "Eccentricity Attenuator", "x": 650.0, "y": 140.0, "coherence_score": 0.82},

        # Isolated anchor (Unconsolidated)
        {"id": "c1", "label": "Exploratory Thought Fragment", "x": 400.0, "y": 400.0, "coherence_score": 0.40},
    ]


@pytest.fixture
def canvas_connections():
    return [
        {"source": "a1", "target": "a2"},
        {"source": "a2", "target": "a3"},
        {"source": "b1", "target": "b2"},
    ]


def test_empty_vault():
    vault = AnchorConsolidationVault()
    result = vault.consolidate_subcanvases(raw_anchors=[])
    assert isinstance(result, VaultResult)
    assert result.telemetry.total_anchors_evaluated == 0
    assert result.telemetry.active_clusters_detected == 0
    assert result.telemetry.consolidated_snapshots_stored == 0
    assert result.telemetry.cowan_bounded is True
    assert len(result.anchors) == 0
    assert len(result.clusters) == 0
    assert len(result.snapshots) == 0
    assert result.svg_vault_map == ""
    assert result.rehydration_manifest_md == ""


def test_consolidation_and_snapshot_generation(architectural_canvas_anchors, canvas_connections):
    vault = AnchorConsolidationVault(coherence_threshold=0.65)
    result = vault.consolidate_subcanvases(
        raw_anchors=architectural_canvas_anchors,
        raw_connections=canvas_connections,
        cluster_proximity_radius=200.0,
    )

    assert result.telemetry.total_anchors_evaluated == 6
    assert result.telemetry.active_clusters_detected >= 3
    assert result.telemetry.consolidated_snapshots_stored == 2
    assert result.telemetry.working_memory_slots_freed == 3  # (3-1) + (2-1) = 3 slots
    assert result.telemetry.cowan_headroom_recovered == 3.0
    assert result.telemetry.net_compression_ratio_pct == 50.0
    assert result.telemetry.cowan_bounded is True

    # Validate snapshot structure
    s1, s2 = result.snapshots
    assert s1.snapshot_id.startswith("snap_")
    assert len(s1.content_hash) == 64  # SHA-256
    assert s1.rehydration_key.startswith("dx-rehydrate:")
    assert s1.compression_ratio_pct > 0.0
    assert len(s1.immutable_payload["anchors"]) >= 2


def test_snapshot_rehydration(architectural_canvas_anchors, canvas_connections):
    vault = AnchorConsolidationVault()
    result = vault.consolidate_subcanvases(
        raw_anchors=architectural_canvas_anchors,
        raw_connections=canvas_connections,
    )
    assert len(result.snapshots) >= 1
    snap = result.snapshots[0]

    # Rehydrate by snapshot_id
    payload = vault.rehydrate_snapshot(snap.snapshot_id, result)
    assert payload is not None
    assert payload["cluster_id"] == snap.cluster_id
    assert len(payload["anchors"]) == snap.anchors_count

    # Non-existent snapshot
    assert vault.rehydrate_snapshot("snap_invalid_999", result) is None


def test_coherence_threshold_filtering():
    vault = AnchorConsolidationVault(coherence_threshold=0.90)  # strict threshold
    anchors = [
        {"id": "n1", "label": "Node 1", "x": 100.0, "y": 100.0, "coherence_score": 0.70},
        {"id": "n2", "label": "Node 2", "x": 120.0, "y": 110.0, "coherence_score": 0.75},
    ]
    result = vault.consolidate_subcanvases(raw_anchors=anchors)
    assert result.telemetry.active_clusters_detected == 1
    assert result.telemetry.consolidated_snapshots_stored == 0  # Mean coherence 0.725 < 0.90
    assert result.clusters[0].is_consolidatable is False


def test_cowan_bounding_exceeded():
    vault = AnchorConsolidationVault(cowan_limit=2)
    # 5 isolated low-coherence anchors
    anchors = [
        {"id": f"iso_{i}", "label": f"Fragment {i}", "x": float(i * 400), "y": 100.0, "coherence_score": 0.30}
        for i in range(5)
    ]
    result = vault.consolidate_subcanvases(raw_anchors=anchors)
    assert result.telemetry.consolidated_snapshots_stored == 0
    assert result.telemetry.cowan_bounded is False  # 5 remaining > cowan_limit of 2


def test_svg_export(tmp_path: Path, architectural_canvas_anchors, canvas_connections):
    vault = AnchorConsolidationVault()
    result = vault.consolidate_subcanvases(
        raw_anchors=architectural_canvas_anchors,
        raw_connections=canvas_connections,
    )

    svg_file = tmp_path / "vault_map.svg"
    svg_str = vault.export_svg(result, output_path=str(svg_file))

    assert "<svg" in svg_str
    assert "</svg>" in svg_str
    assert "Working Memory Anchor Consolidation" in svg_str
    assert svg_file.exists()
    assert svg_file.stat().st_size > 500


def test_ascii_report(architectural_canvas_anchors, canvas_connections):
    vault = AnchorConsolidationVault()
    result = vault.consolidate_subcanvases(
        raw_anchors=architectural_canvas_anchors,
        raw_connections=canvas_connections,
    )
    report = vault.generate_ascii_report(result)

    assert "WORKING MEMORY ANCHOR CONSOLIDATION" in report
    assert "Total Anchors Indexed" in report
    assert "Headroom Recovered" in report
    assert "[VAULT]" in report


def test_rehydration_manifest_markdown(architectural_canvas_anchors, canvas_connections):
    vault = AnchorConsolidationVault()
    result = vault.consolidate_subcanvases(
        raw_anchors=architectural_canvas_anchors,
        raw_connections=canvas_connections,
    )

    md = result.rehydration_manifest_md
    assert "# Semantic Snapshot Rehydration Manifest" in md
    assert "| Snapshot ID | Cluster Name |" in md
    assert "dx-rehydrate:" in md
    assert "Cognitive Headroom Recovered" in md


def test_zero_em_dashes():
    source_files = [
        Path("scripts/anchor_consolidation_vault.py"),
        Path("tests/test_anchor_consolidation_vault.py"),
    ]
    for p in source_files:
        if p.exists():
            text = p.read_text(encoding="utf-8")
            assert "\u2014" not in text, f"Em dash found in {p}"
