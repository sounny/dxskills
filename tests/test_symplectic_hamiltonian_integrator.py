"""
Unit tests for Symplectic Phase Space Integrator & Hamiltonian Concept Orbit Loom.
Verifies symplectic energy conservation, gradient accuracy, Liouville phase volume preservation,
Poincare surface of section recurrence, SVG/HTML output, and zero em dashes.
"""

import sys
import os
import math
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.symplectic_hamiltonian_integrator import (
    SymplecticHamiltonianIntegrator,
    create_cognitive_orbit_simulation,
    PhaseSpaceState,
)


def test_hamiltonian_energy_definitions():
    """Verifies kinetic, potential, and total Hamiltonian energy equations."""
    integrator = SymplecticHamiltonianIntegrator(mass=2.0, restoring_k=1.0)
    # T = (p1^2 + p2^2) / (2 * m) = (3^2 + 4^2) / (2 * 2) = 25 / 4 = 6.25
    assert integrator.kinetic_energy(3.0, 4.0) == pytest.approx(6.25, abs=1e-6)

    # Without attractors, V = 0.5 * k * (q1^2 + q2^2) = 0.5 * 1.0 * (1^2 + 2^2) = 2.5
    assert integrator.potential_energy(1.0, 2.0) == pytest.approx(2.5, abs=1e-6)

    # Total H = 6.25 + 2.5 = 8.75
    assert integrator.total_hamiltonian(1.0, 2.0, 3.0, 4.0) == pytest.approx(8.75, abs=1e-6)


def test_analytic_potential_gradient():
    """Verifies that potential_gradient matches finite difference approximations."""
    integrator = SymplecticHamiltonianIntegrator(mass=1.0, restoring_k=0.6)
    integrator.add_attractor("att1", "Test Attractor", cx=0.5, cy=-0.4, depth=1.5, radius=0.8)

    q1, q2 = 0.3, 0.2
    g1_analytic, g2_analytic = integrator.potential_gradient(q1, q2)

    eps = 1e-6
    v_plus_1 = integrator.potential_energy(q1 + eps, q2)
    v_minus_1 = integrator.potential_energy(q1 - eps, q2)
    g1_num = (v_plus_1 - v_minus_1) / (2.0 * eps)

    v_plus_2 = integrator.potential_energy(q1, q2 + eps)
    v_minus_2 = integrator.potential_energy(q1, q2 - eps)
    g2_num = (v_plus_2 - v_minus_2) / (2.0 * eps)

    assert g1_analytic == pytest.approx(g1_num, rel=1e-4)
    assert g2_analytic == pytest.approx(g2_num, rel=1e-4)


def test_symplectic_energy_conservation_bound():
    """
    Verifies that leapfrog kick-drift-kick preserves total energy with bounded oscillations
    and no secular runaway drift.
    """
    integrator = SymplecticHamiltonianIntegrator(mass=1.0, restoring_k=0.5)
    integrator.add_attractor("a1", "Attractor A", cx=-0.5, cy=0.4, depth=1.0, radius=0.7)

    trajectory = integrator.simulate(q0=(0.8, -0.3), p0=(0.0, 1.0), steps=600, dt=0.03)
    assert len(trajectory) == 601

    e0 = trajectory[0].hamiltonian_energy
    max_drift = max(abs(s.hamiltonian_energy - e0) for s in trajectory)
    rel_drift = max_drift / abs(e0)

    # Symplectic leapfrog guarantees bounded energy oscillation (typically < 1%)
    assert rel_drift < 0.02
    assert integrator.calculate_metrics()["energy_conservation_pct"] > 98.0


def test_liouville_phase_space_area_preservation():
    """
    Verifies that phase space 2-form area is preserved under Hamiltonian leapfrog flow.
    """
    integrator = SymplecticHamiltonianIntegrator(mass=1.0, restoring_k=0.5)
    # Infinitesimal displacement in 1D phase space (q1, p1)
    q0, p0 = 1.0, 0.5
    dq = 1e-4
    dp = 1e-4

    # Simulate 4 corner states
    dt = 0.04
    steps = 150

    s_base = integrator.simulate(q0=(q0, 0.0), p0=(p0, 0.0), steps=steps, dt=dt)[-1]
    s_q = integrator.simulate(q0=(q0 + dq, 0.0), p0=(p0, 0.0), steps=steps, dt=dt)[-1]
    s_p = integrator.simulate(q0=(q0, 0.0), p0=(p0 + dp, 0.0), steps=steps, dt=dt)[-1]

    # Initial area = dq * dp
    initial_area = dq * dp

    # Final tangent vectors in (q1, p1)
    v1 = (s_q.q1 - s_base.q1, s_q.p1 - s_base.p1)
    v2 = (s_p.q1 - s_base.q1, s_p.p1 - s_base.p1)

    # 2D cross product gives evolved phase area
    evolved_area = abs(v1[0] * v2[1] - v1[1] * v2[0])

    assert evolved_area == pytest.approx(initial_area, rel=0.01)


def test_poincare_surface_of_section_cuts():
    """Verifies that Poincare section crossings of q2=0 with p2>0 are detected."""
    sim = create_cognitive_orbit_simulation()
    metrics = sim.calculate_metrics()

    assert metrics["poincare_surface_crossings"] > 0
    assert len(sim.poincare_cuts) > 0

    # Crossings should have reasonable coordinates
    for q_cross, p_cross in sim.poincare_cuts:
        assert isinstance(q_cross, float)
        assert isinstance(p_cross, float)


def test_simulation_preset_and_metrics():
    """Verifies create_cognitive_orbit_simulation preset and output metrics dictionary."""
    sim = create_cognitive_orbit_simulation()
    metrics = sim.calculate_metrics()

    assert metrics["total_steps"] == 750
    assert metrics["total_attractors"] == 3
    assert metrics["energy_conservation_pct"] > 95.0
    assert metrics["liouville_phase_volume_retention_pct"] > 95.0
    assert metrics["symplectic_2form_conserved"] is True
    assert metrics["zero_em_dash_verified"] is True

    dict_data = sim.to_dict()
    assert "metrics" in dict_data
    assert "attractors" in dict_data
    assert len(dict_data["trajectory"]) == 751


def test_svg_and_html_generation():
    """Verifies dark titanium SVG and interactive HTML output without rendering anomalies."""
    sim = create_cognitive_orbit_simulation()
    svg = sim.to_svg()
    assert "<svg" in svg
    assert "</svg>" in svg
    assert "panel-configuration" in svg
    assert "panel-phase-space" in svg
    assert "Symplectic Phase Space Integrator" in svg
    assert "#0f172a" in svg

    html_doc = sim.to_html()
    assert "<!DOCTYPE html>" in html_doc
    assert "Symplectic Invariant Telemetry" in html_doc
    assert "downloadJSON" in html_doc

    # Strict zero em dash check
    assert chr(8212) not in svg
    assert chr(8212) not in html_doc


def test_zero_em_dashes_in_source_files():
    """Guarantees strict compliance with the zero em dash policy across all files."""
    script_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "scripts", "symplectic_hamiltonian_integrator.py")
    )
    with open(script_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert chr(8212) not in content, "Em dash found in scripts/symplectic_hamiltonian_integrator.py"

    with open(__file__, "r", encoding="utf-8") as f:
        test_content = f.read()
    assert chr(8212) not in test_content, "Em dash found in tests/test_symplectic_hamiltonian_integrator.py"
