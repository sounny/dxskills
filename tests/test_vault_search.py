#!/usr/bin/env python3
"""
Unit tests for Autonomous Cognitive Multi-Vault Semantic Vector Search & Spatial Similarity Mesh
Part of the DxSkills Cognitive Architecture Suite (https://dxskills.sounny.com)
"""

import os
import json
import unittest
import tempfile
import shutil

from scripts.vault_search import (
    tokenize,
    VaultDocument,
    SearchResult,
    SemanticBridge,
    MultiVaultVectorSearch,
    VaultSearchCanvasExporter
)


class TestMultiVaultVectorSearch(unittest.TestCase):
    """Tests for multi-vault semantic search, indexing, ranking, and canvas export."""

    def setUp(self):
        self.search_engine = MultiVaultVectorSearch()

    def test_tokenize(self):
        text = "The quick brown fox jumps over the lazy dog and 123 robots."
        tokens = tokenize(text)
        self.assertIn("quick", tokens)
        self.assertIn("brown", tokens)
        self.assertIn("fox", tokens)
        self.assertIn("robots", tokens)
        # Verify stop words and numbers excluded
        self.assertNotIn("the", tokens)
        self.assertNotIn("and", tokens)
        self.assertNotIn("123", tokens)

    def test_index_document_and_build_index(self):
        doc1 = self.search_engine.index_document(
            vault_name="VaultA",
            rel_path="notes/spatial_design.md",
            content="Spatial reasoning and 2D canvas layouts alleviate visual crowding and cognitive load.",
            title="Spatial Design"
        )
        doc2 = self.search_engine.index_document(
            vault_name="VaultB",
            rel_path="notes/audio_engine.md",
            content="Binaural audio cues and acoustic soundscapes guide navigation through virtual chambers.",
            title="Audio Engine"
        )
        self.search_engine.build_index()

        self.assertEqual(len(self.search_engine.documents), 2)
        d1 = self.search_engine.documents[doc1]
        self.assertGreater(d1.norm, 0.0)
        self.assertIn("spatial", d1.tfidf_vector)

    def test_semantic_search_ranking(self):
        self.search_engine.index_document(
            vault_name="Architecture",
            rel_path="plans/spatial_campus.md",
            content="Architectural floorplans require 2D spatial layouts, orbital chambers, and structural navigation.",
            title="Spatial Campus"
        )
        self.search_engine.index_document(
            vault_name="SoundEngineering",
            rel_path="audio/binaural_tones.md",
            content="Synthesizing binaural stereo acoustic beats with 432Hz frequency modulation and spatial reverberation.",
            title="Binaural Tones"
        )
        self.search_engine.index_document(
            vault_name="Cooking",
            rel_path="recipes/moroccan_tajine.md",
            content="Slow cooked lamb with caramelized prunes, toasted almonds, saffron, and aromatic spices.",
            title="Moroccan Tajine"
        )
        self.search_engine.build_index()

        results = self.search_engine.search("spatial architectural floorplans and layout", top_k=3)
        self.assertTrue(len(results) >= 1)
        top = results[0]
        self.assertEqual(top.title, "Spatial Campus")
        self.assertEqual(top.vault_name, "Architecture")
        self.assertGreater(top.similarity, 0.2)
        self.assertIn("spatial", top.shared_keywords)

    def test_cross_vault_semantic_bridges(self):
        self.search_engine.index_document(
            vault_name="ResearchVault",
            rel_path="ai/neural_transformers.md",
            content="Deep learning transformer models utilize multi-head attention mechanisms and high-dimensional vector embeddings.",
            title="Neural Transformers"
        )
        self.search_engine.index_document(
            vault_name="EngineeringVault",
            rel_path="mlops/vector_embeddings.md",
            content="Deploying high-dimensional vector embeddings and transformer attention for real-time document search.",
            title="Vector Embeddings Production"
        )
        self.search_engine.index_document(
            vault_name="PersonalVault",
            rel_path="journal/morning_walk.md",
            content="Sunny walk in the park with fresh coffee, birds chirping, and cool morning breeze.",
            title="Morning Walk"
        )
        self.search_engine.build_index()

        results = self.search_engine.search("vector embeddings and transformer attention", top_k=5)
        bridges = self.search_engine.compute_cross_vault_bridges(results, threshold=0.20)

        self.assertTrue(len(bridges) >= 1)
        bridge = bridges[0]
        self.assertNotEqual(bridge.doc_a_vault, bridge.doc_b_vault)
        self.assertTrue(any(kw in bridge.shared_keywords for kw in ["vector", "embeddings", "transformer", "attention"]))

    def test_canvas_export(self):
        doc1 = SearchResult(
            doc_id="VaultA::notes/geo.md",
            vault_name="VaultA",
            rel_path="notes/geo.md",
            title="Geospatial Projections",
            similarity=0.85,
            shared_keywords=["geospatial", "projections"],
            excerpt="Mercator and Winkel Tripel coordinates."
        )
        doc2 = SearchResult(
            doc_id="VaultB::notes/carto.md",
            vault_name="VaultB",
            rel_path="notes/carto.md",
            title="Cartographic Maps",
            similarity=0.62,
            shared_keywords=["cartographic", "maps"],
            excerpt="Topological contours and elevation layers."
        )
        bridge = SemanticBridge(
            doc_a_id=doc1.doc_id,
            doc_a_title=doc1.title,
            doc_a_vault=doc1.vault_name,
            doc_b_id=doc2.doc_id,
            doc_b_title=doc2.title,
            doc_b_vault=doc2.vault_name,
            similarity=0.74,
            shared_keywords=["maps"]
        )

        canvas_data = VaultSearchCanvasExporter.export_canvas(
            query="cartographic geospatial maps",
            results=[doc1, doc2],
            bridges=[bridge]
        )

        self.assertIn("nodes", canvas_data)
        self.assertIn("edges", canvas_data)
        # Query node + 2 result nodes
        self.assertEqual(len(canvas_data["nodes"]), 3)
        # 2 query edges + 1 bridge edge
        self.assertEqual(len(canvas_data["edges"]), 3)

        # Verify center query node
        query_node = canvas_data["nodes"][0]
        self.assertEqual(query_node["id"], "node_query_center")
        self.assertEqual(query_node["x"], 0)
        self.assertEqual(query_node["y"], 0)

    def test_svg_and_summary_export(self):
        doc = SearchResult(
            doc_id="VaultA::notes/test.md",
            vault_name="VaultA",
            rel_path="notes/test.md",
            title="Test Document",
            similarity=0.75,
            shared_keywords=["test", "sample"],
            excerpt="Sample excerpt context."
        )
        svg = VaultSearchCanvasExporter.export_svg("sample query", [doc])
        self.assertTrue(svg.startswith("<svg"))
        self.assertTrue(svg.endswith("</svg>"))
        self.assertIn("sample query", svg)
        self.assertIn("Test Document", svg)

        summary = VaultSearchCanvasExporter.export_summary("sample query", [doc])
        self.assertIn("# Multi-Vault Semantic Vector Search", summary)
        self.assertIn("Test Document", summary)

    def test_zero_em_dashes(self):
        import inspect
        import scripts.vault_search as vs
        source = inspect.getsource(vs)
        self.assertNotIn(chr(8212), source, "Illegal em dash found in scripts/vault_search.py")


if __name__ == "__main__":
    unittest.main()
