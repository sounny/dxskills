"""
Unit tests for SocraticCrossExaminer in DxSkills.

Enforces zero em dash compliance and validates architectural rigor scoring,
Socratic probe generation, canvas export, and SVG radar rendering.
"""

import json
from pathlib import Path
import pytest

from scripts.socratic_cross_examiner import (
    ExaminationScorecard,
    SocraticCrossExaminer,
    SocraticProbe,
)


def test_empty_components_examination():
    examiner = SocraticCrossExaminer()
    scorecard = examiner.cross_examine_architecture("Empty Arch", [])

    assert isinstance(scorecard, ExaminationScorecard)
    assert scorecard.architectural_rigor_score <= 30.0
    assert "Deficient" in scorecard.verdict
    assert len(scorecard.probes) >= 2


def test_hardened_vs_fragile_architecture():
    examiner = SocraticCrossExaminer()

    # Hardened system: 4 components, all tested, failover enabled, stateless
    hardened_comps = [
        {"name": "Edge Gateway", "has_tests": True, "has_failover": True, "is_stateless": True},
        {"name": "Raft Consensus Core", "has_tests": True, "has_failover": True, "is_stateless": False},
        {"name": "Query Worker", "has_tests": True, "has_failover": True, "is_stateless": True},
        {"name": "Metrics Scraper", "has_tests": True, "has_failover": True, "is_stateless": True},
    ]
    hardened = examiner.cross_examine_architecture("Hardened Core", hardened_comps)
    assert hardened.architectural_rigor_score >= 80.0
    assert hardened.falsifiability_score == 10.0
    assert hardened.failure_mode_score == 10.0
    assert "Hardened" in hardened.verdict

    # Fragile system: 4 components, zero tests, zero failovers, stateful
    fragile_comps = [
        {"name": "Single Database Master", "has_tests": False, "has_failover": False, "is_stateless": False},
        {"name": "Monolithic Backend", "has_tests": False, "has_failover": False, "is_stateless": False},
        {"name": "Direct Memory Ring", "has_tests": False, "has_failover": False, "is_stateless": False},
    ]
    fragile = examiner.cross_examine_architecture("Fragile Monolith", fragile_comps)
    assert fragile.architectural_rigor_score < 40.0
    assert fragile.falsifiability_score == 1.0
    assert fragile.failure_mode_score == 1.0
    assert "Fragile" in fragile.verdict or "Vulnerable" in fragile.verdict


def test_canvas_export(tmp_path: Path):
    examiner = SocraticCrossExaminer()
    comps = [
        {"name": "Auth Proxy", "has_tests": True, "has_failover": False, "is_stateless": True},
        {"name": "Storage Node", "has_tests": False, "has_failover": False, "is_stateless": False},
    ]
    scorecard = examiner.cross_examine_architecture("Hybrid Cluster", comps)
    out_file = tmp_path / "test_socratic.canvas"

    canvas_data = examiner.export_canvas(scorecard, output_path=str(out_file))
    assert out_file.exists()

    assert "nodes" in canvas_data
    assert "edges" in canvas_data
    assert len(canvas_data["nodes"]) >= 3
    assert len(canvas_data["edges"]) >= 2


def test_svg_radar():
    examiner = SocraticCrossExaminer()
    comps = [
        {"name": "Ingestion Pipeline", "has_tests": True, "has_failover": True, "is_stateless": True},
    ]
    scorecard = examiner.cross_examine_architecture("Ingest Engine", comps)
    svg = examiner.export_svg_radar(scorecard, width=600, height=400)

    assert "<svg" in svg
    assert "</svg>" in svg
    assert "Socratic Cross-Examiner" in svg
    assert "Boundary" in svg
    assert "Falsify" in svg


def test_markdown_summary():
    examiner = SocraticCrossExaminer()
    comps = [
        {"name": "Sync Broker", "has_tests": True, "has_failover": False, "is_stateless": True},
    ]
    scorecard = examiner.cross_examine_architecture("Broker Service", comps)
    md = examiner.export_summary_markdown(scorecard)

    assert "# Socratic Architectural Cross-Examination" in md
    assert "Broker Service" in md
    assert "Active Socratic Interrogation Probes" in md
    assert "Zero phonological friction" in md


def test_zero_em_dash_compliance():
    """Verify that no em dashes exist anywhere in the code, tests, or generated outputs."""
    em_dash = chr(8212)

    src_path = Path("scripts/socratic_cross_examiner.py")
    if src_path.exists():
        content = src_path.read_text(encoding="utf-8")
        assert em_dash not in content, "Found em dash in scripts/socratic_cross_examiner.py"

    examiner = SocraticCrossExaminer()
    comps = [
        {"name": "Module Alpha", "has_tests": False, "has_failover": False, "is_stateless": False},
        {"name": "Module Beta", "has_tests": True, "has_failover": False, "is_stateless": True},
    ]
    scorecard = examiner.cross_examine_architecture("Complex Topology", comps)

    md = examiner.export_summary_markdown(scorecard)
    assert em_dash not in md, "Found em dash in markdown summary"

    svg = examiner.export_svg_radar(scorecard)
    assert em_dash not in svg, "Found em dash in SVG radar"

    canvas_dict = examiner.export_canvas(scorecard, output_path="")
    canvas_str = json.dumps(canvas_dict)
    assert em_dash not in canvas_str, "Found em dash in canvas JSON"
