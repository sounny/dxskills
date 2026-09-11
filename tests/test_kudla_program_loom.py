r"""
Unit tests for Kudla Program Arithmetic Intersection Loom.
Verifies orthogonal Shimura datum, arithmetic special cycles Z_hat(T, v),
Kudla-Rapoport intersection multiplicities, Eisenstein derivative generating series,
and strict zero em dash compliance.
"""

import unittest
import os
import sys

# Ensure scripts dir is accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))
from kudla_program_loom import (
    KudlaProgramLoom,
    KudlaArchetype,
    OrthogonalShimuraDatum,
    SpecialCycleData,
    GreenFunctionData,
    KudlaRapoportIntersectionData,
    EisensteinDerivativeData,
)


class TestKudlaProgramLoom(unittest.TestCase):
    """Test suite for KudlaProgramLoom."""

    def setUp(self):
        self.loom = KudlaProgramLoom(
            signature=(3, 2),
            prime_p=5,
            default_archetype=KudlaArchetype.SO3_2_SIEGEL_SURFACE.value,
        )

    def test_shimura_datum_initialization(self):
        """Verify orthogonal Shimura datum configuration."""
        datum = self.loom.shimura_datum
        self.assertEqual(datum.signature, (3, 2))
        self.assertEqual(datum.dimension_v, 5)
        self.assertEqual(datum.lattice_discriminant, 4)
        self.assertEqual(datum.reflex_field, "Q")
        self.assertIn("D =", datum.symmetric_domain_label)

    def test_special_cycles_and_green_functions(self):
        """Verify arithmetic special cycle generation and Kudla-Green functions."""
        cycles = self.loom.special_cycles
        self.assertEqual(len(cycles), 4)

        c1 = cycles[0]
        self.assertEqual(c1.norm_t, 1)
        self.assertEqual(c1.codimension, 1)
        self.assertGreater(c1.geometric_degree, 0.0)
        self.assertGreater(c1.arithmetic_degree, c1.geometric_degree * 0.5)

        gf = self.loom.compute_green_function(norm_t=1, v=1.0)
        self.assertEqual(gf.parameter_v, 1.0)
        self.assertGreater(gf.log_singularity_coefficient, 0.0)
        self.assertGreater(gf.regularized_integral, 0.0)

    def test_kudla_rapoport_local_and_total_intersections(self):
        """Verify local Kudla-Rapoport multiplicities and total arithmetic intersection pairing."""
        # Local intersection at prime 2 with norm 1 and 2 (det = 2)
        loc = self.loom.compute_local_intersection(prime=2, norm_t1=1, norm_t2=2)
        self.assertEqual(loc.prime_p, 2)
        self.assertEqual(loc.fundamental_matrix_det, 2)
        self.assertEqual(loc.gross_keating_invariant, 1)
        self.assertGreater(loc.local_intersection_multiplicity, 0.0)

        # Total intersection decomposition
        total = self.loom.compute_total_arithmetic_intersection(1, 2)
        self.assertIn("local_intersections", total)
        self.assertGreater(total["finite_places_sum"], 0.0)
        self.assertGreater(total["archimedean_star_product"], 0.0)
        self.assertAlmostEqual(
            total["total_arithmetic_pairing"],
            round(total["finite_places_sum"] + total["archimedean_star_product"], 4),
            places=4,
        )

    def test_eisenstein_derivative_generating_series(self):
        """Verify central derivative of incoherent Eisenstein series matches arithmetic degrees."""
        eis = self.loom.eisenstein_series
        self.assertEqual(eis.weight_k, 2.5)  # 1 + 3/2 = 2.5
        self.assertTrue(eis.kudla_conjecture_verified)

        # Confirm coefficient a'_n equals arithmetic degree of Z_hat(n)
        for cycle in self.loom.special_cycles:
            n = cycle.norm_t
            self.assertEqual(eis.derivative_coefficients[n], cycle.arithmetic_degree)

    def test_svg_generation_and_zero_em_dashes(self):
        """Verify dark titanium SVG generation and strict zero em dash compliance."""
        svg = self.loom.generate_svg()
        self.assertIn("<svg", svg)
        self.assertIn("Kudla Program Arithmetic Intersection Loom", svg)
        self.assertIn("Sh(V)", svg)
        self.assertIn("CH^1(M)_hat", svg)

        # Verify zero em dashes across both test and engine scripts
        cur_file = __file__
        loom_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts", "kudla_program_loom.py"))
        for fpath in [cur_file, loom_file]:
            if os.path.exists(fpath):
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()
                self.assertNotIn("\u2014", content, f"Em dash found in {fpath}")


if __name__ == "__main__":
    unittest.main()
