r"""
Unit tests for Arthur-Selberg Trace Formula & Endoscopic Classification Loom.
Verifies invariant trace formula evaluation, endoscopic groups, Arthur packets,
multiplicity formulas in discrete spectrum, and strict zero em dash compliance.
"""

import unittest
import math
import os
import sys

# Ensure scripts dir is accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))
from arthur_trace_loom import (
    ArthurSelbergTraceLoom,
    ArthurGroupArchetype,
    EndoscopicGroupData,
    ArthurParameterData,
    ArthurPacketRepresentation,
    TraceFormulaEvaluation,
)


class TestArthurTraceLoom(unittest.TestCase):
    """Test suite for ArthurSelbergTraceLoom."""

    def setUp(self):
        self.loom = ArthurSelbergTraceLoom(
            test_function_cutoff=2.5,
            spectral_truncation_level=4,
            default_archetype=ArthurGroupArchetype.SO5_SPLIT.value,
        )

    def test_endoscopic_groups_initialization(self):
        """Verify endoscopic groups and transfer coefficients for SO(5)."""
        groups = self.loom.endoscopic_groups
        self.assertGreaterEqual(len(groups), 2)

        g0 = groups[0]
        self.assertIn("SO_5", g0.group_h_label)
        self.assertEqual(g0.tamagawa_iota_coefficient, 1.0)
        self.assertEqual(g0.transfer_factor_sign, 1)
        self.assertTrue(g0.is_quasi_split)

        h1 = groups[1]
        self.assertIn("SO_3 x SO_3", h1.group_h_label)
        self.assertEqual(h1.tamagawa_iota_coefficient, 0.5)
        self.assertEqual(h1.transfer_factor_sign, -1)

    def test_arthur_parameter_and_packet_multiplicities(self):
        """Verify Arthur parameter and A-packet discrete spectrum multiplicities."""
        param = self.loom.arthur_parameter
        self.assertIsNotNone(param)
        self.assertEqual(param.dual_group_label, "Sp_4(C)")
        self.assertEqual(param.component_group_order, 4)
        self.assertFalse(param.is_tempered)

        packet = self.loom.arthur_packet
        self.assertEqual(len(packet), 4)

        # Multiplicities must be 0 or 1
        multiplicities = [p.multiplicity_in_discrete_spectrum for p in packet]
        for m in multiplicities:
            self.assertIn(m, [0, 1])

        # At least one representation has non-zero multiplicity
        self.assertGreater(sum(multiplicities), 0)

    def test_orbital_and_spectral_balance(self):
        """Verify trace formula geometric and spectral evaluation."""
        eval_res = self.loom.evaluate_trace_formula()
        self.assertGreater(eval_res.geometric_total, 0.0)
        self.assertGreater(eval_res.spectral_total, 0.0)
        self.assertLess(eval_res.trace_identity_residual, 0.25)
        self.assertTrue(eval_res.is_stabilized)
        self.assertGreater(eval_res.cognitive_resonance_score, 0.8)
        self.assertEqual(eval_res.spatial_stability_index, 0.95)

    def test_archetype_switching(self):
        """Verify group archetypes SP4, SO7, and GL4."""
        # Test Sp(4)
        sp4_loom = ArthurSelbergTraceLoom(
            test_function_cutoff=2.0,
            default_archetype=ArthurGroupArchetype.SP4_SPLIT.value,
        )
        self.assertEqual(sp4_loom.arthur_parameter.dual_group_label, "SO_5(C)")
        self.assertTrue(sp4_loom.arthur_parameter.is_tempered)

        # Test GL(4)
        gl4_loom = ArthurSelbergTraceLoom(
            test_function_cutoff=2.0,
            default_archetype=ArthurGroupArchetype.GL4_STANDARD.value,
        )
        self.assertEqual(len(gl4_loom.endoscopic_groups), 1)
        self.assertIn("GL_4", gl4_loom.endoscopic_groups[0].group_h_label)
        self.assertEqual(len(gl4_loom.arthur_packet), 1)

    def test_svg_generation_and_zero_em_dashes(self):
        """Verify dark titanium SVG generation and strict zero em dash compliance."""
        svg = self.loom.generate_svg()
        self.assertIn("<svg", svg)
        self.assertIn("Arthur-Selberg Trace Formula", svg)
        self.assertIn("Geometric Side", svg)
        self.assertIn("Spectral Side", svg)
        self.assertIn("Endoscopic Aperture", svg)

        # Verify zero em dashes across both test and engine scripts
        cur_file = __file__
        loom_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts", "arthur_trace_loom.py"))
        for fpath in [cur_file, loom_file]:
            if os.path.exists(fpath):
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()
                self.assertNotIn("\u2014", content, f"Em dash found in {fpath}")


if __name__ == "__main__":
    unittest.main()
