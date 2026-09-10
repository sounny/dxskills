"""
Autonomous Spatial Cognitive Model Fine-Tuning Dataset Synthesizer for DxSkills.

Compiles instruction-tuning datasets (Alpaca, ShareGPT, OpenAI JSONL) that train
foundation models to transform dense linear text walls into 2D Obsidian Canvas topologies.
Includes validation harness verifying spatial bounding box collisions and graph connectivity.

Zero em dash policy strictly enforced.
"""

import os
import sys
import json
import re
import math
import argparse
from typing import Dict, List, Any, Optional, Tuple


class DatasetSynthesizer:
    """Generates instruction-tuning pairs for spatial graph conversion."""

    SYSTEM_PROMPT = (
        "You are DxSkills Spatial Architect. Your mission is to eliminate phonological "
        "working memory friction by deconstructing linear text into an interactive 2D "
        "Obsidian Canvas graph topology with clear visual hierarchy, color coding, and associative edges."
    )

    @classmethod
    def create_pair(
        cls,
        text: str,
        title: Optional[str] = None,
        fmt: str = "alpaca"
    ) -> Dict[str, Any]:
        """Creates a single instruction-tuning sample from linear prose."""
        clean_text = text.strip()
        doc_title = title or "Architectural Spatial Synthesis"

        # Synthesize target canvas from input text
        canvas_target = cls._synthesize_canvas(clean_text, title=doc_title)
        canvas_json_str = json.dumps(canvas_target, indent=2)

        instruction = (
            f"Transform the following linear technical prose into a structured 2D Obsidian Canvas "
            f"graph topology. Assign spatial coordinates, semantic colors, and relational edge bridges:\n\n{clean_text}"
        )

        if fmt == "sharegpt":
            return {
                "conversations": [
                    {"from": "system", "value": cls.SYSTEM_PROMPT},
                    {"from": "human", "value": instruction},
                    {"from": "gpt", "value": canvas_json_str}
                ]
            }
        elif fmt == "openai":
            return {
                "messages": [
                    {"role": "system", "content": cls.SYSTEM_PROMPT},
                    {"role": "user", "content": instruction},
                    {"role": "assistant", "content": canvas_json_str}
                ]
            }
        else:
            # Alpaca format
            return {
                "instruction": "Deconstruct linear text into a 2D Obsidian Canvas spatial architecture.",
                "input": clean_text,
                "output": canvas_json_str,
                "system": cls.SYSTEM_PROMPT
            }

    @classmethod
    def _synthesize_canvas(cls, text: str, title: str) -> Dict[str, Any]:
        """Extracts bullet points, sentences, and sections into 2D canvas nodes."""
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        
        extracted_concepts = []
        for line in lines:
            if line.startswith(("#", ">")):
                continue
            if line.startswith(("-", "*")) or re.match(r"^\d+\.\s+", line):
                clean = re.sub(r"^[-*+\d.]+\s*", "", line).strip()
                if len(clean) > 8:
                    extracted_concepts.append(clean)
            else:
                sentences = re.split(r"(?<=[.!?])\s+", line)
                for s in sentences:
                    clean = s.strip()
                    if len(clean) > 15:
                        extracted_concepts.append(clean)

        if not extracted_concepts:
            extracted_concepts = [
                "Deconstruct linear paragraph walls into spatial visual clusters.",
                "Assign 2D coordinates with non-overlapping bounding margins.",
                "Form bidirectional relationship edges with semantic progression labels."
            ]

        nodes = []
        edges = []

        # Central Root Hub
        root_id = "node-canvas-hub"
        nodes.append({
            "id": root_id,
            "type": "text",
            "text": f"## {title}\nSpatial Architecture Graph\nNodes: **{len(extracted_concepts)}**",
            "x": 0,
            "y": -220,
            "width": 380,
            "height": 130,
            "color": "5"
        })

        # Orbiting Satellite Nodes arranged in radial or tiered layout
        radius = 420
        total = len(extracted_concepts)
        colors = ["1", "4", "5", "3", "2"]

        for idx, concept in enumerate(extracted_concepts, 1):
            nid = f"concept-node-{idx}"
            angle = (2 * math.pi / total) * (idx - 1)
            nx = round(radius * math.cos(angle))
            ny = round(radius * math.sin(angle)) + 80

            color = colors[(idx - 1) % len(colors)]
            snippet = concept[:36] + ("..." if len(concept) > 36 else "")

            nodes.append({
                "id": nid,
                "type": "text",
                "text": f"### Anchor {idx}\n**{snippet}**\n\n> {concept}",
                "x": nx,
                "y": ny,
                "width": 300,
                "height": 160,
                "color": color
            })

            edges.append({
                "id": f"edge-hub-{idx}",
                "fromNode": root_id,
                "fromSide": "bottom" if ny > -100 else "top",
                "toNode": nid,
                "toSide": "top" if ny > -100 else "bottom",
                "label": f"Vector {idx}"
            })

        return {"nodes": nodes, "edges": edges}


class DatasetValidator:
    """Validates spatial canvas training pairs for topological integrity and geometry."""

    @classmethod
    def validate_pair(cls, pair: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluates bounding collision, connectivity, and schema validity."""
        canvas_str = ""
        if "output" in pair:
            canvas_str = pair["output"]
        elif "messages" in pair:
            canvas_str = pair["messages"][-1]["content"]
        elif "conversations" in pair:
            canvas_str = pair["conversations"][-1]["value"]
        else:
            return {"valid": False, "error": "Unrecognized dataset format"}

        try:
            canvas_data = json.loads(canvas_str)
        except Exception as e:
            return {"valid": False, "error": f"Invalid JSON syntax in output: {str(e)}"}

        nodes = canvas_data.get("nodes", [])
        edges = canvas_data.get("edges", [])

        if not nodes:
            return {"valid": False, "error": "Canvas contains zero nodes"}

        node_ids = {n["id"] for n in nodes if "id" in n}
        if len(node_ids) != len(nodes):
            return {"valid": False, "error": "Duplicate node IDs detected"}

        # Edge validity
        dangling_edges = []
        for e in edges:
            fn = e.get("fromNode")
            tn = e.get("toNode")
            if fn not in node_ids or tn not in node_ids:
                dangling_edges.append(e.get("id", "unknown"))

        if dangling_edges:
            return {
                "valid": False,
                "error": f"Dangling edges detected connecting non-existent nodes: {dangling_edges}"
            }

        # Spatial Collision Check (Bounding Box Overlap)
        collision_count = 0
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                n1 = nodes[i]
                n2 = nodes[j]
                x1, y1 = n1.get("x", 0), n1.get("y", 0)
                w1, h1 = n1.get("width", 250), n1.get("height", 140)
                x2, y2 = n2.get("x", 0), n2.get("y", 0)
                w2, h2 = n2.get("width", 250), n2.get("height", 140)

                # Check bounding box overlap
                if not (x1 + w1 <= x2 or x2 + w2 <= x1 or y1 + h1 <= y2 or y2 + h2 <= y1):
                    collision_count += 1

        # Zero em dash verification
        pair_str = json.dumps(pair)
        has_em_dash = chr(8212) in pair_str

        score = 100.0
        if collision_count > 0:
            score -= min(40.0, collision_count * 15.0)
        if has_em_dash:
            score -= 50.0

        return {
            "valid": len(dangling_edges) == 0 and not has_em_dash,
            "nodes_count": len(nodes),
            "edges_count": len(edges),
            "collision_count": collision_count,
            "has_em_dash": has_em_dash,
            "quality_score": max(0.0, score)
        }


def compile_dataset(
    corpus_entries: List[Tuple[str, str]],
    output_filepath: Optional[str] = None,
    fmt: str = "alpaca"
) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """Compiles a list of (title, text) pairs into a verified dataset JSONL."""
    dataset = []
    total_score = 0.0
    valid_count = 0

    for title, text in corpus_entries:
        pair = DatasetSynthesizer.create_pair(text, title=title, fmt=fmt)
        val = DatasetValidator.validate_pair(pair)
        if val["valid"]:
            valid_count += 1
        total_score += val["quality_score"]
        dataset.append(pair)

    avg_score = round(total_score / max(1, len(dataset)), 1)
    meta = {
        "total_pairs": len(dataset),
        "valid_pairs": valid_count,
        "format": fmt,
        "average_quality_score": avg_score
    }

    if output_filepath:
        os.makedirs(os.path.dirname(os.path.abspath(output_filepath)), exist_ok=True)
        with open(output_filepath, "w", encoding="utf-8") as f:
            for item in dataset:
                f.write(json.dumps(item) + "\n")

    return dataset, meta


def main():
    parser = argparse.ArgumentParser(description="DxSkills Spatial Cognitive Model Dataset Synthesizer")
    parser.add_argument("input", nargs="?", help="Input text note, markdown file, or directory")
    parser.add_argument("--format", "-f", choices=["alpaca", "sharegpt", "openai"], default="alpaca", help="Dataset format")
    parser.add_argument("--output", "-o", help="Output JSONL filepath")
    parser.add_argument("--title", "-t", help="Document title for single input")
    parser.add_argument("--validate", "-v", action="store_true", help="Validate and report dataset quality score")
    parser.add_argument("--json", "-j", action="store_true", help="Output raw JSON preview")

    args = parser.parse_args()

    corpus = []
    if args.input:
        if os.path.isdir(args.input):
            for root, _, files in os.walk(args.input):
                for file in files:
                    if file.endswith((".md", ".txt")):
                        p = os.path.join(root, file)
                        with open(p, "r", encoding="utf-8", errors="ignore") as f:
                            corpus.append((os.path.splitext(file)[0], f.read()))
        elif os.path.isfile(args.input):
            with open(args.input, "r", encoding="utf-8", errors="ignore") as f:
                corpus.append((args.title or os.path.basename(args.input), f.read()))
        else:
            corpus.append((args.title or "Interactive CLI Sample", args.input))
    else:
        if not sys.stdin.isatty():
            corpus.append((args.title or "Standard Ingest", sys.stdin.read()))
        else:
            corpus.append((
                "Core Spatial Scaffolding",
                "# Cognitive Spatial Architecture\n"
                "> **BLUF:** Decouple phonological memory from spatial reasoning models.\n\n"
                "- Spatial Vector 1: 2D radial coordinate positioning.\n"
                "- Spatial Vector 2: Multi-vault topology federation without orphan links.\n"
                "- Spatial Vector 3: Working memory dual-channel stamina balance."
            ))

    dataset, meta = compile_dataset(corpus, output_filepath=args.output, fmt=args.format)

    if args.json:
        print(json.dumps({"meta": meta, "sample": dataset[0] if dataset else None}, indent=2))
    elif not args.output:
        print(f"\n=== [DxSkills: Spatial Model Dataset Synthesizer] ===")
        print(f"Compiled {meta['total_pairs']} pairs ({meta['valid_pairs']} valid) in `{meta['format']}` format.")
        print(f"Average Quality Score: {meta['average_quality_score']}/100")
        if dataset:
            print(f"\n--- Preview Sample (Prompt Snippet) ---")
            sample = dataset[0]
            if "instruction" in sample:
                print(f"Instruction: {sample['instruction']}")
                print(f"Input: {sample['input'][:100]}...")
            elif "conversations" in sample:
                print(f"Human: {sample['conversations'][1]['value'][:100]}...")
    else:
        print(f"[DxSkills] Compiled {meta['total_pairs']} fine-tuning pairs to: {args.output}")
        print(f"  - Format: {meta['format']}")
        print(f"  - Quality Score: {meta['average_quality_score']}/100")


if __name__ == "__main__":
    main()
