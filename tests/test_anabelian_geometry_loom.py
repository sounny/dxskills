"""
Unit tests for Anabelian Geometry & Grothendieck Section Conjecture Loom.
Strictly verifies zero em dashes (chr(8212)), hyperbolic curve topologies,
Galois section splittings, outer Galois representations, and Neukirch-Uchida field reconstructions.
"""

import unittest
import os
import json
from scripts.anabelian_geometry_loom import (
    AnabelianGeometryLoom,
    HyperbolicCurveArchetype,
    BaseFieldType,
)


class TestAnabelianGeometryLoom(unittest.TestCase):
    """Test suite for AnabelianGeometryLoom engine and spatial cognitive mappings."""

    def setUp(self):
        self.loom = AnabelianGeometryLoom(
            base_field=BaseFieldType.RATIONAL_Q.value,
            default_archetype=HyperbolicCurveArchetype.PROJECTIVE_LINE_THREE_PUNCTURES.value,
        )

    def test_hyperbolic_curve_initialization(self):
        """Verify default hyperbolic curve P^1 - {0, 1, oo} and Euler characteristic."""
        self.assertEqual(len(self.loom.curves), 1)
        c = self.loom.curves[0]
        self.assertEqual(c.genus, 0)
        self.assertEqual(c.punctures, 3)
        self.assertEqual(c.euler_characteristic, -1)
        self.assertTrue(c.is_hyperbolic)
        self.assertEqual(c.topological_generators_count, 2)  # Free group of rank 2

        # Punctured elliptic curve (g=1, r=1)
        c_ell = self.loom.construct_hyperbolic_curve(
            curve_id="CURVE-ELL",
            archetype=HyperbolicCurveArchetype.PUNCTURED_ELLIPTIC_CURVE.value,
            genus=1,
            punctures=1,
            curve_equation="y^2 = x^3 - x - {O}",
        )
        self.assertEqual(c_ell.euler_characteristic, -1)
        self.assertTrue(c_ell.is_hyperbolic)
        self.assertEqual(c_ell.topological_generators_count, 2)

        # Compact genus 2 curve (g=2, r=0)
        c_g2 = self.loom.construct_hyperbolic_curve(
            curve_id="CURVE-G2",
            archetype=HyperbolicCurveArchetype.GENUS_TWO_CURVE.value,
            genus=2,
            punctures=0,
            curve_equation="y^2 = x^5 - x + 1",
        )
        self.assertEqual(c_g2.euler_characteristic, -2)
        self.assertTrue(c_g2.is_hyperbolic)
        self.assertEqual(c_g2.topological_generators_count, 4)

    def test_galois_section_evaluation(self):
        """Verify Galois section lifts and Brauer-Manin obstruction status."""
        sec_rat = self.loom.evaluate_galois_section(
            section_id="SEC-01",
            point_label="x_1/2",
            coordinates=(0.5, 0.0),
            is_rational=True,
            is_cuspidal=False,
        )
        self.assertTrue(sec_rat.is_rational)
        self.assertTrue(sec_rat.obstruction_class_vanishes)
        self.assertIn("Conjugacy Class", sec_rat.splitting_conjugacy_class)

        sec_cusp = self.loom.evaluate_galois_section(
            section_id="SEC-02",
            point_label="cusp_0",
            coordinates=(0.0, 0.0),
            is_rational=True,
            is_cuspidal=True,
        )
        self.assertTrue(sec_cusp.is_cuspidal_section)
        self.assertIn("Cuspidal", sec_cusp.splitting_conjugacy_class)

    def test_outer_galois_representation(self):
        """Verify nilpotent depth, Deligne-Ihara Lie dimension, and faithfulness."""
        rep = self.loom.evaluate_outer_galois_representation(
            rep_id="REP-01",
            pro_p_prime=2,
            nilpotent_depth=3,
        )
        self.assertEqual(rep.pro_p_prime, 2)
        self.assertEqual(rep.nilpotent_depth, 3)
        self.assertTrue(rep.is_faithful)
        self.assertTrue(rep.tamagawa_anabelian_certified)
        self.assertGreater(rep.graded_lie_dimension, 0)
        self.assertGreater(rep.galois_conductor, 0)

    def test_anabelian_reconstruction(self):
        """Verify Neukirch-Uchida theorem and Section conjecture evaluation."""
        rec = self.loom.evaluate_anabelian_reconstruction("REC-01")
        self.assertTrue(rec.neukirch_uchida_reconstructed)
        self.assertTrue(rec.isomorphism_determined_by_pi1)
        self.assertIn("Bijective", rec.section_conjecture_status)

    def test_svg_json_and_zero_em_dashes(self):
        """Verify SVG generation, JSON export, and strict zero em dash compliance."""
        self.loom.evaluate_galois_section("SEC-TEST", "x_test", (0.5, 0.0))
        self.loom.evaluate_outer_galois_representation("REP-TEST", pro_p_prime=3, nilpotent_depth=2)
        self.loom.evaluate_anabelian_reconstruction("REC-TEST")

        svg = self.loom.generate_anabelian_svg()
        self.assertTrue(svg.startswith("<svg"))
        self.assertTrue(svg.endswith("</svg>"))
        self.assertIn("Anabelian Geometry", svg)
        self.assertIn("Section Conjecture", svg)
        self.assertIn("Hyperbolic Curve", svg)

        # Assert ZERO em dashes anywhere in generated SVG
        self.assertNotIn(chr(8212), svg)

        # Assert ZERO em dashes in JSON export
        json_data = self.loom.to_json()
        self.assertNotIn(chr(8212), json_data)

        # Verify source file has zero em dashes
        loom_path = os.path.join(os.path.dirname(__file__), "..", "scripts", "anabelian_geometry_loom.py")
        if os.path.exists(loom_path):
            with open(loom_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertNotIn(chr(8212), content)


if __name__ == "__main__":
    unittest.main()
