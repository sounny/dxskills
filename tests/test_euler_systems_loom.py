r"""
Unit tests for Euler Systems & Kolyvagin Derivatives Loom.
Verifies norm relations, Kolyvagin derivatives D_ell, Shafarevich-Tate bounds,
and strictly zero em dashes (chr(8212)).
"""

import unittest
import os
import sys

# Add scripts directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))

from euler_systems_loom import (
    EulerSystemsKolyvaginLoom,
    EulerSystemArchetype,
)


class TestEulerSystemsKolyvaginLoom(unittest.TestCase):
    """Test suite for Euler Systems & Kolyvagin Derivatives Loom."""

    def setUp(self):
        self.loom = EulerSystemsKolyvaginLoom(
            conductor=7,
            prime_p=3,
            default_archetype=EulerSystemArchetype.HEEGNER_POINTS_ELLIPTIC.value,
        )

    def test_euler_system_class_norm_relations(self):
        """Test base Euler class generation and norm compatibility."""
        self.assertEqual(len(self.loom.euler_classes), 1)
        c = self.loom.euler_classes[0]
        self.assertEqual(c.conductor_m, 7)
        self.assertTrue(c.norm_compatibility_verified)
        self.assertEqual(c.galois_group_order, 6)

    def test_kolyvagin_derivative_evaluation(self):
        """Test application of Kolyvagin derivative operator and Chebotarev reciprocity."""
        self.assertEqual(len(self.loom.derivatives), 1)
        d = self.loom.derivatives[0]
        self.assertTrue(d.finite_singular_residue_match)

        eval_res = self.loom.evaluate_kolyvagin_derivative(test_prime_ell=13, mod_power_m=2)
        self.assertEqual(eval_res.prime_ell, 13)
        self.assertEqual(eval_res.annihilator_exponent, 2)
        self.assertTrue(eval_res.finite_singular_residue_match)

    def test_sha_bound_computation(self):
        """Test Shafarevich-Tate order bound calculation."""
        self.assertEqual(len(self.loom.selmer_bounds), 1)
        b = self.loom.selmer_bounds[0]
        self.assertTrue(b.is_sha_finite)
        self.assertEqual(b.mordell_weil_rank, 1)

        new_b = self.loom.compute_sha_bound(order_bound_k=3)
        self.assertEqual(new_b.sha_order_bound, 3)
        self.assertTrue(new_b.is_sha_finite)

    def test_cyclotomic_and_kato_archetypes(self):
        """Test Cyclotomic units and Kato modular Euler system models."""
        cy_loom = EulerSystemsKolyvaginLoom(
            conductor=5,
            prime_p=5,
            default_archetype=EulerSystemArchetype.CYCLOTOMIC_UNITS.value,
        )
        self.assertEqual(cy_loom.selmer_bounds[0].analytic_rank, 0)

        kato_loom = EulerSystemsKolyvaginLoom(
            conductor=11,
            prime_p=2,
            default_archetype=EulerSystemArchetype.KATO_EULER_SYSTEM.value,
        )
        self.assertTrue(kato_loom.euler_classes[0].norm_compatibility_verified)

    def test_svg_generation_and_zero_em_dashes(self):
        """Verify dark titanium SVG generation and zero em dashes across script and tests."""
        svg = self.loom.generate_euler_system_svg()
        self.assertIn("<svg", svg)
        self.assertIn("Euler Systems &amp; Kolyvagin Derivatives Loom", svg)
        self.assertIn("D_&#8467;", svg)
        self.assertIn("Sha", svg)

        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts", "euler_systems_loom.py"))
        if os.path.exists(script_path):
            with open(script_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertNotIn("\u2014", content, "Found em dash in euler_systems_loom.py")

        with open(__file__, "r", encoding="utf-8") as f:
            test_content = f.read()
        self.assertNotIn("\u2014", test_content, "Found em dash in test_euler_systems_loom.py")


if __name__ == "__main__":
    unittest.main()
