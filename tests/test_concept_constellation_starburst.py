"""
Unit tests for Concept Constellation & Synesthetic Starburst Engine.
Verifies celestial coordinate mapping, harmonic auditory frequency assignment,
spectral chromatic categorization, asterism tether synthesis, dark titanium
SVG starburst generation, and markdown telemetry. Strictly zero em dashes enforced.
"""

import pytest
from scripts.concept_constellation_starburst import (
    CelestialConcept,
    ConstellationEdge,
    ConstellationAsterism,
    ConstellationTelemetry,
    ConceptConstellationStarburst,
    sample_concept_stars,
    SPECTRAL_PALETTE,
)


def test_celestial_concept_initialization():
    star = CelestialConcept(
        concept_id="c-1",
        title="Allocentric Anchor",
        magnitude=1.5,
        spectral_class="O",
        frequency_hz=440.0,
        pos_x=250.0,
        pos_y=180.0,
        cluster_id="spatial",
    )
    assert star.concept_id == "c-1"
    assert star.magnitude == 1.5
    assert star.spectral_class == "O"
    assert star.frequency_hz == 440.0
    assert star.cluster_id == "spatial"


def test_synthesize_constellation_empty():
    engine = ConceptConstellationStarburst()
    telemetry = engine.synthesize_constellation([])
    assert telemetry.total_stars == 0
    assert telemetry.total_asterisms == 0
    assert telemetry.mean_resonance == 1.0
    assert len(telemetry.stars) == 0
    assert len(telemetry.edges) == 0
    assert len(telemetry.asterisms) == 0


def test_synthesize_constellation_clusters_and_edges():
    engine = ConceptConstellationStarburst()
    raw = sample_concept_stars()
    telemetry = engine.synthesize_constellation(raw)

    assert telemetry.total_stars == len(raw)
    assert telemetry.total_asterisms == 3  # spatial, reasoning, executive
    assert len(telemetry.edges) > 0

    # Verify bounding boxes are valid
    for ast in telemetry.asterisms:
        min_x, min_y, max_x, max_y = ast.bounding_box
        assert min_x <= max_x
        assert min_y <= max_y
        assert ast.luminary_count > 0


def test_spectral_palette_mapping():
    for spec_class, hex_code in SPECTRAL_PALETTE.items():
        assert hex_code.startswith("#")
        assert len(hex_code) == 7


def test_harmonic_frequency_assignment():
    engine = ConceptConstellationStarburst()
    raw = sample_concept_stars()
    telemetry = engine.synthesize_constellation(raw)

    for star in telemetry.stars:
        assert 200.0 <= star.frequency_hz <= 1000.0


def test_cowan_compliance_check():
    engine = ConceptConstellationStarburst()
    raw = sample_concept_stars()  # 3 asterisms with <= 3 stars each
    telemetry = engine.synthesize_constellation(raw)

    assert telemetry.cowan_compliant is True
    assert 0.0 <= telemetry.mean_resonance <= 1.0


def test_generate_svg():
    engine = ConceptConstellationStarburst()
    raw = sample_concept_stars()
    telemetry = engine.synthesize_constellation(raw)

    svg_code = engine.generate_svg(telemetry)
    assert "<svg" in svg_code
    assert "</svg>" in svg_code
    assert "nebulaGlow" in svg_code
    assert "CONCEPT CONSTELLATION ENGINE" in svg_code
    assert chr(8212) not in svg_code


def test_generate_markdown_report():
    engine = ConceptConstellationStarburst()
    raw = sample_concept_stars()
    telemetry = engine.synthesize_constellation(raw)

    md_report = engine.generate_markdown_report(telemetry)
    assert "# Concept Constellation and Synesthetic Starburst Telemetry" in md_report
    assert "## 1. Celestial Synthesis Overview" in md_report
    assert "## 2. Spectral Chromatic Distribution" in md_report
    assert "## 3. Celestial Concept Catalog" in md_report
    assert "## 4. Constellation Asterism Profiles" in md_report
    assert chr(8212) not in md_report
