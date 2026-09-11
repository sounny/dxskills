"""
Unit tests for Semantic Gravity Well & Conceptual Orbit Engine.
Verifies Keplerian orbital mechanics, gravitational capture perimeters,
eccentricity scaling, Cowan bounds, SVG generation, and markdown telemetry.
Strictly zero em dashes enforced.
"""

import pytest
import math
from scripts.semantic_gravity_well import (
    ConceptualBody,
    OrbitalBodyState,
    GravityWellTelemetry,
    SemanticGravityWell,
    sample_semantic_system,
)


def test_conceptual_body_initialization():
    body = ConceptualBody(
        body_id="test-1",
        title="Knowledge Triangulation",
        mass=42.0,
        domain_tag="epistemology",
        affinity_to_core=0.88,
    )
    assert body.body_id == "test-1"
    assert body.mass == 42.0
    assert body.affinity_to_core == 0.88
    assert body.initial_theta_rad == 0.0


def test_calculate_capture_radius_and_escape_velocity():
    engine = SemanticGravityWell(gravitational_constant_g=10000.0)
    capture_r = engine.calculate_capture_radius(core_mass=25.0)
    assert capture_r > 0.0
    expected_r = math.sqrt(10000.0 * 25.0) * 1.8
    assert abs(capture_r - expected_r) < 1e-4

    esc_v = engine.calculate_escape_velocity(core_mass=25.0, radius_px=100.0)
    assert esc_v > 0.0
    expected_v = math.sqrt(2.0 * 10000.0 * 25.0 / 100.0)
    assert abs(esc_v - expected_v) < 1e-4


def test_solve_orbital_system_empty():
    engine = SemanticGravityWell()
    core = ConceptualBody("core", "Central Core", 50.0, "arch", 1.0)
    telemetry = engine.solve_orbital_system(core, [])
    assert telemetry.core_id == "core"
    assert telemetry.total_satellites == 0
    assert telemetry.orbit_count == 0
    assert telemetry.cowan_overflow_count == 0
    assert telemetry.mean_stability_score == 1.0
    assert len(telemetry.orbital_states) == 0


def test_solve_orbital_system_harmonic_distribution():
    engine = SemanticGravityWell(base_orbit_radius_px=100.0, orbit_spacing_factor=1.4)
    core, satellites = sample_semantic_system()
    telemetry = engine.solve_orbital_system(core, satellites)

    assert telemetry.total_satellites == 5
    assert len(telemetry.orbital_states) == 5

    # Check semi-major axis increases monotonically
    for i in range(len(telemetry.orbital_states) - 1):
        assert (
            telemetry.orbital_states[i].semi_major_axis_px
            <= telemetry.orbital_states[i + 1].semi_major_axis_px
        )


def test_eccentricity_scaling():
    engine = SemanticGravityWell(max_eccentricity=0.40)
    core = ConceptualBody("core", "Thesis Core", 50.0, "main", 1.0)
    high_affinity_sat = ConceptualBody("s1", "Close Concept", 20.0, "core", 0.95)
    low_affinity_sat = ConceptualBody("s2", "Distant Concept", 10.0, "periph", 0.10)

    telemetry = engine.solve_orbital_system(core, [high_affinity_sat, low_affinity_sat])
    s1_state = next(s for s in telemetry.orbital_states if s.body.body_id == "s1")
    s2_state = next(s for s in telemetry.orbital_states if s.body.body_id == "s2")

    # High affinity should yield lower eccentricity than low affinity
    assert s1_state.eccentricity < s2_state.eccentricity
    assert s1_state.eccentricity <= 0.40
    assert s2_state.eccentricity <= 0.40


def test_stability_status_classification():
    engine = SemanticGravityWell()
    core, satellites = sample_semantic_system()
    telemetry = engine.solve_orbital_system(core, satellites)

    valid_statuses = {"locked", "resonant", "metastable", "divergent"}
    for state in telemetry.orbital_states:
        assert state.stability_status in valid_statuses
        assert 0.0 <= state.escape_risk <= 1.0


def test_cowan_overflow_and_telemetry():
    engine = SemanticGravityWell()
    core, satellites = sample_semantic_system()  # 5 satellites
    telemetry = engine.solve_orbital_system(core, satellites)

    # 5 satellites should trigger 1 cowan overflow (N > 4)
    assert telemetry.cowan_overflow_count == 1
    assert telemetry.capture_radius_px > 0.0
    assert telemetry.escape_radius_px > telemetry.capture_radius_px
    assert 0.0 <= telemetry.mean_stability_score <= 1.0


def test_generate_svg_and_markdown():
    engine = SemanticGravityWell()
    core, satellites = sample_semantic_system()
    telemetry = engine.solve_orbital_system(core, satellites)

    svg_out = engine.generate_svg(telemetry)
    assert "<svg" in svg_out
    assert "</svg>" in svg_out
    assert "coreGlow" in svg_out
    assert "SEMANTIC GRAVITY WELL ENGINE" in svg_out
    assert chr(8212) not in svg_out

    md_out = engine.generate_markdown_report(telemetry)
    assert "# Semantic Gravity Well and Conceptual Orbit Telemetry" in md_out
    assert "## 1. Core Thesis Attractor Overview" in md_out
    assert "## 3. Subordinate Concept Orbital Breakdown" in md_out
    assert chr(8212) not in md_out
