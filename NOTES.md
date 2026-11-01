# Working notes, IDS 575 Assignment 2

Append one section per work block. Read this first when switching machines.

---

## Session 1 — 2026-10-20 (macOS laptop). Setup and protocol concepts. No analysis yet.

### What was done

- Read the brief, rubric, data dictionary, course docs, and both starter files.
- Carried A1's working setup over: `CLAUDE.md`, this file, `requirements.txt`
  (same pins as A1), `.gitignore`, `sessions/` with A1's `render_transcript.py`.
- `.venv` built with Python 3.11 from `requirements.txt`.

### Concepts covered (explanations, not decisions)

- **Label counts** n ∈ {50, 100, 250, 1000}: subsets of the 2,000 *train*
  panels, simulating "what if Kestrel had only n tested panels". Dev (1,000)
  is never trained on; every run is scored on all of it.
- **Label draws**: 5 different random subsets per n, from
  `label_subset(n, replicate)`, seed `9000 + 100*r + n`. Not nested across n.
- **Pre-training seeds**: 3 encoders, trained once on the 20,000 unlabelled
  traces, reused in every cell. Second source of randomness, independent of
  the labels.
- `seed=replicate` is the *inner* randomness (ridge's 75/25 penalty split; the
  network's init and 25% early-stopping split), separate from which panels
  are drawn.
- What pre-training is, what the encoder is, and which methods use labelled
  vs unlabelled data — see the session transcript.
- The counts: 2,000 = Kestrel's labelled stock (train); n ∈ {50..1000} =
  simulated budgets drawn from it; 1,000 dev / 1,000 test = held-out grading
  extracts, never fitted on. Table tops out at n=1000 though Kestrel has 2,000.
- My first answer on the incumbent ("1,000 not enough for a linear model;
  collinear, non-linear columns") was challenged: ridge handles collinearity,
  1,000 rows for 161 coefficients is not scarce; the non-linear part is the
  live hypothesis. Data shortage vs model-form limit (variance vs bias) to be
  settled from the table, not asserted.

### Open — decisions that are mine

1. Seed passed to the two frozen rows' ridge (brief only states it for the
   other three rows; `seed=replicate` would match them).
2. Write down expectations before running anything, incl. the incumbent at
   n=50 vs n=1000 in light of the Process Engineering paragraph.
3. Whether to put this folder under git (A1 was, for syncing two machines).
