r"""
Unit tests for Fargues-Scholze Geometrization of Local Langlands Loom.
Verifies Bun_G stacks, local shtukas, excursion operators, and zero em dashes.
"""

import unittest
import os
import sys

# Ensure scripts dir is accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))
from fargues_scholze_loom import (
    FarguesScholzeLoom,
    FarguesScholzeArchetype,
    BunGData,
    LocalShtukaData,
    ExcursionOperatorData,
)


class TestFarguesScholzeLoom(unittest.TestCase):
    """Test suite for FarguesScholzeLoom."""

    def setUp(self):
        self.loom = FarguesScholzeLoom(
            group_label="GL_2",
            prime_p=5,
            default_archetype=FarguesScholzeArchetype.GL2_UNRAMIFIED.value,
        )

    def test_default_gl2_unramified_model(self):
        """Test default GL_2 unramified model."""
        self.assertEqual(self.loom.group_label, "GL_2")
        self.assertEqual(self.loom.prime_p, 5)

        bun = self.loom.bun_g_models[0]
        self.assertEqual(bun.group_label, "GL_2")
        self.assertTrue(len(bun.newton_strata) >= 2)
        self.assertTrue(bun.is_quasi_compact_open)

        sht = self.loom.local_shtukas[0]
        self.assertEqual(sht.legs_count, 1)
        self.assertTrue(sht.compactly_supported_cohomology)

        exc = self.loom.excursion_operators[0]
        self.assertTrue(exc.is_semisimple_l_parameter)
        self.assertEqual(exc.monodromy_operator_order, 0)

    def test_excursion_trace_computation(self):
        """Verify excursion trace sequence growth under Frobenius powers."""
        traces = self.loom.compute_excursion_trace(base_trace=2.0, test_powers=4)
        self.assertEqual(len(traces), 4)
        self.assertEqual(traces[0], 2.0)
        # Sequence strictly scales with p^(0.5*(n-1))
        self.assertTrue(traces[0] < traces[1] < traces[2] < traces[3])

    def test_geometrization_theorem_evaluation(self):
        """Verify geometrization theorem criteria for reductive groups over local fields."""
        # Reductive p-adic case
        res_valid = self.loom.evaluate_geometrization_theorem(is_reductive=True, is_local_p_adic=True)
        self.assertTrue(res_valid["is_applicable"])
        self.assertIn("Proved", res_valid["geometrization_verdict"])

        # Non-reductive or global field
        res_invalid = self.loom.evaluate_geometrization_theorem(is_reductive=False, is_local_p_adic=True)
        self.assertFalse(res_invalid["is_applicable"])
        self.assertIn("Non-Applicable", res_invalid["geometrization_verdict"])

    def test_supercuspidal_and_gsp4_archetypes(self):
        """Test GL_2 supercuspidal and GSp_4 Siegel local archetypes."""
        sc_loom = FarguesScholzeLoom(
            default_archetype=FarguesScholzeArchetype.GL2_SUPER_CUSPIDAL.value,
        )
        self.assertEqual(sc_loom.group_label, "GL_2")
        self.assertEqual(sc_loom.local_shtukas[0].legs_count, 2)
        self.assertIn("Supercuspidal", sc_loom.excursion_operators[0].test_representation)

        gsp_loom = FarguesScholzeLoom(
            default_archetype=FarguesScholzeArchetype.GSP4_SIEGEL_LOCAL.value,
        )
        self.assertEqual(gsp_loom.group_label, "GSp_4")
        self.assertEqual(gsp_loom.local_shtukas[0].legs_count, 3)
        self.assertEqual(gsp_loom.excursion_operators[0].monodromy_operator_order, 1)

    def test_svg_generation_and_zero_em_dashes(self):
        """Verify dark titanium SVG generation and zero em dash compliance."""
        svg = self.loom.generate_fargues_scholze_svg()
        self.assertIn("<svg", svg)
        self.assertIn("Fargues-Scholze Geometrization", svg)
        self.assertIn("Bun_G", svg)

        # Check this file and loom file for zero em dashes
        cur_file = __file__
        loom_file = os.path.join(os.path.dirname(__file__), "fargues_scholze_loom.py")
        for fpath in [cur_file, loom_file]:
            if os.path.exists(fpath):
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()
                self.assertNotIn("\u2014", content, f"Em dash found in {fpath}")


if __name__ == "__main__":
    unittest.main()
