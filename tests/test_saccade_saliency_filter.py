"""
Unit tests for Autonomous Cognitive Spatial Attentional Saccade Saliency Filter & Noise Gate.
Strictly NO em dashes (\u2014) anywhere.
"""

import pytest
from scripts.saccade_saliency_filter import (
    SaliencyNode,
    NoiseGateTelemetry,
    SaccadeSaliencyResult,
    SaccadeSaliencyFilter
)

SAMPLE_NODES = [
    {"id": "n1", "label": "Core Epistemic Anchor", "x": 380, "y": 280, "width": 160, "height": 80},
    {"id": "n2", "label": "Primary Synthesis Nexus", "x": 420, "y": 320, "width": 180, "height": 90},
    {"id": "n3", "label": "Marginal Metadata Clutter Fragment", "x": 100, "y": 80, "width": 120, "height": 60},
    {"id": "n4", "label": "Peripheral Note Boundary Clutter", "x": 750, "y": 550, "width": 140, "height": 70},
]

def test_raw_saliency_calculation():
    filter_obj = SaccadeSaliencyFilter()
    core_node = {"id": "c1", "label": "Core Anchor Nexus", "width": 200, "height": 100}
    raw_s = filter_obj.compute_raw_saliency(core_node)
    assert raw_s > 0.60
    assert raw_s <= 1.0

def test_spatial_attenuation_decay():
    filter_obj = SaccadeSaliencyFilter(foveal_radius=200.0, margin_cutoff=500.0)
    res = filter_obj.apply_filter(SAMPLE_NODES, focus_x=400.0, focus_y=300.0)
    # n1 and n2 are near focus, n3 and n4 are far away
    n1 = next(n for n in res.nodes if n.node_id == "n1")
    n3 = next(n for n in res.nodes if n.node_id == "n3")
    assert n1.distance_to_focus < n3.distance_to_focus
    assert n1.filtered_saliency > n3.filtered_saliency

def test_noise_gate_passing():
    filter_obj = SaccadeSaliencyFilter(threshold=0.30, margin_cutoff=500.0)
    res = filter_obj.apply_filter(SAMPLE_NODES, focus_x=400.0, focus_y=300.0)
    passed_ids = [n.node_id for n in res.nodes if n.pass_gate]
    assert "n1" in passed_ids
    assert "n2" in passed_ids

def test_telemetry_headroom_boost():
    filter_obj = SaccadeSaliencyFilter(threshold=0.35, margin_cutoff=400.0)
    res = filter_obj.apply_filter(SAMPLE_NODES, focus_x=400.0, focus_y=300.0)
    tel = res.telemetry
    assert tel.total_nodes == len(SAMPLE_NODES)
    assert tel.passed_nodes > 0
    assert tel.gated_nodes > 0
    assert tel.headroom_boost_percent > 0.0
    assert tel.attenuated_noise_energy >= 0.0

def test_to_dict_serialization():
    filter_obj = SaccadeSaliencyFilter()
    res = filter_obj.apply_filter(SAMPLE_NODES)
    d = res.to_dict()
    assert "nodes" in d
    assert "telemetry" in d
    assert len(d["nodes"]) == len(SAMPLE_NODES)

def test_svg_rendering_elements():
    filter_obj = SaccadeSaliencyFilter()
    res = filter_obj.apply_filter(SAMPLE_NODES)
    svg = res.saliency_map_svg
    assert "<svg" in svg
    assert "</svg>" in svg
    assert "titaniumBg" in svg
    assert "fovealGlow" in svg
    assert "Attentional Saccade Saliency Filter" in svg

def test_markdown_report_zero_em_dashes():
    filter_obj = SaccadeSaliencyFilter()
    res = filter_obj.apply_filter(SAMPLE_NODES)
    md = res.noise_gate_report_md
    assert "# Attentional Saccade Saliency Filter & Noise Gate Report" in md
    assert "Saliency Attenuation Metrics" in md
    assert "Node Saliency Classification" in md
    assert chr(8212) not in md

def test_empty_nodes_handling():
    filter_obj = SaccadeSaliencyFilter()
    res = filter_obj.apply_filter([])
    assert res.telemetry.total_nodes == 0
    assert res.telemetry.passed_nodes == 0
    assert len(res.nodes) == 0
