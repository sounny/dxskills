---
name: dx-read
version: 0.2.0
description: Anti-Wall-of-Text reading filter. Re-renders dense academic papers, policy documents, and long emails into visual signposts, decision matrices, and executive summaries.
triggers:
  commands:
    - "/dx read"
    - "/dx finance"
  natural_language:
    - "Distill this document"
    - "Summarize this paper into a decision matrix"
    - "Anti-wall-of-text this memo"
parameters:
  input:
    type: string
    description: Dense prose, long email thread, academic PDF text, or financial spreadsheet.
    required: true
  mode:
    type: string
    enum:
      - standard
      - finance
      - executive_briefing
    default: standard
    description: Distillation profile (standard decision matrix, conversational financial digest, or policy briefing book).
runtime_flags:
  silent_polish: true
  zero_em_dashes: true
  anti_wall_of_text: true
  max_paragraph_sentences: 3
output_contract:
  format: markdown
  required_elements:
    - "BLUF (Bottom Line Up Front) in 1-2 sentences"
    - "Categorized key takeaways with bold anchor prefixes"
    - "Structured decision matrix or trade-off table"
    - "Explicit deadlines and milestone constraints"
---

# `dx-read`: Anti-Wall-of-Text Filter

The `dx-read` skill eliminates reader fatigue and cognitive overload caused by uniform, dense blocks of text. It acts as an intake lens, compiling complex or lengthy prose into visually scannable structures.

---

## ⚡ Core Operational Heuristics

1. **Paragraph Quotas (Anti-Uniformity):**
   - Maximum paragraph length is 3 sentences.
   - Break every narrative block into visual anchors: bold topic prefixes, clean bullet lists, and spatial tables.
   - Always lead with a 1-2 sentence **Bottom Line Up Front (BLUF)**.

2. **Visual Hierarchy & Signposting:**
   - Use high-contrast bold lead-ins for every list item (e.g., `- **Key Decision:** ...`).
   - Group related points into distinct sections separated by visual dividers.
   - Extract numerical facts, dates, and requirements into Markdown tables rather than burying them in prose.

3. **Cognitive Distillation Levels:**
   - **Level 1 (BLUF):** What must the reader know in under 10 seconds?
   - **Level 2 (Decision & Impact Table):** What are the trade-offs, deadlines, and responsibilities?
   - **Level 3 (Nuance & Details):** High-signal context, preserved without filler words.

4. **Conversational Financial & Spreadsheet Digest (Richard Branson Archetype):**
   - Use `/dx finance` to translate rows of confusing balance sheets, budget spreadsheets, and financial reports into conversational narrative summaries and visual cash-flow diagrams.
   - Answers four fundamental questions: (1) Inflows, (2) Outflows, (3) Cash in register or runway, and (4) Key margin levers.

5. **Executive Briefing Books (Gavin Newsom Archetype):**
   - Converts 50-page policy briefs, committee memos, or legislative documents into high-contrast briefing books featuring color-coded concept blocks and relational decision matrices instead of pages of prose.

---

## 📋 Trigger & Usage

### Manual Triggers
- `/dx read <long text, URL, or document>`: General anti-wall-of-text filter.
- `/dx finance <spreadsheet dump, balance sheet, or financial report>`: Conversational financial summary and cash-flow diagram.

### Standard Output Format
> **BLUF:** [1-2 sentences capturing core conclusion and urgency]
>
> ### 1. Key Takeaways
> - **[Concept A]:** [Crisp 1-sentence summary]
> - **[Concept B]:** [Crisp 1-sentence summary]
>
> ### 2. Decision Matrix
> | Item / Option | Pros / Status | Cons / Risks | Action Required |
> | :--- | :--- | :--- | :--- |
> | ... | ... | ... | ... |
>
> ### 3. Immediate Constraints & Deadlines
> - **[Date/Time]:** [Specific milestone]
