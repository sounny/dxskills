"""
Unit tests for Arithmetic Geometry & Langlands-Shimura Variety Loom.
Strictly verifies zero em dashes (chr(8212)), Deligne Shimura data (G, X),
reflex fields, PEL moduli, Hecke orbit degrees, and etale cohomology.
"""

import unittest
import os
import json
from scripts.shimura_variety_loom import (
    ShimuraVarietyLoom,
    ShimuraType,
    PELDatumType,
    BoundaryStratumType,
)


class TestShimuraVarietyLoom(unittest.TestCase):
    """Test suite for ShimuraVarietyLoom engine and spatial cognitive mappings."""

    def setUp(self):
        self.loom = ShimuraVarietyLoom(
            shimura_type=ShimuraType.MODULAR_CURVE.value,
            dimension_g=1,
            level_n=1,
        )

    def test_shimura_datum_configuration(self):
        """Verify Deligne Shimura datum dimensions and canonical reflex fields."""
        sd = self.loom.shimura_datum
        self.assertIsNotNone(sd)
        self.assertEqual(sd.complex_dimension, 1)
        self.assertIn("Q", sd.reflex_field)
        self.assertIn("GL_2", sd.group_name)

        # Siegel modular variety test
        siegel_loom = ShimuraVarietyLoom(
            shimura_type=ShimuraType.SIEGEL_MODULAR.value,
            dimension_g=2,
            level_n=1,
        )
        ssd = siegel_loom.shimura_datum
        # For g=2, dim = g(g+1)/2 = 3
        self.assertEqual(ssd.complex_dimension, 3)
        self.assertIn("GSp_4", ssd.group_name)

        # Hilbert-Blumenthal test
        hilb_loom = ShimuraVarietyLoom(
            shimura_type=ShimuraType.HILBERT_BLUMENTHAL.value,
            dimension_g=2,
        )
        hsd = hilb_loom.shimura_datum
        self.assertEqual(hsd.complex_dimension, 2)
        self.assertIn("sqrt(5)", hsd.reflex_field)

        # Picard surface test
        pic_loom = ShimuraVarietyLoom(
            shimura_type=ShimuraType.PICARD_UNITARY.value,
            dimension_g=2,
        )
        psd = pic_loom.shimura_datum
        self.assertEqual(psd.complex_dimension, 2)
        self.assertIn("sqrt(-3)", psd.reflex_field)

    def test_pel_moduli_instantiation(self):
        """Verify polarized abelian variety moduli parameters."""
        moduli = self.loom.instantiate_pel_moduli("PEL-01")
        self.assertEqual(moduli.moduli_id, "PEL-01")
        self.assertEqual(moduli.abelian_dimension, 1)
        self.assertEqual(moduli.polarization_degree, 1)
        self.assertEqual(moduli.level_n, 1)
        self.assertEqual(moduli.moduli_dimension, 1)

    def test_hecke_orbit_degree(self):
        """Verify Hecke operator double coset degrees for GL_2 and GSp_4."""
        # For GL_2 and p=2, degree = p + 1 = 3
        h_gl2 = self.loom.evaluate_hecke_orbit("HECKE-GL2", prime_p=2)
        self.assertEqual(h_gl2.double_coset_degree, 3)
        self.assertEqual(h_gl2.orbit_points_count, 3)
        self.assertGreater(h_gl2.eigenvalue_estimate, 0.0)

        # For Siegel GSp_4 (g=2) and p=2, degree = (2 + 1) * (4 + 1) = 15
        siegel_loom = ShimuraVarietyLoom(
            shimura_type=ShimuraType.SIEGEL_MODULAR.value,
            dimension_g=2,
        )
        h_siegel = siegel_loom.evaluate_hecke_orbit("HECKE-GSP4", prime_p=2)
        self.assertEqual(h_siegel.double_coset_degree, 15)

    def test_etale_cohomology_decomposition(self):
        """Verify Langlands Galois representation dimensions in etale cohomology."""
        coh = self.loom.decompose_etale_cohomology("COH-01", degree=1)
        self.assertEqual(coh.degree, 1)
        self.assertEqual(coh.galois_rep_dim, 2)
        self.assertTrue(coh.ramanujan_bound_verified)
        self.assertGreater(coh.frobenius_eigenvalue, 0.0)

    def test_svg_json_and_zero_em_dashes(self):
        """Verify SVG generation, JSON export, and strict zero em dash compliance."""
        self.loom.instantiate_pel_moduli("PEL-TEST")
        self.loom.evaluate_hecke_orbit("HECKE-TEST")
        self.loom.decompose_etale_cohomology("COH-TEST")

        svg = self.loom.generate_shimura_svg()
        self.assertTrue(svg.startswith("<svg"))
        self.assertTrue(svg.endswith("</svg>"))
        self.assertIn("Arithmetic Geometry", svg)
        self.assertIn("Shimura Variety", svg)
        self.assertIn("Baily-Borel", svg)

        # Assert ZERO em dashes anywhere in generated SVG
        self.assertNotIn(chr(8212), svg)

        # Assert ZERO em dashes in JSON export
        json_data = self.loom.to_json()
        self.assertNotIn(chr(8212), json_data)

        # Verify source file has zero em dashes
        loom_path = os.path.join(os.path.dirname(__file__), "..", "scripts", "shimura_variety_loom.py")
        with open(loom_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertNotIn(chr(8212), content)


if __name__ == "__main__":
    unittest.main()
