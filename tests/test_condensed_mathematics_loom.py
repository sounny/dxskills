"""
Unit tests for Condensed Mathematics & Clausen-Scholze Analytic Loom.
Verifies profinite test sets, Stone duality probes, solid abelian groups,
liquid vector spaces, and abelian exactness.
Strictly zero em dashes allowed.
"""

import unittest
import os
import sys

# Ensure repository root is in path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.condensed_mathematics_loom import (
    CondensedMathematicsLoom,
    CondensedAnalyticResult,
    CondensedSetType,
    ProfiniteTestSet,
    SolidCompletionModule,
    HyperCoverLevel,
)


class TestCondensedMathematicsLoom(unittest.TestCase):
    """Test suite for Condensed Mathematics & Clausen-Scholze Analytic Loom."""

    def setUp(self):
        self.loom = CondensedMathematicsLoom.create_default_liquid_loom()

    def test_default_evaluation(self):
        """Test default evaluation produces valid condensed analytic result."""
        result = self.loom.evaluate_condensed_schema()
        self.assertEqual(len(result.profinite_test_sets), 3)
        self.assertEqual(len(result.hyper_cover), 3)
        self.assertTrue(result.abelian_exactness_verified)
        self.assertTrue(result.liquid_convergence_verified)
        self.assertEqual(result.condensed_type, CondensedSetType.LIQUID_REAL.value)

    def test_profinite_test_sets(self):
        """Test characteristics of profinite Stone test spaces."""
        result = self.loom.evaluate_condensed_schema()
        s0 = result.profinite_test_sets[0]
        self.assertIn("Extremally Disconnected", s0.set_id)
        self.assertEqual(s0.clopen_subsets_count, 16)

        s_cantor = result.profinite_test_sets[1]
        self.assertIn("Cantor", s_cantor.set_id)
        self.assertEqual(s_cantor.strata_levels, 8)

        s_padic = result.profinite_test_sets[2]
        self.assertIn("p-adic", s_padic.set_id)
        self.assertEqual(s_padic.clopen_subsets_count, 32)

    def test_solid_and_liquid_module(self):
        """Test solid and liquid vector space completion properties."""
        result = self.loom.evaluate_condensed_schema()
        mod = result.solid_module
        self.assertTrue(mod.is_solid_complete)
        self.assertIn("R_liq", mod.base_ring)
        self.assertEqual(mod.liquid_parameter_p, 1.0)
        self.assertEqual(mod.solid_tensor_rank, 3)

    def test_derived_ext_dimensions(self):
        """Test vanishing of obstruction Ext^1 groups ensuring exact abelian category."""
        result = self.loom.evaluate_condensed_schema()
        exts = result.derived_ext_dimensions
        self.assertEqual(exts.get(0), 1)
        self.assertEqual(exts.get(1), 0)
        self.assertEqual(exts.get(2), 0)
        self.assertTrue(result.abelian_exactness_verified)

    def test_rendering_outputs_and_zero_em_dashes(self):
        """Test SVG, Markdown report, HTML viewer, and strict zero em dash compliance."""
        result = self.loom.evaluate_condensed_schema()
        svg = self.loom.render_svg(result)
        report = self.loom.generate_markdown_report(result)
        html_view = self.loom.generate_html_viewer(result)
        telemetry = result.to_dict()

        self.assertIn("<svg", svg)
        self.assertIn("Profinite Stone Space Probes", svg)
        self.assertIn("# Cognitive Intuitive Continuum X", report)
        self.assertIn("<!DOCTYPE html>", html_view)
        self.assertIn("profinite_test_sets", telemetry)

        # Strict Zero Em Dash Enforcement
        self.assertNotIn(chr(8212), svg)
        self.assertNotIn(chr(8212), report)
        self.assertNotIn(chr(8212), html_view)
        self.assertNotIn(chr(8212), result.cognitive_interpretation)


if __name__ == "__main__":
    unittest.main()
