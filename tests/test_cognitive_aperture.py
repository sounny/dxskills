"""Unit tests for Autonomous Cognitive Spatial Dynamic Cognitive Aperture & Scope Bounding Harness.

Strict Quality Gate: Zero em dashes anywhere (use hyphens, commas, or parentheses).
"""

from __future__ import annotations

import json
from pathlib import Path
import pytest

from scripts.cognitive_aperture import (
    CognitiveApertureHarness,
    SpatialEntity,
    ApertureTier,
    ApertureTelemetry,
)


def test_empty_entities_handling() -> None:
    """Ensure harness handles empty input gracefully."""
    harness = CognitiveApertureHarness()
    entities, telemetry = harness.calibrate_aperture()

    assert len(entities) == 0
    assert telemetry.total_entities == 0
    assert telemetry.focal_count == 0
    assert telemetry.working_memory_strain_index == 0.0
    assert telemetry.aperture_focus_efficiency_pct == 100.0


def test_cowan_four_slot_aperture_bounding() -> None:
    """Verify that active focal memory is strictly bounded to the 4-chunk Cowan limit."""
    harness = CognitiveApertureHarness(capacity_limit=4, max_peripheral_count=4)
    tasks = {
        f"task_{i}": {
            "title": f"Task {i}",
            "cognitive_weight": float(i % 10 + 1),
            "urgency_score": float(i) / 10.0,
            "strategic_alignment": 0.5,
        }
        for i in range(1, 11)
    }
    harness.load_dict(tasks)
    entities, telemetry = harness.calibrate_aperture()

    assert telemetry.total_entities == 10
    assert telemetry.capacity_limit == 4
    assert telemetry.focal_count == 4
    assert len(telemetry.focal_entities) == 4

    # High urgency tasks (10, 9, 8, 7) should be inside focal aperture
    focal_nodes = [e for e in entities if e.aperture_tier == ApertureTier.FOCAL]
    assert len(focal_nodes) == 4
    for node in focal_nodes:
        assert node.attenuation_factor == 0.0

    # Peripheral nodes must have progressive attenuation > 0
    peripheral_nodes = [e for e in entities if e.aperture_tier == ApertureTier.PERIPHERAL]
    for p in peripheral_nodes:
        assert p.attenuation_factor > 0.0

    # Telemetry strain and efficiency
    assert telemetry.working_memory_strain_index >= 0.0
    assert 0.0 <= telemetry.aperture_focus_efficiency_pct <= 100.0


def test_strategic_horizon_anchoring() -> None:
    """Verify that distant high-value architecture nodes are mapped to the horizon tier."""
    harness = CognitiveApertureHarness(capacity_limit=3, max_peripheral_count=3)
    tasks = {
        "tactical_1": {"title": "Fix critical bug", "urgency_score": 0.95, "strategic_alignment": 0.2},
        "tactical_2": {"title": "Write unit tests", "urgency_score": 0.90, "strategic_alignment": 0.3},
        "tactical_3": {"title": "CLI integration", "urgency_score": 0.85, "strategic_alignment": 0.4},
        "strategic_arch": {"title": "2030 Unified Core Spec", "urgency_score": 0.1, "strategic_alignment": 0.95},
        "minor_chores": {"title": "Clean temp logs", "urgency_score": 0.05, "strategic_alignment": 0.1},
    }
    harness.load_dict(tasks)
    entities, telemetry = harness.calibrate_aperture()

    entity_map = {e.entity_id: e for e in entities}
    assert entity_map["strategic_arch"].aperture_tier == ApertureTier.HORIZON
    assert telemetry.horizon_count >= 1


def test_manual_focal_override() -> None:
    """Verify manual pinning of entities into the focal aperture."""
    harness = CognitiveApertureHarness(capacity_limit=2)
    tasks = {
        "t1": {"title": "High Urgency 1", "urgency_score": 0.99},
        "t2": {"title": "High Urgency 2", "urgency_score": 0.98},
        "t3": {"title": "Low Urgency Pinned", "urgency_score": 0.10},
    }
    harness.load_dict(tasks)
    entities, telemetry = harness.calibrate_aperture(manual_focal_ids=["t3"])

    entity_map = {e.entity_id: e for e in entities}
    assert entity_map["t3"].aperture_tier == ApertureTier.FOCAL


def test_canvas_export(tmp_path: Path) -> None:
    """Verify Obsidian .canvas generation with tier tags and colors."""
    harness = CognitiveApertureHarness()
    tasks = {
        "n1": {"title": "Focus Node", "urgency_score": 0.9},
        "n2": {"title": "Background Node", "urgency_score": 0.2},
    }
    harness.load_dict(tasks)

    canvas_file = str(tmp_path / "aperture_test.canvas")
    canvas_dict = harness.to_canvas(canvas_file, canvas_title="Test Aperture")

    assert Path(canvas_file).exists()
    assert "nodes" in canvas_dict
    assert len(canvas_dict["nodes"]) == 2
    assert "IN-APERTURE FOCAL" in canvas_dict["nodes"][0]["text"] or "IN-APERTURE FOCAL" in canvas_dict["nodes"][1]["text"]


def test_svg_export(tmp_path: Path) -> None:
    """Verify SVG generation with concentric boundary rings."""
    harness = CognitiveApertureHarness()
    tasks = {
        "a": {"title": "Alpha Focus", "urgency_score": 0.95},
        "b": {"title": "Beta Peripheral", "urgency_score": 0.60},
        "c": {"title": "Gamma Horizon", "strategic_alignment": 0.95, "urgency_score": 0.1},
    }
    harness.load_dict(tasks)

    svg_file = str(tmp_path / "aperture_test.svg")
    svg_str = harness.to_svg(svg_file, width=1000, height=700)

    assert Path(svg_file).exists()
    assert "<svg" in svg_str
    assert "</svg>" in svg_str
    assert "Focal Aperture" in svg_str
    assert "Peripheral Attenuation Ring" in svg_str
    assert "Strategic Horizon Ring" in svg_str
    assert "#0B0F17" in svg_str


def test_zero_em_dashes_in_module() -> None:
    """Verify neither script nor test contains em dashes."""
    root_dir = Path(__file__).parent.parent
    script_path = root_dir / "scripts" / "cognitive_aperture.py"
    test_path = root_dir / "tests" / "test_cognitive_aperture.py"

    for p in [script_path, test_path]:
        content = p.read_text(encoding="utf-8")
        assert "\u2014" not in content, f"Em dash found in {p.name}"
