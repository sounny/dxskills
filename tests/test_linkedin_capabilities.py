#!/usr/bin/env python3
"""
Test suite for DxSkills leader archetypes and LinkedIn promised capabilities.

Validates:
1. Gavin Newsom: 4-Room spatial memory storyboard, color anchors, and Mermaid diagram.
2. Richard Branson: Back-of-a-Beer-Mat / Napkin test, unit economics, and value flow.
3. Steve Jobs: Executive Markdown Spec, whole-system metaphor, and tradeoff matrix.
4. Ingvar Kamprad: Mnemonic taxonomy, physical categories, and pictorial assembly schemas.
5. Richard Branson: Conversational financial executive digest and cash-flow funnel.
6. Zero em dash compliance across all templates, CLI commands, and web portal.
"""

import os
import sys
import json
import unittest
import subprocess

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

CLI_SCRIPT = os.path.join(ROOT_DIR, "scripts", "dx_cli.py")
INDEX_PATH = os.path.join(ROOT_DIR, "index.html")


class TestLinkedInCapabilities(unittest.TestCase):
    """Verifies all cognitive capabilities promised in public LinkedIn updates."""

    def run_cli(self, args):
        """Helper to run dx_cli.py as a subprocess and capture stdout."""
        cmd = [sys.executable, CLI_SCRIPT] + args
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8"
        )
        self.assertEqual(
            result.returncode, 0,
            f"CLI failed with code {result.returncode}. Stderr: {result.stderr}"
        )
        return result.stdout

    def test_newsom_storyboard_cli(self):
        """Verifies Gavin Newsom 4-room spatial memory and speech scaffolding."""
        # Test JSON telemetry output
        out_json = self.run_cli(["storyboard", "--title", "Clean Energy Address", "--json"])
        data = json.loads(out_json)

        self.assertIn("title", data)
        self.assertIn("bluf", data)
        self.assertIn("rooms", data)
        self.assertIn("mermaid", data)

        rooms = data["rooms"]
        self.assertEqual(rooms["room1"]["name"], "Context Porch")
        self.assertEqual(rooms["room2"]["name"], "Catalyst Atrium")
        self.assertEqual(rooms["room3"]["name"], "Engine Hall")
        self.assertEqual(rooms["room4"]["name"], "Horizon Terrace")

        # Test Markdown formatted output
        out_md = self.run_cli(["storyboard", "--title", "Clean Energy Address"])
        self.assertIn("Gavin Newsom", out_md)
        self.assertIn("Context Porch", out_md)
        self.assertIn("Catalyst Atrium", out_md)
        self.assertIn("Engine Hall", out_md)
        self.assertIn("Horizon Terrace", out_md)
        self.assertIn("graph LR", out_md)
        self.assertIn("Executive Speaking Cards (Zero Teleprompter)", out_md)
        self.assertIn("Color-Coded Thematic Concept Blocks", out_md)
        self.assertEqual(out_md.count("\u2014"), 0, "Disallowed em dash found in storyboard output")

    def test_branson_napkin_cli(self):
        """Verifies Richard Branson back-of-the-beer-mat test and radical simplification."""
        # Test JSON telemetry output
        out_json = self.run_cli(["napkin", "--price", "10.0", "--cost", "1.50", "--json"])
        data = json.loads(out_json)

        self.assertIn("value_exchange", data)
        self.assertIn("unit_economics", data)
        econ = data["unit_economics"]
        self.assertEqual(econ["price"], 10.0)
        self.assertEqual(econ["cost"], 1.5)
        self.assertEqual(econ["margin"], 8.5)
        self.assertEqual(econ["margin_pct"], 85)

        # Test Markdown formatted output
        out_md = self.run_cli(["napkin", "--price", "10.0", "--cost", "1.50"])
        self.assertIn("Richard Branson", out_md)
        self.assertIn("THE BEER MAT TEST", out_md)
        self.assertIn("CORE VALUE EXCHANGE", out_md)
        self.assertIn("THREE ESSENTIAL LEVERS", out_md)
        self.assertIn("BACK-OF-THE-ENVELOPE MATH", out_md)
        self.assertIn("THE ACID TEST", out_md)
        self.assertIn("Radical Simplification Matrix", out_md)
        self.assertIn("graph LR", out_md)
        self.assertEqual(out_md.count("\u2014"), 0, "Disallowed em dash found in napkin output")

    def test_jobs_spec_cli(self):
        """Verifies Steve Jobs Executive Markdown Spec and whole-system spatial architecture."""
        # Test JSON telemetry output
        out_json = self.run_cli(["spec", "--title", "Edge Cognitive Mesh", "--json"])
        data = json.loads(out_json)

        self.assertIn("bluf", data)
        self.assertIn("mermaid", data)
        self.assertIn("tradeoffs", data)
        self.assertGreaterEqual(len(data["tradeoffs"]), 3)

        # Test Markdown formatted output
        out_md = self.run_cli(["spec", "--title", "Edge Cognitive Mesh"])
        self.assertIn("Steve Jobs", out_md)
        self.assertIn("Whole-System Spatial Metaphor", out_md)
        self.assertIn("Technical Tradeoff & Decision Matrix", out_md)
        self.assertIn("State Persistence", out_md)
        self.assertIn("Executive Specification Breakdown", out_md)
        self.assertIn("graph TD", out_md)
        self.assertEqual(out_md.count("\u2014"), 0, "Disallowed em dash found in spec output")

    def test_kamprad_taxonomy_cli(self):
        """Verifies Ingvar Kamprad visual mnemonic taxonomy and pictorial assembly schemas."""
        # Test JSON telemetry output
        out_json = self.run_cli(["taxonomy", "--title", "Cloud Cluster Setup", "--json"])
        data = json.loads(out_json)

        self.assertIn("taxonomy", data)
        self.assertIn("mermaid", data)
        self.assertGreaterEqual(len(data["taxonomy"]), 3)

        # Test Markdown formatted output
        out_md = self.run_cli(["taxonomy", "--title", "Cloud Cluster Setup"])
        self.assertIn("Ingvar Kamprad", out_md)
        self.assertIn("Visual Mnemonic Taxonomy", out_md)
        self.assertIn("Pictorial Assembly Schema", out_md)
        self.assertIn("River Delta", out_md)
        self.assertIn("The Workbench", out_md)
        self.assertIn("The Archive Vault", out_md)
        self.assertIn("Spatial Volume & Geometric Verification", out_md)
        self.assertIn("graph TD", out_md)
        self.assertEqual(out_md.count("\u2014"), 0, "Disallowed em dash found in taxonomy output")

    def test_branson_finance_cli(self):
        """Verifies Richard Branson conversational financial executive digest."""
        # Test JSON telemetry output
        out_json = self.run_cli(["finance", "--title", "Annual Operating Review", "--json"])
        data = json.loads(out_json)

        self.assertIn("metrics", data)
        self.assertIn("mermaid", data)
        m = data["metrics"]
        self.assertGreater(m["revenue"], 0)
        self.assertGreater(m["net_profit"], 0)
        self.assertGreater(m["cash_balance"], 0)

        # Test Markdown formatted output
        out_md = self.run_cli(["finance", "--title", "Annual Operating Review"])
        self.assertIn("Richard Branson", out_md)
        self.assertIn("The Operating Funnel", out_md)
        self.assertIn("Conversational Financial Matrix", out_md)
        self.assertIn("The Four Boardroom Answers", out_md)
        self.assertIn("Visual Cash-Flow Topology", out_md)
        self.assertIn("graph TD", out_md)
        self.assertEqual(out_md.count("\u2014"), 0, "Disallowed em dash found in finance output")

    def test_archetype_template_files_exist(self):
        """Verifies all 5 modular archetype template files exist and are em-dash free."""
        expected_templates = [
            os.path.join(ROOT_DIR, "skills", "dx-map", "templates", "visual_spatial_storyboard.md"),
            os.path.join(ROOT_DIR, "skills", "dx-dump", "templates", "napkin_beer_mat_test.md"),
            os.path.join(ROOT_DIR, "skills", "dx-dump", "templates", "executive_markdown_spec.md"),
            os.path.join(ROOT_DIR, "skills", "dx-map", "templates", "mnemonic_taxonomy_schema.md"),
            os.path.join(ROOT_DIR, "skills", "dx-read", "templates", "financial_conversational_digest.md"),
        ]

        for tmpl_path in expected_templates:
            self.assertTrue(os.path.isfile(tmpl_path), f"Missing template file: {tmpl_path}")
            with open(tmpl_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertEqual(
                content.count("\u2014"), 0,
                f"Disallowed Unicode em dash (U+2014) in template: {tmpl_path}"
            )

    def test_web_portal_archetype_integration(self):
        """Verifies index.html has presets, diagrams, and zero em dashes."""
        self.assertTrue(os.path.isfile(INDEX_PATH), "Missing index.html")
        with open(INDEX_PATH, "r", encoding="utf-8") as f:
            content = f.read()

        # Check for archetype preset buttons and samples
        self.assertIn("newsom", content)
        self.assertIn("branson", content)
        self.assertIn("jobs", content)
        self.assertIn("kamprad", content)
        self.assertIn("finance", content)

        # Check for diagram views
        self.assertIn("diag-view-storyboard", content)
        self.assertIn("diag-view-napkin", content)
        self.assertIn("diag-view-spec", content)
        self.assertIn("diag-view-taxonomy", content)
        self.assertIn("diag-view-finance", content)

        # Strictly zero em dashes across web portal
        self.assertEqual(
            content.count("\u2014"), 0,
            "Disallowed Unicode em dash (U+2014) found in index.html"
        )


if __name__ == "__main__":
    unittest.main()
