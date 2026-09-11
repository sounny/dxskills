"""
Unit tests for Bifurcation Radar & Path-Dependency Loom.
Strict rule: Zero em dashes across all code, docstrings, and tests.
"""

import pytest
import math
from scripts.bifurcation_radar import (
    BifurcationDecision,
    BifurcationFork,
    MultiverseTelemetry,
    BifurcationRadarLoom,
    sample_bifurcation_forks,
)


def test_decision_commitment_weight():
    """Verifies commitment weight calculation under reversible and irreversible constraints."""
    d_rev = BifurcationDecision("d1", "Reversible Step", "primary", 1, complexity=5.0, downstream_deps=2, reversible=True)
    # 5.0 * (1.0 + 0.3 * 2) * 1.0 = 5.0 * 1.6 = 8.0
    assert math.isclose(d_rev.commitment_weight, 8.0, abs_tol=0.01)

    d_irrev = BifurcationDecision("d2", "Irreversible Step", "primary", 1, complexity=5.0, downstream_deps=2, reversible=False)
    # 5.0 * (1.0 + 0.3 * 2) * 2.0 = 5.0 * 1.6 * 2 = 16.0
    assert math.isclose(d_irrev.commitment_weight, 16.0, abs_tol=0.01)


def test_evaluate_fork_empty_decisions():
    """Verifies that an empty fork remains fluid with zero switching friction."""
    fork = BifurcationFork("f_empty", "Empty Fork", "Root", "primary", ["alt1"])
    loom = BifurcationRadarLoom(s_threshold=100.0)
    res = loom.evaluate_fork(fork)

    assert res.lock_in_score == 0.0
    assert res.switching_cost == 0.0
    assert res.status == "fluid"


def test_evaluate_fork_lock_in_progression():
    """Verifies that cumulative decisions increase lock-in score and escalate status."""
    loom = BifurcationRadarLoom(s_threshold=50.0, coupling_lambda=0.2)
    fork = BifurcationFork("f1", "Storage Choice", "DB", "primary", ["alt"])

    # Step 1: Small decision -> fluid
    fork.decisions.append(BifurcationDecision("d1", "Initial Config", "primary", 1, complexity=3.0, downstream_deps=1, reversible=True))
    res1 = loom.evaluate_fork(fork)
    assert res1.lock_in_score < 0.40
    assert res1.status == "fluid"

    # Step 2: Major irreversible decisions -> soft_lock or hard_lock
    fork.decisions.append(BifurcationDecision("d2", "Proprietary Engine", "primary", 2, complexity=15.0, downstream_deps=5, reversible=False))
    fork.decisions.append(BifurcationDecision("d3", "Deep Schema Integration", "primary", 3, complexity=12.0, downstream_deps=4, reversible=False))
    res2 = loom.evaluate_fork(fork)
    assert res2.lock_in_score >= 0.75
    assert res2.status == "hard_lock"
    assert res2.switching_cost > 50.0


def test_evaluate_multiverse_empty():
    """Verifies graceful handling of empty forks list."""
    loom = BifurcationRadarLoom()
    telemetry = loom.evaluate_multiverse([])

    assert telemetry.total_forks == 0
    assert telemetry.total_decisions == 0
    assert telemetry.mean_lock_in_score == 0.0
    assert telemetry.primary_status == "fluid"


def test_evaluate_multiverse_aggregation():
    """Verifies aggregated metrics across multiple forks."""
    forks = sample_bifurcation_forks()
    loom = BifurcationRadarLoom(s_threshold=100.0)
    telemetry = loom.evaluate_multiverse(forks)

    assert telemetry.total_forks == 3
    assert telemetry.total_decisions == 7
    assert telemetry.mean_lock_in_score > 0.0
    assert telemetry.max_lock_in_score > 0.0
    assert telemetry.total_switching_cost > 0.0
    assert len(telemetry.forks) == 3


def test_counterfactual_entropy():
    """Verifies entropy calculation across alternative branching paths."""
    forks = sample_bifurcation_forks()
    loom = BifurcationRadarLoom()
    telemetry = loom.evaluate_multiverse(forks)

    assert telemetry.counterfactual_entropy >= 0.0
    assert isinstance(telemetry.counterfactual_entropy, float)


def test_generate_svg_structure():
    """Verifies dark titanium SVG diagram generation with active and ghost splines."""
    forks = sample_bifurcation_forks()
    loom = BifurcationRadarLoom()
    telemetry = loom.evaluate_multiverse(forks)
    svg = loom.generate_svg(telemetry, width=900, height=550)

    assert "<svg" in svg
    assert "</svg>" in svg
    assert "#09090b" in svg
    assert "Active Timeline" in svg
    assert "Counterfactual Ghost" in svg
    assert "track-fork-backend" in svg
    assert "event_sourcing" in svg


def test_generate_markdown_report():
    """Verifies publication-ready markdown compliance audit."""
    forks = sample_bifurcation_forks()
    loom = BifurcationRadarLoom()
    telemetry = loom.evaluate_multiverse(forks)
    report = loom.generate_markdown_report(telemetry)

    assert "# Multiverse Bifurcation Radar and Path-Dependency Audit" in report
    assert "Arthur Increasing Returns" in report
    assert "| `fork-backend` |" in report
    assert chr(8212) not in report
