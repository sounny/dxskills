r"""
Unit tests for Fontaine-Mazur Conjecture & Geometric Galois Representations Loom.
Verifies period rings, Hodge-Tate weights, Sen polynomials, and zero em dashes.
"""

import unittest
import os
import sys

# Ensure scripts dir is accessible
sys.path.insert(0, os.path.abspath(r"C:\Users\sounn\.gemini\antigravity\brain\d458b56e-3188-4374-8cf3-234474d7caec\scratch"))
from fontaine_mazur_loom import (
    FontaineMazurLoom,
    FontaineMazurArchetype,
    FontainePeriodRingData,
    HodgeTateData,
    GeometricModularityData,
)


class TestFontaineMazurLoom(unittest.TestCase):
    """Test suite for FontaineMazurLoom."""

    def setUp(self):
        self.loom = FontaineMazurLoom(
            dimension=2,
            prime_p=5,
            default_archetype=FontaineMazurArchetype.ELLIPTIC_CURVE_TATE_MODULE.value,
        )

    def test_default_elliptic_curve_tate_module(self):
        """Test default elliptic curve Tate module model."""
        self.assertEqual(self.loom.dimension, 2)
        self.assertEqual(self.loom.prime_p, 5)
        self.assertTrue(len(self.loom.period_rings) >= 4)
        
        # Check B_dR and B_HT admissibility
        ring_dict = {r.ring_name.split()[0]: r for r in self.loom.period_rings}
        self.assertTrue(ring_dict["B_HT"].is_admissible)
        self.assertTrue(ring_dict["B_dR"].is_admissible)
        self.assertTrue(ring_dict["B_cris"].is_admissible)

        ht = self.loom.hodge_tate_data[0]
        self.assertEqual(ht.hodge_tate_weights, [0, 1])
        self.assertEqual(len(ht.sen_polynomial_coefficients), 3)

        gm = self.loom.geometric_modularity[0]
        self.assertTrue(gm.is_geometric_representation)
        self.assertTrue(gm.is_unramified_almost_everywhere)
        self.assertTrue(gm.is_de_rham_at_p)

    def test_sen_polynomial_computation(self):
        """Verify Sen polynomial roots match Hodge-Tate weights."""
        # For weights [0, 1], poly = T(T - 1) = T^2 - T
        poly = self.loom.compute_sen_polynomial([0, 1])
        self.assertEqual(poly, [1.0, -1.0, 0.0])

        # For weights [0, 11], poly = T(T - 11) = T^2 - 11T
        poly_delta = self.loom.compute_sen_polynomial([0, 11])
        self.assertEqual(poly_delta, [1.0, -11.0, 0.0])

    def test_fontaine_mazur_conjecture_verdict(self):
        """Test conjecture evaluation under various geometric and exotic scenarios."""
        # Geometric case
        res_geom = self.loom.evaluate_fontaine_mazur_conjecture(unramified_ae=True, de_rham=True)
        self.assertTrue(res_geom["is_geometric"])
        self.assertIn("Geometric", res_geom["fontaine_mazur_verdict"])

        # Ramified everywhere
        res_ram = self.loom.evaluate_fontaine_mazur_conjecture(unramified_ae=False, de_rham=True)
        self.assertFalse(res_ram["is_geometric"])
        self.assertIn("Ramified", res_ram["fontaine_mazur_verdict"])

        # Non-de Rham
        res_non_dr = self.loom.evaluate_fontaine_mazur_conjecture(unramified_ae=True, de_rham=False)
        self.assertFalse(res_non_dr["is_geometric"])
        self.assertIn("de Rham", res_non_dr["fontaine_mazur_verdict"])

    def test_ramanujan_and_dirichlet_archetypes(self):
        """Test Ramanujan Delta and Dirichlet character twist archetypes."""
        delta_loom = FontaineMazurLoom(
            default_archetype=FontaineMazurArchetype.RAMANUJAN_DELTA_REP.value,
        )
        self.assertEqual(delta_loom.hodge_tate_data[0].hodge_tate_weights, [0, 11])
        self.assertTrue(delta_loom.geometric_modularity[0].is_geometric_representation)

        dir_loom = FontaineMazurLoom(
            default_archetype=FontaineMazurArchetype.DIRICHLET_TATE_TWIST.value,
        )
        self.assertEqual(dir_loom.dimension, 1)
        self.assertEqual(dir_loom.hodge_tate_data[0].hodge_tate_weights, [1])

    def test_svg_generation_and_zero_em_dashes(self):
        """Verify dark titanium SVG generation and strict zero em dash compliance."""
        svg = self.loom.generate_fontaine_mazur_svg()
        self.assertIn("<svg", svg)
        self.assertIn("Fontaine-Mazur Conjecture", svg)
        self.assertIn("B_dR", svg)

        # Check this file and loom file for zero em dashes
        cur_file = __file__
        loom_file = os.path.join(os.path.dirname(__file__), "fontaine_mazur_loom.py")
        for fpath in [cur_file, loom_file]:
            if os.path.exists(fpath):
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()
                self.assertNotIn("\u2014", content, f"Em dash found in {fpath}")


if __name__ == "__main__":
    unittest.main()
