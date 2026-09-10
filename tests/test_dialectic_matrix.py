#!/usr/bin/env python3
"""
Unit tests for Autonomous Cognitive Multi-Perspective Thesis Dialectic Matrix & Consensus Engine
Part of the DxSkills Cognitive Architecture Suite (https://dxskills.sounny.com)
"""

import os
import json
import unittest

from scripts.dialectic_matrix import (
    tokenize,
    Perspective,
    DialecticTension,
    DialecticSynthesis,
    DialecticMatrixResult,
    DialecticMatrixEngine
)


class TestDialecticMatrixEngine(unittest.TestCase):
    """Tests for perspective decomposition, false divergence detection, and synthesis canvas export."""

    def setUp(self):
        self.engine = DialecticMatrixEngine()

    def test_tokenize(self):
        tokens = tokenize("The architecture must prioritize rapid velocity and low latency throughput.")
        self.assertIn("architecture", tokens)
        self.assertIn("velocity", tokens)
        self.assertIn("latency", tokens)
        self.assertNotIn("the", tokens)
        self.assertNotIn("and", tokens)

    def test_add_perspective(self):
        p = self.engine.add_perspective(
            "Engineering",
            "We must achieve high throughput and low latency. Distributed scaling is vital for our cluster. Correctness cannot be sacrificed."
        )
        self.assertEqual(p.name, "Engineering")
        self.assertGreaterEqual(len(p.key_claims), 2)
        self.assertTrue(any("latency" in c.lower() or "throughput" in c.lower() for c in p.key_claims))

    def test_false_divergence_detection(self):
        # Both perspectives want speed/performance but use different terms (velocity vs throughput vs fast)
        self.engine.add_perspective(
            "ProductLead",
            "Our primary objective is rapid feature velocity and fast delivery to market. We need rapid iterations."
        )
        self.engine.add_perspective(
            "BackendArchitect",
            "Our infrastructure requires high throughput and low latency. Performance benchmarks must be prioritized."
        )

        result = self.engine.analyze_dialectic()
        self.assertGreaterEqual(len(result.tensions), 1)

        # Check that false divergence was detected due to shared conceptual cluster (Speed)
        first_tension = result.tensions[0]
        self.assertTrue(first_tension.is_false_divergence)
        self.assertEqual(first_tension.shared_concept, "Speed")
        self.assertGreaterEqual(result.consensus_readiness_index, 60.0)

    def test_structural_polarity_and_synthesis(self):
        self.engine.add_perspective(
            "SecurityAuditor",
            "All endpoints must undergo mandatory multi-factor authentication, air-gapped network isolation, and rigorous compliance checks."
        )
        self.engine.add_perspective(
            "GrowthMarketer",
            "User onboarding must remain frictionless with zero-click signups, social auth, and minimal barrier to entry."
        )

        result = self.engine.analyze_dialectic()
        self.assertEqual(len(result.syntheses), len(result.tensions))

        # Check synthesis properties
        synth = result.syntheses[0]
        self.assertIn("Layered", synth.title)
        self.assertGreater(synth.consensus_score, 50.0)

    def test_canvas_export(self):
        self.engine.add_perspective("Reviewer1", "The methodology needs more theoretical rigor and extensive proofs.")
        self.engine.add_perspective("Reviewer2", "The practical application is novel and ready for immediate deployment.")

        result = self.engine.analyze_dialectic()
        canvas_data = self.engine.export_canvas(result)

        self.assertIn("nodes", canvas_data)
        self.assertIn("edges", canvas_data)
        self.assertGreaterEqual(len(canvas_data["nodes"]), 5)  # 3 headers + 2 claims + 1 synthesis
        self.assertGreaterEqual(len(canvas_data["edges"]), 2)

    def test_svg_and_summary_export(self):
        self.engine.add_perspective("TeamA", "Focus on simplicity and minimalism.")
        self.engine.add_perspective("TeamB", "Focus on completeness and comprehensive features.")

        result = self.engine.analyze_dialectic()
        svg = self.engine.export_svg(result)
        self.assertTrue(svg.startswith("<svg"))
        self.assertTrue(svg.endswith("</svg>"))
        self.assertIn("Multi-Perspective Dialectic Consensus Matrix", svg)

        summary = DialecticMatrixEngine.export_summary(result)
        self.assertIn("# Multi-Perspective Dialectic Consensus Matrix", summary)
        self.assertIn("Consensus Readiness Index", summary)

    def test_zero_em_dashes(self):
        import inspect
        import scripts.dialectic_matrix as dm
        source = inspect.getsource(dm)
        self.assertNotIn(chr(8212), source, "Illegal em dash found in scripts/dialectic_matrix.py")


if __name__ == "__main__":
    unittest.main()
