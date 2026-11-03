---
title: "Memo"
---

<div class="head">
**To:** Head of Quality, Kestrel Composites\
**From:** Orcun Tasdemir\
**Date:** 3 November 2026\
**Re:** The proposal to fund 2,000 more destructive tests ($8.8 million): a second opinion
</div>

**Recommendation.** Do not fund the 2,000 additional tests. They would not fix the current model: its error has stopped falling, because a straight-line model cannot represent how strength arises. Replace it now with a small neural network trained on the 2,000 panels already tested and built on the 20,000 untested gauge traces: on 1,000 tested panels held out from all fitting, its typical error is **1.7 MPa against the current model's 6.8 MPa**. For the next panel family, budget **up to 1,200 destructive tests ($5.28M)** — 1,000 to train on and 200 kept aside to check accuracy — released in stages and stopped as soon as a further batch costs more than it saves. That ceiling is $3.52M (40%) below the proposal, before any early stop.

**How this was measured.** Every method was fitted on 50, 100, 250 and 1,000 tested panels, each time on five different random selections of panels, and scored on 1,000 further tested panels it never saw (Exhibit 1). Error is the mean squared error (MSE, in MPa²); its square root, the typical miss in MPa, is shown in brackets. A difference smaller than the run-to-run standard deviation (SD) is not read as a difference. Predicting the average strength for every panel scores 188.9 (13.7 MPa).

### 1. Will more destructive tests fix the current model? No.

**The number that settles it:** going from 250 to 1,000 tested panels — 750 tests, $3.3M — improved the current model by **0.7 MPa²** (48.2 → 47.5), about the size of its run-to-run spread. Using all 2,000 panels moved it a further 0.6 (typical miss 6.89 → 6.85 MPa): a change this design cannot separate from noise, and too small to matter even if real.

The model is not short of data. It does learn from the gauges — its error falls from 60.7 at 50 panels to 47.5 at 1,000, where it is 3.98× better than predicting the average and explains 75% of the variation — but it stops there. On the **same** 1,000 panels a neural network reaches **3.5 ± 0.1** where the current model sits at **47.5 ± 0.4**, so whatever noise the gauges cannot explain is at most about 3.5, and **44.0 MPa², 93% of the current model's error, is the model's form, not noise.** More tests cannot remove that.

The reason is the process itself. Process Engineering's account is that resin flow and cure must *both* go right, that the two failure modes multiply, and that a surplus in one cannot make up for a deficit in the other. A weighted sum of gauges assumes exactly that trade-off. Contamination acts through a threshold — no effect below it, a sharp fall above — which a straight line cannot represent either. The limit belongs to a model that is linear in these 160 raw gauges; it is not a limit of the data.

### 2. Can the unlabelled traces be made useful? Yes — but at today's label count, not for accuracy.

The traces are used by *pre-training*: hide 30% of each panel's gauges and train a network to rebuild them. No destructive test is needed, and the network learns the few underlying conditions behind the 160 redundant gauges. Freezing that network and fitting the current model's method on its 64 outputs beats the current model at every label count, clearly (33.5 vs 60.7 at 50 panels; 8.9 vs 47.5 at 1,000).

**Most of that gain is not pre-training.** The same network with random, never-trained weights captures **79–82%** of the improvement: at 1,000 panels, pre-training adds 7.1 of the 38.6 MPa² gained. Without this control, pre-training would have been credited with all of it. Passing the gauges through *any* layer of threshold-like units helps, because thresholds, and sums of them, are the shapes the process needs (the threshold, the multiplication). Pre-training's own contribution, 7–8 MPa², is measurable from 100 panels; at 50 it is smaller than its spread.

**Against a network trained from scratch on the tested panels alone, pre-training buys nothing this study can resolve.** The frozen network has lower average error at 50 and 100 panels (33.5 vs 47.0; 17.6 vs 23.3), but both gaps are smaller than their spread. The ordering changes between 100 and 250 panels: from 250 the network trained from scratch is ahead — marginally at 250, clearly at 1,000 (3.5 vs 8.9) — and below 250 the two cannot be told apart. It overtakes because its features are learned for strength, while the frozen network's were fixed to rebuild gauges; and it does so within a few hundred panels, far earlier than the usual rule of tens of thousands, because this is a simple problem driven by a handful of conditions. Starting the network from the pre-trained one ("fine-tuning") makes no measurable difference: too noisy to tell at 50–100 panels, genuinely equal from 250 (3.6 vs 3.5 at 1,000; 3.1 vs 3.0 at 2,000).

**What to deploy now:** the fine-tuned network trained on all 2,000 panels — **3.1 ± 0.2 (1.7 MPa) against the current model's 46.9 (6.8 MPa)**. It ties the network trained from scratch; I choose it because building the pre-trained network takes seconds and keeps it available for the next panel family, where tested panels are scarce, and for flagging new panels whose gauges it cannot rebuild — panels unlike anything seen before, and natural candidates for a destructive test. Run it as a single network with its random seed recorded, retrain it as tests accumulate, and refresh the pre-training as traces accumulate.

### 3. How many tests should the next panel family budget? Up to 1,200 ($5.28M), in stages.

Test 200 check panels first ($0.88M) and set them aside; they only ever measure accuracy, to about ±10%. Then test training panels in batches — to 100, 250, 500 and 1,000 — refitting after each and scoring on the check panels: the frozen network while panels number in the tens to low hundreds, fine-tuning from about 250. **Continue only if the next batch is expected to save more than it costs** in tests avoided or weak panels caught; each further 250 training panels costs $1.1M. Kestrel has to supply that value; this study cannot.

Either side of 1,000, on this family: at 250 training panels the network's error is 7.2 (2.7 MPa) for $1.98M in all; reaching 1,000 halves it to 3.6 (1.9 MPa); going on to 2,000 bought only 3.1 (1.7 MPa) for $4.4M more. So **1,000 is the number if the specification needs a typical miss near 2 MPa; stop at 250 if about 3 MPa will do.** No budget gets below the noise, at most 3.0 (1.7 MPa) on this family. Against the proposed 2,000 tests ($8.8M), the full ceiling saves $3.52M.

**Held-out check.** The recommended pipeline was fixed before the final extract was opened and scored on it once: **2.87 (1.69 MPa) against 3.01 (1.74 MPa) on the comparison extract**. The difference, −0.14, is smaller than the 0.24 SD the same network shows across retraining runs, and consistent with that extract's slightly lower spread of strength.

### What this evidence does not establish

- **That the next family behaves like this one.** Every curve above is this family's; staging exists so the new family's own numbers decide.
- **Anything beyond 2,000 panels**, and the spread at 2,000 reflects retraining only, not which panels were tested.
- **The noise level** — bounded at about 3, not measured.
- **Pre-training's value at 50–100 panels**, where it should matter most and where the next family starts: the spread is too wide to tell.
- **The 80/20 split beyond one random network**, since only one was tested.
- **Robustness to changing conditions**, or the flagging use: all panels come from one autoclave and period.

<div class="exhibit">

### Exhibit 1. Five methods at four label counts, scored on the 1,000-panel comparison extract

Mean squared error in MPa², mean ± standard deviation over runs; typical miss (RMSE, MPa) in brackets. Lower is better.

| Method | 50 panels | 100 panels | 250 panels | 1,000 panels | Runs per cell |
|---|---:|---:|---:|---:|---:|
| Current model: ridge on the 160 raw gauges | 60.7 ± 5.6 (7.8) | 56.5 ± 6.3 (7.5) | 48.2 ± 0.6 (6.9) | 47.5 ± 0.4 (6.9) | 5 |
| Frozen pre-trained network + ridge | 33.5 ± 12.0 (5.8) | 17.6 ± 5.4 (4.2) | 10.8 ± 2.9 (3.3) | 8.9 ± 2.3 (3.0) | 15 |
| Frozen *random* network + ridge (control) | 39.2 ± 6.6 (6.3) | 25.6 ± 3.5 (5.1) | 18.6 ± 0.8 (4.3) | 16.0 ± 0.2 (4.0) | 5 |
| Network trained from scratch | 47.0 ± 17.8 (6.9) | 23.3 ± 9.4 (4.8) | 7.8 ± 1.5 (2.8) | 3.5 ± 0.1 (1.9) | 5 |
| Fine-tuned pre-trained network | 45.2 ± 21.1 (6.7) | 21.3 ± 5.0 (4.6) | 7.2 ± 0.5 (2.7) | 3.6 ± 0.3 (1.9) | 5 |
| *Reference: predict the average of the tested panels* | 190.2 ± 2.5 (13.8) | 189.4 ± 0.6 (13.8) | 189.4 ± 0.3 (13.8) | 188.9 ± 0.1 (13.7) | 5 |

Runs: five random selections of tested panels per label count; the frozen pre-trained row also crosses them with three independent pre-training runs; fine-tuning on selection *r* starts from pre-training run *r* mod 3. Pre-training uses the 20,000 untested traces only. The 2,000-panel figures quoted in the text use all tested panels with five retraining seeds (`analysis/outputs/all_labels.md`). Every figure in this memo is produced by `python analysis/run.py`.

</div>
