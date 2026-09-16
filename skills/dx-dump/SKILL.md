---
name: dx-dump
version: 0.2.0
description: Compiles unstructured brain dumps, rapid bullet fragments, voice transcripts, and phonetic shorthand into structured architectural outlines, decision tables, and actionable deliverables.
triggers:
  commands:
    - "/dx dump"
    - "/dx napkin"
    - "/dx spec"
  natural_language:
    - "Compile this brain dump"
    - "Extract architecture from notes"
    - "Turn this brainstorm into an action plan"
parameters:
  input:
    type: string
    description: Raw unstructured text, bullet fragments, or transcribed voice notes.
    required: true
  mode:
    type: string
    enum:
      - standard
      - napkin
      - spec
    default: standard
    description: Compilation mode (standard operational, napkin business model, or executive spec).
runtime_flags:
  silent_polish: true
  zero_em_dashes: true
  anti_wall_of_text: true
output_contract:
  format: markdown
  required_elements:
    - "BLUF (Bottom Line Up Front) summary in 1-2 sentences"
    - "Categorized key components or immediate decisions"
    - "Operational table or Mermaid topology diagram"
    - "Concrete next actions with timelines or owners"
---

# `dx-dump`: Brain Dump to Architecture

> **Interactive Web Playground:** [https://dxskills.sounny.com](https://dxskills.sounny.com)

The `dx-dump` skill acts as an intelligent cognitive compiler for non-linear, spatial thinkers who ideate faster than linear keyboards allow. It ingests messy, disordered thought dumps and extracts the underlying architecture without demanding clean input.

---

## ⚡ Core Operational Heuristics

1. **Zero Input Tax (Phonetic & Shorthand Tolerance):**
   - Accept misspelled words, phonetically approximate terms, voice-to-text transcription artifacts, and incomplete bullet fragments without friction.
   - Never correct the user in conversation or ask them to clarify typos if the underlying intent can be deduced.
   - Assume technical or domain context based on surrounding terminology.

2. **Multi-Pass Cognitive Compilation:**
   - **Pass 1 (Intent & Fact Extraction):** Identify the core objective, explicit decisions made, constraints, and dependencies.
   - **Pass 2 (Spatial Topology):** Map out how the components fit together (e.g., inputs, engines, outputs, timelines).
   - **Pass 3 (Structural Formatting):** Render the output using clean visual hierarchies, bullet tiers, and tables.

3. **Standard Output Architecture:**
   Every output generated via `dx-dump` follows this clean visual structure:
   - **BLUF (Bottom Line Up Front):** 1-2 concise sentences summarizing the core takeaway.
   - **Key Components & Decisions:** Grouped categorically with bold lead-ins.
   - **Operational System Diagram / Table:** A concise Markdown table or Mermaid diagram mapping the moving parts.
   - **Actionable Next Steps:** Specific, concrete next moves tagged with owners or timelines.

4. **The Back-of-a-Beer-Mat / Napkin Test (Richard Branson Archetype):**
   - Use `/dx napkin` for radical simplification of business ideas, pitch notes, or product proposals.
   - Compresses sprawling concepts into a single-card view: Core Value Exchange, The 3 Key Levers, Back-of-the-Envelope Math, and Mermaid Flow.

5. **Executive Markdown Specs (Steve Jobs Archetype):**
   - Use `/dx spec` to transform disordered technical fragments, whiteboard notes, and engineering debates into an Executable Mermaid Architecture, Technical Tradeoff Matrix, and Distilled Action Plan.
   - Eliminates 40-page linear specification documents and endless email threads.

---

## 📋 Trigger & Usage

### Manual Triggers
- `/dx dump <raw text or audio transcript>`: Standard operational architecture compilation.
- `/dx napkin <business pitch, idea, or proposal>`: Branson single-card radical simplification.
- `/dx spec <engineering notes, whiteboard dump, or feature list>`: Jobs whole-system executive spec and tradeoff matrix.

### Example Input
```text
ok so we need to fix the data sync pipeline, currently failing when batch size > 500. also we need to update the client config on staging by friday. sarah said the auth token expires in 1hr so refresh logic is broken. lets push patch to staging first then verify before main prod deploy on tuesday
```

### Example Output
> **BLUF:** Resolve data sync pipeline crashes on batches > 500 and fix broken 1-hour auth token refresh logic on staging by Friday, ahead of Tuesday production release.
>
> ### 1. Immediate Issues Identified
> - **Batch Overflow:** Pipeline fails when batch size exceeds 500 records.
> - **Auth Token Expiry:** 1-hour token expiration breaks long-running sync routines.
>
> ### 2. Execution Schedule
> | Target | Deadline | Objective |
> | :--- | :--- | :--- |
> | **Staging Environment** | Friday | Deploy pipeline batch patch and refresh logic fix; update client config. |
> | **Production Environment** | Tuesday | Verify staging stability, then execute main production deployment. |
>
> ### 3. Action Items
> 1. Implement batch chunking limit (<= 250 records per payload).
> 2. Patch auth token refresh loop before staging release.
> 3. Verify client staging config prior to Friday verification.
