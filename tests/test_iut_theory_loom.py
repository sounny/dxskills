"""
Unit tests for Inter-Universal Teichmuller Theory & Mochizuki Hodge Theatre Loom.
Strictly verifies zero em dashes (chr(8212)), Hodge theatres,
theta-link packet deformations, multiradial envelopes, and Szpiro height bounds.
"""

import unittest
import os
import json
from scripts.iut_theory_loom import (
    IUTTheoryLoom,
    HodgeTheatreArchetype,
    IUTLinkType,
)


class TestIUTTheoryLoom(unittest.TestCase):
    """Test suite for IUTTheoryLoom engine and spatial cognitive mappings."""

    def setUp(self):
        self.loom = IUTTheoryLoom(
            base_prime_l=5,
            base_q_parameter=0.05,
        )

    def test_hodge_theatre_initialization(self):
        """Verify default Hodge theatres and capsule size l* = (l - 1) / 2."""
        self.assertEqual(len(self.loom.hodge_theatres), 2)
        ht0 = self.loom.hodge_theatres[0]
        self.assertEqual(ht0.theatre_id, "HT-0-0")
        self.assertEqual(ht0.prime_l, 5)
        self.assertEqual(ht0.capsule_size, 2)  # (5 - 1) // 2 = 2
        self.assertIn("Frobenioid-like", ht0.frobenius_like_status)
        self.assertIn("Etale-like", ht0.etale_like_rigid_status)

        # Theatre with prime l = 7 (capsule size 3)
        ht_l7 = self.loom.construct_hodge_theatre(
            theatre_id="HT-L7",
            log_coord_n=1,
            theta_coord_m=1,
            prime_l=7,
            q_parameter=0.01,
        )
        self.assertEqual(ht_l7.capsule_size, 3)

    def test_theta_link_evaluation(self):
        """Verify theta packet values q^{j^2} and broken ring structure across theatres."""
        lnk = self.loom.evaluate_theta_link(
            link_id="LINK-THETA-01",
            source_theatre_id="HT-0-0",
            target_theatre_id="HT-0-1",
        )
        self.assertEqual(len(lnk.theta_packet_values), 2)
        # q = 0.05: j=1 => 0.05^1 = 0.05, j=2 => 0.05^4 = 0.00000625
        self.assertAlmostEqual(lnk.theta_packet_values[0], 0.05)
        self.assertAlmostEqual(lnk.theta_packet_values[1], 0.05 ** 4)
        self.assertTrue(lnk.ring_axiom_broken)
        self.assertTrue(lnk.anabelian_invariance_certified)

    def test_multiradial_envelope_indeterminacies(self):
        """Verify 3-fold indeterminacies (Indet 1, 2, 3) and Szpiro height bounds."""
        env = self.loom.evaluate_multiradial_envelope("ENV-01", epsilon=0.1)
        self.assertGreater(env.indet_1_automorphism_volume, 0.0)
        self.assertGreater(env.indet_2_kummer_phase_volume, 0.0)
        self.assertGreater(env.indet_3_upper_bound_volume, 0.0)
        self.assertGreater(env.total_log_volume_bound, 0.0)
        self.assertGreater(env.canonical_height_bound, 0.0)
        self.assertTrue(env.szpiro_inequality_satisfied)

    def test_log_theta_lattice_navigation(self):
        """Verify populating the 2D log-theta lattice in Z x Z."""
        self.loom.construct_hodge_theatre("HT-1-0", log_coord_n=1, theta_coord_m=0, prime_l=5)
        self.loom.construct_hodge_theatre("HT-1-1", log_coord_n=1, theta_coord_m=1, prime_l=5)
        theatre_ids = [h.theatre_id for h in self.loom.hodge_theatres]
        self.assertIn("HT-1-0", theatre_ids)
        self.assertIn("HT-1-1", theatre_ids)

    def test_svg_json_and_zero_em_dashes(self):
        """Verify SVG generation, JSON export, and strict zero em dash compliance."""
        self.loom.evaluate_theta_link("LINK-TEST", "HT-0-0", "HT-0-1")
        self.loom.evaluate_multiradial_envelope("ENV-TEST")

        svg = self.loom.generate_iut_svg()
        self.assertTrue(svg.startswith("<svg"))
        self.assertTrue(svg.endswith("</svg>"))
        self.assertIn("Inter-Universal Teichmuller", svg)
        self.assertIn("Hodge Theatre", svg)
        self.assertIn("Theta-Link", svg)
        self.assertIn("Multiradial", svg)

        # Assert ZERO em dashes anywhere in generated SVG
        self.assertNotIn(chr(8212), svg)

        # Assert ZERO em dashes in JSON export
        json_data = self.loom.to_json()
        self.assertNotIn(chr(8212), json_data)

        # Verify source file has zero em dashes
        loom_path = os.path.join(os.path.dirname(__file__), "..", "scripts", "iut_theory_loom.py")
        if os.path.exists(loom_path):
            with open(loom_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertNotIn(chr(8212), content)


if __name__ == "__main__":
    unittest.main()
