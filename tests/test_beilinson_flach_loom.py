#!/usr/bin/env python3
"""
Unit tests for Beilinson-Flach Elements and Asymmetric Euler Systems Loom.
Verifies Rankin-Selberg products, degree 4 Euler factors, Beilinson-Flach
norm-compatibility towers, explicit reciprocity evaluations, and dark titanium SVG output.

Strict constraint: Zero em dashes.
"""

import unittest
from scripts.beilinson_flach_loom import (
    ModularFormSpec,
    RankinSelbergConvolution,
    BeilinsonFlachClass,
    ReciprocityEvaluation,
    BeilinsonFlachLoom,
    run_demo,
)


class TestBeilinsonFlachLoom(unittest.TestCase):
    """Test suite for Beilinson-Flach Loom."""

    def setUp(self):
        self.loom = BeilinsonFlachLoom()

    def test_modular_forms_and_satake(self):
        """Verify Satake parameters alpha and beta satisfy Hecke relations."""
        f = self.loom.form_f
        alpha, beta = f.satake_parameters(2)
        # alpha + beta = a_2 = -2.0
        self.assertAlmostEqual((alpha + beta).real, -2.0, places=5)
        # alpha * beta = 2^{k-1} = 2^{2-1} = 2
        self.assertAlmostEqual((alpha * beta).real, 2.0, places=5)

    def test_rankin_selberg_convolution_and_euler_factors(self):
        """Verify degree 4 Euler factors for Rankin-Selberg product."""
        conv = self.loom.analyze_rankin_selberg()
        self.assertEqual(conv.conductor, 11 * 19)
        self.assertEqual(conv.central_critical_s, 1.5)
        self.assertGreater(conv.central_l_value, 0.0)

        # Check Euler polynomial at ell = 2
        p2 = conv.euler_factors[2]
        self.assertEqual(len(p2), 5)
        self.assertEqual(p2[0], 1.0)  # Leading constant coefficient is 1.0

    def test_beilinson_flach_tower(self):
        """Verify norm tower construction across modular curve levels."""
        levels = [1, 2, 3, 6]
        tower = self.loom.construct_beilinson_flach_tower(levels)
        self.assertEqual(len(tower), 4)
        for bf in tower:
            self.assertTrue(bf.is_non_zero)
            self.assertEqual(bf.cohomology_degree, 1)
            self.assertLess(bf.euler_compatibility_error, 1e-4)

    def test_explicit_reciprocity_and_selmer_bound(self):
        """Verify explicit reciprocity law and Selmer group finiteness."""
        rec = self.loom.evaluate_explicit_reciprocity(5)
        self.assertEqual(rec.prime_p, 5)
        self.assertTrue(rec.reciprocity_verified)
        self.assertEqual(rec.selmer_dimension_bound, 0)
        self.assertEqual(rec.sha_rankin_selberg_order, 1)

    def test_svg_rendering_and_demo(self):
        """Verify dark titanium SVG generation and zero em dashes."""
        svg = self.loom.render_svg()
        self.assertIn("<svg", svg)
        self.assertIn("BEILINSON-FLACH ELEMENTS", svg)
        self.assertIn("ASYMMETRIC EULER TOWER", svg)
        self.assertIn("EXPLICIT RECIPROCITY", svg)
        self.assertIn("SELMER BOUND", svg)
        self.assertNotIn("\u2014", svg)

        demo = run_demo()
        self.assertEqual(demo["status"], "success")
        self.assertIn("rankin_selberg", demo)
        self.assertIn("tower_levels", demo)


if __name__ == "__main__":
    unittest.main()
