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

My Q4 reading: means cross between 100 and 250 ("closer to 250"); table
cannot confirm frozen is ever ahead; scratch catches up early because the
architecture already suits the problem (from Q3).
Agent's corrections (pending my agreement): drop "closer to 250" — a
bracket does not locate within itself; resolvability at 250 is not
information about where the means crossed. Architecture is shared by
frozen and scratch, so it cannot explain the ordering between them: frozen
features are fixed and aimed at reconstruction (levels off 10.8 → 8.9),
scratch learns features for strength (7.8 → 3.5). Early crossover vs
Handout 9's "tens of thousands": few underlying conditions, noise floor
≤ 3.5, so a simple problem; fine-tuned ≈ scratch from 250 agrees.
Proposed wording: "The means cross between 100 and 250 labels. From 250
on, training from scratch is ahead, marginally at 250 and clearly at
1,000. Below 250 the two cannot be told apart: frozen's lower means at 50
and 100 are smaller than their spread."

**Q4 settled in substance (mine, 2026-11-02):** agreed with the corrections
and the proposed wording; "closer to 250" dropped. I briefly attributed the
early crossover to the architecture (shared by both rows) and corrected
myself: the reason is frozen features fixed on the pretext task vs scratch
learning strength-specific features, on a simple problem.
Fine-tuned vs scratch wording: "cannot be told apart at any label count —
at 50 and 100 because the spread is large, from 250 on because they are
genuinely about equal." Only the second half is a positive finding.

**All four Part 1 questions settled in substance.** Next: memo questions
(Q1 lead number, Q2 deploy method at current label count, Q3 budget number
with money), then one test score, then prose.

## Session 1 close — 2026-11-02

- `part1_answers.md` written: final agreed answers to Part 1 Q1–Q4.
- `run.py` now also produces every derived Part 1 number
  (`part1_comparisons.csv`, `part1_split.csv`, Q1 ratios in `checks.txt`).
  Re-run: all quoted values reproduced; `exhibit1_runs.csv` byte-identical.
- Process note §1–§3 brought up to date; `CLAUDE.md` now lists the files to
  read at session start and the Rule A / numbers-from-run.py rules.
- Transcript re-exported (`a2-session-1.{jsonl,txt}`, overwrites the
  11-01 snapshot with the full thread to date).

### Open — next session starts here

1. Memo Q1: which number settles it (0.7 for 4× labels, or 47.5 vs 3.5).
2. Memo Q2: method to deploy at 2,000 labels (table stops at 1,000) and its
   error vs the incumbent.
3. Memo Q3: budget number, both sides of it, money vs $8.8M.
4. Then: score the one recommended pipeline once on test; memo prose
   (merge Part 1 into the memo sections); cut the process note to 1 page.
5. Optional extension (+4) — not yet discussed.
6. Deadline Thursday 2026-11-05, 6:00 PM Central.

---

## Session 2 — 2026-11-02 (macOS laptop). Memo questions.

Same VS Code conversation as session 1 (thread continues in
`0c849d9a….jsonl`), so the session-2 export will contain session 1 as its
opening part — as in A1; to be stated in `sessions/README.md`.
Start state: repo in sync with GitHub at 13db762; all Part 1 settled.

### Decisions made (mine), 2026-11-03

- Memo Q1 leads with both numbers: A (250 → 1,000 = 750 tests ≈ $3.3M
  bought 0.7 MPa²) then B (same 1,000 panels: network 3.5 vs incumbent 47.5).
- Both units in the memo: MSE (MPa²) and RMSE (MPa, typical miss), so the
  reader sees where RMSE comes from and that the ordering is the same.
- Add n = 2,000 (all training labels) on dev — the closest point to the
  engineer's 4,000. Kept separate from Exhibit 1's four columns; SD there
  covers inner seeds only (one possible set of panels).

Implemented in `run.py` (not yet run at time of writing): `summarise`,
`md_table` (RMSE in brackets = √ of the cell's mean MSE; SDs stay in MSE),
`compare` generalised; outputs `all_labels*.csv/md`, RMSE version of
Exhibit 1 inside `exhibit1.md`.

### n = 2,000 run (dev) — `analysis/outputs/all_labels.md`, `checks.txt`

Run 2026-11-03, 65 s total; Exhibit 1 runs byte-unchanged; checks PASS.
Expectation written first (addendum in `expectations.md`).

| Method | n = 2,000 (RMSE) |
|---|---:|
| Ridge raw | 46.9 ± 0.2 (6.8) |
| Frozen pre-trained | 8.5 ± 2.1 (2.9) |
| Frozen random | 15.7 ± 0.0 (4.0) |
| Scratch | 3.0 ± 0.1 (1.7) |
| Fine-tuned | 3.1 ± 0.2 (1.7) |
| Mean of labels | 188.9 ± 0.0 (13.7) |

Incumbent 1,000 → 2,000: 47.5 ± 0.4 → 46.9 ± 0.2, change −0.6 vs larger SD
0.4 — passes Rule A, barely; RMSE 6.89 → 6.85 MPa; 1,000 extra tests =
$4.4M. Caveat: the two SDs measure different things (draws at 1,000, inner
seeds only at 2,000). At 2,000: scratch vs frozen clear (5.4 vs 2.1);
fine-tuned vs scratch gap 0.0 (tie); ridge − scratch 43.9.

**Decided (mine): the incumbent's 1,000 → 2,000 change (−0.6) is not
claimed as real.** My argument: the 5 runs at 2,000 share the same panels,
so the 0.2 SD omits label-draw variation and understates the uncertainty;
against the draw SD at 1,000 (0.4) the change is only 1.5×. Agent's
counterpoint: direction consistent with every earlier step, so a tiny real
gain is plausible but unconfirmed. Conclusion holds either way.
Phrasing: "A further 1,000 tests moved the incumbent by 0.6 MPa² (typical
miss 6.89 → 6.85 MPa), a change this design cannot distinguish from noise
and too small to matter even if real."
Rule A note: defined for Exhibit 1 cells (SDs include draws); at n = 2,000
the SDs are narrower, so it is applied with judgment there.

Memo Q2 in progress: I agree the traces can be made useful but there is no
accuracy reason to use them at 2,000 (scratch ties fine-tuned). Corrected
by the agent: "better" → "tied; simplicity". Arguments against weighed —
robustness, flagging unusual panels, reuse for other targets (mine) — all
logged in `ideas.md` as untested suggestions. Deploy choice (scratch vs
fine-tuned) pending.

**Decided (mine): deploy the fine-tuned network at 2,000 labels.** Reason
(mine): tied for best on dev (3.1 ± 0.2 vs scratch 3.0 ± 0.1), and it means
Kestrel builds and keeps the pre-trained encoder, which supports frozen +
ridge where labels are scarce, fine-tuning where they are not, and flagging
unusual panels. Objection to be ready for: scratch is as accurate and
simpler; the extra benefits are untested options, not findings.
Wording fix (agent): it is a fine-tuned *network* (160 → 64 → 1, Adam), not
"fine-tuned encoder plus ridge" — ridge appears only in the frozen rows.

Frozen − fine-tuned (`run.py`, PAIRS extended): n=50 −11.7 vs SD 21.1 no;
100 −3.6 vs 5.4 no; 250 +3.6 vs 2.9 yes; 1000 +5.3 vs 2.3 yes; 2000 +5.4 vs
2.1 yes. Frozen "possibly better" at 50/100 (means only, consistent with
Handout 9's freeze-at-tens); fine-tuned clearly better from 250.

Open: test pipeline spec — (a) one network (e.g. seed 0, encoder 0) vs its
own dev run, or (b) the same 5 seed/encoder runs as dev, averaged, no
picking. Mine.

**Decided (mine):** fine-tuned network confirmed (the extra step is cheap
and possibly beneficial later). Usefulness-elsewhere points: (1) next panel
family and (2) flagging unusual panels go in the memo as strong claims /
suggestions; (3) robustness in limitations; (4) reuse for other targets
only if space allows.

Test pipeline: agent's opinion given (not yet my decision) — option (a),
one encoder + one fine-tuned network, seeds fixed in advance (encoder 0,
seed 0 = draw 0 of the n=2,000 runs), compared with its own dev run and
shown beside the 5-run dev mean ± SD. Reasoning: the 3 encoders × 5 seeds
are a measuring device, not a deployment; spread at 2,000 is ±0.2 on 3.1,
so an ensemble removes almost nothing and would be an untested new
pipeline; picking the best seed chases noise. Production norms: one model
with recorded seed, retrain on schedule, refresh encoder, version, monitor.

### Test pipeline — fixed BEFORE the test extract is read (2026-11-03)

**Decided (mine): option (a).** The recommended pipeline, specified in full:

1. Pre-train encoder 0: `pretrain(traces, seed=0)` on all 20,000 traces.
2. Fine-tuned network: `supervised(X, y, ..., seed=0, encoder=encoder_0)`
   on all 2,000 training labels (inside: 75% fit / 25% early stopping,
   Adam at 1e-3, patience 60, max 800 epochs).
3. Score once on `labeled_test.csv`.

Its dev counterpart (same pipeline, `all_labels_runs.csv`, draw 0): **3.01**.
For context, the 5 runs at n = 2,000 on dev: 3.01, 3.10, 2.67, 3.31, 3.19
(mean ± SD 3.1 ± 0.2) — seed 0 is mid-range, i.e. typical. Seed 0 was chosen
as the default, not for its score. Only this one number is computed on
test; no other method, no baseline. The test/dev difference is explained by
the data dictionary's note (test var(y) ~10% lower), not by a second look.
Memo will also describe retraining and monitoring after deployment.

### Test score — run once, 2026-11-03 (`analysis/outputs/test_score.txt`)

Recommended pipeline (fine-tuned network, encoder 0, seed 0, all 2,000
labels): **dev MSE 3.01 (RMSE 1.74 MPa), test MSE 2.87 (RMSE 1.69 MPa),
test − dev −0.14.** Within the seed-to-seed spread on dev (SD 0.24, range
2.67–3.31) — matches my pre-registered expectation. All other outputs
unchanged by this run; checks PASS. Test is not to be used for anything
else.

### Memo Q3 — in progress

My first answer: budget 1,000; watch the shape of the error curve (or
compare with the noise level) to judge whether 1,000 captured most of the
accuracy; if not, go to 1,250 / 1,500 and repeat — i.e. staged.
Agent's challenges (pending my answers): (1) justify 1,000 over 250 —
250 → 1,000 halves fine-tuned error (7.2 → 3.6) for $3.3M; 1,000 → 2,000
buys ~0.5 for $4.4M; depends on an accuracy spec the brief never states;
(2) the noise level can only be bounded, and a flattening curve does not
prove noise (the Q1 lesson); (3) a new family has no dev set — held-out
evaluation panels must come out of the budget, or use the inner split;
(4) frozen early, fine-tune from ~250; (5) transfer assumption → limitations.
Costs/step gains to be added to `run.py` once framing is chosen.

Q3 continued (mine): tie the budget to dollars even though value per
accuracy is not given; noise level can be bounded, not measured; keep
frozen + ridge for the early stages. Unsure on total and split.
Agent: dollar framing as a stopping rule ("each further tranche of 250
costs $1.1M; continue only if it saves more than that"); noise ≤ ~3.0 MPa²
(typical miss ≤ ~1.7 MPa) from best dev 3.0 / test 2.87 — an upper bound.
Check-set precision (inline formula √(2/m), normal errors — to go in
run.py if quoted): 100 → ±14%, 200 → ±10%, 250 → ±9%.
Options: A 800 train + 200 check = 1,000 ($4.4M); B 1,000 + 200 = 1,200
($5.28M); C 1,000, inner split only ($4.4M). Agent's view: B, check set
tested first and fixed, stages 100 → 250 → 500 → 1,000. Pending my choice.

**Decided (mine): option B** — 1,000 training tests + 200 check panels on
top = up to 1,200 tests (ceiling, not commitment), released in stages.
Dollar stopping rule (benefit minus cost per tranche) and the noise upper
bound adopted. Proposed stages (pending confirmation): check set first
(200), then 100 → 250 → 500 → 1,000 training; frozen + ridge at the
small stages, fine-tuned from ~250; 500 is a live checkpoint with no
number from our table. Costs to come from `run.py`.

**Decided (mine):** stage sizes 100 → 250 → 500 → 1,000 training panels after
a 200-panel check set; total ceiling 1,200. Careful wording around "test"
(destructive test / check set / our test file).

Budget numbers now in `run.py` (`budget_numbers`, `budget_stages.csv`,
`checks.txt`): check set $880,000; cumulative $1.32M / $1.98M / $3.08M /
$5.28M; tranches $440K / $660K / $1.1M / $2.2M; ceiling $5.28M vs $8.8M =
$3.52M (40%) less; each further 250 = $1.1M; check set of 200 measures MSE
to ±10% (1 SE, normal errors); noise ≤ 3.0 MPa² (1.7 MPa). Exhibit 1,
n=2,000 and test outputs unchanged by this run; checks PASS.

**All memo decisions made.** Next: memo prose (merge Part 1 into the memo
sections), process note to 1 page, optional extension (not yet discussed),
final clean-copy reproducibility check, sessions export, zip.
