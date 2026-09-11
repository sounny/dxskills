"""
Unit tests for Geometric Quantization & Kostant-Souriau Prequantum Loom.
Verifies symplectic Poisson brackets, Hamiltonian vector fields,
Bohr-Sommerfeld action integral foliation, prequantum observables,
and zero em dash constraints.
"""

import unittest
import os
import math
from scripts.geometric_quantization_loom import (
    GeometricQuantizationLoom,
    BohrSommerfeldLeaf,
    PrequantumObservable,
    compute_poisson_bracket,
    hamiltonian_vector_field,
)


class TestGeometricQuantizationLoom(unittest.TestCase):
    """Test suite for GeometricQuantizationLoom and symplectic quantization."""

    def test_poisson_bracket_and_hamiltonian_vector_field(self):
        """Tests Poisson bracket canonical relations and Hamiltonian vector fields."""
        # Canonical coordinates {q, p} = 1
        f_q = lambda q, p: q
        g_p = lambda q, p: p
        pb = compute_poisson_bracket(f_q, g_p, 1.5, -0.8)
        self.assertAlmostEqual(pb, 1.0, places=4)

        # Skew-symmetry {p, q} = -1
        pb_skew = compute_poisson_bracket(g_p, f_q, 1.5, -0.8)
        self.assertAlmostEqual(pb_skew, -1.0, places=4)

        # Self Poisson bracket {f, f} = 0
        pb_self = compute_poisson_bracket(f_q, f_q, 2.0, 3.0)
        self.assertAlmostEqual(pb_self, 0.0, places=4)

        # Harmonic oscillator Hamiltonian H = 0.5 * p^2 + 0.5 * q^2
        h_func = lambda q, p: 0.5 * (p ** 2) + 0.5 * (q ** 2)
        # X_H = (dH/dp, -dH/dq) = (p, -q)
        v_q, v_p = hamiltonian_vector_field(h_func, 2.0, -1.5)
        self.assertAlmostEqual(v_q, -1.5, places=4)
        self.assertAlmostEqual(v_p, -2.0, places=4)

    def test_symplectic_orbit_integration(self):
        """Tests numerical symplectic leapfrog integration of classical orbits."""
        loom = GeometricQuantizationLoom(hbar=0.5, omega=1.0)
        traj, period, action = loom.integrate_orbit(q0=1.0, p0=0.0)

        self.assertGreater(len(traj), 10)
        self.assertGreater(period, 0.0)
        self.assertGreater(action, 0.0)

        # Harmonic period is approx 2 * pi for omega = 1 (modified slightly by anharmonicity)
        self.assertAlmostEqual(period, 2.0 * math.pi, delta=1.5)

    def test_bohr_sommerfeld_foliation(self):
        """Tests extraction of discrete quantized Bohr-Sommerfeld leaves."""
        loom = GeometricQuantizationLoom(hbar=0.5, omega=1.0)
        leaves = loom.compute_bohr_sommerfeld_foliation(max_quantum_levels=4)

        self.assertEqual(len(leaves), 4)

        # Monotonicity of actions and energies
        for i in range(len(leaves) - 1):
            self.assertLess(leaves[i].action_integral, leaves[i + 1].action_integral)
            self.assertLess(leaves[i].energy_level, leaves[i + 1].energy_level)

        # Check target action matching: I_n ~ (n + 0.5) * hbar
        for n, leaf in enumerate(leaves):
            target = (n + 0.5) * loom.hbar
            self.assertAlmostEqual(leaf.action_integral, target, delta=0.08)

    def test_geometric_quantization_result(self):
        """Tests complete diagnostic telemetry structure and serialization."""
        loom = GeometricQuantizationLoom(hbar=0.5)
        res = loom.compute_quantization()

        self.assertEqual(res.num_quantized_leaves, 5)
        self.assertGreater(res.zero_point_energy, 0.0)
        self.assertGreater(res.curvature_flux_integral, 0.0)
        self.assertGreater(res.dirac_groenewold_fidelity, 0.95)
        self.assertGreater(res.epistemic_coherence_index, 0.0)

        d = res.to_dict()
        self.assertIn("bohr_sommerfeld_leaves", d)
        self.assertIn("observables", d)
        self.assertIn("zero_point_energy", d)

    def test_svg_and_markdown_and_html_rendering(self):
        """Tests rendering of dark titanium SVG, Markdown report, and HTML application."""
        loom = GeometricQuantizationLoom()
        res = loom.compute_quantization()

        # 1. SVG
        svg = loom.render_svg(res)
        self.assertTrue(svg.startswith("<svg"))
        self.assertTrue(svg.strip().endswith("</svg>"))
        self.assertIn("GEOMETRIC QUANTIZATION", svg)
        self.assertIn("PHASE SPACE FOLIATION", svg)
        self.assertIn("QUANTIZATION SPECTRUM", svg)

        # 2. Markdown Report
        md = loom.generate_markdown_report(res)
        self.assertIn("# Geometric Quantization & Kostant-Souriau Prequantum Analysis", md)
        self.assertIn("Bohr-Sommerfeld Quantized Foliation", md)
        self.assertIn("Classical vs Prequantum Observables", md)

        # 3. HTML Viewer
        html_doc = loom.generate_html_viewer(res)
        self.assertIn("<!DOCTYPE html>", html_doc)
        self.assertIn("Diagnostic JSON Export", html_doc)

    def test_zero_em_dashes_constraint(self):
        """Strict negative constraint check: verify zero em dashes across code and tests."""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        files = [
            os.path.join(base_dir, "scripts", "geometric_quantization_loom.py"),
            os.path.join(base_dir, "tests", "test_geometric_quantization_loom.py"),
        ]
        for path in files:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertNotIn(chr(8212), content, f"Found em dash in {path}")


if __name__ == "__main__":
    unittest.main()
