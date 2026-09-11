"""
Tests for Grothendieck Dessins d'Enfants and Belyi Map Galois Ramification Loom.
Verifies bipartite ribbon graph vertices, monodromy permutations in S_d,
Euler characteristic and genus via Riemann-Hurwitz, Gal(Q-bar/Q) orbits,
and strict zero em dash compliance.
"""

import unittest
from scripts.dessins_enfants_loom import (
    GrothendieckDessinLoom,
    DessinArchetype,
    DessinVertexData,
    MonodromyPermutationData,
    GaloisOrbitData,
)


class TestGrothendieckDessinLoom(unittest.TestCase):
    """Test suite for GrothendieckDessinLoom algorithms and visualizers."""

    def setUp(self):
        self.loom = GrothendieckDessinLoom(
            belyi_degree=4,
            curve_genus=0,
            default_archetype=DessinArchetype.SHABAT_POLYNOMIAL_TREE.value,
        )

    def test_dessin_graph_and_vertices(self):
        """Verify bipartite ribbon graph vertices and valency conservation."""
        self.assertGreaterEqual(len(self.loom.vertices), 4)
        black_verts = [v for v in self.loom.vertices if v.color == "black"]
        white_verts = [v for v in self.loom.vertices if v.color == "white"]

        self.assertEqual(len(black_verts), 2)
        self.assertEqual(len(white_verts), 2)

        # Sum of black vertex valencies equals degree d = 4
        self.assertEqual(sum(v.valency for v in black_verts), 4)
        # Sum of white vertex valencies equals degree d = 4
        self.assertEqual(sum(v.valency for v in white_verts), 4)

    def test_monodromy_permutation_triad(self):
        """Verify cartographic monodromy triad in S_d and genus computation."""
        self.assertGreaterEqual(len(self.loom.monodromy_records), 1)
        mono = self.loom.monodromy_records[0]
        self.assertIsInstance(mono, MonodromyPermutationData)
        self.assertEqual(mono.degree_d, 4)
        self.assertTrue(mono.is_transitive)
        # Euler characteristic chi = 2 + 2 + 2 - 4 = 2 (genus 0)
        self.assertEqual(mono.euler_characteristic, 2)
        self.assertEqual(mono.genus_calculated, 0)
        self.assertEqual(mono.sigma_0_cycles, [[1, 2, 3], [4]])
        self.assertEqual(mono.sigma_1_cycles, [[1, 4], [2, 3]])

    def test_monodromy_evaluation_algorithm(self):
        """Verify dynamic evaluation of sigma_infty and transitivity."""
        res = self.loom.evaluate_monodromy(
            custom_s0=[[1, 2, 3], [4]],
            custom_s1=[[1, 4], [2, 3]],
        )
        self.assertIsInstance(res, MonodromyPermutationData)
        self.assertTrue(res.is_transitive)
        self.assertEqual(res.euler_characteristic, 2)
        self.assertEqual(res.genus_calculated, 0)
        # Cycle lengths of sigma_infty: [3, 1]
        cycle_lens = sorted([len(c) for c in res.sigma_infty_cycles], reverse=True)
        self.assertEqual(cycle_lens, [3, 1])

    def test_galois_orbit_and_conjugation(self):
        """Verify Gal(Q-bar/Q) orbit and conjugation of Shabat tree."""
        self.assertGreaterEqual(len(self.loom.galois_orbits), 1)
        orb = self.loom.galois_orbits[0]
        self.assertIsInstance(orb, GaloisOrbitData)
        self.assertEqual(orb.orbit_id, "ORBIT-SHABAT-DEG4")
        self.assertEqual(orb.field_discriminant, 5)
        self.assertEqual(orb.galois_orbit_size, 2)
        self.assertTrue(orb.is_galois_faithful)
        self.assertIn("Q(sqrt(5))", orb.moduli_field)

        conj = self.loom.compute_galois_conjugation("ORBIT-CONJ-TEST")
        self.assertIsInstance(conj, GaloisOrbitData)
        self.assertEqual(conj.orbit_id, "ORBIT-CONJ-TEST")
        self.assertEqual(conj.field_discriminant, 5)
        self.assertEqual(len(self.loom.galois_orbits), 2)

    def test_svg_and_zero_em_dash_compliance(self):
        """Verify dark titanium SVG rendering, JSON telemetry, and zero em dashes."""
        self.loom.compute_galois_conjugation()

        svg = self.loom.generate_dessin_svg()
        self.assertIsInstance(svg, str)
        self.assertTrue(svg.startswith("<svg"))
        self.assertTrue(svg.endswith("</svg>"))
        self.assertIn("Grothendieck Dessins d'Enfants", svg)
        self.assertIn("Bipartite Ribbon Graph Dessin", svg)
        self.assertIn("Cartographic Monodromy Triad", svg)
        self.assertIn("Absolute Galois Action", svg)

        # Strict zero em dash verification
        self.assertNotIn("\u2014", svg)
        self.assertNotIn(chr(8212), svg)

        json_str = self.loom.to_json()
        self.assertNotIn("\u2014", json_str)
        self.assertNotIn(chr(8212), json_str)

        with open("scripts/dessins_enfants_loom.py", encoding="utf-8") as f:
            src = f.read()
        self.assertNotIn("\u2014", src)
        self.assertNotIn(chr(8212), src)


if __name__ == "__main__":
    unittest.main()
