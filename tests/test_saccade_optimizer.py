#!/usr/bin/env python3
"""
Unit tests for Autonomous Cognitive Spatial Working Memory Saccade & Visual Glance Path Optimizer
Part of the DxSkills Cognitive Architecture Suite (https://dxskills.sounny.com)
"""

import os
import json
import unittest

from scripts.saccade_optimizer import (
    FixationNode,
    SaccadeMetrics,
    SaccadeGlancePathOptimizer
)


class TestSaccadeGlancePathOptimizer(unittest.TestCase):
    """Tests for ocular scanpath simulation, saccadic metrics, and layout optimization."""

    def setUp(self):
        self.optimizer = SaccadeGlancePathOptimizer()
        self.sample_canvas = {
            "nodes": [
                {"id": "node_1", "type": "text", "text": "Executive Problem Statement", "x": 0, "y": 0, "width": 260, "height": 140, "color": "1"},
                {"id": "node_2", "type": "text", "text": "Spatial Architecture Core", "x": 1200, "y": 900, "width": 260, "height": 140, "color": "2"},
                {"id": "node_3", "type": "text", "text": "Cognitive Load Evaluation", "x": 100, "y": 20, "width": 260, "height": 140, "color": "3"},  # Intentionally overlapping / crowding node_1
                {"id": "node_4", "type": "text", "text": "Obsidian Export Pipeline", "x": 2000, "y": 100, "width": 260, "height": 140, "color": "4"}
            ],
            "edges": [
                {"id": "e1", "fromNode": "node_1", "toNode": "node_2"},
                {"id": "e2", "fromNode": "node_2", "toNode": "node_4"}
            ]
        }

    def test_load_canvas_data(self):
        self.optimizer.load_canvas_data(self.sample_canvas)
        self.assertEqual(len(self.optimizer.nodes), 4)
        self.assertEqual(len(self.optimizer.edges), 2)
        n1 = self.optimizer.nodes["node_1"]
        self.assertEqual(n1.center_x, 130.0)
        self.assertEqual(n1.center_y, 70.0)

    def test_compute_scanpath(self):
        self.optimizer.load_canvas_data(self.sample_canvas)
        scanpath = self.optimizer.compute_scanpath()
        self.assertEqual(len(scanpath), 4)
        # Verify first node in scanpath is node_1 (topological root)
        self.assertEqual(scanpath[0].node_id, "node_1")

    def test_evaluate_metrics(self):
        self.optimizer.load_canvas_data(self.sample_canvas)
        scanpath = self.optimizer.compute_scanpath()
        metrics = self.optimizer.evaluate_metrics(scanpath)

        self.assertGreater(metrics.total_path_distance, 1000.0)
        self.assertGreater(metrics.avg_jump_distance, 200.0)
        self.assertGreater(metrics.crowding_violations, 0)
        self.assertGreater(metrics.cognitive_fatigue_score, 20.0)

    def test_optimize_layout_reduces_metrics(self):
        self.optimizer.load_canvas_data(self.sample_canvas)
        scanpath_orig = self.optimizer.compute_scanpath()
        orig_metrics = self.optimizer.evaluate_metrics(scanpath_orig)

        # Optimize layout
        opt_nodes = self.optimizer.optimize_layout(cols=2, gutter_x=50, gutter_y=60)
        self.assertEqual(len(opt_nodes), 4)

        opt_scanpath = self.optimizer.compute_scanpath(opt_nodes)
        opt_metrics = self.optimizer.evaluate_metrics(opt_scanpath)

        # Confirm total path distance and crowding are significantly reduced
        self.assertLess(opt_metrics.total_path_distance, orig_metrics.total_path_distance)
        self.assertEqual(opt_metrics.crowding_violations, 0)
        self.assertLess(opt_metrics.cognitive_fatigue_score, orig_metrics.cognitive_fatigue_score)

    def test_export_canvas_and_svg(self):
        self.optimizer.load_canvas_data(self.sample_canvas)
        opt_nodes = self.optimizer.optimize_layout(cols=2)
        canvas_out = self.optimizer.export_canvas(opt_nodes)

        self.assertIn("nodes", canvas_out)
        self.assertIn("edges", canvas_out)
        self.assertEqual(len(canvas_out["nodes"]), 4)

        svg = self.optimizer.export_scanpath_svg(list(opt_nodes.values()))
        self.assertTrue(svg.startswith("<svg"))
        self.assertTrue(svg.endswith("</svg>"))
        self.assertIn("saccade-arrow", svg)

    def test_audit_summary(self):
        self.optimizer.load_canvas_data(self.sample_canvas)
        scanpath = self.optimizer.compute_scanpath()
        orig = self.optimizer.evaluate_metrics(scanpath)
        opt_nodes = self.optimizer.optimize_layout(cols=2)
        opt = self.optimizer.evaluate_metrics(list(opt_nodes.values()))

        summary = SaccadeGlancePathOptimizer.export_audit_summary(orig, opt)
        self.assertIn("# Saccadic Eye-Tracking & Glance Path Optimization Audit", summary)
        self.assertIn("Cognitive Fatigue Score", summary)

    def test_zero_em_dashes(self):
        import inspect
        import scripts.saccade_optimizer as so
        source = inspect.getsource(so)
        self.assertNotIn(chr(8212), source, "Illegal em dash found in scripts/saccade_optimizer.py")


if __name__ == "__main__":
    unittest.main()
