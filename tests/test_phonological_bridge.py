"""
Unit tests for Autonomous Cognitive Spatial Multimodal Phonological Loop Bridge & Grapheme Resonator.
Strictly NO em dashes (\u2014) anywhere.
"""

import pytest
from scripts.phonological_bridge import (
    GraphemeToken,
    PhonologicalBridgeTelemetry,
    PhonologicalBridgeResult,
    PhonologicalLoopBridge
)

SAMPLE_TEXT = (
    "The epistemological structure of algebraic topology presents orthographic friction. "
    "Complex phonological dissonance stalls ocular saccades during rapid comprehension."
)

def test_syllable_decomposition():
    bridge = PhonologicalLoopBridge()
    syllables = bridge.decompose_syllables("epistemological")
    assert len(syllables) >= 3
    short = bridge.decompose_syllables("cat")
    assert len(short) == 1

def test_friction_score_computation():
    bridge = PhonologicalLoopBridge()
    f_complex = bridge.compute_friction_score("strengths")
    f_simple = bridge.compute_friction_score("top")
    assert f_complex > f_simple
    assert 0.0 <= f_complex <= 1.0

def test_evaluate_text_pipeline():
    bridge = PhonologicalLoopBridge()
    res = bridge.evaluate_text(SAMPLE_TEXT)
    assert len(res.tokens) > 5
    # Should be sorted by friction descending
    for i in range(len(res.tokens) - 1):
        assert res.tokens[i].friction_score >= res.tokens[i + 1].friction_score

def test_telemetry_metrics():
    bridge = PhonologicalLoopBridge()
    res = bridge.evaluate_text(SAMPLE_TEXT)
    tel = res.telemetry
    assert tel.total_tokens > 0
    assert tel.mean_friction_score > 0.0
    assert tel.phonological_load_index > 0.0
    assert 100.0 <= tel.recommended_pacing_wpm <= 240.0

def test_dissonance_thresholding():
    bridge = PhonologicalLoopBridge()
    res = bridge.evaluate_text("epistemological strengths simple")
    levels = [t.dissonance_level for t in res.tokens]
    assert any(lvl in ("critical", "high", "moderate") for lvl in levels)

def test_to_dict_serialization():
    bridge = PhonologicalLoopBridge()
    res = bridge.evaluate_text(SAMPLE_TEXT)
    d = res.to_dict()
    assert "tokens" in d
    assert "telemetry" in d
    assert len(d["tokens"]) == len(res.tokens)

def test_svg_rendering_elements():
    bridge = PhonologicalLoopBridge()
    res = bridge.evaluate_text(SAMPLE_TEXT)
    svg = res.resonance_map_svg
    assert "<svg" in svg
    assert "</svg>" in svg
    assert "titaniumPhonoBg" in svg
    assert "Multimodal Phonological Loop Bridge" in svg

def test_markdown_report_zero_em_dashes():
    bridge = PhonologicalLoopBridge()
    res = bridge.evaluate_text(SAMPLE_TEXT)
    md = res.audit_report_md
    assert "# Phonological Loop Bridge & Grapheme Resonator Report" in md
    assert "Cognitive Phonological Metrics" in md
    assert "Grapheme Friction Classification" in md
    assert chr(8212) not in md

def test_empty_text_handling():
    bridge = PhonologicalLoopBridge()
    res = bridge.evaluate_text("")
    assert res.telemetry.total_tokens == 0
    assert len(res.tokens) == 0
