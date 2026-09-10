#!/usr/bin/env python3
"""
DxSkills Spatial Graph Clustering & Vector Semantic Search Engine
Computes local vector embeddings, hybrid semantic affinities, and automated
spatial cross-linking between disjoint notes and Canvas graphs without external API dependencies.

Cognitive Principle:
Non-linear thinkers generate rich networks of thoughts that scatter across disjoint sessions.
Automated semantic similarity clustering organizes orphaned nodes into spatial constellations,
eliminating the cognitive anxiety of manual folder filing.

Strict Rule: NO em dashes anywhere (use hyphens, commas, or parentheses).
"""

import os
import re
import sys
import json
import math
from collections import Counter

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if SKILL_DIR not in sys.path:
    sys.path.insert(0, SKILL_DIR)

STOP_WORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
    "any", "are", "as", "at", "be", "because", "been", "before", "being", "below",
    "between", "both", "but", "by", "can", "did", "do", "does", "doing", "don",
    "down", "during", "each", "few", "for", "from", "further", "had", "has",
    "have", "having", "he", "her", "here", "hers", "herself", "him", "himself",
    "his", "how", "i", "if", "in", "into", "is", "it", "its", "itself", "just",
    "me", "more", "most", "my", "myself", "no", "nor", "not", "now", "of", "off",
    "on", "once", "only", "or", "other", "our", "ours", "ourselves", "out", "over",
    "own", "s", "same", "she", "should", "so", "some", "such", "t", "than", "that",
    "the", "their", "theirs", "them", "themselves", "then", "there", "these",
    "they", "this", "those", "through", "to", "too", "under", "until", "up",
    "very", "was", "we", "were", "what", "when", "where", "which", "while",
    "who", "whom", "why", "will", "with", "you", "your", "yours", "yourself"
}

def stem_token(word):
    """Lightweight morphological suffix normalizer for common English inflections."""
    w = word.lower()
    for suff in ["ing", "tion", "tions", "ed", "es", "s", "al", "ment"]:
        if w.endswith(suff) and len(w) - len(suff) >= 3:
            return w[:-len(suff)]
    return w

def tokenize_text(text):
    """Tokenizes text into filtered lowercase stems, stripping markdown and punctuation."""
    em_char = chr(8212)
    clean = text.replace(em_char, " ").lower()
    clean = re.sub(r"[#*`_\[\]()>-]", " ", clean)
    words = re.findall(r"\b[a-z]{3,}\b", clean)
    return [stem_token(w) for w in words if w not in STOP_WORDS]

def compute_tfidf_vectors(documents):
    """Computes normalized TF-IDF vectors for a collection of texts."""
    tokenized_docs = [tokenize_text(doc) for doc in documents]
    num_docs = len(documents)
    
    df = Counter()
    for tokens in tokenized_docs:
        for t in set(tokens):
            df[t] += 1
            
    vocab = sorted(list(df.keys()))
    vocab_idx = {term: idx for idx, term in enumerate(vocab)}
    
    idf = {}
    for term, count in df.items():
        idf[term] = math.log((1 + num_docs) / (1 + count)) + 1.0

    vectors = []
    for tokens in tokenized_docs:
        tf = Counter(tokens)
        total_tokens = len(tokens) or 1
        vec = [0.0] * len(vocab)
        
        for term, freq in tf.items():
            if term in vocab_idx:
                tf_val = freq / total_tokens
                vec[vocab_idx[term]] = tf_val * idf[term]
                
        norm = math.sqrt(sum(x * x for x in vec))
        if norm > 0:
            vec = [x / norm for x in vec]
            
        vectors.append(vec)
        
    return vectors, tokenized_docs, vocab

def cosine_similarity(vec_a, vec_b):
    """Computes cosine similarity between two normalized vectors."""
    if not vec_a or not vec_b or len(vec_a) != len(vec_b):
        return 0.0
    return sum(a * b for a, b in zip(vec_a, vec_b))

def calculate_hybrid_similarity(tokens_a, tokens_b, vec_a, vec_b):
    """
    Combines TF-IDF cosine similarity with Szymkiewicz-Simpson overlap coefficient
    for superior semantic affinity matching on short note fragments.
    """
    if not tokens_a or not tokens_b:
        return 0.0

    # 1. Cosine similarity
    cos_sim = cosine_similarity(vec_a, vec_b)

    # 2. Overlap coefficient
    set_a = set(tokens_a)
    set_b = set(tokens_b)
    intersection = len(set_a & set_b)
    overlap_coeff = intersection / min(len(set_a), len(set_b)) if min(len(set_a), len(set_b)) > 0 else 0.0

    # Weighted hybrid: 40% TF-IDF Cosine, 60% Keyword Overlap
    hybrid_score = (0.4 * cos_sim) + (0.6 * overlap_coeff)
    return round(hybrid_score, 4)

def extract_top_keywords(text, top_n=2):
    """Extracts top keywords for cluster naming."""
    tokens = tokenize_text(text)
    counts = Counter(tokens)
    return [w for w, _ in counts.most_common(top_n)]

class SpatialGraphClusterer:
    """Clusters spatial nodes and synthesizes cross-links across disjoint notes."""

    def __init__(self, similarity_threshold=0.15):
        self.threshold = similarity_threshold

    def cluster_nodes(self, nodes):
        """Groups nodes into semantic clusters based on hybrid vector similarity."""
        if not nodes:
            return []

        doc_texts = [n.get("text", "") for n in nodes]
        vectors, token_lists, _ = compute_tfidf_vectors(doc_texts)

        n_count = len(nodes)
        clusters = []
        assigned = set()

        for i in range(n_count):
            if i in assigned:
                continue

            cluster_members = [i]
            assigned.add(i)

            for j in range(i + 1, n_count):
                if j in assigned:
                    continue
                sim = calculate_hybrid_similarity(token_lists[i], token_lists[j], vectors[i], vectors[j])
                if sim >= self.threshold:
                    cluster_members.append(j)
                    assigned.add(j)

            combined_text = " ".join([nodes[idx].get("text", "") for idx in cluster_members])
            top_k = extract_top_keywords(combined_text, top_n=2)
            cluster_name = " & ".join([w.capitalize() for w in top_k]) if top_k else f"Cluster {len(clusters) + 1}"

            clusters.append({
                "id": f"cluster-{len(clusters) + 1}",
                "name": cluster_name,
                "node_indices": cluster_members,
                "node_ids": [nodes[idx].get("id") for idx in cluster_members],
                "size": len(cluster_members)
            })

        return clusters

    def discover_cross_links(self, nodes, existing_edges=None):
        """Discovers unlinked nodes with high semantic affinity and suggests new directional edges."""
        if len(nodes) < 2:
            return []

        doc_texts = [n.get("text", "") for n in nodes]
        vectors, token_lists, _ = compute_tfidf_vectors(doc_texts)
        
        existing_pairs = set()
        if existing_edges:
            for e in existing_edges:
                existing_pairs.add((e.get("fromNode"), e.get("toNode")))
                existing_pairs.add((e.get("toNode"), e.get("fromNode")))

        discovered = []
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                id_a = nodes[i].get("id")
                id_b = nodes[j].get("id")
                
                if (id_a, id_b) in existing_pairs:
                    continue

                sim = calculate_hybrid_similarity(token_lists[i], token_lists[j], vectors[i], vectors[j])
                if sim >= self.threshold:
                    discovered.append({
                        "id": f"edge-cross-{id_a}-{id_b}",
                        "fromNode": id_a,
                        "toNode": id_b,
                        "similarity": sim,
                        "affinity_label": f"Semantic Affinity ({int(sim * 100)}%)"
                    })

        discovered.sort(key=lambda x: x["similarity"], reverse=True)
        return discovered

    def generate_clustered_canvas(self, nodes, existing_edges=None, title="Clustered Knowledge Canvas"):
        """
        Synthesizes an enhanced Obsidian Canvas (.canvas) JSON where related nodes
        are arranged into spatial constellation groups with cross-link edges.
        """
        clusters = self.cluster_nodes(nodes)
        cross_links = self.discover_cross_links(nodes, existing_edges)

        color_palette = ["1", "4", "2", "5", "6", "3"] # Obsidian node colors
        positioned_nodes = []
        new_edges = list(existing_edges) if existing_edges else []

        group_y_start = 60
        group_spacing_y = 260
        col_spacing_x = 340

        for c_idx, cluster in enumerate(clusters):
            color = color_palette[c_idx % len(color_palette)]
            y_base = group_y_start + (c_idx * group_spacing_y)
            
            for m_idx, n_idx in enumerate(cluster["node_indices"]):
                orig_node = nodes[n_idx]
                node_copy = dict(orig_node)
                node_copy["x"] = 60 + (m_idx * col_spacing_x)
                node_copy["y"] = y_base
                node_copy["color"] = color
                positioned_nodes.append(node_copy)

        for link in cross_links[:8]:
            new_edges.append({
                "id": link["id"],
                "fromNode": link["fromNode"],
                "fromSide": "right",
                "toNode": link["toNode"],
                "toSide": "left",
                "label": link["affinity_label"]
            })

        canvas_data = {
            "nodes": positioned_nodes,
            "edges": new_edges
        }

        return {
            "title": title,
            "clusters_count": len(clusters),
            "cross_links_count": len(cross_links),
            "clusters": clusters,
            "cross_links": cross_links,
            "canvas_json": json.dumps(canvas_data, indent=2)
        }

def format_cluster_terminal_report(cluster_result):
    """Formats human-readable terminal matrix of semantic clusters and discovered cross-links."""
    lines = []
    lines.append("=" * 66)
    lines.append("   DxSkills Spatial Cluster & Cross-Link Discovery Audit")
    lines.append("=" * 66)
    lines.append(f" Total Clusters:     {cluster_result['clusters_count']}")
    lines.append(f" Discovered Links:   {cluster_result['cross_links_count']}")
    lines.append("-" * 66)
    lines.append(" Constellation Clusters:")
    for c in cluster_result["clusters"]:
        node_str = ", ".join(c["node_ids"])
        lines.append(f"   * [{c['name']}] ({c['size']} nodes): {node_str}")
    if cluster_result.get("cross_links"):
        lines.append("-" * 66)
        lines.append(" Discovered Cross-Links:")
        for l in cluster_result["cross_links"][:5]:
            lines.append(f"   * {l['fromNode']} <--> {l['toNode']} ({l['affinity_label']})")
    lines.append("=" * 66)
    return "\n".join(lines)

if __name__ == "__main__":
    sample_nodes = [
        {"id": "node-1", "text": "Deploying Kubernetes cluster with worker replicas and load balancing."},
        {"id": "node-2", "text": "Venture pitch deck financial projections and SaaS recurring revenue."},
        {"id": "node-3", "text": "Container orchestration, Docker worker pods, and cluster autoscaling."},
        {"id": "node-4", "text": "Customer acquisition cost, sales pipeline, and seed round pitch."},
        {"id": "node-5", "text": "Database indexing, query optimization, and connection pooling."}
    ]
    clusterer = SpatialGraphClusterer(similarity_threshold=0.15)
    res = clusterer.generate_clustered_canvas(sample_nodes)
    print(format_cluster_terminal_report(res))
