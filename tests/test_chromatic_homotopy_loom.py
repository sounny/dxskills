"""
Tests for Chromatic Homotopy Theory and Morava K-Theory Loom.
Verifies formal group laws of height n, generator degrees |v_n| = 2(p^n - 1),
Morava K-theory spectrum properties, Morava stabilizer groups S_n,
chromatic fracture square and convergence tower, and strict zero em dash compliance.
"""

import unittest
from scripts.chromatic_homotopy_loom import (
    ChromaticHomotopyLoom,
    ChromaticHeightArchetype,
    FormalGroupLawData,
    MoravaKTheoryData,
    MoravaStabilizerData,
    ChromaticTowerData,
)


class TestChromaticHomotopyLoom(unittest.TestCase):
    """Test suite for ChromaticHomotopyLoom algorithms and visualizers."""

    def setUp(self):
        self.loom = ChromaticHomotopyLoom(base_prime_p=3, chromatic_height=2)

    def test_formal_group_law_and_generator_degrees(self):
        """Verify 1D formal group law properties and generator degrees."""
        self.assertGreaterEqual(len(self.loom.formal_groups), 1)
        fgl = self.loom.formal_groups[0]
        self.assertIsInstance(fgl, FormalGroupLawData)
        self.assertEqual(fgl.height_n, 2)
        self.assertEqual(fgl.base_prime_p, 3)
        # Degree |v_2| = 2 * (3^2 - 1) = 16
        self.assertEqual(fgl.v_n_degree, 16)
        self.assertEqual(fgl.lubin_tate_parameters_count, 1)  # n - 1 = 1
        self.assertIn("v_2", fgl.p_series_expansion)

    def test_morava_k_theory_properties(self):
        """Verify Morava K-theory spectrum K(n) algebraic invariants."""
        self.assertGreaterEqual(len(self.loom.k_theories), 1)
        kt = self.loom.k_theories[0]
        self.assertIsInstance(kt, MoravaKTheoryData)
        self.assertEqual(kt.theory_id, "K(2)-PRIME-3")
        self.assertEqual(kt.height_n, 2)
        self.assertEqual(kt.base_prime_p, 3)
        self.assertEqual(kt.periodicity, 16)
        self.assertTrue(kt.is_field_spectrum)
        self.assertEqual(kt.nilpotence_exponent, 1)

    def test_morava_stabilizer_group(self):
        """Verify Morava stabilizer group division algebra invariants."""
        self.assertGreaterEqual(len(self.loom.stabilizer_groups), 1)
        stab = self.loom.stabilizer_groups[0]
        self.assertIsInstance(stab, MoravaStabilizerData)
        self.assertEqual(stab.height_n, 2)
        # Division algebra dimension n^2 = 4
        self.assertEqual(stab.division_algebra_dim, 4)
        self.assertEqual(stab.invariant_rational, "1/2")
        self.assertTrue(stab.has_finite_subgroups)
        self.assertEqual(stab.maximal_finite_subgroup_order, 16)  # 2 * (3^2 - 1) = 16

    def test_chromatic_tower_evaluation(self):
        """Verify chromatic convergence tower and Bousfield localizations."""
        tow = self.loom.evaluate_chromatic_tower("TOWER-TEST-01")
        self.assertIsInstance(tow, ChromaticTowerData)
        self.assertEqual(tow.tower_id, "TOWER-TEST-01")
        self.assertEqual(tow.max_height, 2)
        self.assertEqual(len(tow.bousfield_classes), 3)  # L_0, L_1, L_2
        self.assertEqual(len(tow.monochromatic_layers), 3)
        self.assertTrue(tow.convergence_verified)
        self.assertIn("alpha_1", tow.adams_novikov_e2_sample)
        self.assertIn("beta_1", tow.adams_novikov_e2_sample)

    def test_svg_and_zero_em_dash_compliance(self):
        """Verify dark titanium SVG rendering, JSON telemetry, and zero em dashes."""
        self.loom.evaluate_chromatic_tower()

        svg = self.loom.generate_chromatic_svg()
        self.assertIsInstance(svg, str)
        self.assertTrue(svg.startswith("<svg"))
        self.assertTrue(svg.endswith("</svg>"))
        self.assertIn("Chromatic Homotopy Theory and Morava K-Theory Loom", svg)
        self.assertIn("Chromatic Height Ladder", svg)
        self.assertIn("Chromatic Fracture Square", svg)
        self.assertIn("Morava Stabilizer Group S_n", svg)

        # Strict zero em dash verification
        self.assertNotIn("\u2014", svg)
        self.assertNotIn(chr(8212), svg)

        json_str = self.loom.to_json()
        self.assertNotIn("\u2014", json_str)
        self.assertNotIn(chr(8212), json_str)

        with open("scripts/chromatic_homotopy_loom.py", encoding="utf-8") as f:
            src = f.read()
        self.assertNotIn("\u2014", src)
        self.assertNotIn(chr(8212), src)


if __name__ == "__main__":
    unittest.main()
