# Cognitive Intake Template: Academic Paper Distillation
# Used by: dx-read (/dx read paper)

## Operational Objective
Transforms 20 to 50 page dense scholarly papers into a scannable 2-page cognitive digest without losing theoretical rigor or empirical nuance.

---

## Standard Output Format

```markdown
# Paper Digest: [Full Title of Paper]

> **Authors:** [Author List] | **Journal / Conference:** [Venue, Year]
> **DOI / Link:** [URL or DOI]
> **BLUF:** [2-sentence core finding and why it matters to the field]

---

## 1. The Core Empirical Claim
- **Primary Hypothesis:** [What the authors set out to test]
- **Key Result:** [What the data actually demonstrated]
- **Magnitude of Effect:** [Exact percentages, p-values, or benchmarks]

## 2. Methodology & Evidence Matrix
| Component | Implementation Details | Critical Assumptions / Biases |
| :--- | :--- | :--- |
| **Dataset / Sample** | [Sample size, demographic, geographic boundaries] | [Potential selection bias] |
| **Model / Intervention** | [Architecture, statistical method, control group] | [Confounding variables] |
| **Evaluation Metric** | [Primary loss, accuracy, F1, qualitative rubric] | [Limitations of metric] |

## 3. Visual System Summary
[Mermaid diagram mapping the conceptual causal model or experimental pipeline]

## 4. Practical Takeaways & Open Questions
- **How to apply this today:** [Concrete takeaway for practitioners]
- **Unaddressed gaps:** [What the paper leaves unanswered]
```
