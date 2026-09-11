"""
Unit tests for MetacognitiveReflector in DxSkills.

Enforces zero em dash compliance and validates cognitive blindspot detection,
perspective lens synthesis, canvas export, and SVG radar generation.
"""

import json
from pathlib import Path
import pytest

from scripts.metacognitive_reflector import (
    BlindspotAssessment,
    MetacognitiveReflector,
    PerspectiveLens,
)


def test_empty_thesis_assessment():
    reflector = MetacognitiveReflector()
    assessment = reflector.assess_thesis("Empty Architecture", [])

    assert isinstance(assessment, BlindspotAssessment)
    assert assessment.total_assumptions == 0
    assert assessment.unvalidated_count == 0
    assert assessment.fixation_risk_score <= 35.0
    assert len(assessment.lenses) >= 2


def test_grounded_vs_fragile_thesis():
    reflector = MetacognitiveReflector()

    # Grounded: 4 assumptions, all validated, 4 perspectives
    grounded_assumptions = [
        {"label": "Network Latency", "validated": True},
        {"label": "Storage Sharding", "validated": True},
        {"label": "State Recovery", "validated": True},
        {"label": "Failover SLA", "validated": True},
    ]
    grounded = reflector.assess_thesis("Grounded System", grounded_assumptions, perspective_breadth=4)
    assert grounded.unvalidated_count == 0
    assert grounded.fixation_risk_score < 40.0
    assert grounded.dialectical_resilience_score > 65.0

    # Fragile: 5 assumptions, all unvalidated, monolithic perspective
    fragile_assumptions = [
        {"label": "Instant User Adoption", "validated": False},
        {"label": "Infinite Cloud Bandwidth", "validated": False},
        {"label": "Zero State Drift", "validated": False},
        {"label": "Infallible Master Node", "validated": False},
        {"label": "Zero Latency WAN", "validated": False},
    ]
    fragile = reflector.assess_thesis("Fragile Spec", fragile_assumptions, perspective_breadth=1)
    assert fragile.unvalidated_count == 5
    assert fragile.fixation_risk_score > 70.0
    assert fragile.confirmation_trap_index > 0.6
    assert "Critical Fragility" in fragile.status or "High Fixation" in fragile.status


def test_canvas_export(tmp_path: Path):
    reflector = MetacognitiveReflector()
    assumptions = [
        {"label": "Decentralized Raft Cluster", "validated": False},
        {"label": "Lock-Free Ring Buffer", "validated": True},
    ]
    assessment = reflector.assess_thesis("Raft Architecture", assumptions, perspective_breadth=2)
    out_file = tmp_path / "test_reflector.canvas"

    canvas_data = reflector.export_canvas(assessment, output_path=str(out_file))
    assert out_file.exists()

    assert "nodes" in canvas_data
    assert "edges" in canvas_data
    assert len(canvas_data["nodes"]) >= 5
    assert len(canvas_data["edges"]) >= 4


def test_svg_radar():
    reflector = MetacognitiveReflector()
    assumptions = [{"label": "Single Database Engine", "validated": False}]
    assessment = reflector.assess_thesis("Monolith", assumptions, perspective_breadth=1)

    svg = reflector.export_svg_radar(assessment, width=600, height=400)
    assert "<svg" in svg
    assert "</svg>" in svg
    assert "Metacognitive Reflector" in svg
    assert "Monolith" in svg
    assert "Inversion" in svg


def test_markdown_summary():
    reflector = MetacognitiveReflector()
    assumptions = [
        {"label": "Global Lock Consistency", "validated": False},
        {"label": "Infinite Cache RAM", "validated": False},
    ]
    assessment = reflector.assess_thesis("Distributed Cache", assumptions, perspective_breadth=2)
    md = reflector.export_summary_markdown(assessment)

    assert "# Metacognitive Reflector and Bias Audit" in md
    assert "Distributed Cache" in md
    assert "Dialectical Counter-Perspectives" in md
    assert "Zero phonological friction" in md


def test_zero_em_dash_compliance():
    """Verify that no em dashes exist anywhere in the code, tests, or generated outputs."""
    em_dash = chr(8212)

    # Check source file
    src_path = Path("scripts/metacognitive_reflector.py")
    if src_path.exists():
        content = src_path.read_text(encoding="utf-8")
        assert em_dash not in content, "Found em dash in scripts/metacognitive_reflector.py"

    reflector = MetacognitiveReflector()
    assumptions = [
        {"label": "Unproven Cloud Scale", "validated": False},
        {"label": "Synchronous RPC Chain", "validated": False},
    ]
    assessment = reflector.assess_thesis("Microservice Mesh", assumptions, perspective_breadth=1)

    md = reflector.export_summary_markdown(assessment)
    assert em_dash not in md, "Found em dash in markdown report"

    svg = reflector.export_svg_radar(assessment)
    assert em_dash not in svg, "Found em dash in SVG visualizer"

    canvas_dict = reflector.export_canvas(assessment, output_path="")
    canvas_str = json.dumps(canvas_dict)
    assert em_dash not in canvas_str, "Found em dash in canvas JSON"
