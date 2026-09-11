"""
Unit tests for Non-Commutative Spectral Triple & Connes Distance Loom.
Verifies Dirac operator diagonalization, Connes geodesic metric calculation,
algebra commutator norms, pure Python linear algebra routines,
and zero em dash constraints.
"""

import unittest
import os
import math
from scripts.noncommutative_spectral_loom import (
    NonCommutativeSpectralLoom,
    ConceptState,
    ConceptObservable,
    ConnesDistancePair,
    matrix_zeros,
    matrix_identity,
    matrix_add,
    matrix_mult,
    matrix_commutator,
    frobenius_norm,
    spectral_operator_norm_symm,
    jacobi_eigenvalues_symm,
)


class TestNonCommutativeSpectralLoom(unittest.TestCase):
    """Test suite for NonCommutativeSpectralLoom and spectral geometry routines."""

    def test_linear_algebra_and_commutator_routines(self):
        """Tests matrix math, Jacobi diagonalization, and commutators."""
        # 1. Identity & Zero
        ident = matrix_identity(3)
        self.assertEqual(ident[0][0], 1.0)
        self.assertEqual(ident[0][1], 0.0)

        # 2. Multiplication
        a = [[1.0, 2.0], [0.0, 1.0]]
        b = [[2.0, 1.0], [1.0, 1.0]]
        ab = matrix_mult(a, b)
        ba = matrix_mult(b, a)
        self.assertNotEqual(ab, ba)  # Non-commutative

        comm = matrix_commutator(a, b)
        norm_c = frobenius_norm(comm)
        self.assertGreater(norm_c, 0.0)

        # Commutator of matrix with itself is exactly zero
        comm_self = matrix_commutator(a, a)
        self.assertAlmostEqual(frobenius_norm(comm_self), 0.0, places=6)

        # 3. Jacobi symmetric eigenvalue solver
        symm = [[2.0, 1.0], [1.0, 2.0]]
        evals, evecs = jacobi_eigenvalues_symm(symm)
        self.assertEqual(len(evals), 2)
        self.assertAlmostEqual(evals[0], 1.0, places=5)
        self.assertAlmostEqual(evals[1], 3.0, places=5)

    def test_default_cognitive_spectral_triple(self):
        """Tests initialization of default 4D cognitive spectral triple."""
        loom = NonCommutativeSpectralLoom.create_default_cognitive_spectral_triple()
        self.assertEqual(loom.hilbert_dim, 4)
        self.assertEqual(len(loom.observables), 3)
        self.assertEqual(len(loom.states), 4)

        # Verify Dirac operator is symmetric
        for i in range(4):
            for j in range(4):
                self.assertAlmostEqual(loom.dirac_operator[i][j], loom.dirac_operator[j][i], places=6)

        # Verify states are unit-normalized
        for st in loom.states:
            norm = math.sqrt(sum(x * x for x in st.vector))
            self.assertAlmostEqual(norm, 1.0, places=5)

    def test_spectral_analysis_computation(self):
        """Tests Dirac eigenspectrum, Connes distances, and commutator telemetry."""
        loom = NonCommutativeSpectralLoom.create_default_cognitive_spectral_triple()
        res = loom.compute_spectral_analysis()

        self.assertEqual(res.hilbert_dim, 4)
        self.assertEqual(len(res.dirac_eigenvalues), 4)
        self.assertGreater(res.spectral_dimension, 0.0)
        self.assertGreater(res.spectral_action, 0.0)

        # 4 states produce 6 pairwise combinations
        self.assertEqual(len(res.connes_distances), 6)
        for cd in res.connes_distances:
            self.assertGreater(cd.connes_distance, 0.0)
            self.assertGreater(cd.euclidean_distance, 0.0)
            self.assertGreater(cd.gradient_norm, 0.0)

        # Commutator norms are positive for non-commutative observables
        self.assertGreater(len(res.commutator_norms), 0)
        for comm_name, c_val in res.commutator_norms.items():
            self.assertGreater(c_val, 0.0)

        self.assertGreater(res.framing_noncommutativity_index, 0.0)

        d = res.to_dict()
        self.assertIn("dirac_eigenvalues", d)
        self.assertIn("connes_distances", d)
        self.assertIn("framing_noncommutativity_index", d)

    def test_commutative_algebra_limit(self):
        """Tests commutative diagonal algebra where all observables commute."""
        loom = NonCommutativeSpectralLoom(hilbert_dim=2)
        loom.set_dirac_operator([[1.0, 0.0], [0.0, -1.0]])

        # Two diagonal observables: [A, B] = 0
        o1 = ConceptObservable("D1", "Diag 1", [[1.0, 0.0], [0.0, 2.0]])
        o2 = ConceptObservable("D2", "Diag 2", [[3.0, 0.0], [0.0, 0.5]])
        loom.add_observable(o1)
        loom.add_observable(o2)

        s1 = ConceptState("S1", "State 1", "Basis 1", [1.0, 0.0])
        s2 = ConceptState("S2", "State 2", "Basis 2", [0.0, 1.0])
        loom.add_state(s1)
        loom.add_state(s2)

        res = loom.compute_spectral_analysis()
        self.assertAlmostEqual(res.framing_noncommutativity_index, 0.0, places=5)
        self.assertAlmostEqual(res.commutator_norms["[D1, D2]"], 0.0, places=5)

    def test_svg_and_markdown_and_html_rendering(self):
        """Tests SVG rendering, Markdown report, and HTML viewer generation."""
        loom = NonCommutativeSpectralLoom.create_default_cognitive_spectral_triple()
        res = loom.compute_spectral_analysis()

        # 1. SVG
        svg = loom.render_svg(res)
        self.assertTrue(svg.startswith("<svg"))
        self.assertTrue(svg.strip().endswith("</svg>"))
        self.assertIn("DIRAC EIGENSPECTRUM D", svg)
        self.assertIn("CONNES DISTANCE GRAPH", svg)
        self.assertIn("NC COMMUTATORS", svg)

        # 2. Markdown Report
        md = loom.generate_markdown_report(res)
        self.assertIn("# Non-Commutative Spectral Triple & Connes Distance Analysis", md)
        self.assertIn("Connes Geodesic Spectral Distances", md)
        self.assertIn("Framing Commutators", md)

        # 3. HTML Viewer
        html_doc = loom.generate_html_viewer(res)
        self.assertIn("<!DOCTYPE html>", html_doc)
        self.assertIn("Telemetry JSON Export", html_doc)

    def test_zero_em_dashes_constraint(self):
        """Strict negative constraint check: verify zero em dashes across code and tests."""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        files = [
            os.path.join(base_dir, "scripts", "noncommutative_spectral_loom.py"),
            os.path.join(base_dir, "tests", "test_noncommutative_spectral_loom.py"),
        ]
        for path in files:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertNotIn(chr(8212), content, f"Found em dash in {path}")


if __name__ == "__main__":
    unittest.main()
