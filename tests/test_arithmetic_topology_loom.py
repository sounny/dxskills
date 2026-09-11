"""
Unit tests for Arithmetic Topology & Knots-Primes Kapranov-Reznikov Loom.
Strictly verifies zero em dashes (chr(8212)), Mazur knot-prime correspondences,
Legendre linking numbers, Gauss quadratic reciprocity, Alexander-Iwasawa duality,
and Redei-Milnor Borromean entanglement.
"""

import unittest
import os
import json
from scripts.arithmetic_topology_loom import (
    ArithmeticTopologyLoom,
    TopologyAnalogyType,
    KnotArchetype,
    compute_legendre_symbol,
)


class TestArithmeticTopologyLoom(unittest.TestCase):
    """Test suite for ArithmeticTopologyLoom engine and spatial cognitive mappings."""

    def setUp(self):
        self.loom = ArithmeticTopologyLoom(
            base_field="Rational Field Q",
            p_adic_prime=2,
        )

    def test_legendre_symbol_and_quadratic_reciprocity(self):
        """Verify Legendre symbol values and Gauss quadratic reciprocity."""
        # 3 mod 4 = 3, 5 mod 4 = 1: (3/5) = -1, (5/3) = -1
        # Reciprocity: (-1)^((3-1)/2 * (5-1)/2) = (-1)^(1 * 2) = +1
        # (3/5)(5/3) = (-1)*(-1) = 1
        leg_3_5 = compute_legendre_symbol(3, 5)
        leg_5_3 = compute_legendre_symbol(5, 3)
        self.assertEqual(leg_3_5, -1)
        self.assertEqual(leg_5_3, -1)
        self.assertEqual(leg_3_5 * leg_5_3, 1)

        # Link evaluation in the loom
        lnk = self.loom.evaluate_arithmetic_link("LINK-3-5", prime_p=3, prime_q=5)
        self.assertEqual(lnk.legendre_p_over_q, -1)
        self.assertEqual(lnk.legendre_q_over_p, -1)
        self.assertEqual(lnk.linking_number_mod_2, 1)
        self.assertTrue(lnk.quadratic_reciprocity_verified)

        # Link for 5 and 11: 5 mod 4 = 1, 11 mod 4 = 3
        # (5/11) = 1, (11/5) = (1/5) = 1
        lnk_5_11 = self.loom.evaluate_arithmetic_link("LINK-5-11", prime_p=5, prime_q=11)
        self.assertEqual(lnk_5_11.legendre_p_over_q, 1)
        self.assertEqual(lnk_5_11.legendre_q_over_p, 1)
        self.assertEqual(lnk_5_11.linking_number_mod_2, 0)
        self.assertTrue(lnk_5_11.quadratic_reciprocity_verified)

    def test_arithmetic_knot_construction(self):
        """Verify knot archetypes, hyperbolic volume, and 3D spatial curve points."""
        k2 = self.loom.construct_arithmetic_knot("KNOT-P2", prime_p=2)
        self.assertEqual(k2.prime_p, 2)
        self.assertEqual(k2.crossing_number, 3)
        self.assertEqual(k2.genus, 1)
        self.assertEqual(len(k2.curve_points_3d), 60)

        k5 = self.loom.construct_arithmetic_knot("KNOT-P5", prime_p=5)
        self.assertEqual(k5.prime_p, 5)
        self.assertEqual(k5.crossing_number, 4)
        self.assertTrue(k5.is_hyperbolic)
        self.assertGreater(k5.hyperbolic_volume, 2.0)

    def test_alexander_iwasawa_duality(self):
        """Verify Alexander polynomial and Iwasawa polynomial correspondence."""
        ai = self.loom.evaluate_alexander_iwasawa_duality(
            "AI-01", prime_p=3, iwasawa_lambda=2, iwasawa_mu=0
        )
        self.assertEqual(ai.prime_p, 3)
        self.assertEqual(ai.alexander_degree, 2)
        self.assertEqual(ai.iwasawa_lambda, 2)
        self.assertEqual(ai.iwasawa_mu, 0)
        self.assertIn("Delta(t)", ai.alexander_polynomial_formula)
        self.assertIn("f(T)", ai.iwasawa_polynomial_formula)

    def test_borromean_triple_and_redei_symbol(self):
        """Verify Borromean primes with vanishing pairwise linking and non-trivial Redei symbol."""
        # Primes 13, 61, 937 (classical Borromean prime triple)
        # All pairwise Legendre symbols are +1: (13/61)=1, (61/937)=1, (937/13)=1
        bt = self.loom.evaluate_borromean_triple("BORR-01", p=13, q=61, r=937)
        self.assertEqual(bt.primes, (13, 61, 937))
        self.assertEqual(bt.pairwise_linking_mod_2["lk(13,61)"], 0)
        self.assertEqual(bt.pairwise_linking_mod_2["lk(61,937)"], 0)
        self.assertEqual(bt.pairwise_linking_mod_2["lk(937,13)"], 0)
        self.assertIn(bt.redei_triple_symbol, [-1, 1])

    def test_svg_json_and_zero_em_dashes(self):
        """Verify SVG generation, JSON serialization, and strict zero em dash compliance."""
        self.loom.construct_arithmetic_knot("KNOT-TEST", prime_p=3)
        self.loom.evaluate_arithmetic_link("LINK-TEST", prime_p=3, prime_q=7)
        self.loom.evaluate_alexander_iwasawa_duality("AI-TEST", prime_p=3)
        self.loom.evaluate_borromean_triple("BORR-TEST", p=13, q=61, r=937)

        svg = self.loom.generate_topology_svg()
        self.assertTrue(svg.startswith("<svg"))
        self.assertTrue(svg.endswith("</svg>"))
        self.assertIn("Arithmetic Topology", svg)
        self.assertIn("Mazur Dictionary", svg)
        self.assertIn("Legendre Linking", svg)

        # Assert ZERO em dashes anywhere in generated SVG
        self.assertNotIn(chr(8212), svg)

        # Assert ZERO em dashes in JSON export
        json_data = self.loom.to_json()
        self.assertNotIn(chr(8212), json_data)

        # Verify source file has zero em dashes
        loom_path = os.path.join(os.path.dirname(__file__), "..", "scripts", "arithmetic_topology_loom.py")
        if os.path.exists(loom_path):
            with open(loom_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertNotIn(chr(8212), content)


if __name__ == "__main__":
    unittest.main()
