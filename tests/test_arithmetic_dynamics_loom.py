"""
Unit tests for Arithmetic Dynamics & Post-Critically Finite Julia-Fatou Loom.
Strictly verifies zero em dashes (chr(8212)), PCF critical orbit cycles,
Call-Silverman canonical heights, Julia-Fatou partitions, and Berkovich trees.
"""

import unittest
import os
import json
from scripts.arithmetic_dynamics_loom import (
    ArithmeticDynamicsLoom,
    MapFamily,
    DynamicalLocus,
    BerkovichNodeType,
)


class TestArithmeticDynamicsLoom(unittest.TestCase):
    """Test suite for ArithmeticDynamicsLoom engine and spatial cognitive mappings."""

    def setUp(self):
        self.loom = ArithmeticDynamicsLoom(
            family=MapFamily.MISIUREWICZ_QUADRATIC.value,
            parameter_c=-2.0,
            degree=2,
        )

    def test_rational_map_initialization_and_pcf(self):
        """Verify Misiurewicz quadratic critical orbits and PCF finiteness."""
        m = self.loom.rational_maps[0]
        self.assertEqual(m.degree, 2)
        self.assertAlmostEqual(m.parameter_c, -2.0)
        self.assertTrue(m.is_post_critically_finite)
        self.assertIn("crit_0", m.post_critical_orbits)

        # Orbit of 0 for c = -2: 0 -> -2 -> 2 -> 2
        orb = m.post_critical_orbits["crit_0"]
        self.assertAlmostEqual(orb[0], 0.0)
        self.assertAlmostEqual(orb[1], -2.0)
        self.assertAlmostEqual(orb[2], 2.0)
        self.assertAlmostEqual(orb[3], 2.0)

        # Chebyshev map test
        cheb_loom = ArithmeticDynamicsLoom(
            family=MapFamily.CHEBYSHEV_POLYNOMIAL.value,
            degree=2,
        )
        cm = cheb_loom.rational_maps[0]
        self.assertTrue(cm.is_post_critically_finite)

    def test_canonical_height_evaluation(self):
        """Verify Call-Silverman height vanishes on preperiodic points."""
        # Preperiodic point at x = 0.0
        h_preper = self.loom.compute_canonical_height("PT-01", coordinate_x=0.0)
        self.assertEqual(h_preper.canonical_height, 0.0)
        self.assertTrue(h_preper.is_preperiodic)

        # Wandering point at x = 10.0
        h_wander = self.loom.compute_canonical_height("PT-02", coordinate_x=10.0)
        self.assertGreater(h_wander.canonical_height, 0.0)
        self.assertFalse(h_wander.is_preperiodic)

    def test_julia_fatou_partition(self):
        """Verify Julia dimension and connectivity across parameters."""
        part = self.loom.evaluate_julia_fatou_partition("PART-01")
        self.assertEqual(part.julia_box_dimension, 1.0)
        self.assertTrue(part.is_julia_connected)
        self.assertFalse(part.is_julia_cantor_dust)

        # Cantor dust test for c = -3.0
        dust_loom = ArithmeticDynamicsLoom(
            family=MapFamily.MISIUREWICZ_QUADRATIC.value,
            parameter_c=-3.0,
        )
        d_part = dust_loom.evaluate_julia_fatou_partition("PART-DUST")
        self.assertFalse(d_part.is_julia_connected)
        self.assertTrue(d_part.is_julia_cantor_dust)

    def test_berkovich_tree_construction(self):
        """Verify non-archimedean Berkovich tree properties and Gauss point."""
        tree = self.loom.construct_berkovich_tree("TREE-01", prime_p=2, depth=3)
        self.assertEqual(tree.prime_p, 2)
        self.assertEqual(tree.tree_depth, 3)
        self.assertIn("Gauss", tree.gauss_point_id)
        self.assertIn("Good Reduction", tree.reduction_type)

    def test_svg_json_and_zero_em_dashes(self):
        """Verify SVG generation, JSON export, and strict zero em dash compliance."""
        self.loom.compute_canonical_height("PT-TEST", coordinate_x=0.0)
        self.loom.evaluate_julia_fatou_partition("PART-TEST")
        self.loom.construct_berkovich_tree("TREE-TEST")

        svg = self.loom.generate_dynamics_svg()
        self.assertTrue(svg.startswith("<svg"))
        self.assertTrue(svg.endswith("</svg>"))
        self.assertIn("Arithmetic Dynamics", svg)
        self.assertIn("Julia-Fatou", svg)
        self.assertIn("Call-Silverman", svg)

        # Assert ZERO em dashes anywhere in generated SVG
        self.assertNotIn(chr(8212), svg)

        # Assert ZERO em dashes in JSON export
        json_data = self.loom.to_json()
        self.assertNotIn(chr(8212), json_data)

        # Verify source file has zero em dashes
        loom_path = os.path.join(os.path.dirname(__file__), "..", "scripts", "arithmetic_dynamics_loom.py")
        with open(loom_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertNotIn(chr(8212), content)


if __name__ == "__main__":
    unittest.main()
