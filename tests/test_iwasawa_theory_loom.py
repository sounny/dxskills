r"""
Unit tests for Iwasawa Main Conjecture & p-Adic L-Functions Loom.
Verifies Lambda-module invariants, class number asymptotics, p-adic L-functions,
and strictly zero em dashes (chr(8212)).
"""

import unittest
import os
import sys

# Add scripts directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))

from iwasawa_theory_loom import (
    IwasawaTheoryLoom,
    IwasawaArchetype,
)


class TestIwasawaTheoryLoom(unittest.TestCase):
    """Test suite for Iwasawa Theory Loom."""

    def setUp(self):
        self.loom = IwasawaTheoryLoom(
            base_prime=5,
            lambda_inv=1,
            default_archetype=IwasawaArchetype.CYCLOTOMIC_Z_P.value,
        )

    def test_iwasawa_module_structure(self):
        """Test Lambda-module decomposition and mu = 0 invariant."""
        self.assertEqual(len(self.loom.modules), 1)
        m = self.loom.modules[0]
        self.assertEqual(m.prime_p, 5)
        self.assertEqual(m.mu_invariant, 0)
        self.assertEqual(m.lambda_invariant, 1)
        self.assertTrue(m.is_ferrero_washington_mu_zero)

    def test_class_number_growth_asymptotics(self):
        """Test Iwasawa class number asymptotic formula e_n = mu*p^n + lambda*n + nu."""
        growth = self.loom.evaluate_class_number_growth(layer_n=3)
        self.assertEqual(growth["layer_n"], 3)
        self.assertEqual(growth["exponent_e_n"], 3)  # 0*125 + 1*3 + 0
        self.assertEqual(growth["order_approx"], 125)

    def test_main_conjecture_verification(self):
        """Test Mazur-Wiles Main Conjecture identification."""
        self.assertTrue(self.loom.verify_main_conjecture())
        self.assertEqual(len(self.loom.comparisons), 1)
        comp = self.loom.comparisons[0]
        self.assertTrue(comp.ideals_coincide)

    def test_ordinary_and_totally_real_archetypes(self):
        """Test ordinary elliptic curve and totally real field towers."""
        ord_loom = IwasawaTheoryLoom(
            base_prime=7,
            lambda_inv=2,
            default_archetype=IwasawaArchetype.ELLIPTIC_CURVE_ORDINARY.value,
        )
        self.assertEqual(ord_loom.modules[0].prime_p, 7)
        self.assertEqual(ord_loom.modules[0].nu_invariant, 1)

        real_loom = IwasawaTheoryLoom(
            base_prime=3,
            lambda_inv=2,
            default_archetype=IwasawaArchetype.TOTALLY_REAL_FIELD.value,
        )
        self.assertTrue(real_loom.verify_main_conjecture())

    def test_svg_generation_and_zero_em_dashes(self):
        """Verify dark titanium SVG generation and zero em dashes across script and tests."""
        svg = self.loom.generate_iwasawa_svg()
        self.assertIn("<svg", svg)
        self.assertIn("Iwasawa Main Conjecture &amp; p-Adic L-Functions Loom", svg)
        self.assertIn("Z_p", svg)
        self.assertIn("L_p", svg)

        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts", "iwasawa_theory_loom.py"))
        if os.path.exists(script_path):
            with open(script_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertNotIn("\u2014", content, "Found em dash in iwasawa_theory_loom.py")

        with open(__file__, "r", encoding="utf-8") as f:
            test_content = f.read()
        self.assertNotIn("\u2014", test_content, "Found em dash in test_iwasawa_theory_loom.py")


if __name__ == "__main__":
    unittest.main()
