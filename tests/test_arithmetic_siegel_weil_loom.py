#!/usr/bin/env python3
"""
Unit tests for Arithmetic Siegel-Weil Formula Loom.
Verifies orthogonal Shimura spaces, incoherent Eisenstein series central vanishing,
arithmetic special cycles (Kudla-Rapoport), arithmetic degrees, and zero em dashes.

Strict constraint: Zero em dashes.
"""

import unittest
from scripts.arithmetic_siegel_weil_loom import (
    QuadraticSpaceSpec,
    ArithmeticCycleData,
    EisensteinDerivativeCoeff,
    KudlaProgramResult,
    KudlaProgramLoom,
    run_demo,
)


class TestArithmeticSiegelWeilLoom(unittest.TestCase):
    """Test suite for Arithmetic Siegel-Weil Loom."""

    def setUp(self):
        self.loom = KudlaProgramLoom("shimura_curve")

    def test_quadratic_space_and_central_vanishing(self):
        """Verify orthogonal Shimura space signature and central incoherent vanishing."""
        res = self.loom.analyze()
        self.assertEqual(res.space.signature_p, 1)
        self.assertEqual(res.space.signature_q, 2)
        self.assertEqual(res.space.dimension, 3)
        self.assertTrue(res.central_point_vanishing_verified)

    def test_arithmetic_cycles_decomposition(self):
        """Verify arithmetic degree decomposes into archimedean and non-archimedean parts."""
        res = self.loom.analyze([1, 2, 3])
        self.assertEqual(len(res.cycles), 3)

        for c in res.cycles:
            self.assertGreater(c.total_arithmetic_degree, 0.0)
            self.assertAlmostEqual(
                c.total_arithmetic_degree,
                c.archimedean_green_contribution + c.non_archimedean_intersection,
                places=4
            )

    def test_arithmetic_siegel_weil_matching(self):
        """Verify arithmetic degrees match central derivative Eisenstein coefficients."""
        res = self.loom.analyze([1, 2, 3, 5])
        self.assertEqual(len(res.eisenstein_coeffs), 4)

        for coeff in res.eisenstein_coeffs:
            self.assertTrue(coeff.arithmetic_siegel_weil_match)
            self.assertLess(coeff.discrepancy, 1e-4)

    def test_hilbert_surface_model(self):
        """Verify loom functions on Hilbert modular surface V(2,2)."""
        loom = KudlaProgramLoom("hilbert_surface")
        res = loom.analyze()
        self.assertEqual(res.space.signature_p, 2)
        self.assertEqual(res.space.signature_q, 2)
        self.assertEqual(res.space.eisenstein_weight, 2.0)
        self.assertEqual(res.kudla_conjecture_status, "VERIFIED")

    def test_svg_rendering_and_zero_em_dashes(self):
        """Verify dark titanium SVG generation, contents, and zero em dashes."""
        res = self.loom.analyze()
        svg = self.loom.render_svg(res)

        self.assertIn("<svg", svg)
        self.assertIn("KUDLA PROGRAM", svg)
        self.assertIn("ARITHMETIC SIEGEL-WEIL", svg)
        self.assertIn("FALTINGS HEIGHTS", svg)
        self.assertNotIn("\u2014", svg)

        demo = run_demo("shimura_curve")
        self.assertEqual(demo["status"], "success")
        self.assertTrue(demo["central_vanishing"])
        self.assertEqual(demo["kudla_status"], "VERIFIED")


if __name__ == "__main__":
    unittest.main()
