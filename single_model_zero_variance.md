# Single Model, Zero Variance

**Nick Cunningham**
*Independent Research — April 2026*
*nickcunningham.io | github.com/blazingRadar/sib29*

---

Everyone builds AI code review the same way.

One model. One prompt. One pass.

It misses bugs → add another model.

That's the default thinking.

I didn't buy it.

---

## The Starting Point

I gave a frontier model a simple task:

Find all the bugs.

It found about half.

And worse — it wasn't consistent.

Same model. Same code. Same prompt.

Different bugs every time.

That's what people accept as the ceiling.

I didn't think it was a capability problem.

I thought it was an activation problem.

---

## The Key Realization

The model knew every bug it missed.

If I asked about the bug directly, it explained it perfectly.

So the issue wasn't intelligence.

It was access.

The model had the knowledge.

It just wasn't using it during the audit.

---

## What I Did

I stopped asking one big question.

I broke the problem apart.

Step by step.

---

## Step 1: Themed Analytical Decomposition

I call this **Themed Analytical Decomposition**.

In practice, that means splitting the thinking.

Instead of:
> "find all bugs"

I ran multiple focused passes.

Each one looked at the code through a different lens.

No overlap. No competition.

**Result:**

- More bugs found
- Same bugs every time

Variance dropped immediately.

### Why That Works

In a normal prompt, findings compete.

Big obvious bugs crowd out subtle ones.

There's only so much output space.

I call this **attention slot competition.**

When you remove the competition:
Subtle bugs finally show up.

---

## Step 2 — Force Proof

The model was close on the remaining bugs.

It saw the area, but got the diagnosis wrong.

So I forced it to prove its claims.

Not *"is this a bug?"*

But:

- What exact input breaks this?
- What exact type causes failure?
- What exactly crashes?

And this is where it got interesting.

**The mode mattered.**

| Mode | Result |
|---|---|
| Agreeable | Misses bugs |
| Skeptical | Finds them |

So:
- Discovery → no role
- Verification → skeptical only

That combination unlocked everything.

---

## Result

Same model.

**6 out of 6 bugs.**

Every run.

Zero recall variance.

"Zero variance" here refers to recall stability: the same 6 bugs surfaced on every run. Individual finding wording and non-bug commentary may still vary between runs; the bug set does not.

No hallucinations.

---

## Step 3 — Activation vs Knowledge

This was a big one.

Not all misses are the same.

Two types:

- **Activation gap** → model knows, but didn't use it
- **Knowledge gap** → model genuinely doesn't know

Most of what looked like "limits" were activation gaps.

The model knew.

It just needed the right question.

---

## Step 4 — Break Defense Trust

Models trust code too much.

They see validation and assume it works.

That's a huge blind spot.

So I forced them to compute instead of judge.

Not:
> "is this safe?"

But:
> What should this handle?
> What does it actually handle?
> What's missing?

That delta is the bug.

That change alone unlocked an entire class of misses.

---

## Step 5 — Let the Model Fix Itself

This was the unlock.

I asked the model:

> Why did you miss this?

And it answered. Clearly.

It told me:

- what assumption it made
- why it trusted something it shouldn't
- what it failed to check

I took that, turned it into a rule, fed it back in.

Next run: bug found.

Same model. No retraining.

### The Pattern

```
Miss → ask why → extract principle → fix prompt
```

The model told me how to use it.

---

## The Architecture

You don't need more models.

You need better structure.

1. Split the thinking
2. Remove competition
3. Force proof
4. Break assumptions
5. Learn from failures

That's it.

---

## What This Proves

The ceiling isn't the model.

It's how you ask.

Most "limits" aren't real.

They're activation failures.

---

## Ground Truth

A note on how the 6-bug ground truth was established.

The target codebase was a single, bounded code artifact chosen for the
experiment. The 6-bug set was established by the author through prior
inspection and direct testing — this is single-author labeling, not
an external benchmark or peer-reviewed bug set.

Known limitations of the ground truth:

- Single labeler (author). No inter-rater reliability measurement.
- Single codebase. Generalization to other codebases is not established
  by this experiment.
- "Bug" is defined by the author as a defect the model was expected
  to surface. Definitional drift is possible.
- The 6-bug set was known to the author before the runs. The runs were
  not blind evaluations — the author knew which bugs the model should
  find and observed whether it did.

These limitations do not invalidate the finding — the reproducibility of
6/6 recall across 18 runs is observed regardless of how the ground truth
was established — but they bound the claim. "The themed-decomposition
approach surfaces the specified bug set reproducibly under these
conditions" is the accurate reading; "the themed-decomposition approach
finds all bugs in any codebase" is not.

## Known Limitations

- **Sample size.** 18 runs on one codebase. Statistical claims beyond
  "recall was stable in this sample" are not supported.
- **Single-author labeling.** See Ground Truth section above.
- **Temperature-0 variance not characterized.** "Zero variance" here means
  zero recall variance across 18 runs. Provider-side non-determinism at
  temperature 0 is a known phenomenon (batch routing, token tiebreaks)
  that may produce measurable variance on other metrics (finding wording,
  latency, token counts). That variance was not measured in this
  experiment.
- **Cross-model generalization.** The paper references "works across
  multiple models" but does not document specific model IDs, provider
  versions, or the number of runs per model. Treat cross-model claims
  as preliminary.
- **Codebase generalization.** One codebase. No claim about other
  codebases of different size, language, or structure.
- **Raw artifacts.** Referenced as "github.com/blazingRadar/sib29" but
  not included directly in this repository. Reproducibility requires
  access to those raw artifacts.

---

## Where It Stands

- 6/6 bugs
- 18 runs
- Zero recall variance
- ~80% coverage with current categories

And I only built 5 out of 14 categories.

---

## What's Next

The same loop that finds missed bugs should be able to remove false positives.

Same idea. Opposite direction.

If that works:

You get a system that improves itself without retraining.

---

## My Take

The capability is already there.

We've been asking the wrong way.

Every time I thought I hit a wall…

It wasn't a wall.

It was a bad question.

So far, that's held every time.

---

*Raw data: github.com/blazingRadar/sib29*
*Contact: nickcunningham.io*
*Preliminary research. April 2026.*
