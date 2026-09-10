# Cognitive Dump Template: Academic Peer-Review Rebuttal Matrix
# Used by: dx-dump (/dx dump rebuttal)

## Operational Objective
Converts dense, emotionally exhausting peer review comments and messy reviewer feedback into an organized, point-by-point defense matrix and revision roadmap.

---

## Standard Compilation Output

```markdown
# Peer Review Response Matrix: [Manuscript Title / ID]

> **BLUF:** Addressed all [Number] reviewer comments across [Number] major themes: [Theme 1], [Theme 2], and [Theme 3]. Added [X] new figures, [Y] comparative baselines, and rewritten Section [Z] for clarity.

---

## 1. Reviewer Comment & Action Matrix

| Rev # | Item # | Core Concern Category | Action Taken | Manuscript Impact |
| :--- | :--- | :--- | :--- | :--- |
| R1 | 1.1 | Methodological Rigor | Incorporated 5-fold cross-validation baseline | Section 3.2, Table 2 |
| R1 | 1.2 | Literature Context | Cited recent 2025/2026 foundational literature | Section 2.1, References |
| R2 | 2.1 | Data Representation | Added high-contrast vector workflow diagram | Figure 4 |
| R2 | 2.2 | Limitations Discussion | Explicitly documented compute and edge constraints | Section 5.3 |
| R3 | 3.1 | Statistical Significance | Added p-values and confidence intervals to chart | Figure 6, Table 4 |

---

## 2. Point-by-Point Rebuttal Breakdown

### Reviewer 1

#### Comment 1.1 (Methodology)
> "[Insert raw reviewer comment here]"

- **Response:** We thank the reviewer for this constructive insight. We agree that validating across multiple splits strengthens the generalizability of our findings. We have performed 5-fold cross-validation across the entire benchmark dataset.
- **Changes in Manuscript:** Updated Section 3.2 (lines 142-168) and added Table 2 detailing split metrics.

#### Comment 1.2 (Literature Context)
> "[Insert raw reviewer comment here]"

- **Response:** We appreciate the recommendation to contextualize our framework within recent advances. We have expanded our review to include these pivotal works.
- **Changes in Manuscript:** Revised Section 2.1 (lines 58-74) with 6 additional citations.

---

### Reviewer 2

#### Comment 2.1 (Clarity & Visual Presentation)
> "[Insert raw reviewer comment here]"

- **Response:** We agree that the operational workflow requires visual clarity. We have redesigned the system architecture into a clear, stepped visual diagram.
- **Changes in Manuscript:** Inserted new Figure 4 and revised accompanying caption in Section 4.1.

---

## 3. Revised Manuscript Revision Checklist
- [ ] All new citations compiled in `.bib` file.
- [ ] All diffs tracked with `latexdiff` or Word Track Changes.
- [ ] Zero em dashes verified across revised text.
- [ ] Cover letter updated for handling editor.
```
