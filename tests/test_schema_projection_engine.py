"""Unit tests for Autonomous Cognitive Spatial Schema Morphing & Cross-Scale Projection Engine.

Tests verify:
- Empty schema handling
- Triadic abstraction plane classification (macro, meso, micro)
- Allocentric coordinate invariant tracking across zoom scales
- Cross-scale coherence and drift variance telemetry
- Obsidian .canvas export with plane group frames
- Publication-grade SVG rendering
- ASCII report formatting
- Strict zero em dash rule enforcement

Strict Quality Gate: Zero em dashes anywhere (use hyphens, commas, or parentheses).
"""

import json
import os
import pytest

from scripts.schema_projection_engine import (
    AbstractionPlane,
    CrossScaleProjectionTelemetry,
    ProjectedEntity,
    SchemaCrossScaleProjector,
)


def test_empty_schema_handling():
    projector = SchemaCrossScaleProjector()
    projector.load_dict({})
    entities, telemetry = projector.project_schema()

    assert entities == []
    assert telemetry.total_entities == 0
    assert telemetry.macro_count == 0
    assert telemetry.allocentric_drift_variance == 0.0


def test_triadic_abstraction_plane_classification():
    projector = SchemaCrossScaleProjector()
    nodes = {
        "nodes": {
            "n_arch": {"title": "Strategic Architecture", "text": "Global system macro boundary", "x": 100, "y": 100},
            "n_serv": {"title": "Auth Broker Service", "text": "Meso service interaction conduit", "x": 300, "y": 200},
            "n_code": {"title": "Token Hash Validator", "text": "Micro def validate_token function ast", "x": 500, "y": 400},
        }
    }
    projector.load_dict(nodes)
    entities, telemetry = projector.project_schema()

    assert len(entities) == 3
    assert telemetry.macro_count == 1
    assert telemetry.meso_count == 1
    assert telemetry.micro_count == 1

    ent_map = {e.entity_id: e for e in entities}
    assert ent_map["n_arch"].plane == AbstractionPlane.MACRO_TOPOLOGY
    assert ent_map["n_serv"].plane == AbstractionPlane.MESO_INTERACTION
    assert ent_map["n_code"].plane == AbstractionPlane.MICRO_SPECIFICATION


def test_allocentric_invariant_tracking_and_scaling():
    projector = SchemaCrossScaleProjector(macro_spread_factor=1.0, meso_spread_factor=1.5, micro_spread_factor=2.0)
    nodes = {
        "nodes": {
            "c_macro": {"title": "Macro Top", "text": "High level", "plane": "macro", "x": 0, "y": 0},
            "c_micro": {"title": "Micro Bottom", "text": "Deep code AST", "plane": "micro", "x": 200, "y": 200},
        }
    }
    projector.load_dict(nodes)
    entities, telemetry = projector.project_schema()

    assert len(entities) == 2
    ent_macro = next(e for e in entities if e.entity_id == "c_macro")
    ent_micro = next(e for e in entities if e.entity_id == "c_micro")

    assert ent_macro.zoom_scale_factor == pytest.approx(0.60, 0.01)
    assert ent_micro.zoom_scale_factor == pytest.approx(1.60, 0.01)
    assert ent_macro.invariant_anchor_key.startswith("inv_c_mac")


def test_cross_scale_coherence_telemetry():
    projector = SchemaCrossScaleProjector()
    demo_canvas = {
        "nodes": [
            {"id": "node_sys", "text": "# System\nMacro core domain", "x": 100, "y": 100},
            {"id": "node_api", "text": "# API Gateway\nMeso service channel", "x": 250, "y": 200},
            {"id": "node_ast", "text": "# AST Parser\nMicro function implementation", "x": 400, "y": 300},
        ],
        "edges": []
    }
    projector.load_canvas(demo_canvas)
    _, telemetry = projector.project_schema()

    assert telemetry.total_entities == 3
    assert telemetry.cross_scale_coherence_pct > 80.0
    assert telemetry.allocentric_drift_variance >= 0.0


def test_canvas_export_with_plane_groups(tmp_path):
    projector = SchemaCrossScaleProjector()
    nodes = {
        "nodes": {
            "m1": {"title": "Macro Domain", "text": "Strategic boundaries", "plane": "macro", "x": 100, "y": 100},
            "m2": {"title": "Micro Function", "text": "def calculate_hash()", "plane": "micro", "x": 600, "y": 400},
        }
    }
    projector.load_dict(nodes)
    out_file = tmp_path / "multi_scale.canvas"
    res = projector.to_canvas(str(out_file))

    assert out_file.exists()
    assert any(n.get("type") == "group" for n in res["nodes"])
    assert any(n.get("type") == "text" for n in res["nodes"])


def test_svg_export(tmp_path):
    projector = SchemaCrossScaleProjector()
    nodes = {
        "nodes": {
            "node_a": {"title": "Macro Node", "text": "High strategic domain", "x": 100, "y": 100},
            "node_b": {"title": "Meso Broker", "text": "Service interaction channel", "x": 400, "y": 250},
        }
    }
    projector.load_dict(nodes)
    out_svg = tmp_path / "projection.svg"
    svg_str = projector.to_svg(str(out_svg))

    assert out_svg.exists()
    assert "<svg" in svg_str
    assert "Spatial Schema Morphing &amp; Cross-Scale Projection Engine" in svg_str
    assert "Concentric Multi-Scale Guidance Grid" in svg_str
    assert "Macro Zone" in svg_str


def test_ascii_report():
    projector = SchemaCrossScaleProjector()
    nodes = {
        "nodes": {
            "ent_1": {"title": "Macro Hub", "text": "Strategic domain boundary", "x": 100, "y": 100},
            "ent_2": {"title": "Meso Adapter", "text": "API bridge connection", "x": 300, "y": 200},
        }
    }
    projector.load_dict(nodes)
    _, telemetry = projector.project_schema()
    report = projector.render_ascii_report(telemetry)

    assert "Spatial Schema Morphing & Cross-Scale Projection Report" in report
    assert "Macro Hub" in report
    assert "Cross-Scale Coherence Score:" in report


def test_zero_em_dashes_in_module():
    scripts_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "scripts", "schema_projection_engine.py")
    test_path = __file__

    with open(scripts_path, "r", encoding="utf-8") as f:
        src_text = f.read()
    with open(test_path, "r", encoding="utf-8") as f:
        test_text = f.read()

    assert chr(8212) not in src_text, "Found em dash in scripts/schema_projection_engine.py"
    assert chr(8212) not in test_text, "Found em dash in tests/test_schema_projection_engine.py"
