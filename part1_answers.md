# Part 1 — settled answers

Not a deliverable. The brief asks for these answers "in the memo"; this file
holds the final, agreed version of each so the memo can be drafted from it
and nothing is lost. Settled with the agent in session 1 (2026-11-01 →
11-02); the judgments are mine, the wording was refined together.

Every number is dev MSE in MPa² from `python analysis/run.py`:
`outputs/exhibit1.md` (the table), `outputs/part1_comparisons.csv` (gaps vs
SDs), `outputs/part1_split.csv` (Q3 split), `outputs/checks.txt` (Q1 ratios).

**Reading rule (Rule A, from the brief's wording "do not read a difference
smaller than it"):** a gap between two cells is read only if it exceeds the
larger of the two cells' SDs.

---

## Q1. What happens to the incumbent as labels accumulate?

**Answer.** The incumbent learns from the gauges but stops improving early,
and what stops it is its shape, not a shortage of data.

- It beats ignoring the gauges by a wide margin: 60.7 at n = 50 and 47.5 at
  n = 1,000, against 190.2 → 188.9 for predicting the mean of the labels
  (3.13× → 3.98× lower; it explains 68.1% → 74.9% of the variation).
- It flattens: 60.7 → 56.5 → 48.2 → 47.5. Quadrupling the labels from 250
  to 1,000 bought **0.7 MPa²**, about the size of the SDs at those counts
  (0.6, 0.4).
- **How the table tells data shortage from something else.** A flat curve
  alone could be either the model's limit or irreducible noise. What
  separates them is a flexible model on the *same panels*: at n = 1,000 the
  network from scratch reaches **3.5 ± 0.1** where ridge sits at
  **47.5 ± 0.4**. So the noise floor is at most 3.5, and **44.0 MPa² (93%)**
  of the incumbent's error is its shape, not noise. More labels cannot
  remove that.
- **Why, from the process.** Process Engineering says strength needs resin
  flow *and* cure: the two failure modes multiply, and a surplus in one
  cannot make up for a deficit in the other. A weighted sum of gauges
  assumes exactly that compensation. Separately, contamination acts through
  a threshold — nothing below it, a sharp fall above — which a straight
  line cannot represent either.
- **Scope of the claim.** The floor belongs to a model that is linear in
  *these 160 raw columns*. A linear model on different features (for
  example a flow × cure product) need not have it — the third optional
  extension.

**Objection to be ready for:** "the table stops at 1,000; ridge might
improve at 2,000." Answer: the flat 250 → 1,000 step, and 3.5 on the same
panels shows the remaining error is not noise.

## Q2. What does pre-training buy, and at which label counts? (vs scratch)

**Answer.** Against training from scratch, pre-training buys nothing the
table can resolve at any label count.

- **Frozen pre-trained + ridge vs scratch:** frozen has the lower mean at
  50 (33.5 ± 12.0 vs 47.0 ± 17.8) and 100 (17.6 ± 5.4 vs 23.3 ± 9.4), but
  both gaps (13.5, 5.6) are **smaller than their spread** (17.8, 9.4).
  From 250 scratch is ahead — marginally at 250 (gap 3.1 vs SD 2.9),
  clearly at 1,000 (gap 5.4 vs SD 2.3).
- **Fine-tuned vs scratch:** they cannot be told apart at any label count —
  at 50 and 100 because the spread is large (SDs 21.1, 9.4), from 250 on
  because they are genuinely about equal (gaps 0.6 and 0.1 against SDs of
  1.5 and 0.3). Only the second half is a positive finding: by a few
  hundred labels the pre-trained starting point no longer matters. At 50
  and 100 a real fine-tuning advantage — where Handout 9 says it should be
  largest — could be hiding in the noise.
- The comparison against the incumbent (large and resolved at every n) is
  not part of this question; it goes in the memo's question 2.

## Q3. What does the random-encoder row rule out?

**Answer.** Without it I would have credited the whole improvement of the
frozen pre-trained encoder over the incumbent to pre-training. The control
shows that about **four-fifths of that improvement comes from the
architecture alone** — passing the gauges through a 64-unit nonlinear layer,
even one that never learned anything — and about one-fifth from what
pre-training learned.

| n | raw → pre-trained | random layer alone | pre-training learned |
|---|---:|---:|---:|
| 50 | 27.2 | 21.5 (79%) | 5.7 — smaller than its spread |
| 100 | 38.8 | 30.8 (79%) | 8.0 |
| 250 | 37.4 | 29.6 (79%) | 7.8 |
| 1,000 | 38.6 | 31.5 (82%) | 7.1 |

- The random encoder beats the incumbent at every n, clearly (gaps 21.5 to
  31.5 against SDs of at most 6.6).
- Pre-training adds a roughly constant 6–8 MPa² over the random encoder.
  That edge **becomes measurable at n = 100**; at 50 it is smaller than its
  spread (5.7 vs 12.0). It does not *begin* at 100 — the gap is about the
  same size throughout; the SD is what shrinks.
- So the row does not rule out a pre-training benefit; it **isolates** it.
- **Why any nonlinear layer helps this much** — it ties back to Q1. Ridge on
  64 nonlinear features can use nonlinear combinations of the gauges; it
  weights the useful ones and ignores the rest. A ReLU unit is
  max(0, weighted sum of gauges): a threshold, the contamination shape; sums
  of such hinges approximate products like flow × cure. The incumbent fails
  on shape, so any nonlinear features fix most of it, and pre-training adds
  the last fifth.
- **Caveat.** Only one random encoder was tested; its row's SD covers the
  label draws, not encoder-to-encoder variation. A random network is itself
  a random object, so the 80/20 split rests on one random draw.

## Q4. Where does the ordering change? (frozen vs scratch)

**Answer.** The means cross between 100 and 250 labels. From 250 on,
training from scratch is ahead — marginally at 250 and clearly at 1,000.
Below 250 the two cannot be told apart: frozen's lower means at 50 and 100
are smaller than their spread. The table cannot confirm the frozen encoder
is ever ahead.

- Four label counts bracket the crossover; they do not locate it within
  100–250.
- **Why scratch overtakes frozen.** Not the architecture — both rows share
  the 160 → 64 nonlinear layer. The difference is what the 64 features are
  aimed at: frozen's were learned to rebuild gauges and then fixed, so ridge
  can only re-weight them and the row levels off (10.8 → 8.9 from 250 to
  1,000); scratch learns its features for strength and keeps improving
  (7.8 → 3.5).
- **Why so early**, against Handout 9's general rule (freeze at tens,
  fine-tune at hundreds to thousands, scratch at tens of thousands): the
  gauges reflect a handful of underlying conditions and the noise floor is
  at most 3.5, so this is a simple problem that a small network learns from
  a few hundred panels. Fine-tuned ≈ scratch from 250 agrees.
- This is the crossover between scratch and the *frozen encoder*; the
  crossover between scratch and the *incumbent* is a different one
  (scratch is clearly ahead of the incumbent from n = 100).

---

## Carried into the memo questions (decisions still mine)

- Memo Q1 — which number settles it: 0.7 MPa² for quadrupling the labels,
  or 47.5 vs 3.5 on the same panels.
- Memo Q2 — method to deploy at Kestrel's current 2,000 labels (the table
  stops at 1,000) and its error against the incumbent's.
- Memo Q3 — test budget for the next panel family: pre-training's
  advantage is gone within the low hundreds of labels on this problem;
  give a number, both sides of it, and the money at $4,400 per panel
  against the engineer's 2,000 ($8.8M).
