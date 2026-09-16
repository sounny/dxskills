---
name: dx-voice
version: 0.2.0
description: Speech-to-Architecture pipeline. Converts raw audio dictation, meeting recordings, and voice memos directly into structured Markdown deliverables using local Whisper transcription and cognitive compilation.
triggers:
  commands:
    - "/dx voice"
  natural_language:
    - "Transcribe and structure this audio"
    - "Turn this voice memo into a project plan"
    - "Compile speech dictation into a document"
parameters:
  input:
    type: string
    description: Audio file path (.mp3, .wav, .m4a, .ogg) or raw transcribed text (.srt, .vtt, .txt).
    required: true
  target_format:
    type: string
    enum:
      - auto
      - proposal
      - spec
      - email
      - storyboard
    default: auto
    description: Target deliverable structure.
runtime_flags:
  silent_polish: true
  zero_em_dashes: true
  phonetic_normalization: true
  strip_disfluencies: true
output_contract:
  format: markdown
  required_elements:
    - "Stripped speech disfluencies (um, uh, like, you know)"
    - "Phonetic correction of spatial and technical jargon"
    - "Direct mapping into structured Markdown architecture or email"
    - "Zero em dashes throughout the output"
---

# `dx-voice`: Speech-to-Architecture

Voice dictation is the natural high-bandwidth input channel for non-linear thinkers. Speech completely bypasses the fine motor and orthographic bottlenecks of keyboards. The `dx-voice` skill takes raw audio files or speech transcripts and directly compiles them into structured, publication-ready Markdown deliverables.

---

## ⚡ Core Operational Heuristics

1. **Transcript Cleansing & Filler Stripping:**
   - Automatically strip out disfluencies: "um", "uh", "you know", "like", "so basically", and repetitive restarts.
   - Reconnect fragmented sentences broken by pauses or thinking breaths.
   - Never lose domain terminology, numbers, or technical keywords.

2. **Phonetic & Homophone Normalization:**
   - Apply phoneme correction heuristics to capture transcribed domain jargon accurately (e.g., converting "coral pleth" to "choropleth", "ice a crone" to "isochrone", and "light are" to "LiDAR").
   - Silently resolve phonetic ambiguities based on conversational context.

3. **Autonomous Deliverable Selection:**
   - Detects the intent of the speech automatically:
     - If describing a workflow or system architecture: generates an executable Mermaid flowchart (`dx-map` or `dx spec`).
     - If drafting a message: outputs a polished email in authentic voice (`dx-write`).
     - If discussing tasks: generates an action item matrix (`dx-dump`).
     - If an unscripted speech or presentation: generates a visual spatial storyboard (`dx storyboard`).

4. **The 2-Minute Voice Stream Pipeline (Richard Branson Archetype):**
   - Ingests chaotic 2-minute voice dictations or fragmented voice memos.
   - Filters out conversational disfluencies and clutter while strictly preserving facts and momentum.
   - Compiles the stream into a clean Mermaid system map, an executive brief, and concrete next actions with zero shorthand tax.

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
