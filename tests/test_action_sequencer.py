"""Unit tests for Autonomous Cognitive Spatial Non-Linear Executive Scaffolding & Action Sequencer.

Strict Quality Gate: Zero em dashes anywhere (use hyphens, commas, or parentheses).
"""

from __future__ import annotations

import json
from pathlib import Path
import pytest

from scripts.action_sequencer import (
    ActionSequencer,
    ActionNode,
    TaskStatus,
    MicroSteppingStone,
    SequencingTelemetry,
)


def test_empty_tasks_handling() -> None:
    """Ensure sequencer handles empty task sets without crashing."""
    sequencer = ActionSequencer()
    nodes, telemetry = sequencer.sequence()

    assert len(nodes) == 0
    assert telemetry.total_nodes == 0
    assert telemetry.critical_path_duration_minutes == 0
    assert telemetry.immediately_executable_count == 0


def test_topological_dag_and_critical_path() -> None:
    """Verify Kahn topological sort and Critical Path Method forward/backward pass."""
    sequencer = ActionSequencer()
    # Diamond graph:
    # A (20m) -> B (30m) -> D (10m)
    # A (20m) -> C (15m) -> D (10m)
    # Critical path should be A -> B -> D with total duration 20 + 30 + 10 = 60m
    tasks = {
        "task_a": {"title": "Problem Scoping", "estimated_minutes": 20, "prerequisites": []},
        "task_b": {"title": "Core Engine Architecture", "estimated_minutes": 30, "prerequisites": ["task_a"]},
        "task_c": {"title": "Auxiliary CLI Stubs", "estimated_minutes": 15, "prerequisites": ["task_a"]},
        "task_d": {"title": "Integration Testing", "estimated_minutes": 10, "prerequisites": ["task_b", "task_c"]},
    }
    sequencer.load_dict(tasks)
    nodes, telemetry = sequencer.sequence()

    assert len(nodes) == 4
    assert telemetry.total_nodes == 4
    assert telemetry.total_dependencies == 4
    assert telemetry.critical_path_duration_minutes == 60
    assert telemetry.critical_path_node_count == 3

    node_map = {n.node_id: n for n in nodes}

    # Task A must come before B, C, D
    assert node_map["task_a"].topological_order < node_map["task_b"].topological_order
    assert node_map["task_a"].topological_order < node_map["task_c"].topological_order
    assert node_map["task_b"].topological_order < node_map["task_d"].topological_order
    assert node_map["task_c"].topological_order < node_map["task_d"].topological_order

    # Critical path flags
    assert node_map["task_a"].is_critical_path is True
    assert node_map["task_b"].is_critical_path is True
    assert node_map["task_d"].is_critical_path is True
    assert node_map["task_c"].is_critical_path is False
    assert node_map["task_c"].slack_minutes == 15  # 30m - 15m = 15m slack

    # Initial status
    assert node_map["task_a"].status == TaskStatus.READY
    assert node_map["task_b"].status == TaskStatus.BLOCKED


def test_micro_commitment_stepping_stones() -> None:
    """Verify sub-2-minute micro-commitment synthesis and implementation intentions."""
    sequencer = ActionSequencer()
    tasks = {
        "doc_write": {"title": "Write Technical Monograph", "estimated_minutes": 60, "prerequisites": []},
    }
    sequencer.load_dict(tasks)
    nodes, telemetry = sequencer.sequence()

    task = nodes[0]
    assert len(task.stepping_stones) == 3
    for stone in task.stepping_stones:
        assert stone.target_duration_seconds <= 120
        assert "When" in stone.implementation_intention
        assert len(stone.sensory_anchor) > 5


def test_canvas_export(tmp_path: Path) -> None:
    """Verify Obsidian .canvas structure and stepping stone checklists."""
    sequencer = ActionSequencer()
    tasks = {
        "step_1": {"title": "Setup", "estimated_minutes": 10, "prerequisites": []},
        "step_2": {"title": "Execute", "estimated_minutes": 25, "prerequisites": ["step_1"]},
    }
    sequencer.load_dict(tasks)

    canvas_file = str(tmp_path / "action_runway.canvas")
    canvas_dict = sequencer.to_canvas(canvas_file, canvas_title="Execution Runway")

    assert Path(canvas_file).exists()
    assert len(canvas_dict["nodes"]) == 2
    assert len(canvas_dict["edges"]) == 1

    # Check checklist in text
    node_text = canvas_dict["nodes"][0]["text"]
    assert "Dysfunction Bypass Stepping Stones:" in node_text
    assert "- [ ] `45s`:" in node_text


def test_svg_export(tmp_path: Path) -> None:
    """Verify publication-grade SVG DAG generation."""
    sequencer = ActionSequencer()
    tasks = {
        "step_1": {"title": "Init", "estimated_minutes": 10, "prerequisites": []},
        "step_2": {"title": "Build", "estimated_minutes": 20, "prerequisites": ["step_1"]},
    }
    sequencer.load_dict(tasks)

    svg_file = str(tmp_path / "action_runway.svg")
    svg_str = sequencer.to_svg(svg_file, width=1000, height=600)

    assert Path(svg_file).exists()
    assert "<svg" in svg_str
    assert "</svg>" in svg_str
    assert "Executive Runway" in svg_str
    assert "#0B0F17" in svg_str


def test_zero_em_dashes_in_module() -> None:
    """Verify neither script nor test contains em dashes."""
    root_dir = Path(__file__).parent.parent
    script_path = root_dir / "scripts" / "action_sequencer.py"
    test_path = root_dir / "tests" / "test_action_sequencer.py"

    for p in [script_path, test_path]:
        content = p.read_text(encoding="utf-8")
        assert "\u2014" not in content, f"Em dash found in {p.name}"
