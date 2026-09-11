#!/usr/bin/env python3
"""
Unit tests for Calabi-Yau Modularity and Attractor Mechanism Loom.
Zero em dashes strictly enforced.
"""

import unittest
from scripts.calabi_yau_modularity_loom import (
    CalabiYauModularityLoom,
    HodgeDiamond,
    PicardFuchsSolution,
    AttractorState,
    CalabiYauModularityResult,
)


class TestCalabiYauModularityLoom(unittest.TestCase):
    """Test suite for CalabiYauModularityLoom mathematical and cognitive features."""

    def setUp(self) -> None:
        self.quintic_loom = CalabiYauModularityLoom("Mirror Quintic Threefold")
        self.rigid_loom = CalabiYauModularityLoom("Rigid Schoen Calabi-Yau Threefold")

    def test_hodge_diamond_structure(self) -> None:
        """Verify Hodge numbers and middle cohomology dimension."""
        h_quintic = self.quintic_loom.hodge
        self.assertEqual(h_quintic.h11, 101)
        self.assertEqual(h_quintic.h21, 1)
        self.assertEqual(h_quintic.euler_char, 200)
        self.assertEqual(h_quintic.middle_cohomology_dim(), 4)
        self.assertFalse(h_quintic.is_rigid())

        h_rigid = self.rigid_loom.hodge
        self.assertEqual(h_rigid.h21, 0)
        self.assertEqual(h_rigid.middle_cohomology_dim(), 2)
        self.assertTrue(h_rigid.is_rigid())

    def test_picard_fuchs_series_solution(self) -> None:
        """Verify Frobenius series solutions and conifold singularity distance."""
        z = complex(0.02, 0.05)
        pf = self.quintic_loom.compute_picard_fuchs_series(z, terms=10)
        self.assertIsInstance(pf, PicardFuchsSolution)
        self.assertGreater(abs(pf.varpi_0), 0.5)
        self.assertGreater(pf.conifold_dist, 0.0)
        self.assertEqual(pf.monodromy_order, 5)

    def test_attractor_flow_and_entropy(self) -> None:
        """Verify extremal black hole attractor flow to CM fixed point."""
        charges = (1, 0, 0, -4)
        state, trajectory = self.quintic_loom.simulate_attractor_flow(
            charges=charges, steps=25, init_z=complex(0.1, 0.2)
        )
        self.assertIsInstance(state, AttractorState)
        self.assertEqual(state.charge_vector, charges)
        self.assertGreater(state.horizon_entropy, 0.0)
        self.assertLess(state.cm_discriminant, 0)
        self.assertEqual(len(trajectory), 25)

    def test_hecke_spectrum_and_euler_factors(self) -> None:
        """Verify weight 4 modular form eigenvalues and degree 2 Euler factors."""
        eigenvalues, l_factors = self.rigid_loom.compute_modularity_spectrum(level=48)
        self.assertIn(2, eigenvalues)
        self.assertIn(3, eigenvalues)
        self.assertIn(5, eigenvalues)
        self.assertEqual(eigenvalues[3], -6)
        self.assertEqual(eigenvalues[5], -10)

        # Euler factor for p = 3: 1 - (-6)T + 27 T^2
        poly = l_factors[3]
        self.assertEqual(poly[0], 1.0)
        self.assertEqual(poly[1], 6.0)
        self.assertEqual(poly[2], 27.0)

    def test_complete_analysis_and_svg_rendering(self) -> None:
        """Verify complete pipeline, zero em dashes, and SVG generation."""
        result = self.quintic_loom.analyze(charges=(1, 0, 0, -5))
        self.assertIsInstance(result, CalabiYauModularityResult)
        self.assertTrue(result.modularity_proven)

        svg = self.quintic_loom.render_svg(result)
        self.assertIn("<svg", svg)
        self.assertIn("CALABI-YAU MODULARITY", svg)
        self.assertIn("PANEL A:", svg)
        self.assertIn("PANEL B:", svg)
        self.assertIn("PANEL C:", svg)
        self.assertIn("PANEL D:", svg)
        self.assertNotIn("\u2014", svg, "Em dash detected in generated SVG")


if __name__ == "__main__":
    unittest.main()
