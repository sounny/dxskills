"""
Multi-Modal Audio-Spatial Flashcard and Rapid Retrieval Engine for DxSkills.

Transforms text notes and vocabulary sets into spatial Leitner flashcards
anchored by 2D coordinates, acoustic rhythm cues, and micro-vector clues.
Exports to Obsidian .canvas decks and interactive HTML study sessions.

Zero em dash policy strictly enforced.
"""

import os
import sys
import json
import re
import argparse
from typing import Dict, List, Any, Optional, Tuple


class FlashcardGenerator:
    """Generates multi-modal spatial flashcards from markdown or raw text."""

    SPATIAL_SECTORS = [
        ("Top-Left", -300, -200, "1"),     # Red
        ("Top-Right", 300, -200, "2"),     # Orange
        ("Center-Hub", 0, 0, "4"),         # Green
        ("Bottom-Left", -300, 200, "5"),   # Blue
        ("Bottom-Right", 300, 200, "6")    # Purple
    ]

    ACOUSTIC_PATTERNS = [
        "Rhythmic cadence: emphasize first and last syllable.",
        "Phonetic contrast: contrast against the counter-premise.",
        "Acoustic anchor: short 3-beat mnemonic triad.",
        "Spoken cadence: rising pitch on premise, falling on takeaway."
    ]

    @classmethod
    def generate_cards(cls, content: str) -> List[Dict[str, Any]]:
        raw_items = cls._extract_items(content)
        cards = []

        for idx, (front, back) in enumerate(raw_items, 1):
            sector_name, sx, sy, scolor = cls.SPATIAL_SECTORS[(idx - 1) % len(cls.SPATIAL_SECTORS)]
            acoustic_cue = cls.ACOUSTIC_PATTERNS[(idx - 1) % len(cls.ACOUSTIC_PATTERNS)]

            # Generate micro-vector clue SVG
            svg_clue = cls._generate_micro_svg(idx, scolor)

            cards.append({
                "id": f"card-{idx}",
                "front": front,
                "back": back,
                "box": 1,
                "sector": sector_name,
                "x": sx,
                "y": sy,
                "color": scolor,
                "acoustic_cue": acoustic_cue,
                "svg_clue": svg_clue
            })

        return cards

    @classmethod
    def _extract_items(cls, content: str) -> List[Tuple[str, str]]:
        lines = [line.strip() for line in content.split("\n") if line.strip()]
        items = []

        for line in lines:
            # Check Q&A formats: Q: ... A: ... or Front: ... Back: ...
            if "::" in line:
                parts = line.split("::", 1)
                items.append((parts[0].strip(), parts[1].strip()))
            elif re.match(r"^[-*]?\s*(.*?)\s*[-:=]>\s*(.*)$", line):
                m = re.match(r"^[-*]?\s*(.*?)\s*[-:=]>\s*(.*)$", line)
                items.append((m.group(1).strip(), m.group(2).strip()))
            elif line.startswith(("-", "*")) and ":" in line:
                parts = line.lstrip("-* ").split(":", 1)
                items.append((parts[0].strip(), parts[1].strip()))

        if not items:
            # Default demonstrative set based on Eide MIND framework
            items = [
                ("M-Reasoning (Spatial/Material)", "3D spatial reasoning, mechanics, topology, and physical geometry"),
                ("I-Reasoning (Interconnected)", "Discovering non-obvious patterns, analogies, and holistic connections"),
                ("N-Reasoning (Narrative)", "Episodic memory, causal narrative storytelling, and contextual framing"),
                ("D-Reasoning (Dynamic/Predictive)", "Simulation of future systems, anticipating edge cases, and trend forecasting")
            ]

        return items

    @staticmethod
    def _generate_micro_svg(index: int, color_code: str) -> str:
        colors = {"1": "#ef4444", "2": "#f59e0b", "3": "#eab308", "4": "#10b981", "5": "#3b82f6", "6": "#8b5cf6"}
        c = colors.get(color_code, "#3b82f6")
        return f'<svg width="24" height="24" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9" fill="{c}22" stroke="{c}" stroke-width="2"/><text x="12" y="16" fill="{c}" font-size="11" font-weight="bold" text-anchor="middle">{index}</text></svg>'


class SpatialFlashcardExporter:
    """Exports flashcards into Obsidian .canvas and interactive HTML."""

    @staticmethod
    def to_canvas(cards: List[Dict[str, Any]], deck_title: str = "Spatial Flashcard Deck") -> Dict[str, Any]:
        nodes = []
        edges = []

        # Header node
        nodes.append({
            "id": "node-deck-header",
            "type": "text",
            "text": f"## {deck_title}\nTotal Cards: **{len(cards)}**\nSpatial Leitner Anchors Active",
            "x": 0,
            "y": -340,
            "width": 360,
            "height": 130,
            "color": "1"
        })

        # Arrange cards by Leitner Box columns
        box_x_offsets = {
            1: -600,  # Daily (Box 1)
            2: -200,  # 3 Days (Box 2)
            3: 200,   # Weekly (Box 3)
            4: 600,   # Bi-Weekly (Box 4)
            5: 1000   # Mastery (Box 5)
        }

        box_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}

        for card in cards:
            cid = card["id"]
            box = card.get("box", 1)
            bx = box_x_offsets.get(box, -600)
            by = -140 + (box_counts[box] * 240)
            box_counts[box] += 1

            text_content = (
                f"### {card['front']}\n"
                f"**Sector:** `{card['sector']}` | **Box:** `{box}`\n\n"
                f"---\n"
                f"**Resolution:** {card['back']}\n\n"
                f"> **Acoustic:** {card['acoustic_cue']}"
            )

            nodes.append({
                "id": cid,
                "type": "text",
                "text": text_content,
                "x": bx,
                "y": by,
                "width": 340,
                "height": 210,
                "color": card.get("color", "5")
            })

            edges.append({
                "id": f"edge-header-{cid}",
                "fromNode": "node-deck-header",
                "fromSide": "bottom",
                "toNode": cid,
                "toSide": "top",
                "label": f"Leitner Box {box}"
            })

        return {"nodes": nodes, "edges": edges}

    @staticmethod
    def to_html(cards: List[Dict[str, Any]], deck_title: str = "Spatial Flashcard Deck") -> str:
        cards_json = json.dumps(cards)
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{deck_title}</title>
    <style>
        body {{
            background: #09090b;
            color: #f4f4f5;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            margin: 0;
            padding: 40px 20px;
            display: flex;
            justify-content: center;
        }}
        .container {{
            max-width: 800px;
            width: 100%;
        }}
        .header {{
            background: #18181b;
            border: 1px solid #27272a;
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .card-box {{
            perspective: 1000px;
            margin-bottom: 20px;
        }}
        .card-inner {{
            background: #18181b;
            border: 1px solid #3f3f46;
            border-radius: 12px;
            padding: 24px;
            min-height: 200px;
            cursor: pointer;
            transition: transform 0.3s;
        }}
        .card-inner:hover {{
            border-color: #71717a;
        }}
        .btn {{
            background: #27272a;
            color: #fafafa;
            border: 1px solid #3f3f46;
            padding: 8px 16px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
        }}
        .btn:hover {{
            background: #3f3f46;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div>
                <h1 style="margin: 0 0 6px 0; font-size: 22px;">{deck_title}</h1>
                <div style="color: #a1a1aa; font-size: 13px;">Multi-Modal Audio-Spatial Retrieval Session</div>
            </div>
            <div style="font-size: 14px; color: #38bdf8; font-family: monospace;">Total: {len(cards)} Cards</div>
        </div>

        <div id="card-display" class="card-box">
            <!-- Dynamic interactive card renderer -->
        </div>

        <div style="display: flex; justify-content: space-between; margin-top: 16px;">
            <button class="btn" onclick="prevCard()">Previous</button>
            <button class="btn" style="background: #3b82f6; border-color: #60a5fa;" onclick="flipCard()">Flip Card (Space)</button>
            <button class="btn" onclick="nextCard()">Next</button>
        </div>
    </div>

    <script>
        const cards = {cards_json};
        let currentIndex = 0;
        let isFlipped = false;

        function renderCard() {{
            if (cards.length === 0) return;
            const c = cards[currentIndex];
            const el = document.getElementById('card-display');
            const content = isFlipped ? 
                `<div style="color: #4ade80; font-size: 12px; font-weight: bold; text-transform: uppercase; margin-bottom: 8px;">Resolution / Concept</div><div style="font-size: 18px; line-height: 1.5; color: #f4f4f5;">${{c.back}}</div><div style="margin-top: 16px; color: #a1a1aa; font-size: 13px;">${{c.acoustic_cue}}</div>` :
                `<div style="color: #38bdf8; font-size: 12px; font-weight: bold; text-transform: uppercase; margin-bottom: 8px;">Spatial Query (${{c.sector}})</div><div style="font-size: 20px; font-weight: 600; color: #fafafa;">${{c.front}}</div><div style="margin-top: 20px; font-size: 12px; color: #71717a;">Click or press Space to reveal resolution</div>`;
            
            el.innerHTML = `
                <div class="card-inner" onclick="flipCard()">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 12px;">
                        <span style="font-family: monospace; color: #a1a1aa;">Card ${{currentIndex + 1}} / ${{cards.length}}</span>
                        <span style="color: #fbbf24; font-weight: bold; font-size: 12px;">Leitner Box ${{c.box}}</span>
                    </div>
                    ${{content}}
                </div>
            `;
        }}

        function flipCard() {{
            isFlipped = !isFlipped;
            renderCard();
        }}

        function nextCard() {{
            currentIndex = (currentIndex + 1) % cards.length;
            isFlipped = false;
            renderCard();
        }}

        function prevCard() {{
            currentIndex = (currentIndex - 1 + cards.length) % cards.length;
            isFlipped = false;
            renderCard();
        }}

        document.addEventListener('keydown', (e) => {{
            if (e.code === 'Space') {{
                e.preventDefault();
                flipCard();
            }} else if (e.code === 'ArrowRight') {{
                nextCard();
            }} else if (e.code === 'ArrowLeft') {{
                prevCard();
            }}
        }});

        renderCard();
    </script>
</body>
</html>"""


def run_flashcards(
    content: str,
    title: Optional[str] = None,
    output_canvas: Optional[str] = None,
    output_html: Optional[str] = None
) -> Tuple[List[Dict[str, Any]], Dict[str, Any], str]:
    """Generates cards and formats canvas and html outputs."""
    cards = FlashcardGenerator.generate_cards(content)
    deck_title = title or "Spatial Retrieval Deck"

    canvas_data = SpatialFlashcardExporter.to_canvas(cards, deck_title=deck_title)
    html_code = SpatialFlashcardExporter.to_html(cards, deck_title=deck_title)

    if output_canvas:
        os.makedirs(os.path.dirname(os.path.abspath(output_canvas)), exist_ok=True)
        with open(output_canvas, "w", encoding="utf-8") as f:
            json.dump(canvas_data, f, indent=2)

    if output_html:
        os.makedirs(os.path.dirname(os.path.abspath(output_html)), exist_ok=True)
        with open(output_html, "w", encoding="utf-8") as f:
            f.write(html_code)

    return cards, canvas_data, html_code


def main():
    parser = argparse.ArgumentParser(description="DxSkills Multi-Modal Audio-Spatial Flashcard & Retrieval Engine")
    parser.add_argument("input", nargs="?", help="Input markdown note, Q&A list, or vocabulary file")
    parser.add_argument("--title", "-t", help="Flashcard deck title")
    parser.add_argument("--canvas", "-c", help="Output Obsidian .canvas filepath")
    parser.add_argument("--html", help="Output interactive HTML session filepath")
    parser.add_argument("--json", "-j", action="store_true", help="Output raw JSON cards")

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
            # Default MIND Framework vocabulary
            content = (
                "M-Reasoning (Material/Spatial) :: 3D spatial reasoning, mechanics, topology, and physical geometry\n"
                "I-Reasoning (Interconnected) :: Discovering non-obvious patterns, analogies, and holistic connections\n"
                "N-Reasoning (Narrative) :: Episodic memory, causal narrative storytelling, and contextual framing\n"
                "D-Reasoning (Dynamic/Predictive) :: Simulation of future systems, anticipating edge cases, and trend forecasting"
            )

    cards, canvas_data, html_code = run_flashcards(
        content,
        title=args.title,
        output_canvas=args.canvas,
        output_html=args.html
    )

    if args.json:
        print(json.dumps({"deck_title": args.title or "Spatial Retrieval Deck", "cards_count": len(cards), "cards": cards}, indent=2))
    elif not (args.canvas or args.html):
        print(f"\n=== [DxSkills: Spatial Flashcard Deck ({len(cards)} Cards)] ===")
        for c in cards:
            print(f"[{c['id']}] {c['front']} ({c['sector']}) -> {c['back']}")
    else:
        print(f"[DxSkills] Generated {len(cards)} spatial flashcards.")
        if args.canvas:
            print(f"  - Canvas: {args.canvas}")
        if args.html:
            print(f"  - HTML: {args.html}")


if __name__ == "__main__":
    main()
