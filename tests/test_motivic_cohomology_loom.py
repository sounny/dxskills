"""
Unit tests for Motivic Cohomology & Beilinson-Soule Regulators Loom.
Strictly verifies zero em dashes (chr(8212)), Bloch higher Chow cycles,
Deligne intermediate Jacobians, Beilinson regulators, and Adams eigenspaces.
"""

import unittest
import os
import json
from scripts.motivic_cohomology_loom import (
    MotivicCohomologyLoom,
    MotivicComplexType,
    RegulatorDomain,
    RegulatorRegime,
)


class TestMotivicCohomologyLoom(unittest.TestCase):
    """Test suite for MotivicCohomologyLoom engine and spatial cognitive mappings."""

    def setUp(self):
        self.loom = MotivicCohomologyLoom(
            domain=RegulatorDomain.NUMBER_FIELD_RING.value,
            codimension_p=2,
            weight_q=2,
        )

    def test_higher_chow_cycle_construction(self):
        """Verify Bloch higher Chow cycle parameters and boundary closure."""
        cycle = self.loom.construct_higher_chow_cycle("CYCLE-01", codimension_p=2, simplicial_weight_m=1)
        self.assertEqual(cycle.cycle_id, "CYCLE-01")
        self.assertEqual(cycle.codimension_p, 2)
        self.assertEqual(cycle.simplicial_weight_m, 1)
        # Motivic degree 2p - m = 4 - 1 = 3
        self.assertEqual(cycle.motivic_degree, 3)
        self.assertEqual(cycle.boundary_norm, 0.0)
        self.assertTrue(cycle.is_closed)

        d = cycle.to_dict()
        self.assertIn("cycle_id", d)
        self.assertEqual(d["motivic_degree"], 3)

    def test_deligne_intermediate_jacobian(self):
        """Verify Deligne intermediate Jacobian dimension and period volume."""
        jac = self.loom.jacobians[0]
        self.assertIsNotNone(jac)
        self.assertEqual(jac.weight_q, 2)
        self.assertEqual(jac.complex_dimension, 1)
        self.assertGreater(jac.period_volume, 0.0)

        # Higher weight test
        higher_loom = MotivicCohomologyLoom(weight_q=3)
        h_jac = higher_loom.jacobians[0]
        self.assertEqual(h_jac.weight_q, 3)
        self.assertEqual(h_jac.complex_dimension, 2)

    def test_beilinson_regulator_evaluation(self):
        """Verify Beilinson regulator vector and lattice volume determinant."""
        cycle = self.loom.construct_higher_chow_cycle("CYCLE-02")
        reg = self.loom.evaluate_beilinson_regulator("REG-01", cycle.cycle_id, dimension_d=2)
        self.assertEqual(reg.regulator_id, "REG-01")
        self.assertEqual(len(reg.regulator_vector), 2)
        self.assertGreater(reg.regulator_determinant, 0.0)
        self.assertTrue(reg.beilinson_conjecture_verified)

    def test_adams_eigenspace_decomposition(self):
        """Verify algebraic K-theory Adams eigenspace matching higher Chow groups."""
        adams = self.loom.decompose_adams_eigenspace(k_group_label="K_1(X)", m_weight=1, j_weight=2)
        self.assertEqual(adams.k_group_label, "K_1(X)")
        self.assertEqual(adams.simplicial_weight_m, 1)
        self.assertEqual(adams.adams_weight_j, 2)
        self.assertIn("CH^2(X, 1)", adams.motivic_cohomology_group)
        self.assertEqual(adams.eigenspace_rank, 1)

    def test_svg_json_and_zero_em_dashes(self):
        """Verify SVG generation, JSON export, and strict zero em dash compliance."""
        cycle = self.loom.construct_higher_chow_cycle("CYCLE-TEST")
        self.loom.evaluate_beilinson_regulator("REG-TEST", cycle.cycle_id)
        self.loom.decompose_adams_eigenspace()

        svg = self.loom.generate_motivic_svg()
        self.assertTrue(svg.startswith("<svg"))
        self.assertTrue(svg.endswith("</svg>"))
        self.assertIn("Motivic Cohomology", svg)
        self.assertIn("Bloch Higher Chow", svg)
        self.assertIn("Beilinson Regulator", svg)

        # Assert ZERO em dashes anywhere in generated SVG
        self.assertNotIn(chr(8212), svg)

        # Assert ZERO em dashes in JSON export
        json_data = self.loom.to_json()
        self.assertNotIn(chr(8212), json_data)

        # Verify source file has zero em dashes
        loom_path = os.path.join(os.path.dirname(__file__), "..", "scripts", "motivic_cohomology_loom.py")
        with open(loom_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertNotIn(chr(8212), content)


if __name__ == "__main__":
    unittest.main()
