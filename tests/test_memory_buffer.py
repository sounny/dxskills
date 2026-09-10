"""
Tests for Autonomous Cognitive Spatial Working Memory Buffer Monitor.
Strict zero em dash compliance verified across all test assertions.
"""

import os
import sys
import json
import unittest
import tempfile
import subprocess

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))
from memory_buffer import (
    MemoryBufferTracker,
    MemoryBufferExporter,
    run_buffer_monitor,
)


class TestMemoryBuffer(unittest.TestCase):

    def setUp(self):
        self.spatial_sample = (
            "# High Contrast Spatial Architecture\n"
            "> **BLUF:** Balanced dual-channel cognitive working memory offload.\n\n"
            "## Core Spatial Nodes\n"
            "- Node 1: Visual sketchpad mapping with coordinate anchoring.\n"
            "- Node 2: Real-time dual-channel buffer telemetry.\n"
            "- Node 3: 4-4-4-4 Box Breathing recovery triggers.\n\n"
            "| Metric | Target | Current |\n"
            "| :--- | :--- | :--- |\n"
            "| Asymmetry | <0.30 | 0.15 |\n"
            "| Phono Load | <50% | 28% |\n"
        )

        self.dense_unbroken_sample = (
            "Linear text blocks with uninterrupted phrasing create an immediate accumulation of phonological "
            "subvocalization pressure that taxes working memory capacity because human working memory cannot "
            "maintain more than four acoustic chunks simultaneously without rapid cognitive fatigue and decoding degradation. "
            "When non-linear thinkers attempt to read extensive walls of text without structural spatial anchors, tables, "
            "or diagrams, their attentional stamina decreases exponentially resulting in severe cognitive overload and burnout."
        )

    def test_buffer_evaluation_spatial(self):
        result = MemoryBufferTracker.evaluate_buffer(
            self.spatial_sample,
            session_minutes=15.0,
            uninterrupted_minutes=10.0
        )
        m = result["metrics"]

        self.assertIn(m["exhaustion_risk"], ["Optimal", "Moderate"])
        self.assertGreaterEqual(result["spatial_anchors"], 3)
        self.assertGreater(m["visuospatial_utilization_pct"], 20.0)
        self.assertLessEqual(m["recommended_reset_seconds"], 30)

    def test_buffer_evaluation_critical_fatigue(self):
        result = MemoryBufferTracker.evaluate_buffer(
            self.dense_unbroken_sample,
            session_minutes=60.0,
            uninterrupted_minutes=50.0
        )
        m = result["metrics"]

        self.assertEqual(m["exhaustion_risk"], "Critical")
        self.assertGreaterEqual(m["phonological_saturation_pct"], 75.0)
        self.assertEqual(m["recommended_reset_seconds"], 120)
        self.assertIn("Immediate cognitive reset required", result["action_prompt"])

    def test_canvas_export(self):
        telemetry = MemoryBufferTracker.evaluate_buffer(self.spatial_sample)
        canvas = MemoryBufferExporter.to_canvas(telemetry, title="Buffer Test Canvas")

        self.assertIn("nodes", canvas)
        self.assertIn("edges", canvas)
        self.assertEqual(len(canvas["nodes"]), 4)
        self.assertEqual(len(canvas["edges"]), 3)

        root = [n for n in canvas["nodes"] if n["id"] == "node-buffer-root"][0]
        self.assertIn("Buffer Test Canvas", root["text"])

    def test_svg_hud_export(self):
        telemetry = MemoryBufferTracker.evaluate_buffer(self.spatial_sample)
        svg = MemoryBufferExporter.to_svg_hud(telemetry, title="HUD Test")

        self.assertTrue(svg.startswith("<svg"))
        self.assertTrue(svg.endswith("</svg>"))
        self.assertIn("HUD Test", svg)
        self.assertIn("Phonological Loop Saturation", svg)
        self.assertIn("Visuospatial Sketchpad Utilization", svg)
        self.assertIn("CHANNEL ASYMMETRY", svg)

    def test_run_buffer_pipeline(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            out_canvas = os.path.join(tmpdir, "buf.canvas")
            out_svg = os.path.join(tmpdir, "hud.svg")

            telemetry, canvas_data, svg_code = run_buffer_monitor(
                self.spatial_sample,
                session_minutes=25.0,
                uninterrupted_minutes=20.0,
                title="CI Pipeline Check",
                output_canvas=out_canvas,
                output_svg=out_svg
            )

            self.assertTrue(os.path.exists(out_canvas))
            self.assertTrue(os.path.exists(out_svg))

            with open(out_canvas, "r", encoding="utf-8") as f:
                saved = json.load(f)
            self.assertEqual(len(saved["nodes"]), 4)

    def test_cli_buffer_integration(self):
        cli_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts", "dx_cli.py"))
        with tempfile.TemporaryDirectory() as tmpdir:
            out_canvas = os.path.join(tmpdir, "cli_buf.canvas")
            res = subprocess.run(
                [
                    sys.executable,
                    cli_path,
                    "buffer",
                    self.spatial_sample,
                    "--minutes", "20",
                    "--title", "CLI Buffer Test",
                    "--canvas", out_canvas
                ],
                capture_output=True,
                text=True
            )
            self.assertEqual(res.returncode, 0, f"CLI stderr: {res.stderr}")
            self.assertIn("[DxSkills] Buffer evaluated:", res.stdout)
            self.assertTrue(os.path.exists(out_canvas))

    def test_zero_em_dash_compliance(self):
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts", "memory_buffer.py"))
        with open(script_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertNotIn(chr(8212), content, f"Em dash found in {script_path}")

        with open(__file__, "r", encoding="utf-8") as f:
            test_content = f.read()
        self.assertNotIn(chr(8212), test_content, "Em dash found in test file")


if __name__ == "__main__":
    unittest.main()
