r"""
Unit tests for Taylor-Wiles Patching & Modularity Lifting Loom.
Verifies residual Galois representations, Selmer group Euler characteristics,
Taylor-Wiles prime systems, Auslander-Buchsbaum freeness, R = T isomorphism,
and strict zero em dash compliance.
"""

import unittest
import math
import os
import sys

# Ensure scripts dir is accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))
from taylor_wiles_patching_loom import (
    TaylorWilesPatchingLoom,
    TaylorWilesArchetype,
    ResidualGaloisRepresentationData,
    SelmerGroupData,
    TaylorWilesPrimeData,
    PatchedModuleData,
    ModularityIsomorphismEvaluation,
)


class TestTaylorWilesPatchingLoom(unittest.TestCase):
    """Test suite for TaylorWilesPatchingLoom."""

    def setUp(self):
        self.loom = TaylorWilesPatchingLoom(
            prime_p=5,
            patching_level=2,
            default_archetype=TaylorWilesArchetype.FERMAT_FREY_CURVE.value,
        )

    def test_residual_representation_and_selmer_balance(self):
        """Verify residual Galois representation and Selmer Euler balance."""
        rr = self.loom.residual_rep
        self.assertIsNotNone(rr)
        self.assertEqual(rr.prime_p, 5)
        self.assertEqual(rr.conductor_level_n, 2)
        self.assertEqual(rr.serre_weight_k, 2)
        self.assertTrue(rr.is_absolutely_irreducible)
        self.assertTrue(rr.is_odd)

        sg = self.loom.selmer_group
        self.assertIsNotNone(sg)
        self.assertEqual(sg.euler_characteristic_deficit, 0)
        self.assertEqual(sg.selmer_dimension_h1, sg.dual_selmer_dimension_h1_perp)

    def test_taylor_wiles_primes_and_auxiliary_levels(self):
        """Verify Taylor-Wiles prime selection neutralizing dual Selmer."""
        tw = self.loom.tw_primes
        self.assertEqual(len(tw), self.loom.selmer_group.dual_selmer_dimension_h1_perp)

        for tp in tw:
            self.assertTrue(tp.is_taylor_wiles_prime)
            self.assertEqual(tp.torus_quotient_order, 5**2)
            self.assertNotEqual(tp.frobenius_alpha_eigenvalue, tp.frobenius_beta_eigenvalue)

    def test_patched_module_freeness_and_r_equals_t(self):
        """Verify Auslander-Buchsbaum freeness of M_infty and R = T theorem."""
        pm = self.loom.patched_module
        self.assertIsNotNone(pm)
        self.assertEqual(pm.module_rank_over_s_infty, 1)
        self.assertTrue(pm.is_free_s_infty_module)
        self.assertEqual(pm.complete_intersection_defect, 0)

        eval_res = self.loom.evaluate_modularity_lifting()
        self.assertTrue(eval_res.is_r_equals_t_isomorphism)
        self.assertTrue(eval_res.multiplicity_one_verified)
        self.assertEqual(eval_res.numerical_criterion_ratio, 1.0)
        self.assertGreater(eval_res.cognitive_resonance_score, 0.9)
        self.assertEqual(eval_res.spatial_stability_index, 0.96)

    def test_archetype_switching(self):
        """Verify ordinary, Kisin framed, and unitary Calegari-Geraghty archetypes."""
        ord_loom = TaylorWilesPatchingLoom(
            prime_p=7,
            default_archetype=TaylorWilesArchetype.TAYLOR_WILES_ORDINARY.value,
        )
        self.assertEqual(ord_loom.prime_p, 7)
        self.assertEqual(ord_loom.selmer_group.selmer_dimension_h1, 3)

        kisin_loom = TaylorWilesPatchingLoom(
            default_archetype=TaylorWilesArchetype.KISIN_POTENTIALLY_BARSOTTI_TATE.value,
        )
        self.assertIn("Barsotti-Tate", kisin_loom.residual_rep.representation_label)
        self.assertEqual(kisin_loom.patched_module.patching_depth_g, 4)

    def test_svg_generation_and_zero_em_dashes(self):
        """Verify dark titanium SVG generation and strict zero em dash compliance."""
        svg = self.loom.generate_svg()
        self.assertIn("<svg", svg)
        self.assertIn("Taylor-Wiles Patching", svg)
        self.assertIn("Galois Deformation Ring", svg)
        self.assertIn("Hecke Algebra", svg)
        self.assertIn("Taylor-Wiles Auxiliary Primes", svg)

        # Verify zero em dashes across both test and engine scripts
        cur_file = __file__
        loom_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts", "taylor_wiles_patching_loom.py"))
        for fpath in [cur_file, loom_file]:
            if os.path.exists(fpath):
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()
                self.assertNotIn("\u2014", content, f"Em dash found in {fpath}")


if __name__ == "__main__":
    unittest.main()
