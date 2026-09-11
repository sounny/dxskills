#!/usr/bin/env python3
"""
Unit tests for Autonomous Cognitive Multi-Perspective Decision Matrix & Spatial Opportunity Cost Evaluator
Part of the DxSkills Cognitive Architecture Suite (https://dxskills.sounny.com)
"""

import os
import unittest
import json
from scripts.decision_matrix import (
    SpatialDecisionMatrix,
    DecisionOption,
    DecisionAudit,
    create_sample_decision_matrix
)


class TestSpatialDecisionMatrix(unittest.TestCase):
    """Test suite verifying decision quadrant classification, leverage math, and canvas exports."""

    def setUp(self):
        self.matrix = SpatialDecisionMatrix()

    def test_option_addition_and_score_bounds(self):
        """Test score clamping and boundary handling."""
        opt = self.matrix.add_option(
            name="Test Option",
            immediate_utility=1.8,       # Clamps to 1.0
            compounding_leverage=-0.4,    # Clamps to 0.0
            opportunity_cost_risk=0.75,
            cognitive_flow=0.85,
            description="Clamping test"
        )
        self.assertEqual(opt.immediate_utility, 1.0)
        self.assertEqual(opt.compounding_leverage, 0.0)
        self.assertEqual(opt.opportunity_cost_risk, 0.75)
        self.assertEqual(opt.cognitive_flow, 0.85)

    def test_quadrant_classification(self):
        """Verify strict spatial quadrant assignment."""
        matrix = SpatialDecisionMatrix()
        # Q1: High Leverage, High Flow
        o1 = matrix.add_option("Q1 Item", immediate_utility=0.8, compounding_leverage=0.8, opportunity_cost_risk=0.8, cognitive_flow=0.8)
        # Q2: High Leverage, Low Flow
        o2 = matrix.add_option("Q2 Item", immediate_utility=0.8, compounding_leverage=0.8, opportunity_cost_risk=0.8, cognitive_flow=0.2)
        # Q3: Low Leverage, High Flow
        o3 = matrix.add_option("Q3 Item", immediate_utility=0.8, compounding_leverage=0.2, opportunity_cost_risk=0.2, cognitive_flow=0.8)
        # Q4: Low Leverage, Low Flow
        o4 = matrix.add_option("Q4 Item", immediate_utility=0.2, compounding_leverage=0.2, opportunity_cost_risk=0.2, cognitive_flow=0.2)

        self.assertEqual(o1.quadrant, "q1")
        self.assertEqual(o2.quadrant, "q2")
        self.assertEqual(o3.quadrant, "q3")
        self.assertEqual(o4.quadrant, "q4")

    def test_evaluate_matrix_and_audit(self):
        """Verify audit calculations, rankings, and priority order."""
        sample_matrix = create_sample_decision_matrix()
        audit = sample_matrix.evaluate_matrix()

        self.assertEqual(audit.total_options, 4)
        self.assertEqual(audit.q1_count, 1)
        self.assertEqual(audit.q2_count, 1)
        self.assertEqual(audit.q3_count, 1)
        self.assertEqual(audit.q4_count, 1)

        self.assertEqual(audit.highest_leverage_option.name, "Automate CLI Scaffolding Pipeline")
        self.assertEqual(audit.action_roadmap[0].name, "Automate CLI Scaffolding Pipeline")
        self.assertGreater(audit.action_roadmap[0].leverage_score, audit.action_roadmap[1].leverage_score)

    def test_obsidian_canvas_export(self):
        """Verify Obsidian .canvas structure, quadrant hubs, and priority edges."""
        sample_matrix = create_sample_decision_matrix()
        audit = sample_matrix.evaluate_matrix()
        canvas = sample_matrix.export_canvas(audit)

        self.assertIn("nodes", canvas)
        self.assertIn("edges", canvas)
        self.assertGreaterEqual(len(canvas["nodes"]), 8)  # 4 hubs + 4 option cards

        hub_nodes = [n for n in canvas["nodes"] if "hub-" in n["id"]]
        self.assertEqual(len(hub_nodes), 4)

    def test_svg_matrix_rendering(self):
        """Verify SVG visualization contains quadrants, axes, and decision circles."""
        sample_matrix = create_sample_decision_matrix()
        audit = sample_matrix.evaluate_matrix()
        svg_code = sample_matrix.export_svg_matrix(audit, width=760, height=540)

        self.assertIn("<svg", svg_code)
        self.assertIn("</svg>", svg_code)
        self.assertIn("Q1: Compounding Superhighway", svg_code)
        self.assertIn("Q2: Strategic Breakthrough", svg_code)
        self.assertIn("Q3: Flow Sprints", svg_code)
        self.assertIn("Q4: Cognitive Debt Traps", svg_code)
        self.assertIn("circle", svg_code)

    def test_serialization_roundtrip(self):
        """Verify JSON dictionary serialization and reconstruction."""
        sample_matrix = create_sample_decision_matrix()
        data = sample_matrix.to_dict()
        restored = SpatialDecisionMatrix.from_dict(data)

        self.assertEqual(len(sample_matrix.options), len(restored.options))
        for oid, opt in sample_matrix.options.items():
            self.assertIn(oid, restored.options)
            r_opt = restored.options[oid]
            self.assertEqual(opt.name, r_opt.name)
            self.assertAlmostEqual(opt.leverage_score, r_opt.leverage_score)
            self.assertEqual(opt.quadrant, r_opt.quadrant)

    def test_zero_em_dashes_enforcement(self):
        """Strict compliance test: zero em dashes across scripts and tests."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(current_dir, "..", "scripts", "decision_matrix.py")
        test_path = os.path.abspath(__file__)

        with open(script_path, "r", encoding="utf-8") as f:
            script_content = f.read()
            self.assertNotIn(chr(8212), script_content, "Em dash found in scripts/decision_matrix.py")

        with open(test_path, "r", encoding="utf-8") as f:
            test_content = f.read()
            self.assertNotIn(chr(8212), test_content, "Em dash found in tests/test_decision_matrix.py")


if __name__ == "__main__":
    unittest.main()
