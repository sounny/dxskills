#!/usr/bin/env python3
"""
DxSkills Voice Ingestion & Transcription Pipeline
Transcribes raw voice memos using faster-whisper (or whisper CLI),
cleans speech disfluencies, and compiles directly into D-Mode visual architecture.
"""

import os
import sys
import re
import argparse

DISFLUENCIES = [
    r"\bum\b", r"\buh\b", r"\byou know\b", r"\blike\b", r"\bso basically\b",
    r"\bah\b", r"\ber\b", r"\bI mean\b", r"\bkind of\b", r"\bsort of\b"
]

def clean_speech_transcript(text):
    cleaned = text
    for pattern in DISFLUENCIES:
        cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)
    
    # Remove duplicate spaces and clean punctuation gaps
    cleaned = re.sub(r"\s+", " ", cleaned)
    cleaned = re.sub(r"\s+([.,?!])", r"\1", cleaned).strip()
    
    # Strictly remove em dashes
    cleaned = cleaned.replace("\u2014", " - ")
    return cleaned

def transcribe_audio_faster_whisper(audio_path, model_size="base.en"):
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print("[DxSkills Voice] faster-whisper not installed.")
        print("To enable on-device transcription, run: pip install faster-whisper")
        return None

    print(f"[DxSkills Voice] Loading faster-whisper model ({model_size})...")
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    
    print(f"[DxSkills Voice] Transcribing: {audio_path}")
    segments, info = model.transcribe(audio_path, beam_size=5)
    
    transcript_chunks = []
    for segment in segments:
        transcript_chunks.append(segment.text.strip())
        
    return " ".join(transcript_chunks)

def compile_to_d_mode(transcript):
    cleaned = clean_speech_transcript(transcript)
    if not cleaned:
        return "No speech detected in input audio."

    sentences = [s.strip() for s in cleaned.split(".") if s.strip()]
    if not sentences:
        sentences = [cleaned]

    bluf = sentences[0]
    if not bluf.endswith("."):
        bluf += "."
    bluf = bluf[0].upper() + bluf[1:]

    rows = []
    remaining = sentences[1:]
    if not remaining:
        rows.append(("Primary Objective", "Active", bluf))
    else:
        for idx, s in enumerate(remaining, 1):
            s_low = s.lower()
            if any(k in s_low for k in ["deadline", "friday", "month", "sync", "call", "schedule"]):
                item = "Timeline / Alignment"
                status = "Scheduled"
            elif any(k in s_low for k in ["package", "runway", "work", "budget", "deliverable"]):
                item = "Deliverable Scope"
                status = "In Progress"
            else:
                item = f"Milestone {idx}"
                status = "Active"
            rows.append((item, status, s))

    md = []
    md.append(f"> **BLUF:** {bluf}")
    md.append("")
    md.append("| Deliverable | Timeline / Status | Action Item |")
    md.append("| :--- | :--- | :--- |")
    for item, status, action in rows:
        md.append(f"| {item} | {status} | {action} |")
    md.append("")
    md.append("### Refined Action Draft")
    md.append("")
    md.append("Team,")
    md.append("")
    md.append(bluf)
    md.append("")
    for item, _, action in rows:
        md.append(f"- **{item}:** {action}")
    md.append("")
    md.append("Let me know if anything is blocked.")

    result = "\n".join(md).replace("\u2014", " - ")
    return result

def main():
    parser = argparse.ArgumentParser(description="DxSkills Voice-to-Architecture Compiler")
    parser.add_argument("--input", "-i", type=str, required=True, help="Path to audio file (.mp3, .wav, .m4a) or text transcript")
    parser.add_argument("--model", "-m", type=str, default="base.en", help="faster-whisper model size")
    parser.add_argument("--output", "-o", type=str, default=None, help="Path to write compiled markdown")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: Input file not found: {args.input}")
        sys.exit(1)

    raw_transcript = ""
    ext = os.path.splitext(args.input)[1].lower()
    
    if ext in [".txt", ".vtt", ".srt", ".md"]:
        with open(args.input, "r", encoding="utf-8") as f:
            raw_transcript = f.read()
    else:
        # Audio file
        raw_transcript = transcribe_audio_faster_whisper(args.input, model_size=args.model)
        if not raw_transcript:
            print("[DxSkills Voice] Fallback: Please provide transcript as .txt file if whisper is not installed.")
            sys.exit(1)

    print("[DxSkills Voice] Ingested speech. Compiling D-Mode architecture...")
    compiled_output = compile_to_d_mode(raw_transcript)
    
    print("\n--- Compiled D-Mode Output ---\n")
    print(compiled_output)
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(compiled_output)
        print(f"\n[DxSkills Voice] Saved architecture to: {args.output}")

if __name__ == "__main__":
    main()
