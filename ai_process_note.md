# AI process note — Assignment 2

Agent: Claude Code (VS Code extension), one conversation across three working sessions, plus one failed start (see `sessions/`).

## What I delegated

- **Implementing the fixed protocol** in `analysis/run.py`: three encoders pre-trained once outside the label loop, the 4 × 5 loop over label counts and draws with the brief's run counts per row, fine-tuning from encoder *r* mod 3; later the 2,000-label run, the staged-budget costs and the single test score.
- **The arithmetic of reading the table.** I asked for gap-vs-SD for every pair I compared, the architecture/pre-training split and the RMSE conversions rather than eyeballing overlaps; each was first computed ad hoc, then moved into `run.py`.
- **Explanations** I needed before deciding anything: label draws, what pre-training and the encoder are, which rows use labelled vs unlabelled data, Adam vs early stopping, SD vs standard error, bracketing.
- **Drafting the memo prose** from decisions I had made, the PDF rendering, and a checker for the memo's numbers.

## What I changed, rejected or corrected

- **Rejected a paired per-draw comparison** the agent offered when frozen vs scratch was unresolvable at 50 and 100 labels. Choosing a sharper test after the prescribed one failed to confirm what theory predicts is motivated analysis; the brief fixes mean ± SD.
- **Overrode the run's mechanical verdict at 2,000 labels.** The incumbent's −0.6 "passed" my gap-vs-SD rule against an SD of 0.4, but all five runs at 2,000 use the same panels, so that SD omits which-panels variation. The memo reports it as indistinguishable from noise.
- **Caught a contradiction in the agent's explanation** before the test score: it said a model's error "doesn't scale with" the variance of strength, then that lower variance could lower the error. Corrected: variance sets the predict-the-mean error exactly; a model's error moves only if the removed spread was in panels it gets wrong.
- **Changed the agent's process:** it handed me an expectations sheet; I had it ask the questions one at a time so each answer was challenged. My wrong guesses: ridge at 50 labels near 188.9 (got 60.7); the random encoder close to raw ridge (it beat it at every count); the crossover at 250–1,000 (the means crossed at 100–250).
- **My decisions:** seed = replicate for the frozen rows; the mean of the *n* drawn labels as baseline, after checking the brief does not specify; the gap-vs-larger-SD rule, because the brief says "do not read a difference smaller than it"; adding 2,000 labels on dev; the fine-tuned network over scratch at a tie (cheap, keeps the encoder); one network with seed fixed in advance rather than a best-seed pick or ensemble; 1,000 training plus 200 check panels on top, staged.
- **My readings that were corrected:** "short of data" for the incumbent (the rubric's named trap; collinearity is not the problem); I confused the random and pre-trained encoders; expected 15 runs to shrink an SD; said pre-training's edge "begins" at 100 (it becomes *measurable*); placed the crossover "closer to 250"; credited the architecture for scratch overtaking frozen, though both share it; called scratch "better" at 2,000 (a tie); called the deployed model "fine-tuned + ridge".

## How I checked the numbers

- **Three checks in `run.py`:** no panel appears in two files; pre-trained encoders rebuild hidden dev gauges at 0.013–0.015 against 2.225 for the random one and 1.042 for guessing; a re-run gives bit-identical encoder weights and scores.
- **Every re-run after adding code** reproduced Exhibit 1 byte-for-byte (`cmp`/`git diff` on `exhibit1_runs.csv`).
- **`analysis/check_memo_numbers.py`** finds all 102 numbers in the memo in `analysis/outputs/`; I confirmed it flags three planted wrong numbers.
- **Test extract:** the pipeline and its dev score (3.01) were committed and pushed before test was read, with my expectation. Result 2.87, within the 0.24 retraining spread; nothing else was scored on test.
- **What I would not bet on:** pre-training's value at 50–100 labels, and the 80/20 split, which rests on one random network.
