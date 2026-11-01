# Assignment 2 — Learning a representation without labels

**IDS 575: Machine Learning and Statistical Methods for Business Analytics · Fall 2026**
Released Wednesday, October 14 · **Due Thursday, November 5, 6:00 PM Central** · 10% of course grade

Covers Lectures 6, 7 and 9: learned representations, training with early stopping, self-supervised pre-training, frozen representations, and fine-tuning.

Expected effort: **4–6 focused hours**. The architectures, learning rates, sample sizes and splits are fixed for you below and implemented in `starter/kestrel.py`. You will not have to write a neural network or a training loop. Your work is to run one comparison, read it, and make a recommendation.

Running the code needs only Lectures 6 and 7, which you have already had, so build the table in the first week. Lecture 9 on 22 October is what tells you how to read it, and Midterm 2 on 29 October covers the same material — so working through the table before the exam is good preparation for it. Handout 9 is posted with Lecture 9; until then, the summary under *What Handout 9 gives you* below is everything you need to build the table. The deadline falls a week after the exam so that you are not doing both in the same week.

---

## The situation

Kestrel Composites cures carbon-fibre panels for aircraft interiors. Every panel is cured in an instrumented autoclave that logs **160 process gauges**. Quality control is done by **destructive testing**: a panel is loaded to failure in a press and its interlaminar shear strength recorded.

Destructive testing is expensive. Each test costs about **$1,400 in lab time and destroys a $3,000 panel**. Over five years the lab has tested **2,000 panels**. Meanwhile every panel ever cured — **20,000 of them** — has a complete gauge trace sitting in the historian, unlabelled and unused.

Quality wants to predict strength from the gauges and test only the panels the model is unsure about. An engineer has fitted a regularized linear model on the 160 gauges. It is not accurate enough, and his read is that the fix is more data:

> "We're at 2,000 tested panels. The model is still well short of what the spec needs. My recommendation is to budget another 2,000 tests over the next two years and re-fit."

The Head of Quality wants a second opinion before signing off on **$8.8 million** of destroyed panels and lab time.

## The three questions

> 1. Will more destructive tests fix the current model?
> 2. Can the 20,000 unlabelled traces be made useful?
> 3. For the next panel family, how many destructive tests should Kestrel budget?

You are not trying to win a modelling competition. There are no marks for beating the models prescribed below.

---

## What Handout 9 gives you

Handout 9 establishes, with numbers, the results this assignment applies. You are not asked to rediscover them.

- **§2** — self-supervised pre-training: hide part of an input, ask a network to rebuild it, and you have a training signal that needs no labels.
- **§2.1** — the three ways to use the resulting encoder: freeze it and fit something simple on top, fine-tune it, or ignore it and train from scratch.
- **§3.1–3.2** — pre-training substitutes for labelled data, so its value is greatest where labels are scarcest and shrinks as they accumulate. The rule by label regime: freeze at tens of labels, fine-tune at hundreds to thousands, train from scratch at tens of thousands.
- **§3.3** — the control that is usually omitted: an untrained encoder of identical shape. Without it you cannot separate "pre-training learned something" from "this architecture makes useful random features."

Your job is to apply these to Kestrel's data and say what they imply for Kestrel's budget.

---

## The protocol

Fixed, and implemented in `starter/kestrel.py`. You should not need to change any of it.

| | Value |
|---|---|
| Label counts | *n* ∈ {50, 100, 250, 1000}, drawn from the 2,000 labelled panels |
| Label draws | **5 per cell**, from `label_subset(n, replicate)` |
| Pre-training seeds | **3** — pre-train three encoders, once each, and reuse them in every cell |
| Pre-training | Masked reconstruction: hide 30% of the gauges, rebuild them. 40 epochs, Adam at 3e-3 |
| Encoder | 160 → 64 → 16 → 160. The **representation is the first hidden layer**, 64 numbers |
| Frozen head | Ridge on those 64 numbers |
| Incumbent baseline | The same ridge, on the 160 raw gauges |
| From scratch | 160 → 64 → 1, Adam at 2e-3 |
| Fine-tuning | The same network started from the pre-trained encoder, Adam at 1e-3 |
| Early stopping | 25% inner validation split, patience 60, at most 800 epochs |
| Evaluation | `labeled_dev.csv` for everything in Part 1 |

**Why five label draws and three pre-training seeds.** Both are sources of variation and both are large here. With 50 labels the answer depends on *which* 50 panels happened to get tested, and a pre-trained encoder is itself a random object — two runs of the same pre-training produce different representations. At *n* = 50 the standard deviation across runs is bigger than several of the gaps you will be comparing. Report the standard deviation next to every mean, and do not read a difference smaller than it.

**What each cell averages over.** Use these run counts, so that every submission's table is comparable:

| Row | Runs per cell |
|---|---|
| Ridge on the raw gauges | 5 — one per label draw, `seed=replicate` |
| Frozen encoder + ridge | 15 — each of the 3 encoders × 5 label draws |
| Frozen random encoder + ridge | 5 — one `random_encoder()` × 5 label draws |
| Network from scratch | 5 — one per label draw, `seed=replicate` |
| Fine-tuned encoder | 5 — one per label draw, `seed=replicate`, draw *r* starting from encoder *r* mod 3, so all three encoders are used |

**Pre-train once per seed, outside your label loop.** Pre-training is the only slow step, about 10 seconds. Nothing about it depends on the labels. Doing it inside the loop turns a two-minute analysis into an hour.

**Two evaluation extracts.** Everything you compare is scored on `labeled_dev.csv`. `labeled_test.csv` is scored once, on the single pipeline you recommend. Anything you decide by looking at data is decided on dev.

---

## Part 1 — One table

**Exhibit 1.** Five methods at four label counts, scored on the dev extract, each cell a mean and a standard deviation:

1. **Ridge on the 160 raw gauges** — the incumbent.
2. **Frozen encoder + ridge** — pre-train on the unlabelled traces, freeze, fit ridge on the representation.
3. **Frozen random encoder + ridge** — the control Handout 9 §3.3 requires.
4. **Network from scratch.**
5. **Fine-tuned encoder.**

`starter/kestrel.py` has one function for each. The whole table is two nested loops.

Then answer, in the memo:

1. **What happens to the incumbent as labels accumulate?** Compare its error at *n* = 50 against *n* = 1000, and against the error you would get by ignoring the gauges entirely and predicting the mean strength. Say what kind of limit this is — a shortage of data, or something else — and how your table tells the two apart.
2. **What does pre-training buy, and at which label counts?** Give the comparison against training from scratch at the same *n*.
3. **What does the random-encoder row rule out?** State what your table would have meant without it.
4. **Where does the ordering change?** Compare the frozen encoder against training from scratch at each label count. Say where the ordering changes, if it does, and where your standard deviations do not let you say. Bracket the crossover — four label counts bracket it, they do not locate it.

## Part 2 — The recommendation

**`memo.pdf` — at most 2 pages of prose plus Exhibit 1**, addressed to the Head of Quality. Answer her three questions in order:

1. **Will more destructive tests fix the current model?** Give the number that settles it.
2. **Can the unlabelled traces be made useful?** Say what method you would deploy at Kestrel's current label count, and what error it gives against the incumbent's.
3. **How many tests should the next panel family budget?** Give a number, and say what happens on either side of it. Convert it to money at $4,400 per tested panel, against the engineer's proposed 2,000.

Then score your recommended pipeline **once** on `labeled_test.csv`, report that number beside its dev counterpart, and note the difference in one sentence.

Close with what your evidence does not establish.

---

## Optional extension (up to 4 bonus points)

Not required, and a wrong answer cannot lower your score. Pick one.

- **Does the pretext task have to be hard?** `pretrain()` takes `mask_fraction`. Try 0.05 and 0.60 alongside the prescribed 0.30 and report what the frozen representation is worth in each case.
- **How much unlabelled data do you need?** Pre-train on the first 2,000 traces instead of all 20,000 and report the difference. Say what that implies for a plant that has just installed the instrumentation.
- **Beat the incumbent honestly.** The linear model fails for a structural reason. Construct a feature set that fixes it without any pre-training, fit the same ridge on it, and say how close it gets and what you had to know to build it. Keep the model a ridge: the point is the features, not a more flexible learner.

---

## Deliverables

Full format in `../00_start_here/04_submission_checklist.md`.

1. **`memo.pdf`** or `.md` — at most 2 pages of prose plus Exhibit 1. The exhibit does not count against the limit.
2. **`analysis/`** — your code, runnable end to end with one command, plus a `README` saying what to run.
3. **`ai_process_note.md`** — at most 1 page. What you delegated, what you rejected or corrected and why, and how you checked the numbers.
4. **`sessions/`** — exported history of every AI session used.

## What is in this folder

```
data/labeled_train.csv         2,000 tested panels — your labels
data/labeled_dev.csv           1,000 tested panels — every comparison
data/labeled_test.csv          1,000 tested panels — scored once
data/unlabeled_traces.csv.gz  20,000 untested panels — gauges only
data/DATA_DICTIONARY.md        read this first
starter/kestrel.py             loaders and all five models
starter/mlp.py                 the network itself; you should not need to open it
rubric.md                      how this is graded
```

`python3 kestrel.py` runs a smoke test in about 15 seconds and prints four numbers. If that works, your environment is fine.

You may use scikit-learn or PyTorch instead. You are not responsible for the hand-written backward pass inside `mlp.py`; you are responsible for knowing what each model consumes, produces, and assumes.

Also on Canvas: the start-here guide (`00_start_here/`), Handout 6 (`lecture06_neural_networks.pdf`) and, from 22 October, Handout 9 (`lecture09_transfer_learning.pdf`).

## Where the concepts are

| For | Read |
|---|---|
| Why a learned representation beats a guessed one | Handout 6, §1 — the comparisons with trees and forests in §1.1–1.2 use methods this course does not cover, and you can skip them |
| What the hidden layers learn — the thing you will be freezing | Handout 6, §4 |
| Self-supervised learning: making a label out of the data | Handout 9, §2 |
| Freeze, fine-tune, or train from scratch | Handout 9, §2.1 |
| The crossover, and the rule by label regime | Handout 9, §3.1–3.2 |
| The random-weights control | Handout 9, §3.3 |
| Which layer to take as the representation | Handout 9, §3.4 |

## Things that commonly go wrong

- **Reporting one run.** The protocol asks for three pre-training seeds and five label draws. At *n* = 50 a single run tells you almost nothing.
- **Reading a difference smaller than its standard deviation.** Some of the comparisons in this table are not resolvable at *n* = 50. Saying so scores better than picking a winner.
- **Pre-training inside the label loop.** This is the difference between two minutes and an hour.
- **Selecting on the test extract.** Compare on dev. Score once on test, on one pipeline.
- **Reporting the study and never answering the question.** The Head of Quality asked for a budget number.
