"""
test_narrative_branch_reconciler.py - Unit tests for NarrativeBranchReconciler (Phase 109, Cycle 105).

Tests multiscale narrative branch tracking, Arthur path-dependent divergence fork detection,
Hegelian architectural bridge synthesis, SVG export, and zero em dashes.

Strict constraint: Strictly zero em dashes (Unicode U+2014) anywhere.
"""

from pathlib import Path
import pytest
from scripts.narrative_branch_reconciler import (
    BranchReconcilerResult,
    DivergencePoint,
    NarrativeBranch,
    NarrativeBranchReconciler,
    NarrativeWaypoint,
    ReconciliationBridge,
    ReconciliationTelemetry,
)


@pytest.fixture
def architectural_branches():
    return [
        {
            "id": "br_a",
            "name": "Branch Alpha: Monolithic Memory Store",
            "origin_id": "root_fork",
            "intent": "Maximize raw in-memory lookup performance",
            "terminal_state": "Zero-latency in-memory cache",
            "waypoints": [
                {
                    "id": "wp_a1",
                    "label": "Shared SharedArrayBuffer Pool",
                    "phase_order": 1,
                    "assumptions": ["Dedicated multi-core hardware available"],
                    "tradeoffs": {"latency": 0.05, "ram_usage": 0.85, "portability": 0.30},
                },
                {
                    "id": "wp_a2",
                    "label": "Direct Binary Pointer Dereference",
                    "phase_order": 2,
                    "assumptions": ["Static layout offsets remain unchanged"],
                    "tradeoffs": {"latency": 0.02, "ram_usage": 0.90, "portability": 0.20},
                },
            ],
        },
        {
            "id": "br_b",
            "name": "Branch Beta: Distributed Micro-Vaults",
            "origin_id": "root_fork",
            "intent": "Maximize multi-tenant isolation and fault tolerance",
            "terminal_state": "Decoupled immutable snapshot replicas",
            "waypoints": [
                {
                    "id": "wp_b1",
                    "label": "Ephemeral Local IndexedDB Clones",
                    "phase_order": 1,
                    "assumptions": ["Browser quota allows 50MB storage"],
                    "tradeoffs": {"latency": 0.45, "ram_usage": 0.20, "portability": 0.90},
                },
                {
                    "id": "wp_b2",
                    "label": "Event-Driven Sync Message Mesh",
                    "phase_order": 2,
                    "assumptions": ["Eventual consistency within 100ms"],
                    "tradeoffs": {"latency": 0.50, "ram_usage": 0.25, "portability": 0.95},
                },
            ],
        },
    ]


def test_empty_reconciler():
    reconciler = NarrativeBranchReconciler()
    res = reconciler.analyze_and_reconcile(raw_branches=[])

    assert isinstance(res, BranchReconcilerResult)
    assert res.telemetry.total_branches_tracked == 0
    assert res.telemetry.divergence_forks_detected == 0
    assert res.telemetry.reconciliation_bridges_synthesized == 0
    assert res.telemetry.cowan_bounded is True
    assert len(res.branches) == 0
    assert len(res.bridges) == 0
    assert res.svg_reconciliation_map == ""
    assert res.executive_synthesis_md == ""


def test_branch_tracking_and_divergence(architectural_branches):
    reconciler = NarrativeBranchReconciler(drift_threshold=0.30)
    res = reconciler.analyze_and_reconcile(raw_branches=architectural_branches)

    assert res.telemetry.total_branches_tracked == 2
    assert res.telemetry.total_waypoints_analyzed == 4
    assert res.telemetry.divergence_forks_detected == 1
    assert res.telemetry.reconciliation_bridges_synthesized == 1
    assert res.telemetry.mean_drift_distance > 0.40
    assert res.telemetry.systemic_convergence_ratio == 1.0
    assert res.telemetry.cowan_bounded is True

    # Validate divergence point
    fork = res.divergences[0]
    assert fork.bifurcation_origin_id == "root_fork"
    assert "br_a" in fork.divergent_branch_ids
    assert "br_b" in fork.divergent_branch_ids
    assert fork.divergence_severity in ["MODERATE", "CRITICAL"]

    # Validate bridge synthesis
    bridge = res.bridges[0]
    assert bridge.source_branch_id == "br_a"
    assert bridge.target_branch_id == "br_b"
    assert bridge.tradeoff_consensus_score > 0.65
    assert "Pareto-optimal" in bridge.unifying_strategy


def test_low_drift_no_unnecessary_bridge():
    # Two nearly identical branches sharing tradeoffs
    branches = [
        {
            "id": "b1",
            "name": "Standard Flow A",
            "origin_id": "root",
            "waypoints": [{"id": "w1", "tradeoffs": {"speed": 0.8, "cost": 0.5}}],
        },
        {
            "id": "b2",
            "name": "Standard Flow B",
            "origin_id": "root",
            "waypoints": [{"id": "w2", "tradeoffs": {"speed": 0.82, "cost": 0.48}}],
        },
    ]
    reconciler = NarrativeBranchReconciler(drift_threshold=0.45)
    res = reconciler.analyze_and_reconcile(raw_branches=branches)

    assert res.telemetry.divergence_forks_detected == 1
    assert res.divergences[0].divergence_severity == "LOW"
    assert res.telemetry.reconciliation_bridges_synthesized == 0  # Below drift threshold


def test_cowan_branch_bounding_exceeded():
    reconciler = NarrativeBranchReconciler(max_active_branches=3)
    branches = [
        {"id": f"br_{i}", "name": f"Branch {i}", "origin_id": "root", "waypoints": []}
        for i in range(5)
    ]
    res = reconciler.analyze_and_reconcile(raw_branches=branches)

    assert res.telemetry.total_branches_tracked == 5
    assert res.telemetry.cowan_bounded is False


def test_svg_export(tmp_path: Path, architectural_branches):
    reconciler = NarrativeBranchReconciler()
    res = reconciler.analyze_and_reconcile(raw_branches=architectural_branches)

    svg_file = tmp_path / "narrative_reconciliation.svg"
    svg_str = reconciler.export_svg(res, output_path=str(svg_file))

    assert "<svg" in svg_str
    assert "</svg>" in svg_str
    assert "Multiscale Narrative Branching" in svg_str
    assert svg_file.exists()
    assert svg_file.stat().st_size > 500


def test_ascii_report(architectural_branches):
    reconciler = NarrativeBranchReconciler()
    res = reconciler.analyze_and_reconcile(raw_branches=architectural_branches)
    report = reconciler.generate_ascii_report(res)

    assert "MULTISCALE NARRATIVE BRANCHING & RECONCILER" in report
    assert "Active Branches" in report
    assert "Divergence Forks" in report
    assert "[BRANCH] br_a" in report
    assert "[BRIDGE]" in report


def test_executive_synthesis_markdown(architectural_branches):
    reconciler = NarrativeBranchReconciler()
    res = reconciler.analyze_and_reconcile(raw_branches=architectural_branches)

    md = res.executive_synthesis_md
    assert "# Multiscale Narrative Branching & Divergence Reconciliation" in md
    assert "| Bridge ID | Conjoined Branches |" in md
    assert "Pareto-optimal" in md
    assert "Bifurcation Forks Detected:" in md


def test_zero_em_dashes():
    source_files = [
        Path("scripts/narrative_branch_reconciler.py"),
        Path("tests/test_narrative_branch_reconciler.py"),
    ]
    for p in source_files:
        if p.exists():
            text = p.read_text(encoding="utf-8")
            assert "\u2014" not in text, f"Em dash found in {p}"
