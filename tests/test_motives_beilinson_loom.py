"""
Tests for Motives & Beilinson Conjectures on Special Values Loom.
Verifies Chow motives, motivic cohomology, Beilinson regulators into Deligne cohomology,
L-function leading coefficients, and strict zero em dash compliance.
"""

import unittest
from scripts.motives_beilinson_loom import (
    MotivesBeilinsonLoom,
    MotivicWeightArchetype,
    ChowMotiveData,
    BeilinsonRegulatorData,
    MotivicLFunctionSpecialValueData,
)


class TestMotivesBeilinsonLoom(unittest.TestCase):
    """Test suite for MotivesBeilinsonLoom algorithms and visualizers."""

    def setUp(self):
        self.loom = MotivesBeilinsonLoom(
            motive_weight=1,
            tate_twist=1,
            default_archetype=MotivicWeightArchetype.ELLIPTIC_CURVE_H1.value,
        )

    def test_chow_motive_and_realizations(self):
        """Verify Chow motive structure, Betti, and de Rham realizations."""
        self.assertGreaterEqual(len(self.loom.motives), 1)
        mot = self.loom.motives[0]
        self.assertIsInstance(mot, ChowMotiveData)
        self.assertEqual(mot.betti_dimension, 2)
        self.assertEqual(mot.de_rham_dimension, 2)
        self.assertEqual(mot.tate_twist_n, 1)
        self.assertEqual(mot.hodge_diamond_row, [1, 1])
        self.assertIn("Elliptic Curve", mot.underlying_variety)

    def test_beilinson_regulator_mapping(self):
        """Verify Beilinson regulator volume determinant in Deligne cohomology."""
        self.assertGreaterEqual(len(self.loom.regulators), 1)
        reg = self.loom.regulators[0]
        self.assertIsInstance(reg, BeilinsonRegulatorData)
        self.assertEqual(reg.deligne_dimension, 1)
        self.assertEqual(reg.motivic_cohomology_rank, 1)
        self.assertTrue(reg.is_lattice_volume_non_zero)
        self.assertAlmostEqual(reg.regulator_determinant, 0.5218, places=4)

        # Dynamic evaluation with rank 2
        eval_reg = self.loom.evaluate_motivic_cohomology(weight_i=2, twist_n=1, test_rank=2)
        self.assertEqual(eval_reg.motivic_cohomology_rank, 2)
        self.assertEqual(eval_reg.deligne_dimension, 2)
        self.assertTrue(eval_reg.is_lattice_volume_non_zero)

    def test_special_value_conjecture_ratio(self):
        """Verify leading coefficient L^*(M, s) and rational Beilinson ratio."""
        self.assertGreaterEqual(len(self.loom.special_values), 1)
        sp = self.loom.special_values[0]
        self.assertIsInstance(sp, MotivicLFunctionSpecialValueData)
        self.assertEqual(sp.order_of_vanishing_r, 1)
        self.assertTrue(sp.conjecture_verified)
        self.assertAlmostEqual(sp.beilinson_conjecture_ratio, 1.5, places=3)

        eval_sp = self.loom.compute_special_value_conjecture(eval_s=1)
        self.assertIsInstance(eval_sp, MotivicLFunctionSpecialValueData)
        self.assertTrue(eval_sp.conjecture_verified)
        self.assertGreater(eval_sp.beilinson_conjecture_ratio, 0.0)

    def test_k3_surface_motive(self):
        """Verify weight 2 K3 surface Chow motive and Betti dimension."""
        k3_loom = MotivesBeilinsonLoom(
            motive_weight=2,
            tate_twist=1,
            default_archetype=MotivicWeightArchetype.K3_SURFACE_CHOW.value,
        )
        mot = k3_loom.motives[0]
        self.assertEqual(mot.betti_dimension, 22)
        self.assertEqual(mot.de_rham_dimension, 22)
        self.assertEqual(mot.hodge_diamond_row, [1, 20, 1])
        self.assertIn("K3 Surface", mot.underlying_variety)

    def test_svg_and_zero_em_dash_compliance(self):
        """Verify dark titanium SVG rendering, JSON telemetry, and zero em dashes."""
        self.loom.compute_special_value_conjecture()

        svg = self.loom.generate_beilinson_svg()
        self.assertIsInstance(svg, str)
        self.assertTrue(svg.startswith("<svg"))
        self.assertTrue(svg.endswith("</svg>"))
        self.assertIn("Motives &amp; Beilinson Conjectures on Special Values Loom", svg)
        self.assertIn("Chow Motive &amp; Realizations", svg)
        self.assertIn("Beilinson Regulator in H_D", svg)
        self.assertIn("L-Function Special Values", svg)

        # Strict zero em dash verification
        self.assertNotIn("\u2014", svg)
        self.assertNotIn(chr(8212), svg)

        json_str = self.loom.to_json()
        self.assertNotIn("\u2014", json_str)
        self.assertNotIn(chr(8212), json_str)

        with open("scripts/motives_beilinson_loom.py", encoding="utf-8") as f:
            src = f.read()
        self.assertNotIn("\u2014", src)
        self.assertNotIn(chr(8212), src)


if __name__ == "__main__":
    unittest.main()
