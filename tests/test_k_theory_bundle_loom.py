"""
Unit tests for Topological K-Theory & Vector Bundle Classification Loom.
Verifies clutching function degrees, Grothendieck group virtual classes,
Bott periodicity cycle evaluation, stable equivalence, and zero em dash constraints.
"""

import unittest
import os
import math
from scripts.k_theory_bundle_loom import (
    KTheoryBundleLoom,
    VectorBundle,
    VirtualBundleKClass,
    BottPeriodicityStep,
    compute_clutching_degree,
)


class TestKTheoryBundleLoom(unittest.TestCase):
    """Test suite for KTheoryBundleLoom and vector bundle classification."""

    def test_clutching_degree_calculation(self):
        """Tests winding number / degree of clutching maps S^1 -> C*."""
        # 1. Trivial map (constant 1.0)
        deg_triv = compute_clutching_degree(lambda theta: complex(1.0, 0.0))
        self.assertEqual(deg_triv, 0)

        # 2. Hopf map e^{i theta} (degree +1)
        deg_hopf = compute_clutching_degree(lambda theta: complex(math.cos(theta), math.sin(theta)))
        self.assertEqual(deg_hopf, 1)

        # 3. Anti-Hopf map e^{-i theta} (degree -1)
        deg_antihopf = compute_clutching_degree(lambda theta: complex(math.cos(-theta), math.sin(-theta)))
        self.assertEqual(deg_antihopf, -1)

        # 4. Degree 2 winding e^{2i theta}
        deg_double = compute_clutching_degree(lambda theta: complex(math.cos(2 * theta), math.sin(2 * theta)))
        self.assertEqual(deg_double, 2)

    def test_default_cognitive_suite(self):
        """Tests initialization and bundle invariants in default suite."""
        loom = KTheoryBundleLoom.create_default_cognitive_k_theory_suite()
        self.assertEqual(len(loom.bundles), 4)

        b_triv = next(b for b in loom.bundles if b.bundle_id == "E_triv")
        b_hopf = next(b for b in loom.bundles if b.bundle_id == "E_hopf")
        b_anti = next(b for b in loom.bundles if b.bundle_id == "E_antihopf")
        b_syn = next(b for b in loom.bundles if b.bundle_id == "E_synergy")

        self.assertEqual(b_triv.rank, 1)
        self.assertEqual(b_triv.first_chern_number_c1, 0)
        self.assertTrue(b_triv.is_trivial)

        self.assertEqual(b_hopf.rank, 1)
        self.assertEqual(b_hopf.first_chern_number_c1, 1)
        self.assertFalse(b_hopf.is_trivial)

        self.assertEqual(b_anti.first_chern_number_c1, -1)

        self.assertEqual(b_syn.rank, 2)
        self.assertEqual(b_syn.first_chern_number_c1, 1)

    def test_grothendieck_classes_and_stable_equivalence(self):
        """Tests Grothendieck group virtual bundles and stable equivalence."""
        loom = KTheoryBundleLoom.create_default_cognitive_k_theory_suite()
        res = loom.classify_bundles()

        self.assertEqual(res.num_bundles, 4)
        self.assertEqual(len(res.k_classes), 4)
        self.assertTrue(res.stable_equivalence_verified)
        self.assertEqual(res.h_topological_charge, 1)

        # Verify Chern character of Hopf class
        k_hopf = next(kc for kc in res.k_classes if kc.bundle_e_id == "E_hopf")
        self.assertEqual(k_hopf.virtual_rank, 0)  # 1 - 1 = 0
        self.assertEqual(k_hopf.ch1, 1.0)
        self.assertFalse(k_hopf.is_stably_trivial)

        # Verify trivial class is stably trivial
        k_triv = next(kc for kc in res.k_classes if kc.bundle_e_id == "E_triv")
        self.assertTrue(k_triv.is_stably_trivial)

        d = res.to_dict()
        self.assertIn("bundles", d)
        self.assertIn("k_classes", d)
        self.assertIn("bott_periodicity_cycle", d)

    def test_bott_periodicity_cycle_steps(self):
        """Tests Bott periodicity 2-fold complex and 8-fold real cycles."""
        loom = KTheoryBundleLoom()
        cycle = loom.evaluate_bott_periodicity_cycle()

        self.assertEqual(len(cycle), 9)  # k = 0 .. 8
        for k, step in enumerate(cycle):
            self.assertEqual(step.dimension_k, k)
            self.assertEqual(step.mod_2_phase, k % 2)
            self.assertEqual(step.mod_8_phase, k % 8)
            self.assertIsInstance(step.complex_group_pi_k_minus_1_u, str)
            self.assertIsInstance(step.real_group_pi_k_minus_1_o, str)

    def test_svg_and_markdown_and_html_rendering(self):
        """Tests rendering of dark titanium SVG, Markdown report, and HTML application."""
        loom = KTheoryBundleLoom.create_default_cognitive_k_theory_suite()
        res = loom.classify_bundles()

        # 1. SVG
        svg = loom.render_svg(res)
        self.assertTrue(svg.startswith("<svg"))
        self.assertTrue(svg.strip().endswith("</svg>"))
        self.assertIn("CLUTCHING WINDING LOOP", svg)
        self.assertIn("BOTT PERIODICITY WHEEL", svg)
        self.assertIn("GROTHENDIECK K_0(X)", svg)

        # 2. Markdown Report
        md = loom.generate_markdown_report(res)
        self.assertIn("# Topological K-Theory & Vector Bundle Classification Analysis", md)
        self.assertIn("Classified Vector Bundles", md)
        self.assertIn("Bott Periodicity Cycles", md)

        # 3. HTML Viewer
        html_doc = loom.generate_html_viewer(res)
        self.assertIn("<!DOCTYPE html>", html_doc)
        self.assertIn("Diagnostic JSON Export", html_doc)

    def test_zero_em_dashes_constraint(self):
        """Strict negative constraint check: verify zero em dashes across code and tests."""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        files = [
            os.path.join(base_dir, "scripts", "k_theory_bundle_loom.py"),
            os.path.join(base_dir, "tests", "test_k_theory_bundle_loom.py"),
        ]
        for path in files:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertNotIn(chr(8212), content, f"Found em dash in {path}")


if __name__ == "__main__":
    unittest.main()
