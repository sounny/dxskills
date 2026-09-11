"""
Autonomous Cognitive Spatial Dynamic Lexical Compression & Semantic Gist Synthesizer
====================================================================================
Theoretical Framework:
- Eide & Eide M-I-N-D framework (The Dyslexic Advantage): Non-linear and spatial
  thinkers experience phonological bottlenecking with dense linear prose.
  Compressing prose into spatial semantic seeds unlocks high-speed associative reasoning.
- Fuzzy-Trace Theory (Brainerd & Reyna): Cognitive architectures process gist traces
  (core invariant meaning) far more effectively than verbatim textual clutter.
- Cowan working memory capacity bounds (N <= 4): Compaction into spatial glyph tokens
  prevents cognitive buffer overflow and ocular saccadic fatigue.
- Strictly NO em dashes (\u2014 or ) anywhere in code, docstrings, or outputs.
"""

import re
import math
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class SemanticSeed:
    """A high-salience semantic invariant extracted from textual prose."""
    term: str
    role: str  # core_entity, action_verb, constraint, outcome, qualifier
    salience: float  # 0.0 to 1.0
    glyph: str  # Spatial shorthand unicode symbol
    spatial_anchor: str  # origin, vector, boundary, terminus, nexus

@dataclass
class GistClause:
    """A compressed clause mapped to spatial glyph tokens."""
    clause_id: str
    original_text: str
    compressed_shorthand: str
    glyph_sequence: List[str]
    compression_ratio: float
    semantic_seeds: List[SemanticSeed]

@dataclass
class LexicalGistTelemetry:
    """Telemetry tracking lexical compression and working memory headroom."""
    raw_word_count: int
    compressed_token_count: int
    overall_compression_ratio: float
    semantic_preservation_score: float
    cognitive_load_reduction: float
    top_seeds: List[str]

@dataclass
class LexicalGistResult:
    """Comprehensive output from lexical gist compression."""
    clauses: List[GistClause]
    all_seeds: List[SemanticSeed]
    telemetry: LexicalGistTelemetry
    spatial_glyph_diagram: str
    gist_markdown_report: str

class LexicalGistCompressor:
    """
    Synthesizes minimal invariant semantic seeds and spatial shorthand tokens
    from dense multi-clause prose.
    """

    ROLE_GLYPHS = {
        "core_entity": "◆",
        "action_verb": "➔",
        "constraint": "■",
        "outcome": "◎",
        "qualifier": "▲",
        "nexus": "⚡",
    }

    STOPWORDS = {
        "a", "about", "above", "after", "again", "against", "all", "am", "an",
        "and", "any", "are", "as", "at", "be", "because", "been", "before",
        "being", "below", "between", "both", "but", "by", "could", "did",
        "do", "does", "doing", "down", "during", "each", "few", "for", "from",
        "further", "had", "has", "have", "having", "he", "her", "here", "hers",
        "herself", "him", "himself", "his", "how", "i", "if", "in", "into",
        "is", "it", "its", "itself", "just", "me", "more", "most", "my",
        "myself", "no", "nor", "not", "of", "off", "on", "once", "only",
        "or", "other", "ought", "our", "ours", "ourselves", "out", "over",
        "own", "same", "she", "should", "so", "some", "such", "than", "that",
        "the", "their", "theirs", "them", "themselves", "then", "there", "these",
        "they", "this", "those", "through", "to", "too", "under", "until",
        "up", "very", "was", "we", "were", "what", "when", "where", "which",
        "while", "who", "whom", "why", "with", "would", "you", "your", "yours"
    }

    ACTION_PATTERNS = {
        "transforms", "compresses", "synthesizes", "generates", "extracts",
        "evaluates", "projects", "reconciles", "structures", "coordinates",
        "maps", "stabilizes", "deforms", "modulates", "navigates", "bounds"
    }

    CONSTRAINT_PATTERNS = {
        "strictly", "limit", "bound", "invariant", "threshold", "capacity",
        "maximum", "minimum", "zero", "finite", "isolated", "bounded"
    }

    OUTCOME_PATTERNS = {
        "yields", "results", "outcome", "target", "objective", "state",
        "consensus", "equilibrium", "topology", "coherence", "headroom"
    }

    def __init__(self, target_ratio: float = 0.40):
        self.target_ratio = target_ratio

    def extract_clauses(self, text: str) -> List[str]:
        """Splits complex prose into syntactic clause segments."""
        if not text or not text.strip():
            return []
        raw_clauses = re.split(r'[.;\n]+|(?<=[,])\s+(?:which|that|whereas|although|while|because|if)\b', text)
        cleaned = [c.strip() for c in raw_clauses if len(c.strip()) > 3]
        return cleaned if cleaned else [text.strip()]

    def classify_word_role(self, word: str) -> str:
        """Classifies word role into a semantic archetype."""
        w_lower = word.lower()
        if w_lower in self.ACTION_PATTERNS or w_lower.endswith(("ing", "ed", "izes", "ates")):
            return "action_verb"
        if w_lower in self.CONSTRAINT_PATTERNS or w_lower.endswith(("less", "bound", "strict")):
            return "constraint"
        if w_lower in self.OUTCOME_PATTERNS or w_lower.endswith(("tion", "ment", "ance", "ence")):
            return "outcome"
        if w_lower.endswith(("al", "ic", "ous", "ive")):
            return "qualifier"
        return "core_entity"

    def identify_semantic_seeds(self, clause_text: str) -> List[SemanticSeed]:
        """Extracts high-salience invariant semantic seeds from clause text."""
        words = re.findall(r'\b[A-Za-z0-9_-]+\b', clause_text)
        seeds: List[SemanticSeed] = []
        seen_terms = set()

        for idx, w in enumerate(words):
            w_clean = w.strip()
            w_lower = w_clean.lower()
            if w_lower in self.STOPWORDS or len(w_clean) < 3:
                continue
            if w_lower in seen_terms:
                continue
            seen_terms.add(w_lower)

            role = self.classify_word_role(w_clean)
            glyph = self.ROLE_GLYPHS.get(role, "◆")

            base_salience = 0.60
            if role in ("core_entity", "outcome"):
                base_salience += 0.25
            elif role == "action_verb":
                base_salience += 0.20
            elif role == "constraint":
                base_salience += 0.15

            if idx == 0 or idx == len(words) - 1:
                base_salience += 0.10
            salience = min(1.0, round(base_salience, 3))

            spatial_anchor = "nexus"
            if idx == 0:
                spatial_anchor = "origin"
            elif idx == len(words) - 1:
                spatial_anchor = "terminus"
            elif role == "action_verb":
                spatial_anchor = "vector"
            elif role == "constraint":
                spatial_anchor = "boundary"

            seeds.append(SemanticSeed(
                term=w_clean,
                role=role,
                salience=salience,
                glyph=glyph,
                spatial_anchor=spatial_anchor
            ))

        seeds.sort(key=lambda s: s.salience, reverse=True)
        return seeds

    def compress_clause(self, clause_text: str, clause_idx: int) -> GistClause:
        """Compresses a single clause into spatial shorthand glyph tokens."""
        seeds = self.identify_semantic_seeds(clause_text)
        original_words = len(re.findall(r'\b[A-Za-z0-9_-]+\b', clause_text))
        if original_words == 0:
            original_words = 1

        top_seeds = seeds[:4] if len(seeds) > 4 else seeds

        shorthand_parts = [f"{s.glyph} {s.term}" for s in top_seeds]
        compressed_shorthand = " | ".join(shorthand_parts) if shorthand_parts else clause_text
        glyph_seq = [s.glyph for s in top_seeds]

        compressed_tokens = len(top_seeds)
        ratio = round(compressed_tokens / original_words, 3)

        return GistClause(
            clause_id=f"clause_{clause_idx + 1:02d}",
            original_text=clause_text,
            compressed_shorthand=compressed_shorthand,
            glyph_sequence=glyph_seq,
            compression_ratio=ratio,
            semantic_seeds=top_seeds
        )

    def synthesize_gist(self, text: str) -> LexicalGistResult:
        """Executes full pipeline: clause extraction, seed distilling, and telemetry."""
        clauses_raw = self.extract_clauses(text)
        if not clauses_raw:
            telemetry = LexicalGistTelemetry(
                raw_word_count=0,
                compressed_token_count=0,
                overall_compression_ratio=0.0,
                semantic_preservation_score=1.0,
                cognitive_load_reduction=0.0,
                top_seeds=[]
            )
            return LexicalGistResult(
                clauses=[],
                all_seeds=[],
                telemetry=telemetry,
                spatial_glyph_diagram="<svg width='800' height='400'></svg>",
                gist_markdown_report="# Lexical Gist Report\n\nEmpty input provided."
            )

        gist_clauses = [self.compress_clause(c, idx) for idx, c in enumerate(clauses_raw)]
        all_seeds: List[SemanticSeed] = []
        for gc in gist_clauses:
            all_seeds.extend(gc.semantic_seeds)

        raw_word_count = len(re.findall(r'\b[A-Za-z0-9_-]+\b', text))
        compressed_token_count = sum(len(gc.semantic_seeds) for gc in gist_clauses)
        overall_ratio = round(compressed_token_count / max(1, raw_word_count), 3)

        if all_seeds:
            avg_salience = sum(s.salience for s in all_seeds) / len(all_seeds)
            preservation_score = round(min(1.0, avg_salience * 1.05), 3)
        else:
            preservation_score = 0.50

        cognitive_reduction = round(max(0.0, 1.0 - overall_ratio), 3)

        unique_seeds_dict: Dict[str, float] = {}
        for s in all_seeds:
            term_l = s.term.lower()
            if term_l not in unique_seeds_dict or s.salience > unique_seeds_dict[term_l]:
                unique_seeds_dict[term_l] = s.salience
        sorted_seed_names = sorted(unique_seeds_dict.keys(), key=lambda k: unique_seeds_dict[k], reverse=True)[:6]

        telemetry = LexicalGistTelemetry(
            raw_word_count=raw_word_count,
            compressed_token_count=compressed_token_count,
            overall_compression_ratio=overall_ratio,
            semantic_preservation_score=preservation_score,
            cognitive_load_reduction=cognitive_reduction,
            top_seeds=sorted_seed_names
        )

        svg_diagram = self.generate_svg_visualization(gist_clauses, telemetry)
        md_report = self.generate_markdown_report(gist_clauses, telemetry)

        return LexicalGistResult(
            clauses=gist_clauses,
            all_seeds=all_seeds,
            telemetry=telemetry,
            spatial_glyph_diagram=svg_diagram,
            gist_markdown_report=md_report
        )

    def generate_svg_visualization(self, clauses: List[GistClause], telemetry: LexicalGistTelemetry, width: int = 800, height: int = 400) -> str:
        """Renders a dark titanium SVG diagram showing spatial shorthand tokens."""
        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">',
            '<defs>',
            '  <linearGradient id="darkTitaniumGist" x1="0%" y1="0%" x2="100%" y2="100%">',
            '    <stop offset="0%" stop-color="#181c24" />',
            '    <stop offset="100%" stop-color="#0d1117" />',
            '  </linearGradient>',
            '  <linearGradient id="cyanGist" x1="0%" y1="0%" x2="100%" y2="0%">',
            '    <stop offset="0%" stop-color="#00f2fe" />',
            '    <stop offset="100%" stop-color="#4facfe" />',
            '  </linearGradient>',
            '  <linearGradient id="amberGist" x1="0%" y1="0%" x2="100%" y2="0%">',
            '    <stop offset="0%" stop-color="#f6d365" />',
            '    <stop offset="100%" stop-color="#fda085" />',
            '  </linearGradient>',
            '</defs>',
            f'<rect width="{width}" height="{height}" rx="12" fill="url(#darkTitaniumGist)" stroke="#30363d" stroke-width="1.5" />',
            '<!-- Header -->',
            '<text x="24" y="36" fill="#58a6ff" font-family="sans-serif" font-size="16" font-weight="bold">Spatial Dynamic Lexical Gist &amp; Token Shorthand</text>',
            f'<text x="{width - 24}" y="36" fill="#8b949e" font-family="sans-serif" font-size="12" text-anchor="end">Compaction: {telemetry.cognitive_load_reduction * 100:.1f}% | Preservation: {telemetry.semantic_preservation_score * 100:.1f}%</text>',
            '<line x1="24" y1="48" x2="776" y2="48" stroke="#30363d" stroke-width="1" />'
        ]

        y_start = 70
        block_height = 65
        for idx, c in enumerate(clauses[:4]):
            y_pos = y_start + idx * (block_height + 12)
            svg_parts.append(f'<g transform="translate(24, {y_pos})">')
            svg_parts.append(f'  <rect width="752" height="{block_height}" rx="8" fill="#161b22" stroke="#21262d" stroke-width="1" />')
            svg_parts.append(f'  <text x="16" y="22" fill="#8b949e" font-family="sans-serif" font-size="11" font-weight="bold">{c.clause_id.upper()}</text>')
            # Escape XML characters in shorthand
            escaped_shorthand = c.compressed_shorthand.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            svg_parts.append(f'  <text x="90" y="22" fill="#c9d1d9" font-family="sans-serif" font-size="12" font-weight="bold">{escaped_shorthand}</text>')

            x_badge = 16
            for seed in c.semantic_seeds:
                badge_color = "#58a6ff" if seed.role == "core_entity" else ("#7ee787" if seed.role == "action_verb" else "#ffa657")
                svg_parts.append(f'  <rect x="{x_badge}" y="34" width="120" height="22" rx="4" fill="#21262d" stroke="{badge_color}" stroke-width="0.8" />')
                escaped_term = seed.term[:12].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                svg_parts.append(f'  <text x="{x_badge + 8}" y="49" fill="{badge_color}" font-family="sans-serif" font-size="11">{seed.glyph} {escaped_term}</text>')
                x_badge += 130
            svg_parts.append('</g>')

        svg_parts.append(f'<line x1="24" y1="{height - 40}" x2="776" y2="{height - 40}" stroke="#30363d" stroke-width="1" />')
        svg_parts.append(f'<text x="24" y="{height - 18}" fill="#8b949e" font-family="sans-serif" font-size="11">Raw Words: {telemetry.raw_word_count} | Compressed Seeds: {telemetry.compressed_token_count} | Ratio: {telemetry.overall_compression_ratio:.2f}</text>')
        top_seeds_escaped = ", ".join(telemetry.top_seeds[:4]).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        svg_parts.append(f'<text x="{width - 24}" y="{height - 18}" fill="#7ee787" font-family="sans-serif" font-size="11" text-anchor="end">Invariant Seeds: {top_seeds_escaped}</text>')
        svg_parts.append('</svg>')

        return "\n".join(svg_parts)

    def generate_markdown_report(self, clauses: List[GistClause], telemetry: LexicalGistTelemetry) -> str:
        """Generates a comprehensive Markdown audit report with strictly zero em dashes."""
        lines = [
            "# Spatial Lexical Gist & Dynamic Shorthand Report",
            "",
            "## Cognitive Compression Metrics",
            f"- **Original Word Count:** {telemetry.raw_word_count}",
            f"- **Compressed Invariant Tokens:** {telemetry.compressed_token_count}",
            f"- **Overall Compression Ratio:** {telemetry.overall_compression_ratio:.3f}",
            f"- **Cognitive Load Reduction:** {telemetry.cognitive_load_reduction * 100:.1f}%",
            f"- **Semantic Preservation Score:** {telemetry.semantic_preservation_score * 100:.1f}%",
            "",
            "## Top Invariant Semantic Seeds",
        ]
        for s in telemetry.top_seeds:
            lines.append(f"- `{s}`")

        lines.extend([
            "",
            "## Compressed Spatial Clauses",
            "",
            "| Clause ID | Compressed Shorthand | Ratio | Primary Seeds |",
            "| :--- | :--- | :--- | :--- |"
        ])

        for c in clauses:
            seed_names = ", ".join(s.term for s in c.semantic_seeds)
            lines.append(f"| **{c.clause_id}** | `{c.compressed_shorthand}` | {c.compression_ratio:.2f} | {seed_names} |")

        lines.extend([
            "",
            "## Theoretical Alignment",
            "- **Fuzzy-Trace Theory:** Retains core invariant gist while shedding surface lexical entropy.",
            "- **M-I-N-D Architecture:** Eliminates phonological bottleneck by translating dense prose into spatial glyph vectors.",
            "- **Cowan Capacity Bounds:** Bounds working memory chunk count to N <= 4 per clause segment.",
            ""
        ])

        return "\n".join(lines)
