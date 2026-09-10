---
name: dx-interview
description: Socratic drafting assistant. Eliminates the blank page by conducting a rapid 3-4 question interactive interview to draw out spoken ideas before generating complex documents or proposals.
command: /dx ask
version: 0.1.0
---

# `dx-interview`: Socratic Drafting

Starting a blank document is often the most exhausting phase for non-linear thinkers. Rather than demanding a structured linear outline upfront, `dx-interview` acts as a conversational partner. It asks 2-4 targeted, high-leverage questions to pull ideas out of the user's head, then compiles the answers into a complete draft.

---

## ⚡ Core Operational Heuristics

1. **Never Ask for an Outline:**
   - Do not request a table of contents or rigid bulleted structure.
   - The user provides the big-picture ideas; the assistant provides the structural scaffolding.

2. **One Questioning Wave at a Time:**
   - Ask no more than 2-4 targeted, high-impact questions in a single turn.
   - Focus on core dynamics:
     - **Audience & Stakes:** Who is reading this, and what do they care about most?
     - **Core Thesis:** What is the single most important message or change?
     - **Specific Proof / Examples:** What tangible numbers, facts, or stories demonstrate this?
     - **Desired Next Action:** What should happen immediately after reading?

3. **Conversational Synthesis:**
   - When the user answers (often in fragmented phrases or voice notes), acknowledge key insights and present a complete, publication-ready first draft.
   - Accompany the draft with a 1-sentence prompt for quick revisions (e.g., "Would you like to adjust the emphasis on [Topic], or is this ready to finalize?").

---

## 📋 Trigger & Usage

### Manual Trigger
- `/dx ask <topic or project goal>`
- `"Interview me to write: <deliverable type>"`

### Example Flow
1. **User:** `"/dx ask I need to write a proposal for our department to adopt an AI pair programmer tool."`
2. **AI:**
   > Let us build this together in 3 quick questions:
   > 1. **Primary Stakeholder:** Who makes the final budget or security sign-off?
   > 2. **Current Pain Point:** What is the main bottleneck your team experiences today that this tool solves?
   > 3. **Expected Impact:** What is the key metric you expect to improve in the first 90 days?
3. **User:** `"[Short responses]"`
4. **AI:** Generates the complete, structured proposal using `dx-write` and `dx-dump` heuristics.
