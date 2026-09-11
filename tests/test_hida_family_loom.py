r"""
Unit tests for Hida Families & Ordinary Modular Deformations Loom.
Verifies ordinary Hecke algebra, weight specializations, big Galois representations,
and strictly zero em dashes (chr(8212)).
"""

import unittest
import os
import sys

# Add scripts directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))

from hida_family_loom import (
    HidaFamilyLoom,
    HidaFamilyArchetype,
)


class TestHidaFamilyLoom(unittest.TestCase):
    """Test suite for Hida Families & Ordinary Modular Deformations Loom."""

    def setUp(self):
        self.loom = HidaFamilyLoom(
            level_n=11,
            prime_p=5,
            default_archetype=HidaFamilyArchetype.WEIGHT_TWO_ELLIPTIC.value,
        )

    def test_hida_family_data_structure(self):
        """Test ordinary Hecke algebra rank and p-ordinary coefficients."""
        self.assertEqual(len(self.loom.families), 1)
        fam = self.loom.families[0]
        self.assertEqual(fam.level_n, 11)
        self.assertEqual(fam.prime_p, 5)
        self.assertTrue(fam.is_ordinary_at_p)
        self.assertEqual(fam.hecke_algebra_rank, 1)

    def test_weight_specialization(self):
        """Test specialization of Lambda-adic form to classical weights k >= 2."""
        self.assertEqual(len(self.loom.specializations), 1)
        init_spec = self.loom.specializations[0]
        self.assertEqual(init_spec.weight_k, 2)
        self.assertTrue(init_spec.is_classical_cusp_form)

        spec4 = self.loom.specialize_to_weight(target_weight=4)
        self.assertEqual(spec4.weight_k, 4)
        self.assertTrue(spec4.is_classical_cusp_form)
        self.assertGreater(spec4.hecke_eigenvalue_a_p, 1.0)

    def test_ordinary_galois_representation(self):
        """Test big Galois representation local shape and congruence ideal."""
        self.assertEqual(len(self.loom.representations), 1)
        rep = self.loom.representations[0]
        self.assertTrue(rep.is_unramified_outside_np)
        self.assertIn("Upper Triangular", rep.local_p_shape)

        new_rep = self.loom.evaluate_congruence_ideal(test_order=3)
        self.assertEqual(new_rep.congruence_order, 3)

    def test_ramanujan_delta_and_cm_archetypes(self):
        """Test Ramanujan Delta and CM family models."""
        delta_loom = HidaFamilyLoom(
            default_archetype=HidaFamilyArchetype.RAMANUJAN_DELTA_FAMILY.value,
        )
        self.assertEqual(delta_loom.specializations[0].weight_k, 12)
        self.assertIn("Delta_12", delta_loom.specializations[0].classical_form_label)

        cm_loom = HidaFamilyLoom(
            level_n=7,
            prime_p=7,
            default_archetype=HidaFamilyArchetype.CM_FAMILY.value,
        )
        self.assertEqual(cm_loom.families[0].hecke_algebra_rank, 2)

    def test_svg_generation_and_zero_em_dashes(self):
        """Verify dark titanium SVG generation and zero em dashes across script and tests."""
        svg = self.loom.generate_hida_svg()
        self.assertIn("<svg", svg)
        self.assertIn("Hida Families &amp; Ordinary Modular Deformations Loom", svg)
        self.assertIn("h^ord", svg)
        self.assertIn("P_k", svg)

        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts", "hida_family_loom.py"))
        if os.path.exists(script_path):
            with open(script_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertNotIn("\u2014", content, "Found em dash in hida_family_loom.py")

        with open(__file__, "r", encoding="utf-8") as f:
            test_content = f.read()
        self.assertNotIn("\u2014", test_content, "Found em dash in test_hida_family_loom.py")


if __name__ == "__main__":
    unittest.main()
