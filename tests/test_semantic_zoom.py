#!/usr/bin/env python3
"""
Unit tests for Autonomous Cognitive Multi-Scale Hierarchical Zoom & Semantic Chunking Engine
Part of the DxSkills Cognitive Architecture Suite (https://dxskills.sounny.com)
"""

import os
import json
import unittest

from scripts.semantic_zoom import (
    SemanticNode,
    SemanticZoomAudit,
    SemanticZoomEngine
)


class TestSemanticZoomEngine(unittest.TestCase):
    """Tests for multi-scale semantic decomposition, canvas radial chunking, and LOD export."""

    def setUp(self):
        self.engine = SemanticZoomEngine()

    def test_chunk_monolithic_text(self):
        title = "Distributed Cognitive Architecture"
        body = (
            "Distributed spatial memory models offload executive working memory onto spatial canvasing. "
            "Visual nodes eliminate linear phonological decoding fatigue. "
            "Bi-directional graph topologies provide immediate topological context. "
            "Satellite detail cards unpack dense technical explanations without breaking focus."
        )
        macro, meso, micro = self.engine.chunk_monolithic_text(title, body)
        self.assertTrue(len(macro.split()) <= 16)
        self.assertGreaterEqual(len(meso), 3)
        self.assertEqual(micro, body)

    def test_add_node_and_audit(self):
        n1 = self.engine.add_node(
            "Spatial Vector Mesh",
            "Spatial vector meshes maintain cognitive landmark stability across varying zoom magnifications.",
            x=100.0,
            y=200.0
        )
        self.assertEqual(n1.title, "Spatial Vector Mesh")
        self.assertEqual(n1.x, 100.0)
        self.assertEqual(n1.y, 200.0)

        audit = self.engine.audit_engine()
        self.assertEqual(audit.total_nodes, 1)
        self.assertEqual(audit.spatial_landmark_stability_index, 100.0)
        self.assertIn(0, audit.lod_levels_supported)
        self.assertIn(1, audit.lod_levels_supported)
        self.assertIn(2, audit.lod_levels_supported)

    def test_decompose_canvas_monolith(self):
        # Monolithic text with over 75 words
        dense_paragraph = (
            "Hyperdimensional vector architectures deconstruct monolithic infrastructure into "
            "asynchronous micro-services with deterministic telemetric observability across distributed clusters. "
            "By partitioning high-throughput ingress controllers, edge proxies achieve zero-copy packet switching. "
            "Furthermore, spatial graph databases resolve cyclic inter-dependencies through topological sorting. "
            "Consequently, memory footprint is reduced by forty percent while throughput doubles. "
            "All telemetry streams remain strictly synchronized via consensus heartbeats."
        )
        canvas_data = {
            "nodes": [
                {"id": "node-small", "type": "text", "text": "Small quick idea note.", "x": 0, "y": 0},
                {"id": "node-huge", "type": "text", "text": dense_paragraph, "x": 500, "y": 500}
            ],
            "edges": []
        }

        result = self.engine.decompose_canvas(canvas_data, max_words=40)
        # Small node kept, huge node replaced with parent + radial micro satellites
        self.assertGreater(len(result["nodes"]), 2)
        self.assertGreaterEqual(len(result["edges"]), 1)

        # Check that original small node is intact
        small_node = next(n for n in result["nodes"] if n["id"] == "node-small")
        self.assertEqual(small_node["text"], "Small quick idea note.")

        # Check that huge node has anchor label and child nodes
        parent_node = next(n for n in result["nodes"] if n["id"] == "node-huge")
        self.assertIn("Anchor Macro", parent_node["text"])

    def test_export_canvas_lod_levels(self):
        self.engine.add_node("Concept Alpha", "First foundational pillar of system design and cognitive offload.")
        self.engine.add_node("Concept Beta", "Second architectural layer ensuring fault tolerance.")

        for lod in [0, 1, 2]:
            canvas = self.engine.export_canvas_lod(lod_level=lod)
            self.assertEqual(len(canvas["nodes"]), 2)
            if lod == 0:
                self.assertIn(">", canvas["nodes"][0]["text"])
            elif lod == 1:
                self.assertIn("Key Takeaways", canvas["nodes"][0]["text"])
            else:
                self.assertIn("Micro Detail", canvas["nodes"][0]["text"])

    def test_export_svg_and_summary(self):
        self.engine.add_node("Root A", "Primary database index optimization.")
        self.engine.add_node("Root B", "Secondary caching tier deployment.")

        svg = self.engine.export_svg(lod_level=1)
        self.assertTrue(svg.startswith("<svg"))
        self.assertTrue(svg.endswith("</svg>"))
        self.assertIn("Multi-Scale Hierarchical Zoom", svg)

        audit = self.engine.audit_engine()
        summary = SemanticZoomEngine.export_summary(audit, list(self.engine.nodes.values()))
        self.assertIn("# Multi-Scale Hierarchical Zoom & Semantic Chunking Audit", summary)
        self.assertIn("Spatial Landmark Stability", summary)

    def test_zero_em_dashes(self):
        import inspect
        import scripts.semantic_zoom as sz
        source = inspect.getsource(sz)
        self.assertNotIn(chr(8212), source, "Illegal em dash found in scripts/semantic_zoom.py")


if __name__ == "__main__":
    unittest.main()
