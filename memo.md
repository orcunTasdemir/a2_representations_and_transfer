---
title: "Memo"
---

<div class="head">
**To:** Head of Quality, Kestrel Composites\
**From:** Orcun Tasdemir\
**Date:** 5 November 2026\
**Re:** The proposal to fund 2,000 more destructive tests ($8.8 million): a second opinion
</div>

**Recommendation.** Do not fund the 2,000 additional tests. More tests will not fix the current model: its error has stopped falling, and the cause is the model's straight-line form, not a lack of data. Instead:

1. **Now:** replace the current model with a small neural network trained on the 2,000 panels already tested and built on the 20,000 untested gauge traces. On tested panels it never saw, its typical miss is **1.7 MPa, against 6.8 MPa for the current model**.
2. **Next panel family:** budget **up to 1,200 destructive tests ($5.28M)**: 1,000 to train the model and 200 to check its accuracy. Release them in batches and stop when a batch stops paying. This ceiling is $3.52M (40%) below the proposal.

**How this was measured.** I fitted five methods on 50, 100, 250 and 1,000 tested panels, repeating each fit on five random selections of panels. I scored every fit on the *dev set*: 1,000 tested panels never used for fitting (Exhibit 1). Error is the mean squared error (MSE, in MPa²); its square root, the *typical miss* in MPa, is shown in brackets. I treat two results as different only when the gap exceeds the larger standard deviation (SD) across the repeated fits. For scale, predicting the average strength for every panel scores 188.9 (13.7 MPa).

### 1. Will more destructive tests fix the current model? No.

**The number that settles it:** 750 more tests (from 250 to 1,000 panels, $3.3M) improved the current model by **0.7 MPa²** (48.2 → 47.5). That gain is about the size of its run-to-run spread. Fitting on all 2,000 panels moved it another 0.6 (typical miss 6.89 → 6.85 MPa). This design cannot separate that change from noise, and it is too small to matter even if real.

**The model is not short of data; its form is wrong.** The current model does learn: its error falls from 60.7 at 50 panels to 47.5 at 1,000, where it is 3.98× better than predicting the average and explains 75% of the variation. But a neural network fitted on the **same** 1,000 panels reaches **3.5 ± 0.1**, against **47.5 ± 0.4**. So the noise the gauges cannot explain is at most about 3.5, and **44.0 MPa² — 93% of the current model's error — comes from its form.** More tests cannot remove that.

**Why the form fails.** Process Engineering describes strength in three facts: resin flow and cure must both go right, and the two failure modes multiply; a surplus in one cannot make up for a deficit in the other; contamination does nothing below a threshold and causes a sharp fall above it. The current model is a weighted sum of gauges. A weighted sum assumes that a surplus in one gauge offsets a deficit in another, and it cannot draw a threshold. The limit belongs to a model that is linear in these 160 raw gauges, not to the data.

### 2. Can the untested traces be made useful? Yes — but at today's label count they add no accuracy.

**What pre-training does.** *Pre-training* hides 30% of each panel's gauges and trains a network to rebuild them. It needs no destructive tests. To rebuild hidden gauges, the network must learn the few process conditions behind the 160 redundant gauges.

**Pre-training beats the current model, but most of that gain is not pre-training.** A *frozen* pre-trained network (its weights fixed, with the current model's fitting method applied to its 64 outputs) beats the current model clearly at every label count: 33.5 vs 60.7 at 50 panels, 8.9 vs 47.5 at 1,000. The control is the same network with random, never-trained weights. It captures **79–82%** of that improvement: at 1,000 panels, pre-training adds only 7.1 of the 38.6 MPa² gained. Without the control, pre-training would have received credit for all 38.6. The control works because its units are thresholds, and sums of thresholds can form both the threshold and the multiplication the process needs. Pre-training's own 7–8 MPa² is measurable from 100 panels; at 50 it is smaller than its spread.

**Against a network trained only on tested panels ("from scratch"), pre-training adds nothing this study can resolve.**

- *Frozen vs scratch.* The frozen network has the lower average at 50 and 100 panels (33.5 vs 47.0; 17.6 vs 23.3), but both gaps are smaller than their spread. The ordering changes between 100 and 250 panels: from 250 the scratch network leads, marginally at 250 and clearly at 1,000 (3.5 vs 8.9). Below 250 the two cannot be told apart.
- *Why scratch overtakes.* The scratch network learns its features for strength; the frozen network's features were fixed to rebuild gauges. This happens within a few hundred panels, far earlier than the usual rule of tens of thousands, because a handful of conditions drive this process.
- *Fine-tuned vs scratch.* A *fine-tuned* network starts from the pre-trained weights and keeps training on tested panels. It cannot be told apart from scratch: too noisy at 50–100 panels, and equal from 250 (3.6 vs 3.5 at 1,000; 3.1 vs 3.0 at 2,000).

**What to deploy now.** The fine-tuned network trained on all 2,000 panels: **3.1 ± 0.2 (1.7 MPa), against 46.9 (6.8 MPa) for the current model.** It ties the scratch network. I choose it because the pre-trained network costs seconds to build and stays available for two uses: the next panel family, and flagging new panels whose gauges it cannot rebuild — panels unlike any seen before, and natural candidates for a destructive test.

**How to run it.**

- Run one network and record its random seed.
- In operation the model predicts every panel. Only panels predicted near the specification limit get a destructive test; those tests become new labels.
- Retrain periodically by re-running the same recipe on all panels tested to date. Swap the new version in only if it scores at least as well on a random check set (champion against challenger).
- Keep destructively testing a small random sample of production every period. Without it the training data drifts towards panels near the limit, and errors elsewhere go unseen (a feedback loop).
- Refresh the pre-training as traces accumulate.

### 3. How many tests should the next panel family budget? Up to 1,200 ($5.28M), released in batches.

These tests build the model. They are one-off, and separate from the routine tests in operation.

1. **Test 200 check panels first** ($0.88M), drawn at random. Use them only to measure accuracy; 200 panels measure the error to about ±10%.
2. **Test training panels at random, in batches** to 100, 250, 500 and 1,000. After each batch, fine-tune the network on all training panels so far and score it on the check panels. Keep fine-tuning's reduced learning rate, which protects the pre-trained weights. (The curves below assume random selection.)
3. **Stop when the last batch improved check-panel error by less than the check panels can measure** (about 10%). The next batch's gain would be smaller still, and could not even be seen.
4. **Price each batch before buying it.** Count the check panels the current model would send for a destructive test in operation (predicted within its typical miss of the limit). Assume the next batch improves accuracy by no more than the last one did. Compare the resulting yearly reduction in tests × $4,400 × years in use with the batch's cost: each further 250 training panels costs $1.1M. This step needs the specification limit and the annual volume, which Kestrel has and this study does not.

**Why fine-tune from the first batch.** At 50 and 100 panels no method can be told apart, so fine-tuning loses nothing measurable; from 250 it is clearly the best; and the extension below shows it does not need a large trace pool. Its cost: at 50–100 panels its results vary most between runs (SD 21.1 at 50), so one early model can land well above or below its average. The check panels catch that.

**Either side of 1,000 training panels**, on this family: at 250 the fine-tuned error is 7.2 (2.7 MPa), for $1.98M in all; at 1,000 it halves to 3.6 (1.9 MPa); going on to 2,000 bought only 3.1 (1.7 MPa), for $4.4M more. So **budget 1,000 if the specification needs a typical miss near 2 MPa; stop at 250 if about 3 MPa is enough.** No budget gets below the noise: at most 3.0 (1.7 MPa) on this family. Against the proposed 2,000 tests ($8.8M), the full ceiling saves $3.52M.

### Optional extension: how much untested data does pre-training need?

This is the question for a plant that has just installed its gauges, or for a new panel family. I pre-trained three networks on the first 2,000 traces instead of all 20,000, with the same recipe of 40 passes over the traces. That also means 10× fewer training steps. I kept the recipe on purpose: a new plant would run the standard recipe on the traces it has, with no larger pool to match. So this result does not separate "less data" from "less training".

- **Frozen:** worse than the 20,000-trace version at every label count, readably from 250 panels (15.5 vs 10.8; 12.1 vs 8.9 at 1,000). It beats the random-weight control only from 250 panels (by 3.1 and 3.8); at 50 and 100 panels it cannot be told apart from a network that learned nothing.
- **Fine-tuned:** unaffected at every label count (7.8 vs 7.2 at 250; 3.7 vs 3.6 at 1,000; every gap within the spread).

**Implication.** The frozen shortcut needs a large trace pool before it beats a random network; fine-tuning does not. A new plant or panel family should fine-tune from the first batch rather than wait for traces to accumulate. That is why step 2 above fine-tunes from the start.

**Held-out check.** I fixed the recommended pipeline before opening the *test set*, a further 1,000 tested panels, and scored it there once: **2.87 (1.69 MPa) on test, against 3.01 (1.74 MPa) on dev.** The difference, −0.14, is smaller than the 0.24 SD the same network shows across retraining runs, and consistent with the test set's slightly lower spread of strength.

### What this evidence does not establish

- **That the next family behaves like this one.** Every curve above is this family's; the batches exist so the new family's own numbers decide.
- **Anything beyond 2,000 panels.** The spread at 2,000 reflects retraining only, not which panels were tested.
- **The noise level.** It is bounded at about 3, not measured.
- **Pre-training's value at 50–100 panels**, where it should matter most and where a new family starts: the spread is too wide to tell.
- **The 80/20 split beyond one random network**, since only one was tested.
- **Less data vs less training** in the extension, and whether an even lower fine-tuning rate helps with very few panels (untested).
- **Robustness to changing conditions**, or the flagging use: all panels come from one autoclave and one period.

<div class="exhibit">

### Exhibit 1. Five methods at four label counts, scored on the 1,000-panel dev set

Mean squared error in MPa², mean ± standard deviation over runs; typical miss (RMSE, MPa) in brackets. Lower is better.

| Method | 50 panels | 100 panels | 250 panels | 1,000 panels | Runs per cell |
|---|---:|---:|---:|---:|---:|
| Current model: ridge on the 160 raw gauges | 60.7 ± 5.6 (7.8) | 56.5 ± 6.3 (7.5) | 48.2 ± 0.6 (6.9) | 47.5 ± 0.4 (6.9) | 5 |
| Frozen pre-trained network + ridge | 33.5 ± 12.0 (5.8) | 17.6 ± 5.4 (4.2) | 10.8 ± 2.9 (3.3) | 8.9 ± 2.3 (3.0) | 15 |
| Frozen *random* network + ridge (control) | 39.2 ± 6.6 (6.3) | 25.6 ± 3.5 (5.1) | 18.6 ± 0.8 (4.3) | 16.0 ± 0.2 (4.0) | 5 |
| Network trained from scratch | 47.0 ± 17.8 (6.9) | 23.3 ± 9.4 (4.8) | 7.8 ± 1.5 (2.8) | 3.5 ± 0.1 (1.9) | 5 |
| Fine-tuned pre-trained network | 45.2 ± 21.1 (6.7) | 21.3 ± 5.0 (4.6) | 7.2 ± 0.5 (2.7) | 3.6 ± 0.3 (1.9) | 5 |
| *Reference: predict the average of the tested panels* | 190.2 ± 2.5 (13.8) | 189.4 ± 0.6 (13.8) | 189.4 ± 0.3 (13.8) | 188.9 ± 0.1 (13.7) | 5 |

Runs: five random selections of tested panels per label count; the frozen pre-trained row also crosses them with three independent pre-training runs; fine-tuning on selection *r* starts from pre-training run *r* mod 3. Pre-training uses the 20,000 untested traces only. The 2,000-panel figures in the text use all tested panels with five retraining seeds (`analysis/outputs/all_labels.md`); the extension's figures are in `analysis/outputs/extension2.md`. Every figure in this memo is produced by `python analysis/run.py`.

</div>
