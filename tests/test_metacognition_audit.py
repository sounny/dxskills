"""
Tests for Autonomous Cognitive Metacognition and Synthesis Audit Suite.
Strict zero em dash compliance verified across all test assertions.
"""

import os
import sys
import json
import unittest
import tempfile
import subprocess

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))
from metacognition_audit import (
    MetacognitionAuditor,
    MetacognitionExporter,
    run_audit,
)


class TestMetacognitionAudit(unittest.TestCase):

    def setUp(self):
        self.spatial_text = (
            "# Strategic Spatial Deliverable\n"
            "> **BLUF:** Decouple phonological working memory from spatial reasoning models.\n\n"
            "## Architectural Vectors\n"
            "- 1. High-contrast spatial canvas topology.\n"
            "- 2. Automated cross-vault synchronization without manual ID linking.\n"
            "- 3. Lossless multi-modal audio-spatial flashcards.\n\n"
            "| Pillar | Latency | Status |\n"
            "| :--- | :--- | :--- |\n"
            "| Canvas | 0ms | Active |\n"
            "| Audio | 12ms | Verified |\n\n"
            "Associative reference to [[SpatialMemory]] and [[CognitiveOffload]]."
        )

        self.dense_wall_of_text = (
            "We must utilize and leverage our synergy to operationalize a disruptive multifaceted paradigm "
            "notwithstanding the difficulties that have heretofore presented substantial resistance to our "
            "organizational capacity to execute long-term strategic initiatives across diverse institutional sectors. "
            "This overarching systematic operational framework will encompass every individual component in an "
            "interconnected architecture that will facilitate continuous evaluation without interruption."
        )

    def test_auditor_spatial_text(self):
        result = MetacognitionAuditor.audit_text(self.spatial_text, title="Spatial Test")
        m = result["metrics"]

        self.assertGreater(m["cognitive_leverage_score"], 60.0)
        self.assertGreater(m["spatial_leverage"], 40.0)
        self.assertLess(m["working_memory_tax"], 60.0)
        self.assertGreaterEqual(result["spatial_features"]["bullet_points"], 3)
        self.assertGreaterEqual(result["spatial_features"]["headers"], 2)
        self.assertGreaterEqual(result["spatial_features"]["wikilinks"], 2)

    def test_auditor_wall_of_text(self):
        result = MetacognitionAuditor.audit_text(self.dense_wall_of_text, title="Dense Wall Test")
        m = result["metrics"]

        # Jargon and long sentences should trigger higher friction and lower spatial leverage
        self.assertGreater(m["phonological_friction"], 40.0)
        self.assertEqual(result["spatial_features"]["bullet_points"], 0)
        self.assertEqual(result["spatial_features"]["headers"], 0)
        self.assertTrue(len(result["recommendations"]) > 0)

    def test_empty_audit(self):
        result = MetacognitionAuditor.audit_text("", title="Empty Test")
        self.assertEqual(result["word_count"], 0)
        self.assertEqual(result["metrics"]["cognitive_leverage_score"], 0.0)

    def test_canvas_exporter(self):
        result = MetacognitionAuditor.audit_text(self.spatial_text)
        canvas = MetacognitionExporter.to_canvas(result)

        self.assertIn("nodes", canvas)
        self.assertIn("edges", canvas)
        self.assertEqual(len(canvas["nodes"]), 4)
        self.assertEqual(len(canvas["edges"]), 3)

        root = [n for n in canvas["nodes"] if n["id"] == "node-audit-root"][0]
        self.assertIn("Cognitive Leverage Score", root["text"])

    def test_svg_dashboard_exporter(self):
        result = MetacognitionAuditor.audit_text(self.spatial_text, title="Vector SVG Test")
        svg = MetacognitionExporter.to_svg_dashboard(result)

        self.assertTrue(svg.startswith("<svg"))
        self.assertTrue(svg.endswith("</svg>"))
        self.assertIn("Vector SVG Test", svg)
        self.assertIn("Working Memory Stamina Tax", svg)

    def test_run_audit_pipeline(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            out_canvas = os.path.join(tmpdir, "scorecard.canvas")
            out_svg = os.path.join(tmpdir, "dashboard.svg")

            audit_data, canvas_data, svg_code = run_audit(
                self.spatial_text,
                title="Pipeline Verification",
                output_canvas=out_canvas,
                output_svg=out_svg
            )

            self.assertTrue(os.path.exists(out_canvas))
            self.assertTrue(os.path.exists(out_svg))

            with open(out_canvas, "r", encoding="utf-8") as f:
                saved = json.load(f)
            self.assertEqual(len(saved["nodes"]), 4)

    def test_cli_audit_command(self):
        cli_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts", "dx_cli.py"))
        with tempfile.TemporaryDirectory() as tmpdir:
            out_canvas = os.path.join(tmpdir, "cli.canvas")
            res = subprocess.run(
                [
                    sys.executable,
                    cli_path,
                    "audit",
                    self.spatial_text,
                    "--title", "CLI Audit Verification",
                    "--canvas", out_canvas
                ],
                capture_output=True,
                text=True
            )
            self.assertEqual(res.returncode, 0, f"CLI stderr: {res.stderr}")
            self.assertIn("Completed audit", res.stdout)
            self.assertTrue(os.path.exists(out_canvas))

    def test_zero_em_dash_compliance(self):
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts", "metacognition_audit.py"))
        with open(script_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertNotIn(chr(8212), content, f"Em dash found in {script_path}")

        with open(__file__, "r", encoding="utf-8") as f:
            test_content = f.read()
        self.assertNotIn(chr(8212), test_content, "Em dash found in test file")


if __name__ == "__main__":
    unittest.main()
