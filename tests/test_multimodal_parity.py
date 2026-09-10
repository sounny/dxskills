#!/usr/bin/env python3
"""
Unit Tests for DxSkills Multi-Modal Parity Suite & Export Telemetry
Verifies cross-modal synchronization between Markdown, Audio Digest,
Obsidian Canvas (.canvas), and Notion Block Exports.

Strict Rule: NO em dashes anywhere (use hyphens, commas, or parentheses).
"""

import os
import sys
import unittest
import json

# Ensure repository root is in sys.path
REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_DIR not in sys.path:
    sys.path.insert(0, REPO_DIR)

import scripts.multimodal_parity as mp

class TestMultiModalParity(unittest.TestCase):

    def setUp(self):
        self.sample_markdown = """# Distributed Architecture Platform
> **BLUF:** High-throughput microservice architecture eliminating database locking bottlenecks.

## System Topology
- Decoupled worker queues with pub-sub event fabric.
- Read-replicas deployed across 3 edge locations.

## Production Milestones
- [ ] 1. Provision Terraform staging environment.
- [ ] 2. Run load tests at 50,000 requests per second.
- [ ] 3. Deploy canary cluster to primary production region.
"""

    def test_extract_canonical_landmarks(self):
        landmarks = mp.extract_canonical_landmarks(self.sample_markdown)
        self.assertEqual(landmarks["title"], "Distributed Architecture Platform")
        self.assertIn("High-throughput microservice", landmarks["bluf"])
        self.assertIn("System Topology", landmarks["pillars"])
        self.assertIn("Production Milestones", landmarks["pillars"])
        self.assertTrue(any("Terraform" in a for a in landmarks["actions"]))

    def test_validate_multimodal_parity_pass(self):
        res = mp.validate_multimodal_parity(self.sample_markdown)
        self.assertEqual(res["status"], "PASS")
        self.assertGreaterEqual(res["parity_score"], 85.0)
        self.assertGreaterEqual(res["checks_passed"], 14)
        self.assertTrue(res["modalities"]["markdown"]["status"] == "OK")
        self.assertTrue(res["modalities"]["audio_digest"]["status"] == "OK")
        self.assertTrue(res["modalities"]["obsidian_canvas"]["status"] == "OK")
        self.assertTrue(res["modalities"]["svg_canvas"]["status"] == "OK")
        self.assertTrue(res["modalities"]["obsidian_vault"]["status"] == "OK")
        self.assertTrue(res["modalities"]["notion_payload"]["status"] == "OK")

    def test_multilingual_parity_french(self):
        fr_markdown = """# Plateforme d'Architecture Distribuee
> **BLUF:** Architecture de microservices a haut debit eliminant les verrous de base de donnees.

## Topologie du Systeme
- Files de travail decouplees avec tissu d'evenements.
- Replicas en lecture sur trois sites peripheriques.

## Jalons de Production
- [ ] 1. Deploiement de l'environnement de preproduction Terraform.
- [ ] 2. Tests de charge a 50000 requetes par seconde.
"""
        res = mp.validate_multimodal_parity(fr_markdown, lang="fr")
        self.assertEqual(res["status"], "PASS")
        self.assertGreaterEqual(res["parity_score"], 80.0)

    def test_pipeline_telemetry_check(self):
        telemetry = mp.run_pipeline_telemetry_check(self.sample_markdown)
        self.assertGreaterEqual(telemetry["parity_score"], 85.0)
        self.assertTrue(telemetry["canvas_json_valid"])
        self.assertTrue(telemetry["notion_blocks_valid"])
        self.assertTrue(telemetry["zero_em_dash_clean"])
        self.assertGreaterEqual(telemetry["modalities_verified"], 6)

    def test_zero_em_dash_enforcement_in_parity(self):
        # Inject an em dash dynamically to verify parity audit catches it
        bad_markdown = f"# Test {chr(8212)} Dynamic Dash\n> **BLUF:** Testing dash.\n\n## Section\n- Item"
        res = mp.validate_multimodal_parity(bad_markdown)
        failed_dashes = [d for d in res["diagnostics"] if "Em dash detected in Markdown" in d]
        self.assertTrue(len(failed_dashes) > 0)

    def test_format_terminal_parity_report(self):
        res = mp.validate_multimodal_parity(self.sample_markdown)
        report = mp.format_terminal_parity_report(res)
        self.assertIn("DxSkills Multi-Modal Parity & Telemetry Audit", report)
        self.assertIn("Modality Coverage Matrix:", report)
        self.assertIn("obsidian_canvas", report)
        self.assertNotIn(chr(8212), report)

if __name__ == "__main__":
    unittest.main()
