r"""
Unit tests for Relative Trace Formula & Gan-Gross-Prasad (GGP) Loom.
Verifies spherical subgroups, GGP branching laws, Ichino-Ikeda formula,
Arithmetic AGGP height pairings, and strict zero em dash compliance.
"""

import unittest
import math
import os
import sys

# Ensure scripts dir is accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))
from relative_trace_ggp_loom import (
    RelativeTraceGGPLoom,
    GGPArchetype,
    SphericalSubgroupData,
    GGPRepresentationPair,
    RelativeOrbitalIntegral,
    IchinoIkedaCentralValueData,
    ArithmeticAGGPHeightData,
    RelativeTraceEvaluation,
)


class TestRelativeTraceGGPLoom(unittest.TestCase):
    """Test suite for RelativeTraceGGPLoom."""

    def setUp(self):
        self.loom = RelativeTraceGGPLoom(
            spectral_parameter=1.0,
            subgroup_truncation=2.0,
            default_archetype=GGPArchetype.UNITARY_U3_U2.value,
        )

    def test_spherical_subgroup_and_ggp_representation(self):
        """Verify spherical pair U(3) x U(2) and GGP representation pair."""
        sd = self.loom.spherical_data
        self.assertIsNotNone(sd)
        self.assertIn("U(3)", sd.group_g_label)
        self.assertIn("U(2)", sd.subgroup_h_label)
        self.assertEqual(sd.dimension_g, 13)
        self.assertEqual(sd.dimension_h, 4)
        self.assertTrue(sd.is_symmetric_pair)

        rp = self.loom.rep_pair
        self.assertIsNotNone(rp)
        self.assertEqual(rp.hom_multiplicity, 1)
        self.assertLessEqual(rp.hom_multiplicity, 1)
        self.assertEqual(rp.vogan_packet_size, 4)
        self.assertTrue(rp.is_distinguished_by_h)
        self.assertEqual(rp.local_root_number_sign, 1)

    def test_relative_orbital_integrals(self):
        """Verify relative orbital integrals on double coset H \\ G / H."""
        orbitals = self.loom.relative_orbitals
        self.assertGreaterEqual(len(orbitals), 2)

        orb0 = orbitals[0]
        self.assertIn("1_G", orb0.double_coset_orbit)
        self.assertTrue(orb0.is_regular)
        self.assertGreater(orb0.relative_integral_value, 0.0)

        # Check total geometric sum
        eval_res = self.loom.evaluate_relative_trace()
        self.assertGreater(eval_res.rtf_geometric_total, 0.0)
        self.assertTrue(eval_res.ggp_multiplicity_one_holds)

    def test_ichino_ikeda_formula(self):
        """Verify Ichino-Ikeda formula relating period square to central L-value."""
        ii = self.loom.ichino_ikeda
        self.assertIsNotNone(ii)
        self.assertGreater(ii.central_l_value, 0.0)
        self.assertGreater(ii.adjoint_l1_value, 0.0)
        self.assertGreater(ii.adjoint_l2_value, 0.0)
        self.assertGreater(ii.normalized_period_square, 0.0)
        self.assertTrue(ii.conjecture_verified)

    def test_arithmetic_aggp_curve_and_vanishing(self):
        """Verify Arithmetic AGGP setting with L(1/2)=0 and non-vanishing L'(1/2)."""
        aggp_loom = RelativeTraceGGPLoom(
            spectral_parameter=1.0,
            default_archetype=GGPArchetype.ARITHMETIC_AGGP_CURVE.value,
        )
        self.assertEqual(aggp_loom.ichino_ikeda.central_l_value, 0.0)
        self.assertEqual(aggp_loom.ichino_ikeda.normalized_period_square, 0.0)

        ag = aggp_loom.aggp_height
        self.assertIsNotNone(ag)
        self.assertTrue(ag.is_exceptional_vanishing)
        self.assertGreater(ag.central_derivative_l_prime, 0.0)
        self.assertGreater(ag.beilinson_bloch_height, 0.0)
        self.assertEqual(ag.height_derivative_ratio, 1.0)

    def test_svg_generation_and_zero_em_dashes(self):
        """Verify dark titanium SVG generation and strict zero em dash compliance."""
        svg = self.loom.generate_svg()
        self.assertIn("<svg", svg)
        self.assertIn("Relative Trace Formula", svg)
        self.assertIn("GGP Branching Prism", svg)
        self.assertIn("Ichino-Ikeda", svg)

        # Verify zero em dashes across both test and engine scripts
        cur_file = __file__
        loom_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts", "relative_trace_ggp_loom.py"))
        for fpath in [cur_file, loom_file]:
            if os.path.exists(fpath):
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()
                self.assertNotIn("\u2014", content, f"Em dash found in {fpath}")


if __name__ == "__main__":
    unittest.main()
