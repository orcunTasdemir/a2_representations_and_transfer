# Expectations, written before Exhibit 1 was run

Written by me (in chat, session 1, 2026-11-01) before any model in the table
was fitted, then recorded here. My answers are in my words, typos lightly
corrected. The agent's comments from the discussion are marked separately;
where they corrected my reasoning, that is noted.

The only number known at the time: predicting the mean strength scores
**MSE 188.9 MPa²** on dev (RMSE 13.7 MPa). Every error below is dev MSE in
MPa²; lower is better, 0 is perfect, 188.9 is "the gauges told us nothing".

Not a deliverable. Kept so the table has something to be compared against,
and as evidence for the process note.

---

## 1. Ridge on the 160 raw gauges (the incumbent)

**Mine.** At n = 50, near 188.9, since that is very little training data. At
n = 1,000, far below, but there should be a bias threshold it can't go under,
since the model is the wrong shape for the question. It should flatten out
for the same reason.

*Earlier, rejected after discussion:* "1,000 is not enough for a linear
model, with collinear and non-linear columns." Ridge handles collinearity,
and 1,000 rows for 161 coefficients is not scarce; the wrong-shape part is
what survived.

**Agent's comments.** Ridge's penalty shrinks toward predicting the mean, so
at n = 50 it tends to fall back toward 188.9 rather than far past it; but the
penalty is chosen on 13 panels, so expect a large SD. A flat curve alone does
not prove bias: irreducible noise also flattens it. What separates the two is
ridge against the networks at the same n. If a flexible model beats ridge on
the same panels, the gap is ridge's shape, not noise.

## 2. Frozen pre-trained encoder + ridge

**Mine.** At n = 50, slightly better or the same as raw ridge, since 64 is
still bigger than 50. At 1,000, much better, since the learned representation
is easier for a linear model to fit than the raw columns: ridge is now linear
in the representation. It also has fewer coefficients to learn (64).

**Agent's comments.** Two separate reasons, acting at different ends: fewer
coefficients (compression) reduces variance, which matters most at *small* n;
nonlinear features (shape) matter at every n and are the only thing still
helping at large n. Feature count vs rows is not the barrier (raw ridge
already had 160 > 50); what matters is whether the signal is concentrated in
few directions. "Definitely" is too strong: the encoder was trained to
rebuild gauges, not predict strength, so flow × cure need not be linearly
available in its 64 features, and frozen features have their own floor.

## 3. Frozen random encoder + ridge (the control)

**Mine.** Closer to raw ridge: a representation only matters if there is an
information benefit, and a random one should be very similar to the raw
inputs. If it were close to the pre-trained row instead, pre-training did not
help and the improvement came from the shape of the encoder. It could be
worse than raw ridge because it is random: it might amplify features that do
not matter and weaken ones that do.

**Agent's comments.** Interpretation is right: row 1 → row 3 is what the
architecture alone buys, row 3 → row 2 is what pre-training learned. But a
random ReLU layer is not neutral: random nonlinear features can help on their
own (that is why the control is required), while the random 160 → 64
projection and ReLU zeroing can lose information. Ridge re-weights features,
so "amplifying the wrong ones" is not the risk; lost information is.

**Added after Exhibit 1 was run (not a pre-result expectation).** I had
pictured the random encoder on its own and missed that a ridge head is
trained on top of it. Knowing that, I would have said it *could* beat raw
ridge, but not for sure: random features can help or hurt, and there was no
way to know before running it. Result: it beat raw ridge at every n.

## 4. Network from scratch

**Mine.** At n = 50, depends on the learning rate: low, similar to raw ridge;
high, much higher or lower error. At 1,000, assuming that is enough data for
the network to learn the concept, better than raw ridge, but the point where
it overtakes ridge may be higher, like 2,000–3,000.

*Corrected:* I first described the frozen random encoder as trained on the
pretext task. It is never trained; that is the pre-trained row.

**Agent's comments.** The learning rate is fixed by the protocol (2e-3), so
it does not vary here. What decides n = 50: ~10,400 weights from 37 panels,
early stopping judged on 13, centring that pulls an early-stopped network
toward the mean, and random initialisation. Expect around baseline or raw
ridge, possibly worse, with a large SD. Handout 9's "scratch at tens of
thousands" compares scratch to pre-trained methods, not to raw ridge.

## 5. Fine-tuned encoder

**Mine.** Against scratch, helps more at small n: pre-learned
representations make up for a lack of labelled data; the network
understands the shape and tendencies of the data before training on the
task. Against frozen, at low n it might hurt because it might over-adjust to
limited data; at medium n it is worth it; with very much data the best is to
train from scratch. The lower learning rate is because it might over-adjust
to the limited labelled data.

**Agent's comments.** (a) and (b) match Handout 9 §3.1–3.2. Our table stops
at 1,000, so the "scratch at tens of thousands" end cannot be observed; and
at large n fine-tuning's advantage usually shrinks to zero rather than
turning negative. (c) The main reason for the low rate is protecting the
starting point: the new output layer is random, its early gradients are
large and noisy, and big steps would overwrite what pre-training learned.
Overfitting is early stopping's job.

## 6. Spread (standard deviations)

**Mine.** Largest at n = 50: least information, most dependent on which 50
are chosen. Largest row: network from scratch, since it starts from random
and networks need more data than linear models. The frozen pre-trained row
has 3 encoders; I expected that to smooth over and decrease the SD, since SD
has n or n − 1 in the denominator.

*Corrected:* more runs do not make the SD smaller; they make it a better
estimate of the spread. The standard error of the mean (SD/√k) is what
shrinks. A second source of randomness (which encoder) *adds* variance, so
the frozen row's SD should be larger or equal. Averaging over encoders makes
its *mean* more trustworthy, not its SD smaller. Also: "performs worst" is a
claim about the mean, not the SD; the case for scratch having the largest SD
is the number of random choices per run (init, split, stopping point).

## 7. Crossover (frozen pre-trained vs scratch)

**Mine.** At 50, frozen encoder + ridge will be best. Scratch and fine-tune
will get better and pass the frozen encoder as we go from 50 to 1,000. If
there is no flip, the data might just not be enough.

**Committed bracket (mine).** Between 250 and 1,000; my guess is nearer the
top of that range. (I first said "500 to 1,000", misremembering 500 as one of
the label counts; a bracket's ends must be measured counts.)

**Agent's comments.** Bracketing explained: state the flip as "between two
measured n", never a point; where the two are within one SD, that n cannot
narrow the bracket. Still to commit to: a specific bracket, and whether at
n = 50 frozen is *clearly* ahead or only within one SD. No flip by 1,000
means a one-sided bracket ("above 1,000"); the table says nothing about
1,000–2,000, where Kestrel already is.

## 8. What would look too good, or wrong

**Mine.** A model doing significantly worse than 188.9. Fine-tuning or
scratch getting worse as n increases. (Random encoder matching pre-trained
everywhere: could be true, maybe the crossover is beyond 1,000.) n = 50
models doing very well would suggest leakage.

**Agent's comments.** Slightly above 188.9 at n = 50 can be honest noise; at
n = 1,000 it means a bug (misaligned rows, mean not added back, wrong y).
Getting worse with n is a flag for *every* row, beyond its SD. Random ≥
pre-trained is not the crossover question; it is either a genuine §3.3
finding or a failed/mis-wired pre-training, checkable by comparing masked
reconstruction error of pre-trained vs random encoders. Anything near 0 at
any n is a bug until shown otherwise.

---

## Addendum — n = 2,000 (all training labels), written 2026-11-03 before it was run

**Mine.** The incumbent might not improve at all: it is at or around the
limit of its shape. Frozen pre-trained + ridge will get better but not
surpass the other two. Scratch and fine-tuned will stay the same or get
very slightly better; the ordering will not change. Scratch will win: the
labelled data is already enough for this architecture to learn the problem,
since its shape suits this problem.

---

## Addendum — the single test score, written 2026-11-03 before it was run

**Mine.** Even if the test MSE comes out slightly lower than the dev 3.01, it
will most likely not be decisive: the difference will be smaller than the
spread.

Made checkable (agreed wording): the test MSE will differ from the dev 3.01
by less than the run-to-run spread on dev at n = 2,000 (SD 0.2; runs ranged
2.67–3.31). The test score is one run, so it has no SD of its own.

**Result (added after the run).** Test MSE 2.87 vs dev 3.01: −0.14, smaller
than the dev run-to-run SD (0.24) and inside the 2.67–3.31 range. As
expected: slightly lower, not decisive.
