"""
Unit tests for Semantic Entropy Decoupler & Syntactic De-Noising Gate Engine.
Verifies Shannon entropy, signal-to-noise ratio (SNR in dB), hedging attenuation,
telemetry aggregation, SVG rendering, markdown reporting, and strict zero-em-dash compliance.
"""

import os
import pytest
from scripts.semantic_entropy_decoupler import (
    TextEntropyProfile,
    ManifoldEntropyTelemetry,
    SemanticEntropyDecoupler,
    sample_noisy_nodes,
)


def test_calculate_shannon_entropy():
    decoupler = SemanticEntropyDecoupler()
    assert decoupler.calculate_shannon_entropy([]) == 0.0

    # Single token repeated -> entropy 0.0
    assert decoupler.calculate_shannon_entropy(["node", "node", "node"]) == 0.0

    # 4 distinct tokens with uniform frequency -> entropy log2(4) = 2.0 bits
    assert decoupler.calculate_shannon_entropy(["a", "b", "c", "d"]) == pytest.approx(2.0, abs=1e-2)


def test_text_entropy_profile_initialization():
    profile = TextEntropyProfile(
        node_id="n1",
        title="Sample Node",
        raw_text="Test raw text",
        total_tokens=3,
        unique_tokens=3,
        shannon_entropy_bits=1.58,
        syntactic_noise_ratio=0.33,
        signal_to_noise_ratio_db=3.01,
        core_semantic_tokens=["test", "raw"],
        attenuated_noise_tokens=["text"],
        de_noised_text="Test raw",
    )
    assert profile.node_id == "n1"
    assert profile.title == "Sample Node"
    assert profile.total_tokens == 3
    assert profile.shannon_entropy_bits == 1.58
    assert profile.signal_to_noise_ratio_db == 3.01


def test_analyze_node_clean_vs_noisy():
    decoupler = SemanticEntropyDecoupler(snr_alert_threshold_db=3.0)

    clean_text = "Asymmetric cryptography validates digital signatures using elliptic curve discrete logarithms."
    noisy_text = "It seems that arguably in order to achieve consistency it might perhaps be useful to consider replication."

    clean_prof = decoupler.analyze_node("clean", "Clean Node", clean_text)
    noisy_prof = decoupler.analyze_node("noisy", "Noisy Node", noisy_text)

    # Clean text should have high SNR and low noise ratio
    assert clean_prof.signal_to_noise_ratio_db > noisy_prof.signal_to_noise_ratio_db
    assert clean_prof.syntactic_noise_ratio < noisy_prof.syntactic_noise_ratio
    assert clean_prof.signal_to_noise_ratio_db > 3.0
    assert noisy_prof.signal_to_noise_ratio_db < 3.0

    # De-noised text should isolate key nouns
    assert "cryptography" in clean_prof.core_semantic_tokens
    assert "signatures" in clean_prof.core_semantic_tokens


def test_analyze_node_empty():
    decoupler = SemanticEntropyDecoupler()
    prof = decoupler.analyze_node("empty", "Empty Node", "   ")
    assert prof.total_tokens == 0
    assert prof.shannon_entropy_bits == 0.0
    assert prof.signal_to_noise_ratio_db == 0.0
    assert prof.de_noised_text == ""


def test_analyze_nodes_aggregation():
    decoupler = SemanticEntropyDecoupler(snr_alert_threshold_db=3.0)
    nodes = sample_noisy_nodes()
    telemetry = decoupler.analyze_nodes(nodes)

    assert telemetry.node_count == 4
    assert telemetry.mean_entropy_bits > 0.0
    assert len(telemetry.profiles) == 4
    assert telemetry.high_noise_nodes_count >= 1  # At least node-2 or node-4 should trigger warning


def test_generate_markdown_report():
    decoupler = SemanticEntropyDecoupler()
    nodes = sample_noisy_nodes()
    telemetry = decoupler.analyze_nodes(nodes)
    report = decoupler.generate_markdown_report(telemetry)

    assert "# Semantic Entropy Decoupler and Syntactic De-Noising Report" in report
    assert "Shannon Information Entropy" in report
    assert "Node Entropy & Signal-to-Noise Catalog" in report
    assert "Clean Core" in report


def test_generate_svg():
    decoupler = SemanticEntropyDecoupler()
    nodes = sample_noisy_nodes()
    telemetry = decoupler.analyze_nodes(nodes)
    svg = decoupler.generate_svg(telemetry, width=900, height=540)

    assert "<svg" in svg
    assert "</svg>" in svg
    assert "SEMANTIC ENTROPY DECOUPLER HUD" in svg
    assert "0 dB" in svg
    assert "Clean Core" in svg or "Clean" in svg


def test_zero_em_dashes_in_source_and_outputs():
    # Verify module source file
    script_path = os.path.join(os.path.dirname(__file__), "..", "scripts", "semantic_entropy_decoupler.py")
    with open(script_path, "r", encoding="utf-8") as f:
        source = f.read()
    assert chr(8212) not in source

    # Verify report and svg outputs
    decoupler = SemanticEntropyDecoupler()
    nodes = sample_noisy_nodes()
    telemetry = decoupler.analyze_nodes(nodes)
    report = decoupler.generate_markdown_report(telemetry)
    svg = decoupler.generate_svg(telemetry)

    assert chr(8212) not in report
    assert chr(8212) not in svg
