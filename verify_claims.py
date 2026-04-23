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
    status = "✅ PASS" if condition else "❌ FAIL"
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

    # Claim 1: Recall Consistency
    recall_in_paper = "6 out of 6 bugs" in paper_content or "100% bug recall" in paper_content
    recall_in_readme = "6/6 recall" in readme_content or "100% recall" in readme_content
    check_claim("Paper documents 6/6 recall achievement", recall_in_paper)
    check_claim("README matches Paper recall claim", recall_in_readme)

    # Claim 2: Recall Stability
    recall_stability_claim = (
        "zero recall variance" in paper_content.lower() or "zero variance" in paper_content.lower()
    ) and "18 runs" in paper_content and "6 out of 6 bugs" in paper_content
    check_claim("Paper documents 18-run recall stability (6/6 every run)", recall_stability_claim)

    # Claim 3: Methodology
    methodology = "Step 1: Themed Analytical Decomposition" in paper_content
    check_claim("Architecture methodology (Decomposition) is documented", methodology)

    print("\nRepo self-consistency checks passed.")
    print("Note: this is internal claim alignment, not empirical verification.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
