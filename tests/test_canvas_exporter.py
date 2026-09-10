#!/usr/bin/env python3
"""
DxSkills Automated Spatial Mindmap & Obsidian Canvas Exporter Test Suite
Verifies .canvas JSON schema compliance, 2D coordinates, directional edges,
SVG vector output, DOM landmarks in index.html, and strict zero em dash compliance.
"""

import os
import sys
import json
import unittest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from scripts.canvas_exporter import parse_markdown_to_spatial_graph, generate_obsidian_canvas, generate_svg_canvas

INDEX_PATH = os.path.join(ROOT_DIR, "index.html")

class TestCanvasExporter(unittest.TestCase):

    def setUp(self):
        self.sample_doc = (
            "# Autonomous Drone Fleet\n"
            "> **BLUF:** Deploy swarm intelligence coordinator by Q4.\n\n"
            "## Mesh Networking\n"
            "- Ultra-wideband telemetry links\n"
            "- Dynamic topology routing\n\n"
            "## Collision Avoidance\n"
            "- Stereo depth vision sensor\n"
            "- Microsecond optical flow tracking\n"
        )

    def test_parse_markdown_to_spatial_graph(self):
        """Verifies decomposition into hierarchical nodes and directional edges."""
        graph = parse_markdown_to_spatial_graph(self.sample_doc, title="Swarm Robotics")
        self.assertIn("nodes", graph)
        self.assertIn("edges", graph)

        nodes = graph["nodes"]
        edges = graph["edges"]

        self.assertGreaterEqual(len(nodes), 3)
        self.assertGreaterEqual(len(edges), 2)

        # Check Root node
        root = nodes[0]
        self.assertTrue(root["id"].startswith("node-root-"))
        self.assertIn("Swarm Robotics", root["text"])
        self.assertIn("Deploy swarm intelligence", root["text"])
        self.assertEqual(root["color"], "1")
        self.assertGreater(root["width"], 200)

        # Check section node
        sec = next(n for n in nodes if n["id"].startswith("node-sec-"))
        self.assertIn("Mesh Networking", sec["text"])
        self.assertEqual(sec["color"], "4")

        # Check edges have valid connections
        node_ids = {n["id"] for n in nodes}
        for e in edges:
            self.assertIn(e["fromNode"], node_ids)
            self.assertIn(e["toNode"], node_ids)
            self.assertEqual(e["fromSide"], "right")
            self.assertEqual(e["toSide"], "left")

    def test_generate_obsidian_canvas_json(self):
        """Verifies valid JSON and official Obsidian Canvas specification fields."""
        json_str = generate_obsidian_canvas(self.sample_doc, title="Drone Fleet")
        data = json.loads(json_str)

        self.assertIsInstance(data, dict)
        self.assertIn("nodes", data)
        self.assertIn("edges", data)

        for node in data["nodes"]:
            self.assertIn("id", node)
            self.assertIn("type", node)
            self.assertEqual(node["type"], "text")
            self.assertIn("x", node)
            self.assertIn("y", node)
            self.assertIn("width", node)
            self.assertIn("height", node)
            self.assertIn("text", node)

    def test_generate_svg_canvas(self):
        """Verifies vector SVG output format."""
        graph = parse_markdown_to_spatial_graph(self.sample_doc)
        svg = generate_svg_canvas(graph, width=1200, height=800)

        self.assertTrue(svg.startswith("<svg"))
        self.assertTrue(svg.endswith("</svg>"))
        self.assertIn('viewBox="0 0 1200 800"', svg)
        self.assertIn('marker id="arrow"', svg)
        self.assertIn("<rect", svg)
        self.assertIn("<path", svg)

    def test_html_canvas_dom_elements(self):
        """Verifies presence of Spatial Canvas view and controllers in index.html."""
        self.assertTrue(os.path.isfile(INDEX_PATH), "index.html must exist")
        with open(INDEX_PATH, "r", encoding="utf-8") as f:
            html = f.read()

        required_elements = [
            'id="sim-tab-canvas"',
            'id="sim-view-canvas"',
            'id="canvas-svg-container"',
            'id="canvas-node-type-badge"',
            'id="canvas-node-id"',
            'id="canvas-node-text"',
            'id="canvas-node-edges"',
            'switchSimulatorView(\'canvas\')',
            'renderInteractiveCanvas()',
            'switchCanvasPreset(',
            'selectCanvasNode(',
            'downloadObsidianCanvasFile()',
            'downloadCanvasSvgFile()',
            'copyCanvasJson()',
            'sendCanvasToPlayground()',
            'Spatial Canvas Visualizer',
        ]
        for elem in required_elements:
            self.assertIn(elem, html, f"Missing canvas UI element: {elem}")

    def test_zero_em_dashes(self):
        """Verifies strict zero em dash constraint."""
        em_dash = "\u2014"
        files_to_check = [
            os.path.join(ROOT_DIR, "scripts", "canvas_exporter.py"),
            os.path.join(ROOT_DIR, "tests", "test_canvas_exporter.py"),
        ]
        for path in files_to_check:
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                self.assertNotIn(em_dash, content, f"{path} must contain zero em dashes")

if __name__ == "__main__":
    unittest.main()
