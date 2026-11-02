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

1. ~~Crossover bracket~~ committed: between 250 and 1,000, guess nearer the top.
2. **Decided (mine): baseline option B** — predict the mean of the n drawn
   labels, per draw, scored on dev; mean ± SD over the same 5 draws as the
   other rows. Shown as a reference line under the five method rows, not as
   a sixth method. (A = full-train mean 188.9 and C = dev mean were the
   alternatives; C is not a usable predictor.)
3. Sanity checks to build into the script (proposed, not yet agreed):
   pre-trained vs random masked-reconstruction error; train/dev panel-ID
   overlap; baseline printed beside the table.
4. Next: write `analysis/` and run Exhibit 1.

## Session 1, continued — 2026-11-01. Exhibit 1 run.

### Decisions made (mine)

- Sanity checks 1–3 adopted (pre-training learned / no panel overlap /
  bit-identical re-run).

### What was done

- `analysis/run.py` written and run: `python analysis/run.py`, 41 s.
  Outputs in `analysis/outputs/`. Test extract not touched.
- All three checks PASS. Check 1: masked reconstruction MSE on dev gauges
  0.015 / 0.014 / 0.013 (pre-trained), 2.225 (random), 1.042 (predict 0).

### Exhibit 1 (dev MSE, MPa², mean ± SD) — from `analysis/outputs/exhibit1.md`

| Method | n=50 | n=100 | n=250 | n=1000 |
|---|---:|---:|---:|---:|
| Ridge raw | 60.7 ± 5.6 | 56.5 ± 6.3 | 48.2 ± 0.6 | 47.5 ± 0.4 |
| Frozen pre-trained | 33.5 ± 12.0 | 17.6 ± 5.4 | 10.8 ± 2.9 | 8.9 ± 2.3 |
| Frozen random | 39.2 ± 6.6 | 25.6 ± 3.5 | 18.6 ± 0.8 | 16.0 ± 0.2 |
| Scratch | 47.0 ± 17.8 | 23.3 ± 9.4 | 7.8 ± 1.5 | 3.5 ± 0.1 |
| Fine-tuned | 45.2 ± 21.1 | 21.3 ± 5.0 | 7.2 ± 0.5 | 3.6 ± 0.3 |
| Mean of n labels | 190.2 ± 2.5 | 189.4 ± 0.6 | 189.4 ± 0.3 | 188.9 ± 0.1 |

### Part 1 Q1 — settled in substance (mine), prose not yet written

The incumbent's limit is its shape, not data. Evidence: flat 250 → 1,000
(48.2 → 47.5, gain 0.7 ≈ SDs); scratch reaches 3.5 ± 0.1 on the same
panels, so 44.0 MPa² (93%) of ridge's 47.5 is shape, not noise (computed
from `exhibit1.csv`). Process link: flow × cure multiply (a sum assumes
compensation the physics rules out) and a contamination threshold. Floor is
specific to a model linear in these 160 columns (links to bonus option 3).
Ridge vs mean: 3.98× lower at 1,000; explains 68% (n=50) → 75% (n=1,000).

Post-result clarification (marked as such in `expectations.md`): I had
missed that the random encoder has a ridge head; would then have said it
*could* beat raw ridge.

### Checkpoint at session close

- `memo.md` working draft (Q1 substance, Exhibit 1, TBD sections) and
  `ai_process_note.md` working draft started.
- Transcript exported to `sessions/claude-code/a2-session-1.{jsonl,txt}`.
  A failed Oct 21 start (OAuth expired, one message) exported as
  `a2-session-0-failed.{jsonl,txt}`.

### Open — next session starts here

1. Part 1 Q2: what pre-training buys vs scratch, at which n (frozen vs
   scratch, fine-tuned vs scratch, with SDs).
2. Part 1 Q3 (random-encoder control) and Q4 (crossover bracket; I
   expected 250–1,000).
3. Memo decisions: the single number that settles Q1; RMSE alongside MSE?
4. Process note §2 now lists accepted/changed items; still worth finding a
   piece of agent *output* I reject on substance.
5. New standing rule (mine): write every keepable point down immediately —
   `ideas.md` created and back-filled from session 1; rule added to
   `CLAUDE.md`.

## Session 1, continued — 2026-11-01. Part 1 Q2 in progress.

Gap-vs-SD tables (inline `python -c` on `analysis/outputs/exhibit1.csv`; must
be added to `run.py` if any of it goes in the memo). Rule A = gap > larger
SD (brief's wording); Rule B = gap > sum of SDs (ranges don't touch).

| n | frozen − scratch | larger SD | SD sum | A | B | finetuned − scratch | larger SD | A | B |
|---|---:|---:|---:|:-:|:-:|---:|---:|:-:|:-:|
| 50 | −13.5 | 17.8 | 29.8 | no | no | −1.8 | 21.1 | no | no |
| 100 | −5.6 | 9.4 | 14.8 | no | no | −2.0 | 9.4 | no | no |
| 250 | +3.1 | 2.9 | 4.4 | yes (barely) | no | −0.6 | 1.5 | no | no |
| 1000 | +5.4 | 2.3 | 2.4 | yes | yes | +0.1 | 0.3 | no | no |

My first Q2 reading: scratch overtakes frozen between 100 and 250;
fine-tuned vs scratch unresolvable everywhere. Agent's challenge: frozen is
never *clearly* ahead (fails both rules at 50, 100), so a two-sided bracket
is not supported; only "scratch clearly ahead by 1,000, marginally by 250".
Fine-tuned ≈ scratch at n ≥ 250 is a real tie (small SDs), not hidden noise.

Open (mine): Rule A or B; whether to compute paired per-draw differences
(footnote at most); which comparison answers "can the traces be made
useful" — vs scratch (nothing resolved) or vs raw ridge (large gains).

Q2 decisions so far (mine): agreed with the corrected reading (no two-sided
bracket; "smaller than its spread" at 50/100). **Rejected** the paired
per-draw comparison — post-hoc sharper test = motivated analysis (logged in
process note §2). Brief's wording endorses Rule A (gap vs a single SD).
Still open: confirm Rule A with larger SD; include fine-tuned vs scratch in
Q2; raw-ridge comparison in Q2 or only in memo Q2.

**Q2 settled in substance (mine):** Rule A, larger of the two SDs (matches
the brief's wording). Q2 covers both frozen vs scratch and fine-tuned vs
scratch (both use the pre-trained encoder). Raw-ridge comparison kept out
of Part 1 Q2 — the question asks only for the comparison with scratch, and
page economy — and used in memo question 2 instead.

## Part 1 Q3 — Rule A tables (inline on `exhibit1.csv`)

| n | random − raw ridge | larger SD | A | pre-trained − random | larger SD | A |
|---|---:|---:|:-:|---:|---:|:-:|
| 50 | −21.5 | 6.6 | yes | −5.7 | 12.0 | no |
| 100 | −30.8 | 6.3 | yes | −8.0 | 5.4 | yes |
| 250 | −29.6 | 0.8 | yes | −7.8 | 2.9 | yes |
| 1000 | −31.5 | 0.4 | yes | −7.1 | 2.3 | yes |

Q3 split of raw → pre-trained gain (inline on `exhibit1.csv` means):

| n | total | random layer alone | pre-training learned |
|---|---:|---:|---:|
| 50 | 27.2 | 21.5 (79%) | 5.7 (21%, unresolved) |
| 100 | 38.8 | 30.8 (79%) | 8.0 (21%) |
| 250 | 37.4 | 29.6 (79%) | 7.8 (21%) |
| 1000 | 38.6 | 31.5 (82%) | 7.1 (18%) |

My Q3 reading: without the control I would have credited all of the gain
to pre-training; most comes from the nonlinear shape of the layer; random
features give ridge nonlinear combinations to pick from. Agent's
corrections (pending my agreement): ~80/20 split at every n; the pre-trained
edge is roughly constant (~6–8) and becomes *measurable* at 100, not
*begins* between 50 and 100; "regardless of the weights" too strong (learned
weights add a resolved 7–8, and only one random encoder was tested).

**Q3 settled in substance (mine, 2026-11-02):** agreed with all three
corrections — ~80/20 split stated as such; pre-training's edge "becomes
measurable at 100" (not "begins"); drop "regardless of the weights", and
note only one random encoder was tested (a random object, per the brief).

## Part 1 Q4 — started 2026-11-02
