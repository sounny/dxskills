r"""
Unit tests for Coleman Families & Overconvergent Modular Forms Loom.
Verifies Banach spaces, Fredholm determinants, Coleman classicality,
and strictly zero em dashes (chr(8212)).
"""

import unittest
import os
import sys

# Add scripts directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))

from coleman_family_loom import (
    ColemanFamilyLoom,
    ColemanFamilyArchetype,
)


class TestColemanFamilyLoom(unittest.TestCase):
    """Test suite for Coleman Families & Overconvergent Modular Forms Loom."""

    def setUp(self):
        self.loom = ColemanFamilyLoom(
            level_n=1,
            prime_p=2,
            weight_k=4,
            default_archetype=ColemanFamilyArchetype.COLEMAN_MAZUR_EIGENCURVE.value,
        )

    def test_overconvergent_banach_space(self):
        """Test overconvergent module parameters and U_p compactness."""
        self.assertEqual(len(self.loom.spaces), 1)
        sp = self.loom.spaces[0]
        self.assertEqual(sp.level_n, 1)
        self.assertEqual(sp.prime_p, 2)
        self.assertEqual(sp.weight_k, 4)
        self.assertTrue(sp.is_u_p_compact)
        self.assertGreater(sp.overconvergence_radius_r, 0.0)

    def test_fredholm_determinant_and_newton_polygon(self):
        """Test Fredholm series entireness and Newton polygon vertices."""
        self.assertEqual(len(self.loom.fredholm_series), 1)
        fred = self.loom.fredholm_series[0]
        self.assertTrue(fred.is_entire_function)
        self.assertGreaterEqual(len(fred.newton_polygon_vertices), 2)

        slopes = self.loom.compute_newton_polygon_slopes(test_degree=4)
        self.assertEqual(len(slopes), 4)
        self.assertEqual(slopes[0], 0.0)

    def test_coleman_classicality_threshold(self):
        """Test Coleman's classicality condition alpha < k - 1."""
        self.assertEqual(len(self.loom.eigencurve_points), 1)
        pt = self.loom.eigencurve_points[0]
        self.assertTrue(pt.is_strictly_classical)

        eval_res = self.loom.evaluate_classicality_threshold(slope=1.5, weight=4)
        self.assertEqual(eval_res["critical_bound"], 3)
        self.assertTrue(eval_res["is_strictly_classical"])

        eval_phantom = self.loom.evaluate_classicality_threshold(slope=3.5, weight=4)
        self.assertFalse(eval_phantom["is_strictly_classical"])
        self.assertTrue(eval_phantom["phantom_overconvergent"])

    def test_critical_and_ramanujan_archetypes(self):
        """Test critical slope alpha = k - 1 and Ramanujan slope families."""
        crit_loom = ColemanFamilyLoom(
            weight_k=4,
            default_archetype=ColemanFamilyArchetype.CRITICAL_SLOPE_K_MINUS_1.value,
        )
        self.assertFalse(crit_loom.eigencurve_points[0].is_strictly_classical)

        ram_loom = ColemanFamilyLoom(
            default_archetype=ColemanFamilyArchetype.RAMANUJAN_SLOPE_FAMILY.value,
        )
        self.assertEqual(ram_loom.spaces[0].weight_k, 12)
        self.assertTrue(ram_loom.eigencurve_points[0].is_strictly_classical)

    def test_svg_generation_and_zero_em_dashes(self):
        """Verify dark titanium SVG generation and zero em dashes across script and tests."""
        svg = self.loom.generate_coleman_svg()
        self.assertIn("<svg", svg)
        self.assertIn("Coleman Families &amp; Overconvergent Modular Forms Loom", svg)
        self.assertIn("U_p", svg)
        self.assertIn("Eigencurve", svg)

        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts", "coleman_family_loom.py"))
        if os.path.exists(script_path):
            with open(script_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertNotIn("\u2014", content, "Found em dash in coleman_family_loom.py")

        with open(__file__, "r", encoding="utf-8") as f:
            test_content = f.read()
        self.assertNotIn("\u2014", test_content, "Found em dash in test_coleman_family_loom.py")


if __name__ == "__main__":
    unittest.main()
