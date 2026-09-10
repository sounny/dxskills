#!/usr/bin/env python3
"""
Unit Tests for DxSkills Spatial Graph Clustering & Vector Semantic Search
Verifies TF-IDF vectorization, hybrid similarity computation, automated
constellation clustering, and cross-link edge discovery.

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

import scripts.spatial_cluster as sc

class TestSpatialCluster(unittest.TestCase):

    def setUp(self):
        self.clusterer = sc.SpatialGraphClusterer(similarity_threshold=0.15)
        self.sample_nodes = [
            {"id": "node-1", "text": "Deploying Kubernetes cluster with worker replicas and load balancing."},
            {"id": "node-2", "text": "Venture pitch deck financial projections and SaaS recurring revenue."},
            {"id": "node-3", "text": "Container orchestration, Docker worker pods, and cluster autoscaling."},
            {"id": "node-4", "text": "Customer acquisition cost, sales pipeline, and seed round pitch."},
            {"id": "node-5", "text": "Database indexing, query optimization, and connection pooling."}
        ]

    def test_tokenize_and_stem(self):
        tokens = sc.tokenize_text("Deploying worker clusters with load balancing")
        self.assertIn("deploy", tokens)
        self.assertIn("worker", tokens)
        self.assertIn("cluster", tokens)
        self.assertNotIn("with", tokens)  # stop word removed

    def test_tfidf_vectors_normalized(self):
        docs = ["Kubernetes cluster worker pods.", "Venture financial pitch deck."]
        vectors, token_lists, vocab = sc.compute_tfidf_vectors(docs)
        self.assertEqual(len(vectors), 2)
        norm0 = sum(x * x for x in vectors[0])
        self.assertAlmostEqual(norm0, 1.0, places=4)

    def test_cosine_similarity(self):
        vec_a = [1.0, 0.0]
        vec_b = [1.0, 0.0]
        vec_c = [0.0, 1.0]
        self.assertAlmostEqual(sc.cosine_similarity(vec_a, vec_b), 1.0)
        self.assertAlmostEqual(sc.cosine_similarity(vec_a, vec_c), 0.0)

    def test_hybrid_similarity(self):
        t_a = ["cluster", "worker", "deploy"]
        t_b = ["cluster", "worker", "pod"]
        t_c = ["financial", "pitch", "deck"]
        
        sim_ab = sc.calculate_hybrid_similarity(t_a, t_b, [0.5, 0.5], [0.5, 0.5])
        sim_ac = sc.calculate_hybrid_similarity(t_a, t_c, [0.5, 0.5], [0.0, 0.0])
        
        self.assertGreater(sim_ab, sim_ac)
        self.assertGreaterEqual(sim_ab, 0.20)

    def test_cluster_nodes(self):
        clusters = self.clusterer.cluster_nodes(self.sample_nodes)
        self.assertTrue(len(clusters) >= 2)
        # Verify node-1 and node-3 clustered together
        cluster_found = False
        for c in clusters:
            if "node-1" in c["node_ids"] and "node-3" in c["node_ids"]:
                cluster_found = True
                break
        self.assertTrue(cluster_found)

    def test_discover_cross_links(self):
        links = self.clusterer.discover_cross_links(self.sample_nodes)
        self.assertTrue(len(links) >= 1)
        first_link = links[0]
        self.assertIn("fromNode", first_link)
        self.assertIn("toNode", first_link)
        self.assertIn("similarity", first_link)
        self.assertIn("affinity_label", first_link)

    def test_canvas_generation(self):
        res = self.clusterer.generate_clustered_canvas(self.sample_nodes)
        self.assertIn("canvas_json", res)
        canvas_data = json.loads(res["canvas_json"])
        self.assertIn("nodes", canvas_data)
        self.assertIn("edges", canvas_data)
        self.assertEqual(len(canvas_data["nodes"]), 5)
        # Check node positions and colors
        for n in canvas_data["nodes"]:
            self.assertIn("x", n)
            self.assertIn("y", n)
            self.assertIn("color", n)

    def test_zero_em_dash_enforcement(self):
        bad_nodes = [
            {"id": "n1", "text": f"First thought {chr(8212)} very critical."},
            {"id": "n2", "text": "Second thought related to first thought."}
        ]
        res = self.clusterer.generate_clustered_canvas(bad_nodes)
        self.assertNotIn(chr(8212), res["canvas_json"])

if __name__ == "__main__":
    unittest.main()
