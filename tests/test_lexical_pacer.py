"""
test_lexical_pacer.py - Unit tests for LexicalPacer (Phase 98, Cycle 94).

Tests sub-lexical fixation point synthesizer, Rayner OVP calculation,
adaptive reading speed governor, SVG export, HTML reader export, and zero em dashes.

Strict constraint: Strictly zero em dashes (Unicode U+2014) anywhere.
"""

from pathlib import Path
import pytest
from scripts.lexical_pacer import (
    FixationAnchor,
    LexicalPacer,
    LexicalPacerResult,
    LexicalPacerTelemetry,
    PacedLine,
)


@pytest.fixture
def sample_text():
    return (
        "Distributed systems require explicit boundary decoupling to maintain resilience.\n"
        "When microservices mutate shared state concurrently, data divergence triggers cascading latency.\n"
        "Local-first architectures with deterministic conflict-free resolution provide optimal throughput."
    )


def test_empty_text():
    pacer = LexicalPacer()
    result = pacer.pace_text("")
    assert isinstance(result, LexicalPacerResult)
    assert len(result.lines) == 0
    assert result.telemetry.total_words == 0
    assert result.bionic_markdown == ""
    assert result.bionic_html == ""


def test_count_syllables():
    pacer = LexicalPacer()
    assert pacer.count_syllables("cat") == 1
    assert pacer.count_syllables("system") == 2
    assert pacer.count_syllables("architecture") >= 4


def test_calculate_ovp():
    pacer = LexicalPacer()
    assert pacer.calculate_ovp("cat") == 0
    assert pacer.calculate_ovp("system") == 1
    assert pacer.calculate_ovp("distributed") >= 2


def test_synthesize_anchor_technical_words():
    pacer = LexicalPacer()

    # Long technical word
    anchor = pacer.synthesize_anchor("Decoupled")
    assert isinstance(anchor, FixationAnchor)
    assert anchor.prefix_len >= 3
    assert anchor.prefix == "Dec" or anchor.prefix == "Deco"
    assert anchor.is_stop_word is False
    assert anchor.estimated_fixation_ms > 150.0

    # Stop word
    stop_anchor = pacer.synthesize_anchor("the")
    assert stop_anchor.is_stop_word is True
    assert stop_anchor.prefix_len <= 1

    # Word with punctuation
    punct_anchor = pacer.synthesize_anchor("(resilience).")
    assert punct_anchor.prefix.startswith("(")
    assert punct_anchor.suffix.endswith(").")


def test_pace_text(sample_text):
    pacer = LexicalPacer(target_wpm=280)
    result = pacer.pace_text(sample_text)

    assert len(result.lines) == 3
    assert result.telemetry.total_words > 20
    assert result.telemetry.bionic_coverage_pct > 80.0
    assert result.telemetry.predicted_regression_reduction_pct > 25.0
    assert "**Dis" in result.bionic_markdown or "**Dist" in result.bionic_markdown
    assert '<span class="dx-anchor' in result.bionic_html


def test_svg_export(sample_text, tmp_path):
    pacer = LexicalPacer()
    result = pacer.pace_text(sample_text)

    svg_file = tmp_path / "lexical_pacer.svg"
    svg_content = pacer.export_svg(result, str(svg_file))

    assert svg_file.exists()
    assert "<svg" in svg_content
    assert "</svg>" in svg_content
    assert "Bionic Lexical Pacing" in svg_content
    assert "PRIMARY FOVEAL ANCHOR (OVP)" in svg_content


def test_html_reader_export(sample_text, tmp_path):
    pacer = LexicalPacer()
    result = pacer.pace_text(sample_text)

    html_file = tmp_path / "reader.html"
    html_content = pacer.export_html_reader(result, str(html_file))

    assert html_file.exists()
    assert "<!DOCTYPE html>" in html_content
    assert "dx-paced-line" in html_content
    assert "dx-anchor" in html_content


def test_ascii_report(sample_text):
    pacer = LexicalPacer()
    result = pacer.pace_text(sample_text)
    report = pacer.generate_ascii_report(result)

    assert "DYNAMIC LEXICAL PACING" in report
    assert "Regression Reduction" in report
    assert "Target Reading Cadence" in report
    assert "Line 01" in report


def test_zero_em_dashes():
    """Verify strictly zero em dashes in code and test files."""
    files_to_check = [
        Path("scripts/lexical_pacer.py"),
        Path("tests/test_lexical_pacer.py"),
    ]
    em_dash = chr(8212)
    for fpath in files_to_check:
        if fpath.exists():
            text = fpath.read_text(encoding="utf-8")
            assert em_dash not in text, f"Em dash found in {fpath}"
