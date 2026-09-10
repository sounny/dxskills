#!/usr/bin/env python3
"""
DxSkills Automated Vault & Database Exporter Test Suite
Verifies Obsidian YAML frontmatter, obsidian:// URI generation, Notion block payload structure,
CLI arguments, DOM landmarks, and strict zero em dash compliance.
"""

import os
import sys
import json
import unittest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from scripts.vault_exporter import format_obsidian_markdown, format_notion_payload

INDEX_PATH = os.path.join(ROOT_DIR, "index.html")

class TestVaultExporter(unittest.TestCase):

    def test_format_obsidian_markdown(self):
        """Verifies Obsidian YAML frontmatter and obsidian:// URI generation."""
        sample_doc = "# Executive Briefing\n> **BLUF:** Ship on Friday.\n\n## Actions\n- Review code\n- Deploy cluster"
        res = format_obsidian_markdown(sample_doc, title="Cloud Cutover", tags="devops, cutover", vault="WorkVault")

        self.assertEqual(res["title"], "Cloud Cutover")
        md = res["markdown"]
        self.assertTrue(md.startswith("---"), "Markdown must begin with YAML frontmatter")
        self.assertIn('title: "Cloud Cutover"', md)
        self.assertIn("type: specification", md)
        self.assertIn("status: active", md)
        self.assertIn("- dxskills", md)
        self.assertIn("- devops", md)
        self.assertIn("- cutover", md)
        self.assertIn('bluf: "**BLUF:** Ship on Friday."', md)
        self.assertIn("## Actions", md)

        # Check Obsidian URI
        uri = res["obsidian_uri"]
        self.assertTrue(uri.startswith("obsidian://new?"), "URI must start with obsidian://new?")
        self.assertIn("vault=WorkVault", uri)
        self.assertIn("name=Cloud%20Cutover", uri)

    def test_format_notion_payload(self):
        """Verifies Notion API block conversion for headings, callouts, lists, and tables."""
        sample_doc = (
            "# Strategic Alignment\n"
            "> **Decision Requested:** Authorize Phase 2 expansion.\n\n"
            "## Market Opportunity\n"
            "High growth potential in enterprise spatial intelligence.\n\n"
            "### Target Segments\n"
            "- Architecture firms\n"
            "- Urban planning teams\n\n"
            "### Implementation Milestones\n"
            "1. Pilot launch in Q1\n"
            "2. Global rollout in Q2\n\n"
            "| Metric | Target |\n"
            "| :--- | :--- |\n"
            "| ARR | $1.2M |\n"
            "| NPS | 82 |\n"
        )
        payload = format_notion_payload(sample_doc, title="Strategic Roadmap", database_id="db_12345")

        self.assertEqual(payload["parent"]["database_id"], "db_12345")
        self.assertEqual(payload["properties"]["Name"]["title"][0]["text"]["content"], "Strategic Roadmap")

        children = payload["children"]
        block_types = [b["type"] for b in children]

        self.assertIn("callout", block_types)
        self.assertIn("heading_2", block_types)
        self.assertIn("paragraph", block_types)
        self.assertIn("heading_3", block_types)
        self.assertIn("bulleted_list_item", block_types)
        self.assertIn("numbered_list_item", block_types)
        self.assertIn("table", block_types)

        callout_block = next(b for b in children if b["type"] == "callout")
        self.assertIn("Authorize Phase 2 expansion", callout_block["callout"]["rich_text"][0]["text"]["content"])

    def test_html_export_buttons_and_functions(self):
        """Verifies that index.html contains Obsidian and Notion export buttons and functions."""
        self.assertTrue(os.path.isfile(INDEX_PATH), "index.html must exist")
        with open(INDEX_PATH, "r", encoding="utf-8") as f:
            html = f.read()

        required_snippets = [
            "exportInterviewToObsidian()",
            "exportInterviewToNotion()",
            "exportPlaygroundToObsidian()",
            "exportPlaygroundToNotion()",
            "exportToObsidianVault(",
            "exportToNotionPayload(",
            "formatObsidianFrontmatter(",
            "formatNotionPagePayload(",
            "obsidian://new?name=",
        ]
        for snippet in required_snippets:
            self.assertIn(snippet, html, f"Missing required snippet in index.html: {snippet}")

    def test_zero_em_dashes(self):
        """Verifies zero em dashes in vault exporter script and this test file."""
        em_dash = "\u2014"
        files_to_check = [
            os.path.join(ROOT_DIR, "scripts", "vault_exporter.py"),
            os.path.join(ROOT_DIR, "tests", "test_vault_exporter.py"),
        ]
        for path in files_to_check:
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                self.assertNotIn(em_dash, content, f"{path} must contain zero em dashes")

if __name__ == "__main__":
    unittest.main()
