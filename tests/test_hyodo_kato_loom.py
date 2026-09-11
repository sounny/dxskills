"""
Tests for Hodge-Tate Spectral Sequences & Hyodo-Kato Cohomology Loom.
Verifies log-crystalline cohomology H_HK^m, log-Frobenius phi, log-monodromy N,
monodromy weight filtration, Hard Lefschetz isomorphisms, and strict zero em dash compliance.
"""

import unittest
from scripts.hyodo_kato_loom import (
    HyodoKatoCohomologyLoom,
    SemistableReductionArchetype,
    LogCrystallineCohomologyData,
    MonodromyWeightFiltrationData,
    HyodoKatoComparisonData,
)


class TestHyodoKatoCohomologyLoom(unittest.TestCase):
    """Test suite for HyodoKatoCohomologyLoom algorithms and visualizers."""

    def setUp(self):
        self.loom = HyodoKatoCohomologyLoom(
            cohomology_degree=2,
            base_prime_p=5,
            toric_rank=2,
            default_archetype=SemistableReductionArchetype.CALABI_YAU_DEGENERATION.value,
        )

    def test_log_crystalline_cohomology_and_operators(self):
        """Verify log-crystalline cohomology invariants and N phi = p phi N."""
        self.assertGreaterEqual(len(self.loom.log_cris_records), 1)
        rec = self.loom.log_cris_records[0]
        self.assertIsInstance(rec, LogCrystallineCohomologyData)
        self.assertEqual(rec.cohomology_degree_m, 2)
        # For degree 2 with toric rank 2: hodge numbers [1, 2, 1], dim = 4
        self.assertEqual(rec.k0_vector_space_dim, 4)
        self.assertEqual(rec.monodromy_n_nilpotency_order, 3)
        self.assertTrue(rec.n_phi_relation_verified)
        self.assertEqual(rec.frobenius_slopes, [0.0, 1.0, 2.0])

    def test_monodromy_weight_filtration(self):
        """Verify monodromy weight filtration Gr_j^M and weight-monodromy conjecture."""
        self.assertGreaterEqual(len(self.loom.weight_filtrations), 1)
        wf = self.loom.weight_filtrations[0]
        self.assertIsInstance(wf, MonodromyWeightFiltrationData)
        self.assertEqual(wf.cohomology_degree, 2)
        self.assertEqual(wf.weight_graded_dims["Gr_2^M"], 2)
        self.assertTrue(wf.hard_lefschetz_isomorphisms)
        self.assertTrue(wf.weight_monodromy_conjecture_satisfied)
        # Weights p^0 = 1, p^1 = 5, p^2 = 25
        self.assertEqual(wf.p_weight_eigenvalues, [1.0, 5.0, 25.0])

    def test_monodromy_nilpotency_evaluation(self):
        """Verify Hard Lefschetz isomorphism N^k: Gr_{m+k}^M -> Gr_{m-k}^M."""
        res = self.loom.evaluate_monodromy_nilpotency(test_step=2)
        self.assertIsInstance(res, dict)
        self.assertTrue(res["hard_lefschetz_isomorphism"])
        self.assertEqual(res["commutation_scalar"], "p^2 = 25")
        self.assertIn("Gr_{4}^M", res["source_graded_piece"])
        self.assertIn("Gr_{0}^M", res["target_graded_piece"])

    def test_hyodo_kato_comparison(self):
        """Verify Hyodo-Kato comparison isomorphism and Hodge-Tate E_1 degeneration."""
        self.assertGreaterEqual(len(self.loom.comparison_records), 1)
        comp = self.loom.compute_hyodo_kato_comparison("HK-TEST-01", "pi_Eisenstein")
        self.assertIsInstance(comp, HyodoKatoComparisonData)
        self.assertEqual(comp.comparison_id, "HK-TEST-01")
        self.assertEqual(comp.de_rham_dim, 4)
        self.assertTrue(comp.hodge_tate_degeneration_e1)
        self.assertTrue(comp.tsuji_c_st_established)

    def test_svg_and_zero_em_dash_compliance(self):
        """Verify dark titanium SVG rendering, JSON telemetry, and zero em dashes."""
        self.loom.compute_hyodo_kato_comparison()

        svg = self.loom.generate_hyodo_kato_svg()
        self.assertIsInstance(svg, str)
        self.assertTrue(svg.startswith("<svg"))
        self.assertTrue(svg.endswith("</svg>"))
        self.assertIn("Hodge-Tate Spectral Sequences &amp; Hyodo-Kato Cohomology Loom", svg)
        self.assertIn("Semistable Log-Structure", svg)
        self.assertIn("Frobenius &amp; Monodromy Operators", svg)
        self.assertIn("Monodromy Weight Filtration", svg)

        # Strict zero em dash verification
        self.assertNotIn("\u2014", svg)
        self.assertNotIn(chr(8212), svg)

        json_str = self.loom.to_json()
        self.assertNotIn("\u2014", json_str)
        self.assertNotIn(chr(8212), json_str)

        with open("scripts/hyodo_kato_loom.py", encoding="utf-8") as f:
            src = f.read()
        self.assertNotIn("\u2014", src)
        self.assertNotIn(chr(8212), src)


if __name__ == "__main__":
    unittest.main()
