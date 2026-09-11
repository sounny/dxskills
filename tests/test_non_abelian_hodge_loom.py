"""
Unit tests for Non-Abelian Hodge Theory & Hitchin-Simpson Corlette Loom.
Strictly verifies zero em dashes (chr(8212)), Hitchin base dimensions,
harmonic metric solutions, and Simpson correspondence twistor rotations.
"""

import unittest
import math
import os
import json
from scripts.non_abelian_hodge_loom import (
    NonAbelianHodgeLoom,
    ModuliComponent,
    GaugeGroup,
    StabilityClassification,
)


class TestNonAbelianHodgeLoom(unittest.TestCase):
    """Test suite for NonAbelianHodgeLoom engine and spatial cognitive mappings."""

    def setUp(self):
        self.loom = NonAbelianHodgeLoom(genus=2, rank=2, group=GaugeGroup.SL2C.value)

    def test_hitchin_base_dimensions(self):
        """Verify Riemann-Roch base dimensions, moduli dimensions, and Prym variety."""
        base = self.loom.hitchin_base
        self.assertIsNotNone(base)
        # For g=2, r=2: base_dim = (2^2 - 1) * (2 - 1) = 3
        self.assertEqual(base.base_dimension, 3)
        self.assertEqual(base.moduli_dimension, 6)
        # Spectral curve genus: 1 + 2^2 * (2 - 1) = 5
        self.assertEqual(base.spectral_curve_genus, 5)
        # Prym dimension: 5 - 2 = 3 = base_dimension
        self.assertEqual(base.prym_variety_dimension, 3)

        # Higher genus and rank test
        higher_loom = NonAbelianHodgeLoom(genus=3, rank=3, group=GaugeGroup.SL3C.value)
        h_base = higher_loom.hitchin_base
        # For g=3, r=3: base_dim = (3^2 - 1) * (3 - 1) = 8 * 2 = 16
        self.assertEqual(h_base.base_dimension, 16)
        self.assertEqual(h_base.moduli_dimension, 32)
        # Spectral curve genus: 1 + 9 * 2 = 19
        self.assertEqual(h_base.spectral_curve_genus, 19)
        # Prym dimension: 19 - 3 = 16 = base_dimension
        self.assertEqual(h_base.prym_variety_dimension, 16)

    def test_higgs_bundle_creation_and_stability(self):
        """Verify Higgs bundle construction and slope stability parameters."""
        bundle = self.loom.create_higgs_bundle("HB-01", degree=0)
        self.assertEqual(bundle.bundle_id, "HB-01")
        self.assertEqual(bundle.rank, 2)
        self.assertEqual(bundle.degree, 0)
        self.assertEqual(bundle.slope, 0.0)
        self.assertEqual(bundle.canonical_degree, 2)
        self.assertEqual(bundle.stability, StabilityClassification.STABLE.value)

        # Check serialization dictionary
        d = bundle.to_dict()
        self.assertIn("bundle_id", d)
        self.assertIn("higgs_field_matrix", d)
        self.assertEqual(len(d["higgs_field_matrix"]), 2)

    def test_harmonic_metric_solver(self):
        """Verify Hitchin-Simpson-Corlette harmonic metric solver and defect."""
        bundle = self.loom.create_higgs_bundle("HB-02")
        metric = self.loom.solve_harmonic_metric(bundle.bundle_id)
        self.assertTrue(metric.is_harmonic)
        self.assertLess(metric.hitchin_defect, 1e-4)
        self.assertEqual(len(metric.hermitian_matrix), 2)
        self.assertGreater(metric.hermitian_matrix[0][0], 0.0)

    def test_simpson_correspondence_and_hyperkahler_rotation(self):
        """Verify hyperkahler twistor rotations and moduli correspondence regimes."""
        # Theta = 0: Dolbeault
        corr_dol = self.loom.compute_simpson_correspondence("SIMP-DOL", theta=0.0)
        self.assertIn("Dolbeault", corr_dol.complex_structure)

        # Theta = pi / 2: de Rham flat connection
        corr_dr = self.loom.compute_simpson_correspondence("SIMP-DR", theta=math.pi / 2.0)
        self.assertIn("de Rham", corr_dr.complex_structure)

        # Theta = pi: Hyperkahler twistor inversion
        corr_tw = self.loom.compute_simpson_correspondence("SIMP-TW", theta=math.pi)
        self.assertIn("Complex Structure K", corr_tw.complex_structure)

        self.assertIn("gamma_A1", corr_dol.monodromy_generators)
        self.assertIn("gamma_B1", corr_dol.monodromy_generators)

    def test_spectral_curve_evaluation(self):
        """Verify spectral curve characteristic evaluation."""
        val = self.loom.evaluate_spectral_curve(lambda_param=1.0 + 0j)
        self.assertAlmostEqual(val.real, 0.25)

    def test_moduli_svg_and_zero_em_dashes(self):
        """Verify SVG generation, JSON export, and strict zero em dash compliance."""
        self.loom.create_higgs_bundle("HB-TEST")
        self.loom.solve_harmonic_metric("HB-TEST")
        self.loom.compute_simpson_correspondence("CORR-TEST", theta=0.5)

        svg = self.loom.generate_moduli_svg()
        self.assertTrue(svg.startswith("<svg"))
        self.assertTrue(svg.endswith("</svg>"))
        self.assertIn("Non-Abelian Hodge", svg)
        self.assertIn("Hitchin Base", svg)

        # Assert ZERO em dashes anywhere in generated SVG
        self.assertNotIn(chr(8212), svg)

        # Assert ZERO em dashes in JSON export
        json_data = self.loom.to_json()
        self.assertNotIn(chr(8212), json_data)

        # Verify source file has zero em dashes
        loom_path = os.path.join(os.path.dirname(__file__), "..", "scripts", "non_abelian_hodge_loom.py")
        with open(loom_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertNotIn(chr(8212), content)


if __name__ == "__main__":
    unittest.main()
