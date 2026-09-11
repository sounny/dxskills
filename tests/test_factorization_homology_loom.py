"""
Unit tests for the Factorization Homology & Topological Chiral Homology Loom.
Tests little n-disks E_n-algebras, disk configuration embeddings, chiral bar complexes,
and zero em dash compliance.
"""

import unittest
from scripts.factorization_homology_loom import (
    FactorizationHomologyLoom,
    EnAlgebraType,
    ManifoldType,
    FactorizationHomologyResult,
    DiskEmbedding,
    ChiralBarSimplex,
)


class TestFactorizationHomologyLoom(unittest.TestCase):
    """Test cases for FactorizationHomologyLoom."""

    def setUp(self):
        self.loom = FactorizationHomologyLoom.create_default_torus_loom()

    def test_default_loom_initialization(self):
        """Verify default loom initializes with Torus T^2 and E_2 braided algebra."""
        self.assertEqual(self.loom.manifold_dim, 2)
        self.assertEqual(self.loom.manifold_type, ManifoldType.TORUS_T2.value)
        self.assertEqual(self.loom.algebra_type, EnAlgebraType.E2_BRAIDED.value)

    def test_evaluation_disks_and_bar_complex(self):
        """Verify disk embeddings and chiral bar complex compute non-zero total chiral dimension."""
        res = self.loom.evaluate_factorization_homology()
        self.assertIsInstance(res, FactorizationHomologyResult)
        self.assertTrue(res.excision_verified)
        self.assertTrue(res.non_abelian_poincare_verified)
        self.assertEqual(len(res.disks), 4)
        self.assertEqual(len(res.bar_stages), 4)
        self.assertGreater(res.total_chiral_dimension, 0)
        self.assertEqual(res.total_chiral_dimension, sum(b.homology_rank for b in res.bar_stages))

    def test_algebra_types_evaluation(self):
        """Verify evaluation across all four operadic little n-disks algebra types."""
        alg_types = [
            EnAlgebraType.E1_ASSOCIATIVE,
            EnAlgebraType.E2_BRAIDED,
            EnAlgebraType.EN_HIGHER,
            EnAlgebraType.E_INF_COMMUTATIVE,
        ]
        for at in alg_types:
            loom = FactorizationHomologyLoom(
                schema_name="Test Schema",
                manifold_name="Test Manifold",
                manifold_dim=3,
                manifold_type=ManifoldType.SPHERE_S2.value,
                algebra_type=at.value,
            )
            res = loom.evaluate_factorization_homology()
            self.assertEqual(res.algebra.algebra_type, at.value)
            self.assertTrue(res.non_abelian_poincare_verified)
            self.assertIn("Map_c", res.poincare_dual_mapping_space)

    def test_disk_embedding_properties(self):
        """Verify disk embeddings have positive geometric coordinates and non-empty state labels."""
        res = self.loom.evaluate_factorization_homology()
        for d in res.disks:
            self.assertGreater(d.radius, 0.0)
            self.assertGreater(d.center_x, 0.0)
            self.assertGreater(d.center_y, 0.0)
            self.assertGreater(d.tensor_rank, 0)
            self.assertTrue(len(d.local_state_label) > 0)

    def test_svg_html_and_report_generation(self):
        """Verify SVG, HTML viewer, and markdown report render correctly without em dashes."""
        res = self.loom.evaluate_factorization_homology()

        # SVG check
        svg = self.loom.render_svg(res)
        self.assertIn("<svg", svg)
        self.assertIn("Factorization Homology", svg)
        self.assertNotIn(chr(8212), svg)

        # HTML check
        html = self.loom.generate_html_viewer(res)
        self.assertIn("<!DOCTYPE html>", html)
        self.assertIn("Factorization Homology", html)
        self.assertNotIn(chr(8212), html)

        # Markdown report check
        report = self.loom.generate_markdown_report(res)
        self.assertIn("Factorization Homology Telemetry", report)
        self.assertIn("Chiral Bar Complex Stages", report)
        self.assertNotIn(chr(8212), report)


if __name__ == "__main__":
    unittest.main()
