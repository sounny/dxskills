#!/usr/bin/env python3
"""
Unit tests for Autonomous Cognitive Visual Typography Kerning & Lexical Anchor Balancer
Part of the DxSkills Cognitive Architecture Suite (https://dxskills.sounny.com)
"""

import os
import json
import unittest

from scripts.typography_balancer import (
    count_syllables,
    split_syllables_heuristic,
    anchor_word_bionic,
    anchor_word_syllables,
    TypographyAudit,
    VisualTypographyBalancer
)


class TestVisualTypographyBalancer(unittest.TestCase):
    """Tests for syllable counting, bionic root bolding, audit metrics, and canvas transformation."""

    def setUp(self):
        self.balancer = VisualTypographyBalancer()

    def test_count_syllables(self):
        self.assertEqual(count_syllables(""), 0)
        self.assertEqual(count_syllables("cat"), 1)
        self.assertEqual(count_syllables("code"), 1)
        self.assertEqual(count_syllables("simple"), 2)
        self.assertEqual(count_syllables("typography"), 4)
        self.assertGreaterEqual(count_syllables("electromagnetism"), 5)

    def test_split_syllables_heuristic(self):
        short = split_syllables_heuristic("fast")
        self.assertEqual(short, ["fast"])

        prefixed = split_syllables_heuristic("deconstruct")
        self.assertGreaterEqual(len(prefixed), 2)
        self.assertEqual(prefixed[0].lower(), "de")

        suffixed = split_syllables_heuristic("playful")
        self.assertGreaterEqual(len(suffixed), 2)
        self.assertEqual(suffixed[-1].lower(), "ful")

        multi = split_syllables_heuristic("development")
        self.assertEqual(multi, ["de", "velop", "ment"])

    def test_anchor_word_bionic(self):
        # 1-2 chars
        self.assertEqual(anchor_word_bionic("in"), "**i**n")
        # 3-4 chars
        self.assertEqual(anchor_word_bionic("code"), "**co**de")
        # 5-7 chars
        self.assertEqual(anchor_word_bionic("system"), "**sys**tem")
        # 8+ chars
        anchored = anchor_word_bionic("architecture")
        self.assertTrue(anchored.startswith("**"))
        self.assertIn("**", anchored[2:])

        # Word with punctuation
        punct = anchor_word_bionic("(test)!")
        self.assertTrue(punct.startswith("(**"))
        self.assertTrue(punct.endswith(")!"))

    def test_anchor_word_syllables(self):
        syll_word = anchor_word_syllables("interaction")
        self.assertIn("\u00B7", syll_word)

    def test_audit_text_empty(self):
        audit = self.balancer.audit_text("")
        self.assertEqual(audit.total_words, 0)
        self.assertEqual(audit.wpm_boost_pct, 0.0)

    def test_audit_text_dense(self):
        dense_text = (
            "Hyperdimensional vector architectures deconstruct monolithic infrastructure "
            "into asynchronous micro-services with deterministic telemetric observability."
        )
        audit = self.balancer.audit_text(dense_text)
        self.assertGreater(audit.total_words, 5)
        self.assertGreater(audit.complex_words_count, 3)
        self.assertGreater(audit.lexical_friction_index, 30.0)
        self.assertGreater(audit.estimated_anchored_wpm, audit.estimated_standard_wpm)
        self.assertGreaterEqual(audit.wpm_boost_pct, 12.0)

    def test_balance_text_modes(self):
        text = "Cognitive spatial reasoning accelerates synthesis."
        bionic = self.balancer.balance_text(text, mode="bionic_anchor")
        self.assertIn("**Cogni**tive", bionic)
        self.assertIn("**spa**tial", bionic)

        dots = self.balancer.balance_text(text, mode="syllable_dot")
        self.assertIn("\u00B7", dots)

        hybrid = self.balancer.balance_text(text, mode="hybrid_dx")
        self.assertTrue(len(hybrid) > len(text))

    def test_balance_canvas(self):
        canvas_data = {
            "nodes": [
                {"id": "1", "type": "text", "text": "Understanding cognitive spatial layouts."},
                {"id": "2", "type": "group", "label": "Group 1"}
            ],
            "edges": []
        }
        balanced = self.balancer.balance_canvas(canvas_data, mode="bionic_anchor")
        self.assertEqual(len(balanced["nodes"]), 2)
        text_node = balanced["nodes"][0]
        self.assertIn("**", text_node["text"])
        # Non-text nodes untouched
        self.assertEqual(balanced["nodes"][1], canvas_data["nodes"][1])

    def test_svg_and_summary_export(self):
        sample = "Spatial anchors reduce visual wandering and eye strain."
        audit = self.balancer.audit_text(sample)
        svg = self.balancer.export_comparison_svg(sample, audit)
        self.assertTrue(svg.startswith("<svg"))
        self.assertTrue(svg.endswith("</svg>"))
        self.assertIn("Visual Typography Kerning &amp; Lexical Anchor Balancer", svg)

        summary = VisualTypographyBalancer.export_summary(audit, sample, self.balancer.balance_text(sample))
        self.assertIn("# Visual Typography Kerning & Lexical Anchor Audit", summary)
        self.assertIn("Reading Speed Enhancement", summary)

    def test_zero_em_dashes(self):
        import inspect
        import scripts.typography_balancer as tb
        source = inspect.getsource(tb)
        self.assertNotIn(chr(8212), source, "Illegal em dash found in scripts/typography_balancer.py")


if __name__ == "__main__":
    unittest.main()
