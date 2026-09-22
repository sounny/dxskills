---
name: dx-plan
version: 0.2.0
description: Turns a fuzzy goal, deadline, or scattered task dump into an ordered, time-blocked execution checklist that supports task initiation, working memory, and executive function for non-linear and dyslexic thinkers.
triggers:
  commands:
    - "/dx plan"
    - "/dx checklist"
    - "/dx timeblock"
  natural_language:
    - "Break this goal into steps"
    - "Turn this into a checklist"
    - "Help me plan my day"
    - "What do I do first"
parameters:
  input:
    type: string
    description: A goal, deadline, or unordered list of tasks in raw, phonetic, or shorthand form.
    required: true
  horizon:
    type: string
    enum:
      - day
      - week
      - project
    default: day
    description: Planning horizon (single day, one week, or a multi-step project).
runtime_flags:
  silent_polish: true
  zero_em_dashes: true
  anti_wall_of_text: true
output_contract:
  format: markdown
  required_elements:
    - "BLUF (Bottom Line Up Front) restating the goal in 1-2 sentences"
    - "A single, unambiguous first physical action to defeat task-initiation friction"
    - "An ordered, numbered checklist of steps with checkboxes"
    - "A time-blocked table with focus-block estimates and energy tags"
---

# `dx-plan`: Goal to Ordered Execution Checklist

> **Interactive Web Playground:** [https://dxskills.sounny.com](https://dxskills.sounny.com)

The `dx-plan` skill closes the gap between intention and action. Non-linear and dyslexic thinkers often hold a rich, complete plan in their heads but stall at sequencing it and starting the first step. This skill converts a fuzzy goal or scattered task dump into a single, ordered, time-blocked checklist so the next physical action is always obvious.

---

## ⚡ Core Operational Heuristics

1. **Zero Input Tax (Shorthand & Phonetic Tolerance):**
   - Accept unordered fragments, voice-to-text artifacts, and phonetic spelling without friction.
   - Never ask the user to reformat or clarify spelling if the intent can be deduced.

2. **Defeat Task-Initiation Friction (The 2-Minute Start):**
   - Always surface one unambiguous first physical action at the top of the plan.
   - Shrink that action to a 2-minute version so starting feels trivial (for example, "Open the doc and write the title").

3. **Sequence, Do Not Just List:**
   - Order steps by dependency first, then by effort, so nothing is blocked by a later step.
   - Group tightly related steps so working memory holds one cluster at a time, not a long flat list.

4. **Time-Block With Honest Energy Tags:**
   - Assign each step a focus-block estimate (short 15 min, standard 25 min, or deep 45 min).
   - Tag each block with the energy it needs (High, Medium, Low) so the user can match work to their state.

5. **Standard Output Architecture:**
   Every `dx-plan` output follows this structure:
   - **BLUF:** 1-2 sentences restating the goal and the deadline.
   - **Start Here:** the single first physical action, in its 2-minute form.
   - **Ordered Checklist:** numbered steps with `[ ]` checkboxes.
   - **Time-Block Schedule:** a table of Step, Focus Block, Energy, and Done.

---

## 📋 Trigger & Usage

### Manual Triggers
- `/dx plan <goal or task dump>`: Order a goal into a checklist for a single day.
- `/dx checklist <task dump>`: Emphasize the numbered, checkbox execution list.
- `/dx timeblock <task dump>`: Emphasize the focus-block schedule for the week.

### Example Input
```text
need to submit the grant by thursday. still havent finished the budget section. sarah has to review the methods. also need to email the letters of support ppl. and the abstract is too long
```

### Example Output
> **BLUF:** Submit the grant by Thursday. Four steps remain, with the budget and Sarah's methods review on the critical path.
>
> ### Start Here (2-minute version)
> Open the grant document and trim the abstract to the word limit. Just delete the first filler sentence to begin.
>
> ### Ordered Checklist
> 1. [ ] Trim the abstract to the word limit.
> 2. [ ] Finish the budget section.
> 3. [ ] Send the methods section to Sarah for review.
> 4. [ ] Email the letters-of-support contacts.
>
> ### Time-Block Schedule
> | Step | Focus Block | Energy | Done |
> | :--- | :--- | :--- | :--- |
> | Trim the abstract | 15 min | Low | [ ] |
> | Finish the budget section | 45 min | High | [ ] |
> | Send methods to Sarah | 15 min | Low | [ ] |
> | Email support contacts | 25 min | Medium | [ ] |
