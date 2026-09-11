"""
Unit tests for Attentional Funnel & Saccadic Boundary Gasket.
Strict rule: Zero em dashes across all code, docstrings, and tests.
"""

import pytest
import math
from scripts.attentional_funnel_gasket import (
    CanvasEntity,
    FunnelConduit,
    BoundaryLeakageMeasurement,
    AttentionalFunnelTelemetry,
    AttentionalFunnelGasket,
    sample_canvas_entities,
)


def test_canvas_entity_center():
    """Verifies bounding box center coordinate calculation."""
    entity = CanvasEntity("e1", "Test Box", 100.0, 200.0, width=80.0, height=40.0)
    cx, cy = entity.center
    assert math.isclose(cx, 140.0, abs_tol=0.01)
    assert math.isclose(cy, 220.0, abs_tol=0.01)


def test_evaluate_canvas_empty():
    """Verifies graceful handling of empty entities list."""
    gasket = AttentionalFunnelGasket()
    telemetry, conduit = gasket.evaluate_canvas([])

    assert telemetry.total_entities == 0
    assert telemetry.raw_leakage_index == 0.0
    assert telemetry.noise_suppression_pct == 0.0
    assert conduit.focal_label == "Empty"


def test_calculate_transparency_curve():
    """Verifies foveal plateau, smooth falloff, and peripheral floor."""
    gasket = AttentionalFunnelGasket(foveal_radius=100.0, gasket_radius=300.0, min_transparency=0.15)

    # Inside foveal radius: exactly 1.0
    assert math.isclose(gasket.calculate_transparency(50.0), 1.0, abs_tol=0.01)
    assert math.isclose(gasket.calculate_transparency(100.0), 1.0, abs_tol=0.01)

    # Midway through gasket zone: between 0.15 and 1.0
    mid_t = gasket.calculate_transparency(200.0)
    assert 0.15 < mid_t < 1.0

    # Outside gasket perimeter: exactly min_transparency
    assert math.isclose(gasket.calculate_transparency(350.0), 0.15, abs_tol=0.01)


def test_focal_entity_selection():
    """Verifies explicit focal entity selection vs automatic selection."""
    entities = sample_canvas_entities()
    gasket = AttentionalFunnelGasket()

    # Explicit selection by entity_id
    telemetry, conduit = gasket.evaluate_canvas(entities, focal_entity_id="core-2")
    assert conduit.focal_label == "State Machine Harness"

    # Default to active focus / highest saliency
    telemetry2, conduit2 = gasket.evaluate_canvas(entities)
    assert conduit2.focal_label == "Executive Core Model"


def test_boundary_leakage_mitigation():
    """Verifies that boundary gasket suppresses raw peripheral visual noise."""
    entities = sample_canvas_entities()
    gasket = AttentionalFunnelGasket()
    telemetry, conduit = gasket.evaluate_canvas(entities)

    assert telemetry.total_entities == len(entities)
    assert telemetry.raw_leakage_index > telemetry.attenuated_leakage_index
    assert telemetry.noise_suppression_pct > 0.0
    assert telemetry.active_entities_count >= 1
    assert telemetry.peripheral_entities_count >= 1


def test_leakage_risk_classification():
    """Verifies risk tiers (contained, parafoveal_leak, peripheral_chatter)."""
    entities = sample_canvas_entities()
    gasket = AttentionalFunnelGasket(foveal_radius=150.0, gasket_radius=350.0)
    telemetry, _ = gasket.evaluate_canvas(entities)

    risks = {m.entity_id: m.leakage_risk for m in telemetry.measurements}
    assert risks["core-1"] == "contained"
    assert "peripheral_chatter" in risks.values()


def test_generate_svg_structure():
    """Verifies valid SVG markup generation with dark titanium styling and gasket rings."""
    entities = sample_canvas_entities()
    gasket = AttentionalFunnelGasket()
    telemetry, conduit = gasket.evaluate_canvas(entities)
    svg = gasket.generate_svg(telemetry, conduit, entities, width=900, height=540)

    assert "<svg" in svg
    assert "</svg>" in svg
    assert "#09090b" in svg
    assert "Attentional Funnel" in svg
    assert "fovealAperture" in svg
    assert "Executive Core Model" in svg


def test_generate_markdown_report():
    """Verifies publication-ready markdown compliance audit."""
    entities = sample_canvas_entities()
    gasket = AttentionalFunnelGasket()
    telemetry, _ = gasket.evaluate_canvas(entities)
    report = gasket.generate_markdown_report(telemetry)

    assert "# Attentional Funnel and Saccadic Boundary Gasket Audit" in report
    assert "Bouma Law of Visual Crowding" in report
    assert "Lavie Perceptual Load Theory" in report
    assert "| `core-1` |" in report
    assert chr(8212) not in report
