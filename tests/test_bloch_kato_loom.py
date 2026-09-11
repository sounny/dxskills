r"""
Unit tests for Tamagawa Numbers & Bloch-Kato Exponential Map Loom.
Verifies local Selmer conditions, exponential map exp_BK, global Tamagawa numbers,
and strictly zero em dashes (chr(8212)).
"""

import unittest
import os
import sys

# Add scripts directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))

from bloch_kato_loom import (
    BlochKatoExponentialLoom,
    BlochKatoSubspaceKind,
    MotivicGaloisArchetype,
)


class TestBlochKatoExponentialLoom(unittest.TestCase):
    """Test suite for Bloch-Kato Exponential Loom."""

    def setUp(self):
        self.loom = BlochKatoExponentialLoom(
            base_prime=5,
            dimension_v=2,
            default_archetype=MotivicGaloisArchetype.ELLIPTIC_CURVE_P_ADIC.value,
        )

    def test_local_selmer_subspaces(self):
        """Test local Galois cohomology subspace inclusions H_e^1 subset H_f^1 subset H_g^1 subset H^1."""
        self.assertEqual(len(self.loom.local_conditions), 1)
        cond = self.loom.local_conditions[0]
        self.assertEqual(cond.prime_v, 5)
        self.assertLessEqual(cond.dim_h_exponential, cond.dim_h_finite)
        self.assertLessEqual(cond.dim_h_finite, cond.dim_h_geometric)
        self.assertLessEqual(cond.dim_h_geometric, cond.dim_h_total)
        self.assertGreaterEqual(cond.local_tamagawa_factor_c_v, 1)

    def test_bloch_kato_exponential_evaluation(self):
        """Test evaluation of the p-adic exponential map on tangent space."""
        self.assertEqual(len(self.loom.exponential_maps), 1)
        exp_m = self.loom.exponential_maps[0]
        self.assertTrue(exp_m.is_isomorphism)
        self.assertEqual(exp_m.exponential_kernel_dim, 0)

        eval_res = self.loom.evaluate_bloch_kato_exponential(tangent_vector_norm=2.0)
        self.assertEqual(eval_res["map_id"], exp_m.map_id)
        self.assertGreater(eval_res["cohomology_image_norm"], 0.0)
        self.assertTrue(eval_res["is_injective"])

    def test_global_tamagawa_number_computation(self):
        """Test global Tamagawa number conjecture calculation."""
        self.assertEqual(len(self.loom.tamagawa_data), 1)
        tam = self.loom.tamagawa_data[0]
        self.assertTrue(tam.conjecture_satisfied)
        self.assertEqual(tam.tamagawa_number_tam_m, 1.0)

        new_tam = self.loom.compute_tamagawa_number(test_sha=4, test_c_v=2)
        self.assertGreater(new_tam.tamagawa_number_tam_m, 0.0)
        self.assertEqual(new_tam.sha_order, 4)

    def test_modular_and_calabi_yau_archetypes(self):
        """Test Modular form and Calabi-Yau Galois representation models."""
        mod_loom = BlochKatoExponentialLoom(
            base_prime=7,
            dimension_v=2,
            default_archetype=MotivicGaloisArchetype.MODULAR_FORM_DELIGNE.value,
        )
        cond = mod_loom.local_conditions[0]
        self.assertEqual(cond.prime_v, 7)
        self.assertEqual(cond.dim_h_total, 4)
        self.assertEqual(cond.dim_h_geometric, 2)

        cy_loom = BlochKatoExponentialLoom(
            base_prime=3,
            dimension_v=4,
            default_archetype=MotivicGaloisArchetype.CALABI_YAU_P_ADIC.value,
        )
        self.assertEqual(cy_loom.local_conditions[0].dim_h_total, 4)

    def test_svg_generation_and_zero_em_dashes(self):
        """Verify dark titanium SVG generation and zero em dashes across script and tests."""
        svg = self.loom.generate_bloch_kato_svg()
        self.assertIn("<svg", svg)
        self.assertIn("Tamagawa Numbers &amp; Bloch-Kato Exponential Map Loom", svg)
        self.assertIn("H_f^1", svg)
        self.assertIn("exp_BK", svg)

        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts", "bloch_kato_loom.py"))
        if os.path.exists(script_path):
            with open(script_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertNotIn("\u2014", content, "Found em dash in bloch_kato_loom.py")

        with open(__file__, "r", encoding="utf-8") as f:
            test_content = f.read()
        self.assertNotIn("\u2014", test_content, "Found em dash in test_bloch_kato_loom.py")


if __name__ == "__main__":
    unittest.main()
