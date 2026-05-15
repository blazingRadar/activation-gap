# Single Model, Zero Recall Variance

Author: Nick Cunningham
Date: April 2026
Status: preliminary single-codebase research note

## Summary

This note reports a narrow observation from an LLM code-audit experiment. In one single-codebase, single-author-labeled setup, a themed prompt-decomposition workflow surfaced the same specified six-bug set across 18 reported runs.

The phrase "zero variance" in this repository means zero observed recall variance for that specified bug set in that sample. It does not mean that all model output was deterministic. It does not establish that the method generalizes to other codebases, models, providers, or audit tasks.

The public repository contains the writeup and a self-consistency script. It does not include raw model outputs, prompts, target code, or scoring tables, so the empirical result is not independently reproducible from this repository alone.

## Problem

A single broad prompt such as "find all bugs" can produce unstable recall in code-audit tasks. The model may identify some defects in one run and different defects in another run. This note explores one decomposition strategy for reducing that recall instability.

The working hypothesis was that some misses are activation failures rather than knowledge failures. In this framing, the model may be capable of explaining a defect when asked directly, but may fail to surface that defect during a broad audit pass.

## Method

The workflow split the audit into themed analytical passes instead of asking one broad question. Each pass focused on a narrower lens, such as dataflow, security, or symmetry. The goal was to reduce competition between candidate findings and make subtle defects easier to surface.

The workflow also used proof-oriented follow-up prompts for candidate findings:

- What exact input breaks this?
- What exact type causes failure?
- What exactly crashes?
- What assumption made the previous pass miss this?

Misses were treated as diagnostic events. When the model missed a known target defect, the next prompt asked why the miss happened, extracted a rule from that explanation, and fed the rule back into the next run.

## Reported Result

The reported target set contained six author-labeled bugs in one bounded code artifact. Under the themed-decomposition workflow, the same six-bug set surfaced on every one of 18 reported runs.

The bounded claim is:

> The themed-decomposition workflow produced stable recall of the specified six-bug set across 18 reported runs in this single-codebase setup.

The stronger claims are not established here:

- The method finds all bugs in a codebase.
- The method generalizes across codebases.
- The method generalizes across model families or provider versions.
- The method eliminates all model-output variance.
- The method controls false positives.

## Ground Truth

The six-bug ground truth was established by the author through prior inspection and direct testing of the target artifact. This is single-author labeling, not an external benchmark or peer-reviewed bug set.

Known limitations of the ground truth:

- Single labeler. No inter-rater reliability measurement.
- Single codebase. Generalization to other codebases is not established.
- The author knew the six-bug set before the runs. The runs were not blind evaluations.
- The public repository does not include the target artifact or raw model outputs.
- False-positive accounting is not documented in this repository.

These limitations bound the result. They do not erase the reported recall-stability observation, but they prevent broader claims.

## Confidence Values

Earlier framing described a "0.9 accuracy" barrier. This repository does not include raw confidence traces or a statistical analysis sufficient to support a proof-level claim about aggregate model confidence.

The bounded observation is simpler: confidence-style summaries, when present in the author's recorded runs, were not sufficient by themselves to distinguish unstable recall from stable recall. The public artifact does not support a broader claim that confidence is constant across models or tasks.

## Reproducibility Status

This repository is not a standalone reproducibility package. The raw run artifacts are not public here. The previous raw-data reference pointed at a repository path that is not publicly reachable, so it has been removed rather than left as a broken reproducibility claim.

To make the result independently reproducible, a future package would need at least:

- the target code artifact
- the six-bug expected set
- prompt files
- model and provider metadata
- raw model outputs for all runs
- scoring criteria
- false-positive accounting
- rerun instructions

## Verification Script

`verify_claims.py` checks repository self-consistency only. It verifies that the README and paper contain aligned bounded claims. It does not verify empirical reproduction, model behavior, raw outputs, or the existence of the six target bugs.

Run:

```shell
python3 verify_claims.py
```

## Interpretation

The useful design idea is themed decomposition: instead of asking one model to perform a broad audit in one pass, divide the review into narrower analytical lenses and use proof-oriented follow-up prompts on candidate findings and misses.

In this single reported setup, that structure coincided with stable recall of the specified bug set. Treat it as a hypothesis and method note, not as a general benchmark result.

## Future Work

A stronger public study would add:

- multiple target codebases
- blinded ground-truth labels
- external reviewers
- raw run artifacts
- false-positive measurement
- cross-model reruns with exact model identifiers
- a scoring harness that can be rerun by others

## Status

Preliminary research note. April 2026.
