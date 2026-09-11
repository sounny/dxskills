"""
Tests for Geometric Satake Equivalence and Mirkovic-Vilonen Cycles Loom.
Verifies affine Grassmannian Schubert varieties, spherical perverse sheaves,
Mirkovic-Vilonen cycles, convolution fusion, and strict zero em dash compliance.
"""

import unittest
from scripts.geometric_satake_loom import (
    GeometricSatakeLoom,
    ReductiveGroupType,
    ReductiveGroupData,
    AffineSchubertVarietyData,
    MirkovicVilonenCycleData,
    SatakeEquivalenceData,
)


class TestGeometricSatakeLoom(unittest.TestCase):
    """Test suite for GeometricSatakeLoom algorithms and visualizers."""

    def setUp(self):
        self.loom = GeometricSatakeLoom()

    def test_reductive_group_and_schubert_variety(self):
        """Verify reductive group and affine Schubert variety properties."""
        self.assertGreaterEqual(len(self.loom.groups), 1)
        grp = self.loom.groups[0]
        self.assertIsInstance(grp, ReductiveGroupData)
        self.assertEqual(grp.rank, 1)
        self.assertEqual(grp.dual_group_label, "PGL_2")
        self.assertEqual(grp.weyl_group_order, 2)

        self.assertGreaterEqual(len(self.loom.schubert_varieties), 1)
        var = self.loom.schubert_varieties[0]
        self.assertIsInstance(var, AffineSchubertVarietyData)
        self.assertEqual(var.dominant_coweight, [2])
        # dim = 2 * <rho, lambda> = 2 * (1.0 * 2) = 4
        self.assertEqual(var.dimension_2rho_lambda, 4)
        self.assertIn("IC(Gr^[2])", var.intersection_cohomology_sheaf)

    def test_mirkovic_vilonen_cycles(self):
        """Verify Mirkovic-Vilonen cycles as weight spaces of dual representations."""
        cycles = self.loom.evaluate_mirkovic_vilonen_cycles()
        self.assertEqual(len(cycles), 3)  # weights -2, 0, 2 for SL2 coweight [2]
        weights = [c.weight_mu[0] for c in cycles]
        self.assertEqual(weights, [-2, 0, 2])
        for c in cycles:
            self.assertIsInstance(c, MirkovicVilonenCycleData)
            self.assertEqual(c.weight_space_dimension, 1)

    def test_satake_equivalence_and_fusion(self):
        """Verify tensor categorical equivalence and convolution fusion decomposition."""
        eq = self.loom.compute_satake_equivalence("SATAKE-TEST-01")
        self.assertIsInstance(eq, SatakeEquivalenceData)
        self.assertEqual(eq.representation_dimension, 3)  # Sym^2(C^2) is 3-dimensional
        self.assertIn("Sym^2(C^2)", eq.highest_weight_representation)
        # Clebsch-Gordan: V(2) (x) V(2) = V(4) (+) V(2) (+) V(0)
        self.assertEqual(len(eq.tensor_convolution_decomposition), 3)
        self.assertIn("IC(Gr^[4])", eq.tensor_convolution_decomposition)
        self.assertIn("IC(Gr^[2])", eq.tensor_convolution_decomposition)
        self.assertIn("IC(Gr^[0])", eq.tensor_convolution_decomposition)

    def test_rank_2_group_sl3(self):
        """Verify SL3 / PGL3 geometric Satake configuration and weight multiplicities."""
        loom_sl3 = GeometricSatakeLoom(
            default_group=ReductiveGroupType.SL3_PGL3.value,
            coweight_level=2,
        )
        grp = loom_sl3.groups[0]
        self.assertEqual(grp.rank, 2)
        self.assertEqual(grp.cartan_type, "A_2")
        self.assertEqual(grp.dual_group_label, "PGL_3")

        var = loom_sl3.schubert_varieties[0]
        self.assertEqual(var.dominant_coweight, [2, 1])

        cycles = loom_sl3.evaluate_mirkovic_vilonen_cycles()
        self.assertGreater(len(cycles), 0)
        # Check that the zero weight space has multiplicity 2 for adjoint-like weight
        zero_weights = [c for c in cycles if c.weight_mu == [0, 0]]
        self.assertEqual(len(zero_weights), 1)
        self.assertEqual(zero_weights[0].weight_space_dimension, 2)

    def test_svg_and_zero_em_dash_compliance(self):
        """Verify SVG rendering, JSON telemetry, and zero em dashes across all outputs."""
        self.loom.evaluate_mirkovic_vilonen_cycles()
        self.loom.compute_satake_equivalence()

        svg = self.loom.generate_satake_svg()
        self.assertIsInstance(svg, str)
        self.assertTrue(svg.startswith("<svg"))
        self.assertTrue(svg.endswith("</svg>"))
        self.assertIn("Affine Grassmannian Gr_G Stratification", svg)
        self.assertIn("Mirkovic-Vilonen Weight Spaces", svg)
        self.assertIn("Satake Tensor Equivalence", svg)

        # Strict zero em dash verification
        self.assertNotIn("\u2014", svg)
        self.assertNotIn(chr(8212), svg)

        json_str = self.loom.to_json()
        self.assertNotIn("\u2014", json_str)
        self.assertNotIn(chr(8212), json_str)

        with open("scripts/geometric_satake_loom.py", encoding="utf-8") as f:
            src = f.read()
        self.assertNotIn("\u2014", src)
        self.assertNotIn(chr(8212), src)


if __name__ == "__main__":
    unittest.main()
