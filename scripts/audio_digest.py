#!/usr/bin/env python3
"""
DxSkills Audio Digest Synthesizer & Spoken Voice Overview
Converts dense structured specifications, executive briefings, and pitch decks into
phonetically optimized audio digests (60 to 90 seconds) for auditory-first comprehension.

Cognitive Principle:
Auditory pre-exposure reduces visual phonological crowding and working memory exhaustion
by establishing spatial anchors before deep reading.

Strict Rule: NO em dashes anywhere (use hyphens, commas, or parentheses).
"""

import os
import re
import sys
import subprocess
import shutil

def extract_digest_metadata(markdown_text, title=None):
    """Extracts title, BLUF/decision, key sections, and actions from markdown."""
    lines = [l.strip() for l in markdown_text.strip().splitlines() if l.strip()]
    
    extracted_title = title or "Deliverable Overview"
    bluf = ""
    headings = []
    actions = []
    
    for line in lines:
        if not title and line.startswith("# ") and extracted_title == "Deliverable Overview":
            extracted_title = line.lstrip("# ").strip()
        elif line.startswith("> ") and not bluf:
            clean_q = line.lstrip("> ").strip()
            if any(k in clean_q for k in ["BLUF", "Decision Requested", "Core Value", "Primary Learning", "Summary"]):
                bluf = clean_q.replace("**", "").replace("*", "")
        elif line.startswith("## "):
            headings.append(line.lstrip("## ").strip())
        elif re.match(r"^\d+\.\s", line) or line.startswith("- [ ]") or line.startswith("- "):
            clean_item = re.sub(r"^\d+\.\s+", "", line).replace("- [ ]", "").lstrip("-* ").strip()
            if len(clean_item) > 5 and len(actions) < 4:
                actions.append(clean_item)
                
    return {
        "title": extracted_title,
        "bluf": bluf,
        "headings": headings[:4],
        "actions": actions[:3]
    }

def generate_audio_digest_script(markdown_text, title=None, lang="en"):
    """
    Formats an acoustic-optimized speech script with natural cadence and spoken cues.
    Languages supported: English ('en') and French ('fr').
    """
    meta = extract_digest_metadata(markdown_text, title=title)
    
    if lang == "fr":
        # French spoken script
        parts = [
            f"Synthese audio DxSkills: {meta['title']}.",
            "Pause de cadrage."
        ]
        if meta["bluf"]:
            parts.append(f"Point essentiel: {meta['bluf']}.")
        if meta["headings"]:
            sections_str = ", ".join(meta["headings"])
            parts.append(f"Les themes cles abordes sont: {sections_str}.")
        if meta["actions"]:
            parts.append("Prochaines etapes prioritaires:")
            for idx, act in enumerate(meta["actions"], 1):
                parts.append(f"Numero {idx}: {act}.")
        parts.append("Fin de la synthese audio. Vous pouvez consulter les details dans le document complet.")
    else:
        # English spoken script
        parts = [
            f"DxSkills audio overview: {meta['title']}.",
            "Acoustic anchor engaged."
        ]
        if meta["bluf"]:
            parts.append(f"Bottom line up front: {meta['bluf']}.")
        if meta["headings"]:
            sections_str = ", ".join(meta["headings"])
            parts.append(f"The core areas covered are: {sections_str}.")
        if meta["actions"]:
            parts.append("Immediate priority actions:")
            for idx, act in enumerate(meta["actions"], 1):
                parts.append(f"Step {idx}: {act}.")
        parts.append("End of audio overview. Detailed specification is available for visual inspection.")

    return "\n\n".join(parts)

def synthesize_audio_file(script_text, output_path, lang="en"):
    """
    Synthesizes speech audio from script using local OS engines:
    - Windows: PowerShell System.Speech.Synthesis.SpeechSynthesizer
    - macOS: 'say' command with afconvert
    - Linux: 'espeak' or 'spd-say' fallback
    Returns True if audio file was successfully generated.
    """
    output_path = os.path.abspath(output_path)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Clean text of any problematic quotes for shell synthesis
    safe_text = script_text.replace('"', '""').replace('`', '')
    
    if sys.platform == "win32":
        ps_script = f"""
        Add-Type -AssemblyName System.Speech;
        $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer;
        $synth.Rate = 1;
        $synth.SetOutputToWaveFile("{output_path}");
        $synth.Speak(@'
{script_text}
'@);
        $synth.Dispose();
        """
        try:
            res = subprocess.run(
                ["powershell", "-NoProfile", "-Command", ps_script],
                capture_output=True,
                text=True,
                check=True
            )
            return os.path.isfile(output_path) and os.path.getsize(output_path) > 0
        except Exception as e:
            sys.stderr.write(f"[DxSkills Audio Error] Windows synthesis failed: {e}\n")
            return False

    elif sys.platform == "darwin":
        try:
            subprocess.run(["say", "-o", output_path, script_text], check=True)
            return os.path.isfile(output_path) and os.path.getsize(output_path) > 0
        except Exception as e:
            sys.stderr.write(f"[DxSkills Audio Error] macOS synthesis failed: {e}\n")
            return False

    else:
        # Linux fallback using espeak if installed
        if shutil.which("espeak"):
            try:
                subprocess.run(["espeak", "-w", output_path, script_text], check=True)
                return os.path.isfile(output_path) and os.path.getsize(output_path) > 0
            except Exception as e:
                sys.stderr.write(f"[DxSkills Audio Error] Linux espeak failed: {e}\n")
                return False
        else:
            sys.stderr.write("[DxSkills Audio Notice] No local Linux TTS engine found (install espeak).\n")
            return False

if __name__ == "__main__":
    sample = (
        "# Cloud Migration Strategy\n"
        "> **BLUF:** Migrate production database to multi-region cluster by Friday.\n\n"
        "## Infrastructure Architecture\n"
        "Active-passive failover with automatic replication.\n\n"
        "## Security Matrix\n"
        "End-to-end encryption at rest and in transit.\n\n"
        "## Next Steps\n"
        "1. Provision staging environment\n"
        "2. Execute mock cutover drill\n"
        "3. Verify telemetry streams\n"
    )
    script = generate_audio_digest_script(sample, title="Cloud Migration")
    print("=== Audio Digest Script ===")
    print(script)
