"""
Tests for Multi-Modal Audio-Spatial Flashcard & Rapid Retrieval Engine.
Strict zero em dash compliance verified across all test assertions.
"""

import os
import sys
import json
import unittest
import tempfile
import subprocess

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))
from spatial_flashcards import (
    FlashcardGenerator,
    SpatialFlashcardExporter,
    run_flashcards,
)


class TestSpatialFlashcards(unittest.TestCase):

    def setUp(self):
        self.sample_qa_text = (
            "Spatial Anchoring :: Relational coordinate mapping in working memory\n"
            "Acoustic Rhythm -> Phonetic cadence reducing decoding friction\n"
            "- Working Memory Stamina: Cognitive capacity limit before fatigue reset\n"
            "- Multi-Vault Sync: Cross-repository graph topology resolution"
        )

    def test_flashcard_generator_parsing(self):
        cards = FlashcardGenerator.generate_cards(self.sample_qa_text)
        self.assertEqual(len(cards), 4)

        c1 = cards[0]
        self.assertEqual(c1["front"], "Spatial Anchoring")
        self.assertEqual(c1["back"], "Relational coordinate mapping in working memory")
        self.assertIn("sector", c1)
        self.assertIn("acoustic_cue", c1)
        self.assertIn("svg_clue", c1)
        self.assertEqual(c1["box"], 1)

    def test_flashcard_canvas_exporter(self):
        cards = FlashcardGenerator.generate_cards(self.sample_qa_text)
        canvas = SpatialFlashcardExporter.to_canvas(cards, deck_title="Cognitive Science Deck")

        self.assertIn("nodes", canvas)
        self.assertIn("edges", canvas)
        # Header node + 4 card nodes
        self.assertEqual(len(canvas["nodes"]), 5)

        header_node = [n for n in canvas["nodes"] if n["id"] == "node-deck-header"][0]
        self.assertIn("Cognitive Science Deck", header_node["text"])

        # Check edge labels include Leitner Box
        edge = canvas["edges"][0]
        self.assertIn("Leitner Box", edge["label"])

    def test_flashcard_html_exporter(self):
        cards = FlashcardGenerator.generate_cards(self.sample_qa_text)
        html = SpatialFlashcardExporter.to_html(cards, deck_title="Cognitive Science Deck")

        self.assertIn("<!DOCTYPE html>", html)
        self.assertIn("Spatial Retrieval Session", html)
        self.assertIn("flipCard()", html)
        self.assertNotIn(chr(8212), html)

    def test_run_flashcards_file_exports(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            c_file = os.path.join(tmpdir, "deck.canvas")
            h_file = os.path.join(tmpdir, "deck.html")

            cards, canvas_data, html_code = run_flashcards(
                self.sample_qa_text,
                title="Test Flashcard Deck",
                output_canvas=c_file,
                output_html=h_file
            )

            self.assertTrue(os.path.isfile(c_file))
            self.assertTrue(os.path.isfile(h_file))

            with open(h_file, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertNotIn(chr(8212), content)

    def test_cli_cards_command(self):
        cli_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts", "dx_cli.py"))
        res = subprocess.run(
            [sys.executable, cli_path, "cards", "--title", "CLI Cards Test"],
            capture_output=True,
            text=True,
            check=True
        )
        self.assertEqual(res.returncode, 0)
        self.assertIn("DxSkills: Spatial Flashcard Deck", res.stdout)
        self.assertNotIn(chr(8212), res.stdout)

    def test_zero_em_dash_in_source(self):
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts", "spatial_flashcards.py"))
        if os.path.exists(script_path):
            with open(script_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertNotIn(chr(8212), content, "Found em dash in scripts/spatial_flashcards.py")


if __name__ == "__main__":
    unittest.main()
