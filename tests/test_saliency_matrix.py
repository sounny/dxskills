"""Unit tests for Autonomous Cognitive Spatial Working Memory Saliency Decoupler & Attenuation Matrix.

Strict Quality Gate: Zero em dashes anywhere (use hyphens, commas, or parentheses).
"""

from __future__ import annotations

import json
from pathlib import Path
import pytest

from scripts.saliency_matrix import (
    AttenuationTier,
    SaliencyDecouplerMatrix,
    SaliencyMatrixTelemetry,
    SaliencyNode,
)


def test_empty_input_handling() -> None:
    """Ensure saliency matrix handles empty input gracefully without errors."""
    matrix = SaliencyDecouplerMatrix()
    nodes, telemetry = matrix.attenuate()

    assert len(nodes) == 0
    assert telemetry.total_nodes == 0
    assert telemetry.peripheral_noise_reduction_pct == 0.0
    assert telemetry.focal_saliency_boost == 1.0


def test_focal_node_attenuation_tiers() -> None:
    """Verify concentric tier assignment radiating from selected focal locus."""
    matrix = SaliencyDecouplerMatrix(decay_rate=0.002, hop_penalty=0.20)
    data = {
        "nodes": {
            "node_focal": {"title": "Active Kernel", "x": 100.0, "y": 100.0, "dependencies": ["node_near"]},
            "node_near": {"title": "Near Neighbor", "x": 180.0, "y": 140.0, "dependencies": ["node_mid"]},
            "node_mid": {"title": "Mid Peripheral", "x": 500.0, "y": 450.0, "dependencies": ["node_far"]},
            "node_far": {"title": "Distant Background", "x": 1400.0, "y": 1200.0, "dependencies": []},
        }
    }
    matrix.load_dict(data)
    nodes, telemetry = matrix.attenuate(focal_node_id="node_focal")

    assert len(nodes) == 4
    node_map = {n.node_id: n for n in nodes}

    # Focal node must have opacity 1.0 and FOCAL_LOCUS tier
    focal = node_map["node_focal"]
    assert focal.tier == AttenuationTier.FOCAL_LOCUS
    assert focal.opacity == 1.0
    assert focal.distance_from_focus == 0.0

    # Near neighbor must have higher opacity than distant background
    near = node_map["node_near"]
    far = node_map["node_far"]
    assert near.opacity > far.opacity
    assert near.contrast_ratio > far.contrast_ratio
    assert far.tier in [AttenuationTier.PERIPHERAL_REF, AttenuationTier.BACKGROUND_CHATTER]

    # Telemetry verification
    assert telemetry.peripheral_noise_reduction_pct > 10.0
    assert telemetry.focal_saliency_boost > 1.0


def test_exponential_decay_distance() -> None:
    """Verify opacity decreases monotonically as Euclidean distance increases."""
    matrix = SaliencyDecouplerMatrix(decay_rate=0.001, hop_penalty=0.10)
    data = {
        "nodes": {
            "center": {"title": "Center", "x": 0.0, "y": 0.0, "dependencies": ["ring_1"]},
            "ring_1": {"title": "Ring 1", "x": 120.0, "y": 0.0, "dependencies": ["ring_2"]},
            "ring_2": {"title": "Ring 2", "x": 300.0, "y": 0.0, "dependencies": ["ring_3"]},
            "ring_3": {"title": "Ring 3", "x": 600.0, "y": 0.0, "dependencies": []},
        }
    }
    matrix.load_dict(data)
    nodes, telemetry = matrix.attenuate(focal_node_id="center")

    node_map = {n.node_id: n for n in nodes}
    assert node_map["center"].opacity > node_map["ring_1"].opacity
    assert node_map["ring_1"].opacity > node_map["ring_2"].opacity
    assert node_map["ring_2"].opacity > node_map["ring_3"].opacity


def test_canvas_export(tmp_path: Path) -> None:
    """Verify export to Obsidian .canvas file with attenuation tier badges."""
    matrix = SaliencyDecouplerMatrix()
    data = {
        "nodes": {
            "a": {"title": "Task Alpha", "x": 100, "y": 100},
            "b": {"title": "Task Beta", "x": 800, "y": 800},
        }
    }
    matrix.load_dict(data)

    out_file = str(tmp_path / "attenuated.canvas")
    res = matrix.to_canvas(focal_node_id="a", output_path=out_file, canvas_title="Focus Mode")

    assert Path(out_file).exists()
    assert "nodes" in res
    assert len(res["nodes"]) == 2

    # Node A is focal (cyan / 5), Node B is peripheral/background (dim / 0 or 3)
    node_a = next(n for n in res["nodes"] if n["id"] == "a")
    node_b = next(n for n in res["nodes"] if n["id"] == "b")
    assert node_a["color"] == "5"
    assert "ACTIVE FOCAL LOCUS" in node_a["text"]
    assert "Saliency Tier:" in node_b["text"]


def test_svg_export(tmp_path: Path) -> None:
    """Verify publication-grade SVG generation with spotlight gradients."""
    matrix = SaliencyDecouplerMatrix()
    data = {
        "c": {"title": "Core Hub", "x": 300, "y": 250},
        "p": {"title": "Peripheral Spec", "x": 850, "y": 600},
    }
    matrix.load_dict(data)

    out_file = str(tmp_path / "saliency_matrix.svg")
    svg_str = matrix.to_svg(focal_node_id="c", output_path=out_file, width=1200, height=800)

    assert Path(out_file).exists()
    assert "<svg" in svg_str
    assert "</svg>" in svg_str
    assert "#0B0F17" in svg_str
    assert "focalSpotlight" in svg_str
    assert "Saliency Decoupler Metrics" in svg_str


def test_ascii_report() -> None:
    """Verify terminal ASCII summary generation."""
    matrix = SaliencyDecouplerMatrix()
    data = {
        "n1": {"title": "Focal Anchor", "x": 100, "y": 100},
        "n2": {"title": "Side Note", "x": 600, "y": 500},
    }
    matrix.load_dict(data)
    nodes, telemetry = matrix.attenuate(focal_node_id="n1")
    report = matrix.render_ascii_matrix(telemetry)

    assert "Spatial Working Memory Saliency Decoupler & Attenuation Matrix" in report
    assert "Total Canvas Nodes:" in report
    assert "Focal Saliency Boost:" in report
    assert "Focal Anchor" in report


def test_zero_em_dashes_in_module() -> None:
    """Verify neither script nor test contains em dashes."""
    root_dir = Path(__file__).parent.parent
    script_path = root_dir / "scripts" / "saliency_matrix.py"
    test_path = root_dir / "tests" / "test_saliency_matrix.py"

    for p in [script_path, test_path]:
        content = p.read_text(encoding="utf-8")
        assert "\u2014" not in content, f"Em dash found in {p.name}"
