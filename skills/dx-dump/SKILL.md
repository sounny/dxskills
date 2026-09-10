---
name: dx-dump
description: Compiles unstructured brain dumps, rapid bullet fragments, voice transcripts, and phonetic shorthand into structured architectural outlines, decision tables, and actionable deliverables.
command: /dx dump
version: 0.1.0
---

# `dx-dump`: Brain Dump to Architecture

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

---

## 📋 Trigger & Usage

### Manual Trigger
- `/dx dump <raw text or audio transcript>`
- `"Compile this brain dump: <text>"`

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
