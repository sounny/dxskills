"""
Unit tests for the Higher Category Theory & Lurie (infinity, 1)-Topos Loom.
Tests Joyal quasi-categories, inner horn fillers, Lurie-Giraud axioms,
and zero em dash compliance.
"""

import unittest
from scripts.higher_topos_loom import (
    HigherToposLoom,
    HornType,
    DescentAxiomType,
    HigherToposResult,
    SimplicialNerveNode,
    HornFillingCondition,
    DescentConditionData,
)


class TestHigherToposLoom(unittest.TestCase):
    """Test cases for HigherToposLoom."""

    def setUp(self):
        self.loom = HigherToposLoom.create_default_smooth_topos_loom()

    def test_default_loom_initialization(self):
        """Verify default loom initializes with smooth manifolds higher topos."""
        self.assertEqual(self.loom.schema_name, "Cognitive Higher Universe X")
        self.assertIn("Smooth Manifolds", self.loom.topos_name)
        self.assertEqual(self.loom.max_simplex_dim, 3)

    def test_evaluation_quasi_category_and_descent(self):
        """Verify quasi-category condition holds and Lurie-Giraud descent axioms are satisfied."""
        res = self.loom.evaluate_higher_topos()
        self.assertIsInstance(res, HigherToposResult)
        self.assertTrue(res.is_quasi_category)
        self.assertTrue(res.is_hypercomplete_topos)
        self.assertGreater(res.total_simplices_count, 0)
        self.assertEqual(len(res.simplicial_nodes), 6)
        self.assertEqual(len(res.horn_fillings), 4)
        self.assertEqual(len(res.descent_conditions), 4)

    def test_horn_fillings_structure(self):
        """Verify inner horns admit fillers and outer horns are properly classified."""
        res = self.loom.evaluate_higher_topos()
        inner_horns = [h for h in res.horn_fillings if h.is_inner_horn]
        self.assertGreaterEqual(len(inner_horns), 2)
        for h in inner_horns:
            self.assertTrue(h.has_filler)
            self.assertIn("Lambda^", h.horn_id)
            self.assertGreater(len(h.boundary_faces), 0)

    def test_lurie_giraud_axioms(self):
        """Verify all four fundamental higher topos descent conditions are present and satisfied."""
        res = self.loom.evaluate_higher_topos()
        axiom_names = [d.axiom_type for d in res.descent_conditions]
        self.assertTrue(any("Universal Colimits" in a for a in axiom_names))
        self.assertTrue(any("Disjoint Coproducts" in a for a in axiom_names))
        self.assertTrue(any("Effective Groupoid" in a for a in axiom_names))
        self.assertTrue(any("Hypercompleteness" in a for a in axiom_names))

        for d in res.descent_conditions:
            self.assertTrue(d.is_satisfied)
            self.assertGreater(len(d.formal_property), 0)

    def test_svg_html_and_report_generation(self):
        """Verify SVG, HTML viewer, and markdown report render correctly without em dashes."""
        res = self.loom.evaluate_higher_topos()

        # SVG check
        svg = self.loom.render_svg(res)
        self.assertIn("<svg", svg)
        self.assertIn("Higher Category Theory", svg)
        self.assertNotIn(chr(8212), svg)

        # HTML check
        html = self.loom.generate_html_viewer(res)
        self.assertIn("<!DOCTYPE html>", html)
        self.assertIn("Higher Topos Loom", html)
        self.assertNotIn(chr(8212), html)

        # Markdown report check
        report = self.loom.generate_markdown_report(res)
        self.assertIn("Higher Topos Telemetry", report)
        self.assertIn("Simplicial Horn Fillings", report)
        self.assertNotIn(chr(8212), report)


if __name__ == "__main__":
    unittest.main()
