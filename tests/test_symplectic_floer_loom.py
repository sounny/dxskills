"""
Unit tests for the Symplectic Floer Homology & Fukaya A-Infinity Category Loom.
Tests Lagrangian intersections, pseudo-holomorphic Whitney disks, Stasheff associahedra,
and zero em dash compliance.
"""

import unittest
from scripts.symplectic_floer_loom import (
    SymplecticFloerLoom,
    LagrangianType,
    AInfinityOperationDegree,
    SymplecticFloerResult,
    LagrangianSubmanifoldData,
    IntersectionPointData,
    PseudoHolomorphicDisk,
    AInfinityOperationData,
)


class TestSymplecticFloerLoom(unittest.TestCase):
    """Test cases for SymplecticFloerLoom."""

    def setUp(self):
        self.loom = SymplecticFloerLoom.create_default_cotangent_loom()

    def test_default_loom_initialization(self):
        """Verify default loom initializes with exact Lagrangians in cotangent bundle."""
        self.assertEqual(self.loom.lagrangian_type, LagrangianType.EXACT_LAGRANGIAN.value)
        self.assertIn("Cotangent", self.loom.ambient_manifold)

    def test_evaluation_lagrangians_and_intersections(self):
        """Verify Lagrangian submanifolds and intersection generators are properly constructed."""
        res = self.loom.evaluate_symplectic_floer()
        self.assertIsInstance(res, SymplecticFloerResult)
        self.assertTrue(res.d_squared_zero_verified)
        self.assertTrue(res.a_infinity_relations_verified)
        self.assertEqual(len(res.lagrangians), 3)
        self.assertEqual(len(res.intersections), 4)
        self.assertEqual(len(res.whitney_disks), 3)
        self.assertEqual(len(res.a_infinity_ops), 4)

    def test_whitney_disks_properties(self):
        """Verify pseudo-holomorphic Whitney disks have positive energy and connect valid intersections."""
        res = self.loom.evaluate_symplectic_floer()
        point_ids = {p.point_id for p in res.intersections}
        for disk in res.whitney_disks:
            self.assertIn(disk.source_point_id, point_ids)
            self.assertIn(disk.target_point_id, point_ids)
            self.assertGreater(disk.symplectic_energy, 0.0)
            self.assertEqual(disk.maslov_index_diff, 1)

    def test_a_infinity_higher_operations(self):
        """Verify higher A-infinity operations m_1 through m_4 satisfy Stasheff relations."""
        res = self.loom.evaluate_symplectic_floer()
        op_names = [op.operation_name for op in res.a_infinity_ops]
        self.assertTrue(any("m_1" in name for name in op_names))
        self.assertTrue(any("m_2" in name for name in op_names))
        self.assertTrue(any("m_3" in name for name in op_names))
        self.assertTrue(any("m_4" in name for name in op_names))

        for op in res.a_infinity_ops:
            self.assertTrue(op.relation_verified)
            self.assertGreater(len(op.boundary_associahedron), 0)

    def test_floer_cohomology_ranks(self):
        """Verify Floer cohomology groups match the expected graded ranks."""
        res = self.loom.evaluate_symplectic_floer()
        self.assertEqual(res.floer_cohomology_ranks.get(0), 1)
        self.assertEqual(res.floer_cohomology_ranks.get(1), 0)
        self.assertEqual(res.floer_cohomology_ranks.get(2), 1)

    def test_svg_html_and_report_generation(self):
        """Verify SVG, HTML viewer, and markdown report render correctly without em dashes."""
        res = self.loom.evaluate_symplectic_floer()

        # SVG check
        svg = self.loom.render_svg(res)
        self.assertIn("<svg", svg)
        self.assertIn("Symplectic Floer Homology", svg)
        self.assertNotIn(chr(8212), svg)

        # HTML check
        html = self.loom.generate_html_viewer(res)
        self.assertIn("<!DOCTYPE html>", html)
        self.assertIn("Fukaya A-Infinity Loom", html)
        self.assertNotIn(chr(8212), html)

        # Markdown report check
        report = self.loom.generate_markdown_report(res)
        self.assertIn("Symplectic Floer Homology Telemetry", report)
        self.assertIn("Fukaya A-Infinity Operations", report)
        self.assertNotIn(chr(8212), report)


if __name__ == "__main__":
    unittest.main()
