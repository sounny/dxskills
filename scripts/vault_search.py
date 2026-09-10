#!/usr/bin/env python3
"""
Autonomous Cognitive Multi-Vault Semantic Vector Search & Spatial Similarity Mesh
Part of the DxSkills Cognitive Architecture Suite (https://dxskills.sounny.com)

Enables non-linear, spatial, and dyslexic thinkers to search across multiple
independent Obsidian vaults and note collections simultaneously. Instead of
forcing strict keyword recall, computes semantic TF-IDF cosine similarity and
projects results into an interactive 2D orbital constellation canvas.

Core Principles:
- Zero Phonological Memory Strain: Visual proximity represents conceptual relevance.
- Cross-Vault Semantic Bridging: Identifies hidden connections between distinct vaults.
- Spatial Constellation Topology: Central query hub with orbital concentric rings.
"""

import os
import re
import math
import json
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple, Set


# Standard English stop words for lightweight vectorization
STOP_WORDS: Set[str] = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
    "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being",
    "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't",
    "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during",
    "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't",
    "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here",
    "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i",
    "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's",
    "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself",
    "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought",
    "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she",
    "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such",
    "than", "that", "that's", "the", "their", "theirs", "them", "themselves",
    "then", "there", "there's", "these", "they", "they'd", "they'll", "they're",
    "they've", "this", "those", "through", "to", "too", "under", "until", "up",
    "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were",
    "weren't", "what", "what's", "when", "when's", "where", "where's", "which",
    "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would",
    "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours",
    "yourself", "yourselves"
}


def tokenize(text: str) -> List[str]:
    """Tokenize raw text into normalized words, omitting stop words and single characters."""
    raw_tokens = re.findall(r'[a-zA-Z0-9_\-\u00C0-\u017F]+', text.lower())
    clean_tokens = []
    for tok in raw_tokens:
        tok_clean = tok.strip("-_")
        if len(tok_clean) > 2 and tok_clean not in STOP_WORDS and not tok_clean.isdigit():
            clean_tokens.append(tok_clean)
    return clean_tokens


@dataclass
class VaultDocument:
    """Represents an indexed document from a specific vault."""
    doc_id: str
    vault_name: str
    rel_path: str
    title: str
    content: str
    tokens: List[str] = field(default_factory=list)
    term_counts: Counter = field(default_factory=Counter)
    tfidf_vector: Dict[str, float] = field(default_factory=dict)
    norm: float = 0.0


@dataclass
class SearchResult:
    """Represents a scored search result."""
    doc_id: str
    vault_name: str
    rel_path: str
    title: str
    similarity: float
    shared_keywords: List[str]
    excerpt: str


@dataclass
class SemanticBridge:
    """Represents a cross-vault similarity connection between two documents."""
    doc_a_id: str
    doc_a_title: str
    doc_a_vault: str
    doc_b_id: str
    doc_b_title: str
    doc_b_vault: str
    similarity: float
    shared_keywords: List[str]


class MultiVaultVectorSearch:
    """Multi-vault semantic vector search engine using TF-IDF and cosine similarity."""

    def __init__(self):
        self.documents: Dict[str, VaultDocument] = {}
        self.vault_paths: Dict[str, str] = {}
        self.doc_freq: Counter = Counter()
        self.total_docs: int = 0
        self.idf: Dict[str, float] = {}
        self.is_indexed: bool = False

    def register_vault(self, vault_name: str, root_path: str) -> int:
        """Scan and register all Markdown notes from a vault root directory."""
        self.vault_paths[vault_name] = root_path
        indexed_count = 0
        if not os.path.isdir(root_path):
            return 0

        for root, _, files in os.walk(root_path):
            for file in files:
                if file.endswith(".md"):
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, root_path)
                    try:
                        with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()
                        title = file[:-3]
                        self.index_document(vault_name, rel_path, content, title)
                        indexed_count += 1
                    except Exception:
                        pass
        return indexed_count

    def index_document(self, vault_name: str, rel_path: str, content: str, title: Optional[str] = None) -> str:
        """Index an individual document into the multi-vault index."""
        doc_id = f"{vault_name}::{rel_path}"
        if not title:
            title = os.path.splitext(os.path.basename(rel_path))[0]

        tokens = tokenize(content + " " + title)
        term_counts = Counter(tokens)

        doc = VaultDocument(
            doc_id=doc_id,
            vault_name=vault_name,
            rel_path=rel_path,
            title=title,
            content=content,
            tokens=tokens,
            term_counts=term_counts
        )
        self.documents[doc_id] = doc
        self.is_indexed = False
        return doc_id

    def build_index(self):
        """Compute IDF weights and document vector norms across the full multi-vault corpus."""
        self.total_docs = len(self.documents)
        if self.total_docs == 0:
            self.is_indexed = True
            return

        self.doc_freq = Counter()
        for doc in self.documents.values():
            unique_terms = set(doc.term_counts.keys())
            for term in unique_terms:
                self.doc_freq[term] += 1

        # Smooth IDF: log((N + 1) / (df + 1)) + 1
        self.idf = {}
        for term, df in self.doc_freq.items():
            self.idf[term] = math.log((self.total_docs + 1.0) / (df + 1.0)) + 1.0

        # Compute TF-IDF vectors and vector norms
        for doc in self.documents.values():
            vec = {}
            squared_sum = 0.0
            total_terms = sum(doc.term_counts.values()) or 1
            for term, count in doc.term_counts.items():
                tf = count / total_terms
                weight = tf * self.idf.get(term, 1.0)
                vec[term] = weight
                squared_sum += weight * weight
            doc.tfidf_vector = vec
            doc.norm = math.sqrt(squared_sum)

        self.is_indexed = True

    def search(self, query: str, top_k: int = 8, min_similarity: float = 0.02) -> List[SearchResult]:
        """Search across all vaults using cosine similarity between query and documents."""
        if not self.is_indexed:
            self.build_index()

        query_tokens = tokenize(query)
        if not query_tokens or self.total_docs == 0:
            return []

        query_counts = Counter(query_tokens)
        query_vec = {}
        q_squared_sum = 0.0
        total_q_terms = len(query_tokens)

        for term, count in query_counts.items():
            tf = count / total_q_terms
            weight = tf * self.idf.get(term, 1.0)
            query_vec[term] = weight
            q_squared_sum += weight * weight

        q_norm = math.sqrt(q_squared_sum)
        if q_norm == 0.0:
            return []

        scored_results: List[SearchResult] = []

        for doc in self.documents.values():
            if doc.norm == 0.0:
                continue

            # Dot product calculation
            dot_product = 0.0
            shared_terms = []
            for term, q_weight in query_vec.items():
                if term in doc.tfidf_vector:
                    d_weight = doc.tfidf_vector[term]
                    dot_product += q_weight * d_weight
                    shared_terms.append((term, q_weight * d_weight))

            if dot_product > 0.0:
                similarity = dot_product / (q_norm * doc.norm)
                if similarity >= min_similarity:
                    # Sort shared terms by contribution
                    shared_terms.sort(key=lambda x: x[1], reverse=True)
                    top_shared = [t[0] for t in shared_terms[:5]]

                    # Extract concise excerpt
                    excerpt = self._generate_excerpt(doc.content, query_tokens)
                    scored_results.append(SearchResult(
                        doc_id=doc.doc_id,
                        vault_name=doc.vault_name,
                        rel_path=doc.rel_path,
                        title=doc.title,
                        similarity=round(similarity, 4),
                        shared_keywords=top_shared,
                        excerpt=excerpt
                    ))

        scored_results.sort(key=lambda r: r.similarity, reverse=True)
        return scored_results[:top_k]

    def _generate_excerpt(self, content: str, query_tokens: List[str], max_len: int = 160) -> str:
        """Extract a readable excerpt showing context around query tokens."""
        clean_text = " ".join(content.replace("\n", " ").split())
        if not clean_text:
            return ""

        lower_text = clean_text.lower()
        first_idx = -1
        for tok in query_tokens:
            idx = lower_text.find(tok)
            if idx != -1 and (first_idx == -1 or idx < first_idx):
                first_idx = idx

        if first_idx == -1:
            return clean_text[:max_len] + ("..." if len(clean_text) > max_len else "")

        start = max(0, first_idx - 40)
        end = min(len(clean_text), first_idx + max_len - 40)
        snippet = clean_text[start:end]
        if start > 0:
            snippet = "..." + snippet
        if end < len(clean_text):
            snippet = snippet + "..."
        return snippet

    def compute_cross_vault_bridges(self, results: List[SearchResult], threshold: float = 0.25) -> List[SemanticBridge]:
        """Identify high-similarity cross-vault connections among top search matches."""
        bridges: List[SemanticBridge] = []
        n = len(results)
        for i in range(n):
            for j in range(i + 1, n):
                r_a = results[i]
                r_b = results[j]
                if r_a.vault_name == r_b.vault_name:
                    continue  # Only cross-vault bridges

                doc_a = self.documents.get(r_a.doc_id)
                doc_b = self.documents.get(r_b.doc_id)
                if not doc_a or not doc_b or doc_a.norm == 0.0 or doc_b.norm == 0.0:
                    continue

                dot = 0.0
                shared = []
                for term, wa in doc_a.tfidf_vector.items():
                    if term in doc_b.tfidf_vector:
                        wb = doc_b.tfidf_vector[term]
                        score = wa * wb
                        dot += score
                        shared.append((term, score))

                if dot > 0.0:
                    sim = dot / (doc_a.norm * doc_b.norm)
                    if sim >= threshold:
                        shared.sort(key=lambda x: x[1], reverse=True)
                        top_shared = [t[0] for t in shared[:4]]
                        bridges.append(SemanticBridge(
                            doc_a_id=r_a.doc_id,
                            doc_a_title=r_a.title,
                            doc_a_vault=r_a.vault_name,
                            doc_b_id=r_b.doc_id,
                            doc_b_title=r_b.title,
                            doc_b_vault=r_b.vault_name,
                            similarity=round(sim, 4),
                            shared_keywords=top_shared
                        ))

        bridges.sort(key=lambda b: b.similarity, reverse=True)
        return bridges


class VaultSearchCanvasExporter:
    """Exports multi-vault search results to Obsidian .canvas, SVG, and Markdown formats."""

    COLOR_PALETTE = {
        "query": "1",    # Red / Focal anchor
        "vault_1": "2",  # Orange
        "vault_2": "3",  # Yellow
        "vault_3": "4",  # Green
        "vault_4": "5",  # Cyan
        "vault_5": "6",  # Purple
    }

    @classmethod
    def export_canvas(cls, query: str, results: List[SearchResult], bridges: Optional[List[SemanticBridge]] = None) -> Dict[str, Any]:
        """
        Generate an Obsidian .canvas JSON graph with radial orbital positioning.
        Center: Search query node.
        Orbits: Scored matches arranged radially based on cosine similarity.
        """
        nodes = []
        edges = []

        # 1. Central Query Anchor Node
        query_node_id = "node_query_center"
        query_text = (
            f"### [SEARCH HUB] Query Anchor\n\n"
            f"**Query:** `{query}`\n"
            f"**Matches Found:** {len(results)}\n"
            f"**Format:** Semantic Multi-Vault Constellation"
        )
        nodes.append({
            "id": query_node_id,
            "type": "text",
            "text": query_text,
            "x": 0,
            "y": 0,
            "width": 320,
            "height": 160,
            "color": cls.COLOR_PALETTE["query"]
        })

        if not results:
            return {"nodes": nodes, "edges": edges}

        # 2. Assign distinct colors to unique vaults
        vaults = sorted(list({r.vault_name for r in results}))
        vault_color_map = {}
        color_keys = ["vault_1", "vault_2", "vault_3", "vault_4", "vault_5"]
        for idx, v in enumerate(vaults):
            vault_color_map[v] = cls.COLOR_PALETTE[color_keys[idx % len(color_keys)]]

        # 3. Position search results radially based on similarity
        # Higher similarity -> smaller orbit radius
        count = len(results)
        angle_step = (2 * math.pi) / max(count, 1)

        for idx, res in enumerate(results):
            node_id = f"node_res_{idx}"
            angle = idx * angle_step

            # Orbit radius scaled inversely with similarity: similarity in [0.05, 1.0]
            # Map 1.0 -> 350px, 0.1 -> 750px
            sim_clamped = max(0.05, min(1.0, res.similarity))
            radius = int(800 - (sim_clamped * 450))

            x = int(radius * math.cos(angle)) - 150
            y = int(radius * math.sin(angle)) - 100

            color = vault_color_map.get(res.vault_name, "3")
            shared_str = ", ".join(res.shared_keywords) if res.shared_keywords else "General Context"
            pct = int(res.similarity * 100)

            node_text = (
                f"### [[{res.title}]]\n"
                f"**Vault:** `{res.vault_name}`\n"
                f"**Match:** {pct}% cosine proximity\n"
                f"**Keywords:** {shared_str}\n\n"
                f"> {res.excerpt}"
            )

            nodes.append({
                "id": node_id,
                "type": "text",
                "text": node_text,
                "x": x,
                "y": y,
                "width": 300,
                "height": 200,
                "color": color
            })

            # Connect Query Center to Result Node
            edges.append({
                "id": f"edge_query_to_{idx}",
                "fromNode": query_node_id,
                "fromSide": "bottom" if y > 0 else "top",
                "toNode": node_id,
                "toSide": "top" if y > 0 else "bottom",
                "label": f"{pct}% match"
            })

        # 4. Add Cross-Vault Bridges
        if bridges:
            # Map doc_id to result node id
            doc_to_node = {res.doc_id: f"node_res_{idx}" for idx, res in enumerate(results)}
            for b_idx, bridge in enumerate(bridges):
                node_a = doc_to_node.get(bridge.doc_a_id)
                node_b = doc_to_node.get(bridge.doc_b_id)
                if node_a and node_b:
                    b_pct = int(bridge.similarity * 100)
                    kw = ", ".join(bridge.shared_keywords[:2]) if bridge.shared_keywords else "Bridge"
                    edges.append({
                        "id": f"edge_bridge_{b_idx}",
                        "fromNode": node_a,
                        "fromSide": "right",
                        "toNode": node_b,
                        "toSide": "left",
                        "color": "4",
                        "label": f"Bridge {b_pct}% ({kw})"
                    })

        return {"nodes": nodes, "edges": edges}

    @classmethod
    def export_svg(cls, query: str, results: List[SearchResult], width: int = 1000, height: int = 700) -> str:
        """Export a clean vector SVG graphic of the semantic constellation."""
        cx = width // 2
        cy = height // 2

        elements = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">',
            f'  <rect width="{width}" height="{height}" fill="#09090b" rx="16" />',
            f'  <!-- Concentric Orbital Reference Rings -->',
            f'  <circle cx="{cx}" cy="{cy}" r="150" fill="none" stroke="#27272a" stroke-dasharray="4 4" stroke-width="1.5" />',
            f'  <circle cx="{cx}" cy="{cy}" r="250" fill="none" stroke="#27272a" stroke-dasharray="4 4" stroke-width="1.5" />',
            f'  <circle cx="{cx}" cy="{cy}" r="350" fill="none" stroke="#27272a" stroke-dasharray="4 4" stroke-width="1.5" />',
            f'  <text x="{cx + 155}" y="{cy - 5}" fill="#71717a" font-size="10" font-family="monospace">80% Proximity</text>',
            f'  <text x="{cx + 255}" y="{cy - 5}" fill="#71717a" font-size="10" font-family="monospace">50% Proximity</text>',
            f'  <text x="{cx + 355}" y="{cy - 5}" fill="#71717a" font-size="10" font-family="monospace">20% Proximity</text>',
        ]

        count = len(results)
        angle_step = (2 * math.pi) / max(count, 1)

        # Draw rays and result nodes
        for idx, res in enumerate(results):
            angle = idx * angle_step
            sim_clamped = max(0.05, min(1.0, res.similarity))
            radius = int(380 - (sim_clamped * 230))

            px = int(cx + radius * math.cos(angle))
            py = int(cy + radius * math.sin(angle))

            pct = int(res.similarity * 100)
            safe_title = res.title.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

            # Ray line
            elements.append(f'  <line x1="{cx}" y1="{cy}" x2="{px}" y2="{py}" stroke="#3f3f46" stroke-width="1.2" />')
            # Outer halo
            elements.append(f'  <circle cx="{px}" cy="{py}" r="18" fill="#18181b" stroke="#3b82f6" stroke-width="2" />')
            # Inner circle
            elements.append(f'  <circle cx="{px}" cy="{py}" r="6" fill="#60a5fa" />')
            # Label
            text_anchor = "start" if px >= cx else "end"
            text_offset_x = 22 if px >= cx else -22
            elements.append(f'  <text x="{px + text_offset_x}" y="{py - 2}" fill="#f4f4f5" font-size="12" font-weight="600" font-family="sans-serif" text-anchor="{text_anchor}">{safe_title}</text>')
            elements.append(f'  <text x="{px + text_offset_x}" y="{py + 13}" fill="#a1a1aa" font-size="10" font-family="sans-serif" text-anchor="{text_anchor}">{res.vault_name} ({pct}%)</text>')

        # Center Query Node
        elements.append(f'  <!-- Center Query Node -->')
        elements.append(f'  <circle cx="{cx}" cy="{cy}" r="38" fill="#18181b" stroke="#ef4444" stroke-width="2.5" />')
        elements.append(f'  <circle cx="{cx}" cy="{cy}" r="14" fill="#ef4444" />')
        safe_query = query.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        elements.append(f'  <text x="{cx}" y="{cy + 52}" fill="#ffffff" font-size="13" font-weight="700" font-family="sans-serif" text-anchor="middle">Query: {safe_query[:28]}</text>')

        elements.append('</svg>')
        return "\n".join(elements)

    @classmethod
    def export_summary(cls, query: str, results: List[SearchResult], bridges: Optional[List[SemanticBridge]] = None) -> str:
        """Export executive Markdown briefing of multi-vault semantic search."""
        lines = [
            f"# Multi-Vault Semantic Vector Search",
            f"",
            f"**Query:** `{query}`",
            f"**Total Matches:** {len(results)}",
            f"",
            f"## Top Semantic Proximity Matches",
            f"",
            f"| Rank | Title | Vault | Proximity | Shared Keywords |",
            f"| :--- | :--- | :--- | :--- | :--- |"
        ]

        for idx, res in enumerate(results, 1):
            pct = f"{int(res.similarity * 100)}%"
            kw = ", ".join(res.shared_keywords[:3]) if res.shared_keywords else "Context"
            lines.append(f"| **{idx}** | `{res.title}` | `{res.vault_name}` | **{pct}** | {kw} |")

        if bridges:
            lines.extend([
                f"",
                f"## Cross-Vault Semantic Bridges",
                f"",
                f"| Vault A | Document A | Vault B | Document B | Proximity | Shared Anchor |",
                f"| :--- | :--- | :--- | :--- | :--- | :--- |"
            ])
            for b in bridges:
                b_pct = f"{int(b.similarity * 100)}%"
                kw = ", ".join(b.shared_keywords[:2]) if b.shared_keywords else "Link"
                lines.append(f"| `{b.doc_a_vault}` | `{b.doc_a_title}` | `{b.doc_b_vault}` | `{b.doc_b_title}` | **{b_pct}** | {kw} |")

        return "\n".join(lines)


def main():
    """Quick CLI runner for testing."""
    import sys
    print("MultiVaultVectorSearch Engine Loaded.")


if __name__ == "__main__":
    main()
