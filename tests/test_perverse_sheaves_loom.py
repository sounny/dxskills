"""
Unit tests for Perverse Sheaves & Intersection Cohomology Loom.
Verifies stratified spaces, perversity profiles, intersection cohomology Betti numbers,
Poincare-Verdier duality, and BBDG direct sum decomposition.
Strictly zero em dashes allowed.
"""

import unittest
import os
import sys

# Ensure repository root is in path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.perverse_sheaves_loom import (
    PerverseSheavesLoom,
    PerverseSheafResult,
    PerversityType,
    Stratum,
    PerversityProfile,
    IntersectionCohomologyGroup,
    BBDGDecompositionSummand,
)


class TestPerverseSheavesLoom(unittest.TestCase):
    """Test suite for Perverse Sheaves & Intersection Cohomology Loom."""

    def setUp(self):
        self.loom = PerverseSheavesLoom.create_default_stratified_loom()

    def test_default_stratified_evaluation(self):
        """Test default evaluation produces valid stratified result with 3 strata."""
        result = self.loom.evaluate_intersection_cohomology()
        self.assertEqual(len(result.strata), 3)
        self.assertEqual(result.ambient_dimension, 4)
        self.assertTrue(result.poincare_verdier_verified)
        self.assertTrue(result.bbdg_decomposition_verified)

    def test_perversity_values(self):
        """Test calculation of lower-middle, upper-middle, zero, and top perversities."""
        # Lower middle: p(c) = (c-2)//2
        # For c=2: 0, c=3: 0, c=4: 1
        p_lower = self.loom.compute_perversity(PerversityType.LOWER_MIDDLE.value)
        self.assertEqual(p_lower.values[2], 0)
        self.assertEqual(p_lower.values[3], 0)
        self.assertEqual(p_lower.values[4], 1)

        # Top perversity: p(c) = c - 2
        p_top = self.loom.compute_perversity(PerversityType.TOP.value)
        self.assertEqual(p_top.values[2], 0)
        self.assertEqual(p_top.values[3], 1)
        self.assertEqual(p_top.values[4], 2)

        # Zero perversity: p(c) = 0
        p_zero = self.loom.compute_perversity(PerversityType.ZERO.value)
        self.assertEqual(p_zero.values[2], 0)
        self.assertEqual(p_zero.values[3], 0)
        self.assertEqual(p_zero.values[4], 0)

    def test_poincare_verdier_self_duality(self):
        """Test Poincare-Verdier symmetry of intersection cohomology Betti numbers."""
        result = self.loom.evaluate_intersection_cohomology(PerversityType.LOWER_MIDDLE.value)
        betti = [ih.dimension_betti for ih in result.intersection_cohomology]
        # Betti: [1, 0, 2, 0, 1]
        self.assertEqual(betti[0], betti[4])
        self.assertEqual(betti[1], betti[3])
        self.assertEqual(betti[2], 2)
        self.assertTrue(result.poincare_verdier_verified)

    def test_bbdg_decomposition_summands(self):
        """Test BBDG decomposition contains expected simple perverse sheaves."""
        result = self.loom.evaluate_intersection_cohomology()
        self.assertEqual(len(result.bbdg_summands), 3)

        reg_summand = result.bbdg_summands[0]
        self.assertEqual(reg_summand.stratum, "S_reg")
        self.assertEqual(reg_summand.shift_degree, 0)

        cusp_summand = result.bbdg_summands[1]
        self.assertEqual(cusp_summand.stratum, "S_cusp")
        self.assertEqual(cusp_summand.shift_degree, 2)

    def test_rendering_outputs_and_zero_em_dashes(self):
        """Test SVG, Markdown report, HTML viewer, and strict zero em dash compliance."""
        result = self.loom.evaluate_intersection_cohomology()
        svg = self.loom.render_svg(result)
        report = self.loom.generate_markdown_report(result)
        html_view = self.loom.generate_html_viewer(result)
        telemetry = result.to_dict()

        self.assertIn("<svg", svg)
        self.assertIn("Stratification Strata Filtration", svg)
        self.assertIn("# Cognitive Multi-Modal Locus X", report)
        self.assertIn("<!DOCTYPE html>", html_view)
        self.assertIn("strata", telemetry)

        # Strict Zero Em Dash Enforcement
        self.assertNotIn(chr(8212), svg)
        self.assertNotIn(chr(8212), report)
        self.assertNotIn(chr(8212), html_view)
        self.assertNotIn(chr(8212), result.cognitive_interpretation)


if __name__ == "__main__":
    unittest.main()
