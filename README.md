# activation-gap

Frontier LLMs miss bugs not because they lack the knowledge but because standard prompts fail to activate it.

This repository documents five steps that dissolved each capability ceiling — from 3/6 bugs with random variance to 6/6 bugs with zero variance across 18 independent runs — using a single model and no fine-tuning.

Read the paper: [single_model_zero_variance.md](single_model_zero_variance.md)

- **Mechanism:** Themed Analytical Decomposition, Adversarial Mode Selection, Cognitive Mode Mapping, Set-Theory Defense Verification, and Model-Guided Prompt Generation.
- **Results:** 100% recall on primary benchmark, validated across 12 real-world CVEs in 7 languages.
- **Data:** [github.com/blazingRadar/sib29-gate](https://github.com/blazingRadar/sib29-gate)
- **Full pipeline:** [github.com/blazingRadar/sib29](https://github.com/blazingRadar/sib29) (private, under active development)
- **Contact:** [nickcunningham.io](https://nickcunningham.io)
