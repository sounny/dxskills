"""Unit tests for Autonomous Cognitive Spatial Dual-Foveal Saccadic Pivot & Anchor Restorer.

Strict Quality Gate: Zero em dashes anywhere.
"""

import json
from pathlib import Path
import pytest

from scripts.saccadic_pivot import (
    DualFovealSaccadicPivot,
    PivotTelemetry,
    PivotTrajectory,
    RestorationBeacon,
)


def test_node_center():
    pivot = DualFovealSaccadicPivot()
    node = {"x": 100, "y": 200, "width": 300, "height": 100}
    assert pivot.get_node_center(node) == (250.0, 250.0)


def test_compute_reentry_kinematics():
    pivot = DualFovealSaccadicPivot(px_per_deg=38.0)

    # 380px is 10 degrees
    amp, vel, dur, err, lat = pivot.compute_reentry_kinematics(380.0)
    assert pytest.approx(amp, rel=1e-2) == 10.0
    assert 200.0 < vel < 400.0
    assert 40.0 < dur < 60.0
    assert err > 1.0
    assert lat > 300.0


def test_extract_anchor_phrase():
    pivot = DualFovealSaccadicPivot()
    assert pivot.extract_anchor_phrase("## Raft Consensus Module\n\nElection details") == "Raft Consensus Module"
    assert pivot.extract_anchor_phrase("") == "Active Focal Point"
    long_line = "Distributed state machine replication protocol with Byzantine fault tolerance across global clusters"
    extracted = pivot.extract_anchor_phrase(long_line)
    assert len(extracted.split()) <= 6


def test_plan_saccadic_pivot_and_exports(tmp_path: Path):
    pivot = DualFovealSaccadicPivot()
    canvas_data = {
        "nodes": [
            {"id": "node-src", "x": 0, "y": 0, "width": 200, "height": 100, "text": "Source Code Editor"},
            {"id": "node-tgt", "x": 800, "y": 450, "width": 250, "height": 150, "text": "Target Architecture Topology\n\nCluster details."},
        ],
        "edges": []
    }

    enriched_canvas, telemetry = pivot.plan_saccadic_pivot(
        canvas_data,
        source_id="node-src",
        target_id="node-tgt",
        history_trail=["node-src", "Pivot-Arc", "node-tgt"]
    )

    assert telemetry.source_id == "node-src"
    assert telemetry.target_id == "node-tgt"
    assert telemetry.trajectory.distance_px > 800.0
    assert telemetry.reentry_efficiency_pct > 50.0
    assert telemetry.beacon.foveal_anchor_phrase == "Target Architecture Topology"

    # Enriched canvas checks
    assert len(enriched_canvas["nodes"]) == 3  # source + target + beacon card
    assert len(enriched_canvas["edges"]) == 1  # pivot trajectory edge

    # ASCII render check
    ascii_out = pivot.render_ascii_pivot(telemetry)
    assert "Dual-Foveal Saccadic Pivot" in ascii_out
    assert "node-src" in ascii_out
    assert "Target Architecture Topology" in ascii_out

    # SVG export check
    svg_path = tmp_path / "test_pivot.svg"
    pivot.export_svg_trajectory(telemetry, svg_path)
    assert svg_path.exists()
    svg_data = svg_path.read_text(encoding="utf-8")
    assert "<svg" in svg_data
    assert "Saccadic Pivot" in svg_data


def test_zero_em_dashes():
    script_file = Path(__file__).resolve().parent.parent / "scripts" / "saccadic_pivot.py"
    test_file = Path(__file__).resolve()

    em_dash = chr(8212)
    assert em_dash not in script_file.read_text(encoding="utf-8")
    assert em_dash not in test_file.read_text(encoding="utf-8")
