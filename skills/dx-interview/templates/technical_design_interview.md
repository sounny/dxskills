# Socratic Interview Template: Technical Design Document (RFC)
# Used by: dx-interview (/dx ask rfc)

## Phase 1: Interactive Question Wave
Ask these 4 targeted questions to the engineer or architect:

1. **The System Objective:** In 1 sentence, what business problem or architectural limitation are we solving?
2. **The Hard Constraints:** What are the non-negotiables (e.g., latency under 50ms, backward compatibility, zero downtime, budget)?
3. **The Proposed Solution:** Walk through the proposed data flow or technical architecture in rough terms.
4. **The Considered Alternatives:** What other approaches did you discard, and what was the disqualifying flaw?

---

## Phase 2: Compiler Synthesis Template
Compile the response into this engineering RFC structure:

```markdown
# RFC: [System Feature / Architectural Change]

> **Status:** Draft | **Author:** [Name] | **Date:** [Date]
> **BLUF:** [1-2 sentences summarizing proposed architecture and impact]

---

## 1. Context & Motivation
- **Current State Limitations:** [Synthesized from Question 1]
- **Target Metrics:** [Latency, throughput, availability goals from Question 2]

## 2. Proposed Architecture & Data Flow
[Insert Mermaid diagram synthesized from Question 3]

| Component | Responsibility | Tech Stack | Failure Mode |
| :--- | :--- | :--- | :--- |
| ... | ... | ... | ... |

## 3. Evaluated Alternatives
| Alternative | Key Advantage | Reason Rejected |
| :--- | :--- | :--- |
| ... | ... | [From Question 4] |

## 4. Rollout & Migration Strategy
- **Phase 1 (Canary):** Deploy to 5% of traffic with active error budgeting.
- **Phase 2 (Gradual Ramp):** Expand to 50% after 24h stability verification.
- **Phase 3 (Full Cutover):** Decommission legacy service.
```
