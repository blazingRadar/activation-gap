#!/usr/bin/env python3
import sys
from pathlib import Path

# Repo Self-Consistency Check.
#
# This script verifies that the README and paper make matching claims.
# It does NOT verify:
#   - Whether the experimental results reproduce
#   - Whether the bugs described actually exist in the target codebase
#   - Whether the 18 runs were performed as described
#   - Whether model outputs actually converge as reported
#
# Empirical reproducibility requires the raw run artifacts, which are
# referenced but not included in this repository.
REPO_ROOT = Path(__file__).parent
PAPER = REPO_ROOT / "single_model_zero_variance.md"
README = REPO_ROOT / "README.md"

def check_claim(label, condition):
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {label}")
    return condition

def main():
    if not PAPER.exists():
        print(f"Error: {PAPER.name} not found.")
        return 1

    print("="*60)
    print("  ACTIVATION GAP: REPO SELF-CONSISTENCY CHECK")
    print("  (Verifies README <-> paper claim alignment only.")
    print("   Does NOT verify experimental reproducibility.)")
    print("="*60)

    paper_content = PAPER.read_text()
    readme_content = README.read_text()

    checks = []

    # Claim 1: Recall consistency is bounded to the specified six-bug set.
    recall_in_paper = "specified six-bug set across 18 reported runs" in paper_content
    recall_in_readme = "specified six-bug set across 18 reported runs" in readme_content
    checks.append(check_claim("Paper documents bounded six-bug recall stability", recall_in_paper))
    checks.append(check_claim("README matches bounded recall-stability claim", recall_in_readme))

    # Claim 2: Recall Stability
    recall_stability_claim = (
        "zero observed recall variance" in paper_content.lower()
        and "all model output was deterministic" in paper_content.lower()
        and "does not mean" in paper_content.lower()
    )
    checks.append(check_claim("Paper bounds zero-variance wording to recall stability", recall_stability_claim))

    # Claim 3: Methodology
    methodology = "themed prompt-decomposition workflow" in paper_content
    checks.append(check_claim("Themed decomposition methodology is documented", methodology))

    reproducibility_boundary = (
        "not a standalone reproducibility package" in paper_content
        and "does not verify empirical reproduction" in readme_content
    )
    checks.append(check_claim("Reproducibility boundary is explicit", reproducibility_boundary))

    if all(checks):
        print("\nRepo self-consistency checks passed.")
        print("Note: this is claim alignment only, not empirical verification.")
        return 0

    print("\nRepo self-consistency checks failed.")
    print("At least one public claim boundary is missing or misaligned.")
    return 1

if __name__ == "__main__":
    sys.exit(main())
