"""
Tests for Autonomous Multi-Modal Spatial Audio-Visual Storyboarder.
Strict zero em dash compliance verified across all test assertions.
"""

import os
import sys
import json
import unittest
import tempfile
import subprocess

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))
from spatial_storyboard import (
    StoryboardSequencer,
    StoryboardExporter,
    run_storyboard,
)


class TestSpatialStoryboard(unittest.TestCase):

    def setUp(self):
        self.sample_script = (
            "# Act I: Inciting Incident\n"
            "- Establish the friction: Linear text walls overload phonological working memory.\n"
            "- Inciting shift: Non-linear thinkers struggle to communicate complex holistic architectures.\n"
            "# Act II: Core Exploration\n"
            "- Core exploration: The DxSkills cognitive engine decouples spatial mental models.\n"
            "- Technical deep dive: High-dimensional vector similarity clusters ideas into constellations.\n"
            "- Multi-vault bridge: Cross-repository synchronizers identify dangling wikilinks.\n"
            "# Act III: Climax and Resolution\n"
            "- Resolution vista: The user presents a hardened spatial canvas that disarms reductionist critics."
        )

    def test_sequencer_parsing(self):
        result = StoryboardSequencer.sequence_script(self.sample_script)
        self.assertEqual(result["total_shots"], 6)
        self.assertGreater(result["total_duration_seconds"], 0)
        self.assertIn("Act I", result["acts"])
        self.assertIn("Act II", result["acts"])
        self.assertIn("Act III", result["acts"])

        shot_1 = result["shots"][0]
        self.assertEqual(shot_1["shot_index"], 1)
        self.assertEqual(shot_1["act"], "Act I")
        self.assertIn("Overhead Spatial Map (OSM)", shot_1["framing"])
        self.assertGreaterEqual(shot_1["duration_seconds"], 3)
        self.assertIn("Acoustic Beat 1", shot_1["audio_cue"])

    def test_sequencer_fallback_defaults(self):
        result = StoryboardSequencer.sequence_script("")
        self.assertEqual(result["total_shots"], 6)
        self.assertEqual(len(result["shots"]), 6)
        self.assertIn("Act I", result["acts"])
        self.assertIn("Act III", result["acts"])

    def test_canvas_exporter(self):
        result = StoryboardSequencer.sequence_script(self.sample_script)
        canvas = StoryboardExporter.to_canvas(result, title="Venture Pitch Storyboard")

        self.assertIn("nodes", canvas)
        self.assertIn("edges", canvas)
        # 1 header node + 6 shot nodes = 7 nodes
        self.assertEqual(len(canvas["nodes"]), 7)
        self.assertEqual(len(canvas["edges"]), 6)

        header = [n for n in canvas["nodes"] if n["id"] == "node-storyboard-header"][0]
        self.assertIn("Venture Pitch Storyboard", header["text"])
        self.assertIn("Total Shots: **6**", header["text"])

        edge_1 = canvas["edges"][0]
        self.assertEqual(edge_1["fromNode"], "node-storyboard-header")
        self.assertEqual(edge_1["toNode"], "shot-node-1")
        self.assertTrue(edge_1["label"].startswith("+"))

    def test_svg_animatic_exporter(self):
        result = StoryboardSequencer.sequence_script(self.sample_script)
        svg = StoryboardExporter.to_svg_animatic(result, title="Executive Pitch Strip")

        self.assertTrue(svg.startswith("<svg"))
        self.assertTrue(svg.endswith("</svg>"))
        self.assertIn("Executive Pitch Strip", svg)
        self.assertIn("SHOT 1", svg)
        self.assertIn("SHOT 6", svg)
        self.assertIn("stroke-dasharray=\"2 2\"", svg)  # Rule of thirds guides

    def test_svg_empty_fallback(self):
        empty_storyboard = {"total_shots": 0, "shots": [], "acts": {}}
        svg = StoryboardExporter.to_svg_animatic(empty_storyboard)
        self.assertIn("No shots sequenced", svg)

    def test_run_storyboard_file_outputs(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            canvas_path = os.path.join(tmpdir, "storyboard.canvas")
            svg_path = os.path.join(tmpdir, "animatic.svg")

            sb, canvas_data, svg_code = run_storyboard(
                self.sample_script,
                title="Test Pipeline",
                output_canvas=canvas_path,
                output_svg=svg_path
            )

            self.assertTrue(os.path.exists(canvas_path))
            self.assertTrue(os.path.exists(svg_path))

            with open(canvas_path, "r", encoding="utf-8") as f:
                saved_canvas = json.load(f)
            self.assertEqual(len(saved_canvas["nodes"]), 7)

            with open(svg_path, "r", encoding="utf-8") as f:
                saved_svg = f.read()
            self.assertIn("Test Pipeline", saved_svg)

    def test_cli_integration(self):
        cli_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts", "dx_cli.py"))
        with tempfile.TemporaryDirectory() as tmpdir:
            out_canvas = os.path.join(tmpdir, "cli.canvas")
            out_svg = os.path.join(tmpdir, "cli.svg")

            res = subprocess.run(
                [
                    sys.executable,
                    cli_path,
                    "storyboard",
                    "--title", "CLI Cinematic Test",
                    "--canvas", out_canvas,
                    "--svg", out_svg
                ],
                capture_output=True,
                text=True
            )
            self.assertEqual(res.returncode, 0, f"CLI stderr: {res.stderr}")
            self.assertIn("[DxSkills] Sequenced", res.stdout)
            self.assertTrue(os.path.exists(out_canvas))
            self.assertTrue(os.path.exists(out_svg))

    def test_zero_em_dash_compliance(self):
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts", "spatial_storyboard.py"))
        with open(script_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertNotIn(chr(8212), content, f"Em dash found in {script_path}")
        with open(__file__, "r", encoding="utf-8") as f:
            test_content = f.read()
        self.assertNotIn(chr(8212), test_content, "Em dash found in test file")


if __name__ == "__main__":
    unittest.main()
