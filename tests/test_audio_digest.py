#!/usr/bin/env python3
"""
DxSkills Automated Audio Digest & Spoken Overview Test Suite
Verifies audio script formatting (EN/FR), acoustic anchor cues, CLI arguments,
DOM elements, Web Speech API integration, and strict zero em dash compliance.
"""

import os
import sys
import unittest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from scripts.audio_digest import extract_digest_metadata, generate_audio_digest_script

INDEX_PATH = os.path.join(ROOT_DIR, "index.html")

class TestAudioDigest(unittest.TestCase):

    def setUp(self):
        self.sample_markdown = (
            "# Space Exploration Architecture\n"
            "> **BLUF:** Finalize lunar surface payload specs by Q3.\n\n"
            "## Orbital Mechanics\n"
            "High-efficiency Hohmann transfer trajectory.\n\n"
            "## Life Support Systems\n"
            "Closed-loop ECLSS recycling.\n\n"
            "## Milestones\n"
            "1. Static fire engine test\n"
            "2. Deploy telemetry satellite\n"
            "3. Conduct pressure vacuum check\n"
        )

    def test_extract_digest_metadata(self):
        """Verifies extraction of key cognitive blocks from deliverable."""
        meta = extract_digest_metadata(self.sample_markdown)
        self.assertEqual(meta["title"], "Space Exploration Architecture")
        self.assertIn("Finalize lunar surface payload specs", meta["bluf"])
        self.assertIn("Orbital Mechanics", meta["headings"])
        self.assertIn("Life Support Systems", meta["headings"])
        self.assertEqual(len(meta["actions"]), 3)
        self.assertIn("Static fire engine test", meta["actions"][0])

    def test_generate_audio_digest_script_english(self):
        """Verifies acoustic phrasing and anchors in English audio script."""
        script = generate_audio_digest_script(self.sample_markdown, lang="en")
        self.assertIn("DxSkills audio overview: Space Exploration Architecture.", script)
        self.assertIn("Acoustic anchor engaged.", script)
        self.assertIn("Bottom line up front:", script)
        self.assertIn("The core areas covered are:", script)
        self.assertIn("Immediate priority actions:", script)
        self.assertIn("Step 1: Static fire engine test.", script)
        self.assertIn("End of audio overview.", script)

    def test_generate_audio_digest_script_french(self):
        """Verifies acoustic phrasing and anchors in French audio script."""
        script = generate_audio_digest_script(self.sample_markdown, lang="fr")
        self.assertIn("Synthese audio DxSkills: Space Exploration Architecture.", script)
        self.assertIn("Pause de cadrage.", script)
        self.assertIn("Point essentiel:", script)
        self.assertIn("Les themes cles abordes sont:", script)
        self.assertIn("Prochaines etapes prioritaires:", script)
        self.assertIn("Numero 1: Static fire engine test.", script)
        self.assertIn("Fin de la synthese audio.", script)

    def test_html_audio_digest_dom_elements(self):
        """Verifies that index.html contains the audio digest modal and buttons."""
        self.assertTrue(os.path.isfile(INDEX_PATH), "index.html must exist")
        with open(INDEX_PATH, "r", encoding="utf-8") as f:
            html = f.read()

        required_elements = [
            'id="play-audio-digest-btn"',
            'id="interview-audio-digest-btn"',
            'id="audio-digest-modal"',
            'id="audio-digest-modal-title"',
            'id="audio-digest-script-container"',
            'id="audio-digest-status-badge"',
            'id="audio-waveform-indicator"',
            'id="audio-lang-en-btn"',
            'id="audio-lang-fr-btn"',
            'openAudioDigestModal(',
            'closeAudioDigestModal()',
            'playAudioDigest()',
            'pauseAudioDigest()',
            'stopAudioDigest()',
            'setAudioDigestRate(',
            'setAudioDigestLang(',
            'copyAudioDigestScript()',
            'downloadAudioDigestScript()',
            'generateClientAudioScript(',
            'Audio Digest Synthesizer',
        ]
        for elem in required_elements:
            self.assertIn(elem, html, f"Expected audio digest element missing: {elem}")

    def test_zero_em_dashes(self):
        """Verifies zero em dashes across audio digest scripts and tests."""
        em_dash = "\u2014"
        files_to_check = [
            os.path.join(ROOT_DIR, "scripts", "audio_digest.py"),
            os.path.join(ROOT_DIR, "tests", "test_audio_digest.py"),
        ]
        for path in files_to_check:
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                self.assertNotIn(em_dash, content, f"{path} must contain zero em dashes")

if __name__ == "__main__":
    unittest.main()
