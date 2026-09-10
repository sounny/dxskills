"""
Tests for Autonomous Spatial Cognitive Model Fine-Tuning Dataset Synthesizer.
Strict zero em dash compliance verified across all test assertions.
"""

import os
import sys
import json
import unittest
import tempfile
import subprocess

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))
from dataset_synthesizer import (
    DatasetSynthesizer,
    DatasetValidator,
    compile_dataset,
)


class TestDatasetSynthesizer(unittest.TestCase):

    def setUp(self):
        self.sample_doc = (
            "# Strategic Spatial Deliverable\n"
            "> **BLUF:** Decouple phonological working memory from spatial reasoning models.\n\n"
            "## Architectural Vectors\n"
            "- 1. High-contrast spatial canvas topology.\n"
            "- 2. Automated cross-vault synchronization without manual ID linking.\n"
            "- 3. Lossless multi-modal audio-spatial flashcards.\n\n"
            "Associative reference to [[SpatialMemory]] and [[CognitiveOffload]]."
        )

    def test_synthesizer_formats(self):
        # 1. Alpaca
        p_alpaca = DatasetSynthesizer.create_pair(self.sample_doc, title="Test Alpaca", fmt="alpaca")
        self.assertIn("instruction", p_alpaca)
        self.assertIn("input", p_alpaca)
        self.assertIn("output", p_alpaca)
        canvas_alpaca = json.loads(p_alpaca["output"])
        self.assertIn("nodes", canvas_alpaca)
        self.assertIn("edges", canvas_alpaca)

        # 2. ShareGPT
        p_sharegpt = DatasetSynthesizer.create_pair(self.sample_doc, title="Test ShareGPT", fmt="sharegpt")
        self.assertIn("conversations", p_sharegpt)
        self.assertEqual(len(p_sharegpt["conversations"]), 3)
        self.assertEqual(p_sharegpt["conversations"][0]["from"], "system")
        self.assertEqual(p_sharegpt["conversations"][1]["from"], "human")
        self.assertEqual(p_sharegpt["conversations"][2]["from"], "gpt")

        # 3. OpenAI
        p_openai = DatasetSynthesizer.create_pair(self.sample_doc, title="Test OpenAI", fmt="openai")
        self.assertIn("messages", p_openai)
        self.assertEqual(len(p_openai["messages"]), 3)
        self.assertEqual(p_openai["messages"][0]["role"], "system")
        self.assertEqual(p_openai["messages"][1]["role"], "user")
        self.assertEqual(p_openai["messages"][2]["role"], "assistant")

    def test_validator_valid_pair(self):
        pair = DatasetSynthesizer.create_pair(self.sample_doc, title="Valid Test", fmt="alpaca")
        val = DatasetValidator.validate_pair(pair)

        self.assertTrue(val["valid"])
        self.assertGreaterEqual(val["quality_score"], 70.0)
        self.assertFalse(val["has_em_dash"])
        self.assertGreaterEqual(val["nodes_count"], 3)
        self.assertGreaterEqual(val["edges_count"], 2)

    def test_validator_broken_json(self):
        broken_pair = {
            "instruction": "Test broken",
            "input": "Broken",
            "output": "{ broken_json: true, "
        }
        val = DatasetValidator.validate_pair(broken_pair)
        self.assertFalse(val["valid"])
        self.assertIn("Invalid JSON", val["error"])

    def test_validator_dangling_edge(self):
        dangling_canvas = {
            "nodes": [
                {"id": "node-1", "text": "Node 1", "x": 0, "y": 0, "width": 100, "height": 50}
            ],
            "edges": [
                {"id": "e1", "fromNode": "node-1", "toNode": "non-existent-node"}
            ]
        }
        broken_pair = {
            "instruction": "Test",
            "input": "Input",
            "output": json.dumps(dangling_canvas)
        }
        val = DatasetValidator.validate_pair(broken_pair)
        self.assertFalse(val["valid"])
        self.assertIn("Dangling edges", val["error"])

    def test_compile_dataset_pipeline(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            out_jsonl = os.path.join(tmpdir, "dataset.jsonl")
            corpus = [
                ("Note 1", self.sample_doc),
                ("Note 2", "- Idea A: Spatial clustering.\n- Idea B: Leitner spaced repetition.")
            ]

            dataset, meta = compile_dataset(corpus, output_filepath=out_jsonl, fmt="alpaca")

            self.assertEqual(meta["total_pairs"], 2)
            self.assertEqual(meta["valid_pairs"], 2)
            self.assertTrue(os.path.exists(out_jsonl))

            with open(out_jsonl, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]
            self.assertEqual(len(lines), 2)

    def test_cli_dataset_integration(self):
        cli_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts", "dx_cli.py"))
        with tempfile.TemporaryDirectory() as tmpdir:
            out_jsonl = os.path.join(tmpdir, "cli_dataset.jsonl")
            res = subprocess.run(
                [
                    sys.executable,
                    cli_path,
                    "dataset",
                    self.sample_doc,
                    "--format", "sharegpt",
                    "--output", out_jsonl
                ],
                capture_output=True,
                text=True
            )
            self.assertEqual(res.returncode, 0, f"CLI stderr: {res.stderr}")
            self.assertIn("[DxSkills] Compiled", res.stdout)
            self.assertTrue(os.path.exists(out_jsonl))

    def test_zero_em_dash_compliance(self):
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts", "dataset_synthesizer.py"))
        with open(script_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertNotIn(chr(8212), content, f"Em dash found in {script_path}")

        with open(__file__, "r", encoding="utf-8") as f:
            test_content = f.read()
        self.assertNotIn(chr(8212), test_content, "Em dash found in test file")


if __name__ == "__main__":
    unittest.main()
