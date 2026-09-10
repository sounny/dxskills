#!/usr/bin/env python3
"""
Unit tests for Autonomous Cognitive Multi-Perspective Architectural Trade-Off Radar & Pareto Frontier
Part of the DxSkills Cognitive Architecture Suite (https://dxskills.sounny.com)
"""

import os
import unittest
import json
from scripts.tradeoff_radar import (
    ArchitecturalTradeoffRadar,
    ArchitectureCandidate,
    create_sample_tradeoff_radar
)


class TestArchitecturalTradeoffRadar(unittest.TestCase):
    """Test suite verifying Pareto frontier logic, radar geometry, and canvas exports."""

    def setUp(self):
        self.radar = ArchitecturalTradeoffRadar(axes=[
            "cognitive_simplicity",
            "throughput_speed",
            "maintainability"
        ])

    def test_candidate_creation_and_bounds(self):
        """Test candidate score normalization and boundary enforcement."""
        cand = self.radar.add_candidate(
            name="Test Architecture",
            scores={
                "cognitive_simplicity": 1.5,  # Should clamp to 1.0
                "throughput_speed": -0.2,     # Should clamp to 0.0
                "maintainability": 0.75
            },
            description="Clamping test architecture"
        )
        self.assertEqual(cand.get_score("cognitive_simplicity"), 1.0)
        self.assertEqual(cand.get_score("throughput_speed"), 0.0)
        self.assertEqual(cand.get_score("maintainability"), 0.75)
        self.assertEqual(cand.get_score("non_existent"), 0.0)

    def test_dominance_and_pareto_frontier(self):
        """Verify Pareto dominance logic identifying optimal vs dominated designs."""
        # A: Strong across all axes
        cand_a = self.radar.add_candidate(
            name="Arch A",
            scores={"cognitive_simplicity": 0.9, "throughput_speed": 0.9, "maintainability": 0.9}
        )
        # B: Dominated by A (strictly worse or equal on all axes)
        cand_b = self.radar.add_candidate(
            name="Arch B",
            scores={"cognitive_simplicity": 0.5, "throughput_speed": 0.5, "maintainability": 0.5}
        )
        # C: Non-dominated trade-off (better throughput than A, lower simplicity)
        cand_c = self.radar.add_candidate(
            name="Arch C",
            scores={"cognitive_simplicity": 0.6, "throughput_speed": 0.99, "maintainability": 0.8}
        )

        analysis = self.radar.evaluate_pareto()

        self.assertIn(cand_a.candidate_id, analysis.pareto_frontier_ids)
        self.assertIn(cand_c.candidate_id, analysis.pareto_frontier_ids)
        self.assertIn(cand_b.candidate_id, analysis.dominated_ids)

        self.assertIn(cand_b.candidate_id, cand_a.dominates)
        self.assertIn(cand_a.candidate_id, cand_b.dominated_by)

    def test_tradeoff_tensions_detection(self):
        """Verify inverse correlation detection between competing architectural goals."""
        radar = ArchitecturalTradeoffRadar(axes=["speed", "simplicity"])
        radar.add_candidate("UltraFast", scores={"speed": 0.95, "simplicity": 0.20})
        radar.add_candidate("UltraSimple", scores={"speed": 0.20, "simplicity": 0.95})
        radar.add_candidate("Balanced", scores={"speed": 0.55, "simplicity": 0.55})

        analysis = radar.evaluate_pareto()
        self.assertGreater(len(analysis.tradeoff_tensions), 0)
        tension = analysis.tradeoff_tensions[0]
        self.assertGreater(tension["tension_score"], 0.8)

    def test_radar_svg_generation(self):
        """Verify SVG generation includes radar polygons, labels, and styles."""
        sample_radar = create_sample_tradeoff_radar()
        svg_content = sample_radar.export_radar_svg(width=800, height=600)

        self.assertIn("<svg", svg_content)
        self.assertIn("</svg>", svg_content)
        self.assertIn("Modular Monolith", svg_content)
        self.assertIn("Cognitive Simplicity", svg_content)
        self.assertIn("Throughput &amp; Speed", svg_content)
        self.assertIn("PARETO", svg_content)
        self.assertIn("polygon", svg_content)

    def test_obsidian_canvas_export(self):
        """Verify Obsidian .canvas structure, color coding, and dominance edges."""
        sample_radar = create_sample_tradeoff_radar()
        canvas = sample_radar.export_pareto_canvas()

        self.assertIn("nodes", canvas)
        self.assertIn("edges", canvas)
        self.assertGreaterEqual(len(canvas["nodes"]), 4)

        # Check that Pareto candidate has green card color ('4')
        modular_node = next(n for n in canvas["nodes"] if "Modular Monolith" in n.get("text", ""))
        self.assertEqual(modular_node["color"], "4")

        # Check that dominated candidate has red card color ('1')
        legacy_node = next(n for n in canvas["nodes"] if "Tangled Legacy Core" in n.get("text", ""))
        self.assertEqual(legacy_node["color"], "1")

        # Check dominance edges exist
        self.assertGreater(len(canvas["edges"]), 0)
        self.assertEqual(canvas["edges"][0]["toEnd"], "arrow")

    def test_serialization_roundtrip(self):
        """Verify JSON dictionary serialization and reconstruction."""
        sample_radar = create_sample_tradeoff_radar()
        data = sample_radar.to_dict()
        restored = ArchitecturalTradeoffRadar.from_dict(data)

        self.assertEqual(len(sample_radar.candidates), len(restored.candidates))
        for cid, cand in sample_radar.candidates.items():
            self.assertIn(cid, restored.candidates)
            rest_cand = restored.candidates[cid]
            self.assertEqual(cand.name, rest_cand.name)
            for ax in sample_radar.axes:
                self.assertAlmostEqual(cand.get_score(ax), rest_cand.get_score(ax))

    def test_zero_em_dashes_enforcement(self):
        """Strict compliance test: zero em dashes across scripts and tests."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(current_dir, "..", "scripts", "tradeoff_radar.py")
        test_path = os.path.abspath(__file__)

        with open(script_path, "r", encoding="utf-8") as f:
            script_content = f.read()
            self.assertNotIn(chr(8212), script_content, "Em dash found in scripts/tradeoff_radar.py")

        with open(test_path, "r", encoding="utf-8") as f:
            test_content = f.read()
            self.assertNotIn(chr(8212), test_content, "Em dash found in tests/test_tradeoff_radar.py")


if __name__ == "__main__":
    unittest.main()
