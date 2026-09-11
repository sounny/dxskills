"""
Unit tests for Atiyah-Singer Index Theorem & Topological Anomaly Loom.
Verifies analytical vs topological index equivalence, characteristic classes,
chiral Dirac operator spectra, spectral flows, and zero em dash constraints.
"""

import unittest
import os
import math
from scripts.atiyah_singer_index_loom import (
    AtiyahSingerIndexLoom,
    CharacteristicClasses,
    AtiyahSingerResult,
    SpectralFlowPoint,
    gaussian_rank,
    jacobi_symm_eigenvalues,
)


class TestAtiyahSingerIndexLoom(unittest.TestCase):
    """Test suite for AtiyahSingerIndexLoom and topological index theorems."""

    def test_gaussian_rank_and_jacobi_eigenvalues(self):
        """Tests linear algebra routines for rank and eigenspectra."""
        # 1. Full rank 3x3
        m_full = [[1.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 3.0]]
        self.assertEqual(gaussian_rank(m_full), 3)

        # 2. Rank deficient 3x3
        m_def = [[1.0, 2.0, 3.0], [2.0, 4.0, 6.0], [0.0, 1.0, 1.0]]
        self.assertEqual(gaussian_rank(m_def), 2)

        # 3. Rectangular 4x3
        m_rect = [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
            [0.0, 0.0, 0.0],
        ]
        self.assertEqual(gaussian_rank(m_rect), 3)

        # 4. Jacobi symmetric eigenvalues
        symm = [[3.0, 1.0], [1.0, 3.0]]
        evals = jacobi_symm_eigenvalues(symm)
        self.assertEqual(len(evals), 2)
        self.assertAlmostEqual(evals[0], 2.0, places=5)
        self.assertAlmostEqual(evals[1], 4.0, places=5)

    def test_characteristic_classes_genus_variation(self):
        """Tests topological invariants across different manifold genera."""
        # Genus 0 (Sphere): chi = 2
        loom_g0 = AtiyahSingerIndexLoom(manifold_dim=2, genus=0)
        cc_g0 = loom_g0.compute_characteristic_classes()
        self.assertEqual(cc_g0.euler_characteristic, 2)
        self.assertEqual(cc_g0.genus, 0)
        self.assertAlmostEqual(cc_g0.todd_genus, 1.0, places=5)

        # Genus 1 (Torus): chi = 0
        loom_g1 = AtiyahSingerIndexLoom(manifold_dim=2, genus=1)
        cc_g1 = loom_g1.compute_characteristic_classes()
        self.assertEqual(cc_g1.euler_characteristic, 0)
        self.assertEqual(cc_g1.genus, 1)
        self.assertAlmostEqual(cc_g1.todd_genus, 0.0, places=5)

        # Genus 2 (Double Torus): chi = -2
        loom_g2 = AtiyahSingerIndexLoom(manifold_dim=2, genus=2)
        cc_g2 = loom_g2.compute_characteristic_classes()
        self.assertEqual(cc_g2.euler_characteristic, -2)
        self.assertEqual(cc_g2.genus, 2)
        self.assertAlmostEqual(cc_g2.todd_genus, -1.0, places=5)

    def test_chiral_dirac_operator_and_index_theorem(self):
        """Tests Atiyah-Singer index theorem equivalence: ind_a == ind_t."""
        loom = AtiyahSingerIndexLoom(manifold_dim=2, genus=1, twisting_bundle_rank=2)
        res = loom.evaluate_atiyah_singer()

        self.assertTrue(res.index_theorem_verified)
        self.assertEqual(res.analytical_index, res.topological_index)
        self.assertEqual(res.analytical_index, -1)
        self.assertEqual(res.dimension_ker_d, 0)
        self.assertEqual(res.dimension_coker_d, 1)
        self.assertGreater(res.chiral_anomaly_coefficient, 0.0)

        d = res.to_dict()
        self.assertIn("analytical_index", d)
        self.assertIn("topological_index", d)
        self.assertIn("characteristic_classes", d)

    def test_spectral_flow_trajectory(self):
        """Tests 1-parameter family Dirac operator eigenspectrum tracking."""
        loom = AtiyahSingerIndexLoom(manifold_dim=2, genus=1)
        traj, sf = loom.compute_spectral_flow(steps=11)

        self.assertEqual(len(traj), 11)
        self.assertEqual(traj[0].parameter_t, 0.0)
        self.assertEqual(traj[-1].parameter_t, 1.0)

        for pt in traj:
            self.assertEqual(len(pt.eigenvalues), 7)  # 4 + 3 = 7
            self.assertGreaterEqual(pt.num_positive, 0)
            self.assertGreaterEqual(pt.num_negative, 0)
            self.assertGreaterEqual(pt.num_zero, 0)

    def test_svg_and_markdown_and_html_rendering(self):
        """Tests rendering of dark titanium SVG, Markdown report, and HTML application."""
        loom = AtiyahSingerIndexLoom()
        res = loom.evaluate_atiyah_singer()

        # 1. SVG
        svg = loom.render_svg(res)
        self.assertTrue(svg.startswith("<svg"))
        self.assertTrue(svg.strip().endswith("</svg>"))
        self.assertIn("ATIYAH-SINGER INDEX THEOREM", svg)
        self.assertIn("DIRAC SPECTRAL FLOW", svg)
        self.assertIn("INDEX THEOREM EQUALITY", svg)

        # 2. Markdown Report
        md = loom.generate_markdown_report(res)
        self.assertIn("# Atiyah-Singer Index Theorem & Topological Anomaly Analysis", md)
        self.assertIn("Topological Invariants & Characteristic Classes", md)
        self.assertIn("Spectral Flow Telemetry", md)

        # 3. HTML Viewer
        html_doc = loom.generate_html_viewer(res)
        self.assertIn("<!DOCTYPE html>", html_doc)
        self.assertIn("Diagnostic JSON Export", html_doc)

    def test_zero_em_dashes_constraint(self):
        """Strict negative constraint check: verify zero em dashes across code and tests."""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        files = [
            os.path.join(base_dir, "scripts", "atiyah_singer_index_loom.py"),
            os.path.join(base_dir, "tests", "test_atiyah_singer_index_loom.py"),
        ]
        for path in files:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertNotIn(chr(8212), content, f"Found em dash in {path}")


if __name__ == "__main__":
    unittest.main()
