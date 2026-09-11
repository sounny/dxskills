"""
Unit tests for the Topological Quantum Field Theory & Atiyah-Segal Axiomatic Loom.
Tests symmetric monoidal cobordism categories, 2D commutative Frobenius algebras,
Atiyah-Segal axioms, and zero em dash compliance.
"""

import unittest
from scripts.tqft_axiomatic_loom import (
    TQFTAxiomaticLoom,
    TQFTDimension,
    CobordismType,
    TQFTResult,
    BoundaryStateSpace,
    CobordismComponent,
    FrobeniusAlgebraData,
)


class TestTQFTAxiomaticLoom(unittest.TestCase):
    """Test cases for TQFTAxiomaticLoom."""

    def setUp(self):
        self.loom = TQFTAxiomaticLoom.create_default_2d_frobenius_loom()

    def test_default_loom_initialization(self):
        """Verify default loom initializes with 2D TQFT and CP^2 cohomology Frobenius algebra."""
        self.assertEqual(self.loom.spacetime_dim, TQFTDimension.DIM_2D.value)
        self.assertEqual(self.loom.algebra_dim, 3)
        self.assertEqual(self.loom.algebra_name, "Cohomology Ring H^*(CP^2; C)")

    def test_evaluation_axioms_and_state_spaces(self):
        """Verify Atiyah-Segal axioms hold and boundary state spaces are generated."""
        res = self.loom.evaluate_tqft()
        self.assertIsInstance(res, TQFTResult)
        self.assertTrue(res.gluing_axiom_verified)
        self.assertTrue(res.monoidal_axiom_verified)
        self.assertTrue(res.cylinder_axiom_verified)
        self.assertGreater(res.closed_spacetime_invariant, 0.0)
        self.assertEqual(len(res.state_spaces), 4)
        self.assertEqual(len(res.cobordisms), 5)

    def test_frobenius_algebra_structure(self):
        """Verify Frobenius algebra satisfies non-degeneracy and dimension consistency."""
        res = self.loom.evaluate_tqft()
        frob = res.frobenius_algebra
        self.assertIsInstance(frob, FrobeniusAlgebraData)
        self.assertEqual(frob.dimension, 3)
        self.assertTrue(frob.frobenius_pairing_non_degenerate)
        self.assertIn("H^0", frob.unit_element)
        self.assertIn("CP^2", frob.counit_trace)

    def test_cobordism_operators(self):
        """Verify elementary cobordisms include cylinder, pair of pants, and caps."""
        res = self.loom.evaluate_tqft()
        cob_types = [c.cobordism_type for c in res.cobordisms]
        self.assertTrue(any("Cylinder" in t for t in cob_types))
        self.assertTrue(any("Merge" in t for t in cob_types))
        self.assertTrue(any("Split" in t for t in cob_types))
        self.assertTrue(any("Cap In" in t for t in cob_types))
        self.assertTrue(any("Cap Out" in t for t in cob_types))

        for cob in res.cobordisms:
            self.assertGreater(cob.operator_rank, 0)
            self.assertGreater(cob.operator_trace, 0.0)

    def test_svg_html_and_report_generation(self):
        """Verify SVG, HTML viewer, and markdown report render correctly without em dashes."""
        res = self.loom.evaluate_tqft()

        # SVG check
        svg = self.loom.render_svg(res)
        self.assertIn("<svg", svg)
        self.assertIn("Topological Quantum Field Theory", svg)
        self.assertNotIn(chr(8212), svg)

        # HTML check
        html = self.loom.generate_html_viewer(res)
        self.assertIn("<!DOCTYPE html>", html)
        self.assertIn("Atiyah-Segal TQFT", html)
        self.assertNotIn(chr(8212), html)

        # Markdown report check
        report = self.loom.generate_markdown_report(res)
        self.assertIn("Atiyah-Segal TQFT Telemetry", report)
        self.assertIn("Commutative Frobenius Algebra Structure", report)
        self.assertNotIn(chr(8212), report)


if __name__ == "__main__":
    unittest.main()
