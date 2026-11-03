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
  singular SD); larger of the two SDs = cautious reading. Confirmed
  (mine): Rule A with the larger SD. (S1)
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

- **Page economy (structure).** The brief says to answer the Part 1
  questions "in the memo", so Part 1 and Part 2 share the 2 prose pages.
  Part 1 Q1 and memo Q1 overlap heavily (and Part 1 Q2/Q3 with memo Q2):
  consider merging rather than saying things twice. My call at drafting. (S1)
- **Raw-ridge comparison goes in memo Q2, not Part 1 Q2** — decided (mine);
  Part 1 Q2 asks only for the comparison with scratch. (S1)

- **~80/20 split.** Of the raw → pre-trained gain, ~80% comes from the
  random nonlinear layer alone, ~20% from what pre-training learned, at
  every n (79/79/79/82%). Without the control, pre-training would have been
  credited ~5× too much. Strong single line for memo Q2. (S1)
- **Pre-training's edge over random is ~constant (5.7, 8.0, 7.8, 7.1)**;
  what changes with n is the SD. It becomes measurable at 100, it does not
  begin there. Same "smaller than its spread" logic as Q2. (S1)
- **ReLU = threshold.** max(0, ·) is literally the contamination shape;
  sums of hinges approximate products like flow × cure. So even random
  hinges give ridge the building blocks the process needs. Ties Q1 and Q3
  into one story: the incumbent fails on shape, so any nonlinear features
  fix most of it; pre-training adds the last ~20%. (S1)

- **Why scratch overtakes frozen (Q4):** not architecture (shared) but the
  target of the features — frozen's are fixed and aimed at rebuilding
  gauges (levels off 10.8 → 8.9, 250 → 1,000); scratch's are learned for
  strength (7.8 → 3.5). (S1)
- **Handout 9's regime thresholds shift down here:** scratch catches frozen
  by a few hundred labels, not tens of thousands, because the problem is
  simple (few underlying conditions; noise floor ≤ 3.5). Fine-tuned ≈
  scratch from 250 agrees. Feeds the budget question: pre-training's
  advantage is gone within the low hundreds. Budget number is mine. (S1)
- **Fine-tuned vs scratch: absence of evidence vs evidence of absence.**
  At 50/100, can't tell (huge SDs — a real fine-tuning advantage could hide
  there, where Handout 9 says it should be); from 250 on, genuinely equal
  (small SDs, tinier gaps). (S1)
- **[used → ai_process_note.md §2]** **Low priority — expectations vs result.** I expected the crossover at
  250–1,000; the means crossed at 100–250. Not required anywhere; at most a
  phrase in the process note §3. (S1)

- **Robust conclusion for memo Q1:** whether the incumbent's 0.6 gain at
  2,000 is real or noise, the decision is the same — $4.4M of tests for
  6.89 → 6.85 MPa typical miss vs ~1.7 MPa for a network. (S2)
- **Networks still gain from labels; the incumbent doesn't:** scratch
  3.5 → 3.0 (SD 0.1) from 1,000 → 2,000. Same panels, more labels help the
  model whose shape fits. (S2) — if used, add the scratch change to run.py.
- **Scratch vs fine-tuned at 2,000: dead tie** (gap 0.0, SD 0.2). Neither
  "wins"; matters for naming the deployed pipeline. (S2)

- **Memo Q2 — "can the traces be useful": yes, but not for this model at
  today's count** (scratch ties fine-tuned at 2,000, so no accuracy gain;
  the reason to skip them now is simplicity, not accuracy). Points I liked,
  all untested here so framed as suggestions (S2):
  - **Robustness:** 20,000 traces likely span more operating conditions
    than the 2,000 tested; an encoder that has seen them *might* hold up
    better under shifts. Dev is same autoclave/period, so untestable here.
  - **Flagging unlike-historical panels** via reconstruction error — fits
    Quality's goal of testing only the panels the model is unsure about.
    Needs the full pre-trained network (with its decoder) kept alongside
    whichever predictor is deployed; the fine-tuned model drops the decoder,
    so flagging does not favour fine-tuning over scratch.
  - **Reuse for other targets** (mine): a learned representation could feed
    models for other quality outcomes later.
  - **Next panel family:** traces accumulate from day one while labels are
    scarce — where pre-training is meant to pay (memo Q3).
  - Cost of using them is small (~5 s pre-training per encoder).

- **[decided (mine): 1 and 2 in memo, 3 in limitations, 4 if space]**
  **Agent's ranking of the usefulness-elsewhere points**: 1 next panel family (memo Q3); 2 flagging unusual panels
  (one sentence, as suggestion); 3 robustness (limitations — untestable
  here); 4 reuse for other targets (keep for oral check). (S2)
- **Freeze vs fine-tune by label count** (from `run.py`): frozen's means
  lower at 50/100 but within spread; fine-tuned clearly better from 250.
  Supports "freeze while labels are tens, fine-tune from a few hundred" for
  the next family, with the caveat that the low end is unresolved. (S2)

- **Production framing for the recommendation** (S2): one encoder + one
  fine-tuned network, seed fixed and recorded; retrain as tests accumulate;
  refresh the encoder as traces accumulate; version models; monitor with
  reconstruction-error flags. The study's 3 encoders × 5 seeds measured
  luck (± 0.2 at 2,000), they are not the deployment.

- **Test vs dev one-sentence note** (S2): test var(y) ~10% lower (data
  dictionary). That scales the predict-the-mean error exactly, but a good
  model's error is its residual, so it can move only if the removed spread
  was in panels the model gets wrong (e.g. fewer delaminated ones). Report
  the difference; do not explain it with a second look at test.

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
- **Only one random encoder tested** (`random_encoder()`, one seed): the
  control row's SD covers label draws only, not encoder-to-encoder
  variation. A different random layer could do somewhat better or worse;
  "the architecture alone buys ~80%" rests on one random draw. (S1)
- **n = 2,000 SDs cover inner seeds only** (one possible set of panels);
  they understate uncertainty relative to Exhibit 1's SDs. (S2)
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
