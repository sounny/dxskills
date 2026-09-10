#!/usr/bin/env python3
"""
Unit Tests for DxSkills Voice Streamer & Real-Time Canvas Generator
Verifies audio chunk streaming, disfluency scrubbing, live spatial graph
mutation, and export pipelines.

Strict Rule: NO em dashes anywhere (use hyphens, commas, or parentheses).
"""

import os
import sys
import json
import unittest

# Ensure repository root is in sys.path
REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_DIR not in sys.path:
    sys.path.insert(0, REPO_DIR)

import scripts.voice_streamer as vs

class TestVoiceStreamer(unittest.TestCase):

    def setUp(self):
        self.streamer = vs.LiveCanvasStreamer(session_title="Architecture Brainstorm")

    def test_clean_speech_chunk(self):
        raw = "Um, like, so basically we need to deploy the worker cluster."
        cleaned = vs.clean_speech_chunk(raw)
        self.assertNotIn("Um", cleaned)
        self.assertNotIn("like", cleaned)
        self.assertNotIn("so basically", cleaned)
        self.assertTrue(cleaned.startswith("we need to deploy"))

    def test_live_voice_buffer(self):
        buf = vs.LiveVoiceBuffer()
        buf.add_chunk("The core architecture is distributed.")
        buf.add_chunk("First, setup Kafka queue fabric.")
        buf.add_chunk("Second, deploy the backend nodes.")
        
        self.assertTrue(buf.bluf.startswith("The core architecture"))
        self.assertGreaterEqual(len(buf.actions), 1)

    def test_live_canvas_streamer_incremental(self):
        res1 = self.streamer.process_chunk("The objective is zero latency rendering.")
        self.assertEqual(res1["nodes_count"], 1)
        self.assertEqual(res1["edges_count"], 0)

        res2 = self.streamer.process_chunk("Our primary focus is GPU texture streaming.")
        self.assertGreaterEqual(res2["nodes_count"], 2)
        self.assertGreaterEqual(res2["edges_count"], 1)

        res3 = self.streamer.process_chunk("First, deploy WebGL canvas shader.")
        self.assertGreaterEqual(res3["nodes_count"], 3)
        self.assertGreaterEqual(res3["edges_count"], 2)

    def test_canvas_json_schema(self):
        self.streamer.process_chunk("The system will handle 50k requests.")
        self.streamer.process_chunk("First, build read replicas.")
        canvas_json = self.streamer.get_canvas_json()
        data = json.loads(canvas_json)
        self.assertIn("nodes", data)
        self.assertIn("edges", data)
        self.assertTrue(any("node-root" in n["id"] for n in data["nodes"]))

    def test_canvas_svg_generation(self):
        self.streamer.process_chunk("Initial speech memo on system scalability.")
        svg_data = self.streamer.get_canvas_svg()
        self.assertTrue(svg_data.startswith("<svg"))
        self.assertTrue(svg_data.strip().endswith("</svg>"))
        self.assertIn("viewBox", svg_data)
        self.assertIn("nodes-group", svg_data)

    def test_zero_em_dash_enforcement(self):
        bad_chunk = f"First priority {chr(8212)} very critical for launch."
        self.streamer.process_chunk(bad_chunk)
        
        md = self.streamer.get_markdown_summary()
        c_json = self.streamer.get_canvas_json()
        svg = self.streamer.get_canvas_svg()
        
        self.assertNotIn(chr(8212), md)
        self.assertNotIn(chr(8212), c_json)
        self.assertNotIn(chr(8212), svg)

    def test_export_session_files(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            base_path = os.path.join(tmpdir, "test_session")
            self.streamer.process_chunk("Testing export capability.")
            exports = self.streamer.export_session(output_prefix=base_path)
            
            self.assertTrue(os.path.isfile(exports["canvas"]))
            self.assertTrue(os.path.isfile(exports["svg"]))
            self.assertTrue(os.path.isfile(exports["markdown"]))

if __name__ == "__main__":
    unittest.main()
