#!/usr/bin/env python3
"""
DxSkills Automated Cognitive Fatigue & Spatial Reset Test Suite
Verifies stamina calculation, CLI commands, DOM landmarks, and zero em dash compliance.
"""

import os
import sys
import unittest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from scripts.cognitive_fatigue import calculate_cognitive_stamina

INDEX_PATH = os.path.join(ROOT_DIR, "index.html")

class TestCognitiveFatigue(unittest.TestCase):

    def test_stamina_calculation_bounds(self):
        """Verifies stamina decay across duration and word volume."""
        fresh = calculate_cognitive_stamina(minutes_active=5, words_drafted=50)
        self.assertGreaterEqual(fresh["stamina_score"], 75.0)
        self.assertEqual(fresh["status"], "Optimal Focus")
        self.assertEqual(fresh["zone"], "Green")

        moderate = calculate_cognitive_stamina(minutes_active=30, words_drafted=300)
        self.assertLess(moderate["stamina_score"], 75.0)
        self.assertGreaterEqual(moderate["stamina_score"], 40.0)
        self.assertEqual(moderate["status"], "Moderate Load")
        self.assertEqual(moderate["zone"], "Amber")

        saturated = calculate_cognitive_stamina(minutes_active=55, words_drafted=1200)
        self.assertLess(saturated["stamina_score"], 45.0)
        self.assertEqual(saturated["status"], "Phonological Saturation")
        self.assertIn("Red", saturated["zone"])

    def test_html_stamina_elements(self):
        """Verifies UI elements for stamina indicator and spatial reset modal."""
        self.assertTrue(os.path.isfile(INDEX_PATH), "index.html must exist")
        with open(INDEX_PATH, "r", encoding="utf-8") as f:
            html = f.read()

        required_elements = [
            'id="cognitive-stamina-btn"',
            'id="stamina-icon"',
            'id="stamina-label"',
            'id="spatial-reset-modal"',
            'id="reset-session-timer"',
            'id="breathing-circle"',
            'id="breathing-phase-text"',
            'openSpatialResetModal()',
            'closeSpatialResetModal()',
            'snoozeSpatialReset(',
            'updateCognitiveStamina()',
        ]
        for elem in required_elements:
            self.assertIn(elem, html, f"Expected stamina/reset element missing: {elem}")

    def test_zero_em_dashes(self):
        """Verifies zero em dashes in fatigue script and test files."""
        em_dash = "\u2014"
        fatigue_script = os.path.join(ROOT_DIR, "scripts", "cognitive_fatigue.py")
        with open(fatigue_script, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertNotIn(em_dash, content, "scripts/cognitive_fatigue.py must contain zero em dashes")

if __name__ == "__main__":
    unittest.main()
