"""
Tests for Non-Abelian Chabauty & Kim Motivic Fundamental Group Loom.
Verifies unipotent Selmer variety dimension gaps, p-adic iterated Coleman integrals,
effective Diophantine bounding of rational points, and strict zero em dash compliance.
"""

import unittest
from scripts.non_abelian_chabauty_loom import (
    NonAbelianChabautyLoom,
    ChabautyDepthArchetype,
    SelmerVarietyData,
    PAdicIteratedIntegralData,
    RationalPointBoundData,
)


class TestNonAbelianChabautyLoom(unittest.TestCase):
    """Test suite for NonAbelianChabautyLoom algorithms and visualizers."""

    def setUp(self):
        self.loom = NonAbelianChabautyLoom(
            curve_genus=2,
            mordell_weil_rank=2,
            prime_p=7,
            unipotent_depth=2,
            default_archetype=ChabautyDepthArchetype.DEPTH_2_QUADRATIC_CHABAUTY.value,
        )

    def test_selmer_variety_dimensions_and_gap(self):
        """Verify unipotent Selmer variety local and global dimensions and gap."""
        self.assertGreaterEqual(len(self.loom.selmer_records), 1)
        sel = self.loom.selmer_records[0]
        self.assertIsInstance(sel, SelmerVarietyData)
        self.assertEqual(sel.curve_genus, 2)
        self.assertEqual(sel.mordell_weil_rank, 2)
        self.assertEqual(sel.unipotent_depth_n, 2)
        # Global dim = r = 2
        self.assertEqual(sel.global_selmer_dim, 2)
        # Local dim = g + (n - 1) = 2 + 1 = 3
        self.assertEqual(sel.local_selmer_dim, 3)
        # Gap = 3 - 2 = 1 > 0
        self.assertEqual(sel.dimension_gap, 1)
        self.assertTrue(sel.cutting_equations_exist)

    def test_iterated_coleman_integrals(self):
        """Verify p-adic iterated Coleman integrals and convergence."""
        self.assertGreaterEqual(len(self.loom.iterated_integrals), 2)
        int1 = self.loom.iterated_integrals[0]
        self.assertEqual(int1.depth, 1)
        self.assertTrue(int1.is_coleman_convergent)

        int2 = self.loom.iterated_integrals[1]
        self.assertEqual(int2.depth, 2)
        self.assertTrue(int2.is_coleman_convergent)

        # Dynamic calculation of depth 3 integral
        int3 = self.loom.compute_iterated_integral("INT-TEST-DEPTH3", depth=3)
        self.assertEqual(int3.depth, 3)
        self.assertTrue(int3.is_coleman_convergent)
        self.assertGreater(int3.local_evaluation_value, 0.0)

    def test_rational_point_bounding(self):
        """Verify Chabauty-Kim cutting locus bounds on X(Q)."""
        self.assertGreaterEqual(len(self.loom.rational_bounds), 1)
        bnd = self.loom.rational_bounds[0]
        self.assertIsInstance(bnd, RationalPointBoundData)
        self.assertEqual(bnd.prime_p, 7)
        self.assertEqual(bnd.finite_annihilating_locus_size, 6)
        self.assertEqual(bnd.verified_rational_points_count, 4)
        self.assertEqual(bnd.chabauty_kim_status, "PROVED_FINITE")
        self.assertIn("infty", bnd.rational_points_sample)

    def test_higher_depth_selmer_evaluation(self):
        """Verify Selmer variety behavior at depth n = 3."""
        sel3 = self.loom.evaluate_selmer_variety(target_depth=3)
        self.assertIsInstance(sel3, SelmerVarietyData)
        self.assertEqual(sel3.unipotent_depth_n, 3)
        # Local dim = g + (n - 1) = 2 + 2 = 4
        self.assertEqual(sel3.local_selmer_dim, 4)
        # Global dim = r = 2
        self.assertEqual(sel3.global_selmer_dim, 2)
        # Gap = 4 - 2 = 2
        self.assertEqual(sel3.dimension_gap, 2)
        self.assertTrue(sel3.cutting_equations_exist)

    def test_svg_and_zero_em_dash_compliance(self):
        """Verify dark titanium SVG rendering, JSON telemetry, and zero em dashes."""
        self.loom.evaluate_selmer_variety(target_depth=2)

        svg = self.loom.generate_chabauty_svg()
        self.assertIsInstance(svg, str)
        self.assertTrue(svg.startswith("<svg"))
        self.assertTrue(svg.endswith("</svg>"))
        self.assertIn("Non-Abelian Chabauty", svg)
        self.assertIn("Selmer Varieties", svg)
        self.assertIn("p-Adic Iterated Coleman Integrals", svg)
        self.assertIn("Annihilating Locus X(Q_p)_n", svg)

        # Strict zero em dash verification
        self.assertNotIn("\u2014", svg)
        self.assertNotIn(chr(8212), svg)

        json_str = self.loom.to_json()
        self.assertNotIn("\u2014", json_str)
        self.assertNotIn(chr(8212), json_str)

        with open("scripts/non_abelian_chabauty_loom.py", encoding="utf-8") as f:
            src = f.read()
        self.assertNotIn("\u2014", src)
        self.assertNotIn(chr(8212), src)


if __name__ == "__main__":
    unittest.main()
