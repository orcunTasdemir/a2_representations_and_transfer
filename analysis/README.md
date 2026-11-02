# Analysis — Assignment 2

## The one command

From the assignment folder (the one containing `data/` and `starter/`):

    python analysis/run.py

About 45 seconds on a laptop CPU. Needs Python 3.10+ with numpy and pandas
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
6. **Check 3**: re-runs pre-training for seed 0 and the n=50, draw 0 cell,
   and confirms the results are bit-identical.

`labeled_test.csv` is not read by this script.

## Outputs (`outputs/`)

| File | Contents |
|---|---|
| `exhibit1_runs.csv` | One row per run: n, draw, method, encoder, dev MSE |
| `exhibit1.csv` | One row per cell: mean, sample SD (ddof=1), runs |
| `exhibit1.md` | Exhibit 1, formatted |
| `part1_comparisons.csv` | Every Part 1 pair: means, SDs, gap, larger SD, Rule A |
| `part1_split.csv` | Raw → pre-trained gain: architecture alone vs pre-training |
| `checks.txt` | Full console log: the three checks and the Part 1 numbers |
