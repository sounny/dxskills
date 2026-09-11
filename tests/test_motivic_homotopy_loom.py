"""
Unit tests for Motivic Homotopy & Voevodsky Slice Filtration Loom.
Verifies bi-graded motivic spheres, A^1-homotopy invariance,
Nisnevich descent, and the Voevodsky slice theorem for algebraic K-theory.
Strictly zero em dashes allowed.
"""

import unittest
import os
import sys

# Ensure repository root is in path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.motivic_homotopy_loom import (
    MotivicHomotopyLoom,
    MotivicHomotopyResult,
    MotivicSphere,
    SliceStage,
    A1HomotopyLocus,
    MotivicSpectralSequence,
)


class TestMotivicHomotopyLoom(unittest.TestCase):
    """Test suite for Motivic Homotopy & Voevodsky Slice Filtration Loom."""

    def setUp(self):
        self.loom = MotivicHomotopyLoom.create_default_kgl_loom()

    def test_default_evaluation(self):
        """Test default evaluation produces valid motivic homotopy result."""
        result = self.loom.evaluate_motivic_homotopy()
        self.assertEqual(len(result.spheres), 4)
        self.assertEqual(len(result.slice_tower), 4)
        self.assertTrue(result.slice_theorem_verified)
        self.assertTrue(result.locus.has_nisnevich_descent)
        self.assertTrue(result.locus.has_a1_invariance)

    def test_motivic_spheres_simplicial_dim(self):
        """Test calculation of simplicial dimensions p - q for bi-graded spheres."""
        result = self.loom.evaluate_motivic_homotopy()
        # S^(1,0) -> simplicial dim 1
        s10 = result.spheres[0]
        self.assertEqual(s10.label, "S^(1,0)")
        self.assertEqual(s10.simplicial_dim, 1)

        # S^(1,1) -> simplicial dim 0 (algebraic G_m)
        s11 = result.spheres[1]
        self.assertEqual(s11.label, "S^(1,1)")
        self.assertEqual(s11.simplicial_dim, 0)

        # S^(2,1) -> simplicial dim 1 (projective line P^1)
        s21 = result.spheres[2]
        self.assertEqual(s21.label, "S^(2,1)")
        self.assertEqual(s21.simplicial_dim, 1)
        self.assertEqual(s21.euler_characteristic, 2)

    def test_voevodsky_slice_tower(self):
        """Test that slice cofibers s_n(KGL) match Sigma^(2n, n) HZ."""
        result = self.loom.evaluate_motivic_homotopy()
        for st in result.slice_tower:
            n = st.level_n
            self.assertEqual(st.shift_simplicial, 2 * n)
            self.assertEqual(st.shift_weight, n)
            self.assertIn(f"Sigma^({2*n},{n}) HZ", st.associated_slice)

    def test_a1_invariance_and_nisnevich_descent(self):
        """Test A^1-contractibility and spectral sequence convergence."""
        result = self.loom.evaluate_motivic_homotopy()
        self.assertTrue(result.locus.has_a1_invariance)
        self.assertTrue(result.locus.has_nisnevich_descent)
        self.assertTrue(result.locus.transfers_enabled)
        self.assertTrue(result.spectral_sequence.convergence_verified)
        self.assertEqual(result.spectral_sequence.differentials_count, 0)

    def test_rendering_outputs_and_zero_em_dashes(self):
        """Test SVG, Markdown report, HTML viewer, and verify zero em dashes."""
        result = self.loom.evaluate_motivic_homotopy()
        svg = self.loom.render_svg(result)
        report = self.loom.generate_markdown_report(result)
        html_view = self.loom.generate_html_viewer(result)
        telemetry = result.to_dict()

        self.assertIn("<svg", svg)
        self.assertIn("Bi-Graded Motivic Spheres", svg)
        self.assertIn("# Cognitive Perspective Scheme X", report)
        self.assertIn("<!DOCTYPE html>", html_view)
        self.assertIn("spheres", telemetry)

        # Strict Zero Em Dash Enforcement
        self.assertNotIn(chr(8212), svg)
        self.assertNotIn(chr(8212), report)
        self.assertNotIn(chr(8212), html_view)
        self.assertNotIn(chr(8212), result.cognitive_interpretation)


if __name__ == "__main__":
    unittest.main()
