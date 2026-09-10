#!/usr/bin/env python3
"""
Unit tests for Autonomous Cognitive Visual Attention Heatmap & Dyslexia Glare Optimizer
Part of the DxSkills Cognitive Architecture Suite (https://dxskills.sounny.com)
"""

import os
import json
import unittest

from scripts.glare_optimizer import (
    hex_to_rgb,
    get_relative_luminance,
    calculate_contrast_ratio,
    NodeVisualProfile,
    GlareAuditReport,
    DyslexiaGlareOptimizer,
    DYSLEXIA_PALETTES
)


class TestDyslexiaGlareOptimizer(unittest.TestCase):
    """Tests for optical comfort audit, glare detection, chromatic calibration, and SVG heatmap."""

    def setUp(self):
        self.optimizer = DyslexiaGlareOptimizer()
        self.sample_canvas = {
            "nodes": [
                {"id": "node_1", "type": "text", "text": "Core Objective", "x": 0, "y": 0, "width": 260, "height": 160, "color": "1"},
                {"id": "node_2", "type": "text", "text": "Implementation Plan", "x": 300, "y": 0, "width": 260, "height": 160, "color": "2"},
                {"id": "node_3", "type": "text", "text": "Cognitive Load Buffer", "x": 310, "y": 10, "width": 260, "height": 160, "color": "6"}  # Crowded next to node_2
            ],
            "edges": [
                {"id": "e1", "fromNode": "node_1", "toNode": "node_2"}
            ]
        }

    def test_hex_to_rgb(self):
        self.assertEqual(hex_to_rgb("#ffffff"), (255, 255, 255))
        self.assertEqual(hex_to_rgb("#000000"), (0, 0, 0))
        self.assertEqual(hex_to_rgb("fff"), (255, 255, 255))
        self.assertEqual(hex_to_rgb("invalid"), (128, 128, 128))

    def test_relative_luminance_and_contrast(self):
        white = hex_to_rgb("#ffffff")
        black = hex_to_rgb("#000000")
        l_white = get_relative_luminance(white)
        l_black = get_relative_luminance(black)

        self.assertAlmostEqual(l_white, 1.0, places=2)
        self.assertAlmostEqual(l_black, 0.0, places=2)

        ratio = calculate_contrast_ratio(white, black)
        self.assertAlmostEqual(ratio, 21.0, places=1)

    def test_audit_optical_comfort(self):
        self.optimizer.load_canvas(self.sample_canvas)
        audit = self.optimizer.audit_optical_comfort()

        self.assertEqual(audit.total_nodes, 3)
        self.assertGreater(audit.average_contrast_ratio, 1.0)
        self.assertGreater(audit.high_crowding_nodes, 0)
        self.assertGreaterEqual(audit.optical_comfort_score, 0.0)
        self.assertLessEqual(audit.optical_comfort_score, 100.0)
        self.assertIn(audit.palette_recommendation, ["soft_slate", "warm_paper"])

    def test_optimize_canvas(self):
        self.optimizer.load_canvas(self.sample_canvas)
        opt = self.optimizer.optimize_canvas(target_palette="warm_paper")

        self.assertIn("nodes", opt)
        self.assertIn("edges", opt)
        self.assertEqual(len(opt["nodes"]), 3)

        # Check that colors have been calibrated to palette sequence
        pal = DYSLEXIA_PALETTES["warm_paper"]
        expected_colors = [pal["color_1"], pal["color_2"], pal["color_3"]]
        for idx, n in enumerate(opt["nodes"]):
            self.assertEqual(n["color"], expected_colors[idx])

    def test_export_heatmap_svg_and_markdown(self):
        self.optimizer.load_canvas(self.sample_canvas)
        audit = self.optimizer.audit_optical_comfort()

        svg = self.optimizer.export_heatmap_svg(audit)
        self.assertTrue(svg.startswith("<svg"))
        self.assertTrue(svg.endswith("</svg>"))
        self.assertIn("glare-severe", svg)
        self.assertIn("Visual Attention &amp; Glare Heatmap", svg)

        report = DyslexiaGlareOptimizer.export_audit_markdown(audit)
        self.assertIn("# Visual Attention Heatmap & Dyslexia Glare Audit", report)
        self.assertIn("Optical Comfort Score", report)

    def test_zero_em_dashes(self):
        import inspect
        import scripts.glare_optimizer as go
        source = inspect.getsource(go)
        self.assertNotIn(chr(8212), source, "Illegal em dash found in scripts/glare_optimizer.py")


if __name__ == "__main__":
    unittest.main()
