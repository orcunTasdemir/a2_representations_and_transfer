# Analysis — Assignment 2

## The one command

From the assignment folder (the one containing `data/` and `starter/`):

    python analysis/run.py

About 65 seconds on a laptop CPU. Needs Python 3.10+ with numpy and pandas
only; versions used are pinned in `../requirements.txt`. It imports
`starter/kestrel.py` unchanged and reads `data/` by relative path.

## What it does

1. **Check 2**: confirms no `panel_id` appears in more than one data file.
2. Pre-trains the three encoders (seeds 0, 1, 2) once, on the 20,000
   unlabelled traces, outside the label loop.
3. **Check 1**: masked reconstruction error of each encoder on the dev
   gauges (no strength values used), against the random encoder and against
   predicting 0.
4. **Exhibit 1**: for n in {50, 100, 250, 1000} and draws r = 0..4, fits all
   five methods on the same `label_subset(n, r)` panels and scores each on
   `labeled_dev.csv`. Runs per cell follow the brief. Inner seeds are
   `seed=r` for every method, including both frozen rows. Fine-tuning on
   draw r starts from encoder r mod 3. A reference line predicts the mean
   of the n drawn labels.
5. The Part 1 reading numbers: gap and Rule A verdict (gap > larger SD)
   for every pair compared, the split of the raw → pre-trained gain into
   architecture vs pre-training, and the incumbent's ratios to the mean
   baseline and to the network from scratch.
6. **All 2,000 training labels** (Kestrel's current count), every method
   scored on dev, 5 inner seeds (SD covers inner randomness only — there is
   one possible set of panels). Kept separate from Exhibit 1, with the same
   Rule A comparisons and the incumbent's 1,000 → 2,000 change and cost.
7. Memo Q3 budget numbers: the staged plan (200 check panels, then 100 →
   250 → 500 → 1,000 training panels) with costs at $4,400 per panel, the
   dev error this study measured at each stage, the saving against the
   engineer's 2,000, the check set's precision, and the noise upper bound.
8. The single test score (see below).
9. **Check 3**: re-runs pre-training for seed 0 and the n=50, draw 0 cell,
   and confirms the results are bit-identical.

`labeled_test.csv` is read once, at the end, to score the single
recommended pipeline (fine-tuned network from encoder 0, seed 0, trained on
all 2,000 labels). That pipeline was fixed in `NOTES.md` before test was
read; no other model is scored on test and nothing is chosen from it.

## Checking the memo

    python analysis/check_memo_numbers.py

Run after `run.py`. Lists any number in `../memo.md` that no file in
`outputs/` produces at the precision the memo states it. Kept out of
`run.py` so a clean copy without a memo still runs end to end.

## Outputs (`outputs/`)

| File | Contents |
|---|---|
| `exhibit1_runs.csv` | One row per run: n, draw, method, encoder, dev MSE |
| `exhibit1.csv` | One row per cell: mean, sample SD (ddof=1), runs |
| `exhibit1.md` | Exhibit 1, formatted; second version with RMSE (MPa) in brackets |
| `all_labels_runs.csv`, `all_labels.csv`, `all_labels.md` | The n = 2,000 runs, cells and table |
| `all_labels_comparisons.csv` | Rule A comparisons at n = 2,000 |
| `part1_comparisons.csv` | Every Part 1 pair: means, SDs, gap, larger SD, Rule A |
| `part1_split.csv` | Raw → pre-trained gain: architecture alone vs pre-training |
| `budget_stages.csv` | Memo Q3: staged plan — panels, tranche and cumulative cost, measured dev error per stage |
| `test_score.txt` | The recommended pipeline's dev and test MSE / RMSE |
| `checks.txt` | Full console log: the three checks and the Part 1 numbers |
