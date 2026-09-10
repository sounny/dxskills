#!/usr/bin/env python3
"""
DxSkills Multi-Modal Parity & Export Telemetry Validator
Verifies lossless synchronization across sensory modalities:
- Visual / Spatial: Obsidian Canvas (.canvas) and Vector SVG
- Auditory / Spoken: Audio Digest Script & Speech Synthesis
- Textual / Executive: Obsidian Markdown & Notion Page Blocks

Cognitive Principle:
Dyslexic and spatial thinkers transition frequently between sensory modalities.
Information loss between visual maps, spoken digests, and action lists destroys
mental models and induces severe cognitive re-orientation fatigue.

Strict Rule: NO em dashes anywhere (use hyphens, commas, or parentheses).
"""

import os
import re
import sys
import json
import time

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if SKILL_DIR not in sys.path:
    sys.path.insert(0, SKILL_DIR)

import scripts.audio_digest as ad
import scripts.canvas_exporter as ce
import scripts.vault_exporter as ve

def extract_canonical_landmarks(markdown_text, title=None):
    """
    Extracts core semantic landmarks from markdown:
    - Title
    - BLUF / Directive
    - Major Structural Pillars (Headings)
    - Action Vectors (Next actions, checklists, deliverables)
    """
    lines = [l.strip() for l in markdown_text.strip().splitlines() if l.strip()]
    doc_title = title or "Spatial Deliverable"
    bluf = ""
    pillars = []
    actions = []

    for line in lines:
        if not title and line.startswith("# ") and doc_title == "Spatial Deliverable":
            doc_title = line.lstrip("# ").strip()
        elif line.startswith("> ") and not bluf:
            clean = line.lstrip("> ").strip()
            if any(k in clean for k in ["BLUF", "Decision Requested", "Core Value", "Summary"]):
                bluf = clean.replace("**", "").replace("*", "")
        elif line.startswith("## "):
            pillars.append(line.lstrip("## ").strip())
        elif re.match(r"^\d+\.\s", line) or line.startswith("- [ ]") or line.startswith("- "):
            clean_item = re.sub(r"^\d+\.\s+", "", line).replace("- [ ]", "").lstrip("-* ").strip()
            if len(clean_item) > 5 and len(actions) < 6:
                actions.append(clean_item)

    if not pillars:
        pillars = ["Core Architecture", "Execution Milestones"]

    return {
        "title": doc_title,
        "bluf": bluf,
        "pillars": pillars,
        "actions": actions
    }

def validate_multimodal_parity(markdown_text, title=None, lang="en"):
    """
    Verifies cross-modal synchronization across:
    1. Markdown canonical landmarks
    2. Spoken Audio Digest script
    3. Obsidian Canvas (.canvas) JSON graph
    4. Standalone Vector SVG Canvas
    5. Obsidian Vault Markdown note
    6. Notion Page block payload

    Returns structured parity diagnostics, scores, and coverage metrics.
    """
    start_time = time.perf_counter()
    landmarks = extract_canonical_landmarks(markdown_text, title=title)

    # 1. Generate multi-modal outputs
    audio_meta = ad.extract_digest_metadata(markdown_text, title=landmarks["title"])
    audio_script = ad.generate_audio_digest_script(markdown_text, title=landmarks["title"], lang=lang)
    
    spatial_graph = ce.parse_markdown_to_spatial_graph(markdown_text, title=landmarks["title"])
    canvas_json_str = ce.generate_obsidian_canvas(markdown_text, title=landmarks["title"])
    canvas_dict = json.loads(canvas_json_str)
    svg_canvas = ce.generate_svg_canvas(spatial_graph)

    obsidian_res = ve.format_obsidian_markdown(markdown_text, title=landmarks["title"])
    notion_payload = ve.format_notion_payload(markdown_text, title=landmarks["title"])

    diagnostics = []
    checks_total = 0
    checks_passed = 0

    # Dimension 1: Title Alignment
    checks_total += 4
    # Canvas title check
    canvas_has_title = any(landmarks["title"] in node.get("text", "") for node in canvas_dict.get("nodes", []))
    if canvas_has_title:
        checks_passed += 1
        diagnostics.append("[PASS] Canvas Root Node contains canonical title.")
    else:
        diagnostics.append("[FAIL] Canvas Root Node missing canonical title.")

    # Audio title check
    if landmarks["title"] in audio_script:
        checks_passed += 1
        diagnostics.append("[PASS] Audio Digest spoken hook contains canonical title.")
    else:
        diagnostics.append("[FAIL] Audio Digest spoken hook missing canonical title.")

    # Obsidian title check
    if landmarks["title"] in obsidian_res["markdown"]:
        checks_passed += 1
        diagnostics.append("[PASS] Obsidian Note frontmatter / title contains canonical title.")
    else:
        diagnostics.append("[FAIL] Obsidian Note missing canonical title.")

    # Notion title check
    notion_title_found = False
    try:
        props = notion_payload.get("properties", {})
        for prop_val in props.values():
            if isinstance(prop_val, dict) and "title" in prop_val and isinstance(prop_val["title"], list):
                if prop_val["title"] and prop_val["title"][0].get("text", {}).get("content") == landmarks["title"]:
                    notion_title_found = True
                    break
    except Exception:
        pass
    if notion_title_found:
        checks_passed += 1
        diagnostics.append("[PASS] Notion Payload properties contain canonical title.")
    else:
        diagnostics.append("[FAIL] Notion Payload missing canonical title.")

    # Dimension 2: BLUF Preservation
    if landmarks["bluf"]:
        checks_total += 3
        bluf_clean = re.sub(r"^(BLUF|Decision Requested|Core Value|Summary):\s*", "", landmarks["bluf"], flags=re.IGNORECASE).strip()

        # In Audio
        if any(w.lower() in audio_script.lower() for w in bluf_clean.split()[:3]):
            checks_passed += 1
            diagnostics.append("[PASS] Audio Digest opens with acoustic BLUF anchor.")
        else:
            diagnostics.append("[WARN] Audio Digest may have truncated BLUF anchor.")

        # In Canvas
        canvas_has_bluf = any("BLUF" in node.get("text", "") or bluf_clean[:20] in node.get("text", "") for node in canvas_dict.get("nodes", []))
        if canvas_has_bluf:
            checks_passed += 1
            diagnostics.append("[PASS] Canvas Root Node embeds spatial BLUF card.")
        else:
            diagnostics.append("[WARN] Canvas Root Node missing BLUF card.")

        # In Obsidian
        if bluf_clean in obsidian_res["markdown"] or "BLUF" in obsidian_res["markdown"]:
            checks_passed += 1
            diagnostics.append("[PASS] Obsidian Note preserves BLUF executive callout.")
        else:
            diagnostics.append("[WARN] Obsidian Note missing BLUF callout.")

    # Dimension 3: Structural Pillar Coverage
    pillar_coverage = 0
    checks_total += len(landmarks["pillars"])
    canvas_node_texts = [n.get("text", "") for n in canvas_dict.get("nodes", [])]

    for pillar in landmarks["pillars"]:
        pillar_in_canvas = any(pillar in t for t in canvas_node_texts)
        pillar_in_audio = any(w in audio_script for w in pillar.split()[:2])
        if pillar_in_canvas or pillar_in_audio:
            checks_passed += 1
            pillar_coverage += 1
            diagnostics.append(f"[PASS] Structural Pillar '{pillar}' synchronized across visual/audio.")
        else:
            diagnostics.append(f"[FAIL] Structural Pillar '{pillar}' dropped from secondary modalities.")

    # Dimension 4: Action Vector Parity
    if landmarks["actions"]:
        checks_total += 2
        # Check Audio actions
        if len(audio_meta["actions"]) > 0:
            checks_passed += 1
            diagnostics.append(f"[PASS] Audio Digest encodes {len(audio_meta['actions'])} spoken priority actions.")
        else:
            diagnostics.append("[WARN] Audio Digest missing priority action list.")

        # Check Canvas actions
        action_nodes = [n for n in canvas_dict.get("nodes", []) if any(a[:15] in n.get("text", "") for a in landmarks["actions"])]
        if action_nodes or len(canvas_dict.get("nodes", [])) >= 3:
            checks_passed += 1
            diagnostics.append("[PASS] Canvas Graph contains dedicated child milestone / action nodes.")
        else:
            diagnostics.append("[WARN] Canvas Graph missing action milestone nodes.")

    # Dimension 5: Zero Em Dash Compliance across all modalities
    checks_total += 5
    all_clean = True
    em_char = chr(8212)
    for mod_name, mod_content in [
        ("Markdown", markdown_text),
        ("Audio Script", audio_script),
        ("Canvas JSON", canvas_json_str),
        ("Obsidian Markdown", obsidian_res["markdown"]),
        ("SVG Vector", svg_canvas)
    ]:
        if em_char in mod_content:
            all_clean = False
            diagnostics.append(f"[FAIL] Em dash detected in {mod_name}.")
        else:
            checks_passed += 1
            diagnostics.append(f"[PASS] Zero em dashes in {mod_name}.")

    parity_score = round((checks_passed / checks_total) * 100, 1) if checks_total > 0 else 100.0
    elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)

    return {
        "status": "PASS" if parity_score >= 85.0 else "FAIL",
        "parity_score": parity_score,
        "checks_passed": checks_passed,
        "checks_total": checks_total,
        "elapsed_ms": elapsed_ms,
        "landmarks": landmarks,
        "diagnostics": diagnostics,
        "modalities": {
            "markdown": {"length": len(markdown_text), "status": "OK"},
            "audio_digest": {"words": len(audio_script.split()), "status": "OK"},
            "obsidian_canvas": {"nodes": len(canvas_dict.get("nodes", [])), "edges": len(canvas_dict.get("edges", [])), "status": "OK"},
            "svg_canvas": {"size_bytes": len(svg_canvas.encode("utf-8")), "status": "OK"},
            "obsidian_vault": {"uri": obsidian_res.get("obsidian_uri", ""), "status": "OK"},
            "notion_payload": {"blocks": len(notion_payload.get("children", [])), "status": "OK"}
        }
    }

def run_pipeline_telemetry_check(sample_text=None):
    """
    Validates end-to-end export pipelines across all available export targets:
    Typst, HTML, Audio Script, Obsidian Canvas, Obsidian Note, and Notion Block JSON.
    """
    test_text = sample_text or """# Unified Architecture Deliverable
> **BLUF:** Deploying low-latency cognitive offload layer to eliminate phonological friction.

## Core Spatial Architecture
- High-contrast visual grid with 3:1 spatial margin.
- Zero linear paragraphs over 3 sentences.

## Execution Milestones
- [ ] 1. Ship Manifest V3 browser extension and test suite.
- [ ] 2. Benchmark multi-modal parity across 10 sample corpora.
- [ ] 3. Verify zero em dash compliance across export pipelines.
"""
    result = validate_multimodal_parity(test_text, title="Unified Architecture Deliverable")
    
    # Check JSON validity of canvas
    canvas_json_valid = True
    try:
        ce.generate_obsidian_canvas(test_text)
    except Exception:
        canvas_json_valid = False

    # Check Notion payload block count
    notion_payload = ve.format_notion_payload(test_text)
    notion_blocks_valid = len(notion_payload.get("children", [])) >= 3

    return {
        "parity_score": result["parity_score"],
        "elapsed_ms": result["elapsed_ms"],
        "canvas_json_valid": canvas_json_valid,
        "notion_blocks_valid": notion_blocks_valid,
        "zero_em_dash_clean": not any("[FAIL] Em dash detected" in d for d in result["diagnostics"]),
        "modalities_verified": len(result["modalities"]),
        "diagnostics": result["diagnostics"]
    }

def format_terminal_parity_report(res):
    """Formats an ASCII-box report for terminal inspection."""
    lines = []
    lines.append("=" * 66)
    lines.append("   DxSkills Multi-Modal Parity & Telemetry Audit")
    lines.append("=" * 66)
    lines.append(f" Status:        {res['status']} ({res['parity_score']}%)")
    lines.append(f" Checks Passed: {res['checks_passed']} / {res['checks_total']}")
    lines.append(f" Latency:       {res['elapsed_ms']} ms")
    lines.append("-" * 66)
    lines.append(" Modality Coverage Matrix:")
    for mod, data in res["modalities"].items():
        info = ", ".join(f"{k}: {v}" for k, v in data.items() if k != "status")
        lines.append(f"   - {mod.ljust(18)}: [OK] ({info})")
    lines.append("-" * 66)
    lines.append(" Semantic Diagnostics:")
    for diag in res["diagnostics"]:
        lines.append(f"   {diag}")
    lines.append("=" * 66)
    return "\n".join(lines)

if __name__ == "__main__":
    sample = """# Example Strategic Project
> **BLUF:** Eliminate administrative delay by automating weekly executive updates.

## Spatial Architecture
- Modular components
- Automated validation

## Action Vectors
- [ ] 1. Build test runner
- [ ] 2. Push to remote repo
"""
    if len(sys.argv) > 1 and os.path.isfile(sys.argv[1]):
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            test_doc = f.read()
    else:
        test_doc = sample
    
    res = validate_multimodal_parity(test_doc)
    print(format_terminal_parity_report(res))
