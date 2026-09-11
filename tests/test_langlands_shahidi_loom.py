r"""
Unit tests for Langlands-Shahidi Method & Automorphic L-Functions Loom.
Verifies quasi-split groups, Levi representations, Shahidi local gamma-factors,
global automorphic L-functions, unitary axis non-vanishing, and strict zero em dash compliance.
"""

import unittest
import math
import os
import sys

# Ensure scripts dir is accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))
from langlands_shahidi_loom import (
    LanglandsShahidiLoom,
    ShahidiArchetype,
    QuasiSplitGroupData,
    LeviRepresentationData,
    ShahidiLocalFactorData,
    GlobalAutomorphicLData,
)


class TestLanglandsShahidiLoom(unittest.TestCase):
    """Test suite for LanglandsShahidiLoom."""

    def setUp(self):
        self.loom = LanglandsShahidiLoom(
            spectral_s=1.0,
            prime_p=5,
            default_archetype=ShahidiArchetype.SO5_SPLIT_STANDARD.value,
        )

    def test_quasi_split_group_and_parabolic_initialization(self):
        """Verify quasi-split reductive group and parabolic datum."""
        grp = self.loom.group_data
        self.assertEqual(grp.group_label, "SO_5 (Split B_2)")
        self.assertEqual(grp.dimension_g, 10)
        self.assertIn("GL_2", grp.levi_m_label)
        self.assertEqual(grp.unipotent_n_dimension, 3)
        self.assertEqual(grp.adjoint_pieces_count, 2)
        self.assertIn("w_0", grp.weyl_element_w0)

    def test_levi_generic_representation(self):
        """Verify generic cuspidal representation on Levi factor."""
        rep = self.loom.levi_representation
        self.assertTrue(rep.is_globally_generic)
        self.assertIn("psi", rep.whittaker_model_character)
        self.assertAlmostEqual(rep.ramanujan_bound_parameter, 7.0 / 64.0, places=4)
        self.assertTrue(rep.central_character_trivial)

    def test_shahidi_local_factors_computation(self):
        """Verify Shahidi local factors gamma, L, and epsilon."""
        factors = self.loom.local_factors
        self.assertEqual(len(factors), 2)

        f1 = factors[0]
        self.assertEqual(f1.adjoint_piece_index, 1)
        self.assertEqual(f1.conductor, 1)
        self.assertGreater(f1.local_l_value, 0.0)
        self.assertEqual(f1.local_epsilon_value, 1.0)
        self.assertGreater(f1.local_gamma_value, 0.0)

    def test_unitary_axis_and_global_l_data(self):
        """Verify unitary axis Re(s) = 1 non-vanishing and global L-data."""
        eval_res = self.loom.evaluate_unitary_axis()
        self.assertTrue(eval_res["is_on_unitary_axis"])
        self.assertTrue(eval_res["non_vanishing_guaranteed"])
        self.assertTrue(eval_res["intertwining_operator_invertible"])

        gl = self.loom.global_l_data
        self.assertTrue(gl.has_meromorphic_continuation)
        self.assertTrue(gl.unitary_axis_non_vanishing)
        self.assertEqual(gl.functional_equation_root_number, 1.0)
        self.assertIn("Sym^3", gl.functorial_lift_type)

    def test_svg_generation_and_zero_em_dashes(self):
        """Verify dark titanium SVG generation and strict zero em dash compliance."""
        svg = self.loom.generate_svg()
        self.assertIn("<svg", svg)
        self.assertIn("Langlands-Shahidi Method", svg)
        self.assertIn("M(s, &#960;)", svg)
        self.assertIn("&#947;(s", svg)

        # Verify zero em dashes across both test and engine scripts
        cur_file = __file__
        loom_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts", "langlands_shahidi_loom.py"))
        for fpath in [cur_file, loom_file]:
            if os.path.exists(fpath):
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()
                self.assertNotIn("\u2014", content, f"Em dash found in {fpath}")


if __name__ == "__main__":
    unittest.main()
