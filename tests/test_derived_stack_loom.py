"""
Unit tests for Derived Algebraic Geometry & Higher Stacks Loom.
Verifies simplicial nerve presentations, cotangent complexes,
deformation theories, and virtual fundamental classes.
Strictly zero em dashes allowed.
"""

import unittest
import os
import sys

# Ensure repository root is in path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.derived_stack_loom import (
    DerivedStackLoom,
    DerivedStackResult,
    StackCategory,
    CognitiveStackLocus,
    CotangentComplex,
    DeformationProfile,
    VirtualFundamentalClass,
)


class TestDerivedStackLoom(unittest.TestCase):
    """Test suite for Derived Algebraic Geometry & Higher Stacks Loom."""

    def setUp(self):
        self.loom = DerivedStackLoom.create_default_cognitive_moduli_stack()

    def test_default_stack_evaluation(self):
        """Test default stack evaluation produces valid Artin stack."""
        result = self.loom.evaluate_derived_stack(
            base_dim=4,
            automorphism_dim=1,
            num_relations=2,
            higher_syzygies=0,
            automorphism_group="GL(1, C)",
        )
        self.assertEqual(result.stack_category, StackCategory.ARTIN.value)
        self.assertEqual(len(result.simplicial_nerve), 3)
        self.assertEqual(result.simplicial_nerve[0].dimension, 4)
        self.assertEqual(result.simplicial_nerve[1].dimension, 5)
        self.assertEqual(result.simplicial_nerve[2].dimension, 6)

        # Cotangent complex
        self.assertEqual(result.cotangent_complex.h0_differentials_dim, 4)
        self.assertEqual(result.cotangent_complex.h_minus1_relations_dim, 2)
        self.assertEqual(result.cotangent_complex.h_minus2_syzygies_dim, 0)
        self.assertTrue(result.cotangent_complex.is_quasi_smooth)
        self.assertEqual(result.cotangent_complex.total_euler_characteristic, 2)

    def test_deligne_mumford_classification(self):
        """Test stack with discrete automorphism group is classified as Deligne-Mumford."""
        dm_loom = DerivedStackLoom(stack_name="Orbifold Stack X // G")
        result = dm_loom.evaluate_derived_stack(
            base_dim=3,
            automorphism_dim=0,
            num_relations=0,
            higher_syzygies=0,
            automorphism_group="Z/2Z",
        )
        self.assertEqual(result.stack_category, StackCategory.DELIGNE_MUMFORD.value)
        self.assertEqual(result.deformation_profile.t0_automorphisms_dim, 0)
        self.assertTrue(result.virtual_class.is_unobstructed)
        self.assertEqual(result.virtual_class.virtual_dimension, 3)

    def test_higher_stack_classification(self):
        """Test stack with higher syzygies is classified as Higher Geometric Stack."""
        higher_loom = DerivedStackLoom(stack_name="2-Stack of 2-Groupoids")
        result = higher_loom.evaluate_derived_stack(
            base_dim=5,
            automorphism_dim=2,
            num_relations=3,
            higher_syzygies=1,
            automorphism_group="B(U(1))",
        )
        self.assertEqual(result.stack_category, StackCategory.HIGHER_STACK.value)
        self.assertFalse(result.cotangent_complex.is_quasi_smooth)
        self.assertEqual(result.cotangent_complex.amplitude_min, -2)
        self.assertEqual(result.cotangent_complex.amplitude_max, 0)

    def test_virtual_fundamental_class(self):
        """Test calculation of virtual dimension and excess dimension."""
        result = self.loom.evaluate_derived_stack(
            base_dim=6,
            automorphism_dim=2,
            num_relations=3,
            higher_syzygies=0,
        )
        # vdim = t1 - t2 - t0 = 6 - 3 - 2 = 1
        self.assertEqual(result.virtual_class.virtual_dimension, 1)
        # actual_dim = 6 - 2 = 4
        self.assertEqual(result.virtual_class.actual_dimension, 4)
        # excess_dim = 4 - 1 = 3
        self.assertEqual(result.virtual_class.excess_dimension, 3)
        self.assertAlmostEqual(result.virtual_class.virtual_cycle_degree, 1.0 / 4.0)

    def test_rendering_outputs_and_zero_em_dashes(self):
        """Test SVG, Markdown report, HTML viewer, and verify zero em dashes."""
        result = self.loom.evaluate_derived_stack()
        svg = self.loom.render_svg(result)
        report = self.loom.generate_markdown_report(result)
        html_view = self.loom.generate_html_viewer(result)
        telemetry = result.to_dict()

        self.assertIn("<svg", svg)
        self.assertIn("Simplicial Nerve", svg)
        self.assertIn("# Cognitive Perspective Moduli Stack M_persp", report)
        self.assertIn("<!DOCTYPE html>", html_view)
        self.assertIn("stack_category", telemetry)

        # Strict Zero Em Dash Enforcement
        self.assertNotIn(chr(8212), svg)
        self.assertNotIn(chr(8212), report)
        self.assertNotIn(chr(8212), html_view)
        self.assertNotIn(chr(8212), result.cognitive_interpretation)


if __name__ == "__main__":
    unittest.main()
