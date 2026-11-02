# Ideas log — points not yet in a deliverable

Anything said, noticed or decided that could strengthen `memo.md`,
`ai_process_note.md` or the analysis, written down the moment it comes up so
it survives context compression, new sessions and machine switches.
When a point is used, mark it **[used → file]**; when dropped, **[dropped:
reason]**. Never delete a line. Where a point needs a judgment from me, it
says so.

Source tags: S1 = session 1 (2026-10-20 → 11-01).

---

## For the memo — Part 1 reading

- **Two crossovers, not one.** Handout 9's "scratch at tens of thousands" is
  scratch vs *pre-trained* methods; scratch vs *raw ridge* is a different
  crossover. Don't conflate them in Q4. (S1)
- **Fine-tuning at large n:** its advantage over scratch usually shrinks to
  zero rather than turning negative; "train from scratch" at large n means
  pre-training is no longer *needed*, not that it hurts. Our table cannot
  see that end (stops at 1,000). (S1)
- **Q3 decomposition:** row 1 → row 3 = what the architecture alone buys
  (random nonlinear features); row 3 → row 2 = what pre-training learned.
  Without row 3, the whole row 1 → row 2 gap would be credited to
  pre-training. (S1)
- **Q3 curiosity:** the random encoder reconstructs gauges *worse* than
  predicting 0 (2.225 vs 1.042), yet ridge on its features beats raw ridge
  at every n. Reconstruction quality and usefulness for strength are not the
  same thing. Possibly worth one sentence. (S1, check 1 output)
- **Redundancy confirmed:** pre-trained encoders rebuild hidden gauges ~70×
  better than predicting 0 (0.013–0.015 vs 1.042), consistent with the data
  dictionary's "160 views of a few conditions". Supports why pre-training
  can work here. (S1)
- **Bracketing rule:** where two rows are within one SD at some n, that n
  cannot narrow the bracket. My pre-result expectation: 250–1,000, nearer
  the top. (S1)
- **[dropped: my decision — post-hoc choice of a sharper test is motivated
  analysis; brief fixes mean ± SD]** **Paired comparison.** All methods share the same 5
  draws, so per-draw differences (method A − method B on the same panels)
  could resolve gaps that overlapping SDs cannot. The brief asks for mean ±
  SD and "do not read a difference smaller than it", so at most a footnote.
  Not discussed with me yet. (S1, agent)

- **Brief endorses Rule A** ("do not read a difference smaller than it",
  singular SD); larger of the two SDs = cautious reading. Awaiting my
  confirmation. (S1)
- **Overlap rule — my decision.** Rule A (gap > larger SD, the brief's
  wording) vs Rule B (gap > SD sum). Frozen vs scratch at 250 passes A by
  0.2 and fails B. (S1)
- **Frozen is never clearly ahead of scratch** (fails both rules at 50 and
  100), so the Q4 bracket is one-sided in what it resolves: scratch clearly
  ahead by 1,000, marginally by 250; means cross between 100 and 250. (S1)
- **Fine-tuned ≈ scratch at n ≥ 250 is a genuine tie** (SDs 0.5 / 0.3, gaps
  smaller still): the starting point stops mattering once there are a few
  hundred labels. At 50 / 100 the SDs are too large to tell. (S1)
- **Pre-training vs scratch: nothing resolved; vs raw ridge: large and
  resolved at every n** (33.5 vs 60.7 at 50; 8.9 vs 47.5 at 1,000). Which
  comparison answers "can the traces be made useful" — my call; Q3's
  control then says how much is due to pre-training. (S1)

## For the memo — Part 2 and framing

- **Lead number for Q1 ("the number that settles it") — my decision.**
  Candidates: the 0.7 MPa² bought by quadrupling labels 250 → 1,000; or
  ridge 47.5 vs scratch 3.5 on the same panels. (S1)
- **"A weighted sum assumes compensation the physics rules out"** — the
  one-sentence link between the incumbent's failure and Process
  Engineering. **[used → memo.md draft, Q1]** (S1)
- **The floor is specific to a model linear in these 160 columns**; a
  linear model on engineered features (flow × cure) need not have it.
  Links to bonus option 3. **[used → memo.md draft, Q1]** (S1)
- **Reader-friendly units — my decision.** For a non-modeller: RMSE in MPa
  (typical miss), and/or share of variation explained, 1 − MSE/188.9
  (ridge: 68% at n=50 → 75% at n=1,000). (S1)
- **Kestrel holds 2,000 labels; the table stops at 1,000.** Matters for
  "what to deploy at Kestrel's current label count". **[used → memo.md
  draft, Q2 note + limitations]** (S1)
- **Mean baseline barely moves with n** (190.2 → 188.9): extra error of
  estimating the mean from n labels is roughly var/n. Supports that ridge's
  gain is real learning. (S1)
- **Engineer's plan in numbers:** 2,000 more tests × $4,400 = $8.8M, set
  against what 250 → 1,000 bought ridge (0.7 MPa²). (S1)

## For the limitations section

- Nothing measured between 1,000 and 2,000 labels, or beyond. **[used →
  memo.md draft]** (S1)
- Noise floor is bounded (≤ 3.5), not measured. **[used → memo.md
  draft]** (S1)
- **Reconstruction error as a drift check** for a new panel family: if new
  panels rebuild badly, they are unlike the historical traces and the
  encoder may not transfer. **[used → memo.md draft]** (S1)
- **Protocol asymmetry at small n:** ridge refits on all n after choosing
  its penalty on a 75/25 split; the networks train on 75% only (37 of 50)
  and never refit. Part of the networks' n = 50 handicap is the protocol,
  not the method. (S1)
- At n = 50, every inner decision (ridge penalty, stopping epoch) rests on
  13 panels — one reason the n = 50 SDs are large. (S1)
- Test var(y) is ~10% lower than dev; expect and report a small difference,
  don't explain it away (data dictionary). (S1)

## For the process note

- See `ai_process_note.md` §2 for the running list of accepted / changed /
  rejected items. New ones go there directly.
- **Write-everything-down rule** (this file) — a process practice adopted
  mid-assignment after noticing the risk of losing points to context
  compression. (S1)
