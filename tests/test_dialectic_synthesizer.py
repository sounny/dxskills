"""Unit tests for Autonomous Cognitive Spatial Associative Multi-Perspective Dialectic Synthesizer & Synthesis Mesh.

Strict Quality Gate: Zero em dashes anywhere (use hyphens, commas, or parentheses).
"""

from __future__ import annotations

import json
from pathlib import Path
import pytest

from scripts.dialectic_synthesizer import (
    DialecticSynthesizer,
    PolarityPole,
    DialecticTension,
    SyntheticResolution,
    ResolutionStrategy,
    SynthesisMeshTelemetry,
)


def test_empty_input_handling() -> None:
    """Ensure synthesizer handles empty input gracefully without errors."""
    synthesizer = DialecticSynthesizer()
    tensions, syntheses, telemetry = synthesizer.analyze_mesh()

    assert len(tensions) == 0
    assert len(syntheses) == 0
    assert telemetry.total_poles == 0
    assert telemetry.dialectical_harmony_score == 1.0


def test_dialectic_tension_detection() -> None:
    """Verify detection of structural polarities and competing value divergence."""
    synthesizer = DialecticSynthesizer()
    polarity_data = {
        "poles": {
            "pole_speed": {
                "name": "Extreme Latency Optimization",
                "core_values": ["speed", "low_latency", "in_memory"],
                "strengths": ["sub_millisecond_response", "high_concurrency"],
                "overuse_vulnerabilities": ["memory_exhaustion", "data_loss_on_crash"],
            },
            "pole_consistency": {
                "name": "Strict Transactional Consistency",
                "core_values": ["durability", "acid_guarantees", "write_verification"],
                "strengths": ["zero_loss", "audit_traceability"],
                "overuse_vulnerabilities": ["disk_write_bottlenecks", "elevated_latency"],
            },
        },
        "tensions": [["pole_speed", "pole_consistency"]],
    }
    synthesizer.load_dict(polarity_data)
    tensions, syntheses, telemetry = synthesizer.analyze_mesh()

    assert len(tensions) == 1
    t = tensions[0]
    assert t.thesis.pole_id == "pole_speed"
    assert t.antithesis.pole_id == "pole_consistency"
    assert t.tension_intensity >= 0.35
    assert t.oscillation_risk >= 0.20
    assert len(t.competing_attributes) > 0


def test_third_way_synthetic_resolution_generation() -> None:
    """Verify synthesis strategy selection and decoupling mechanism synthesis."""
    synthesizer = DialecticSynthesizer()
    polarity_data = {
        "poles": {
            "pole_sec": {
                "name": "Zero Trust Security",
                "core_values": ["security", "isolation", "strict_auth"],
                "strengths": ["perimeter_defense", "confidentiality"],
            },
            "pole_dev_speed": {
                "name": "Frictionless Developer Experience",
                "core_values": ["speed", "access", "agility"],
                "strengths": ["rapid_iteration", "developer_autonomy"],
            },
        },
        "tensions": [["pole_sec", "pole_dev_speed"]],
    }
    synthesizer.load_dict(polarity_data)
    tensions, syntheses, telemetry = synthesizer.analyze_mesh()

    assert len(syntheses) == 1
    s = syntheses[0]
    assert s.strategy in [
        ResolutionStrategy.DUAL_PLANE_ISOLATION,
        ResolutionStrategy.ORTHOGONAL_ABSTRACTION,
        ResolutionStrategy.TEMPORAL_DECOUPLING,
        ResolutionStrategy.HIERARCHICAL_TIERING,
        ResolutionStrategy.ADAPTIVE_EQUILIBRIUM,
    ]
    assert s.synthesis_rigor_score >= 0.70
    assert len(s.mechanisms) >= 2
    assert len(s.integrative_insight) > 10


def test_canvas_export(tmp_path: Path) -> None:
    """Verify Obsidian .canvas structure for triadic clusters."""
    synthesizer = DialecticSynthesizer()
    polarity_data = {
        "poles": {
            "pole_central": {"name": "Central Governance", "core_values": ["central", "standardization"]},
            "pole_local": {"name": "Local Agility", "core_values": ["local", "distributed"]},
        },
        "tensions": [["pole_central", "pole_local"]],
    }
    synthesizer.load_dict(polarity_data)

    canvas_file = str(tmp_path / "dialectic_mesh.canvas")
    canvas_dict = synthesizer.to_canvas(canvas_file, canvas_title="Dialectic Triad")

    assert Path(canvas_file).exists()
    assert "nodes" in canvas_dict
    assert "edges" in canvas_dict
    assert len(canvas_dict["nodes"]) == 3  # Thesis, Antithesis, Synthesis
    assert len(canvas_dict["edges"]) == 3  # Tension edge + 2 convergence edges


def test_svg_export(tmp_path: Path) -> None:
    """Verify publication-grade SVG triad generation."""
    synthesizer = DialecticSynthesizer()
    polarity_data = {
        "poles": {
            "p1": {"name": "Static Strictness", "core_values": ["static", "guaranteed"]},
            "p2": {"name": "Dynamic Adaptability", "core_values": ["dynamic", "flex"]},
        },
        "tensions": [["p1", "p2"]],
    }
    synthesizer.load_dict(polarity_data)

    svg_file = str(tmp_path / "dialectic_mesh.svg")
    svg_str = synthesizer.to_svg(svg_file, width=1000, height=700)

    assert Path(svg_file).exists()
    assert "<svg" in svg_str
    assert "</svg>" in svg_str
    assert "THESIS:" in svg_str
    assert "ANTITHESIS:" in svg_str
    assert "SYNTHESIS (Aufhebung)" in svg_str
    assert "#0B0F17" in svg_str


def test_zero_em_dashes_in_module() -> None:
    """Verify neither script nor test contains em dashes."""
    root_dir = Path(__file__).parent.parent
    script_path = root_dir / "scripts" / "dialectic_synthesizer.py"
    test_path = root_dir / "tests" / "test_dialectic_synthesizer.py"

    for p in [script_path, test_path]:
        content = p.read_text(encoding="utf-8")
        assert "\u2014" not in content, f"Em dash found in {p.name}"
