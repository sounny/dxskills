"""
Tests for Geometric Class Field Theory and Langlands Duality for Function Fields Loom.
Verifies Rosenlicht-Serre generalized Jacobians, Deligne Hecke eigensheaves on Pic_X,
Abel-Jacobi descent from Sym^d(X), Weil Riemann hypothesis L-functions, and strict zero em dash compliance.
"""

import math
import unittest
from scripts.geometric_cft_loom import (
    GeometricClassFieldTheoryLoom,
    CurveModulusArchetype,
    GeometricReciprocityData,
    DeligneHeckeSheafData,
    FunctionFieldLFunctionData,
)


class TestGeometricClassFieldTheoryLoom(unittest.TestCase):
    """Test suite for GeometricClassFieldTheoryLoom algorithms and visualizers."""

    def setUp(self):
        self.loom = GeometricClassFieldTheoryLoom(
            curve_genus=2,
            field_q=5,
            modulus_points=2,
            modulus_archetype=CurveModulusArchetype.TAME_MODULUS.value,
        )

    def test_reciprocity_and_generalized_jacobian(self):
        """Verify Rosenlicht-Serre generalized Jacobian and Picard order."""
        self.assertGreaterEqual(len(self.loom.reciprocity_records), 1)
        rec = self.loom.reciprocity_records[0]
        self.assertIsInstance(rec, GeometricReciprocityData)
        self.assertEqual(rec.curve_genus, 2)
        self.assertEqual(rec.field_cardinality_q, 5)
        self.assertEqual(rec.modulus_degree, 2)
        # For tame modulus: dim(J_m) = g + (m - 1) = 2 + 1 = 3
        self.assertEqual(rec.generalized_jacobian_dim, 3)
        self.assertTrue(rec.reciprocity_verified)
        self.assertIn("G_m", rec.affine_group_type)

        # Test wild modulus extension
        wild_loom = GeometricClassFieldTheoryLoom(
            curve_genus=2,
            field_q=5,
            modulus_points=2,
            modulus_archetype=CurveModulusArchetype.WILD_MODULUS.value,
        )
        wild_rec = wild_loom.reciprocity_records[0]
        # Wild: dim = g + (m-1) + m = 2 + 1 + 2 = 5
        self.assertEqual(wild_rec.generalized_jacobian_dim, 5)
        self.assertIn("G_a", wild_rec.affine_group_type)

    def test_deligne_hecke_sheaf(self):
        """Verify Deligne Abel-Jacobi descent and Hecke eigensheaf on Pic_X."""
        self.assertGreaterEqual(len(self.loom.hecke_sheaves), 1)
        shf = self.loom.hecke_sheaves[0]
        self.assertIsInstance(shf, DeligneHeckeSheafData)
        self.assertEqual(shf.rank, 1)
        # Degree d >= 2g - 1: d = 2*2 - 1 = 3
        self.assertEqual(shf.symmetric_power_degree, 3)
        self.assertEqual(shf.abel_jacobi_fiber_dim, 1)  # 3 - 2 = 1 (P^1 fiber)
        self.assertTrue(shf.hecke_eigenvalue_verified)

    def test_hecke_eigenvalue_action(self):
        """Verify Hecke eigenvalue action and Frobenius trace."""
        hecke_eval = self.loom.evaluate_hecke_eigenvalue(point_deg=1, test_phase_rad=0.5)
        self.assertIsInstance(hecke_eval, dict)
        self.assertTrue(hecke_eval["hecke_eigenvalue_verified"])
        self.assertAlmostEqual(hecke_eval["eigenvalue_modulus"], 1.0, places=4)
        self.assertAlmostEqual(hecke_eval["trace_frobenius"], 2.0 * math.cos(0.5), places=3)

    def test_function_field_l_function(self):
        """Verify Grothendieck-Deligne L-function and Weil Riemann hypothesis."""
        lfn = self.loom.compute_function_field_l_function("L-TEST-01")
        self.assertIsInstance(lfn, FunctionFieldLFunctionData)
        self.assertEqual(lfn.l_function_id, "L-TEST-01")
        # Degree = 2g - 2 + m = 2*2 - 2 + 2 = 4
        self.assertEqual(lfn.degree_of_l_polynomial, 4)
        self.assertEqual(len(lfn.frobenius_eigenvalues), 4)
        self.assertTrue(lfn.riemann_hypothesis_satisfied)
        self.assertGreater(lfn.special_value_at_1, 0.0)

    def test_svg_and_zero_em_dash_compliance(self):
        """Verify dark titanium SVG rendering, JSON telemetry, and zero em dashes."""
        self.loom.compute_function_field_l_function()

        svg = self.loom.generate_geometric_cft_svg()
        self.assertIsInstance(svg, str)
        self.assertTrue(svg.startswith("<svg"))
        self.assertTrue(svg.endswith("</svg>"))
        self.assertIn("Geometric Class Field Theory", svg)
        self.assertIn("Rosenlicht-Serre Generalized Jacobian", svg)
        self.assertIn("Deligne Abel-Jacobi Descent", svg)
        self.assertIn("Weil Riemann Hypothesis", svg)

        # Strict zero em dash verification
        self.assertNotIn("\u2014", svg)
        self.assertNotIn(chr(8212), svg)

        json_str = self.loom.to_json()
        self.assertNotIn("\u2014", json_str)
        self.assertNotIn(chr(8212), json_str)

        with open("scripts/geometric_cft_loom.py", encoding="utf-8") as f:
            src = f.read()
        self.assertNotIn("\u2014", src)
        self.assertNotIn(chr(8212), src)


if __name__ == "__main__":
    unittest.main()
