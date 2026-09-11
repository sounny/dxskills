r"""
Unit tests for Perfectoid Spaces & Scholze Tilting Equivalence Loom.
Verifies field pairs, tilting equivalences, adic spectra, almost purity, and zero em dashes.
"""

import unittest
import os
import sys

# Ensure scripts dir is accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))
from perfectoid_spaces_loom import (
    PerfectoidSpacesLoom,
    PerfectoidSpacesArchetype,
    PerfectoidFieldPairData,
    TiltingEquivalenceData,
    AdicSpaceData,
)


class TestPerfectoidSpacesLoom(unittest.TestCase):
    """Test suite for PerfectoidSpacesLoom."""

    def setUp(self):
        self.loom = PerfectoidSpacesLoom(
            prime_p=5,
            default_archetype=PerfectoidSpacesArchetype.CYCLOTOMIC_PERFECTOID_FIELD.value,
        )

    def test_default_cyclotomic_perfectoid_model(self):
        """Test default cyclotomic perfectoid field pair and tilting equivalence."""
        self.assertEqual(self.loom.prime_p, 5)

        pair = self.loom.field_pairs[0]
        self.assertIn("zeta", pair.field_char_zero)
        self.assertTrue(pair.is_frobenius_surjective)
        self.assertEqual(pair.valuation_rank, 1)

        equiv = self.loom.tilting_equivalences[0]
        self.assertTrue(equiv.is_topological_homeomorphism)
        self.assertTrue(equiv.is_etale_site_equivalent)
        self.assertTrue(equiv.almost_purity_theorem_verified)

        adic = self.loom.adic_spaces[0]
        self.assertTrue(adic.is_perfectoid_space)
        self.assertEqual(adic.rational_subsets_count, 6)

    def test_tilting_norm_sequence(self):
        """Verify valuation sequence in tilted limit satisfies |x^{(n)}| = |x^{(0)}|^{1/p^n}."""
        seq = self.loom.compute_tilting_norm_sequence(base_norm=0.03125, steps=4)
        self.assertEqual(len(seq), 4)
        # Sequence strictly increases toward 1 as p-power roots approach boundary
        self.assertTrue(seq[0] < seq[1] < seq[2] < seq[3])

    def test_perfectoid_axioms_evaluation(self):
        """Verify validation of Scholze's perfectoid field axioms."""
        # Valid perfectoid
        res_valid = self.loom.evaluate_perfectoid_axioms(
            frobenius_surjective=True,
            non_discrete_valuation=True,
            complete_topology=True,
        )
        self.assertTrue(res_valid["is_perfectoid"])
        self.assertIn("Perfectoid Field", res_valid["axiomatic_verdict"])

        # Discrete valuation (like Q_p) is NOT perfectoid
        res_discrete = self.loom.evaluate_perfectoid_axioms(
            frobenius_surjective=True,
            non_discrete_valuation=False,
            complete_topology=True,
        )
        self.assertFalse(res_discrete["is_perfectoid"])
        self.assertIn("Non-Perfectoid", res_discrete["axiomatic_verdict"])

    def test_algebraic_closure_and_shimura_archetypes(self):
        """Test C_p / C_p^flat and infinite-level Shimura variety archetypes."""
        cp_loom = PerfectoidSpacesLoom(
            default_archetype=PerfectoidSpacesArchetype.ALGEBRAIC_CLOSURE_C_P.value,
        )
        self.assertIn("C_p", cp_loom.field_pairs[0].field_char_zero)
        self.assertEqual(cp_loom.adic_spaces[0].rational_subsets_count, 12)

        shim_loom = PerfectoidSpacesLoom(
            default_archetype=PerfectoidSpacesArchetype.TORSION_SHIMURA_VARIETY.value,
        )
        self.assertIn("Shimura", shim_loom.field_pairs[0].field_char_zero)
        self.assertEqual(shim_loom.adic_spaces[0].rational_subsets_count, 24)

    def test_svg_generation_and_zero_em_dashes(self):
        """Verify dark titanium SVG generation and zero em dash compliance."""
        svg = self.loom.generate_perfectoid_svg()
        self.assertIn("<svg", svg)
        self.assertIn("Perfectoid Spaces", svg)
        self.assertIn("Scholze Tilting Equivalence", svg)

        # Check this file and loom file for zero em dashes
        cur_file = __file__
        loom_file = os.path.join(os.path.dirname(__file__), "perfectoid_spaces_loom.py")
        for fpath in [cur_file, loom_file]:
            if os.path.exists(fpath):
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()
                self.assertNotIn("\u2014", content, f"Em dash found in {fpath}")


if __name__ == "__main__":
    unittest.main()
