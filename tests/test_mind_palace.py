"""
Tests for Autonomous Cognitive Spatial Mind Palace Virtual Tour & Spatial Audio Navigator.
Strict zero em dash compliance verified across all test assertions.
"""

import os
import sys
import json
import unittest
import tempfile
import subprocess

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))
from mind_palace import (
    MindPalaceProjector,
    MindPalaceExporter,
    run_mind_palace,
)


class TestMindPalace(unittest.TestCase):

    def setUp(self):
        self.sample_text = (
            "# Strategic Spatial Architecture\n"
            "- Establish entry friction: Linear prose overloads working memory.\n"
            "- Core system: 2D spatial canvas decouples ideas from text walls.\n"
            "- Vector routing: High-dimensional embeddings cluster conceptual anchors.\n"
            "- Multi-vault federation: Cross-repository synchronizers bridge dangling wikilinks.\n"
            "- Dual-channel balance: Working memory monitor gauges phonological load.\n"
            "- Resolution horizon: Method-of-loci memory palaces activate hippocampal recall."
        )

    def test_palace_projection(self):
        nodes = [{"text": line.lstrip("- ")} for line in self.sample_text.split("\n") if line.startswith("-")]
        palace = MindPalaceProjector.project_palace(nodes, palace_title="Executive Palace")

        self.assertEqual(palace["title"], "Executive Palace")
        self.assertGreaterEqual(palace["total_chambers"], 2)
        self.assertEqual(palace["total_loci"], len(nodes))

        # Check chamber properties
        c1 = palace["chambers"][0]
        self.assertEqual(c1["name"], "The Grand Atrium")
        self.assertIn("theme", c1)
        self.assertIn("hex_color", c1)

        # Check loci spatial audio
        loc1 = c1["loci"][0]
        self.assertIn("fixture", loc1)
        self.assertIn("spatial_audio", loc1)
        sa = loc1["spatial_audio"]
        self.assertIn("azimuth_degrees", sa)
        self.assertIn("stereo_pan", sa)
        self.assertIn("distance_meters", sa)

    def test_palace_empty_fallback(self):
        palace = MindPalaceProjector.project_palace([], palace_title="Fallback Palace")
        self.assertGreaterEqual(palace["total_chambers"], 1)
        self.assertGreaterEqual(palace["total_loci"], 4)

    def test_canvas_export(self):
        nodes = [{"text": f"Concept {i}"} for i in range(1, 5)]
        palace = MindPalaceProjector.project_palace(nodes, palace_title="Canvas Export Palace")
        canvas = MindPalaceExporter.to_canvas(palace)

        self.assertIn("nodes", canvas)
        self.assertIn("edges", canvas)

        # Should contain root entry node + chamber header nodes + loci nodes
        self.assertGreater(len(canvas["nodes"]), 4)
        entry_node = [n for n in canvas["nodes"] if n["id"] == "node-palace-entry"][0]
        self.assertIn("Canvas Export Palace", entry_node["text"])

    def test_svg_blueprint_export(self):
        nodes = [{"text": f"Concept {i}"} for i in range(1, 5)]
        palace = MindPalaceProjector.project_palace(nodes, palace_title="SVG Blueprint Palace")
        svg = MindPalaceExporter.to_svg_blueprint(palace)

        self.assertTrue(svg.startswith("<svg"))
        self.assertTrue(svg.endswith("</svg>"))
        self.assertIn("SVG Blueprint Palace", svg)
        self.assertIn("ATRIUM", svg)

    def test_run_mind_palace_pipeline(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            out_canvas = os.path.join(tmpdir, "palace.canvas")
            out_svg = os.path.join(tmpdir, "blueprint.svg")

            palace, canvas_data, svg_code = run_mind_palace(
                self.sample_text,
                title="CI Pipeline Palace",
                output_canvas=out_canvas,
                output_svg=out_svg
            )

            self.assertTrue(os.path.exists(out_canvas))
            self.assertTrue(os.path.exists(out_svg))

            with open(out_canvas, "r", encoding="utf-8") as f:
                saved = json.load(f)
            self.assertIn("nodes", saved)
            self.assertGreater(len(saved["nodes"]), 4)

    def test_cli_palace_integration(self):
        cli_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts", "dx_cli.py"))
        with tempfile.TemporaryDirectory() as tmpdir:
            out_canvas = os.path.join(tmpdir, "cli_palace.canvas")
            res = subprocess.run(
                [
                    sys.executable,
                    cli_path,
                    "palace",
                    self.sample_text,
                    "--title", "CLI Palace Test",
                    "--canvas", out_canvas
                ],
                capture_output=True,
                text=True
            )
            self.assertEqual(res.returncode, 0, f"CLI stderr: {res.stderr}")
            self.assertIn("[DxSkills] Mind Palace projected:", res.stdout)
            self.assertTrue(os.path.exists(out_canvas))

    def test_zero_em_dash_compliance(self):
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts", "mind_palace.py"))
        with open(script_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertNotIn(chr(8212), content, f"Em dash found in {script_path}")

        with open(__file__, "r", encoding="utf-8") as f:
            test_content = f.read()
        self.assertNotIn(chr(8212), test_content, "Em dash found in test file")


if __name__ == "__main__":
    unittest.main()
