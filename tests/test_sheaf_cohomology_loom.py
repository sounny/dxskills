"""
Unit tests for Sheaf-Theoretic Cohomology & Epistemic Gluing Loom.
Verifies Cech complex construction, coboundary operators delta^0 and delta^1,
sheaf cohomology groups H^0 and H^1, linear algebra routines,
and zero em dash constraints.
"""

import unittest
import os
import math
from scripts.sheaf_cohomology_loom import (
    SheafCohomologyLoom,
    OpenSet,
    PairwiseOverlap,
    TripleOverlap,
    matrix_transpose,
    matrix_multiply,
    gaussian_elimination_rref,
    compute_rank,
    compute_kernel_basis,
)


class TestSheafCohomologyLoom(unittest.TestCase):
    """Test suite for SheafCohomologyLoom and pure Python linear algebra."""

    def test_linear_algebra_routines(self):
        """Tests matrix transpose, multiply, RREF, rank, and kernel."""
        # 1. Transpose
        mat = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]
        t = matrix_transpose(mat)
        self.assertEqual(len(t), 3)
        self.assertEqual(len(t[0]), 2)
        self.assertEqual(t[0][1], 4.0)

        # 2. Multiplication
        a = [[1.0, 2.0], [3.0, 4.0]]
        b = [[2.0, 0.0], [1.0, 2.0]]
        ab = matrix_multiply(a, b)
        self.assertEqual(ab[0][0], 4.0)
        self.assertEqual(ab[0][1], 4.0)
        self.assertEqual(ab[1][0], 10.0)
        self.assertEqual(ab[1][1], 8.0)

        # 3. RREF & Rank (Rank-Nullity theorem)
        mat_sing = [[1.0, 2.0, 3.0], [2.0, 4.0, 6.0], [0.0, 1.0, 1.0]]
        rank = compute_rank(mat_sing)
        self.assertEqual(rank, 2)

        kernel = compute_kernel_basis(mat_sing)
        self.assertEqual(len(kernel), 1)  # 3 cols - rank 2 = 1 dim nullspace

        # Verify kernel satisfies Ax = 0
        kv = kernel[0]
        for row in mat_sing:
            dot = sum(row[i] * kv[i] for i in range(3))
            self.assertAlmostEqual(dot, 0.0, places=5)

    def test_default_epistemic_cover(self):
        """Tests creation and properties of default 5-lens epistemic cover."""
        loom = SheafCohomologyLoom.create_default_epistemic_cover()
        self.assertEqual(len(loom.open_sets), 5)
        self.assertEqual(loom.section_dim, 2)

        overlaps, triples = loom.compute_intersections()
        self.assertGreater(len(overlaps), 0)
        # Default geometry overlaps produce pairwise connections
        for ov in overlaps:
            self.assertGreater(ov.overlap_area, 0.0)
            self.assertEqual(len(ov.discrepancy), 2)

    def test_cech_cohomology_computation(self):
        """Tests Cech complex dimensions, coboundaries, and cohomology invariants."""
        loom = SheafCohomologyLoom.create_default_epistemic_cover()
        res = loom.build_cech_complex()

        self.assertEqual(res.dim_c0, 5 * 2)  # 5 lenses * 2 dim
        self.assertEqual(res.dim_c1, len(res.overlaps) * 2)
        self.assertEqual(res.dim_c2, len(res.triples) * 2)

        self.assertGreaterEqual(res.betti_h0, 0)
        self.assertGreaterEqual(res.betti_h1, 0)
        self.assertGreater(res.consensus_index, 0.0)
        self.assertLessEqual(res.consensus_index, 1.0)
        self.assertIsInstance(res.obstruction_summary, str)

        d = res.to_dict()
        self.assertIn("cohomology_groups", d)
        self.assertIn("cochain_dimensions", d)

    def test_unanimous_consensus_trivial_cohomology(self):
        """Tests when all local sections agree perfectly, yielding exact gluing."""
        loom = SheafCohomologyLoom(section_dim=1)
        # Triangle of three overlapping lenses with identical section value 2.5
        lenses = [
            OpenSet("A", "Alpha", "Domain 1", 100.0, 100.0, 80.0, [2.5]),
            OpenSet("B", "Beta", "Domain 2", 150.0, 100.0, 80.0, [2.5]),
            OpenSet("C", "Gamma", "Domain 3", 125.0, 140.0, 80.0, [2.5]),
        ]
        for lens in lenses:
            loom.add_lens(lens)

        res = loom.build_cech_complex()
        # Pairwise discrepancy must be 0.0 everywhere
        for ov in res.overlaps:
            self.assertAlmostEqual(ov.discrepancy_norm, 0.0, places=6)

        self.assertAlmostEqual(res.global_gluing_energy, 0.0, places=6)
        self.assertAlmostEqual(res.consensus_index, 1.0, places=5)
        self.assertEqual(res.betti_h1, 0)  # No obstruction

    def test_inconsistent_triangle_obstruction(self):
        """Tests when pairwise discrepancy induces non-zero gluing energy."""
        loom = SheafCohomologyLoom(section_dim=1)
        # 3 lenses with cyclic disagreement
        lenses = [
            OpenSet("U1", "Lens 1", "Domain 1", 100.0, 100.0, 80.0, [1.0]),
            OpenSet("U2", "Lens 2", "Domain 2", 150.0, 100.0, 80.0, [2.0]),
            OpenSet("U3", "Lens 3", "Domain 3", 125.0, 140.0, 80.0, [3.0]),
        ]
        for lens in lenses:
            loom.add_lens(lens)

        res = loom.build_cech_complex()
        self.assertGreater(res.global_gluing_energy, 0.0)
        self.assertTrue(res.gluing_obstruction_detected)

    def test_svg_and_markdown_and_html_rendering(self):
        """Tests visual rendering to SVG, Markdown report, and HTML viewer."""
        loom = SheafCohomologyLoom.create_default_epistemic_cover()
        res = loom.build_cech_complex()

        # 1. SVG
        svg = loom.render_svg(res)
        self.assertTrue(svg.startswith("<svg"))
        self.assertTrue(svg.strip().endswith("</svg>"))
        self.assertIn("EPISTEMIC SHEAF COHOMOLOGY", svg)
        self.assertIn("COHOMOLOGY METRICS", svg)

        # 2. Markdown Report
        md = loom.generate_markdown_report(res)
        self.assertIn("# Sheaf-Theoretic Cohomology & Epistemic Gluing Analysis", md)
        self.assertIn("Cech Cochain Complex Architecture", md)
        self.assertIn("Pairwise Overlaps", md)

        # 3. HTML Viewer
        html_doc = loom.generate_html_viewer(res)
        self.assertIn("<!DOCTYPE html>", html_doc)
        self.assertIn("Diagnostic JSON Export", html_doc)

    def test_zero_em_dashes_constraint(self):
        """Strict negative constraint check: verify zero em dashes across code and tests."""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        files = [
            os.path.join(base_dir, "scripts", "sheaf_cohomology_loom.py"),
            os.path.join(base_dir, "tests", "test_sheaf_cohomology_loom.py"),
        ]
        for path in files:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertNotIn(chr(8212), content, f"Found em dash in {path}")


if __name__ == "__main__":
    unittest.main()
