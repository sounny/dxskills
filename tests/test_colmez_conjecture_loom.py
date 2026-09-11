r"""
Unit tests for Colmez Conjecture & Faltings Heights of CM Abelian Varieties Loom.
Verifies CM fields, CM types, Faltings arithmetic heights, Artin L-function derivatives,
Colmez conjecture equality, and strict zero em dash compliance.
"""

import unittest
import math
import os
import sys

# Ensure scripts dir is accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))
from colmez_conjecture_loom import (
    ColmezConjectureLoom,
    ColmezArchetype,
    CMFieldData,
    CMTypeData,
    FaltingsHeightData,
    ArtinLDerivativeData,
)


class TestColmezConjectureLoom(unittest.TestCase):
    """Test suite for ColmezConjectureLoom."""

    def setUp(self):
        self.loom = ColmezConjectureLoom(
            dimension_g=1,
            discriminant_d=7,
            default_archetype=ColmezArchetype.IMAGINARY_QUADRATIC_CHOWLA_SELBERG.value,
        )

    def test_cm_field_and_type_initialization(self):
        """Verify CM field and CM type configuration."""
        cf = self.loom.cm_field
        self.assertEqual(cf.dimension_g, 1)
        self.assertEqual(cf.degree_e, 2)
        self.assertEqual(cf.discriminant_e, -7)
        self.assertEqual(cf.discriminant_f, 1)
        self.assertEqual(cf.galois_group_label, "Z/2Z")

        ct = self.loom.cm_type
        self.assertEqual(ct.embeddings_count, 1)
        self.assertEqual(ct.reflex_field, "E")
        self.assertTrue(ct.is_primitive)

    def test_artin_l_derivatives_computation(self):
        """Verify Artin L-function values and logarithmic derivatives."""
        derivatives = self.loom.artin_derivatives
        self.assertEqual(len(derivatives), 2)

        # Trivial character
        triv = derivatives[0]
        self.assertEqual(triv.conductor, 1)
        self.assertEqual(triv.l_zero_value, -0.5)
        self.assertAlmostEqual(triv.logarithmic_derivative, math.log(2.0 * math.pi), places=4)

        # Quadratic character
        quad = derivatives[1]
        self.assertEqual(quad.conductor, 7)
        self.assertEqual(quad.l_zero_value, 1.0)
        self.assertNotEqual(quad.l_prime_zero_value, 0.0)

    def test_faltings_and_taguchi_smith_heights(self):
        """Verify stable Faltings height and Taguchi-Smith normalization."""
        fh = self.loom.faltings_height
        self.assertEqual(fh.dimension_g, 1)
        self.assertIsInstance(fh.stable_faltings_height, float)
        self.assertIsInstance(fh.taguchi_smith_height, float)
        # Difference between Taguchi-Smith and Faltings height is 0.5 * log(pi)
        expected_diff = 0.5 * math.log(math.pi)
        self.assertAlmostEqual(fh.taguchi_smith_height - fh.stable_faltings_height, expected_diff, places=4)
        self.assertGreater(fh.archimedean_period_integral, 0.0)

    def test_colmez_conjecture_equality_and_evaluation(self):
        """Verify Colmez conjecture arithmetic vs analytic equality."""
        eval_res = self.loom.evaluate_colmez_conjecture()
        self.assertTrue(eval_res["is_colmez_equality_satisfied"])
        self.assertLess(eval_res["absolute_discrepancy"], 1e-4)
        self.assertIn("Chowla-Selberg", eval_res["proof_status"])
        self.assertIn("Andre-Oort", eval_res["andre_oort_consequence"])

    def test_svg_generation_and_zero_em_dashes(self):
        """Verify dark titanium SVG generation and strict zero em dash compliance."""
        svg = self.loom.generate_svg()
        self.assertIn("<svg", svg)
        self.assertIn("Colmez Conjecture", svg)
        self.assertIn("h_Fal(A)", svg)
        self.assertIn("L'(0", svg)

        # Verify zero em dashes across both test and engine scripts
        cur_file = __file__
        loom_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts", "colmez_conjecture_loom.py"))
        for fpath in [cur_file, loom_file]:
            if os.path.exists(fpath):
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()
                self.assertNotIn("\u2014", content, f"Em dash found in {fpath}")


if __name__ == "__main__":
    unittest.main()
