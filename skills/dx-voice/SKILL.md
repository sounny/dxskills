---
name: dx-voice
description: Speech-to-Architecture pipeline. Converts raw audio dictation, meeting recordings, and voice memos directly into structured Markdown deliverables using local Whisper transcription and cognitive compilation.
command: /dx voice
version: 0.1.0
---

# `dx-voice`: Speech-to-Architecture

Voice dictation is the natural high-bandwidth input channel for non-linear thinkers. Speech completely bypasses the fine motor and orthographic bottlenecks of keyboards. The `dx-voice` skill takes raw audio files or speech transcripts and directly compiles them into structured, publication-ready Markdown deliverables.

---

## ⚡ Core Operational Heuristics

1. **Transcript Cleansing & Filler Stripping:**
   - Automatically strip out disfluencies: "um", "uh", "you know", "like", "so basically", and repetitive restarts.
   - Reconnect fragmented sentences broken by pauses or thinking breaths.
   - Never lose domain terminology, numbers, or technical keywords.

2. **Integration with Local Transcribers:**
   - Integrates seamlessly with local transcription tools (e.g., `faster-whisper`, OpenAI Whisper, Apple Dictation).
   - Ingests audio formats (`.mp3`, `.wav`, `.m4a`, `.ogg`) or raw transcript files (`.vtt`, `.srt`, `.txt`).

3. **Autonomous Deliverable Selection:**
   - Detects the intent of the speech automatically:
     - If describing a workflow: generates a Mermaid flowchart (`dx-map`).
     - If drafting a message: outputs a polished email in authentic voice (`dx-write`).
     - If discussing tasks: generates an action item matrix (`dx-dump`).

---

## 📋 Trigger & Usage

### Manual Trigger
- `/dx voice <audio file or transcript path>`
- `"Compile this voice memo into a proposal: <file>"`

### Example Command Flow
```bash
# Transcribe raw audio using local whisper, then compile via dx-voice
python scripts/dx_cli.py voice --input memo_0910.m4a --type proposal
```
