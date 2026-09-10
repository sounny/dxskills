"""
Socratic Debate and Thesis Stress-Testing Simulator for DxSkills.

Autonomous dialectical challenger that stress-tests spatial architecture
proposals, designs, and theses against reductionist and pragmatic critiques.
Generates hardened claim-rebuttal matrices and Obsidian debate canvases.

Zero em dash policy strictly enforced.
"""

import os
import sys
import json
import re
import argparse
from typing import Dict, List, Any, Optional, Tuple


class PropositionAnalyzer:
    """Extracts claims, premises, and vulnerability indicators from proposals."""

    VULNERABILITY_PATTERNS = [
        (r"\b(seamlessly|effortlessly|automatically|obviously|naturally)\b", "Hand-waving assumption of zero friction"),
        (r"\b(all|always|never|every|none|completely|infinite)\b", "Absolutist claim vulnerable to single counterexample"),
        (r"\b(paradigm shift|revolutionary|disruptive|game[- ]changer)\b", "Buzzword inflation lacking mechanistic proof"),
        (r"\b(simple|trivial|easy|just|merely)\b", "Underestimation of implementation complexity"),
        (r"\b(optimal|perfect|best-in-class|ideal)\b", "Unbounded optimality claim lacking trade-off criteria"),
    ]

    def __init__(self, text: str):
        self.raw_text = text.strip()
        self.sentences = self._split_sentences(self.raw_text)

    @staticmethod
    def _split_sentences(text: str) -> List[str]:
        # Split on sentence boundaries while preserving structure
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        sentences = []
        for line in lines:
            # If line is bullet point or header
            if line.startswith(("#", "-", "*", ">")):
                clean = re.sub(r"^[#\-\*\>\s]+", "", line).strip()
                if clean:
                    sentences.append(clean)
            else:
                parts = re.split(r"(?<=[.!?])\s+", line)
                for part in parts:
                    clean = part.strip()
                    if len(clean) > 8:
                        sentences.append(clean)
        return sentences

    def extract_claims(self) -> List[Dict[str, Any]]:
        """Identifies actionable proposition claims from the text."""
        claims = []
        for i, sentence in enumerate(self.sentences):
            # Check length and substantive content
            tokens = re.findall(r"\b[A-Za-z0-9_\-]+\b", sentence.lower())
            if len(tokens) < 4:
                continue

            vulnerabilities = []
            for pattern, reason in self.VULNERABILITY_PATTERNS:
                matches = re.findall(pattern, sentence, re.IGNORECASE)
                if matches:
                    vulnerabilities.append({
                        "matched": list(set(matches)),
                        "reason": reason
                    })

            # Detect claim type
            s_lower = sentence.lower()
            if any(w in s_lower for w in ["will", "must", "enables", "replaces", "guarantees", "transforms"]):
                claim_type = "Strong Predictive"
            elif any(w in s_lower for w in ["propose", "proposes", "suggest", "suggests", "hypothesize", "hypothesizes", "aim to", "aims to", "explore"]):
                claim_type = "Exploratory Hypothesis"
            elif any(w in s_lower for w in ["because", "since", "due to", "grounded in"]):
                claim_type = "Causal Premise"
            else:
                claim_type = "Structural Assertion"

            claims.append({
                "id": f"claim-{i + 1}",
                "text": sentence,
                "type": claim_type,
                "vulnerabilities": vulnerabilities,
                "vulnerability_score": min(100, len(vulnerabilities) * 30 + (20 if claim_type == "Strong Predictive" else 10))
            })

        # If no sentences met threshold, treat the whole raw text as single claim
        if not claims and self.raw_text:
            claims.append({
                "id": "claim-1",
                "text": self.raw_text,
                "type": "Structural Assertion",
                "vulnerabilities": [],
                "vulnerability_score": 25
            })

        return claims


class SocraticDebater:
    """Simulates adversarial three-party dialectic: Skeptic, Pragmatist, and Synthesizer."""

    SKEPTIC_QUESTIONS = [
        "What empirical baseline proves this assertion over the established null hypothesis?",
        "Where is the boundary condition where this holistic approach categorically fails?",
        "How is this distinct from prior failed architectures attempting the same abstraction?",
        "What is the quantifiable error rate when your core assumption is violated?",
        "Which single point of failure invalidates the entire structural premise?"
    ]

    PRAGMATIST_CONCERNS = [
        "What is the day-one adoption friction for a team unfamiliar with spatial semantics?",
        "How does this handle degraded operating modes or corrupted state transitions?",
        "What is the real cognitive switching overhead between linear tasks and this interface?",
        "Who maintains the graph schema when initial enthusiasm wanes?",
        "What is the cold-start latency before this produces tangible utility?"
    ]

    SYNTHESIS_BRIDGES = [
        "Anchor the claim with an explicit boundary condition and automated fallback path.",
        "Decouple the spatial mental model from the underlying linear execution pipeline.",
        "Provide zero-configuration default templates before introducing spatial graphs.",
        "Formalize a verifiable metric table demonstrating empirical advantage.",
        "Instrument an automated telemetry audit to catch degradation at runtime."
    ]

    def __init__(self, topic: str, claims: List[Dict[str, Any]]):
        self.topic = topic
        self.claims = claims

    def generate_debate(self) -> Dict[str, Any]:
        """Conducts a multi-perspective stress test for each claim."""
        matrix = []
        overall_scores = []

        for idx, claim in enumerate(self.claims):
            c_text = claim["text"]
            v_score = claim["vulnerability_score"]
            overall_scores.append(v_score)

            skeptic_q = self.SKEPTIC_QUESTIONS[idx % len(self.SKEPTIC_QUESTIONS)]
            pragmatist_c = self.PRAGMATIST_CONCERNS[idx % len(self.PRAGMATIST_CONCERNS)]
            synthesis_b = self.SYNTHESIS_BRIDGES[idx % len(self.SYNTHESIS_BRIDGES)]

            # Formulate targeted challenge based on vulnerabilities
            specific_attacks = []
            for v in claim.get("vulnerabilities", []):
                words = ", ".join(f"'{w}'" for w in v["matched"])
                specific_attacks.append(f"Flagged word(s) {words}: {v['reason']}.")

            skeptic_critique = skeptic_q
            if specific_attacks:
                skeptic_critique = f"{' '.join(specific_attacks)} {skeptic_q}"

            pragmatist_critique = f"Operational stress test: {pragmatist_c}"

            # Steel-manned defense synthesis
            defense = (
                f"Defensive protocol: {synthesis_b} Acknowledge operational boundaries upfront "
                f"to disarm reductionist skepticism."
            )

            # Verification artifact required
            required_artifact = self._derive_required_artifact(claim["type"], idx)

            matrix.append({
                "claim_id": claim["id"],
                "claim_text": c_text,
                "claim_type": claim["type"],
                "vulnerability_score": v_score,
                "skeptic_attack": skeptic_critique,
                "pragmatist_challenge": pragmatist_critique,
                "steel_manned_defense": defense,
                "required_proof_artifact": required_artifact
            })

        avg_vulnerability = sum(overall_scores) / len(overall_scores) if overall_scores else 0
        readiness_score = max(0, round(100 - avg_vulnerability))

        return {
            "topic": self.topic,
            "total_claims": len(self.claims),
            "thesis_readiness_score": readiness_score,
            "matrix": matrix
        }

    @staticmethod
    def _derive_required_artifact(claim_type: str, index: int) -> str:
        artifacts = {
            "Strong Predictive": "Benchmark latency comparison or automated unit test assert",
            "Exploratory Hypothesis": "Documented pilot study or 3-step proof of concept",
            "Causal Premise": "Ablation test isolating the dependent variable",
            "Structural Assertion": "Formal architecture block diagram with interface contracts"
        }
        return artifacts.get(claim_type, "Reproducible operational script with telemetry")


class SocraticDebateExporter:
    """Formats and exports debate outcomes to Markdown, HTML, and Obsidian Canvas."""

    @staticmethod
    def to_markdown(debate_data: Dict[str, Any]) -> str:
        lines = []
        topic = debate_data.get("topic", "Architectural Proposal")
        score = debate_data.get("thesis_readiness_score", 70)
        lines.append(f"# Socratic Debate & Stress-Testing Matrix: {topic}")
        lines.append("")
        lines.append(f"> **Thesis Hardening Score:** `{score}/100` | **Total Claims Evaluated:** `{debate_data.get('total_claims', 0)}`")
        lines.append("")
        lines.append("## Adversarial Cross-Examination Matrix")
        lines.append("")
        lines.append("| ID | Proposition / Claim | Skeptic Attack (Reductionist) | Pragmatist Challenge (Operational) | Steel-Manned Defense | Verification Artifact |")
        lines.append("|:---|:---------------------|:------------------------------|:------------------------------------|:---------------------|:----------------------|")

        for item in debate_data.get("matrix", []):
            cid = item["claim_id"]
            c_text = item["claim_text"].replace("|", "\\|")
            skeptic = item["skeptic_attack"].replace("|", "\\|")
            pragmatist = item["pragmatist_challenge"].replace("|", "\\|")
            defense = item["steel_manned_defense"].replace("|", "\\|")
            artifact = item["required_proof_artifact"].replace("|", "\\|")
            lines.append(f"| **{cid}** | {c_text} | {skeptic} | {pragmatist} | {defense} | `{artifact}` |")

        lines.append("")
        lines.append("## Dialectical Synthesis Guidance")
        lines.append("")
        lines.append("1. **Disarm reductionist critics first:** State known failure modes and bounds in your opening slide.")
        lines.append("2. **Translate spatial intuitions into linear metrics:** Accompany every holistic map with a verifiable benchmark.")
        lines.append("3. **Eliminate hand-wavy friction claims:** Replace words like 'seamlessly' with explicit protocol specifications.")
        lines.append("")
        return "\n".join(lines)

    @staticmethod
    def to_html(debate_data: Dict[str, Any]) -> str:
        topic = debate_data.get("topic", "Architectural Proposal")
        score = debate_data.get("thesis_readiness_score", 70)
        matrix = debate_data.get("matrix", [])

        cards_html = []
        for item in matrix:
            cid = item["claim_id"]
            c_text = item["claim_text"]
            v_score = item["vulnerability_score"]
            skeptic = item["skeptic_attack"]
            pragmatist = item["pragmatist_challenge"]
            defense = item["steel_manned_defense"]
            artifact = item["required_proof_artifact"]

            v_color = "#ef4444" if v_score > 60 else ("#f59e0b" if v_score > 35 else "#10b981")

            card = f"""
            <div style="background: rgba(24, 24, 27, 0.85); border: 1px solid #3f3f46; border-radius: 12px; padding: 20px; margin-bottom: 20px; box-shadow: 0 8px 24px rgba(0,0,0,0.4);">
                <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #27272a; padding-bottom: 12px; margin-bottom: 16px;">
                    <span style="font-family: monospace; color: #a1a1aa; font-weight: bold;">{cid} ({item.get('claim_type', 'Claim')})</span>
                    <span style="background: {v_color}22; color: {v_color}; border: 1px solid {v_color}; padding: 3px 8px; border-radius: 6px; font-size: 12px; font-weight: bold;">Vulnerability {v_score}%</span>
                </div>
                <div style="font-size: 16px; font-weight: 600; color: #f4f4f5; margin-bottom: 16px; line-height: 1.5;">
                    "{c_text}"
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-bottom: 16px;">
                    <div style="background: #18181b; border-left: 3px solid #ef4444; padding: 12px; border-radius: 4px;">
                        <div style="color: #f87171; font-weight: bold; font-size: 12px; text-transform: uppercase; margin-bottom: 4px;">The Skeptic Attack</div>
                        <div style="color: #d4d4d8; font-size: 13px; line-height: 1.4;">{skeptic}</div>
                    </div>
                    <div style="background: #18181b; border-left: 3px solid #f59e0b; padding: 12px; border-radius: 4px;">
                        <div style="color: #fbbf24; font-weight: bold; font-size: 12px; text-transform: uppercase; margin-bottom: 4px;">The Pragmatist Challenge</div>
                        <div style="color: #d4d4d8; font-size: 13px; line-height: 1.4;">{pragmatist}</div>
                    </div>
                </div>
                <div style="background: #09090b; border: 1px solid #22c55e44; border-left: 3px solid #22c55e; padding: 14px; border-radius: 4px; margin-bottom: 12px;">
                    <div style="color: #4ade80; font-weight: bold; font-size: 12px; text-transform: uppercase; margin-bottom: 4px;">Steel-Manned Defense Protocol</div>
                    <div style="color: #e4e4e7; font-size: 13px; line-height: 1.5;">{defense}</div>
                </div>
                <div style="display: flex; align-items: center; font-size: 12px; color: #a1a1aa; gap: 6px;">
                    <span>Required Proof:</span>
                    <code style="background: #27272a; color: #38bdf8; padding: 2px 6px; border-radius: 4px; font-family: monospace;">{artifact}</code>
                </div>
            </div>
            """
            cards_html.append(card)

        score_color = "#10b981" if score >= 75 else ("#f59e0b" if score >= 50 else "#ef4444")

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Socratic Debate Stress Test - {topic}</title>
    <style>
        body {{
            background: #09090b;
            color: #f4f4f5;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            margin: 0;
            padding: 40px 20px;
            display: flex;
            justify-content: center;
        }}
        .container {{
            max-width: 900px;
            width: 100%;
        }}
        .header {{
            background: #18181b;
            border: 1px solid #27272a;
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div>
                <h1 style="margin: 0 0 8px 0; font-size: 24px; color: #fafafa;">Socratic Debate Simulator</h1>
                <div style="color: #a1a1aa; font-size: 14px;">Topic: <strong style="color: #e4e4e7;">{topic}</strong></div>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 32px; font-weight: bold; color: {score_color};">{score}<span style="font-size: 16px; color: #71717a;">/100</span></div>
                <div style="font-size: 12px; color: #a1a1aa; text-transform: uppercase;">Hardening Score</div>
            </div>
        </div>
        <div>
            {''.join(cards_html)}
        </div>
    </div>
</body>
</html>"""

    @staticmethod
    def to_canvas(debate_data: Dict[str, Any]) -> Dict[str, Any]:
        """Exports debate items into an Obsidian .canvas structure."""
        nodes = []
        edges = []

        topic = debate_data.get("topic", "Architectural Proposal")
        score = debate_data.get("thesis_readiness_score", 70)

        # Center root node
        nodes.append({
            "id": "root-topic",
            "type": "text",
            "text": f"## {topic}\nHardening Score: **{score}/100**\nStatus: Dialectical Stress-Test Active",
            "x": 0,
            "y": 0,
            "width": 380,
            "height": 140,
            "color": "4"  # Green
        })

        y_offset = 240
        for i, item in enumerate(debate_data.get("matrix", [])):
            cid = item["claim_id"]
            claim_node_id = f"node-{cid}"
            skeptic_node_id = f"node-skep-{cid}"
            prag_node_id = f"node-prag-{cid}"
            defense_node_id = f"node-def-{cid}"

            # Proposition Node (Left-Center)
            nodes.append({
                "id": claim_node_id,
                "type": "text",
                "text": f"### {cid}\n**Claim:** {item['claim_text']}\n*Type:* {item.get('claim_type', 'Claim')}",
                "x": 0,
                "y": y_offset,
                "width": 380,
                "height": 180,
                "color": "5"  # Blue
            })

            # Edge from root to claim
            edges.append({
                "id": f"edge-root-{cid}",
                "fromNode": "root-topic",
                "fromSide": "bottom",
                "toNode": claim_node_id,
                "toSide": "top"
            })

            # Skeptic Node (Left column, Red)
            nodes.append({
                "id": skeptic_node_id,
                "type": "text",
                "text": f"### Reductionist Critique\n{item['skeptic_attack']}",
                "x": -440,
                "y": y_offset - 20,
                "width": 360,
                "height": 160,
                "color": "1"  # Red
            })
            edges.append({
                "id": f"edge-skep-{cid}",
                "fromNode": skeptic_node_id,
                "fromSide": "right",
                "toNode": claim_node_id,
                "toSide": "left"
            })

            # Pragmatist Node (Right column, Orange)
            nodes.append({
                "id": prag_node_id,
                "type": "text",
                "text": f"### Operational Challenge\n{item['pragmatist_challenge']}",
                "x": 440,
                "y": y_offset - 20,
                "width": 360,
                "height": 160,
                "color": "2"  # Orange
            })
            edges.append({
                "id": f"edge-prag-{cid}",
                "fromNode": prag_node_id,
                "fromSide": "left",
                "toNode": claim_node_id,
                "toSide": "right"
            })

            # Defense / Synthesis Node (Directly below claim, Green/Cyan)
            nodes.append({
                "id": defense_node_id,
                "type": "text",
                "text": f"### Hardened Defense\n{item['steel_manned_defense']}\n\n**Artifact:** `{item['required_proof_artifact']}`",
                "x": 0,
                "y": y_offset + 220,
                "width": 380,
                "height": 180,
                "color": "6"  # Purple/Cyan
            })
            edges.append({
                "id": f"edge-def-{cid}",
                "fromNode": claim_node_id,
                "fromSide": "bottom",
                "toNode": defense_node_id,
                "toSide": "top"
            })

            y_offset += 460

        return {"nodes": nodes, "edges": edges}


def run_socratic_debate(
    text: str,
    topic: Optional[str] = None,
    output_format: str = "markdown",
    output_file: Optional[str] = None
) -> Tuple[Dict[str, Any], str]:
    """Orchestrates end-to-end proposition parsing, debate generation, and formatting."""
    analyzer = PropositionAnalyzer(text)
    claims = analyzer.extract_claims()

    derived_topic = topic
    if not derived_topic:
        if claims:
            first_words = claims[0]["text"].split()[:6]
            derived_topic = " ".join(first_words) + ("..." if len(first_words) == 6 else "")
        else:
            derived_topic = "Spatial Architecture Proposal"

    debater = SocraticDebater(derived_topic, claims)
    debate_data = debater.generate_debate()

    if output_format.lower() in ("canvas", "json"):
        canvas_data = SocraticDebateExporter.to_canvas(debate_data)
        formatted_output = json.dumps(canvas_data, indent=2)
    elif output_format.lower() == "html":
        formatted_output = SocraticDebateExporter.to_html(debate_data)
    else:
        formatted_output = SocraticDebateExporter.to_markdown(debate_data)

    if output_file:
        os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(formatted_output)

    return debate_data, formatted_output


def main():
    parser = argparse.ArgumentParser(description="DxSkills Socratic Debate & Thesis Stress-Testing Simulator")
    parser.add_argument("input", nargs="?", help="Input text, proposal markdown file, or raw claim")
    parser.add_argument("--topic", help="Explicit topic title for the debate")
    parser.add_argument("--format", choices=["markdown", "html", "canvas", "json"], default="markdown", help="Output format")
    parser.add_argument("--output", "-o", help="Target output file path")

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
            # Default demonstrative sample
            content = (
                "Our spatial canvas architecture effortlessly eliminates all cognitive friction for non-linear thinkers. "
                "Because users navigate ideas spatially, traditional linear hierarchies will become completely obsolete. "
                "The engine automatically syncs high-dimensional vector graphs without any configuration overhead."
            )

    debate_data, output = run_socratic_debate(
        content,
        topic=args.topic,
        output_format=args.format,
        output_file=args.output
    )

    if not args.output:
        print(output)
    else:
        print(f"[DxSkills] Debate output written to {args.output} (Score: {debate_data['thesis_readiness_score']}/100)")


if __name__ == "__main__":
    main()
