"""Unit tests for Autonomous Cognitive Spatial Multi-Scale Attention Density Calibrator & Visual Restorer.

Strict Quality Gate: Zero em dashes anywhere (use hyphens, commas, or parentheses).
"""

from __future__ import annotations

import json
from pathlib import Path
import pytest

from scripts.density_calibrator import (
    AttentionDensityCalibrator,
    DensityNode,
    CrowdingHotspot,
    CrowdingTier,
    DensityTelemetry,
)


def test_empty_input_handling() -> None:
    """Ensure density calibrator handles empty layout gracefully without errors."""
    calibrator = AttentionDensityCalibrator()
    nodes, hotspots, telemetry = calibrator.calibrate()

    assert len(nodes) == 0
    assert len(hotspots) == 0
    assert telemetry.total_nodes == 0
    assert telemetry.initial_mean_density == 0.0
    assert telemetry.rebalanced_mean_density == 0.0
    assert telemetry.ocular_fatigue_mitigation_score == 1.0


def test_kde_density_and_bouma_clearance() -> None:
    """Verify KDE continuous attention calculation and Bouma window clearance metrics."""
    calibrator = AttentionDensityCalibrator(foveal_sigma=150.0, bouma_factor=1.8)
    nodes_data = {
        "n1": {
            "title": "Auth Core",
            "x": 100.0,
            "y": 100.0,
            "width": 200.0,
            "height": 120.0,
            "text": "Authentication service with JWT signing and OAuth2 token verification.",
        },
        "n2": {
            "title": "Token Vault",
            "x": 140.0,
            "y": 120.0,
            "width": 200.0,
            "height": 120.0,
            "text": "Secure cryptographic key storage and ephemeral session state cache.",
        },
        "n3": {
            "title": "Remote Telemetry",
            "x": 1500.0,
            "y": 1500.0,
            "width": 200.0,
            "height": 120.0,
            "text": "Isolated telemetry logger.",
        },
    }
    calibrator.load_dict(nodes_data)
    nodes, hotspots, telemetry = calibrator.calibrate()

    assert len(nodes) == 3
    node_map = {n.node_id: n for n in nodes}

    # n1 and n2 are very close, should have elevated or critical crowding
    assert node_map["n1"].local_density_score > 0.1
    assert node_map["n1"].crowding_tier == CrowdingTier.CRITICAL_CROWDING
    assert node_map["n2"].crowding_tier == CrowdingTier.CRITICAL_CROWDING
    assert node_map["n1"].bouma_clearance_px > 0.0

    # n3 is isolated, should be sparse
    assert node_map["n3"].crowding_tier == CrowdingTier.SPARSE
    assert node_map["n3"].local_density_score < 0.15


def test_crowding_hotspot_clustering() -> None:
    """Verify spatial clustering of crowded nodes into distinct attention hotspots."""
    calibrator = AttentionDensityCalibrator(foveal_sigma=200.0)
    cluster_nodes = {
        "c1": {"title": "Parser", "x": 300.0, "y": 300.0, "width": 220.0, "height": 140.0, "text": "Lexical parser."},
        "c2": {"title": "AST Builder", "x": 350.0, "y": 320.0, "width": 220.0, "height": 140.0, "text": "Abstract syntax tree generator."},
        "c3": {"title": "Type Checker", "x": 320.0, "y": 380.0, "width": 220.0, "height": 140.0, "text": "Static type inference engine."},
    }
    calibrator.load_dict(cluster_nodes)
    nodes, hotspots, telemetry = calibrator.calibrate()

    assert len(hotspots) >= 1
    h = hotspots[0]
    assert h.node_count >= 2
    assert h.peak_density > 0.0
    assert h.recommended_expansion_factor >= 1.2


def test_force_directed_rebalancing() -> None:
    """Verify repulsive force expands nodes to restore whitespace and alleviate crowding."""
    calibrator = AttentionDensityCalibrator(foveal_sigma=180.0)
    overlap_nodes = {
        "a": {"title": "Node A", "x": 400.0, "y": 400.0, "width": 200.0, "height": 100.0, "text": "High priority task node."},
        "b": {"title": "Node B", "x": 420.0, "y": 410.0, "width": 200.0, "height": 100.0, "text": "Dependent task execution."},
    }
    calibrator.load_dict(overlap_nodes)
    nodes, hotspots, telemetry = calibrator.calibrate(iterations=15, repulsion_k=40000.0)

    node_a = next(n for n in nodes if n.node_id == "a")
    node_b = next(n for n in nodes if n.node_id == "b")

    init_dx = abs(node_a.x - node_b.x)
    init_dy = abs(node_a.y - node_b.y)
    init_dist = (init_dx ** 2 + init_dy ** 2) ** 0.5

    post_dx = abs(node_a.adjusted_x - node_b.adjusted_x)
    post_dy = abs(node_a.adjusted_y - node_b.adjusted_y)
    post_dist = (post_dx ** 2 + post_dy ** 2) ** 0.5

    # Post distance must be greater than initial distance due to repulsive expansion
    assert post_dist > init_dist


def test_canvas_export(tmp_path: Path) -> None:
    """Verify export to Obsidian .canvas file format with adjusted coordinates and badges."""
    calibrator = AttentionDensityCalibrator()
    canvas_input = {
        "nodes": [
            {"id": "node_alpha", "x": 100, "y": 100, "width": 250, "height": 140, "text": "# Alpha Task\nInitial node."},
            {"id": "node_beta", "x": 150, "y": 120, "width": 250, "height": 140, "text": "# Beta Task\nCrowded child."},
        ],
        "edges": [
            {"id": "edge_1", "fromNode": "node_alpha", "toNode": "node_beta"},
        ],
    }
    calibrator.load_canvas(canvas_input)

    output_file = str(tmp_path / "rebalanced.canvas")
    result = calibrator.to_canvas(output_path=output_file, canvas_title="Calibrated Space")

    assert Path(output_file).exists()
    assert "nodes" in result
    assert "edges" in result
    assert len(result["nodes"]) == 2
    assert len(result["edges"]) == 1

    # Ensure nodes contain badges and adjusted position coordinates
    node_out = result["nodes"][0]
    assert "Density:" in node_out["text"]
    assert "Bouma Clearance:" in node_out["text"]
    assert "color" in node_out


def test_svg_export(tmp_path: Path) -> None:
    """Verify publication-grade dark titanium SVG generation."""
    calibrator = AttentionDensityCalibrator()
    data = {
        "k1": {"title": "Kernel A", "x": 200, "y": 200, "width": 200, "height": 100, "text": "Core kernel module."},
        "k2": {"title": "Kernel B", "x": 230, "y": 210, "width": 200, "height": 100, "text": "Secondary driver."},
    }
    calibrator.load_dict(data)

    svg_file = str(tmp_path / "density_map.svg")
    svg_str = calibrator.to_svg(output_path=svg_file, width=1200, height=800)

    assert Path(svg_file).exists()
    assert "<svg" in svg_str
    assert "</svg>" in svg_str
    assert "#0B0F17" in svg_str
    assert "Attention Density Metrics" in svg_str
    assert "Bouma Window Clearance" in svg_str


def test_ascii_report() -> None:
    """Verify terminal-friendly ASCII summary generation."""
    calibrator = AttentionDensityCalibrator()
    data = {
        "n1": {"title": "Cluster 1", "x": 100, "y": 100, "width": 180, "height": 90, "text": "Item 1"},
        "n2": {"title": "Cluster 2", "x": 130, "y": 120, "width": 180, "height": 90, "text": "Item 2"},
    }
    calibrator.load_dict(data)
    nodes, hotspots, telemetry = calibrator.calibrate()
    report = calibrator.render_ascii_report(telemetry)

    assert "Spatial Multi-Scale Attention Density & Whitespace Report" in report
    assert "Total Canvas Nodes:" in report
    assert "Density Reduction:" in report


def test_zero_em_dashes_in_module() -> None:
    """Verify neither script nor test contains em dashes."""
    root_dir = Path(__file__).parent.parent
    script_path = root_dir / "scripts" / "density_calibrator.py"
    test_path = root_dir / "tests" / "test_density_calibrator.py"

    for p in [script_path, test_path]:
        content = p.read_text(encoding="utf-8")
        assert "\u2014" not in content, f"Em dash found in {p.name}"
