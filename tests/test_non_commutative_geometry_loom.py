"""
Tests for Non-Commutative Geometry and Connes Spectral Triples Loom.
Verifies spectral triples, Dirac eigenvalue ladders, Chamseddine-Connes action,
Connes geodesic distance, and strict zero em dash compliance.
"""

import unittest
from scripts.non_commutative_geometry_loom import (
    NonCommutativeGeometryLoom,
    SpectralTripleArchetype,
    DiracOperatorType,
    SpectralTripleData,
    DiracSpectrumData,
    SpectralActionData,
    ConnesDistanceData,
)


class TestNonCommutativeGeometryLoom(unittest.TestCase):
    """Test suite for NonCommutativeGeometryLoom algorithms and visualizers."""

    def setUp(self):
        self.loom = NonCommutativeGeometryLoom()

    def test_default_spectral_triple_initialization(self):
        """Verify default spectral triple construction for non-commutative torus."""
        self.assertGreaterEqual(len(self.loom.triples), 1)
        tr = self.loom.triples[0]
        self.assertIsInstance(tr, SpectralTripleData)
        self.assertEqual(tr.metric_dimension, 2)
        self.assertTrue(tr.is_even_graded)
        self.assertTrue(tr.has_real_structure)
        self.assertEqual(tr.ko_dimension_mod_8, 2)
        self.assertIn("A_theta", tr.algebra_label)

    def test_dirac_spectrum_evaluation(self):
        """Verify Dirac eigenvalue ladder evaluation on non-commutative torus."""
        spectrum = self.loom.evaluate_dirac_spectrum("SPEC-001", max_n=3)
        self.assertIsInstance(spectrum, DiracSpectrumData)
        self.assertEqual(spectrum.spectral_dimension, 2.0)
        self.assertEqual(spectrum.zero_modes_count, 1)
        self.assertGreater(len(spectrum.eigenvalues_sample), 0)
        self.assertGreater(spectrum.dixmier_trace_volume, 0.0)

    def test_chamseddine_connes_spectral_action(self):
        """Verify Chamseddine-Connes spectral action expansion terms."""
        action = self.loom.evaluate_spectral_action("ACT-001", cutoff_lambda=50.0)
        self.assertIsInstance(action, SpectralActionData)
        self.assertGreater(action.cosmological_term, 0.0)
        self.assertGreater(action.einstein_hilbert_term, 0.0)
        self.assertGreater(action.yang_mills_higgs_term, 0.0)
        self.assertGreater(action.total_spectral_action, 0.0)
        self.assertEqual(action.cutoff_lambda, 50.0)

    def test_connes_spectral_distance(self):
        """Verify Connes dual geodesic distance computation."""
        dist = self.loom.evaluate_connes_distance("DIST-001", coordinate_displacement=2.5)
        self.assertIsInstance(dist, ConnesDistanceData)
        self.assertAlmostEqual(dist.spectral_distance, 2.5)
        self.assertTrue(dist.is_classical_metric_limit)
        self.assertAlmostEqual(dist.optimal_commutator_bound, 1.0)

    def test_svg_generation_and_zero_em_dash_compliance(self):
        """Verify SVG generation, JSON export, and zero em dashes across all outputs."""
        self.loom.evaluate_dirac_spectrum("SPEC-TEST", max_n=4)
        self.loom.evaluate_spectral_action("ACT-TEST", cutoff_lambda=100.0)
        self.loom.evaluate_connes_distance("DIST-TEST", coordinate_displacement=1.414)

        svg = self.loom.generate_ncg_svg()
        self.assertIsInstance(svg, str)
        self.assertTrue(svg.startswith("<svg"))
        self.assertTrue(svg.endswith("</svg>"))
        self.assertIn("Dirac Spectrum Ladder", svg)
        self.assertIn("Chamseddine-Connes Action", svg)
        self.assertIn("Connes Spectral Distance", svg)

        # Verify strict zero em dash compliance
        self.assertNotIn("\u2014", svg)
        self.assertNotIn(chr(8212), svg)

        # Verify JSON export
        json_str = self.loom.to_json()
        self.assertIn("default_archetype", json_str)
        self.assertNotIn("\u2014", json_str)
        self.assertNotIn(chr(8212), json_str)

        # Source code compliance
        with open("scripts/non_commutative_geometry_loom.py", encoding="utf-8") as f:
            src = f.read()
        self.assertNotIn("\u2014", src)
        self.assertNotIn(chr(8212), src)


if __name__ == "__main__":
    unittest.main()
