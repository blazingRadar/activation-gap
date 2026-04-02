# Single Model, Zero Variance: How Themed Cognitive Splitting Unlocks Hidden Capability in Frontier LLMs

**Nick Cunningham**
*Independent Research — March–April 2026*
*nickcunningham.io | github.com/blazingRadar/sib29*

---

## Abstract

Every frontier AI code review tool uses the same architecture: one model, one prompt, one pass. When that model misses a bug, the standard response is "add another model." I rejected that assumption. Starting with a single model (Grok-3) that found 3 out of 6 known bugs in a single pass, I systematically dissolved each capability ceiling through five iterative steps — themed analytical decomposition, adversarial mode selection, cognitive mode mapping, set-theory defense verification, and model-guided prompt generation. At Step 5, the same single model found 6 out of 6 bugs with zero variance across 18 independent runs, zero hallucinations, and zero false critical findings on clean files. The architecture was then validated across 12 real-world CVEs in 7 programming languages and confirmed model-agnostic across Grok-3, Claude Sonnet 4, and GPT o3.

Two things are not in this paper: the exact prompt implementations (part of the active pipeline) and a solved noise problem (15-25 findings per file, the gate reduces this but does not eliminate it). Both are documented honestly in the limitations section.

I stopped at Step 5 of a 14-category architecture because the results already challenged the assumption that multi-model pipelines are necessary for reliable code analysis. This paper documents each step, the data behind it, and what remains unbuilt.

---

## 1. The Starting Point

I began with the simplest possible code analysis prompt:

```
Find all the bugs.

{source_code}
```

Applied to `auth.py` from the Python `requests` library (315 lines, 6 independently verified bugs), this prompt produces 8-12 findings per run. Of those, 3-4 are real bugs. The other 4-8 are recommendations, false positives, or noise.

More importantly, the 3-4 bugs found vary between runs. The same model, same prompt, same file, same temperature produces different bugs each time. Run it 6 times and you might see all 6 bugs appear at least once — but no single run finds them all.

This is the ceiling every AI code review tool accepts. The standard response is to add more models, more runs, or more post-processing. I asked a different question: **Is this actually a capability limit, or is it an activation failure?**

To test this, I asked Grok-3 directly about each bug it missed. For every bug the model failed to find during code review, it could explain the bug perfectly when asked about it in isolation. It knew about latin1 encoding limits, about `seek()` failing on bytes objects, about inconsistent format strings in parallel warning messages. It knew all of it. It just didn't report it during the audit.

The capability existed. The activation didn't. That distinction shaped everything that followed.

---

## 2. Five Steps to Zero Variance

### Step 1: Themed Analytical Decomposition

**The claim dissolved:** "A single model can only find 3-4 out of 6 bugs per run."

Instead of one prompt asking "find all the bugs," I created 4 parallel prompts, each constrained to a specific analytical theme — a cognitively distinct lens that focuses the model on one class of bug patterns. Each prompt instructs the model to audit using only that theme's patterns. A focus constraint prevents the model from wandering into patterns assigned to other themes. All 4 calls run in parallel on the same code. Findings are combined via union.

The specific themes and their exact patterns are part of the active pipeline and not published here. What is published: the mechanism, the results, and the principle. The themes are derived from classical bug taxonomy — not arbitrary groupings. Each maps to a distinct reasoning mode that activates different model attention patterns.

**Result:** 4 out of 6 bugs, found consistently. Each bug was found by exactly one theme. Bugs B (seek on bytes/string) and I (latin1 crash) were still missed. But the 4 that were found appeared in every run. **The variance on those 4 bugs dropped to zero.**

**Why it works:** In a single prompt, findings compete for output tokens. Dramatic findings (null dereference, SQL injection) consume output space at the expense of subtle findings (format string inconsistency, encoding limitation). By constraining each call to one theme, the competition is eliminated. A subtle finding becomes the most important finding within its theme — even though it would rank last in an unconstrained analysis. I call this phenomenon **attention slot competition**: findings competing for limited output space. It is an output-side limitation, distinct from the input-side "Lost in the Middle" phenomenon documented by Liu et al. (2023).

**Cost:** 4 API calls instead of 1. ~$0.28 per file instead of ~$0.07.

---

### Step 2: Adversarial Mode Verification

**The claim dissolved:** "Bugs B and I cannot be found by this model."

Both bugs were present in Phase 1 output — the model mentioned the relevant lines and general area. But the diagnosis was wrong:

- Bug B: "seek() could fail due to non-seekable file-like objects" — but the actual bug is that the body could be `bytes` or `str`, which have no `seek()` method at all
- Bug I: "encoding inconsistency between latin1 and utf-8" — but the actual bug is that `latin1` raises `UnicodeEncodeError` on any character above code point 255

The findings were in the neighborhood. The diagnosis was wrong. I needed a second pass to sharpen them.

**What I tried:** A sequential verification call that takes all Phase 1 findings as input and asks three questions about each:

1. What is the most specific input that triggers a crash? (exact type, value, exception)
2. For every encoding operation: what characters crash it?
3. For every method call: what types could that variable be at runtime? Which types lack this method?

I tested 10 cognitive modes for this verification step. The modes fall into two behavioral categories: skeptical modes that challenge the Phase 1 diagnosis and agreeable modes that accept it.

**Result:** Skeptical modes found both bugs. Agreeable modes dismissed Bug I as "not a crash, just an inconsistency." Five of ten modes failed on Bug I. The specific mode names and framing patterns are part of the active pipeline. What is published: the principle that verification mode matters significantly, and that the mode producing the highest skepticism toward Phase 1 findings produced the highest accuracy.

Skeptical modes dig past the framing to test limits. Agreeable modes accept the Phase 1 description and move on. The winning mode specifically interrogates encoding operations by testing boundary characters — which leads directly to the `UnicodeEncodeError` on latin1.

**Combined result:** Phase 1 (4 themed calls) + Phase 1b (1 skeptical verification call) = **6 out of 6 bugs. Every run. 36/36 across 18 independent runs.**

**Critical finding about modes:** Mode instruction helps Phase 1b (verification) but hurts Phase 1a (discovery). In Phase 1a, uninstructed mode outperformed every instructed mode tested. The model's natural mode selection produces the best discovery results. Adding "You are a security expert" or any role instruction inflated confidence without improving accuracy.

This contradicts the common practice of role-based prompting for code analysis. **For discovery, no role is the best role. For verification, skeptical framing is the only framing that adds value.**

**Cost:** 5 API calls total. ~$0.35 per file.

---

### Step 3: Activation Gaps vs. Knowledge Gaps

**The claim dissolved:** "If one model can't find it, you need a different model."

I discovered that every model has blind spots, but they fall into two distinct categories:

**Activation gaps:** The model has the knowledge but doesn't apply it during code review. Testable by asking the model directly about the concept in isolation. If it answers correctly, the gap is activatable with the right prompt.

**Knowledge gaps:** The model genuinely lacks the knowledge. No prompt can fix this. A different model or a different approach is required.

**Testing methodology:**
1. Ask the model: "What happens when you run `'你好'.encode('latin1')` in Python?"
2. If it correctly says `UnicodeEncodeError` → activation gap
3. If it cannot explain → knowledge gap

Testing across 3 models on 7 CVEs:

| Bug | Grok-3 | Claude Sonnet 4 | GPT o3 |
|-----|--------|-----------------|--------|
| latin1 crash | Activation gap (fixed by skeptical mode) | Activation gap (fixed by skeptical mode) | Activation gap (fixed by skeptical mode) |
| Protocol-relative URL `//evil.com` | Activation gap (found with set-theory) | Activation gap (found with set-theory) | Knowledge gap (0/10 modes found it) |
| Spring4Shell property chain | Activation gap (found with guard bypass) | Knowledge gap | Knowledge gap |

**The key finding:** Every bug in the test set was an activation gap for at least one model. No bug required a different model — it required a different question.

This doesn't mean multi-model pipelines are worthless. They provide redundancy and cover knowledge gaps efficiently. But the assumption that capability ceilings require more models is wrong in most cases. Most ceilings require better activation.

---

### Step 4: Set-Theory Defense Verification

**The claim dissolved:** "Models can't find bugs where the defense looks correct."

I documented a systematic failure across all three models: when a model encounters a security mechanism during code review — a validation check, encoding function, sanitization routine, allowlist — it assumes the mechanism works and moves on. I call this **defense trust bias**.

Every model could explain why the defense was flawed when told where the bug was. But during unprompted review, all three trusted it:

- Django: Saw validation logic, didn't trace past the `continue` that bypasses it
- urllib3: Saw the header stripping frozenset, assumed it was complete (Cookie was missing)
- Werkzeug: Saw the size check, didn't test with the default `None` value that disables it
- Express: Saw `encodeUrl()`, assumed encoding equals sanitization

I asked each model why it missed each bug. The self-diagnoses were consistent across all three: "I saw the defense and assumed it worked."

**The solution:** Force computation instead of judgment.

The prompt forces explicit set-theoretic reasoning for every security-relevant operation: define the complete expected set from security standards, enumerate the actual set from code, compute the difference, and verify that every defense is reachable from all code paths. The exact prompt structure is part of the active pipeline.

"Is this secure?" requires judgment. "What should this operation handle that it doesn't?" requires computation. The model retrieves RFCs, OWASP guidelines, CWE definitions — the exact knowledge that defines what "should" be there — and compares against what "is" there. The delta is the bug.

**Result on 5 CVEs previously missed by Themes 1-4:**

| CVE | Before Theme 5 | After Theme 5 |
|-----|---------------|---------------|
| Django SQL injection (validation bypass) | FOUND* | FOUND |
| urllib3 Cookie header leak | MISSED | FOUND |
| Werkzeug DoS (default None) | MISSED | FOUND |
| Express open redirect | FOUND* | FOUND |
| Go Host header injection | FOUND* | FOUND |

**Cost:** 6 API calls total (5 Phase 1a + 1 Phase 1b). ~$0.42 per file.

---

### Step 5: Model-Guided Prompt Generation

**The claim dissolved:** "If the prompt doesn't find it, you need a human to write a better prompt."

Two bugs remained stubbornly difficult: Spring4Shell (incomplete property filter in Java introspection) and curl SOCKS5 (heap overflow from hostname length truncation). Both were found in some runs but not consistently.

I tried something unconventional: I told each model where the bug was, then asked: "Why did you miss this? What do you need to do better next time?"

The models' self-diagnoses were specific and actionable.

**curl SOCKS5 — Grok-3's self-diagnosis:**
> "I trusted the guard at line ~589 because it appeared sufficient. My analysis focused on the initial execution path and did not account for dynamic runtime behaviors such as redirects or state changes between check and use."

**Spring4Shell — Grok-3's self-diagnosis:**
> "I did not connect the dots to the module property as a potential bypass without specific prompting. I did not account for alternative property chains or paths added by newer language versions."

**urllib3 Cookie header — all three models independently:**
> "I saw the list and assumed it was complete."

From each diagnosis, I extracted a generalized principle and turned it into a prompt instruction. The exact instructions are part of the active pipeline. The principle: **the model's self-diagnosis named the assumption that caused the failure. Negating that assumption in the prompt reversed the failure.**

The generalized instruction for guard bypass — derived directly from the curl and Spring4Shell diagnoses — found Spring4Shell on the next run. The model identified that the property filter only applies in the main introspection path, and that the interface introspection path and plain-accessor path skip it entirely.

The generalized instruction for list completeness — derived from the urllib3 diagnosis — caused all three models to find the missing Cookie header on the next run.

**The models told me how to prompt them. I asked why they failed. They explained. I generalized the explanation into a prompt instruction. It worked across all three model families.**

This loop — miss → ask why → extract principle → generalize → validate — was done manually over six days. It could be systematized. The self-diagnosis step requires ground truth to identify what was missed. Given ground truth, the rest is mechanical.

---

## 3. The Architecture at Step 5

```
SOURCE CODE
    │
    ▼
Phase 0 — File router (deterministic, ~50 tokens):
    Read file extension + first 50 lines of imports
    Select which themes are relevant
    Universal (always run): Themes 1-3
    Conditional (triggered by signals): Themes 4-5+
    Average: 3-6 calls per file, not all 14
    │
    ▼
Phase 1a — Parallel calls (uninstructed, any frontier model):
    Calls 1-N: Themed analytical lenses (N = 3-6 based on Phase 0 routing)
    Each call: one bug class, one cognitive frame, full attention budget
    Focus constraint prevents cross-theme wandering
    Union of all results
    │
    ▼
Phase 1b — Sequential call (skeptical verification mode):
    For each Phase 1a finding:
      Challenge the diagnosis
      Test encoding boundaries
      Verify runtime type assumptions
    │
    ▼
FINDINGS (with line numbers, crash inputs, severity)
```

**Total: 6 API calls per file. ~$0.42. ~90 seconds.**

**On Phase 0:** The router does not use an LLM classifier. It reads deterministic signals: file extension for language and memory model, import statements for libraries and domain, and a short scan for operation types. This keeps routing variance at zero — the only variance in the pipeline is in the model outputs, not in which calls are made.

**On prompt design:** The right prompt is not always the most specific or the most structured. The prompt should serve the cognitive task the model needs to perform. Discovery tasks need freedom — get out of the way and let the model think. Verification tasks need constraint — force the model into a specific epistemic position. Consolidation tasks need structure — now formatting serves a purpose because the thinking is already done. Applying structure to a discovery task is like asking someone to think carefully while filling out a form. The form gets completed. The thinking suffers. This principle — matching prompt style to cognitive task — underlies every step in this architecture. See also: *The Structure Paradox* (Cunningham, 2026c).

**On noise:** The pipeline produces 15-25 findings per file on average, of which 4-6 are real bugs. Noise reduction is a separate problem addressed by the behavioral gate documented in Cunningham (2026b).

---

## 4. Validation

### 4.1 Primary Test File: 18 Variance Runs

18 runs of the complete pipeline on `auth.py` (6 runs × 3 experimental conditions):

| Bug | Hit Rate |
|-----|----------|
| A (None→header) | 6/6 — 100% |
| B (seek on bytes) | 6/6 — 100% |
| D (KeyError) | 6/6 — 100% |
| G (format string) | 6/6 — 100% |
| H (object confusion) | 6/6 — 100% |
| I (latin1 crash) | 6/6 — 100% |

**36/36 bug detections. 0 variance. 0 hallucinations. 0 false critical findings.**

*Data: `variance_6runs_pipeline/run{1-6}/`, `phase1b_5modes_6runs/`*

### 4.2 CVE Benchmark: 12 Real-World Vulnerabilities, 7 Languages

**Key:** FOUND = explicitly identified | FOUND* = actionable, developer would remediate | MISSED = no useful signal

| CVE | Language | Grok-3 | Claude Sonnet 4 | GPT o3 |
|-----|----------|--------|-----------------|--------|
| CVE-2021-35042 (Django SQL injection) | Python | FOUND | FOUND* | FOUND |
| CVE-2019-14234 (Django JSONField) | Python | FOUND | FOUND | FOUND |
| CVE-2023-43804 (urllib3 header leak) | Python | FOUND | FOUND* | MISSED |
| CVE-2023-25577 (Werkzeug DoS) | Python | FOUND | FOUND | FOUND |
| CVE-2024-29041 (Express open redirect) | JavaScript | FOUND | FOUND | FOUND* |
| CVE-2024-34351 (Next.js SSRF) | TypeScript | FOUND | FOUND | FOUND |
| CVE-2021-23337 (lodash code injection) | JavaScript | FOUND | FOUND | FOUND |
| CVE-2023-29406 (Go header injection) | Go | FOUND | FOUND | FOUND |
| CVE-2021-44228 (Log4Shell) | Java | FOUND | FOUND | FOUND |
| CVE-2022-22965 (Spring4Shell) | Java | FOUND | FOUND | MISSED |
| CVE-2014-0160 (Heartbleed) | C | FOUND | FOUND | FOUND |
| CVE-2023-38545 (curl heap overflow) | C | FOUND* | MISSED | FOUND* |

**Same prompts, three different models.** Union across all three: 11/12 CVEs with at least one FOUND or FOUND*. All FOUND* findings were manually reviewed and confirmed actionable by an experienced developer without additional context.

*Data: `cat5_5files_3models/`, `cat5_v2_5files_3models/`*

### 4.3 Blind Test: 10 Unseen Files

10 files never seen during development — 5 with known CVEs, 5 clean, across 8 languages:

| Finding | Result | Notes |
|---------|--------|-------|
| Text4Shell (CVE-2022-42889) | FOUND | Phase 4 and Phase 5 both identified explicitly |
| Pillow DoS (CVE-2023-44271) | FOUND* | Actionable finding buried in noise |
| jsonwebtoken RCE (CVE-2022-23529) | MISSED | Touched vulnerable line but rated LOW — not actionable |
| Sanitize XSS (CVE-2023-36823) | MISSED | Parser differential — not covered by current themes |
| Clean files (5 files) | 19 false HIGH | Noise addressed by behavioral gate (Cunningham 2026b) |

*Data: `validation_blind/`, `grok_remaining_bugs/`*

---

## 5. What I Stopped Building

I designed 14 analytical categories but only built and tested 5. The remaining 9 address vulnerability classes the current pipeline doesn't cover:

| Category | Covers | Status |
|----------|--------|--------|
| 6. Concurrency | Race conditions, TOCTOU, lock ordering | Tested — activation gap confirmed |
| 7. Buffer/Memory Safety | Overflow, over-read, use-after-free | Tested on 1 file |
| 8. Cryptographic Weakness | Weak algorithms, predictable randomness | Designed, untested |
| 9. DoS/Complexity | Regex DoS, hash collision, recursive bombs | Designed, untested |
| 10. Information Disclosure | Stack traces, verbose errors, timing leaks | Designed, untested |
| 11. Business Logic | Auth bypass, privilege escalation | Designed, untested |
| 12. Deserialization | pickle, yaml.load, ObjectInputStream | Designed, untested |
| 13. Prototype Pollution | __proto__ manipulation (JS-specific) | Designed, untested |
| 14. Integer Overflow | Truncation, wraparound, narrowing casts | Tested on 1 file |

Each category has a complete prompt written. The Phase 0 router selects which to run per file. I stopped at 5 because 5 was enough to prove the thesis: **the capability ceiling is not the model. It is the prompt architecture.**

**On Category 6 — Concurrency:** During review of this paper, an AI assistant predicted that race condition detection would represent a genuine knowledge gap — the one place where single-model activation would fail and multi-model consensus would be required. The reasoning was sound: temporal interleaving across non-deterministic thread execution requires simulation, not retrieval.

The human researcher tested it anyway.

All three models found both race conditions in a token bucket implementation and explained them correctly. Their self-diagnoses were nearly identical:

**Grok-3:**
> "I may have focused on the functional correctness of the token bucket algorithm without considering the implications of concurrent access. If the context of multi-threading wasn't explicitly mentioned, I might not have assumed the need for thread safety."

**Claude Sonnet 4:**
> "I sometimes focus too much on the high-level logic rather than carefully tracing through the low-level execution steps. Ask me to trace specific interleavings."

**GPT o3:**
> "The example code doesn't show explicit thread usage... static analysis or a review of single-threaded logic might not highlight the hazards. Provide context on how the class is used concurrently."

All three said the same thing: they default to single-threaded analysis unless explicitly told otherwise. `import threading` at the top of the file was not sufficient activation. Explicit concurrency framing is — and it is exactly what Category 6 provides. The AI predicted a wall. The human found another door. The pattern held.

**On the remaining categories:** The 5-category pipeline reliably finds approximately 80% of bugs across tested codebases. The remaining 20% lives in categories 8-14. These are known gaps, not unknown unknowns. Each has a designed prompt. The honest expectation is that most will follow the same pattern as categories 1-6: suspected knowledge gaps that turn out to be activation gaps when tested. Some may be genuine limits. The only way to know is to test them.

---

## 6. What Didn't Work

**Behavioral gate on structured findings:** The behavioral gate documented in Cunningham (2026b) was validated on single-pass discovery outputs. When applied to themed split findings — structured, line-specific, with crash inputs already provided — the gate required recalibration. This is an input format dependency, not a gate failure. Recalibration work is ongoing.

**Phase 2 consolidation as a filter:** A single consolidation prompt reduces 95 raw findings to 15 readable items. This looks like noise reduction. It loses 67% of real bugs. It keeps dramatic findings and drops subtle ones, reintroducing attention slot competition at the output stage. It is a developer presentation tool, not a filter. Use it after the gate. Not instead of it.

**Severity rating:** Model-assigned severity does not reliably match human expert judgment in current testing — a false positive was rated CRITICAL above confirmed real bugs. Severity calibration is on the roadmap and being tested.

**Mode instruction on Phase 1a:** Every instructed mode performed worse than uninstructed for discovery. "You are a security expert" inflated confidence without improving accuracy. No role is the best role for discovery.

**Framework context in Phase 0:** Adding framework context (even 189 tokens) steered models into analysis mode and reduced bug detection. More context hurt. This was counterintuitive and reproducible.

**Generic oblique prompts:** Unstructured metaphorical prompts without adversarial framing produced 0/6 on the primary test file. Models treated them as riddles. This is distinct from the Billy framework documented in Cunningham (2026c) — Billy is not a generic poem. It is a specifically constructed adversarial narrative that removes compliance overhead without triggering audit mode. The difference: generic oblique prompts are unstructured but passive. Billy is unstructured and adversarial. The adversarial framing is what activates discovery. The natural language format removes the compliance tax. Both elements are required.

---

## 7. Limitations

**Noise.** 15-25 findings per file, 4-6 real bugs. Noise reduction is being addressed through the behavioral gate documented in Cunningham (2026b).

**Severity rating.** Model-assigned severity does not reliably match human expert judgment. On the roadmap and being tested.

**Single-file analysis.** Bugs requiring cross-file reasoning remain challenging. The defense verification theme partially addresses this by prompting models to consider paths from other components, but full cross-file attack chain reconstruction is not reliable.

**Remaining vulnerability classes.** The 5-theme pipeline finds approximately 80% of bugs across tested codebases. Categories 8-14 address the remaining 20%. Known gaps, designed prompts, untested execution.

**Sample size.** Primary validation: one 315-line Python file, 18 runs. CVE benchmark: 12 files, 7 languages. Blind test: 10 files. Not a large-scale benchmark.

**One researcher.** All experiments run by one person on one machine. No independent replication yet.

---

## 8. The Implication

I started with a model that found 3 out of 6 bugs. Everyone — including the AI systems I consulted — said the remaining bugs required different models, more compute, or fine-tuning.

They were wrong.

The same model found 6 out of 6 bugs when I changed how I asked. Not what I asked — how. Split the analysis into themed lenses. Verify with skeptical mode. Force set-theory computation on defenses. Ask the model why it failed and use its answer to fix the prompt.

Each step dissolved a ceiling that looked like a capability limit but was an activation failure. The model had the knowledge the entire time. It needed the right question.

The pattern held through category 6. It will probably hold through most of categories 7-14. There may be genuine limits somewhere in the remaining nine categories. Those limits are real. They just haven't been found yet.

At 5 categories, the pipeline finds roughly 80% of bugs. Each additional category bridges part of the remaining gap. The architecture scales cleanly — one more parallel API call per category, running independently, adding coverage without touching what already works.

**The next experiment: closing the noise loop**

The self-diagnosis loop that found missed bugs in Step 5 points toward a broader architecture. If models can diagnose why they missed a real bug, they may be equally capable of diagnosing why they hallucinated a false one.

A Phase 1c pass would work like this: show the model its own high-severity findings and ask it to find the specific line of code that prevents the bug from actually being exploitable. Not "prove this crashes" but "prove this doesn't." If the model finds the line, the finding was wrong and it now knows why. If it can't find the line, the finding may be real.

The longer implication is a pipeline that evolves its own instructions from its own failures — not through weight updates but through accumulated prompt refinement against ground truth. Each missed bug sharpens the discovery prompts. Each false positive sharpens the filtering instructions. The model stays the same. The questions get better.

This is the V0 of a self-evolving code reviewer. Every failure contains the instruction that prevents the next failure of the same class. The discovery direction has been proven over five steps. The noise direction is the next experiment.

This is preliminary speculation. Phase 1c has not been run. It is documented here because the mechanism is the same one already proven to work, applied in the opposite direction. If it holds, the noise problem and the coverage problem have the same solution.

The implication for anyone building AI code review tools: before adding another model to your pipeline, try asking the model you have a better question. The capability is already there. We kept finding that out. So far, we have not been wrong.

---

## References

- Cunningham, N. (2026a). *C ≈ 0.9: LLM Confidence Is a Constant, Not a Measurement*. Independent Research.
- Cunningham, N. (2026b). *Behavioral Uncertainty Signatures*. Independent Research. github.com/blazingRadar/sib29-gate
- Cunningham, N. (2026c). *The Structure Paradox: Why Format Compliance Is the Enemy of LLM Reasoning*. Independent Research.
- Khot, T., et al. (2022). Decomposed Prompting: A Modular Approach for Solving Complex Tasks. *ICLR 2023*.
- Liu, N.F., et al. (2023). Lost in the Middle: How Language Models Use Long Contexts. *TACL 2024*.
- Wang, X., et al. (2022). Self-Consistency Improves Chain of Thought Reasoning in Language Models.
- Wang, Y., et al. (2024). Multi-Expert Prompting Improves Reliability, Safety, and Usefulness of Large Language Models. *EMNLP 2024*.
- Kadavath, S., et al. (2022). Language Models (Mostly) Know What They Know. *arXiv:2207.05221*.

---

*Raw data: github.com/blazingRadar/sib29*
*Contact: nickcunningham.io*
*Preliminary research. April 2026.*
*Total experimental cost: ~$70 in API calls over 7 days.*
