"""
Tests for Categorical Langlands and Ind-Coherent Sheaves on Bun_G Loom.
Verifies D-modules on Bun_G, IndCoh_Nilp(LocSys_{G^vee}), Hecke eigensheaves,
Whittaker normalization, and strict zero em dash compliance.
"""

import unittest
from scripts.categorical_langlands_loom import (
    CategoricalLanglandsLoom,
    AutomorphicStackArchetype,
    SpectralLocSysArchetype,
    AlgebraicCurveData,
    AutomorphicDModuleData,
    SpectralIndCohData,
    CategoricalLanglandsEquivalenceData,
)


class TestCategoricalLanglandsLoom(unittest.TestCase):
    """Test suite for CategoricalLanglandsLoom algorithms and visualizers."""

    def setUp(self):
        self.loom = CategoricalLanglandsLoom(curve_genus=2)

    def test_curve_and_stack_initialization(self):
        """Verify algebraic curve and moduli stack Bun_G properties."""
        self.assertGreaterEqual(len(self.loom.curves), 1)
        crv = self.loom.curves[0]
        self.assertIsInstance(crv, AlgebraicCurveData)
        self.assertEqual(crv.genus, 2)
        self.assertEqual(crv.euler_characteristic, -2)  # 2 - 2*2 = -2
        self.assertEqual(crv.canonical_bundle_degree, 2)  # 2*2 - 2 = 2

        self.assertGreaterEqual(len(self.loom.automorphic_dmodules), 1)
        dmod = self.loom.automorphic_dmodules[0]
        self.assertIsInstance(dmod, AutomorphicDModuleData)
        # dim(Bun_SL2) = (g - 1) * 3 = 3
        self.assertEqual(dmod.dimension_bun_g, 3)
        self.assertEqual(dmod.characteristic_variety_dim, 3)
        self.assertTrue(dmod.is_whittaker_normalized)
        self.assertTrue(dmod.is_hecke_eigensheaf)

    def test_spectral_ind_coherent_sheaf(self):
        """Verify IndCoh_Nilp sheaf on derived stack LocSys_{G^vee}."""
        self.assertGreaterEqual(len(self.loom.spectral_sheaves), 1)
        sheaf = self.loom.spectral_sheaves[0]
        self.assertIsInstance(sheaf, SpectralIndCohData)
        self.assertEqual(sheaf.dual_group, "PGL_2")
        self.assertTrue(sheaf.is_nilpotent_cone_restricted)
        self.assertEqual(sheaf.cohomological_amplitude, (0, 2))
        self.assertEqual(sheaf.singular_support_dimension, 3)

    def test_hecke_eigensheaf_action(self):
        """Verify Hecke action evaluation and eigenvalue equation."""
        res = self.loom.evaluate_hecke_eigensheaf(point_coordinate_x=0.25, test_coweight=1)
        self.assertIsInstance(res, dict)
        self.assertEqual(res["representation_dimension"], 2)
        self.assertTrue(res["hecke_eigenvalue_verified"])
        self.assertIn("Sym^1(C^2)", res["representation_tested"])
        self.assertAlmostEqual(res["eigenvalue_scalar_trace"], 0.0, places=4)  # cos(pi/2) = 0

    def test_categorical_equivalence_synthesis(self):
        """Verify global categorical Langlands equivalence synthesis."""
        eq = self.loom.compute_categorical_equivalence("GLC-TEST-01")
        self.assertIsInstance(eq, CategoricalLanglandsEquivalenceData)
        self.assertTrue(eq.hecke_operator_matching)
        self.assertTrue(eq.whittaker_functor_faithfulness)
        self.assertTrue(eq.poincare_duality_compatibility)
        self.assertTrue(eq.trace_formula_spectral_agreement)
        self.assertIn("ARINKIN-GAITSGORY", eq.status_summary)

    def test_svg_and_zero_em_dash_compliance(self):
        """Verify SVG rendering, JSON telemetry, and zero em dashes across all outputs."""
        self.loom.evaluate_hecke_eigensheaf()
        self.loom.compute_categorical_equivalence()

        svg = self.loom.generate_langlands_svg()
        self.assertIsInstance(svg, str)
        self.assertTrue(svg.startswith("<svg"))
        self.assertTrue(svg.endswith("</svg>"))
        self.assertIn("Automorphic Side: D(Bun_G)", svg)
        self.assertIn("Hecke Correspondence", svg)
        self.assertIn("Spectral Side: IndCoh_Nilp", svg)

        # Strict zero em dash verification
        self.assertNotIn("\u2014", svg)
        self.assertNotIn(chr(8212), svg)

        json_str = self.loom.to_json()
        self.assertNotIn("\u2014", json_str)
        self.assertNotIn(chr(8212), json_str)

        with open("scripts/categorical_langlands_loom.py", encoding="utf-8") as f:
            src = f.read()
        self.assertNotIn("\u2014", src)
        self.assertNotIn(chr(8212), src)


if __name__ == "__main__":
    unittest.main()
