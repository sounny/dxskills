---
name: dx-write
version: 0.2.0
description: Voice preservation and silent mechanical polish. Corrects spelling, homophones, and syntax in the background while fiercely protecting authentic human warmth, directness, and cadence. Eliminates AI fluff and em dashes.
triggers:
  commands:
    - "/dx write"
  natural_language:
    - "Polish this draft"
    - "Clean up my dictation"
    - "Fix errors without making it sound like an AI"
parameters:
  input:
    type: string
    description: Rough notes, unpunctuated voice dictation, or draft email.
    required: true
  context:
    type: string
    enum:
      - email
      - memo
      - documentation
      - message
    default: email
    description: Target communication channel.
runtime_flags:
  silent_polish: true
  zero_em_dashes: true
  preserve_voice: true
  no_artificial_lists: true
  max_paragraph_sentences: 3
output_contract:
  format: text
  required_elements:
    - "Silent mechanical correction of typos and homophones"
    - "Preservation of human tone and colloquial warmth"
    - "Natural paragraph breaks with zero forced bullet outlines for correspondence"
    - "Zero em dashes and zero robotic filler phrases"
---

# `dx-write`: Voice & Silent Polish

The `dx-write` skill solves a persistent tension for dyslexic professionals: the fear of mechanical errors leading to over-edited, sterile, AI-sounding text. It provides reliable clerical perfection in the background while keeping the author's real human voice intact.

---

## ⚡ Core Operational Heuristics

1. **Silent Mechanical Polish:**
   - Quietly fix spelling, transposition errors, homophones (e.g., their/there, site/sight), and punctuation.
   - Never highlight, annotate, or list the mechanical fixes made.
   - Output the finished document cleanly and ready for delivery.

2. **Embedded Phonetic & Homophone Correction Table:**
   When ingesting voice dictation or rapid typing, automatically map phonetic speech-to-text approximations and dyslexic slips to their intended canonical terms:

   | Phonetic / Dictation Slip | Canonical Term | Domain Context |
   | :--- | :--- | :--- |
   | `coral pleth`, `chora pleth` | `choropleth` | Spatial analysis / Thematic mapping |
   | `ice a crone`, `iso crone` | `isochrone` | Spatial travel-time analysis |
   | `light are`, `lie dar` | `LiDAR` | Remote sensing / Elevation data |
   | `rest or`, `rass ter` | `raster` | Grid/pixel spatial datasets |
   | `jew reference`, `geo reference` | `georeference` | Coordinate system alignment |
   | `ortho photo`, `author photo` | `orthophoto` | Aerial orthorectified imagery |
   | `special join`, `spatial joyn` | `spatial join` | GIS attribute joins by geometry |
   | `top ology`, `toe pology` | `topology` | Geometric adjacency rules |
   | `day tum`, `date um` | `datum` | Geodetic reference frame |
   | `poly gone`, `poly gan` | `polygon` | Vector geometry boundary |
   | `site` (when referencing vision) | `sight` | Common homophone slip |
   | `cite` (when referencing location) | `site` | Common homophone slip |
   | `affect` (as noun) / `effect` (as verb) | Context-corrected | Grammatical homophone slip |
   | `lead` (past tense) | `led` | Irregular phonetic spelling |
   | `discreet` (separate/distinct) | `discrete` | Technical precision slip |

3. **Authentic Voice Preservation:**
   - **Tone:** Direct, grounded, warm, and collegial.
   - **Salutations:** Use natural, direct greetings (e.g., "[Name],") rather than rigid formulas ("Dear [Name],") unless formal protocol explicitly requires it.
   - **Cadence:** Keep sentence structures energetic and conversational.
   - **Closings:** Use clean, human sign-offs (e.g., "Best,", "Talk soon,").

4. **Strict Ban on AI Fluff & Jargon:**
   - Eliminate corporate filler: "I hope this email finds you well", "In today's fast-paced world", "delve", "testament", "beacon", "orchestrate", "leverage" (when used as a cliché).
   - **Zero Em Dashes:** Never generate em dashes (Unicode U+2014) anywhere. Use commas, hyphens, colons, or parentheses instead.

5. **Natural Paragraphs Over Forced Lists & Bullets:**
   - **No Artificial Lists:** NEVER convert natural human prose, discussion board replies, emails, peer feedback, or conversational messages into bulleted lists, bold topic prefixes, or slide-deck outlines.
   - **Anti-Wall-of-Text for Prose:** Use short, scannable paragraphs (1 to 3 sentences maximum) separated by clean paragraph breaks. Whitespace provides visual breathing room and reduces visual crowding without stripping away human warmth or sounding like an AI outline.
   - **Authentic Conversational Voice:** Dyslexic professionals often excel in direct narrative momentum, authentic warmth, and big-picture clarity. Communicate like a genuine person in natural conversational flow, not an automated summary or corporate slide deck. Reserve bullet points and tables strictly for technical documentation, step-by-step checklists, or multi-option trade-off evaluations where explicitly requested.

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
