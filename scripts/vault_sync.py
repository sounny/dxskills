"""
Multi-Vault Spatial Bi-Directional Synchronizer for DxSkills.

Scans multi-root knowledge vaults, maps cross-vault graph topologies,
detects orphaned canvas nodes and dangling wikilinks, and generates
consolidated cross-vault federation maps.

Zero em dash policy strictly enforced.
"""

import os
import sys
import json
import re
import argparse
from typing import Dict, List, Set, Any, Optional, Tuple
from collections import defaultdict


class MultiVaultScanner:
    """Scans one or more vault directories for markdown notes and canvases."""

    WIKILINK_PATTERN = re.compile(r"\[\[([^\]\|#]+)(?:#[^\]\|]+)?(?:\|[^\]]+)?\]\]")
    MD_LINK_PATTERN = re.compile(r"\[([^\]]+)\]\(([^)]+\.md)\)")

    def __init__(self, vault_paths: List[str]):
        self.vault_paths = [os.path.abspath(p) for p in vault_paths if os.path.exists(p)]
        self.notes: Dict[str, Dict[str, Any]] = {}
        self.canvases: Dict[str, Dict[str, Any]] = {}

    def scan(self) -> Dict[str, Any]:
        """Indexes all markdown and canvas files across specified vaults."""
        for vault_idx, vault_root in enumerate(self.vault_paths):
            vault_name = os.path.basename(vault_root) or f"vault_{vault_idx + 1}"
            for root, _, files in os.walk(vault_root):
                for file in files:
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, vault_root).replace("\\", "/")
                    base_stem = os.path.splitext(file)[0]

                    if file.endswith(".md"):
                        self._index_markdown_file(full_path, rel_path, base_stem, vault_name, vault_root)
                    elif file.endswith(".canvas"):
                        self._index_canvas_file(full_path, rel_path, base_stem, vault_name, vault_root)

        return {
            "vaults_count": len(self.vault_paths),
            "notes_count": len(self.notes),
            "canvases_count": len(self.canvases)
        }

    def _index_markdown_file(self, full_path: str, rel_path: str, base_stem: str, vault_name: str, vault_root: str):
        try:
            with open(full_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
        except Exception:
            return

        # Extract outgoing links
        wikilinks = set(self.WIKILINK_PATTERN.findall(content))
        md_links = set(os.path.splitext(os.path.basename(m[1]))[0] for m in self.MD_LINK_PATTERN.findall(content))
        all_targets = wikilinks.union(md_links)

        doc_id = f"{vault_name}::{base_stem}"
        self.notes[doc_id] = {
            "id": doc_id,
            "stem": base_stem,
            "filename": os.path.basename(full_path),
            "rel_path": rel_path,
            "full_path": full_path,
            "vault": vault_name,
            "vault_root": vault_root,
            "targets": list(all_targets),
            "char_count": len(content)
        }

    def _index_canvas_file(self, full_path: str, rel_path: str, base_stem: str, vault_name: str, vault_root: str):
        try:
            with open(full_path, "r", encoding="utf-8", errors="replace") as f:
                data = json.load(f)
        except Exception:
            return

        file_targets = []
        text_content_nodes = []
        for node in data.get("nodes", []):
            if node.get("type") == "file" and node.get("file"):
                target_stem = os.path.splitext(os.path.basename(node["file"]))[0]
                file_targets.append(target_stem)
            elif node.get("type") == "text" and node.get("text"):
                text_content_nodes.append(node["text"])
                # Also check text nodes for wikilinks
                wlinks = self.WIKILINK_PATTERN.findall(node["text"])
                file_targets.extend(wlinks)

        doc_id = f"{vault_name}::{base_stem}"
        self.canvases[doc_id] = {
            "id": doc_id,
            "stem": base_stem,
            "filename": os.path.basename(full_path),
            "rel_path": rel_path,
            "full_path": full_path,
            "vault": vault_name,
            "vault_root": vault_root,
            "file_targets": list(set(file_targets)),
            "nodes_count": len(data.get("nodes", [])),
            "edges_count": len(data.get("edges", []))
        }


class GraphTopologyResolver:
    """Builds global adjacency graph, finds bridges, dangling links, and orphans."""

    def __init__(self, notes: Dict[str, Dict[str, Any]], canvases: Dict[str, Dict[str, Any]]):
        self.notes = notes
        self.canvases = canvases

    def resolve(self) -> Dict[str, Any]:
        # Fast lookup mapping stem to doc_ids
        stem_to_docs = defaultdict(list)
        for doc_id, note in self.notes.items():
            stem_to_docs[note["stem"].lower()].append(doc_id)

        inbound_links = defaultdict(set)
        outbound_links = defaultdict(set)
        dangling_links = []
        cross_vault_bridges = []

        # Analyze notes
        for doc_id, note in self.notes.items():
            source_vault = note["vault"]
            for target_stem in note["targets"]:
                matched_docs = stem_to_docs.get(target_stem.lower(), [])
                if not matched_docs:
                    # Target doesn't exist anywhere
                    dangling_links.append({
                        "source_id": doc_id,
                        "source_file": note["rel_path"],
                        "vault": source_vault,
                        "missing_target": target_stem
                    })
                else:
                    for tgt_id in matched_docs:
                        outbound_links[doc_id].add(tgt_id)
                        inbound_links[tgt_id].add(doc_id)
                        tgt_vault = self.notes[tgt_id]["vault"]
                        if tgt_vault != source_vault:
                            cross_vault_bridges.append({
                                "source": doc_id,
                                "target": tgt_id,
                                "from_vault": source_vault,
                                "to_vault": tgt_vault,
                                "type": "note-to-note"
                            })

        # Analyze canvases
        for canvas_id, canvas in self.canvases.items():
            source_vault = canvas["vault"]
            for target_stem in canvas["file_targets"]:
                matched_docs = stem_to_docs.get(target_stem.lower(), [])
                if not matched_docs:
                    dangling_links.append({
                        "source_id": canvas_id,
                        "source_file": canvas["rel_path"],
                        "vault": source_vault,
                        "missing_target": target_stem
                    })
                else:
                    for tgt_id in matched_docs:
                        outbound_links[canvas_id].add(tgt_id)
                        inbound_links[tgt_id].add(canvas_id)
                        tgt_vault = self.notes[tgt_id]["vault"]
                        if tgt_vault != source_vault:
                            cross_vault_bridges.append({
                                "source": canvas_id,
                                "target": tgt_id,
                                "from_vault": source_vault,
                                "to_vault": tgt_vault,
                                "type": "canvas-to-note"
                            })

        # Find orphaned notes (0 outbound and 0 inbound links)
        orphans = []
        for doc_id, note in self.notes.items():
            if len(outbound_links[doc_id]) == 0 and len(inbound_links[doc_id]) == 0:
                orphans.append({
                    "id": doc_id,
                    "stem": note["stem"],
                    "vault": note["vault"],
                    "rel_path": note["rel_path"]
                })

        # Calculate network density and health score
        total_entities = len(self.notes) + len(self.canvases)
        total_connections = sum(len(tgts) for tgts in outbound_links.values())
        health_score = 100
        if total_entities > 0:
            orphan_penalty = (len(orphans) / total_entities) * 40
            dangling_penalty = min(50, len(dangling_links) * 5)
            health_score = max(0, round(100 - orphan_penalty - dangling_penalty))

        return {
            "total_entities": total_entities,
            "total_connections": total_connections,
            "health_score": health_score,
            "orphans_count": len(orphans),
            "orphans": orphans,
            "dangling_count": len(dangling_links),
            "dangling_links": dangling_links,
            "cross_vault_bridges_count": len(cross_vault_bridges),
            "cross_vault_bridges": cross_vault_bridges
        }


class FederationCanvasBuilder:
    """Renders multi-vault topology into a structured Obsidian .canvas file."""

    VAULT_COLORS = {
        0: "1",  # Red
        1: "2",  # Orange
        2: "4",  # Green
        3: "5",  # Blue
        4: "6",  # Purple
    }

    @classmethod
    def build_canvas(
        cls,
        notes: Dict[str, Dict[str, Any]],
        canvases: Dict[str, Dict[str, Any]],
        topology: Dict[str, Any]
    ) -> Dict[str, Any]:
        nodes = []
        edges = []

        vault_groups = defaultdict(list)
        for doc_id, note in notes.items():
            vault_groups[note["vault"]].append(note)

        x_offset = 0
        vault_color_map = {}
        for idx, (vault_name, vnotes) in enumerate(vault_groups.items()):
            color_code = cls.VAULT_COLORS.get(idx % len(cls.VAULT_COLORS), "3")
            vault_color_map[vault_name] = color_code

            # Group header node
            group_id = f"group-vault-{vault_name}"
            nodes.append({
                "id": group_id,
                "type": "text",
                "text": f"## Vault: {vault_name}\nNotes indexed: **{len(vnotes)}**",
                "x": x_offset,
                "y": 0,
                "width": 360,
                "height": 120,
                "color": color_code
            })

            y_offset = 180
            for note in vnotes[:12]:  # Display top 12 per vault in canvas
                nid = f"node-{note['id'].replace('::', '-')}"
                nodes.append({
                    "id": nid,
                    "type": "text",
                    "text": f"### {note['stem']}\nPath: `{note['rel_path']}`",
                    "x": x_offset,
                    "y": y_offset,
                    "width": 340,
                    "height": 100,
                    "color": color_code
                })
                # Edge from group header
                edges.append({
                    "id": f"edge-header-{nid}",
                    "fromNode": group_id,
                    "fromSide": "bottom",
                    "toNode": nid,
                    "toSide": "top"
                })
                y_offset += 140

            x_offset += 440

        # Cross-vault bridge edges
        for idx, bridge in enumerate(topology.get("cross_vault_bridges", [])[:30]):
            src_nid = f"node-{bridge['source'].replace('::', '-')}"
            tgt_nid = f"node-{bridge['target'].replace('::', '-')}"
            edges.append({
                "id": f"edge-bridge-{idx}",
                "fromNode": src_nid,
                "fromSide": "right",
                "toNode": tgt_nid,
                "toSide": "left",
                "label": "cross-vault bridge",
                "color": "6"
            })

        return {"nodes": nodes, "edges": edges}


def run_vault_sync(
    vault_paths: List[str],
    output_canvas: Optional[str] = None
) -> Tuple[Dict[str, Any], str]:
    """Orchestrates multi-vault indexing, topology analysis, and reporting."""
    scanner = MultiVaultScanner(vault_paths)
    scan_meta = scanner.scan()

    resolver = GraphTopologyResolver(scanner.notes, scanner.canvases)
    topology = resolver.resolve()

    report_lines = []
    report_lines.append("# Multi-Vault Spatial Bi-Directional Topology Report")
    report_lines.append("")
    report_lines.append(f"> **Vault Health Score:** `{topology['health_score']}/100` | **Vaults Indexed:** `{scan_meta['vaults_count']}`")
    report_lines.append(f"> **Total Notes:** `{scan_meta['notes_count']}` | **Canvases:** `{scan_meta['canvases_count']}` | **Cross-Vault Bridges:** `{topology['cross_vault_bridges_count']}`")
    report_lines.append("")
    report_lines.append("## Topology Overview")
    report_lines.append(f"- **Active Connections:** {topology['total_connections']}")
    report_lines.append(f"- **Orphaned Notes:** {topology['orphans_count']}")
    report_lines.append(f"- **Dangling/Missing References:** {topology['dangling_count']}")
    report_lines.append("")

    if topology["cross_vault_bridges"]:
        report_lines.append("## Cross-Vault Bridge Conduits")
        report_lines.append("| Source Note/Canvas | Target Note | Origin Vault | Destination Vault |")
        report_lines.append("|:-------------------|:------------|:-------------|:------------------|")
        for b in topology["cross_vault_bridges"][:15]:
            report_lines.append(f"| `{b['source']}` | `{b['target']}` | {b['from_vault']} | {b['to_vault']} |")
        report_lines.append("")

    if topology["dangling_links"]:
        report_lines.append("## Dangling / Missing Targets")
        report_lines.append("| Referencing Note | Vault | Missing Target |")
        report_lines.append("|:-----------------|:------|:---------------|")
        for d in topology["dangling_links"][:15]:
            report_lines.append(f"| `{d['source_file']}` | {d['vault']} | `[[{d['missing_target']}]]` |")
        report_lines.append("")

    if topology["orphans"]:
        report_lines.append("## Isolated / Orphaned Notes")
        for o in topology["orphans"][:10]:
            report_lines.append(f"- `{o['vault']}/{o['rel_path']}`")
        report_lines.append("")

    report_text = "\n".join(report_lines)

    if output_canvas:
        canvas_data = FederationCanvasBuilder.build_canvas(scanner.notes, scanner.canvases, topology)
        os.makedirs(os.path.dirname(os.path.abspath(output_canvas)), exist_ok=True)
        with open(output_canvas, "w", encoding="utf-8") as f:
            json.dump(canvas_data, f, indent=2)

    return topology, report_text


def main():
    parser = argparse.ArgumentParser(description="DxSkills Multi-Vault Spatial Bi-Directional Synchronizer")
    parser.add_argument("vaults", nargs="*", help="Paths to vault root directories")
    parser.add_argument("--canvas", "-c", help="Output filepath for consolidated federation .canvas")
    parser.add_argument("--json", "-j", action="store_true", help="Output raw JSON topology telemetry")

    args = parser.parse_args()
    vault_paths = args.vaults if args.vaults else [os.getcwd()]

    topology, report = run_vault_sync(vault_paths, output_canvas=args.canvas)

    if args.json:
        print(json.dumps(topology, indent=2))
    else:
        print(report)

    if args.canvas:
        print(f"[DxSkills] Consolidated federation canvas written to: {args.canvas}")


if __name__ == "__main__":
    main()
