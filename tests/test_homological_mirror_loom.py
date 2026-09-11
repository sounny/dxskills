"""
Unit tests for Homological Mirror Symmetry & Kontsevich Dual Loom.
Verifies Lagrangian Floer intersection calculations, coherent sheaf Ext groups,
Kontsevich equivalence theorem, Hodge diamond mirror inversion, and zero em dash constraints.
"""

import unittest
import os
from scripts.homological_mirror_loom import (
    HomologicalMirrorLoom,
    LagrangianSubmanifold,
    CoherentSheaf,
    FloerIntersectionPoint,
    MirrorSymmetryResult,
)


class TestHomologicalMirrorLoom(unittest.TestCase):
    """Test suite for HomologicalMirrorLoom and Kontsevich HMS duality."""

    def test_lagrangian_intersection_numbers(self):
        """Tests topological intersection calculation on T^2 = R^2 / Z^2."""
        loom = HomologicalMirrorLoom()

        # 1. Parallel cycles (0 intersections)
        l_par1 = LagrangianSubmanifold("L_par1", 1, 0, offset_y=0.2)
        l_par2 = LagrangianSubmanifold("L_par2", 1, 0, offset_y=0.6)
        n_par, pts_par = loom.compute_intersections(l_par1, l_par2)
        self.assertEqual(n_par, 0)
        self.assertEqual(len(pts_par), 0)

        # 2. Orthogonal cycles (1 intersection)
        l_h = LagrangianSubmanifold("L_h", 1, 0)
        l_v = LagrangianSubmanifold("L_v", 0, 1)
        n_orth, pts_orth = loom.compute_intersections(l_h, l_v)
        self.assertEqual(n_orth, 1)
        self.assertEqual(len(pts_orth), 1)

        # 3. Higher winding (2, 1) and (1, 3) -> |2*3 - 1*1| = 5
        l_a = LagrangianSubmanifold("L_a", 2, 1)
        l_b = LagrangianSubmanifold("L_b", 1, 3)
        n_ab, pts_ab = loom.compute_intersections(l_a, l_b)
        self.assertEqual(n_ab, 5)
        self.assertEqual(len(pts_ab), 5)

    def test_kontsevich_equivalence_default(self):
        """Tests Kontsevich homological equivalence on default mirror pair."""
        loom = HomologicalMirrorLoom.create_default_elliptic_mirror_pair()
        res = loom.evaluate_mirror_symmetry()

        self.assertTrue(res.kontsevich_equivalence_verified)
        self.assertEqual(res.dim_floer_cohomology_hf, 2)
        self.assertEqual(res.dim_ext_groups_sum, 2)
        self.assertEqual(res.intersection_number, 2)
        self.assertEqual(len(res.floer_points), 2)

        d = res.to_dict()
        self.assertIn("a_model_lagrangians", d)
        self.assertIn("b_model_sheaves", d)
        self.assertIn("kontsevich_equivalence_verified", d)

    def test_hodge_diamond_inversion(self):
        """Tests mirror symmetry exchange of Hodge numbers h11 <-> h21."""
        loom = HomologicalMirrorLoom()
        res = loom.evaluate_mirror_symmetry()

        h_orig = res.hodge_diamond_original
        h_mirr = res.hodge_diamond_mirror

        self.assertEqual(h_orig["h11"], h_mirr["h21"])
        self.assertEqual(h_orig["h21"], h_mirr["h11"])
        self.assertEqual(h_orig["chi"], -h_mirr["chi"])

    def test_svg_and_markdown_and_html_rendering(self):
        """Tests rendering of dark titanium SVG, Markdown report, and HTML application."""
        loom = HomologicalMirrorLoom.create_default_elliptic_mirror_pair()
        res = loom.evaluate_mirror_symmetry()

        # 1. SVG
        svg = loom.render_svg(res)
        self.assertTrue(svg.startswith("<svg"))
        self.assertTrue(svg.strip().endswith("</svg>"))
        self.assertIn("A-MODEL: FUKAYA TORUS", svg)
        self.assertIn("B-MODEL: COHERENT SHEAVES", svg)
        self.assertIn("KONTSEVICH EQUIVALENCE", svg)

        # 2. Markdown Report
        md = loom.generate_markdown_report(res)
        self.assertIn("# Homological Mirror Symmetry & Kontsevich Dual Analysis", md)
        self.assertIn("A-Model vs B-Model Dual Pairs", md)
        self.assertIn("Hodge Diamond Inversion", md)

        # 3. HTML Viewer
        html_doc = loom.generate_html_viewer(res)
        self.assertIn("<!DOCTYPE html>", html_doc)
        self.assertIn("Diagnostic JSON Export", html_doc)

    def test_zero_em_dashes_constraint(self):
        """Strict negative constraint check: verify zero em dashes across code and tests."""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        files = [
            os.path.join(base_dir, "scripts", "homological_mirror_loom.py"),
            os.path.join(base_dir, "tests", "test_homological_mirror_loom.py"),
        ]
        for path in files:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertNotIn(chr(8212), content, f"Found em dash in {path}")


if __name__ == "__main__":
    unittest.main()
