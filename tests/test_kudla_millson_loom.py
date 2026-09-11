#!/usr/bin/env python3
"""
Unit tests for Kudla-Millson Forms and Arithmetic Cohomology Loom.
Verifies orthogonal space signatures, closed differential form properties,
modular weight calculations, Poincare duality pairings, and zero em dashes.

Strict constraint: Zero em dashes.
"""

import unittest
from scripts.kudla_millson_loom import (
    KudlaMillsonSpace,
    PoincareCyclePairing,
    KudlaMillsonResult,
    KudlaMillsonLoom,
    run_demo,
)


class TestKudlaMillsonLoom(unittest.TestCase):
    """Test suite for Kudla-Millson Loom."""

    def setUp(self):
        self.loom = KudlaMillsonLoom((2, 1))

    def test_space_signature_and_weight(self):
        """Verify space signature and modular weight k = (p + q) / 2."""
        res = self.loom.analyze()
        self.assertEqual(res.space.signature_p, 2)
        self.assertEqual(res.space.signature_q, 1)
        self.assertEqual(res.space.modular_weight, 1.5)
        self.assertEqual(res.space.symmetric_space_dim, 2)

    def test_form_closure_and_laplacian(self):
        """Verify Kudla-Millson differential form is closed and harmonic."""
        res = self.loom.analyze()
        self.assertTrue(res.form_closed)
        self.assertEqual(res.harmonic_laplacian_eigenvalue, 0.0)

    def test_poincare_duality_pairings(self):
        """Verify Poincare duality pairings match cycle intersection numbers."""
        res = self.loom.analyze(max_n=6)
        self.assertEqual(len(res.pairings), 6)

        for p in res.pairings:
            self.assertTrue(p.duality_match)
            self.assertLess(p.discrepancy, 1e-5)
            self.assertEqual(p.cycle_intersection_number, int(p.cohomology_pairing_value))

    def test_higher_signature_spaces(self):
        """Verify loom functions on signature (3, 2) space."""
        loom = KudlaMillsonLoom((3, 2))
        res = loom.analyze()
        self.assertEqual(res.space.signature_p, 3)
        self.assertEqual(res.space.signature_q, 2)
        self.assertEqual(res.space.modular_weight, 2.5)
        self.assertEqual(res.poincare_duality_status, "VERIFIED")

    def test_svg_rendering_and_zero_em_dashes(self):
        """Verify dark titanium SVG generation, contents, and zero em dashes."""
        res = self.loom.analyze()
        svg = self.loom.render_svg(res)

        self.assertIn("<svg", svg)
        self.assertIn("KUDLA-MILLSON FORMS", svg)
        self.assertIn("POINCARE DUALITY", svg)
        self.assertIn("COHOMOLOGY LATTICE", svg)
        self.assertNotIn("\u2014", svg)

        demo = run_demo((2, 1))
        self.assertEqual(demo["status"], "success")
        self.assertTrue(demo["form_closed"])
        self.assertEqual(demo["poincare_duality_status"], "VERIFIED")


if __name__ == "__main__":
    unittest.main()
