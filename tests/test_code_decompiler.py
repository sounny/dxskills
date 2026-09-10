"""
Tests for Autonomous Spatial Multi-Modal Code Architecture Decompiler.
Strict zero em dash compliance verified across all test assertions.
"""

import os
import sys
import json
import unittest
import tempfile
import subprocess

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))
from code_decompiler import (
    CodeArchitectureDecompiler,
    CodeTopologyExporter,
    run_code_decompiler,
)


class TestCodeDecompiler(unittest.TestCase):

    def setUp(self):
        self.sample_code = """
import os
import sys
from math import sqrt

class SpatialNode:
    '''Base spatial coordinate node.'''
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, other):
        return sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

def calculate_centroid(nodes):
    '''Computes geometric center.'''
    if not nodes:
        return (0, 0)
    return (sum(n.x for n in nodes) / len(nodes), sum(n.y for n in nodes) / len(nodes))
"""

    def test_decompile_source(self):
        result = CodeArchitectureDecompiler.decompile_source(self.sample_code, module_name="test_mod")

        self.assertEqual(result["module_name"], "test_mod")
        self.assertEqual(len(result["classes"]), 1)
        self.assertEqual(result["classes"][0]["name"], "SpatialNode")
        self.assertIn("distance", result["classes"][0]["methods"])

        self.assertEqual(len(result["functions"]), 1)
        self.assertEqual(result["functions"][0]["name"], "calculate_centroid")

        self.assertGreaterEqual(len(result["imports"]), 3)

    def test_circular_dependency_detection(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            mod_a_path = os.path.join(tmpdir, "module_a.py")
            mod_b_path = os.path.join(tmpdir, "module_b.py")

            with open(mod_a_path, "w", encoding="utf-8") as f:
                f.write("import module_b\nclass A: pass\n")
            with open(mod_b_path, "w", encoding="utf-8") as f:
                f.write("import module_a\nclass B: pass\n")

            decompiled = CodeArchitectureDecompiler.decompile_project(tmpdir)

            self.assertEqual(decompiled["total_modules"], 2)
            self.assertGreaterEqual(len(decompiled["circular_cycles"]), 1)

            coupling = decompiled["coupling_metrics"]
            self.assertTrue(coupling["module_a"]["is_circular"])
            self.assertTrue(coupling["module_b"]["is_circular"])

    def test_canvas_exporter(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "sample.py")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(self.sample_code)

            decompiled, canvas_data, svg_code = run_code_decompiler(file_path, title="Canvas Test")

            self.assertIn("nodes", canvas_data)
            self.assertIn("edges", canvas_data)
            self.assertGreaterEqual(len(canvas_data["nodes"]), 2)

            header = [n for n in canvas_data["nodes"] if n["id"] == "node-code-header"][0]
            self.assertIn("Canvas Test", header["text"])

    def test_svg_diagram_exporter(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "sample.py")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(self.sample_code)

            decompiled, canvas_data, svg_code = run_code_decompiler(file_path, title="SVG Circuit Test")

            self.assertTrue(svg_code.startswith("<svg"))
            self.assertTrue(svg_code.endswith("</svg>"))
            self.assertIn("SVG Circuit Test", svg_code)
            self.assertIn("Decompiled AST Topology", svg_code)

    def test_cli_integration(self):
        cli_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts", "dx_cli.py"))
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "cli_sample.py")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(self.sample_code)

            out_canvas = os.path.join(tmpdir, "cli_arch.canvas")
            res = subprocess.run(
                [
                    sys.executable,
                    cli_path,
                    "code-arch",
                    file_path,
                    "--title", "CLI Code Test",
                    "--canvas", out_canvas
                ],
                capture_output=True,
                text=True
            )
            self.assertEqual(res.returncode, 0, f"CLI stderr: {res.stderr}")
            self.assertIn("[DxSkills] Decompiled", res.stdout)
            self.assertTrue(os.path.exists(out_canvas))

    def test_zero_em_dash_compliance(self):
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts", "code_decompiler.py"))
        with open(script_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertNotIn(chr(8212), content, f"Em dash found in {script_path}")

        with open(__file__, "r", encoding="utf-8") as f:
            test_content = f.read()
        self.assertNotIn(chr(8212), test_content, "Em dash found in test file")


if __name__ == "__main__":
    unittest.main()
