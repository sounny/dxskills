#!/usr/bin/env python3
"""
Unit tests for Gross-Kohnen-Zagier (GKZ) Theorem and Higher Modular Forms Loom.
Verifies Kohnen plus space conditions, Fourier coefficients, canonical height pairings,
generating series modularity, and zero em dashes.

Strict constraint: Zero em dashes.
"""

import unittest
from scripts.gross_kohnen_zagier_loom import (
    KohnenFormSpec,
    HeegnerDiscriminantData,
    GKZHeightPairing,
    GKZAnalysisResult,
    GrossKohnenZagierLoom,
    run_demo,
)


class TestGrossKohnenZagierLoom(unittest.TestCase):
    """Test suite for Gross-Kohnen-Zagier Loom."""

    def setUp(self):
        self.loom = GrossKohnenZagierLoom("37a1")

    def test_kohnen_plus_space_condition(self):
        """Verify Fourier coefficients satisfy Kohnen condition -n = 0, 1 mod 4."""
        form = self.loom.kohnen_form
        # For d = -7: |-7| = 7 = 3 mod 4, so -7 = 1 mod 4 (valid)
        self.assertEqual(form.get_coeff(-7), 1.0)
        # For d = -11: |-11| = 11 = 3 mod 4 (valid)
        self.assertEqual(form.get_coeff(-11), -1.0)
        # For d = -5: |-5| = 5 = 1 mod 4 (not 0 or 3 mod 4, so vanishes in S_{3/2}^+)
        self.assertEqual(form.get_coeff(-5), 0.0)

    def test_proportionality_constant(self):
        """Verify kappa = L'(E,1) / (4 * pi * (f,f)) > 0."""
        self.assertGreater(self.loom.proportionality_c, 0.0)
        self.assertAlmostEqual(
            self.loom.proportionality_c,
            self.loom.l_derivative / (4.0 * 3.141592653589793 * self.loom.petersson_norm),
            places=5
        )

    def test_gkz_analysis_pairings(self):
        """Verify Gross-Kohnen-Zagier height pairings <P_d1, P_d2> match kappa * c(d1) * c(d2)."""
        res = self.loom.analyze([-7, -11, -19])
        self.assertEqual(len(res.discriminants), 3)
        self.assertEqual(len(res.pairings), 6)  # 3 * 4 / 2

        for pairing in res.pairings:
            self.assertTrue(pairing.exact_match)
            self.assertLess(pairing.relative_discrepancy, 1e-4)

    def test_multiple_curves(self):
        """Verify loom functions across multiple elliptic curves."""
        for label in ["11a1", "37a1", "389a1"]:
            loom = GrossKohnenZagierLoom(label)
            res = loom.analyze()
            self.assertEqual(res.curve_label, label)
            self.assertGreater(res.conductor_n, 0)
            self.assertTrue(res.generating_series_modularity_proven)

    def test_svg_rendering_and_zero_em_dashes(self):
        """Verify dark titanium SVG rendering, validity, and zero em dashes."""
        res = self.loom.analyze()
        svg = self.loom.render_svg(res)

        self.assertIn("<svg", svg)
        self.assertIn("GROSS-KOHNEN-ZAGIER", svg)
        self.assertIn("SHIMURA-KOHNEN LIFT", svg)
        self.assertIn("GKZ HEIGHT FORMULA", svg)
        self.assertIn("GENERATING SERIES", svg)
        self.assertNotIn("\u2014", svg)

        demo = run_demo("37a1")
        self.assertEqual(demo["status"], "success")
        self.assertTrue(demo["modularity_proven"])


if __name__ == "__main__":
    unittest.main()
