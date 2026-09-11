r"""
Unit tests for Serre's Modularity Conjecture & Odd Galois Representations Loom.
Verifies Serre invariants, tame inertia weights, Khare-Wintenberger theorem, and zero em dashes.
"""

import unittest
import os
import sys

# Ensure scripts dir is accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))
from serre_modularity_loom import (
    SerreModularityLoom,
    SerreModularityArchetype,
    OddGaloisRepresentationData,
    SerreInvariantsData,
    KhareWintenbergerModularityData,
)


class TestSerreModularityLoom(unittest.TestCase):
    """Test suite for SerreModularityLoom."""

    def setUp(self):
        self.loom = SerreModularityLoom(
            level_n=11,
            prime_p=5,
            default_archetype=SerreModularityArchetype.WEIGHT_TWO_ELLIPTIC.value,
        )

    def test_default_weight_two_elliptic_model(self):
        """Test default elliptic curve residual representation."""
        self.assertEqual(self.loom.level_n, 11)
        self.assertEqual(self.loom.prime_p, 5)

        rep = self.loom.representations[0]
        self.assertTrue(rep.is_odd)
        self.assertTrue(rep.is_irreducible)
        self.assertEqual(rep.dimension, 2)
        self.assertEqual(rep.artin_conductor_prime_to_p, 11)

        inv = self.loom.serre_invariants[0]
        self.assertEqual(inv.serre_level_n, 11)
        self.assertEqual(inv.serre_weight_k, 2)
        self.assertTrue(inv.is_fontaine_laffaille)

        mod = self.loom.modularity_data[0]
        self.assertTrue(mod.is_modular)
        self.assertIn("S_2(Gamma_0(11))", mod.modular_eigenform_space)

    def test_serre_weight_computation(self):
        """Verify Serre weight computation from tame inertia powers."""
        # Tame weights a = 0, b = 1 -> k = 1 + 1 - 0 = 2
        k2 = self.loom.compute_serre_weight_level_one(0, 1, 5)
        self.assertEqual(k2, 2)

        # Tame weights a = 0, b = 11 -> k = 1 + 11 = 12
        k12 = self.loom.compute_serre_weight_level_one(0, 11, 5)
        self.assertEqual(k12, 12)

    def test_serre_conjecture_verdict_and_parity_obstruction(self):
        """Verify odd modular case vs even non-modular parity obstruction."""
        # Odd and irreducible -> modular
        res_mod = self.loom.evaluate_serre_conjecture(
            is_odd=True,
            is_irreducible=True,
            level_n=11,
            weight_k=2,
        )
        self.assertTrue(res_mod["is_modular"])
        self.assertIn("Modular", res_mod["serre_verdict"])

        # Even representation -> non-modular parity obstruction
        res_even = self.loom.evaluate_serre_conjecture(
            is_odd=False,
            is_irreducible=True,
            level_n=1,
            weight_k=2,
        )
        self.assertFalse(res_even["is_modular"])
        self.assertIn("Parity", res_even["serre_verdict"])

    def test_ramanujan_and_even_archetypes(self):
        """Test Ramanujan Delta and Even Non-Modular archetypes."""
        ram_loom = SerreModularityLoom(
            default_archetype=SerreModularityArchetype.RAMANUJAN_DELTA_MOD_P.value,
        )
        self.assertEqual(ram_loom.serre_invariants[0].serre_weight_k, 12)
        self.assertTrue(ram_loom.modularity_data[0].is_modular)

        even_loom = SerreModularityLoom(
            default_archetype=SerreModularityArchetype.EVEN_NON_MODULAR.value,
        )
        self.assertFalse(even_loom.representations[0].is_odd)
        self.assertFalse(even_loom.modularity_data[0].is_modular)

    def test_svg_generation_and_zero_em_dashes(self):
        """Verify dark titanium SVG generation and zero em dash compliance."""
        svg = self.loom.generate_serre_svg()
        self.assertIn("<svg", svg)
        self.assertIn("Serre's Modularity Conjecture", svg)
        self.assertIn("Khare-Wintenberger", svg)

        # Check this file and loom file for zero em dashes
        cur_file = __file__
        loom_file = os.path.join(os.path.dirname(__file__), "serre_modularity_loom.py")
        for fpath in [cur_file, loom_file]:
            if os.path.exists(fpath):
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()
                self.assertNotIn("\u2014", content, f"Em dash found in {fpath}")


if __name__ == "__main__":
    unittest.main()
