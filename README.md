# Single Model, Zero Variance: The Activation Gap

**Zero recall variance: the same 6 bugs surfaced on every one of 18 independent runs. (This is a recall-stability claim, not a claim that all model outputs are deterministic.)**

---

## Abstract

This repository documents the discovery of the **Activation Gap** — the measurable divergence in model performance when asked to solve complex, multi-variable problems (like full-codebase auditing) in a single pass.

The core findings show that **single-model recursion produces massive variance**, but **themed cognitive splitting** can eliminate it entirely. By splitting a single audit into independent, themed observation paths, we can achieve **zero recall variance** — the same 6 bugs found on every one of 18 independent runs for the same codebase.

---

## Experimental Results

- **18 Runs, 36 Bugs**: In standard single-prompt runs, the same model found different bugs each time (High Variance).
- **Themed Solution**: By decomposing the audit into distinct cognitive paths (e.g., Dataflow, Security, Symmetry), we achieved 6/6 recall on every run — 100% recall consistency.
- **The "0.9 Accuracy" Barrier**: Proves that aggregate model confidence is a constant, regardless of whether the model is in a high-variance or low-variance state.

---

## Related Research

| Research | Link |
|---|---|
| **BUS (Hallucination Detection)** | [github.com/blazingRadar/sib29-gate](https://github.com/blazingRadar/sib29-gate) |
| **Cognitive Modes** | [github.com/blazingRadar/cognitive-modes](https://github.com/blazingRadar/cognitive-modes) |
| **Keeping Agents Honest** | [github.com/blazingRadar/keeping-agents-honest](https://github.com/blazingRadar/keeping-agents-honest) |

---

## Professional Implementation

These findings inform ongoing governance-pipeline research — a bounded, audit-discipline-driven system for LLM-orchestrated code review under measured scope constraints. For ongoing work, visit [nickcunningham.io](https://nickcunningham.io).

---

*Nick Cunningham — April 2026 — nickcunningham.io*
