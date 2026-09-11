"""Unit tests for Autonomous Cognitive Spatial Multi-Scale Attention Tunnel & Peripheral Fovea Synchronizer.

Strict Quality Gate: Zero em dashes anywhere.
"""

import json
from pathlib import Path
import pytest

from scripts.fovea_synchronizer import (
    DampingMode,
    FoveaSyncTelemetry,
    PeripheralAnchor,
    SpatialFoveaSynchronizer,
)


def test_calculate_tunnel_radius():
    sync = SpatialFoveaSynchronizer(base_tunnel_radius_px=450.0)

    # High load tightens the tunnel radius
    r_high = sync.calculate_tunnel_radius(cognitive_load=0.9)
    assert 300.0 <= r_high <= 380.0

    # Low load opens the visual field
    r_low = sync.calculate_tunnel_radius(cognitive_load=0.1)
    assert 480.0 <= r_low <= 550.0
    assert r_high < r_low


def test_apply_attention_tunnel_empty():
    sync = SpatialFoveaSynchronizer()
    canvas, telemetry = sync.apply_attention_tunnel({"nodes": []})

    assert telemetry.total_nodes == 0
    assert telemetry.foveal_nodes_count == 0
    assert telemetry.damped_peripheral_count == 0
    assert telemetry.spatial_orientation_integrity_score == 1.0


def test_apply_attention_tunnel_nodes():
    sync = SpatialFoveaSynchronizer(base_tunnel_radius_px=400.0)

    sample_canvas = {
        "nodes": [
            {
                "id": "node_focus",
                "x": 0,
                "y": 0,
                "width": 250,
                "height": 140,
                "color": "1",
                "text": "### Core System State\nActive consensus algorithm and memory barrier",
            },
            {
                "id": "node_near",
                "x": 150,
                "y": 100,
                "width": 250,
                "height": 140,
                "color": "2",
                "text": "### Immediate Dependency\nMutex locks for thread pool",
            },
            {
                "id": "node_far",
                "x": 900,
                "y": 800,
                "width": 250,
                "height": 140,
                "color": "3",
                "text": "### Legacy Backup Archive\nCold storage glacier bucket sync pipeline",
            },
        ],
        "edges": [],
    }

    transformed_canvas, telemetry = sync.apply_attention_tunnel(
        canvas_data=sample_canvas,
        focus_node_id="node_focus",
        cognitive_load=0.7,
        damping_mode=DampingMode.DESATURATE_DAMP,
    )

    assert telemetry.total_nodes == 3
    assert telemetry.foveal_nodes_count >= 1
    assert telemetry.damped_peripheral_count >= 1
    assert telemetry.crowding_reduction_pct > 20.0
    assert telemetry.spatial_orientation_integrity_score >= 0.80

    # Far node must be dampened in text and color
    far_node = [n for n in transformed_canvas["nodes"] if n["id"] == "node_far"][0]
    assert far_node["color"] == "6"
    assert "spatial context" in far_node["text"]

    # Focus node retains original color
    focus_node = [n for n in transformed_canvas["nodes"] if n["id"] == "node_focus"][0]
    assert focus_node["color"] == "1"


def test_damping_modes():
    sync = SpatialFoveaSynchronizer(base_tunnel_radius_px=200.0)
    sample_canvas = {
        "nodes": [
            {"id": "n1", "x": 0, "y": 0, "width": 200, "height": 100, "text": "### Focus Node\nMain text"},
            {"id": "n2", "x": 800, "y": 800, "width": 200, "height": 100, "text": "### Distant Node\nSecondary line 1\nSecondary line 2"},
        ]
    }

    # Test minimal skeleton
    c_skel, tel_skel = sync.apply_attention_tunnel(
        sample_canvas, focus_node_id="n1", damping_mode=DampingMode.MINIMAL_SKELETON
    )
    far_skel = [n for n in c_skel["nodes"] if n["id"] == "n2"][0]
    assert "peripheral anchor" in far_skel["text"]

    # Test desaturate damp
    c_desat, tel_desat = sync.apply_attention_tunnel(
        sample_canvas, focus_node_id="n1", damping_mode=DampingMode.DESATURATE_DAMP
    )
    far_desat = [n for n in c_desat["nodes"] if n["id"] == "n2"][0]
    assert "spatial context" in far_desat["text"]


def test_export_svg_tunnel(tmp_path):
    sync = SpatialFoveaSynchronizer()
    anchors = [
        PeripheralAnchor("f1", "Focus Node", 0, 0, 0.0, 0.0, 1.0, True, "1"),
        PeripheralAnchor("p1", "Peripheral Node", 500, 300, 583.1, 31.0, 0.35, False, "6"),
    ]
    telemetry = FoveaSyncTelemetry(
        focus_node_id="f1",
        focus_node_title="Focus Node",
        tunnel_radius_px=420.0,
        cognitive_load=0.6,
        total_nodes=2,
        foveal_nodes_count=1,
        damped_peripheral_count=1,
        crowding_reduction_pct=38.5,
        spatial_orientation_integrity_score=0.92,
        damping_mode="desaturate_damp",
    )

    out_svg = tmp_path / "tunnel_radar.svg"
    svg_str = sync.export_svg_tunnel(anchors, telemetry, str(out_svg))

    assert out_svg.exists()
    assert "<svg" in svg_str
    assert "</svg>" in svg_str
    assert "Foveal Tunnel" in svg_str
    assert "Focus Node" in svg_str


def test_zero_em_dashes_enforcement():
    sync = SpatialFoveaSynchronizer()
    sample_canvas = {
        "nodes": [
            {"id": "n1", "x": 0, "y": 0, "width": 200, "height": 100, "text": "### Focal Hub\nCritical tokens"},
            {"id": "n2", "x": 600, "y": 600, "width": 200, "height": 100, "text": "### Peripheral Task\nSecondary tokens"},
        ]
    }
    c_out, telemetry = sync.apply_attention_tunnel(sample_canvas, focus_node_id="n1")
    md_report = sync.generate_markdown_report(telemetry)

    anchors = [
        PeripheralAnchor("n1", "Focal Hub", 0, 0, 0.0, 0.0, 1.0, True, "1"),
        PeripheralAnchor("n2", "Peripheral Task", 600, 600, 848.5, 45.0, 0.25, False, "6"),
    ]
    svg_str = sync.export_svg_tunnel(anchors, telemetry)

    full_text = md_report + svg_str + json.dumps(c_out) + json.dumps(telemetry.to_dict())
    assert chr(8212) not in full_text
    assert "\u2014" not in full_text
