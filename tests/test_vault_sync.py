"""
Tests for Multi-Vault Spatial Bi-Directional Synchronizer.
Strict zero em dash compliance verified across all test assertions.
"""

import os
import sys
import json
import unittest
import tempfile
import subprocess

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))
from vault_sync import (
    MultiVaultScanner,
    GraphTopologyResolver,
    FederationCanvasBuilder,
    run_vault_sync,
)


class TestVaultSync(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = self.temp_dir.name

        # Create two simulated vaults: Vault A (Research) and Vault B (Studio)
        self.vault_a = os.path.join(self.root, "Vault_Research")
        self.vault_b = os.path.join(self.root, "Vault_Studio")
        os.makedirs(self.vault_a, exist_ok=True)
        os.makedirs(self.vault_b, exist_ok=True)

        # In Vault A:
        # Note1: links to Note2 (same vault) and Note3 (Vault B)
        with open(os.path.join(self.vault_a, "Note1.md"), "w", encoding="utf-8") as f:
            f.write("# Research Foundations\nLinks to [[Note2]] and cross-vault [[Note3]]. Also broken link [[MissingNote]].")

        # Note2: links back to Note1
        with open(os.path.join(self.vault_a, "Note2.md"), "w", encoding="utf-8") as f:
            f.write("# Methodology\nReferencing [[Note1]].")

        # Orphan Note A: zero links
        with open(os.path.join(self.vault_a, "IsolatedIdea.md"), "w", encoding="utf-8") as f:
            f.write("# Isolated Fragment\nNo links here.")

        # In Vault B:
        # Note3: links to Note4
        with open(os.path.join(self.vault_b, "Note3.md"), "w", encoding="utf-8") as f:
            f.write("# Studio Strategy\nConnecting to [Design Plan](Note4.md).")

        # Note4: links to Note1 (cross-vault back)
        with open(os.path.join(self.vault_b, "Note4.md"), "w", encoding="utf-8") as f:
            f.write("# Design Plan\nGrounding in [[Note1]].")

        # Canvas in Vault B referencing Note3
        canvas_data = {
            "nodes": [
                {"id": "c1", "type": "file", "file": "Note3.md", "x": 0, "y": 0, "width": 200, "height": 100},
                {"id": "c2", "type": "text", "text": "See [[Note2]] for methodology", "x": 300, "y": 0, "width": 200, "height": 100}
            ],
            "edges": []
        }
        with open(os.path.join(self.vault_b, "StrategyMap.canvas"), "w", encoding="utf-8") as f:
            json.dump(canvas_data, f)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_multi_vault_scanner_indexing(self):
        scanner = MultiVaultScanner([self.vault_a, self.vault_b])
        meta = scanner.scan()

        self.assertEqual(meta["vaults_count"], 2)
        self.assertEqual(meta["notes_count"], 5)  # Note1, Note2, IsolatedIdea, Note3, Note4
        self.assertEqual(meta["canvases_count"], 1)

        # Check Note1 targets
        n1_key = [k for k in scanner.notes if "Note1" in k][0]
        targets = scanner.notes[n1_key]["targets"]
        self.assertIn("Note2", targets)
        self.assertIn("Note3", targets)
        self.assertIn("MissingNote", targets)

    def test_topology_resolver_detects_bridges_and_orphans(self):
        scanner = MultiVaultScanner([self.vault_a, self.vault_b])
        scanner.scan()

        resolver = GraphTopologyResolver(scanner.notes, scanner.canvases)
        topology = resolver.resolve()

        self.assertGreater(topology["total_connections"], 0)
        self.assertTrue(0 <= topology["health_score"] <= 100)

        # Orphan detection: IsolatedIdea
        orphan_stems = [o["stem"] for o in topology["orphans"]]
        self.assertIn("IsolatedIdea", orphan_stems)

        # Dangling detection: MissingNote
        missing = [d["missing_target"] for d in topology["dangling_links"]]
        self.assertIn("MissingNote", missing)

        # Cross-vault bridge detection
        self.assertGreaterEqual(topology["cross_vault_bridges_count"], 2)

    def test_federation_canvas_builder(self):
        scanner = MultiVaultScanner([self.vault_a, self.vault_b])
        scanner.scan()
        resolver = GraphTopologyResolver(scanner.notes, scanner.canvases)
        topology = resolver.resolve()

        canvas = FederationCanvasBuilder.build_canvas(scanner.notes, scanner.canvases, topology)
        self.assertIn("nodes", canvas)
        self.assertIn("edges", canvas)

        # Check group header nodes exist for both vaults
        group_nodes = [n for n in canvas["nodes"] if n["id"].startswith("group-vault-")]
        self.assertEqual(len(group_nodes), 2)

        # Check bridge edges exist
        bridge_edges = [e for e in canvas["edges"] if "edge-bridge" in e["id"]]
        self.assertGreater(len(bridge_edges), 0)

    def test_run_vault_sync_and_file_export(self):
        out_canvas = os.path.join(self.root, "federation.canvas")
        topology, report = run_vault_sync([self.vault_a, self.vault_b], output_canvas=out_canvas)

        self.assertTrue(os.path.isfile(out_canvas))
        with open(out_canvas, "r", encoding="utf-8") as f:
            c_data = json.load(f)
        self.assertIn("nodes", c_data)

        # Verify report contains key metrics and zero em dashes
        self.assertIn("Multi-Vault Spatial Bi-Directional Topology Report", report)
        self.assertIn("Vault Health Score", report)
        self.assertIn("Cross-Vault Bridge Conduits", report)
        self.assertNotIn(chr(8212), report)

    def test_cli_sync_command(self):
        cli_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts", "dx_cli.py"))
        res = subprocess.run(
            [sys.executable, cli_path, "sync", self.vault_a, self.vault_b],
            capture_output=True,
            text=True,
            check=True
        )
        self.assertEqual(res.returncode, 0)
        self.assertIn("Multi-Vault Spatial Bi-Directional Topology Report", res.stdout)
        self.assertNotIn(chr(8212), res.stdout)

    def test_zero_em_dash_in_source(self):
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts", "vault_sync.py"))
        if os.path.exists(script_path):
            with open(script_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertNotIn(chr(8212), content, "Found em dash in scripts/vault_sync.py")


if __name__ == "__main__":
    unittest.main()
