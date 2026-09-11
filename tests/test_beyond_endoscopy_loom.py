r"""
Unit tests for Beyond Endoscopy & Langlands Functoriality Loom.
Verifies dual group representations, spectral L-pole residue isolation,
Poisson summation harmonic cancellation, and strict zero em dash compliance.
"""

import unittest
import math
import os
import sys

# Ensure scripts dir is accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))
from beyond_endoscopy_loom import (
    BeyondEndoscopyLoom,
    BeyondEndoscopyArchetype,
    DualRepresentationData,
    LPoleSpectralFilter,
    PoissonGeometricSum,
    AltugSmoothedKernel,
    BeyondEndoscopyEvaluation,
)


class TestBeyondEndoscopyLoom(unittest.TestCase):
    """Test suite for BeyondEndoscopyLoom."""

    def setUp(self):
        self.loom = BeyondEndoscopyLoom(
            test_energy_parameter=1.0,
            smoothing_epsilon=0.05,
            default_archetype=BeyondEndoscopyArchetype.GL2_SYMMETRIC_SQUARE.value,
        )

    def test_dual_representation_initialization(self):
        """Verify dual group representation r and functorial target."""
        dr = self.loom.dual_rep
        self.assertIsNotNone(dr)
        self.assertIn("GL(2, C)", dr.dual_group_label)
        self.assertIn("Sym^2", dr.representation_r_label)
        self.assertEqual(dr.representation_dimension, 3)
        self.assertTrue(dr.is_self_dual)
        self.assertIn("GL(3)", dr.functorial_target_group)

    def test_spectral_pole_residue_isolation(self):
        """Verify isolation of functorial forms via pole residues at s = 1."""
        filters = self.loom.spectral_filters
        self.assertGreaterEqual(len(filters), 3)

        # Trivial representation has pole residue 1.0
        f_triv = filters[0]
        self.assertTrue(f_triv.is_functorial_image)
        self.assertEqual(f_triv.pole_residue_at_s1, 1.0)

        # Monomial/dihedral representation has positive residue
        f_dih = filters[1]
        self.assertTrue(f_dih.is_functorial_image)
        self.assertGreater(f_dih.pole_residue_at_s1, 0.0)

        # Generic non-dihedral cuspidal form has no pole at s = 1
        f_gen = filters[2]
        self.assertFalse(f_gen.is_functorial_image)
        self.assertEqual(f_gen.pole_residue_at_s1, 0.0)

    def test_poisson_geometric_harmonics_and_cancellation(self):
        """Verify Poisson summation harmonic cancellation on non-trivial orbits."""
        harmonics = self.loom.poisson_harmonics
        self.assertGreaterEqual(len(harmonics), 3)

        h0 = harmonics[0]
        self.assertTrue(h0.is_trivial_orbit)
        self.assertEqual(h0.destructive_phase_cancellation, 1.0)

        # Oscillatory modes have strong phase cancellation
        for h in harmonics[1:]:
            self.assertFalse(h.is_trivial_orbit)
            self.assertLess(h.destructive_phase_cancellation, 0.2)

        eval_res = self.loom.evaluate_beyond_endoscopy()
        self.assertTrue(eval_res.functorial_lift_isolated)
        self.assertGreater(eval_res.cancellation_efficiency_ratio, 0.85)

    def test_archetype_switching(self):
        """Verify archetype switching for Rankin-Selberg and Adjoint lifts."""
        rankin_loom = BeyondEndoscopyLoom(
            default_archetype=BeyondEndoscopyArchetype.GL2_TIMES_GL2_RANKIN.value,
        )
        self.assertEqual(rankin_loom.dual_rep.representation_dimension, 4)
        self.assertIn("GL(4)", rankin_loom.dual_rep.functorial_target_group)

        adjoint_loom = BeyondEndoscopyLoom(
            default_archetype=BeyondEndoscopyArchetype.GL3_ADJOINT_OCTET.value,
        )
        self.assertEqual(adjoint_loom.dual_rep.representation_dimension, 8)
        self.assertIn("GL(8)", adjoint_loom.dual_rep.functorial_target_group)

    def test_svg_generation_and_zero_em_dashes(self):
        """Verify dark titanium SVG generation and strict zero em dash compliance."""
        svg = self.loom.generate_svg()
        self.assertIn("<svg", svg)
        self.assertIn("Beyond Endoscopy", svg)
        self.assertIn("Poisson Summation", svg)
        self.assertIn("L-Pole Filter", svg)

        # Verify zero em dashes across both test and engine scripts
        cur_file = __file__
        loom_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts", "beyond_endoscopy_loom.py"))
        for fpath in [cur_file, loom_file]:
            if os.path.exists(fpath):
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()
                self.assertNotIn("\u2014", content, f"Em dash found in {fpath}")


if __name__ == "__main__":
    unittest.main()
