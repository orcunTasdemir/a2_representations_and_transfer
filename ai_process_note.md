# AI process note — WORKING DRAFT (material, not yet the 1-page note)

Agent: Claude Code (VS Code extension). Collected as I go; to be cut to one
page and put in my own words at the end. Graded on specificity.

## 1. What I delegated

- Environment and admin: `.venv` from A1's pinned `requirements.txt`,
  `CLAUDE.md` / `NOTES.md` carried over from A1, private GitHub repo.
- Implementing the fixed protocol in `analysis/run.py`: three encoders
  pre-trained once outside the label loop, the 4 × 5 loop over label counts
  and draws, the per-row run counts from the brief, fine-tuning from
  encoder r mod 3, the mean ± SD table.
- Three sanity checks (my choice to include them; the agent proposed them).
- The arithmetic of the reading: gap-vs-SD tables for every pair compared
  in Part 1, the architecture / pre-training split of the gain, and the Q1
  ratios. I asked for these explicitly ("do the math for me") rather than
  eyeballing overlaps; they are now produced by `run.py`.
- Explanations of concepts I was unsure of: label draws, what pre-training
  and the encoder are, which rows use labelled vs unlabelled data, Adam vs
  early stopping, SD vs standard error, bracketing a crossover.

## 2. What I decided, changed or rejected

Decisions that were mine:
- `seed=replicate` for the two frozen rows (the brief states it only for the
  other three).
- Baseline: the mean of the n drawn labels per draw (option B), over the
  full-train mean the agent had computed first (A) and the dev mean (C).
  Shown as a reference line, not a sixth method. Before accepting the
  agent's suggestion I asked what the brief and handouts say; they say
  "predict the mean strength" without specifying which mean (Handout R1
  defines ŷ = ȳ), so the choice was mine to make.
- Wrote eight expectations before running anything (`expectations.md`).
- Adopted all three proposed sanity checks, each for a stated reason
  (catching a failed pre-training, leakage, non-reproducibility).
- Overlap rule: asked what the brief itself endorses before choosing; it
  says "do not read a difference smaller than it" (one SD), so Rule A —
  gap vs the larger of the two SDs — over the stricter sum-of-SDs rule.
- Q2 scope: covered both frozen and fine-tuned vs scratch (both use the
  pre-trained encoder); kept the large gain over the incumbent out of Part 1
  Q2, because the question does not ask for it and pages are limited — it
  goes in memo question 2.
- Kept the Q1 floor claim narrow ("linear in these 160 columns", not "a
  linear model can never"), after the agent pointed to bonus option 3.

Agent output I rejected on substance:
- **Paired per-draw comparison (rejected).** When frozen vs scratch turned
  out unresolvable at n = 50 and 100, the agent offered to compute
  per-draw differences (same panels, so shared noise cancels), which would
  likely have "resolved" the gap. I declined: picking a more sensitive test
  *after* the prescribed one failed to confirm what theory predicts is
  motivated analysis, and the brief fixes the standard (mean ± SD, do not
  read a difference smaller than it). The agent agreed with the decision
  but noted pairing does remove shared draw noise — my reason is the
  post-hoc choice, not that pairing is uninformative.

- **Agent's mechanical Rule A verdict at n = 2,000 (overridden).** The
  run flagged the incumbent's 1,000 → 2,000 change (−0.6 vs larger SD 0.4)
  as passing Rule A. I argued it cannot be called real: all five runs at
  2,000 use the same panels, so that SD leaves out which-panels variation;
  against the draw SD at 1,000 the change is 1.5×. Stated in the memo as
  indistinguishable from noise and negligible either way.

Where I accepted a correction of my reading:
- Memo Q2: "scratch gets a better result at 2,000" → it ties fine-tuned
  (gap 0.0 vs SD 0.2); the case for either is simplicity or optionality,
  not accuracy. Also called the deployed model "fine-tuned encoder plus
  ridge" — it is a fine-tuned network; ridge is only in the frozen rows.
- Q2: my first bracket ("scratch overtakes frozen between 100 and 250")
  needed a resolved ordering on both sides; frozen is never clearly ahead,
  so only "scratch clearly ahead by 1,000, marginally by 250" is supported.
  Adopted the "smaller than its spread" phrasing for 50 and 100.

Where I changed the agent's proposed process:
- The agent gave me an expectations sheet to fill in alone; I had it ask
  the eight questions one at a time in chat instead, so each answer was
  challenged before the next — that is where most corrections below came
  from.
- I refused to make the protocol decisions until I understood the protocol
  (label draws, pre-training, which rows use which data), and had those
  explained first rather than accepting defaults.
- Asked for the analysis to wait until every open decision was settled.
- Introduced an ideas log (`ideas.md`) so points raised in conversation are
  not lost to context compression or a machine switch.

Where my own thinking was corrected (from the expectations exercise):
- I first called the incumbent "short of data" at 1,000 rows, citing
  collinearity; ridge handles collinearity and 1,000 rows for 161
  coefficients is not scarce — the named trap in the rubric.
- I mixed up the frozen random encoder with the pre-trained one.
- I expected 15 runs to give the frozen row a *smaller* SD; more runs
  estimate the SD better, and a second source of randomness makes it larger.
- I thought the lower fine-tuning learning rate was mainly about
  overfitting; it is about not overwriting the pre-trained weights.

Expectations the table contradicted: ridge at n = 50 (expected near 188.9;
got 60.7); random encoder (expected close to raw ridge; beat it at every n);
crossover (expected 250–1,000; the means crossed at 100–250). *Low
priority — first to cut if space is needed.*

Readings of the table I corrected or had corrected:
- Q3: "pre-trained gets an edge after 50–100" → the edge is roughly
  constant and only becomes *measurable* at 100; "regardless of the weights"
  dropped (learned weights add a resolved 7–8; one random encoder only).
- Q2/Q4: my first reading of the SDs was "everything overlaps"; with the
  gap tables I could see that *which* comparisons resolve differs —
  fine-tuned vs scratch never; frozen vs scratch only from 250; random vs
  incumbent always; pre-trained vs random from 100.
- Fine-tuned vs scratch: learned to separate "no evidence of a difference"
  (n = 50, 100: SDs too large) from "evidence of no meaningful difference"
  (n ≥ 250: small SDs, tinier gaps).
- Q4: "means cross closer to 250" dropped (a bracket does not locate). I
  first explained the early crossover by the architecture, then corrected
  myself: frozen and scratch share it; the difference is fixed pretext
  features vs features learned for strength.

Found: the paired per-draw comparison (above).

## 3. How I checked the numbers

- No panel_id shared between any two data files (code, all six pairs).
- Pre-training worked: masked-gauge reconstruction on dev 0.013–0.015 for
  the pre-trained encoders vs 2.225 random and 1.042 predicting 0.
- Reproducibility: re-running pre-training (seed 0) gives identical weights;
  re-running the n = 50, draw 0 cell gives identical scores for all 8 runs.
- Ratios quoted in the memo draft (3.98×, 75%, 44.0 = 93%) recomputed from
  `analysis/outputs/exhibit1.csv`, not by hand.
- Every derived number in the Part 1 reading (gaps, Rule A verdicts, 80/20
  split, Q1 ratios) was first computed ad hoc, then moved into `run.py`;
  the re-run reproduced each quoted value, and `exhibit1_runs.csv` came out
  byte-identical to the earlier run (checked with `cmp`).
- Test extract untouched so far.
