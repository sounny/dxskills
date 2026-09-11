#!/usr/bin/env python3
"""
Unit tests for Autonomous Cognitive Dynamic Working Memory Stress-Tester & Load Shedder
Part of the DxSkills Cognitive Architecture Suite (https://dxskills.sounny.com)
"""

import os
import unittest
import json
from scripts.load_shedder import (
    WorkingMemoryLoadShedder,
    CognitiveNode,
    StressTelemetry,
    SheddingAudit,
    create_sample_stress_scenario
)


class TestWorkingMemoryLoadShedder(unittest.TestCase):
    """Test suite verifying stress modeling, cognitive degradation index, and load shedding."""

    def setUp(self):
        self.shedder = WorkingMemoryLoadShedder()

    def test_node_and_edge_addition(self):
        """Test node creation and degree tracking."""
        n1 = self.shedder.add_node("Root Node")
        n2 = self.shedder.add_node("Child Node")
        self.shedder.add_edge(n1.node_id, n2.node_id)

        self.assertEqual(n1.out_degree, 1)
        self.assertEqual(n2.in_degree, 1)
        self.assertEqual(len(self.shedder.nodes), 2)

    def test_markdown_outline_parsing(self):
        """Test hierarchy and depth derivation from indented markdown outline."""
        outline = """# Root Hub
- Level 1 Subconcept
  - Level 2 Leaf Detail"""
        self.shedder.load_from_markdown(outline)
        self.assertEqual(len(self.shedder.nodes), 3)

        root = next(n for n in self.shedder.nodes.values() if n.label == "Root Hub")
        leaf = next(n for n in self.shedder.nodes.values() if n.label == "Level 2 Leaf Detail")

        self.assertEqual(root.depth, 0)
        self.assertGreater(leaf.depth, 0)

    def test_stress_telemetry_calculation(self):
        """Verify Sweller cognitive load component calculations and status."""
        shedder, audit = create_sample_stress_scenario()
        telemetry = audit.initial_telemetry

        self.assertGreater(telemetry.total_nodes, 10)
        self.assertGreater(telemetry.intrinsic_load, 20.0)
        self.assertGreater(telemetry.extraneous_load, 20.0)
        self.assertIn(telemetry.status, ["OPTIMAL", "ELEVATED", "CRITICAL"])
        self.assertGreaterEqual(telemetry.cognitive_degradation_index, 0.0)
        self.assertLessEqual(telemetry.cognitive_degradation_index, 1.0)

    def test_load_shedding_execution(self):
        """Verify leaf pruning, cognitive load points freed, and reduction ratio."""
        shedder, audit = create_sample_stress_scenario()

        self.assertGreater(audit.pruned_leaves_count, 0)
        self.assertGreater(audit.load_points_freed, 20.0)
        self.assertGreater(audit.reduction_percentage, 25.0)
        self.assertLess(audit.post_shed_telemetry.total_load_points, audit.initial_telemetry.total_load_points)
        self.assertEqual(len(audit.retained_nodes) + len(audit.shed_nodes), len(shedder.nodes))

    def test_obsidian_canvas_export(self):
        """Verify Obsidian .canvas structure, HUD node, and folded archive card."""
        shedder, audit = create_sample_stress_scenario()
        canvas = shedder.export_canvas(audit)

        self.assertIn("nodes", canvas)
        self.assertIn("edges", canvas)

        hud_node = next(n for n in canvas["nodes"] if n["id"] == "node-hud-stress")
        self.assertIn("Cognitive Working Memory Health HUD", hud_node["text"])

        archive_node = next(n for n in canvas["nodes"] if n["id"] == "node-folded-archive")
        self.assertIn("Folded Semantic Details", archive_node["text"])

    def test_svg_gauge_rendering(self):
        """Verify SVG visualization contains comparison bars and executive directive."""
        shedder, audit = create_sample_stress_scenario()
        svg_code = shedder.export_svg_gauge(audit, width=780, height=500)

        self.assertIn("<svg", svg_code)
        self.assertIn("</svg>", svg_code)
        self.assertIn("Cognitive Working Memory Stress-Tester", svg_code)
        self.assertIn("INITIAL COGNITIVE LOAD", svg_code)
        self.assertIn("POST-SHED LOAD", svg_code)
        self.assertIn("EXECUTIVE COGNITIVE DIRECTIVE", svg_code)

    def test_zero_em_dashes_enforcement(self):
        """Strict compliance test: zero em dashes across scripts and tests."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(current_dir, "..", "scripts", "load_shedder.py")
        test_path = os.path.abspath(__file__)

        with open(script_path, "r", encoding="utf-8") as f:
            script_content = f.read()
            self.assertNotIn(chr(8212), script_content, "Em dash found in scripts/load_shedder.py")

        with open(test_path, "r", encoding="utf-8") as f:
            test_content = f.read()
            self.assertNotIn(chr(8212), test_content, "Em dash found in tests/test_load_shedder.py")


if __name__ == "__main__":
    unittest.main()
