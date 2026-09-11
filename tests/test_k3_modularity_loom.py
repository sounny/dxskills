#!/usr/bin/env python3
"""
Unit tests for K3 Surfaces Modularity and Borcherds Automorphic Products Loom.
Zero em dashes strictly enforced.
"""

import unittest
from scripts.k3_modularity_loom import (
    K3ModularityLoom,
    K3LatticeDecomposition,
    BorcherdsProductState,
    K3ModularityResult,
)


class TestK3ModularityLoom(unittest.TestCase):
    """Test suite for K3ModularityLoom mathematical and cognitive capabilities."""

    def setUp(self) -> None:
        self.singular_loom = K3ModularityLoom("Shioda-Inose Singular K3 (D=-3)")
        self.fermat_loom = K3ModularityLoom("Fermat Quartic K3 (D=-4)")
        self.generic_loom = K3ModularityLoom("Generic K3 (Picard 1)")

    def test_k3_lattice_invariants(self) -> None:
        """Verify Picard number, transcendental rank, and signatures."""
        lat_sing = self.singular_loom.lattice
        self.assertEqual(lat_sing.picard_number, 20)
        self.assertEqual(lat_sing.transcendental_rank, 2)
        self.assertEqual(lat_sing.picard_signature, (1, 19))
        self.assertEqual(lat_sing.transcendental_signature, (2, 0))
        self.assertTrue(lat_sing.is_singular)
        self.assertEqual(lat_sing.discriminant_d, -3)

        lat_gen = self.generic_loom.lattice
        self.assertEqual(lat_gen.picard_number, 1)
        self.assertEqual(lat_gen.transcendental_rank, 21)
        self.assertFalse(lat_gen.is_singular)

    def test_borcherds_product_evaluation(self) -> None:
        """Verify Borcherds singular theta lift and Weyl vector normalization."""
        b_state = self.singular_loom.evaluate_borcherds_product(sample_z=complex(0.1, 0.5))
        self.assertIsInstance(b_state, BorcherdsProductState)
        self.assertEqual(b_state.lattice_signature, (2, 0))
        self.assertEqual(b_state.input_modular_weight, -8.0)
        self.assertGreater(b_state.weyl_vector_norm, 1.0)
        self.assertTrue(b_state.singular_theta_lift_valid)
        self.assertIsInstance(b_state.product_evaluation_sample, complex)

    def test_kronecker_quadratic_character(self) -> None:
        """Verify Kronecker quadratic character values for CM discriminants."""
        # For D = -3: ( -3 / 2 ) = -1 (since -3 = 5 mod 8)
        self.assertEqual(self.singular_loom.compute_kronecker_symbol(-3, 2), -1)
        # For D = -3: ( -3 / 3 ) = 0 (ramified)
        self.assertEqual(self.singular_loom.compute_kronecker_symbol(-3, 3), 0)
        # For D = -3: ( -3 / 7 ) = 1 (split, 7 = 1 mod 3)
        self.assertEqual(self.singular_loom.compute_kronecker_symbol(-3, 7), 1)
        # For D = -3: ( -3 / 5 ) = -1 (inert, 5 = 2 mod 3)
        self.assertEqual(self.singular_loom.compute_kronecker_symbol(-3, 5), -1)

    def test_weight3_cm_hecke_eigenvalues_and_points(self) -> None:
        """Verify weight 3 newform Hecke eigenvalues and K3 point counts over F_p."""
        hecke, points = self.singular_loom.compute_weight3_hecke_eigenvalues(-3)
        self.assertIn(2, hecke)
        self.assertIn(3, hecke)
        self.assertIn(7, hecke)

        # Inert prime p = 2: a_2 = 0
        self.assertEqual(hecke[2], 0)
        # Point count over F_2: 1 + 4 + 20*2 - 0 = 45
        self.assertEqual(points[2], 45)

        # For p = 7 (split): a_7 != 0
        self.assertIn(7, points)
        self.assertGreater(points[7], 0)

    def test_complete_analysis_and_svg_rendering(self) -> None:
        """Verify complete analysis pipeline, zero em dashes, and SVG generation."""
        res = self.singular_loom.analyze()
        self.assertIsInstance(res, K3ModularityResult)
        self.assertTrue(res.modularity_proven)
        self.assertEqual(res.modular_weight, 3)
        self.assertEqual(res.modular_level, 3)

        svg = self.singular_loom.render_svg(res)
        self.assertIn("<svg", svg)
        self.assertIn("K3 SURFACES MODULARITY", svg)
        self.assertIn("PANEL A:", svg)
        self.assertIn("PANEL B:", svg)
        self.assertIn("PANEL C:", svg)
        self.assertIn("PANEL D:", svg)
        self.assertNotIn("\u2014", svg, "Em dash detected in generated SVG")


if __name__ == "__main__":
    unittest.main()
