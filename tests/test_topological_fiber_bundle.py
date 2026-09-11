"""
Tests for Topological Fiber Bundle & Polytope Holonomy Weaver
Validates Mobius strip half-integer twist, Hopf fibration projections,
torus knot bundles, parallel transport holonomy, SVG rendering, and zero em dash compliance.
"""

import os
import sys
import math
import json
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.topological_fiber_bundle import (
    TopologicalFiberBundle,
    FiberVector,
    HolonomyTelemetry,
)


def test_mobius_bundle_weaving():
    weaver = TopologicalFiberBundle()
    telemetry = weaver.weave_mobius_bundle(radius_px=150.0, steps=64, twist_factor=1.0)
    assert telemetry.bundle_type == "MOBIUS_STRIP"
    assert telemetry.total_steps == 64
    assert len(telemetry.fibers) == 64
    assert telemetry.total_twist_deg == 180.0
    assert telemetry.holonomy_angle_deg == 180.0
    assert telemetry.is_non_trivial_topology is True
    assert telemetry.loop_perimeter_px > 900.0
    assert len(telemetry.warnings) > 0


def test_hopf_fibration_weaving():
    weaver = TopologicalFiberBundle()
    telemetry = weaver.weave_hopf_fibration(base_radius_px=140.0, steps=48, fiber_twist=1.0)
    assert telemetry.bundle_type == "HOPF_FIBRATION"
    assert telemetry.total_steps == 48
    assert len(telemetry.fibers) == 48
    assert telemetry.is_non_trivial_topology is True
    assert telemetry.connection_curvature_integral > 6.0


def test_torus_bundle_weaving():
    weaver = TopologicalFiberBundle()
    telemetry = weaver.weave_torus_bundle(major_radius_px=160.0, minor_radius_px=45.0, p_winds=2, q_winds=3, steps=72)
    assert telemetry.bundle_type == "TORUS_KNOT"
    assert telemetry.total_steps == 72
    assert len(telemetry.fibers) == 72
    assert telemetry.is_non_trivial_topology is True
    assert telemetry.loop_perimeter_px > 0.0


def test_trivial_cylinder_bundle():
    weaver = TopologicalFiberBundle()
    telemetry = weaver.weave_mobius_bundle(twist_factor=0.0, steps=32)
    assert telemetry.total_twist_deg == 0.0
    assert telemetry.holonomy_angle_deg == 0.0
    assert telemetry.is_non_trivial_topology is False


def test_svg_rendering():
    weaver = TopologicalFiberBundle()
    telemetry = weaver.weave_mobius_bundle(steps=40)
    svg = weaver.render_fiber_bundle_svg(telemetry, width=920, height=560)
    assert "<svg" in svg
    assert "</svg>" in svg
    assert "#0b0f14" in svg
    assert "TOPOLOGICAL FIBER BUNDLE" in svg
    assert "Holonomy Angle" in svg
    assert "MOBIUS_STRIP" in svg


def test_export_telemetry_json():
    weaver = TopologicalFiberBundle()
    telemetry = weaver.weave_mobius_bundle(steps=20)
    json_str = weaver.export_telemetry_json(telemetry)
    data = json.loads(json_str)
    assert "bundle_type" in data
    assert "holonomy_angle_deg" in data
    assert "is_non_trivial_topology" in data
    assert data["fiber_count"] == 20


def test_zero_em_dashes():
    """Verify zero em dashes in script and test files."""
    script_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "scripts", "topological_fiber_bundle.py")
    )
    with open(script_path, "r", encoding="utf-8") as f:
        script_code = f.read()
    assert chr(8212) not in script_code, "Unicode em dash found in topological_fiber_bundle.py"

    test_path = os.path.abspath(__file__)
    with open(test_path, "r", encoding="utf-8") as f:
        test_code = f.read()
    assert chr(8212) not in test_code, "Unicode em dash found in test_topological_fiber_bundle.py"
