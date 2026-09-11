"""
Unit tests for Autonomous Cognitive Spatial Dynamic Lexical Compression & Semantic Gist Synthesizer.
Strictly NO em dashes (\u2014) anywhere.
"""

import pytest
from scripts.lexical_gist_compressor import (
    SemanticSeed,
    GistClause,
    LexicalGistTelemetry,
    LexicalGistResult,
    LexicalGistCompressor
)

SAMPLE_PROSE = (
    "The spatial knowledge graph transforms unstructured textual notes into topological coordinates. "
    "Working memory constraints strictly bound the simultaneous activation threshold to four chunks, "
    "which yields stable cognitive equilibrium and protects executive focus against attentional fatigue."
)

def test_clause_extraction():
    compressor = LexicalGistCompressor()
    clauses = compressor.extract_clauses(SAMPLE_PROSE)
    assert len(clauses) >= 2
    assert any("knowledge graph" in c.lower() or "transforms" in c.lower() for c in clauses)

def test_word_role_classification():
    compressor = LexicalGistCompressor()
    assert compressor.classify_word_role("transforms") == "action_verb"
    assert compressor.classify_word_role("synthesizes") == "action_verb"
    assert compressor.classify_word_role("strictly") == "constraint"
    assert compressor.classify_word_role("invariant") == "constraint"
    assert compressor.classify_word_role("equilibrium") == "outcome"
    assert compressor.classify_word_role("topological") == "qualifier"
    assert compressor.classify_word_role("coordinates") == "action_verb" or compressor.classify_word_role("coordinates") == "core_entity"

def test_semantic_seed_extraction():
    compressor = LexicalGistCompressor()
    clause = "Working memory constraints strictly bound the simultaneous activation threshold"
    seeds = compressor.identify_semantic_seeds(clause)
    assert len(seeds) > 0
    # Stopwords like 'the' should be excluded
    terms = [s.term.lower() for s in seeds]
    assert "the" not in terms
    assert all(s.salience >= 0.0 and s.salience <= 1.0 for s in seeds)
    assert any(s.glyph in ("◆", "➔", "■", "◎", "▲", "⚡") for s in seeds)

def test_clause_compression_capacity_bounds():
    compressor = LexicalGistCompressor()
    clause = "The spatial knowledge graph transforms unstructured textual notes into topological coordinates"
    gc = compressor.compress_clause(clause, 0)
    assert gc.clause_id == "clause_01"
    # Working memory bound: at most 4 seeds
    assert len(gc.semantic_seeds) <= 4
    assert gc.compression_ratio < 1.0
    assert " | " in gc.compressed_shorthand or len(gc.semantic_seeds) <= 1

def test_full_pipeline_synthesis():
    compressor = LexicalGistCompressor()
    res = compressor.synthesize_gist(SAMPLE_PROSE)
    assert isinstance(res, LexicalGistResult)
    assert len(res.clauses) >= 2
    assert res.telemetry.raw_word_count > res.telemetry.compressed_token_count
    assert res.telemetry.overall_compression_ratio < 1.0
    assert res.telemetry.cognitive_load_reduction > 0.0
    assert res.telemetry.semantic_preservation_score > 0.50
    assert len(res.telemetry.top_seeds) > 0

def test_svg_generation_dark_titanium():
    compressor = LexicalGistCompressor()
    res = compressor.synthesize_gist(SAMPLE_PROSE)
    svg = res.spatial_glyph_diagram
    assert "<svg" in svg
    assert "</svg>" in svg
    assert "darkTitaniumGist" in svg
    assert "Spatial Dynamic Lexical Gist" in svg

def test_markdown_report_structure():
    compressor = LexicalGistCompressor()
    res = compressor.synthesize_gist(SAMPLE_PROSE)
    md = res.gist_markdown_report
    assert "# Spatial Lexical Gist & Dynamic Shorthand Report" in md
    assert "Cognitive Compression Metrics" in md
    assert "Compressed Spatial Clauses" in md
    assert chr(8212) not in md

def test_empty_input_handling():
    compressor = LexicalGistCompressor()
    res = compressor.synthesize_gist("")
    assert res.telemetry.raw_word_count == 0
    assert res.telemetry.compressed_token_count == 0
    assert len(res.clauses) == 0
