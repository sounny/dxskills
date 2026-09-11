"""
Unit tests for Geometric Langlands Correspondence & Beilinson-Drinfeld Hecke Loom.
Strictly verifies zero em dashes (chr(8212)), Bun_G dimensions,
Hecke eigensheaf critical levels, and Hitchin SYZ mirror symmetry.
"""

import unittest
import os
import json
from scripts.geometric_langlands_loom import (
    GeometricLanglandsLoom,
    LanglandsGroupPair,
    DualitySide,
    HeckeRepresentationType,
)


class TestGeometricLanglandsLoom(unittest.TestCase):
    """Test suite for GeometricLanglandsLoom engine and spatial cognitive mappings."""

    def setUp(self):
        self.loom = GeometricLanglandsLoom(genus=2, group_pair=LanglandsGroupPair.SL2_PGL2.value)

    def test_initialization_and_dimensions(self):
        """Verify Bun_G and Hitchin base dimensions across genus and Lie ranks."""
        m = self.loom.mirror_data
        self.assertIsNotNone(m)
        # For g=2, SL(2): (2^2 - 1) * (2 - 1) = 3
        self.assertEqual(m.bun_g_dimension, 3)
        self.assertEqual(m.base_dimension, 3)
        self.assertEqual(m.fiber_torus_dim, 3)
        self.assertEqual(m.dual_torus_dim, 3)
        self.assertTrue(m.mirror_symmetry_verified)

        # Higher genus and rank test
        higher_loom = GeometricLanglandsLoom(genus=3, group_pair=LanglandsGroupPair.SL3_PGL3.value)
        hm = higher_loom.mirror_data
        # For g=3, SL(3): (3^2 - 1) * (3 - 1) = 8 * 2 = 16
        self.assertEqual(hm.bun_g_dimension, 16)
        self.assertEqual(hm.base_dimension, 16)
        self.assertEqual(hm.fiber_torus_dim, 16)
        self.assertEqual(hm.dual_torus_dim, 16)

    def test_local_system_and_oper(self):
        """Verify Galois local system construction and oper structure."""
        ls = self.loom.create_local_system("LS-01", is_oper=True)
        self.assertEqual(ls.system_id, "LS-01")
        self.assertTrue(ls.is_oper)
        self.assertEqual(ls.nilpotent_support_norm, 0.0)
        self.assertEqual(len(ls.monodromy_eigenvalues), 2)

        # Check serialization dictionary
        d = ls.to_dict()
        self.assertIn("system_id", d)
        self.assertIn("monodromy_eigenvalues", d)

    def test_automorphic_dmodule_and_critical_level(self):
        """Verify Hecke eigensheaf D-module synthesis and critical level k = -h^vee."""
        ls = self.loom.create_local_system("LS-02")
        dmod = self.loom.synthesize_hecke_eigensheaf("DMOD-01", ls.system_id)
        self.assertEqual(dmod.dmodule_id, "DMOD-01")
        self.assertEqual(dmod.hecke_eigenvalue_system_id, "LS-02")
        self.assertTrue(dmod.is_eigensheaf)
        # Dual Coxeter number for SL(2) is 2, critical level = -2.0
        self.assertEqual(dmod.critical_level, -2.0)
        self.assertEqual(dmod.singular_support_dim, 3)

    def test_hecke_operator_actions(self):
        """Verify Hecke operator actions and eigenvalue relations."""
        self.loom.create_local_system("LS-03")
        self.loom.synthesize_hecke_eigensheaf("DMOD-02", "LS-03")

        # Fundamental representation Hecke operator
        h_fund = self.loom.evaluate_hecke_action(
            "HECKE-FUND",
            marked_point_x="x_0",
            representation_type=HeckeRepresentationType.FUNDAMENTAL.value,
        )
        self.assertEqual(h_fund.representation_dimension, 2)
        self.assertTrue(h_fund.relation_verified)

        # Adjoint representation Hecke operator
        h_adj = self.loom.evaluate_hecke_action(
            "HECKE-ADJ",
            marked_point_x="x_1",
            representation_type=HeckeRepresentationType.ADJOINT.value,
        )
        # For SL(2), adjoint dim = 2^2 - 1 = 3
        self.assertEqual(h_adj.representation_dimension, 3)
        self.assertTrue(h_adj.relation_verified)

    def test_hitchin_syz_mirror_symmetry(self):
        """Verify classical limit SYZ dual torus fibration and Fourier-Mukai transform."""
        m = self.loom.mirror_data
        self.assertEqual(m.fiber_torus_dim, m.dual_torus_dim)
        self.assertIn("Poincare", m.fourier_mukai_kernel)

    def test_svg_json_and_zero_em_dashes(self):
        """Verify SVG generation, JSON export, and strict zero em dash compliance."""
        self.loom.create_local_system("LS-TEST")
        self.loom.synthesize_hecke_eigensheaf("DMOD-TEST", "LS-TEST")
        self.loom.evaluate_hecke_action("HECKE-TEST")

        svg = self.loom.generate_langlands_svg()
        self.assertTrue(svg.startswith("<svg"))
        self.assertTrue(svg.endswith("</svg>"))
        self.assertIn("Geometric Langlands", svg)
        self.assertIn("Automorphic", svg)
        self.assertIn("Spectral", svg)

        # Assert ZERO em dashes anywhere in generated SVG
        self.assertNotIn(chr(8212), svg)

        # Assert ZERO em dashes in JSON export
        json_data = self.loom.to_json()
        self.assertNotIn(chr(8212), json_data)

        # Verify source file has zero em dashes
        loom_path = os.path.join(os.path.dirname(__file__), "..", "scripts", "geometric_langlands_loom.py")
        with open(loom_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertNotIn(chr(8212), content)


if __name__ == "__main__":
    unittest.main()
