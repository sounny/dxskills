"""
test_epistemic_uncertainty_radar.py - Unit tests for EpistemicUncertaintyRadar (Phase 106, Cycle 102).

Tests Toulmin empirical grounding calibration, fragility stress vectors,
polar radar SVG export, markdown mitigation table, and zero em dashes.

Strict constraint: Strictly zero em dashes (Unicode U+2014) anywhere.
"""

from pathlib import Path
import pytest
from scripts.epistemic_uncertainty_radar import (
    EpistemicClaim,
    EpistemicRadarResult,
    EpistemicTelemetry,
    EpistemicUncertaintyRadar,
    FragilityStressVector,
)


@pytest.fixture
def architectural_claims_sample():
    return [
        {
            "id": "clm_1",
            "statement": "Hardware-accelerated CSS transforms maintain steady 60fps benchmark telemetry.",
            "category": "PERFORMANCE",
            "grounding_tier": "EMPIRICAL",
            "confidence_score": 0.98,
            "fragility_index": 0.12,
        },
        {
            "id": "clm_2",
            "statement": "Anstis retinal acuity decay equation models peripheral visual dropout correctly.",
            "category": "ARCHITECTURE",
            "grounding_tier": "THEORETICAL",
            "confidence_score": 0.85,
            "fragility_index": 0.28,
        },
        {
            "id": "clm_3",
            "statement": "Typical reading speed will remain stable across variable display contrasts.",
            "category": "ERGONOMICS",
            "grounding_tier": "HEURISTIC",
            "confidence_score": 0.58,
            "fragility_index": 0.65,
        },
        {
            "id": "clm_4",
            "statement": "We assume memory pressure will probably not trigger mobile browser tab reloads.",
            "category": "ARCHITECTURE",
            "grounding_tier": "SPECULATIVE",
            "confidence_score": 0.25,
            "fragility_index": 0.92,
        },
    ]


def test_empty_radar():
    radar = EpistemicUncertaintyRadar()
    result = radar.evaluate_claims(raw_claims=[])
    assert isinstance(result, EpistemicRadarResult)
    assert result.telemetry.total_claims_analyzed == 0
    assert result.telemetry.mean_confidence_score == 0.0
    assert result.telemetry.mean_fragility_index == 0.0
    assert result.telemetry.cowan_bounded is True
    assert len(result.claims) == 0
    assert len(result.stress_vectors) == 0
    assert result.svg_radar == ""
    assert result.mitigation_table_md == ""


def test_evaluate_claims_and_calibration(architectural_claims_sample):
    radar = EpistemicUncertaintyRadar()
    result = radar.evaluate_claims(raw_claims=architectural_claims_sample)

    assert result.telemetry.total_claims_analyzed == 4
    assert result.telemetry.mean_confidence_score > 0.60
    assert result.telemetry.mean_fragility_index < 0.60
    assert result.telemetry.antifragility_rating > 50.0
    assert result.telemetry.cowan_bounded is True

    # Validate claim tiers and severities
    c1, c2, c3, c4 = result.claims
    assert c1.grounding_tier == "EMPIRICAL"
    assert c1.failure_severity == "LOW"
    assert c2.grounding_tier == "THEORETICAL"
    assert c2.failure_severity == "MODERATE"
    assert c3.grounding_tier == "HEURISTIC"
    assert c3.failure_severity == "SEVERE"
    assert c4.grounding_tier == "SPECULATIVE"
    assert c4.failure_severity == "CRITICAL"


def test_keyword_tier_inference():
    radar = EpistemicUncertaintyRadar()
    raw = [
        {"id": "c_data", "statement": "Continuous measured benchmark data confirms throughput."},
        {"id": "c_theo", "statement": "The formal theorem published in literature holds."},
        {"id": "c_heur", "statement": "Our experience and standard rule of thumb works."},
        {"id": "c_spec", "statement": "We guess and assume this should probably work."},
    ]
    result = radar.evaluate_claims(raw_claims=raw)
    tiers = [c.grounding_tier for c in result.claims]
    assert tiers == ["EMPIRICAL", "THEORETICAL", "HEURISTIC", "SPECULATIVE"]


def test_stress_vector_adversarial_simulation(architectural_claims_sample):
    radar = EpistemicUncertaintyRadar()
    custom_scenarios = [
        {"id": "vec_custom_1", "name": "3x CPU Throttling Stress", "multiplier": 3.0},
        {"id": "vec_custom_2", "name": "10x DOM Element Explosion", "multiplier": 10.0},
    ]
    result = radar.evaluate_claims(raw_claims=architectural_claims_sample, stress_scenarios=custom_scenarios)

    assert len(result.stress_vectors) == 2
    sv1, sv2 = result.stress_vectors
    assert sv1.vector_id == "vec_custom_1"
    assert sv2.vector_id == "vec_custom_2"
    assert sv2.cascade_failure_probability_pct > sv1.cascade_failure_probability_pct
    assert sv2.resilience_verdict in ["VULNERABLE", "COLLAPSED"]


def test_cowan_bounding_exceeded():
    radar = EpistemicUncertaintyRadar(fragility_threshold=0.50)
    fragile_claims = [
        {"id": f"frag_{i}", "statement": f"Brittle assumption {i}", "grounding_tier": "SPECULATIVE"}
        for i in range(6)
    ]
    result = radar.evaluate_claims(raw_claims=fragile_claims)
    assert result.telemetry.high_fragility_count == 6
    assert result.telemetry.cowan_bounded is False
    assert result.telemetry.epistemic_drift_risk in ["ELEVATED", "CRITICAL"]


def test_svg_export(tmp_path: Path, architectural_claims_sample):
    radar = EpistemicUncertaintyRadar()
    result = radar.evaluate_claims(raw_claims=architectural_claims_sample)

    svg_file = tmp_path / "epistemic_radar.svg"
    svg_str = radar.export_svg(result, output_path=str(svg_file))

    assert "<svg" in svg_str
    assert "</svg>" in svg_str
    assert "Epistemic Uncertainty Radar" in svg_str
    assert svg_file.exists()
    assert svg_file.stat().st_size > 500


def test_ascii_report(architectural_claims_sample):
    radar = EpistemicUncertaintyRadar()
    result = radar.evaluate_claims(raw_claims=architectural_claims_sample)
    report = radar.generate_ascii_report(result)

    assert "EPISTEMIC UNCERTAINTY RADAR" in report
    assert "Claims Evaluated" in report
    assert "Antifragility Rating" in report
    assert "[STRESS]" in report
    assert "clm_1" in report


def test_markdown_mitigation_table(architectural_claims_sample):
    radar = EpistemicUncertaintyRadar()
    result = radar.evaluate_claims(raw_claims=architectural_claims_sample)

    table = result.mitigation_table_md
    assert "| Claim ID | Category | Grounding |" in table
    assert "`clm_1`" in table
    assert "[CRITICAL]" in table
    assert "fallback redundancy" in table


def test_zero_em_dashes():
    source_files = [
        Path("scripts/epistemic_uncertainty_radar.py"),
        Path("tests/test_epistemic_uncertainty_radar.py"),
    ]
    for p in source_files:
        if p.exists():
            text = p.read_text(encoding="utf-8")
            assert "\u2014" not in text, f"Em dash found in {p}"
