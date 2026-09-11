"""
Unit tests for the Differential Cohomology & Cheeger-Simons Differential Characters Loom.
Tests differential characters, curvature forms, Cheeger-Simons exact hexagon,
and zero em dash compliance.
"""

import unittest
from scripts.differential_cohomology_loom import (
    DifferentialCohomologyLoom,
    DifferentialDegree,
    HexagonExactSequenceType,
    DifferentialCohomologyResult,
    CurvatureFormData,
    DifferentialCharacterData,
    HexagonExactSequenceData,
)


class TestDifferentialCohomologyLoom(unittest.TestCase):
    """Test cases for DifferentialCohomologyLoom."""

    def setUp(self):
        self.loom = DifferentialCohomologyLoom.create_default_u1_gauge_loom()

    def test_default_loom_initialization(self):
        """Verify default loom initializes with degree 2 U(1) gauge bundle."""
        self.assertEqual(self.loom.manifold_dim, 4)
        self.assertEqual(self.loom.degree, DifferentialDegree.DEGREE_2.value)
        self.assertEqual(self.loom.manifold_name, "Spacetime 4-Manifold M^4")

    def test_evaluation_curvature_and_characters(self):
        """Verify differential character and curvature form are properly constructed and verified."""
        res = self.loom.evaluate_differential_cohomology()
        self.assertIsInstance(res, DifferentialCohomologyResult)
        self.assertTrue(res.de_rham_compatibility_verified)
        self.assertTrue(res.cheeger_simons_exactness_verified)
        self.assertEqual(res.curvature.degree_k, 2)
        self.assertTrue(res.curvature.is_closed)
        self.assertTrue(res.curvature.is_integral_flux)
        self.assertGreater(len(res.character.integer_characteristic_class), 0)

    def test_degree_evaluations(self):
        """Verify evaluation succeeds across all four standard differential cohomology degrees."""
        degrees = [
            DifferentialDegree.DEGREE_1,
            DifferentialDegree.DEGREE_2,
            DifferentialDegree.DEGREE_3,
            DifferentialDegree.DEGREE_4,
        ]
        for deg in degrees:
            loom = DifferentialCohomologyLoom(
                schema_name="Test Manifold",
                manifold_name="Test Space",
                manifold_dim=4,
                degree=deg.value,
            )
            res = loom.evaluate_differential_cohomology()
            self.assertEqual(res.degree, deg.value)
            self.assertTrue(res.de_rham_compatibility_verified)
            self.assertTrue(res.cheeger_simons_exactness_verified)

    def test_cheeger_simons_hexagon_sequences(self):
        """Verify both interlocking exact sequences in the Cheeger-Simons hexagon are present and exact."""
        res = self.loom.evaluate_differential_cohomology()
        self.assertEqual(len(res.hexagon_sequences), 2)
        seq_types = [s.sequence_type for s in res.hexagon_sequences]
        self.assertIn(HexagonExactSequenceType.TOP_FLAT_CURVATURE.value, seq_types)
        self.assertIn(HexagonExactSequenceType.BOTTOM_FORMS_TOPOLOGY.value, seq_types)

        for s in res.hexagon_sequences:
            self.assertTrue(s.exactness_verified)
            self.assertGreater(len(s.subgroup_kernel), 0)
            self.assertGreater(len(s.quotient_image), 0)

    def test_svg_html_and_report_generation(self):
        """Verify SVG, HTML viewer, and markdown report render correctly without em dashes."""
        res = self.loom.evaluate_differential_cohomology()

        # SVG check
        svg = self.loom.render_svg(res)
        self.assertIn("<svg", svg)
        self.assertIn("Differential Cohomology", svg)
        self.assertNotIn(chr(8212), svg)

        # HTML check
        html = self.loom.generate_html_viewer(res)
        self.assertIn("<!DOCTYPE html>", html)
        self.assertIn("Differential Cohomology Loom", html)
        self.assertNotIn(chr(8212), html)

        # Markdown report check
        report = self.loom.generate_markdown_report(res)
        self.assertIn("Differential Cohomology Telemetry", report)
        self.assertIn("Cheeger-Simons Hexagon Interlocking Exact Sequences", report)
        self.assertNotIn(chr(8212), report)


if __name__ == "__main__":
    unittest.main()
