"""
Unit tests for the Prismatic Cohomology and Bhatt-Scholze Prism Loom.
Tests universal p-adic integral cohomology specializations, Nygaard filtration,
and zero em dash compliance.
"""

import json
import unittest
from scripts.prismatic_cohomology_loom import (
    PrismaticCohomologyLoom,
    PrismType,
    PrismData,
    PrismaticCohomologyResult,
    PrismaticSpecialization,
    NygaardFiltrationStage,
)


class TestPrismaticCohomologyLoom(unittest.TestCase):
    """Test cases for PrismaticCohomologyLoom."""

    def setUp(self):
        self.loom = PrismaticCohomologyLoom()

    def test_default_loom_initialization(self):
        """Verify default loom initializes with Breuil-Kisin prism configuration."""
        self.assertEqual(self.loom.prime_p, 5)
        self.assertEqual(self.loom.prism_type, PrismType.BREUIL_KISIN)
        bk_loom = PrismaticCohomologyLoom.create_default_breuil_kisin_loom()
        self.assertEqual(bk_loom.prism_type, PrismType.BREUIL_KISIN)

    def test_evaluation_specializations(self):
        """Verify four universal specializations preserve total cohomology ranks."""
        res = self.loom.evaluate_prismatic_cohomology()
        self.assertIsInstance(res, PrismaticCohomologyResult)
        self.assertTrue(res.all_specializations_harmonized)
        self.assertEqual(len(res.specializations), 4)

        modalities = [s.modality for s in res.specializations]
        self.assertTrue(any("de Rham" in m for m in modalities))
        self.assertTrue(any("Hodge-Tate" in m for m in modalities))
        self.assertTrue(any("Crystalline" in m for m in modalities))
        self.assertTrue(any("Etale" in m for m in modalities))

        # Check total rank matching
        total_betti = sum(res.prismatic_betti_ranks)
        for spec in res.specializations:
            self.assertEqual(spec.specialized_cohomology_rank, total_betti)
            self.assertTrue(spec.invariants_verified)

    def test_nygaard_filtration_stages(self):
        """Verify Nygaard filtration stages satisfy monotonicity and divided Frobenius actions."""
        res = self.loom.evaluate_prismatic_cohomology()
        self.assertGreaterEqual(len(res.nygaard_stages), 3)

        for i, stage in enumerate(res.nygaard_stages):
            self.assertEqual(stage.filtration_degree_i, i)
            self.assertIn("N^>=", stage.nygaard_module_label)
            self.assertGreater(stage.divided_frobenius_rank, 0)
            self.assertGreater(stage.cohomology_dimension, 0)

    def test_prism_types_evaluation(self):
        """Verify evaluation succeeds across all four standard prism types."""
        prism_types = [
            PrismType.CRYSTALLINE,
            PrismType.BREUIL_KISIN,
            PrismType.Q_CRYSTALLINE,
            PrismType.PERFECTOID,
        ]
        for pt in prism_types:
            loom = PrismaticCohomologyLoom(prism_type=pt, prime_p=7)
            res = loom.evaluate_prismatic_cohomology()
            self.assertEqual(res.prism.prism_type, pt.value)
            self.assertTrue(res.all_specializations_harmonized)

    def test_svg_html_and_report_generation(self):
        """Verify SVG, HTML viewer, and markdown report render correctly without em dashes."""
        res = self.loom.evaluate_prismatic_cohomology()

        # SVG check
        svg = self.loom.render_svg(res)
        self.assertIn("<svg", svg)
        self.assertIn("Prismatic Cohomology", svg)
        self.assertNotIn(chr(8212), svg)

        # HTML check
        html = self.loom.generate_html_viewer(res)
        self.assertIn("<!DOCTYPE html>", html)
        self.assertIn("Prismatic Cohomology", html)
        self.assertNotIn(chr(8212), html)

        # Markdown report check
        report = self.loom.generate_markdown_report(res)
        self.assertIn("Prismatic Cohomology", report)
        self.assertIn("Nygaard Filtration", report)
        self.assertNotIn(chr(8212), report)


if __name__ == "__main__":
    unittest.main()
