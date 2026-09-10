"""
Tests for Autonomous Multimodal Spatial Lecture & Deck Decompiler.
Strict zero em dash compliance verified across all test assertions.
"""

import os
import sys
import json
import unittest
import tempfile
import subprocess

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))
from deck_decompiler import (
    SlideDeckParser,
    SpatialTopologyDecompiler,
    DeckSummaryExporter,
    decompile_deck,
)


class TestDeckDecompiler(unittest.TestCase):

    def setUp(self):
        self.sample_markdown_deck = (
            "# Slide 1: Mission Overview\n"
            "- Core objective: Decouple spatial reasoning from linear slide decks.\n"
            "- Empower dyslexic and visual thinkers.\n\n"
            "---\n\n"
            "# Slide 2: Core System Architecture\n"
            "- Multi-vault graph topology mapper.\n"
            "- Bi-directional wikilink synchronization engine.\n\n"
            "---\n\n"
            "# Slide 3: Deep Dive: Vector Embedding Telemetry\n"
            "- Benchmarking TF-IDF and Szymkiewicz-Simpson similarity.\n"
            "- Sub-millisecond cluster latency verification.\n\n"
            "---\n\n"
            "# Slide 4: Strategic Deployment Milestones\n"
            "- Rollout standalone local CLI and Obsidian canvas exporter.\n"
            "- Launch progressive web app with offline service worker."
        )

        self.sample_html_deck = (
            "<section><h2>Lecture 1: Introduction</h2><p>Welcome to spatial computing.</p></section>"
            "<section><h2>Lecture 2: Core Architecture</h2><p>Graph database fundamentals.</p></section>"
        )

    def test_slide_deck_parser_markdown(self):
        parser = SlideDeckParser(self.sample_markdown_deck)
        slides = parser.parse()

        self.assertEqual(len(slides), 4)
        self.assertEqual(slides[0]["title"], "Slide 1: Mission Overview")
        self.assertEqual(slides[0]["category"], "Overview")
        self.assertEqual(slides[1]["category"], "Architecture")
        self.assertEqual(slides[2]["category"], "Deep Dive")
        self.assertEqual(slides[3]["category"], "Action")

        for s in slides:
            self.assertIn("bluf", s)
            self.assertIn("bullets", s)
            self.assertIn("keywords", s)

    def test_slide_deck_parser_html_sections(self):
        parser = SlideDeckParser(self.sample_html_deck)
        slides = parser.parse()

        self.assertEqual(len(slides), 2)
        self.assertEqual(slides[0]["title"], "Lecture 1: Introduction")
        self.assertEqual(slides[1]["title"], "Lecture 2: Core Architecture")

    def test_spatial_topology_decompiler_layout(self):
        parser = SlideDeckParser(self.sample_markdown_deck)
        slides = parser.parse()

        canvas = SpatialTopologyDecompiler.decompile_to_canvas(slides, deck_title="Mission Brief")
        self.assertIn("nodes", canvas)
        self.assertIn("edges", canvas)

        # Header node + 4 slide nodes
        self.assertEqual(len(canvas["nodes"]), 5)

        # Edges should include sequential flow and deep dive branch
        edges = canvas["edges"]
        labels = [e.get("label", "") for e in edges]
        self.assertTrue(any("narrative flow" in l for l in labels))
        self.assertTrue(any("technical branch" in l for l in labels))

    def test_deck_summary_exporter_markdown(self):
        parser = SlideDeckParser(self.sample_markdown_deck)
        slides = parser.parse()

        md = DeckSummaryExporter.to_markdown(slides, deck_title="Mission Brief")
        self.assertIn("# Spatial Deck Decompilation: Mission Brief", md)
        self.assertIn("Conceptual Spine & Milestones", md)
        self.assertIn("Modular Spatial Nodes", md)
        self.assertNotIn(chr(8212), md)

    def test_deck_summary_exporter_svg(self):
        parser = SlideDeckParser(self.sample_markdown_deck)
        slides = parser.parse()
        canvas = SpatialTopologyDecompiler.decompile_to_canvas(slides, deck_title="Mission Brief")

        svg = DeckSummaryExporter.to_svg(canvas)
        self.assertIn("<svg", svg)
        self.assertIn("</svg>", svg)
        self.assertIn("<rect", svg)
        self.assertNotIn(chr(8212), svg)

    def test_decompile_deck_file_outputs(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            c_file = os.path.join(tmpdir, "deck.canvas")
            s_file = os.path.join(tmpdir, "deck.svg")
            m_file = os.path.join(tmpdir, "deck.md")

            slides, canvas_data, md_summary = decompile_deck(
                self.sample_markdown_deck,
                deck_title="File Test Deck",
                output_canvas=c_file,
                output_svg=s_file,
                output_markdown=m_file
            )

            self.assertTrue(os.path.isfile(c_file))
            self.assertTrue(os.path.isfile(s_file))
            self.assertTrue(os.path.isfile(m_file))

            with open(m_file, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertNotIn(chr(8212), content)

    def test_cli_decompile_command(self):
        cli_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts", "dx_cli.py"))
        res = subprocess.run(
            [sys.executable, cli_path, "decompile", "--title", "CLI Decompile Test"],
            capture_output=True,
            text=True,
            check=True
        )
        self.assertEqual(res.returncode, 0)
        self.assertIn("Spatial Deck Decompilation: CLI Decompile Test", res.stdout)
        self.assertNotIn(chr(8212), res.stdout)

    def test_zero_em_dash_in_source(self):
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts", "deck_decompiler.py"))
        if os.path.exists(script_path):
            with open(script_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertNotIn(chr(8212), content, "Found em dash in scripts/deck_decompiler.py")


if __name__ == "__main__":
    unittest.main()
