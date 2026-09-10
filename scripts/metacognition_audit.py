"""
Autonomous Cognitive Metacognition and Synthesis Audit Suite for DxSkills.

Evaluates intellectual clarity, phonological friction, and spatial leverage
in architectural proposals, research papers, and strategic notes.
Generates Obsidian .canvas metacognitive scorecards and vector SVG audit dashboards.

Zero em dash policy strictly enforced.
"""

import os
import sys
import json
import re
import math
import argparse
from typing import Dict, List, Any, Optional, Tuple


class MetacognitionAuditor:
    """Evaluates text across phonological, spatial, and cognitive load dimensions."""

    JARGON_PATTERNS = [
        r"\butilize\b", r"\bleverage\b", r"\bsynergy\b", r"\bparadigm\b",
        r"\bheretofore\b", r"\bnotwithstanding\b", r"\bmultifaceted\b",
        r"\bdisruptive\b", r"\bholistic\b", r"\boperationalize\b"
    ]

    @classmethod
    def audit_text(cls, text: str, title: Optional[str] = None) -> Dict[str, Any]:
        """Calculates cognitive metrics and returns a structured audit assessment."""
        clean_text = text.strip()
        doc_title = title or "Strategic Deliverable Audit"

        words = re.findall(r"\b[A-Za-z0-9_-]+\b", clean_text)
        word_count = len(words)
        if word_count == 0:
            return cls._empty_audit(doc_title)

        sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", clean_text) if s.strip()]
        sentence_count = max(1, len(sentences))

        paragraphs = [p.strip() for p in clean_text.split("\n\n") if p.strip()]
        paragraph_count = max(1, len(paragraphs))

        # 1. Phonological Friction Score (0-100, lower is better)
        avg_words_per_sentence = word_count / sentence_count
        long_sentences = sum(1 for s in sentences if len(s.split()) > 24)
        long_sentence_ratio = long_sentences / sentence_count

        jargon_matches = 0
        for pattern in cls.JARGON_PATTERNS:
            jargon_matches += len(re.findall(pattern, clean_text, re.IGNORECASE))
        jargon_density = (jargon_matches / max(1, word_count)) * 100

        # Syllable approximation (count vowel groups)
        vowel_groups = len(re.findall(r"[aeiouyAEIOUY]+", clean_text))
        avg_syllables_per_word = max(1.0, vowel_groups / max(1, word_count))

        phonological_friction = min(100.0, max(0.0, (
            (avg_words_per_sentence * 2.2) +
            (long_sentence_ratio * 40.0) +
            (jargon_density * 8.0) +
            (max(0.0, avg_syllables_per_word - 1.3) * 35.0)
        )))

        # 2. Spatial Leverage Ratio (0-100, higher is better)
        bullet_points = len(re.findall(r"^\s*[-*+]\s+", clean_text, re.MULTILINE))
        numbered_lists = len(re.findall(r"^\s*\d+\.\s+", clean_text, re.MULTILINE))
        headers = len(re.findall(r"^#{1,6}\s+", clean_text, re.MULTILINE))
        table_rows = len(re.findall(r"^\|.+?\|", clean_text, re.MULTILINE))
        code_blocks = len(re.findall(r"```", clean_text)) // 2
        wikilinks = len(re.findall(r"\[\[.+?\]\]", clean_text))

        spatial_anchors = bullet_points + numbered_lists + headers + table_rows + code_blocks + wikilinks
        spatial_leverage = min(100.0, max(0.0, (spatial_anchors / max(1, sentence_count)) * 75.0))

        # 3. Non-Linear Connectivity Score (0-100)
        connectivity_score = min(100.0, max(10.0, (wikilinks * 12.0) + (headers * 6.0) + (table_rows * 4.0)))

        # 4. Cognitive Working Memory Stamina Tax (0-100, lower is better)
        # Baddeley & Sweller model: high phonological friction + low spatial leverage = high working memory tax
        stamina_tax = min(100.0, max(5.0, (phonological_friction * 0.65) + ((100.0 - spatial_leverage) * 0.35)))

        # 5. Composite Cognitive Leverage Score (0-100, higher is better)
        cognitive_leverage_score = round(max(0.0, min(100.0, (
            (100.0 - phonological_friction) * 0.35 +
            spatial_leverage * 0.40 +
            connectivity_score * 0.25
        ))), 1)

        # Refactoring Recommendations
        recommendations = []
        if phonological_friction > 50.0:
            recommendations.append("Reduce average sentence length to under 18 words to minimize phonological loop fatigue.")
        if long_sentence_ratio > 0.25:
            recommendations.append(f"Decompose {long_sentences} run-on sentences into high-contrast bulleted anchors.")
        if spatial_leverage < 40.0:
            recommendations.append("Introduce spatial anchors: structured tables, callout blocks, or headers every 2-3 paragraphs.")
        if jargon_matches > 3:
            recommendations.append(f"Replace {jargon_matches} occurrences of abstract jargon with concrete physical nouns.")
        if wikilinks == 0:
            recommendations.append("Add associative wikilinks ([[concept]]) to enable non-linear spatial navigation.")

        if not recommendations:
            recommendations.append("Document displays exceptional spatial-first architecture and low phonological friction.")

        return {
            "title": doc_title,
            "word_count": word_count,
            "sentence_count": sentence_count,
            "paragraph_count": paragraph_count,
            "metrics": {
                "cognitive_leverage_score": cognitive_leverage_score,
                "phonological_friction": round(phonological_friction, 1),
                "spatial_leverage": round(spatial_leverage, 1),
                "working_memory_tax": round(stamina_tax, 1),
                "connectivity_score": round(connectivity_score, 1)
            },
            "spatial_features": {
                "bullet_points": bullet_points,
                "headers": headers,
                "table_rows": table_rows,
                "wikilinks": wikilinks,
                "code_blocks": code_blocks
            },
            "recommendations": recommendations
        }

    @classmethod
    def _empty_audit(cls, title: str) -> Dict[str, Any]:
        return {
            "title": title,
            "word_count": 0,
            "sentence_count": 0,
            "paragraph_count": 0,
            "metrics": {
                "cognitive_leverage_score": 0.0,
                "phonological_friction": 0.0,
                "spatial_leverage": 0.0,
                "working_memory_tax": 0.0,
                "connectivity_score": 0.0
            },
            "spatial_features": {
                "bullet_points": 0,
                "headers": 0,
                "table_rows": 0,
                "wikilinks": 0,
                "code_blocks": 0
            },
            "recommendations": ["Provide non-empty text to initiate cognitive metacognition audit."]
        }


class MetacognitionExporter:
    """Exports audit findings into Obsidian Canvas scorecards and vector SVG dashboards."""

    @staticmethod
    def to_canvas(audit_data: Dict[str, Any]) -> Dict[str, Any]:
        nodes = []
        edges = []

        m = audit_data.get("metrics", {})
        sf = audit_data.get("spatial_features", {})
        recs = audit_data.get("recommendations", [])
        title = audit_data.get("title", "Cognitive Audit")

        score = m.get("cognitive_leverage_score", 0.0)
        header_color = "4" if score >= 75.0 else ("3" if score >= 50.0 else "1")

        # 1. Central Executive Node
        root_id = "node-audit-root"
        nodes.append({
            "id": root_id,
            "type": "text",
            "text": (
                f"## {title}\n"
                f"**Cognitive Leverage Score:** `{score}/100`\n"
                f"Working Memory Tax: `{m.get('working_memory_tax', 0)}%`\n"
                f"Words: **{audit_data.get('word_count', 0)}** | Sentences: **{audit_data.get('sentence_count', 0)}**"
            ),
            "x": 0,
            "y": -220,
            "width": 380,
            "height": 160,
            "color": header_color
        })

        # 2. Phonological Friction Node
        phono_id = "node-phonological-friction"
        nodes.append({
            "id": phono_id,
            "type": "text",
            "text": (
                f"### Phonological Loop Friction\n"
                f"**Index:** `{m.get('phonological_friction', 0)}/100`\n\n"
                f"> Measures phonological decoding resistance, syllable density, and sentence run-on."
            ),
            "x": -420,
            "y": 40,
            "width": 320,
            "height": 180,
            "color": "1" if m.get("phonological_friction", 0) > 50 else "4"
        })
        edges.append({
            "id": "edge-phono",
            "fromNode": root_id,
            "fromSide": "left",
            "toNode": phono_id,
            "toSide": "top",
            "label": f"Friction: {m.get('phonological_friction', 0)}"
        })

        # 3. Spatial Leverage Node
        spatial_id = "node-spatial-leverage"
        nodes.append({
            "id": spatial_id,
            "type": "text",
            "text": (
                f"### Spatial Leverage Ratio\n"
                f"**Index:** `{m.get('spatial_leverage', 0)}/100`\n\n"
                f"- Bullet Anchors: **{sf.get('bullet_points', 0)}**\n"
                f"- Section Headers: **{sf.get('headers', 0)}**\n"
                f"- Relational Tables: **{sf.get('table_rows', 0)}**\n"
                f"- Associative Links: **{sf.get('wikilinks', 0)}**"
            ),
            "x": 420,
            "y": 40,
            "width": 320,
            "height": 180,
            "color": "4" if m.get("spatial_leverage", 0) >= 50 else "1"
        })
        edges.append({
            "id": "edge-spatial",
            "fromNode": root_id,
            "fromSide": "right",
            "toNode": spatial_id,
            "toSide": "top",
            "label": f"Spatial: {m.get('spatial_leverage', 0)}"
        })

        # 4. Actionable Refactoring Plan
        rec_text = "### Strategic Refactoring Recommendations\n\n" + "\n".join(f"- {r}" for r in recs)
        recs_id = "node-recommendations"
        nodes.append({
            "id": recs_id,
            "type": "text",
            "text": rec_text,
            "x": 0,
            "y": 280,
            "width": 460,
            "height": 220,
            "color": "5"
        })
        edges.append({
            "id": "edge-recs",
            "fromNode": root_id,
            "fromSide": "bottom",
            "toNode": recs_id,
            "toSide": "top",
            "label": "Synthesis Remediation"
        })

        return {"nodes": nodes, "edges": edges}

    @staticmethod
    def to_svg_dashboard(audit_data: Dict[str, Any]) -> str:
        width = 680
        height = 360
        m = audit_data.get("metrics", {})
        title = audit_data.get("title", "Cognitive Audit")
        score = m.get("cognitive_leverage_score", 0.0)

        svg = []
        svg.append(f'<svg width="100%" height="auto" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">')
        svg.append(f'<rect width="{width}" height="{height}" rx="14" fill="#09090b" stroke="#27272a" stroke-width="1.5"/>')

        # Header Title
        svg.append(f'<text x="28" y="38" fill="#fafafa" font-size="18" font-weight="bold" font-family="sans-serif">{title}</text>')
        svg.append(f'<text x="28" y="60" fill="#a1a1aa" font-size="12" font-family="sans-serif">Flavell-Sweller Metacognitive Synthesis Audit | Zero Em Dash Policy Active</text>')

        # Metric Tiles (3 across)
        score_col = "#10b981" if score >= 75.0 else ("#f59e0b" if score >= 50.0 else "#ef4444")
        tiles = [
            ("Cognitive Leverage", f"{score}/100", score_col),
            ("Phonological Friction", f"{m.get('phonological_friction', 0)}%", "#ef4444" if m.get('phonological_friction', 0) > 50 else "#10b981"),
            ("Spatial Leverage", f"{m.get('spatial_leverage', 0)}%", "#10b981" if m.get('spatial_leverage', 0) >= 50 else "#f59e0b")
        ]

        tile_w = 195
        tile_h = 75
        tile_y = 85
        spacing = 20
        start_x = 28

        for idx, (label, val, col) in enumerate(tiles):
            tx = start_x + idx * (tile_w + spacing)
            svg.append(f'<g transform="translate({tx}, {tile_y})">')
            svg.append(f'<rect width="{tile_w}" height="{tile_h}" rx="8" fill="#18181b" stroke="{col}" stroke-width="1.5"/>')
            svg.append(f'<text x="14" y="26" fill="#a1a1aa" font-size="11" font-family="sans-serif">{label}</text>')
            svg.append(f'<text x="14" y="56" fill="{col}" font-size="22" font-weight="bold" font-family="sans-serif">{val}</text>')
            svg.append('</g>')

        # Working Memory Stamina Gauge
        gauge_y = 190
        gauge_w = 624
        tax = m.get("working_memory_tax", 0.0)
        fill_tax = max(10, int(gauge_w * (tax / 100.0)))
        tax_col = "#ef4444" if tax > 60 else ("#f59e0b" if tax > 35 else "#10b981")

        svg.append(f'<text x="28" y="{gauge_y - 8}" fill="#a1a1aa" font-size="11" font-family="sans-serif">Working Memory Stamina Tax ({tax}%)</text>')
        svg.append(f'<rect x="28" y="{gauge_y}" width="{gauge_w}" height="14" rx="7" fill="#27272a"/>')
        svg.append(f'<rect x="28" y="{gauge_y}" width="{fill_tax}" height="14" rx="7" fill="{tax_col}"/>')

        # Strategic Recommendation Box
        box_y = 230
        svg.append(f'<rect x="28" y="{box_y}" width="624" height="85" rx="8" fill="#18181b" stroke="#27272a" stroke-width="1"/>')
        svg.append(f'<text x="44" y="{box_y + 24}" fill="#38bdf8" font-size="12" font-weight="bold" font-family="sans-serif">Primary Refactoring Directive</text>')

        recs = audit_data.get("recommendations", ["Optimal spatial balance."])
        rec_snippet = re.sub(r"[<>&]", "", recs[0])[:75] + ("..." if len(recs[0]) > 75 else "")
        svg.append(f'<text x="44" y="{box_y + 50}" fill="#e4e4e7" font-size="11" font-family="sans-serif">{rec_snippet}</text>')

        # Footer
        svg.append(f'<text x="28" y="340" fill="#52525b" font-size="10" font-family="sans-serif">DxSkills Cognitive Ergonomics Engine</text>')

        svg.append('</svg>')
        return "\n".join(svg)


def run_audit(
    text: str,
    title: Optional[str] = None,
    output_canvas: Optional[str] = None,
    output_svg: Optional[str] = None
) -> Tuple[Dict[str, Any], Dict[str, Any], str]:
    """Runs metacognition audit on input text and exports artifacts."""
    audit_data = MetacognitionAuditor.audit_text(text, title=title)
    canvas_data = MetacognitionExporter.to_canvas(audit_data)
    svg_code = MetacognitionExporter.to_svg_dashboard(audit_data)

    if output_canvas:
        os.makedirs(os.path.dirname(os.path.abspath(output_canvas)), exist_ok=True)
        with open(output_canvas, "w", encoding="utf-8") as f:
            json.dump(canvas_data, f, indent=2)

    if output_svg:
        os.makedirs(os.path.dirname(os.path.abspath(output_svg)), exist_ok=True)
        with open(output_svg, "w", encoding="utf-8") as f:
            f.write(svg_code)

    return audit_data, canvas_data, svg_code


def main():
    parser = argparse.ArgumentParser(description="DxSkills Autonomous Cognitive Metacognition & Synthesis Audit")
    parser.add_argument("input", nargs="?", help="Input text, file path, or markdown note to audit")
    parser.add_argument("--title", "-t", help="Title for the audit report")
    parser.add_argument("--canvas", "-c", help="Output Obsidian .canvas scorecard filepath")
    parser.add_argument("--svg", "-s", help="Output vector SVG audit dashboard filepath")
    parser.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")

    args = parser.parse_args()

    content = ""
    if args.input:
        if os.path.isfile(args.input):
            with open(args.input, "r", encoding="utf-8") as f:
                content = f.read()
        else:
            content = args.input
    else:
        if not sys.stdin.isatty():
            content = sys.stdin.read()
        else:
            content = (
                "# Executive Architecture Proposal\n"
                "> **BLUF:** Decouple phonological working memory from spatial reasoning models.\n\n"
                "## Core Pillars\n"
                "- 1. High-contrast spatial canvas topology.\n"
                "- 2. Automated cross-vault synchronization without manual ID linking.\n"
                "- 3. Lossless multi-modal audio-spatial flashcards.\n\n"
                "| Milestone | Target Horizon | Status |\n"
                "| :--- | :--- | :--- |\n"
                "| Phase 48 | Q3 2026 | Active Deployment |\n"
                "| Phase 49 | Q4 2026 | Backlog Scoping |\n"
            )

    audit_data, canvas_data, svg_code = run_audit(
        content,
        title=args.title,
        output_canvas=args.canvas,
        output_svg=args.svg
    )

    if args.json:
        print(json.dumps(audit_data, indent=2))
    elif not (args.canvas or args.svg):
        m = audit_data["metrics"]
        print(f"\n=== [DxSkills: Metacognitive Synthesis Audit ({m['cognitive_leverage_score']}/100)] ===")
        print(f"Phonological Friction: {m['phonological_friction']}% | Spatial Leverage: {m['spatial_leverage']}%")
        print(f"Working Memory Tax: {m['working_memory_tax']}% | Connectivity: {m['connectivity_score']}%")
        print("\nPrimary Directives:")
        for r in audit_data["recommendations"]:
            print(f"  - {r}")
    else:
        print(f"[DxSkills] Completed audit (Cognitive Leverage: {audit_data['metrics']['cognitive_leverage_score']}/100).")
        if args.canvas:
            print(f"  - Scorecard Canvas: {args.canvas}")
        if args.svg:
            print(f"  - SVG Dashboard: {args.svg}")


if __name__ == "__main__":
    main()
