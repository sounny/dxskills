"""
Unit tests for Derived Algebraic Geometry & Lurie Spectral Schemes Loom.
Strictly verifies zero em dashes (chr(8212)), derived Postnikov towers,
relative cotangent complexes, virtual dimensions, and spectral Picard modules.
"""

import unittest
import os
import json
from scripts.derived_geometry_loom import (
    DerivedGeometryLoom,
    DerivedSchemeArchetype,
    RingSpectraType,
)


class TestDerivedGeometryLoom(unittest.TestCase):
    """Test suite for DerivedGeometryLoom engine and spatial cognitive mappings."""

    def setUp(self):
        self.loom = DerivedGeometryLoom(
            primary_spectrum=RingSpectraType.TMF_TOPOLOGICAL_MODULAR_FORMS.value,
            default_archetype=DerivedSchemeArchetype.DERIVED_CRITICAL_LOCUS.value,
        )

    def test_derived_scheme_initialization(self):
        """Verify default derived scheme, virtual dimension, and Postnikov sheaves."""
        self.assertEqual(len(self.loom.derived_schemes), 1)
        s = self.loom.derived_schemes[0]
        self.assertEqual(s.classical_dimension, 2)
        self.assertEqual(s.virtual_dimension, 0)
        self.assertTrue(s.is_quasi_smooth)
        self.assertEqual(s.homotopical_depth, 3)
        self.assertIn("pi_0", s.homotopy_sheaves)
        self.assertIn("pi_1", s.homotopy_sheaves)
        self.assertIn("pi_2", s.homotopy_sheaves)
        self.assertIn("pi_3", s.homotopy_sheaves)

    def test_cotangent_complex_evaluation(self):
        """Verify cotangent complex amplitude, Euler characteristic, and LCI regime."""
        cc = self.loom.evaluate_cotangent_complex(
            complex_id="L-01",
            amplitude_low=-1,
            amplitude_high=0,
            ext0_automorphisms=0,
            ext2_obstructions=0,
        )
        self.assertEqual(cc.amplitude_low, -1)
        self.assertEqual(cc.amplitude_high, 0)
        self.assertTrue(cc.is_perfect_complex)
        self.assertIn("Quasi-Smooth", cc.deformation_regime)

        # Smooth scheme test
        cc_sm = self.loom.evaluate_cotangent_complex(
            complex_id="L-SMOOTH",
            amplitude_low=0,
            amplitude_high=0,
        )
        self.assertIn("Smooth", cc_sm.deformation_regime)

    def test_spectral_sheaf_evaluation(self):
        """Verify TMF spectral sheaf, Picard rank, and torsion invariants."""
        sh_tmf = self.loom.evaluate_spectral_sheaf(
            sheaf_id="SHEAF-TMF",
            ring_spectrum=RingSpectraType.TMF_TOPOLOGICAL_MODULAR_FORMS.value,
            picard_rank=1,
        )
        self.assertEqual(sh_tmf.picard_rank, 1)
        self.assertIn(24, sh_tmf.torsion_invariants)
        self.assertTrue(sh_tmf.has_higher_homotopical_invertibles)
        self.assertEqual(len(sh_tmf.chern_character_degrees), 4)

        # KU sheaf test
        sh_ku = self.loom.evaluate_spectral_sheaf(
            sheaf_id="SHEAF-KU",
            ring_spectrum=RingSpectraType.KU_COMPLEX_K_THEORY.value,
            picard_rank=2,
        )
        self.assertEqual(sh_ku.picard_rank, 2)
        self.assertIn(2, sh_ku.torsion_invariants)

    def test_alternative_derived_archetypes(self):
        """Verify spectral elliptic moduli stack M_ell and derived self-intersections."""
        s_ell = self.loom.construct_derived_scheme(
            scheme_id="DER-ELL",
            archetype=DerivedSchemeArchetype.SPECTRAL_ELLIPTIC_MODULI.value,
            classical_dimension=1,
            virtual_dimension=1,
            homotopical_depth=4,
            structure_formula="M_ell with Goerss-Hopkins-Miller O_top",
            is_quasi_smooth=True,
        )
        self.assertEqual(s_ell.classical_dimension, 1)
        self.assertTrue(s_ell.is_quasi_smooth)

        s_int = self.loom.construct_derived_scheme(
            scheme_id="DER-INT",
            archetype=DerivedSchemeArchetype.DERIVED_INTERSECTION.value,
            classical_dimension=1,
            virtual_dimension=-1,
            homotopical_depth=2,
            structure_formula="X x^R_Y Z with Tor_i sheaves",
            is_quasi_smooth=False,
        )
        self.assertFalse(s_int.is_quasi_smooth)
        self.assertEqual(s_int.virtual_dimension, -1)

    def test_svg_json_and_zero_em_dashes(self):
        """Verify SVG generation, JSON export, and strict zero em dash compliance."""
        self.loom.evaluate_cotangent_complex("L-TEST", -1, 0)
        self.loom.evaluate_spectral_sheaf("SH-TEST", RingSpectraType.TMF_TOPOLOGICAL_MODULAR_FORMS.value)

        svg = self.loom.generate_derived_svg()
        self.assertTrue(svg.startswith("<svg"))
        self.assertTrue(svg.endswith("</svg>"))
        self.assertIn("Derived Algebraic Geometry", svg)
        self.assertIn("Postnikov", svg)
        self.assertIn("Cotangent Complex", svg)

        # Assert ZERO em dashes anywhere in generated SVG
        self.assertNotIn(chr(8212), svg)

        # Assert ZERO em dashes in JSON export
        json_data = self.loom.to_json()
        self.assertNotIn(chr(8212), json_data)

        # Verify source file has zero em dashes
        loom_path = os.path.join(os.path.dirname(__file__), "..", "scripts", "derived_geometry_loom.py")
        if os.path.exists(loom_path):
            with open(loom_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertNotIn(chr(8212), content)


if __name__ == "__main__":
    unittest.main()
