r"""
Unit tests for Paramodular Conjecture & Modularity of Abelian Surfaces Loom.
Verifies abelian surface data, paramodular form levels, degree 4 Spinor Euler factors,
non-lift filtration, and strict zero em dash compliance.
"""

import unittest
import math
import os
import sys

# Ensure scripts dir is accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))
from paramodular_conjecture_loom import (
    ParamodularConjectureLoom,
    ParamodularArchetype,
    AbelianSurfaceData,
    ParamodularFormDatum,
    SpinorEulerFactorData,
    ParamodularModularityEvaluation,
)


class TestParamodularConjectureLoom(unittest.TestCase):
    """Test suite for ParamodularConjectureLoom."""

    def setUp(self):
        self.loom = ParamodularConjectureLoom(
            conductor_input=277,
            spectral_precision=0.01,
            default_archetype=ParamodularArchetype.PARAMODULAR_N277_MINIMAL.value,
        )

    def test_abelian_surface_and_paramodular_form(self):
        """Verify abelian surface and paramodular cusp form data for N = 277."""
        ab = self.loom.abelian_surface
        self.assertIsNotNone(ab)
        self.assertEqual(ab.conductor_n, 277)
        self.assertEqual(ab.dimension_g, 2)
        self.assertEqual(ab.polarization_degree, 1)
        self.assertIn("End_Q(A) = Z", ab.endomorphism_ring)

        pf = self.loom.paramodular_form
        self.assertIsNotNone(pf)
        self.assertEqual(pf.paramodular_level_k_n, 277)
        self.assertEqual(pf.weight_k, 2)
        self.assertFalse(pf.is_gritsenko_lift)
        self.assertFalse(pf.is_saito_kurokawa)

    def test_spinor_euler_factors(self):
        """Verify degree 4 Spinor Euler factor matching at p = 2, 3, 5."""
        factors = self.loom.euler_factors
        self.assertGreaterEqual(len(factors), 3)

        for ef in factors:
            self.assertIn(ef.prime_p, [2, 3, 5])
            self.assertTrue(ef.is_euler_factor_matched)
            self.assertGreaterEqual(ef.sato_tate_angle_theta1, 0.0)
            self.assertGreaterEqual(ef.sato_tate_angle_theta2, 0.0)

    def test_modularity_evaluation_and_conjecture_verification(self):
        """Verify Paramodular Conjecture evaluation for genuine non-lift."""
        eval_res = self.loom.evaluate_paramodular_conjecture()
        self.assertTrue(eval_res.conductor_matched)
        self.assertEqual(eval_res.spinor_l_degree, 4)
        self.assertTrue(eval_res.is_genuine_non_lift)
        self.assertTrue(eval_res.modularity_conjecture_verified)
        self.assertEqual(eval_res.eigenvalue_congruence_residual, 0.0)
        self.assertGreater(eval_res.cognitive_resonance_score, 0.9)
        self.assertEqual(eval_res.spatial_stability_index, 0.96)

    def test_gritsenko_lift_boundary(self):
        """Verify filtration of Saito-Kurokawa and Gritsenko lifts."""
        lift_loom = ParamodularConjectureLoom(
            default_archetype=ParamodularArchetype.GRITSENKO_LIFT_BOUNDARY.value,
        )
        self.assertTrue(lift_loom.paramodular_form.is_gritsenko_lift)
        self.assertTrue(lift_loom.paramodular_form.is_saito_kurokawa)

        eval_res = lift_loom.evaluate_paramodular_conjecture()
        self.assertFalse(eval_res.is_genuine_non_lift)
        self.assertFalse(eval_res.modularity_conjecture_verified)

    def test_svg_generation_and_zero_em_dashes(self):
        """Verify dark titanium SVG generation and strict zero em dash compliance."""
        svg = self.loom.generate_svg()
        self.assertIn("<svg", svg)
        self.assertIn("Paramodular Conjecture", svg)
        self.assertIn("Abelian Surface A/Q", svg)
        self.assertIn("Paramodular Cusp Form", svg)
        self.assertIn("Spinor Euler Factors", svg)

        # Verify zero em dashes across both test and engine scripts
        cur_file = __file__
        loom_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts", "paramodular_conjecture_loom.py"))
        for fpath in [cur_file, loom_file]:
            if os.path.exists(fpath):
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()
                self.assertNotIn("\u2014", content, f"Em dash found in {fpath}")


if __name__ == "__main__":
    unittest.main()
