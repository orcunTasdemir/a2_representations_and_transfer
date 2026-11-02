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

### Decisions made (mine)

- Frozen rows' ridge uses `seed=replicate`, matching the other rows.
- Folder under git, private repo
  https://github.com/orcunTasdemir/a2_representations_and_transfer, as in A1,
  so I can work on the Windows PC too. Data and handouts tracked (repo is
  private; `data/` is excluded from the submission zip, not from the repo).

### Numbers produced, with provenance

Inline `python -c` under `.venv`, using `kestrel.load` only. To be reproduced
by the analysis script.

| Quantity | Value |
|---|---|
| Train mean strength (n=2000) | 32.81 MPa, sd 13.43 |
| var(y) on dev | 188.8 MPa² |
| Predict-the-train-mean, dev MSE | 188.9 MPa² (RMSE 13.74 MPa) |

### Open

1. Fill `expectations.md` before Exhibit 1 is run. Then build `analysis/`.
2. Baseline detail for the memo: the mean of all 2,000 train labels was used
   above; the mean of only the n drawn labels is the stricter "do-nothing at
   budget n". Mine to choose; difference expected to be small.

## Session 1, continued — 2026-11-01 (macOS laptop). Expectations written.

- Went through the eight expectation questions in chat; recorded in
  `expectations.md` with my answers and the agent's comments kept separate.
- Concepts explained along the way: the 2,000 / n / 1,000 counts; what a
  label draw is (5 subsets per n, all five methods on the same panels);
  ridge's 37/13 penalty split vs the networks' 37/13 early-stopping split
  (networks do not refit on all n); Adam vs early stopping (pre-training has
  no early stopping, ridge has no Adam); SD vs standard error; bracketing.
- Corrections to my thinking worth naming in the process note: frozen random
  encoder is never trained (I had mixed it up with the pre-trained one);
  more runs do not shrink the SD; the fine-tuning learning rate protects the
  pre-trained weights rather than preventing overfitting; "short of data" is
  the named trap for the incumbent.

### Open

1. Still to commit in `expectations.md`: a crossover bracket (Q7).
2. Baseline: mean of all 2,000 train labels vs mean of the n drawn labels.
3. Sanity checks to build into the script (proposed, not yet agreed):
   pre-trained vs random masked-reconstruction error; train/dev panel-ID
   overlap; baseline printed beside the table.
4. Next: write `analysis/` and run Exhibit 1.
