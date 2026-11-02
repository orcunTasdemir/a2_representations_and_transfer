# MEMO — WORKING DRAFT (not for submission)

**To:** Head of Quality, Kestrel Composites
**Re:** Should Kestrel budget 2,000 more destructive tests? A second opinion.

Status, end of session 1 (2026-11-01): Exhibit 1 is built. Part 1 Q1 is
settled in substance; Q2–Q4 and every Part 2 answer are still open. Nothing
below is prose yet: these are my points and the numbers behind them, to be
written up together once the reading is complete. Every number is from
`analysis/outputs/` (`python analysis/run.py`).

Limits: at most 2 pages of prose; Exhibit 1 does not count.

---

## Recommendation (first paragraph — to be written last)

TBD.

## 1. Will more destructive tests fix the current model?

**Settled in substance (Part 1 Q1):**

- The incumbent (ridge on the 160 raw gauges) does learn from the gauges:
  dev MSE 60.7 at n = 50 and 47.5 at n = 1,000, against 188.9 for predicting
  the mean (about 4× lower; it explains about 68% → 75% of the variation).
- It stops improving: 48.2 at n = 250, 47.5 at n = 1,000. Quadrupling the
  labels bought 0.7 MPa², about the size of the SDs (0.6, 0.4).
- The limit is the model's shape, not a shortage of data. On the same 1,000
  panels a network from scratch reaches 3.5 ± 0.1, so the noise floor is at
  most 3.5 and 44.0 MPa² (93%) of the incumbent's error is shape, not noise.
- Why, from the process: strength needs resin flow *and* cure; the two
  failure modes multiply, and a surplus in one cannot make up for a deficit
  in the other. A weighted sum of gauges assumes exactly that compensation.
  Separately, contamination acts through a threshold (nothing below, sharp
  fall above), which a straight line cannot represent either.
- The floor is specific to a model linear in *these* columns. A linear model
  on different features (e.g. a flow × cure product) need not have it.

**Open:** which single number "settles it" for the Head of Quality.
Anticipated objection: the table stops at 1,000 — answered by the flat
250 → 1,000 step plus the 3.5 that a flexible model reaches.

## 2. Can the unlabelled traces be made useful?

TBD — depends on Part 1 Q2 (what pre-training buys vs scratch, by n) and
Q3 (what the random-encoder control rules out). Note the table ends at
1,000 labels while Kestrel holds 2,000.

## 3. How many tests should the next panel family budget?

TBD — depends on Part 1 Q4 (crossover bracket). Must give a number, what
happens on either side of it, and the cost at $4,400 per panel against the
engineer's 2,000 ($8.8M).

## Test-extract score

TBD — the recommended pipeline scored once on `labeled_test.csv`, beside its
dev number, with one sentence on the difference (test var(y) is ~10% lower).
Not run yet: the recommendation is not fixed.

## What the evidence does not establish

Collected so far:
- Nothing between 1,000 and 2,000 labels (Kestrel's current count), nor
  beyond.
- The noise floor is bounded above (≤ 3.5), not measured.
- Possible point: reconstruction error as a check that new panels resemble
  the historical traces (drift), relevant to a new panel family.

---

## Exhibit 1. Dev MSE (MPa²), mean ± SD over runs. Lower is better.

| Method | n = 50 | n = 100 | n = 250 | n = 1,000 | Runs/cell |
|---|---:|---:|---:|---:|---:|
| Ridge on the 160 raw gauges (incumbent) | 60.7 ± 5.6 | 56.5 ± 6.3 | 48.2 ± 0.6 | 47.5 ± 0.4 | 5 |
| Frozen pre-trained encoder + ridge | 33.5 ± 12.0 | 17.6 ± 5.4 | 10.8 ± 2.9 | 8.9 ± 2.3 | 15 |
| Frozen random encoder + ridge (control) | 39.2 ± 6.6 | 25.6 ± 3.5 | 18.6 ± 0.8 | 16.0 ± 0.2 | 5 |
| Network from scratch | 47.0 ± 17.8 | 23.3 ± 9.4 | 7.8 ± 1.5 | 3.5 ± 0.1 | 5 |
| Fine-tuned encoder | 45.2 ± 21.1 | 21.3 ± 5.0 | 7.2 ± 0.5 | 3.6 ± 0.3 | 5 |
| Reference: predict the mean of the n labels, no gauges | 190.2 ± 2.5 | 189.4 ± 0.6 | 189.4 ± 0.3 | 188.9 ± 0.1 | 5 |

Note to self: exhibit caption and whether to add RMSE (MPa) for a
non-modeller reader are still to decide.
