#!/usr/bin/env python3
"""
Unit tests for Autonomous Cognitive Spatial Schema Morphing & Associative Bridge Weaver
Part of the DxSkills Cognitive Architecture Suite (https://dxskills.sounny.com)
"""

import os
import unittest
import json
from scripts.schema_morpher import (
    SpatialSchemaMorpher,
    DomainConcept,
    IsomorphicBridge,
    MorphedSchema,
    create_sample_schema_morpher
)


class TestSpatialSchemaMorpher(unittest.TestCase):
    """Test suite verifying cross-domain schema morphing, analogical bridges, and canvas exports."""

    def setUp(self):
        self.morpher = SpatialSchemaMorpher()

    def test_default_catalog_loaded(self):
        """Verify standard cross-domain schemas are loaded with all 4 domains."""
        self.assertGreaterEqual(len(self.morpher.library), 3)
        for s in self.morpher.library.values():
            self.assertEqual(s.computational.domain, "computational")
            self.assertEqual(s.mechanical.domain, "mechanical")
            self.assertEqual(s.biological.domain, "biological")
            self.assertEqual(s.spatial.domain, "spatial")
            self.assertGreaterEqual(len(s.bridges), 3)

    def test_isomorphic_bridges_created(self):
        """Verify bridges contain structural isomorphisms and high analogical strength."""
        schema = list(self.morpher.library.values())[0]
        targets = {b.target_domain for b in schema.bridges}
        self.assertEqual(targets, {"mechanical", "biological", "spatial"})
        for b in schema.bridges:
            self.assertGreaterEqual(b.analogical_strength, 0.85)
            self.assertTrue(len(b.cognitive_takeaway) > 10)

    def test_dynamic_concept_morphing(self):
        """Test synthesizing bespoke cross-domain schema for new custom concepts."""
        schema = self.morpher.morph_concept(
            concept_name="Async Queue Worker Pool",
            role="buffer",
            description="Background worker pool processing event jobs."
        )
        self.assertIn("Async Queue Worker Pool", schema.computational.name)
        self.assertEqual(schema.primary_role, "buffer")
        self.assertEqual(schema.mechanical.role, "buffer")
        self.assertEqual(schema.biological.role, "buffer")
        self.assertEqual(schema.spatial.role, "buffer")

    def test_obsidian_canvas_export(self):
        """Verify Obsidian .canvas structure, 4 domain nodes, and center HUD."""
        schemas = list(self.morpher.library.values())[:1]
        canvas = self.morpher.export_canvas(schemas)

        self.assertIn("nodes", canvas)
        self.assertIn("edges", canvas)
        self.assertEqual(len(canvas["nodes"]), 5)  # 4 domains + 1 center HUD
        self.assertGreaterEqual(len(canvas["edges"]), 7)  # 4 HUD edges + 3 bridge edges

        hud = next(n for n in canvas["nodes"] if "node-hud" in n["id"])
        self.assertIn("Reactive Backpressure", hud["text"])

    def test_svg_morph_rendering(self):
        """Verify SVG visualization contains quadrant cards and isomorphism diamond."""
        schema = list(self.morpher.library.values())[0]
        svg_code = self.morpher.export_svg_morph(schema, width=800, height=560)

        self.assertIn("<svg", svg_code)
        self.assertIn("</svg>", svg_code)
        self.assertIn("ISOMORPHISM", svg_code)
        self.assertIn("COMPUTATIONAL", svg_code)
        self.assertIn("MECHANICAL", svg_code)
        self.assertIn("BIOLOGICAL", svg_code)
        self.assertIn("SPATIAL", svg_code)

    def test_markdown_summary_report(self):
        """Verify markdown report generation formatting."""
        schemas = list(self.morpher.library.values())
        report = self.morpher.export_summary_markdown(schemas)

        self.assertIn("# Cross-Domain Schema Morphing", report)
        self.assertIn("Reactive Backpressure", report)
        self.assertIn("Quorum Consensus", report)
        self.assertIn("Temporal Caching", report)

    def test_zero_em_dashes_enforcement(self):
        """Strict compliance test: zero em dashes across scripts and tests."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(current_dir, "..", "scripts", "schema_morpher.py")
        test_path = os.path.abspath(__file__)

        with open(script_path, "r", encoding="utf-8") as f:
            script_content = f.read()
            self.assertNotIn(chr(8212), script_content, "Em dash found in scripts/schema_morpher.py")

        with open(test_path, "r", encoding="utf-8") as f:
            test_content = f.read()
            self.assertNotIn(chr(8212), test_content, "Em dash found in tests/test_schema_morpher.py")


if __name__ == "__main__":
    unittest.main()
