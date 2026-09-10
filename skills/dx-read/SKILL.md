---
name: dx-read
description: Anti-Wall-of-Text reading filter. Re-renders dense academic papers, policy documents, and long emails into visual signposts, decision matrices, and executive summaries.
command: /dx read
version: 0.1.0
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

---

## 📋 Trigger & Usage

### Manual Trigger
- `/dx read <long text, URL, or document>`
- `"Filter this wall of text: <text>"`

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
