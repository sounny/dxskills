r"""
Unit tests for Gross-Stark Conjecture & p-Adic Stark Conjectures Loom.
Verifies totally real number fields, Gross-Stark S-units, p-adic L-function derivatives,
Shintani cone decompositions, Gross-Stark equality, and strict zero em dash compliance.
"""

import unittest
import math
import os
import sys

# Ensure scripts dir is accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))
from gross_stark_loom import (
    GrossStarkLoom,
    GrossStarkArchetype,
    TotallyRealFieldData,
    GrossStarkUnitData,
    PadicLDerivativeData,
    ShintaniConeData,
)


class TestGrossStarkLoom(unittest.TestCase):
    """Test suite for GrossStarkLoom."""

    def setUp(self):
        self.loom = GrossStarkLoom(
            degree_g=2,
            discriminant_d=5,
            prime_p=3,
            default_archetype=GrossStarkArchetype.REAL_QUADRATIC_Q_SQRT5.value,
        )

    def test_totally_real_field_initialization(self):
        """Verify totally real number field configuration."""
        field_data = self.loom.totally_real_field
        self.assertEqual(field_data.degree_g, 2)
        self.assertEqual(field_data.discriminant_df, 5)
        self.assertEqual(field_data.narrow_class_number, 1)
        self.assertEqual(field_data.splitting_prime_p, 3)
        self.assertEqual(field_data.ideal_norm_p, 3)

    def test_gross_stark_unit_and_regulator(self):
        """Verify Gross-Stark algebraic S-unit and canonical regulator."""
        unit = self.loom.stark_unit
        self.assertEqual(unit.algebraic_degree, 4)
        self.assertEqual(unit.p_adic_valuation, 1)
        self.assertGreater(unit.iwasawa_padic_log, 0.0)
        self.assertEqual(unit.canonical_regulator, unit.p_adic_valuation * unit.iwasawa_padic_log)
        self.assertIn("x^2", unit.minimal_polynomial)

    def test_padic_l_derivative_and_conjecture_equality(self):
        """Verify p-adic L-function leading derivative and Gross-Stark equality."""
        deriv = self.loom.padic_derivative
        self.assertEqual(deriv.order_of_vanishing, 1)
        self.assertEqual(deriv.conductor, 5)
        self.assertAlmostEqual(deriv.derivative_value, -deriv.padic_regulator, places=5)
        self.assertTrue(deriv.is_conjecture_verified)
        self.assertAlmostEqual(deriv.gross_stark_ratio, 1.0, places=4)

    def test_shintani_cone_decomposition(self):
        """Verify Shintani simplicial cone decomposition."""
        cones = self.loom.shintani_cones
        self.assertGreaterEqual(len(cones), 2)
        c1 = cones[0]
        self.assertEqual(c1.generator_count, 2)
        self.assertGreater(c1.volume_determinant, 0.0)
        self.assertGreater(c1.cocycle_contribution, 0.0)

    def test_svg_generation_and_zero_em_dashes(self):
        """Verify dark titanium SVG generation and strict zero em dash compliance."""
        svg = self.loom.generate_svg()
        self.assertIn("<svg", svg)
        self.assertIn("Gross-Stark Conjecture", svg)
        self.assertIn("L_p'", svg)
        self.assertIn("u_&#967;", svg)

        # Verify zero em dashes across both test and engine scripts
        cur_file = __file__
        loom_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts", "gross_stark_loom.py"))
        for fpath in [cur_file, loom_file]:
            if os.path.exists(fpath):
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()
                self.assertNotIn("\u2014", content, f"Em dash found in {fpath}")


if __name__ == "__main__":
    unittest.main()
