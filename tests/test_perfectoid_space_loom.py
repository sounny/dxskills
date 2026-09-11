"""
Unit tests for Perfectoid Spaces & Fargues-Fontaine Curve Loom.
Strictly verifies zero em dashes (chr(8212)), Scholze tilting equivalence,
Huber adic spaces, and Fargues-Fontaine Harder-Narasimhan slope polygons.
"""

import unittest
import os
import json
from scripts.perfectoid_space_loom import (
    PerfectoidSpaceLoom,
    PerfectoidCharacteristic,
    FontainePeriodRing,
    HarderNarasimhanClassification,
)


class TestPerfectoidSpaceLoom(unittest.TestCase):
    """Test suite for PerfectoidSpaceLoom engine and spatial cognitive mappings."""

    def setUp(self):
        self.loom = PerfectoidSpaceLoom(prime_p=2, base_field_name="C_p (p-Adic Complex Completion)")

    def test_field_initialization_and_tilting(self):
        """Verify perfectoid field characteristics and tilt properties."""
        f = self.loom.fields[0]
        self.assertEqual(f.prime_p, 2)
        self.assertEqual(f.characteristic_type, PerfectoidCharacteristic.MIXED_CHAR.value)
        self.assertTrue(f.frobenius_surjective)
        self.assertIn("F_2", f.tilt_field_name)

        # Higher prime test
        p3_loom = PerfectoidSpaceLoom(prime_p=3, base_field_name="Q_p(3^(1/3^infty))")
        f3 = p3_loom.fields[0]
        self.assertEqual(f3.prime_p, 3)
        self.assertIn("F_3", f3.tilt_field_name)

    def test_adic_space_construction(self):
        """Verify Huber adic space continuous valuation spectra."""
        space = self.loom.construct_adic_space("SPA-01", huber_pair="(C_p, O_Cp)", dimension=1)
        self.assertEqual(space.space_id, "SPA-01")
        self.assertEqual(space.valuation_dimension, 1)
        self.assertEqual(space.huber_pair, "(C_p, O_Cp)")
        self.assertEqual(space.non_archimedean_radius, 1.0)

    def test_fargues_fontaine_curve_classification(self):
        """Verify vector bundle slope decomposition and Harder-Narasimhan polygon."""
        curve = self.loom.synthesize_fargues_fontaine_curve("X-FF-01", bundle_slopes=[2.0, 1.0, 0.5, 0.0])
        self.assertEqual(curve.curve_id, "X-FF-01")
        self.assertTrue(curve.is_geometrically_connected)
        self.assertEqual(len(curve.vector_bundles), 4)

        # Check sorted slopes descending
        self.assertEqual(curve.slopes, [2.0, 1.0, 0.5, 0.0])

        # Check Harder-Narasimhan polygon points
        pts = curve.hn_polygon_points
        self.assertEqual(pts[0], (0, 0))
        # First segment: slope 2.0 (rank 1, deg 2) -> (1, 2)
        self.assertEqual(pts[1], (1, 2))
        # Second segment: slope 1.0 (rank 1, deg 1) -> (2, 3)
        self.assertEqual(pts[2], (2, 3))
        # Third segment: slope 0.5 (rank 2, deg 1) -> (4, 4)
        self.assertEqual(pts[3], (4, 4))
        # Fourth segment: slope 0.0 (rank 1, deg 0) -> (5, 4)
        self.assertEqual(pts[4], (5, 4))

    def test_tilting_equivalence(self):
        """Verify Scholze tilting equivalence between Perf(K) and Perf(K^flat)."""
        equiv = self.loom.compute_tilting_equivalence("TILTING-01")
        self.assertTrue(equiv.category_equivalence_verified)
        self.assertEqual(equiv.almost_mathematics_defect, 0.0)
        self.assertIn("C_p", equiv.until_field)

    def test_svg_json_and_zero_em_dashes(self):
        """Verify SVG generation, JSON export, and strict zero em dash compliance."""
        self.loom.construct_adic_space("SPA-TEST")
        self.loom.synthesize_fargues_fontaine_curve("X-FF-TEST")
        self.loom.compute_tilting_equivalence("TILTING-TEST")

        svg = self.loom.generate_perfectoid_svg()
        self.assertTrue(svg.startswith("<svg"))
        self.assertTrue(svg.endswith("</svg>"))
        self.assertIn("Perfectoid Spaces", svg)
        self.assertIn("Fargues-Fontaine", svg)
        self.assertIn("Harder-Narasimhan", svg)

        # Assert ZERO em dashes anywhere in generated SVG
        self.assertNotIn(chr(8212), svg)

        # Assert ZERO em dashes in JSON export
        json_data = self.loom.to_json()
        self.assertNotIn(chr(8212), json_data)

        # Verify source file has zero em dashes
        loom_path = os.path.join(os.path.dirname(__file__), "..", "scripts", "perfectoid_space_loom.py")
        with open(loom_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertNotIn(chr(8212), content)


if __name__ == "__main__":
    unittest.main()
