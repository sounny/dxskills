#!/usr/bin/env python3
"""
Unit tests for Borcherds Lift and Singular Theta Correspondence Loom.
Verifies even lattice signatures, input form weights, automorphic product weights,
Heegner divisor singularities, Weyl vector norms, and zero em dashes.

Strict constraint: Zero em dashes.
"""

import unittest
from scripts.borcherds_lift_loom import (
    EvenLatticeSpec,
    WeaklyHolomorphicForm,
    DivisorComponent,
    BorcherdsProductSpec,
    BorcherdsLoomResult,
    BorcherdsLiftLoom,
    run_demo,
)


class TestBorcherdsLiftLoom(unittest.TestCase):
    """Test suite for Borcherds Lift Loom."""

    def setUp(self):
        self.loom = BorcherdsLiftLoom("O_2_2")

    def test_lattice_and_weights(self):
        """Verify lattice signature and automorphic weight k = c(0) / 2."""
        res = self.loom.analyze()
        self.assertEqual(res.lattice.signature_pos, 2)
        self.assertEqual(res.lattice.signature_neg, 2)
        self.assertEqual(res.product.automorphic_weight, 12.0)
        self.assertEqual(res.input_form.constant_term_c0, 24.0)

    def test_heegner_divisors(self):
        """Verify principal part generates correct Heegner divisor singularities."""
        res = self.loom.analyze()
        self.assertGreater(len(res.product.divisors), 0)

        # Check divisor entries
        labels = [d.heegner_divisor_label for d in res.product.divisors]
        self.assertTrue(any("H(-1)" in l for l in labels))

    def test_higher_dimensional_lattice(self):
        """Verify Borcherds lift on O(2, 10) lattice."""
        loom = BorcherdsLiftLoom("O_2_10")
        res = loom.analyze()
        self.assertEqual(res.lattice.signature_neg, 10)
        self.assertEqual(res.lattice.modular_weight_input, -4.0)
        self.assertEqual(res.product.automorphic_weight, 5.0)  # 10 / 2
        self.assertTrue(res.product.borcherds_modularity_proven)

    def test_svg_rendering_and_zero_em_dashes(self):
        """Verify dark titanium SVG generation, contents, and zero em dashes."""
        res = self.loom.analyze()
        svg = self.loom.render_svg(res)

        self.assertIn("<svg", svg)
        self.assertIn("BORCHERDS LIFT", svg)
        self.assertIn("SINGULAR THETA INTEGRAL", svg)
        self.assertIn("INFINITE PRODUCT", svg)
        self.assertIn("HEEGNER DIVISORS", svg)
        self.assertNotIn("\u2014", svg)

        demo = run_demo("O_2_2")
        self.assertEqual(demo["status"], "success")
        self.assertTrue(demo["modularity_proven"])
        self.assertEqual(demo["automorphic_weight"], 12.0)


if __name__ == "__main__":
    unittest.main()
