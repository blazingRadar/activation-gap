# Publication Manifest

This repository is a public preliminary research note about reducing recall
variance in an LLM code-audit task with themed prompt decomposition.

## Included

- `README.md`: public landing page and claim boundary.
- `single_model_zero_variance.md`: bounded writeup.
- `verify_claims.py`: README/paper self-consistency check.
- `LICENSE`: MIT license.

## Repository Contract

This is not a standalone reproducibility package. It does not include raw model
outputs, prompts, target code, scoring tables, external labels, or rerun
instructions.

## Claim Boundary

The strongest claim is narrow: in one single-codebase, single-author-labeled
experiment, the themed-decomposition workflow reportedly surfaced the same
specified six-bug set across 18 reported runs.

The repository does not claim cross-model generalization, cross-codebase
generalization, false-positive control, all-output determinism, or proof of a
general model-capability ceiling.

## Verification Surface

`python3 verify_claims.py` checks README/paper claim alignment only. It does not
reproduce the experiment or verify the underlying empirical artifacts.
