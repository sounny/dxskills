"""
test_lexical_stress_tester.py - Unit tests for LexicalStressTester (Phase 101, Cycle 97).

Tests Just & Carpenter capacity parsing, lexical friction scoring,
micro-fixation stepping stone generation, Cowan chunk bounding, SVG export,
and zero em dashes.

Strict constraint: Strictly zero em dashes (Unicode U+2014) anywhere.
"""

from pathlib import Path
import pytest
from scripts.lexical_stress_tester import (
    CodeBlockScope,
    LexicalStressResult,
    LexicalStressTelemetry,
    LexicalStressTester,
    SyntacticToken,
)


@pytest.fixture
def sample_nested_code() -> str:
    return '''
def process_spatial_lattice(node_catalog: dict) -> list:
    active_anchors = []
    for category, cluster in node_catalog.items():
        if cluster.is_active():
            for item in cluster.elements:
                if item.friction_score > 0.65:
                    resolved_concept_identifier = item.synthesize_anchor()
                    active_anchors.append(resolved_concept_identifier)
    return active_anchors
'''


def test_empty_syntax():
    tester = LexicalStressTester()
    result = tester.parse_syntax("")
    assert isinstance(result, LexicalStressResult)
    assert result.telemetry.total_lines == 0
    assert result.telemetry.total_tokens == 0
    assert result.telemetry.max_nesting_depth == 0
    assert result.telemetry.mean_lexical_friction_index == 0.0
    assert result.telemetry.cognitive_drag_level == "NOMINAL"
    assert result.telemetry.stepping_stones_synthesized == 0
    assert result.telemetry.cowan_bounded is True
    assert len(result.stepping_stones) == 0


def test_syntax_parsing_and_friction(sample_nested_code):
    tester = LexicalStressTester(max_acceptable_depth=3, friction_threshold=0.55)
    result = tester.parse_syntax(sample_nested_code)

    assert result.telemetry.total_lines > 5
    assert result.telemetry.total_tokens > 20
    assert result.telemetry.max_nesting_depth >= 4
    assert result.telemetry.mean_lexical_friction_index > 0.1
    assert result.telemetry.stepping_stones_synthesized >= 3
    assert result.telemetry.focal_working_memory_reduction_pct > 25.0

    # Verify stepping stones contain key landmarks
    stone_texts = [s.text for s in result.stepping_stones]
    assert "def" in stone_texts
    assert "return" in stone_texts
    assert any("resolved_concept_identifier" in t for t in stone_texts)


def test_cowan_chunk_bounding():
    tester = LexicalStressTester()

    # Shallow code: nesting depth <= 2 -> Cowan bounded True
    shallow_code = '''
def calculate_offset(x, y):
    return x + y
'''
    res_shallow = tester.parse_syntax(shallow_code)
    assert res_shallow.telemetry.max_nesting_depth <= 2
    assert res_shallow.telemetry.cowan_bounded is True

    # Deeply nested code: nesting depth > 4 -> Cowan bounded False
    deep_code = '''
def deep_hierarchy():
    if True:
        for a in [1]:
            while True:
                try:
                    with open("test"):
                        return 42
                except Exception:
                    pass
'''
    res_deep = tester.parse_syntax(deep_code)
    assert res_deep.telemetry.max_nesting_depth >= 5
    assert res_deep.telemetry.cowan_bounded is False


def test_svg_export(tmp_path: Path, sample_nested_code):
    tester = LexicalStressTester()
    result = tester.parse_syntax(sample_nested_code)

    svg_file = tmp_path / "lexical_stress.svg"
    svg_content = tester.export_svg(result, output_path=str(svg_file))

    assert "<svg" in svg_content
    assert "</svg>" in svg_content
    assert "Syntactic Lexical Stress-Tester" in svg_content
    assert svg_file.exists()
    assert svg_file.stat().st_size > 500


def test_ascii_report(sample_nested_code):
    tester = LexicalStressTester()
    result = tester.parse_syntax(sample_nested_code)
    report = tester.generate_ascii_report(result)

    assert "SYNTACTIC LEXICAL STRESS-TESTER & STEPPING STONES" in report
    assert "Lines Analyzed" in report
    assert "Lexical Friction" in report
    assert "Working Memory Saved" in report
    assert "[STONE]" in report


def test_zero_em_dashes():
    source_files = [
        Path("scripts/lexical_stress_tester.py"),
        Path("tests/test_lexical_stress_tester.py"),
    ]
    for p in source_files:
        if p.exists():
            text = p.read_text(encoding="utf-8")
            assert "\u2014" not in text, f"Em dash found in {p}"
