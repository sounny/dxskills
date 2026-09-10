#!/usr/bin/env python3
"""
DxSkills Automated Browser Extension Test Suite
Verifies Manifest V3 compliance, background service worker, content scripts,
popup DOM elements, and strict zero em dash compliance.
"""

import os
import sys
import json
import unittest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

EXT_DIR = os.path.join(ROOT_DIR, "extensions", "browser-dxskills")
MANIFEST_PATH = os.path.join(EXT_DIR, "manifest.json")
BACKGROUND_PATH = os.path.join(EXT_DIR, "background.js")
CONTENT_PATH = os.path.join(EXT_DIR, "content.js")
POPUP_HTML_PATH = os.path.join(EXT_DIR, "popup", "popup.html")
POPUP_JS_PATH = os.path.join(EXT_DIR, "popup", "popup.js")
INDEX_PATH = os.path.join(ROOT_DIR, "index.html")

class TestBrowserExtension(unittest.TestCase):

    def test_manifest_v3_validity(self):
        """Verifies Manifest V3 structure and required fields."""
        self.assertTrue(os.path.isfile(MANIFEST_PATH), "manifest.json must exist")
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        self.assertEqual(manifest["manifest_version"], 3)
        self.assertEqual(manifest["name"], "DxSkills - Cognitive Scaffolding")
        self.assertIn("version", manifest)
        self.assertIn("contextMenus", manifest["permissions"])
        self.assertIn("storage", manifest["permissions"])
        self.assertIn("activeTab", manifest["permissions"])

        # Service worker check
        sw_file = manifest.get("background", {}).get("service_worker")
        self.assertEqual(sw_file, "background.js")
        self.assertTrue(os.path.isfile(BACKGROUND_PATH), "background.js must exist")

        # Popup check
        popup_file = manifest.get("action", {}).get("default_popup")
        self.assertEqual(popup_file, "popup/popup.html")
        self.assertTrue(os.path.isfile(POPUP_HTML_PATH), "popup.html must exist")

    def test_background_service_worker(self):
        """Verifies context menu registration and event listener bindings."""
        with open(BACKGROUND_PATH, "r", encoding="utf-8") as f:
            code = f.read()

        self.assertIn("chrome.runtime.onInstalled.addListener", code)
        self.assertIn("chrome.contextMenus.create", code)
        self.assertIn("chrome.contextMenus.onClicked.addListener", code)
        self.assertIn("dx-scaffold-selection", code)
        self.assertIn("dx-canvas-selection", code)
        self.assertIn("dx-audio-selection", code)

    def test_content_script_hud(self):
        """Verifies floating HUD overlay and message handler."""
        with open(CONTENT_PATH, "r", encoding="utf-8") as f:
            code = f.read()

        self.assertIn("chrome.runtime.onMessage.addListener", code)
        self.assertIn("renderFloatingOverlay", code)
        self.assertIn("dxskills-hud-overlay", code)
        self.assertIn("obsidian://new", code)

    def test_popup_ui_elements(self):
        """Verifies popup markup and interactive controller."""
        with open(POPUP_HTML_PATH, "r", encoding="utf-8") as f:
            html = f.read()

        self.assertIn('id="popup-input"', html)
        self.assertIn('id="popup-output"', html)
        self.assertIn('id="compile-btn"', html)
        self.assertIn('id="audio-btn"', html)
        self.assertIn('id="copy-btn"', html)
        self.assertIn('id="obsidian-btn"', html)

        with open(POPUP_JS_PATH, "r", encoding="utf-8") as f:
            js = f.read()

        self.assertIn("compileBtn.onclick", js)
        self.assertIn("obsidianBtn.onclick", js)
        self.assertIn("audioBtn.onclick", js)

    def test_index_html_integration(self):
        """Verifies browser extension links and search index entries in index.html."""
        with open(INDEX_PATH, "r", encoding="utf-8") as f:
            html = f.read()

        self.assertIn("extensions/browser-dxskills", html)
        self.assertIn("Browser Extension (Chrome & Firefox)", html)

    def test_zero_em_dashes(self):
        """Verifies zero em dashes in extension files and test suite."""
        em_dash = "\u2014"
        for root, _, files in os.walk(EXT_DIR):
            for f in files:
                path = os.path.join(root, f)
                with open(path, "r", encoding="utf-8") as handle:
                    content = handle.read()
                self.assertNotIn(em_dash, content, f"{path} must contain zero em dashes")

        with open(os.path.join(ROOT_DIR, "tests", "test_browser_extension.py"), "r", encoding="utf-8") as handle:
            self.assertNotIn(em_dash, handle.read())

if __name__ == "__main__":
    unittest.main()
