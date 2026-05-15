# Activation Gap

Preliminary notes on reducing recall variance in an LLM code-audit task with themed prompt decomposition.

## Current Claim

In one single-codebase, single-author-labeled experiment, themed analytical decomposition surfaced the same specified six-bug set across 18 reported runs. In this repository, "zero variance" means zero observed recall variance for that specified bug set in that sample. It does not mean all model outputs were deterministic, and it does not establish generalization to other models, codebases, or tasks.

## Repository Scope

This is a public writeup and self-consistency artifact. It is not a reproducible benchmark package.

Included:

- `single_model_zero_variance.md`: the bounded writeup.
- `verify_claims.py`: a self-consistency check that compares README and paper claims.
- `PUBLICATION_MANIFEST.md`: claim boundary and repository contract.
- `LICENSE`: MIT license.

Not included:

- raw model outputs
- target code artifact
- prompt files
- scoring tables
- external-labeler review
- rerun harness

## What This Shows

- The reported experiment used a specified six-bug target set on one codebase.
- The themed-decomposition approach reportedly surfaced that six-bug set on all 18 runs.
- The strongest public claim is recall stability under the reported conditions, not broad capability improvement.

## What This Does Not Show

- It does not prove that themed decomposition finds all bugs.
- It does not prove cross-model or cross-codebase generalization.
- It does not characterize false positives from the public artifacts.
- It does not prove that confidence values are constant or model-independent.
- It does not provide raw artifacts needed for independent reproduction.

## Verification

```shell
python3 verify_claims.py
```

The script checks that the README and paper make aligned bounded claims. It does not verify empirical reproduction, that the six bugs exist, or that the 18 runs happened as described.

## Related Repositories

| Research | Link |
|---|---|
| BUS (Hallucination Detection) | [github.com/blazingRadar/sib29-gate](https://github.com/blazingRadar/sib29-gate) |
| Cognitive Modes | [github.com/blazingRadar/cognitive-modes](https://github.com/blazingRadar/cognitive-modes) |
| Keeping Agents Honest | [github.com/blazingRadar/keeping-agents-honest](https://github.com/blazingRadar/keeping-agents-honest) |

## Status

Archived preliminary research note. The public artifact is useful as a claim-boundary and methodology note, not as a standalone reproducibility package.
