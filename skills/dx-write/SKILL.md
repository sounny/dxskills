---
name: dx-write
description: Voice preservation and silent mechanical polish. Corrects spelling, homophones, and syntax in the background while fiercely protecting authentic human warmth, directness, and cadence. Eliminates AI fluff and em dashes.
command: /dx write
version: 0.1.0
---

# `dx-write`: Voice & Silent Polish

The `dx-write` skill solves a persistent tension for dyslexic professionals: the fear of mechanical errors leading to over-edited, sterile, AI-sounding text. It provides reliable clerical perfection in the background while keeping the author's real human voice intact.

---

## ⚡ Core Operational Heuristics

1. **Silent Mechanical Polish:**
   - Quietly fix spelling, transposition errors, homophones (e.g., their/there, site/sight), and punctuation.
   - Never highlight, annotate, or list the mechanical fixes made.
   - Output the finished document cleanly and ready for delivery.

2. **Authentic Voice Preservation:**
   - **Tone:** Direct, grounded, warm, and collegial.
   - **Salutations:** Use natural, direct greetings (e.g., "[Name],") rather than rigid formulas ("Dear [Name],") unless formal protocol explicitly requires it.
   - **Cadence:** Keep sentence structures energetic and conversational.
   - **Closings:** Use clean, human sign-offs (e.g., "Best,", "Talk soon,").

3. **Strict Ban on AI Fluff & Jargon:**
   - Eliminate corporate filler: "I hope this email finds you well", "In today's fast-paced world", "delve", "testament", "beacon", "orchestrate", "leverage" (when used as a cliché).
   - **Zero Em Dashes:** Never generate em dashes (Unicode U+2014) anywhere. Use commas, hyphens, colons, or parentheses instead.

---

## 📋 Trigger & Usage

### Manual Trigger
- `/dx write <rough draft, bullet points, or instructions>`
- `"Polish this draft in my authentic voice: <text>"`

### Example Input
```text
Hey team just wanted to let you no that the draft paper is redy for reveiw. i added the new graphs on section 3. please take a look before wednesday noon so we can submit by thursday. thanks!
```

### Example Output
```text
Hi everyone,

The draft paper is ready for your review. I have added the updated charts to Section 3.

Please send over any feedback by Wednesday at noon so we can finalize everything ahead of Thursday's submission.

Best,
[Your Name]
```
