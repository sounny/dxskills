#!/usr/bin/env python3
"""
Unit tests for Autonomous Cognitive Spatial Working Memory Anchor Stacking & Chunk Compression
Part of the DxSkills Cognitive Architecture Suite (https://dxskills.sounny.com)
"""

import os
import unittest
import json
from scripts.chunk_compressor import (
    WorkingMemoryChunkCompressor,
    CanvasConceptNode,
    create_sample_chunk_compressor,
    COWAN_WORKING_MEMORY_LIMIT
)


class TestWorkingMemoryChunkCompressor(unittest.TestCase):
    """Test suite verifying anchor stacking, working memory slot preservation, and canvas export."""

    def setUp(self):
        self.compressor = WorkingMemoryChunkCompressor(max_working_memory_slots=4)

    def test_node_addition_and_defaults(self):
        """Test node creation, bounds, and defaults."""
        node = self.compressor.add_node(
            text="Autonomous Spatial Map",
            category="spatial",
            tags=["gis", "canvas"]
        )
        self.assertEqual(node.text, "Autonomous Spatial Map")
        self.assertEqual(node.category, "spatial")
        self.assertIn("gis", node.tags)
        self.assertEqual(node.color, "1")

    def test_markdown_outline_loader(self):
        """Test hierarchical outline parsing into parent and child nodes."""
        md = """# Parent Core Concept
- Child bullet item 1
- Child bullet item 2
- Child bullet item 3"""
        self.compressor.load_markdown_outline(md)
        self.assertEqual(len(self.compressor.nodes), 4)
        self.assertGreaterEqual(len(self.compressor.edges), 3)

    def test_chunk_compression_ratios(self):
        """Verify slot reduction and Cowan working memory limit compliance."""
        comp, audit = create_sample_chunk_compressor()

        self.assertEqual(audit.original_node_count, 12)
        self.assertEqual(audit.compressed_slots_used, 4)
        self.assertEqual(audit.slot_reduction_count, 8)
        self.assertTrue(audit.cowan_capacity_respected)
        self.assertGreaterEqual(audit.slot_reduction_percentage, 60.0)

        for anchor in audit.anchors:
            self.assertGreaterEqual(anchor.compression_ratio, 1.0)
            self.assertEqual(anchor.compressed_slots, 1)

    def test_obsidian_canvas_export(self):
        """Verify Obsidian .canvas structure, stacked nodes, and telemetry HUD."""
        comp, audit = create_sample_chunk_compressor()
        canvas = comp.export_compressed_canvas(audit)

        self.assertIn("nodes", canvas)
        self.assertIn("edges", canvas)
        self.assertGreaterEqual(len(canvas["nodes"]), 5)

        hud_node = next(n for n in canvas["nodes"] if n["id"] == "node-hud-telemetry")
        self.assertIn("Working Memory Buffer Telemetry", hud_node["text"])
        self.assertEqual(hud_node["color"], "4")

    def test_svg_telemetry_rendering(self):
        """Verify SVG visualization contains telemetry metrics and anchor cards."""
        comp, audit = create_sample_chunk_compressor()
        svg_code = comp.export_svg_telemetry(audit, width=780, height=520)

        self.assertIn("<svg", svg_code)
        self.assertIn("</svg>", svg_code)
        self.assertIn("Spatial Working Memory", svg_code)
        self.assertIn("ORIGINAL NODES", svg_code)
        self.assertIn("COMPRESSED TOKENS", svg_code)
        self.assertIn("COWAN CAPACITY", svg_code)

    def test_custom_capacity_limits(self):
        """Test custom memory slot limit."""
        custom_comp = WorkingMemoryChunkCompressor(max_working_memory_slots=2)
        custom_comp.add_node("Node A", category="cat1")
        custom_comp.add_node("Node B", category="cat2")
        custom_comp.add_node("Node C", category="cat3")

        audit = custom_comp.compress_chunks()
        self.assertEqual(audit.compressed_slots_used, 3)
        self.assertFalse(audit.cowan_capacity_respected)

    def test_zero_em_dashes_enforcement(self):
        """Strict compliance test: zero em dashes across scripts and tests."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(current_dir, "..", "scripts", "chunk_compressor.py")
        test_path = os.path.abspath(__file__)

        with open(script_path, "r", encoding="utf-8") as f:
            script_content = f.read()
            self.assertNotIn(chr(8212), script_content, "Em dash found in scripts/chunk_compressor.py")

        with open(test_path, "r", encoding="utf-8") as f:
            test_content = f.read()
            self.assertNotIn(chr(8212), test_content, "Em dash found in tests/test_chunk_compressor.py")


if __name__ == "__main__":
    unittest.main()
