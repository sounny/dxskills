#!/usr/bin/env python3
"""
Unit tests for Autonomous Cognitive Multimodal Knowledge Synthesis & Triangulation Radar
Part of the DxSkills Cognitive Architecture Suite (https://dxskills.sounny.com)
"""

import os
import json
import unittest

from scripts.knowledge_triangulator import (
    MultimodalSource,
    TriangulatedClaim,
    TriangulationAudit,
    MultimodalKnowledgeTriangulator
)


class TestMultimodalKnowledgeTriangulator(unittest.TestCase):
    """Tests for claim registration, multimodal evidence attachment, radar audit, and canvas export."""

    def setUp(self):
        self.triangulator = MultimodalKnowledgeTriangulator()

    def test_add_claim_and_evidence(self):
        claim = self.triangulator.add_claim("Zero-copy networking minimizes packet latency.")
        self.assertEqual(claim.confidence_score, 0.0)
        self.assertFalse(claim.is_corroborated)

        # Attach text
        self.triangulator.attach_evidence(claim.claim_id, "text", "Spec Sheet", "docs/spec.md", "Direct DMA access.")
        self.assertEqual(claim.confidence_score, 25.0)
        self.assertFalse(claim.is_corroborated)

        # Attach code (2nd modality -> corroborated!)
        self.triangulator.attach_evidence(claim.claim_id, "code", "Kernel Driver", "src/net.rs", "fn send_packet()")
        self.assertGreaterEqual(claim.confidence_score, 50.0)
        self.assertTrue(claim.is_corroborated)

        # Attach audio and visual
        self.triangulator.attach_evidence(claim.claim_id, "audio", "Pod Sync", "audio/ep1.mp3")
        self.triangulator.attach_evidence(claim.claim_id, "visual", "Architecture Flow", "diagrams/flow.svg")
        self.assertEqual(claim.confidence_score, 100.0)
        self.assertIn("Fully Triangulated", claim.recommendation)

    def test_parse_markdown_evidence(self):
        sample_markdown = """
### Claim: Spatial Canvases Eliminate Phonological Fatigue
- Text: Cognitive Research Monograph | Ref: papers/eide2023.pdf | Excerpt: Spatial reasoning bypasses verbal bottlenecks.
- Code: Canvas Renderer AST | Ref: scripts/canvas_exporter.py:L45
- Audio: Lab Discussion Audio Tape | Ref: audio/lab_notes_04.wav
- Visual: 2D Mindmap Graph | Ref: assets/sample_canvas.svg

### Claim: Linear Documents Stifle Macro Synthesis
- Text: Dyslexic Advantage Chapter 3 | Ref: library/mind.epub
"""
        self.triangulator.parse_markdown_evidence(sample_markdown)
        self.assertEqual(len(self.triangulator.claims), 2)

        audit = self.triangulator.audit_synthesis()
        self.assertEqual(audit.total_claims, 2)
        self.assertEqual(audit.corroborated_claims_count, 1)
        self.assertEqual(audit.uncorroborated_claims_count, 1)
        self.assertEqual(audit.modality_distribution["text"], 2)
        self.assertEqual(audit.modality_distribution["code"], 1)
        self.assertEqual(audit.modality_distribution["audio"], 1)
        self.assertEqual(audit.modality_distribution["visual"], 1)

    def test_export_canvas(self):
        c = self.triangulator.add_claim("Core proposition")
        self.triangulator.attach_evidence(c.claim_id, "text", "Note A", "a.md")
        self.triangulator.attach_evidence(c.claim_id, "code", "Impl B", "b.py")

        canvas_data = self.triangulator.export_canvas()
        self.assertIn("nodes", canvas_data)
        self.assertIn("edges", canvas_data)
        self.assertEqual(len(canvas_data["nodes"]), 3)  # 1 claim + 2 evidence satellites
        self.assertEqual(len(canvas_data["edges"]), 2)

    def test_export_svg_and_summary(self):
        c = self.triangulator.add_claim("Vector clustering reduces search space.")
        self.triangulator.attach_evidence(c.claim_id, "text", "Research Note", "notes/vector.md")
        self.triangulator.attach_evidence(c.claim_id, "code", "Cluster Impl", "scripts/spatial_cluster.py")

        svg = self.triangulator.export_svg()
        self.assertTrue(svg.startswith("<svg"))
        self.assertTrue(svg.endswith("</svg>"))
        self.assertIn("Multimodal Knowledge Synthesis", svg)
        self.assertIn("polygon", svg)

        audit = self.triangulator.audit_synthesis()
        summary = MultimodalKnowledgeTriangulator.export_summary(audit, list(self.triangulator.claims.values()))
        self.assertIn("# Multimodal Knowledge Synthesis & Triangulation Radar", summary)
        self.assertIn("Overall Synthesis Confidence", summary)

    def test_zero_em_dashes(self):
        import inspect
        import scripts.knowledge_triangulator as kt
        source = inspect.getsource(kt)
        self.assertNotIn(chr(8212), source, "Illegal em dash found in scripts/knowledge_triangulator.py")


if __name__ == "__main__":
    unittest.main()
