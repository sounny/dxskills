"""
Tests for p-Adic Hodge Theory and Fontaine Period Rings Loom.
Verifies period rings B_cris, B_st, B_dR, B_HT, filtered (phi, N)-modules,
Newton-Hodge polygons, weak admissibility, and strict zero em dash compliance.
"""

import unittest
from scripts.padic_hodge_loom import (
    PAdicHodgeLoom,
    FontaineRingType,
    ReductionArchetype,
    FontaineRingData,
    FilteredPhiNModuleData,
    NewtonHodgePolygonData,
    PAdicRepresentationData,
)


class TestPAdicHodgeLoom(unittest.TestCase):
    """Test suite for PAdicHodgeLoom algorithms and visualizers."""

    def setUp(self):
        self.loom = PAdicHodgeLoom()

    def test_fontaine_rings_initialization(self):
        """Verify initialization and structure of the 4 Fontaine period rings."""
        self.assertEqual(len(self.loom.rings), 4)
        ring_map = {r.ring_type: r for r in self.loom.rings}

        # B_cris
        b_cris = ring_map[FontaineRingType.B_CRIS.value]
        self.assertTrue(b_cris.has_frobenius_phi)
        self.assertFalse(b_cris.has_monodromy_n)
        self.assertTrue(b_cris.has_hodge_filtration)

        # B_st
        b_st = ring_map[FontaineRingType.B_ST.value]
        self.assertTrue(b_st.has_frobenius_phi)
        self.assertTrue(b_st.has_monodromy_n)

        # B_dR
        b_dr = ring_map[FontaineRingType.B_DR.value]
        self.assertFalse(b_dr.has_frobenius_phi)
        self.assertTrue(b_dr.has_hodge_filtration)

        # B_HT
        b_ht = ring_map[FontaineRingType.B_HT.value]
        self.assertFalse(b_ht.has_hodge_filtration)

    def test_filtered_module_evaluation(self):
        """Verify evaluation of filtered (phi, N)-module D_st(V)."""
        mod = self.loom.evaluate_filtered_module("MOD-TEST-01")
        self.assertIsInstance(mod, FilteredPhiNModuleData)
        self.assertEqual(mod.dimension, 2)
        self.assertEqual(mod.base_prime_p, 5)
        self.assertEqual(len(mod.frobenius_slopes), 2)
        self.assertEqual(mod.monodromy_nilpotency_order, 1)  # Crystalline -> N = 0
        self.assertTrue(mod.is_weakly_admissible)

    def test_newton_hodge_polygons(self):
        """Verify Newton and Hodge polygon construction and weak admissibility."""
        poly = self.loom.compute_newton_hodge_polygons("POLY-TEST-01")
        self.assertIsInstance(poly, NewtonHodgePolygonData)
        self.assertTrue(poly.endpoints_match)
        self.assertTrue(poly.newton_above_hodge)
        self.assertEqual(len(poly.hodge_vertices), 3)  # (0,0), (1,0), (2,1)
        self.assertEqual(len(poly.newton_vertices), 3)

    def test_semistable_reduction_archetype(self):
        """Verify semistable non-crystalline representation with monodromy N != 0."""
        loom_st = PAdicHodgeLoom(
            base_prime_p=7,
            default_archetype=ReductionArchetype.SEMISTABLE_NON_CRYSTALLINE.value,
            dimension=2,
        )
        rep = loom_st.representations[0]
        self.assertFalse(rep.is_crystalline)
        self.assertTrue(rep.is_semistable)
        self.assertTrue(rep.is_de_rham)

        mod = loom_st.evaluate_filtered_module("MOD-ST")
        self.assertEqual(mod.monodromy_nilpotency_order, 2)  # N != 0, N^2 = 0

        poly = loom_st.compute_newton_hodge_polygons("POLY-ST")
        self.assertTrue(poly.endpoints_match)
        self.assertTrue(poly.newton_above_hodge)

    def test_svg_and_zero_em_dash_compliance(self):
        """Verify SVG rendering, JSON telemetry, and zero em dashes across all outputs."""
        self.loom.evaluate_filtered_module()
        self.loom.compute_newton_hodge_polygons()

        svg = self.loom.generate_padic_svg()
        self.assertIsInstance(svg, str)
        self.assertTrue(svg.startswith("<svg"))
        self.assertTrue(svg.endswith("</svg>"))
        self.assertIn("Fontaine Rings Inclusion Tower", svg)
        self.assertIn("Newton-Hodge Polygon Duality", svg)
        self.assertIn("Filtered (phi, N)-Module", svg)

        # Strict zero em dash verification
        self.assertNotIn("\u2014", svg)
        self.assertNotIn(chr(8212), svg)

        json_str = self.loom.to_json()
        self.assertNotIn("\u2014", json_str)
        self.assertNotIn(chr(8212), json_str)

        with open("scripts/padic_hodge_loom.py", encoding="utf-8") as f:
            src = f.read()
        self.assertNotIn("\u2014", src)
        self.assertNotIn(chr(8212), src)


if __name__ == "__main__":
    unittest.main()
