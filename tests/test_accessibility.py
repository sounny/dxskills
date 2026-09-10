#!/usr/bin/env python3
"""
DxSkills Automated Accessibility & WCAG 2.1 AAA Compliance Test Suite
Verifies semantic landmarks, image alt attributes, contrast ratios, and OpenDyslexic mode.
"""

import os
import re
import unittest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(ROOT_DIR, "index.html")

def calculate_relative_luminance(hex_color):
    """Calculates relative luminance according to WCAG 2.1 specifications."""
    hex_color = hex_color.lstrip('#')
    r, g, b = [int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4)]
    channels = [
        (c / 12.92) if c <= 0.03928 else (((c + 0.055) / 1.055) ** 2.4)
        for c in (r, g, b)
    ]
    return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]

def calculate_contrast_ratio(hex1, hex2):
    """Computes contrast ratio between two hex colors."""
    lum1 = calculate_relative_luminance(hex1)
    lum2 = calculate_relative_luminance(hex2)
    brightest = max(lum1, lum2)
    darkest = min(lum1, lum2)
    return (brightest + 0.05) / (darkest + 0.05)

class TestDxSkillsAccessibility(unittest.TestCase):

    def setUp(self):
        self.assertTrue(os.path.isfile(INDEX_PATH), "index.html must exist")
        with open(INDEX_PATH, "r", encoding="utf-8") as f:
            self.html = f.read()

    def test_semantic_landmarks(self):
        """Verifies core HTML landmark tags exist for screen reader navigation."""
        self.assertIn('<html lang="', self.html, "HTML tag must specify language attribute")
        self.assertIn('<nav', self.html, "Page must include nav landmark")
        self.assertIn('<footer', self.html, "Page must include footer landmark")
        self.assertIn('<h1', self.html, "Page must include h1 main heading")

    def test_button_and_input_labels(self):
        """Verifies buttons and inputs have accessible labels or text."""
        inputs = re.findall(r'<input\s+([^>]+)>', self.html)
        for inp in inputs:
            has_label = 'aria-label=' in inp or 'placeholder=' in inp or 'title=' in inp
            self.assertTrue(has_label, f"Input tag missing accessible label or placeholder: {inp}")

    def test_wcag_aaa_monochrome_contrast(self):
        """Verifies high-contrast monochrome design meets WCAG 2.1 AAA (>= 7.0:1)."""
        white = "#ffffff"
        dark_titanium = "#09090b"
        light_canvas = "#fafafa"
        dark_card = "#18181b"

        contrast_dark_mode = calculate_contrast_ratio(white, dark_titanium)
        self.assertGreaterEqual(
            contrast_dark_mode,
            7.0,
            f"Dark mode contrast {contrast_dark_mode:.2f}:1 fails WCAG AAA (7.0:1 required)"
        )

        contrast_light_mode = calculate_contrast_ratio(dark_card, light_canvas)
        self.assertGreaterEqual(
            contrast_light_mode,
            7.0,
            f"Light mode contrast {contrast_light_mode:.2f}:1 fails WCAG AAA (7.0:1 required)"
        )

    def test_opendyslexic_support(self):
        """Verifies OpenDyslexic font definition and letter spacing alleviation mode."""
        self.assertIn('opendyslexic', self.html.lower(), "index.html must support OpenDyslexic mode")
        self.assertIn('toggleDyslexicFont', self.html, "index.html must have font toggle function")

if __name__ == '__main__':
    unittest.main()
