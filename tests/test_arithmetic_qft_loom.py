"""
Tests for Arithmetic Quantum Field Theory and Dijkgraaf-Witten Invariants Loom.
Verifies finite gauge groups, arithmetic 3-manifolds, Galois representations,
arithmetic Chern-Simons actions, partition functions, and strict zero em dash compliance.
"""

import unittest
from scripts.arithmetic_qft_loom import (
    ArithmeticQFTLoom,
    ArithmeticGaugeGroupType,
    ArithmeticManifoldType,
    ArithmeticGaugeGroupData,
    ArithmeticManifoldData,
    GaugeConnectionData,
    DijkgraafWittenPartitionData,
)


class TestArithmeticQFTLoom(unittest.TestCase):
    """Test suite for ArithmeticQFTLoom algorithms and visualizers."""

    def setUp(self):
        self.loom = ArithmeticQFTLoom()

    def test_gauge_group_and_manifold_init(self):
        """Verify initialization of finite gauge group and arithmetic 3-manifold."""
        self.assertGreaterEqual(len(self.loom.groups), 1)
        grp = self.loom.groups[0]
        self.assertIsInstance(grp, ArithmeticGaugeGroupData)
        self.assertEqual(grp.group_order, 3)
        self.assertTrue(grp.is_abelian)
        self.assertEqual(grp.cohomology_h3_order, 3)

        self.assertGreaterEqual(len(self.loom.manifolds), 1)
        man = self.loom.manifolds[0]
        self.assertIsInstance(man, ArithmeticManifoldData)
        self.assertEqual(man.discriminant, -4)
        self.assertEqual(man.class_number, 1)
        self.assertIn(2, man.ramified_primes)

    def test_gauge_connections_and_chern_simons(self):
        """Verify Galois representations and arithmetic Chern-Simons invariants."""
        conns = self.loom.evaluate_gauge_connections()
        self.assertGreater(len(conns), 0)
        for conn in conns:
            self.assertIsInstance(conn, GaugeConnectionData)
            self.assertGreaterEqual(conn.chern_simons_invariant, 0.0)
            self.assertLessEqual(conn.chern_simons_invariant, 1.0)
            self.assertGreaterEqual(conn.holonomy_trace, -1.0)
            self.assertLessEqual(conn.holonomy_trace, 1.0)
            self.assertIn("Frob_2", conn.frobenius_images)

    def test_dijkgraaf_witten_partition_function(self):
        """Verify Dijkgraaf-Witten partition function and Wilson loop observables."""
        part = self.loom.compute_dijkgraaf_witten_partition("DW-TEST-01")
        self.assertIsInstance(part, DijkgraafWittenPartitionData)
        self.assertEqual(part.partition_id, "DW-TEST-01")
        self.assertGreater(part.total_gauge_connections, 0)
        self.assertGreaterEqual(part.partition_norm, 0.0)
        self.assertGreater(len(part.wilson_loop_expectations), 0)
        for p_key, val in part.wilson_loop_expectations.items():
            self.assertGreaterEqual(val, 0.0)

    def test_non_abelian_heisenberg_model(self):
        """Verify non-abelian Heisenberg gauge group and class number 2 ring."""
        loom_heis = ArithmeticQFTLoom(
            default_group=ArithmeticGaugeGroupType.HEISENBERG_P.value,
            default_manifold=ArithmeticManifoldType.IMAGINARY_QUADRATIC_D5.value,
            twist_level=2,
        )
        grp = loom_heis.groups[0]
        self.assertFalse(grp.is_abelian)
        self.assertEqual(grp.group_order, 27)

        man = loom_heis.manifolds[0]
        self.assertEqual(man.class_number, 2)
        self.assertEqual(man.discriminant, -20)

        conns = loom_heis.evaluate_gauge_connections()
        self.assertGreater(len(conns), 0)
        part = loom_heis.compute_dijkgraaf_witten_partition()
        self.assertGreater(part.partition_norm, 0.0)

    def test_svg_and_zero_em_dash_compliance(self):
        """Verify SVG generation, JSON telemetry, and zero em dashes across all outputs."""
        self.loom.evaluate_gauge_connections()
        self.loom.compute_dijkgraaf_witten_partition()

        svg = self.loom.generate_aqft_svg()
        self.assertIsInstance(svg, str)
        self.assertTrue(svg.startswith("<svg"))
        self.assertTrue(svg.endswith("</svg>"))
        self.assertIn("Prime Knots Link Complement", svg)
        self.assertIn("Arithmetic Chern-Simons Actions", svg)
        self.assertIn("Dijkgraaf-Witten Partition Z", svg)

        # Strict zero em dash checks
        self.assertNotIn("\u2014", svg)
        self.assertNotIn(chr(8212), svg)

        json_str = self.loom.to_json()
        self.assertNotIn("\u2014", json_str)
        self.assertNotIn(chr(8212), json_str)

        with open("scripts/arithmetic_qft_loom.py", encoding="utf-8") as f:
            src = f.read()
        self.assertNotIn("\u2014", src)
        self.assertNotIn(chr(8212), src)


if __name__ == "__main__":
    unittest.main()
