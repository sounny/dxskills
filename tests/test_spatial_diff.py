"""
Tests for Spatial Cognitive Architecture Graph Differential Engine.
Strict zero em dash compliance verified across all test assertions.
"""

import os
import sys
import json
import unittest
import tempfile
import subprocess

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))
from spatial_diff import (
    SpatialGraphDiffer,
    VisualMergeResolver,
    run_spatial_diff,
)


class TestSpatialDiff(unittest.TestCase):

    def setUp(self):
        self.canvas_a = {
            "nodes": [
                {"id": "node-1", "type": "text", "text": "Linear Architecture", "x": 0, "y": 0, "color": "1"},
                {"id": "node-2", "type": "text", "text": "Phonological Buffer", "x": 300, "y": 0, "color": "2"},
                {"id": "node-3", "type": "text", "text": "Sequential Pipeline", "x": 600, "y": 0, "color": "3"}
            ],
            "edges": [
                {"id": "e1", "fromNode": "node-1", "toNode": "node-2"},
                {"id": "e2", "fromNode": "node-2", "toNode": "node-3"}
            ]
        }

        self.canvas_b = {
            "nodes": [
                # node-1 content modified
                {"id": "node-1", "type": "text", "text": "Spatial Architecture (Updated)", "x": 0, "y": 0, "color": "1"},
                # node-2 relocated spatially (dx = 200, dy = 100)
                {"id": "node-2", "type": "text", "text": "Phonological Buffer", "x": 500, "y": 100, "color": "2"},
                # node-3 removed
                # node-4 added
                {"id": "node-4", "type": "text", "text": "Constellation Topology", "x": 800, "y": 200, "color": "4"}
            ],
            "edges": [
                # e1 retained
                {"id": "e1", "fromNode": "node-1", "toNode": "node-2"},
                # e2 removed (node-3 is gone)
                # e3 added
                {"id": "e3", "fromNode": "node-2", "toNode": "node-4"}
            ]
        }

    def test_graph_differ_analysis(self):
        diff = SpatialGraphDiffer.diff_canvases(self.canvas_a, self.canvas_b)

        summary = diff["summary"]
        self.assertEqual(summary["nodes_before"], 3)
        self.assertEqual(summary["nodes_after"], 3)
        self.assertEqual(summary["nodes_added"], 1)
        self.assertEqual(summary["nodes_removed"], 1)
        self.assertEqual(summary["nodes_modified"], 1)
        self.assertEqual(summary["nodes_relocated"], 1)

        self.assertEqual(summary["edges_retained"], 1)
        self.assertEqual(summary["edges_added"], 1)
        self.assertEqual(summary["edges_removed"], 1)

        # Total edges before = 2, after = 2. Retained = 1.
        # TSI = (2 * 1) / (2 + 2) = 0.5
        self.assertEqual(diff["topological_stability_index"], 0.5)
        self.assertEqual(diff["graph_drift_percentage"], 50.0)

    def test_visual_merge_resolver_canvas(self):
        diff = SpatialGraphDiffer.diff_canvases(self.canvas_a, self.canvas_b)
        merged = VisualMergeResolver.to_differential_canvas(diff, self.canvas_b, title="Test Branch Diff")

        nodes = merged["nodes"]
        edges = merged["edges"]

        header = [n for n in nodes if n["id"] == "node-diff-header"][0]
        self.assertIn("Test Branch Diff", header["text"])
        self.assertIn("Added Nodes: **+1**", header["text"])

        # Check ghost node exists for removed node-3
        ghost = [n for n in nodes if n["id"] == "ghost-node-3"][0]
        self.assertEqual(ghost["color"], "1")
        self.assertIn("[REMOVED IN REVISION]", ghost["text"])

        # Check added node is color 4
        added = [n for n in nodes if n["id"] == "node-4"][0]
        self.assertEqual(added["color"], "4")

        # Check modified node is color 3
        modified = [n for n in nodes if n["id"] == "node-1"][0]
        self.assertEqual(modified["color"], "3")

        # Check relocated node is color 5
        relocated = [n for n in nodes if n["id"] == "node-2"][0]
        self.assertEqual(relocated["color"], "5")

        # Check severed edge exists
        severed = [e for e in edges if e.get("label") == "[SEVERED LINK]"][0]
        self.assertEqual(severed["color"], "1")

    def test_svg_diff_strip_rendering(self):
        diff = SpatialGraphDiffer.diff_canvases(self.canvas_a, self.canvas_b)
        svg = VisualMergeResolver.to_svg_diff_strip(diff, title="Sprint Divergence Map")

        self.assertTrue(svg.startswith("<svg"))
        self.assertTrue(svg.endswith("</svg>"))
        self.assertIn("Sprint Divergence Map", svg)
        self.assertIn("Topological Stability Index", svg)
        self.assertIn("+1", svg)  # Added nodes
        self.assertIn("-1", svg)  # Removed nodes

    def test_run_spatial_diff_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_a = os.path.join(tmpdir, "branch_a.canvas")
            file_b = os.path.join(tmpdir, "branch_b.canvas")
            out_canvas = os.path.join(tmpdir, "diff.canvas")
            out_svg = os.path.join(tmpdir, "diff.svg")

            with open(file_a, "w", encoding="utf-8") as f:
                json.dump(self.canvas_a, f)
            with open(file_b, "w", encoding="utf-8") as f:
                json.dump(self.canvas_b, f)

            diff, merged, svg = run_spatial_diff(
                file_a,
                file_b,
                title="CI Divergence Check",
                output_canvas=out_canvas,
                output_svg=out_svg
            )

            self.assertTrue(os.path.exists(out_canvas))
            self.assertTrue(os.path.exists(out_svg))

            with open(out_canvas, "r", encoding="utf-8") as f:
                saved_canvas = json.load(f)
            self.assertGreater(len(saved_canvas["nodes"]), 3)

    def test_cli_diff_command(self):
        cli_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts", "dx_cli.py"))
        with tempfile.TemporaryDirectory() as tmpdir:
            file_a = os.path.join(tmpdir, "a.canvas")
            file_b = os.path.join(tmpdir, "b.canvas")
            out_canvas = os.path.join(tmpdir, "out.canvas")
            with open(file_a, "w", encoding="utf-8") as f:
                json.dump(self.canvas_a, f)
            with open(file_b, "w", encoding="utf-8") as f:
                json.dump(self.canvas_b, f)

            res = subprocess.run(
                [
                    sys.executable,
                    cli_path,
                    "diff",
                    file_a,
                    file_b,
                    "--title", "CLI Diff Test",
                    "--canvas", out_canvas
                ],
                capture_output=True,
                text=True
            )
            self.assertEqual(res.returncode, 0, f"CLI stderr: {res.stderr}")
            self.assertIn("Computed graph differential", res.stdout)
            self.assertTrue(os.path.exists(out_canvas))

    def test_zero_em_dash_compliance(self):
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts", "spatial_diff.py"))
        with open(script_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertNotIn(chr(8212), content, f"Em dash found in {script_path}")

        with open(__file__, "r", encoding="utf-8") as f:
            test_content = f.read()
        self.assertNotIn(chr(8212), test_content, "Em dash found in test file")


if __name__ == "__main__":
    unittest.main()
