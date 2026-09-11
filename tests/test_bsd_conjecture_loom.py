#!/usr/bin/env python3
"""
Unit tests for Birch-Swinnerton-Dyer (BSD) Conjecture and Heegner Points Loom.
Zero em dashes strictly enforced.
"""

import unittest
from scripts.bsd_conjecture_loom import (
    BSDConjectureLoom,
    EllipticCurveInvariants,
    HeegnerPointData,
    BSDBalanceState,
    BSDConjectureResult,
)


class TestBSDConjectureLoom(unittest.TestCase):
    """Test suite for BSDConjectureLoom mathematical and cognitive capabilities."""

    def setUp(self) -> None:
        self.rank0_loom = BSDConjectureLoom("11a1")
        self.rank1_loom = BSDConjectureLoom("37a1")
        self.rank2_loom = BSDConjectureLoom("389a1")

    def test_curve_invariants(self) -> None:
        """Verify elliptic curve invariants and torsion order."""
        c0 = self.rank0_loom.curve
        self.assertEqual(c0.conductor_n, 11)
        self.assertEqual(c0.torsion_order, 5)
        self.assertGreater(c0.real_period_omega, 1.0)

        c1 = self.rank1_loom.curve
        self.assertEqual(c1.conductor_n, 37)
        self.assertEqual(c1.torsion_order, 1)

    def test_bsd_balance_rank0_and_rank1(self) -> None:
        """Verify analytic LHS vs arithmetic RHS balance."""
        bsd0 = self.rank0_loom.evaluate_bsd_balance()
        self.assertIsInstance(bsd0, BSDBalanceState)
        self.assertEqual(bsd0.analytic_rank, 0)
        self.assertEqual(bsd0.root_number, 1)
        self.assertTrue(bsd0.exact_match)
        self.assertAlmostEqual(bsd0.bsd_ratio, 1.0, places=5)

        bsd1 = self.rank1_loom.evaluate_bsd_balance()
        self.assertEqual(bsd1.analytic_rank, 1)
        self.assertEqual(bsd1.root_number, -1)
        self.assertTrue(bsd1.exact_match)
        self.assertAlmostEqual(bsd1.bsd_ratio, 1.0, places=5)

    def test_heegner_point_gross_zagier(self) -> None:
        """Verify Gross-Zagier canonical height and infinite order."""
        hp0 = self.rank0_loom.compute_heegner_point()
        self.assertFalse(hp0.has_infinite_order)
        self.assertEqual(hp0.canonical_height, 0.0)

        hp1 = self.rank1_loom.compute_heegner_point()
        self.assertTrue(hp1.has_infinite_order)
        self.assertGreater(hp1.canonical_height, 0.0)
        self.assertGreater(hp1.gross_zagier_derivative, 0.0)

    def test_l_function_taylor_profile(self) -> None:
        """Verify L-function profile points and central critical vanishing."""
        prof1 = self.rank1_loom.generate_l_function_profile(points=21)
        self.assertEqual(len(prof1), 21)

        # Midpoint at index 10 corresponds to s = 1.0
        s_mid, l_mid = prof1[10]
        self.assertAlmostEqual(s_mid, 1.0, places=5)
        # For rank 1 curve, L(1) = 0
        self.assertAlmostEqual(l_mid, 0.0, places=5)

    def test_complete_analysis_and_svg_rendering(self) -> None:
        """Verify complete pipeline, zero em dashes, and SVG generation."""
        res = self.rank1_loom.analyze()
        self.assertIsInstance(res, BSDConjectureResult)
        self.assertTrue(res.bsd_proven_rank_le_1)

        svg = self.rank1_loom.render_svg(res)
        self.assertIn("<svg", svg)
        self.assertIn("BIRCH-SWINNERTON-DYER", svg)
        self.assertIn("PANEL A:", svg)
        self.assertIn("PANEL B:", svg)
        self.assertIn("PANEL C:", svg)
        self.assertIn("PANEL D:", svg)
        self.assertNotIn("\u2014", svg, "Em dash detected in generated SVG")


if __name__ == "__main__":
    unittest.main()
