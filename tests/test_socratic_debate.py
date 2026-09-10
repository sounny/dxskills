"""
Tests for Socratic Debate & Thesis Stress-Testing Simulator.
Strict zero em dash compliance verified across all test assertions.
"""

import os
import sys
import json
import unittest
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))
from socratic_debate import (
    PropositionAnalyzer,
    SocraticDebater,
    SocraticDebateExporter,
    run_socratic_debate,
)


class TestSocraticDebate(unittest.TestCase):

    def setUp(self):
        self.sample_text = (
            "# Spatial Architecture Thesis\n"
            "- Our spatial canvas architecture effortlessly eliminates all cognitive friction for non-linear thinkers.\n"
            "- Because users navigate ideas spatially, traditional linear hierarchies will become completely obsolete.\n"
            "- The engine automatically syncs high-dimensional vector graphs without any configuration overhead."
        )

    def test_proposition_analyzer_extracts_claims(self):
        analyzer = PropositionAnalyzer(self.sample_text)
        claims = analyzer.extract_claims()
        self.assertGreaterEqual(len(claims), 2)
        
        first_claim = claims[0]
        self.assertIn("effortlessly eliminates all cognitive friction", first_claim["text"])
        self.assertGreater(len(first_claim["vulnerabilities"]), 0)
        self.assertGreaterEqual(first_claim["vulnerability_score"], 30)

    def test_claim_classification_types(self):
        text = (
            "We propose a new spatial graph model for notes.\n"
            "This will guarantee zero data loss across vaults.\n"
            "Because Baddeley working memory limits phonological bandwidth, spatial anchors are vital."
        )
        analyzer = PropositionAnalyzer(text)
        claims = analyzer.extract_claims()
        claim_types = [c["type"] for c in claims]
        
        self.assertIn("Exploratory Hypothesis", claim_types)
        self.assertIn("Strong Predictive", claim_types)
        self.assertIn("Causal Premise", claim_types)

    def test_socratic_debater_generates_matrix(self):
        analyzer = PropositionAnalyzer(self.sample_text)
        claims = analyzer.extract_claims()
        debater = SocraticDebater("Spatial Canvas Architecture", claims)
        debate_data = debater.generate_debate()

        self.assertEqual(debate_data["topic"], "Spatial Canvas Architecture")
        self.assertEqual(debate_data["total_claims"], len(claims))
        self.assertTrue(0 <= debate_data["thesis_readiness_score"] <= 100)

        matrix = debate_data["matrix"]
        self.assertEqual(len(matrix), len(claims))
        for item in matrix:
            self.assertIn("claim_id", item)
            self.assertIn("skeptic_attack", item)
            self.assertIn("pragmatist_challenge", item)
            self.assertIn("steel_manned_defense", item)
            self.assertIn("required_proof_artifact", item)

    def test_markdown_export_format(self):
        analyzer = PropositionAnalyzer(self.sample_text)
        claims = analyzer.extract_claims()
        debater = SocraticDebater("Spatial Architecture", claims)
        debate_data = debater.generate_debate()

        md = SocraticDebateExporter.to_markdown(debate_data)
        self.assertIn("# Socratic Debate & Stress-Testing Matrix", md)
        self.assertIn("| ID | Proposition / Claim |", md)
        self.assertIn("Reductionist", md)
        # Verify no em dashes
        self.assertNotIn(chr(8212), md)

    def test_html_export_format(self):
        analyzer = PropositionAnalyzer(self.sample_text)
        claims = analyzer.extract_claims()
        debater = SocraticDebater("Spatial Architecture", claims)
        debate_data = debater.generate_debate()

        html = SocraticDebateExporter.to_html(debate_data)
        self.assertIn("<!DOCTYPE html>", html)
        self.assertIn("The Skeptic Attack", html)
        self.assertIn("The Pragmatist Challenge", html)
        self.assertIn("Steel-Manned Defense Protocol", html)
        self.assertNotIn(chr(8212), html)

    def test_canvas_export_structure(self):
        analyzer = PropositionAnalyzer(self.sample_text)
        claims = analyzer.extract_claims()
        debater = SocraticDebater("Spatial Architecture", claims)
        debate_data = debater.generate_debate()

        canvas = SocraticDebateExporter.to_canvas(debate_data)
        self.assertIn("nodes", canvas)
        self.assertIn("edges", canvas)
        
        # Root node check
        root = [n for n in canvas["nodes"] if n["id"] == "root-topic"]
        self.assertEqual(len(root), 1)

        # Edge checks: each claim should connect to root, skeptic, pragmatist, and defense
        edges = canvas["edges"]
        self.assertGreaterEqual(len(edges), len(claims) * 3)

    def test_run_socratic_debate_file_output(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = os.path.join(tmpdir, "debate_test.md")
            debate_data, content = run_socratic_debate(
                self.sample_text,
                topic="Vault Optimization",
                output_format="markdown",
                output_file=out_file
            )
            self.assertTrue(os.path.isfile(out_file))
            with open(out_file, "r", encoding="utf-8") as f:
                saved_text = f.read()
            self.assertEqual(saved_text, content)
            self.assertNotIn(chr(8212), saved_text)

    def test_cli_debate_command(self):
        import subprocess
        cli_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts", "dx_cli.py"))
        res = subprocess.run(
            [sys.executable, cli_path, "debate", "--topic", "CLI Integration Test"],
            capture_output=True,
            text=True,
            check=True
        )
        self.assertEqual(res.returncode, 0)
        self.assertIn("Socratic Debate & Stress-Testing Matrix: CLI Integration Test", res.stdout)
        self.assertNotIn(chr(8212), res.stdout)

    def test_zero_em_dash_in_source(self):
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts", "socratic_debate.py"))
        if os.path.exists(script_path):
            with open(script_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertNotIn(chr(8212), content, "Found em dash in scripts/socratic_debate.py")


if __name__ == "__main__":
    unittest.main()
