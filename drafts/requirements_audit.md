# Requirements audit — session 4, 2026-11-03

Every requirement in `README.md`, `rubric.md`, `course_docs/04_submission_checklist.md`
and `data/DATA_DICTIONARY.md`, against where the submission meets it.
✔ = met; ⚠ = gap, with the proposed fix; ☐ = still to do.

## Exhibit 1 (rubric 1, 30 pts)

| Requirement | Where | |
|---|---|---|
| Five methods × four label counts, on dev | memo p.3; `outputs/exhibit1.md` | ✔ |
| Includes the Handout 9 §3.3 random-encoder control | Exhibit row 3 | ✔ |
| Every cell mean and SD | Exhibit | ✔ |
| Runs per cell as prescribed (5/15/5/5/5); 3 encoders pre-trained once outside the loop | Exhibit column + note; `run.py` | ✔ |

## Part 1 questions, "in the memo" (rubric 2, 28 pts)

| Question | Where in memo | |
|---|---|---|
| Q1 incumbent at 50 vs 1,000 | §1 ¶2 (60.7 → 47.5) | ✔ |
| Q1 vs predicting the mean | "How this was measured" (188.9); §1 ¶2 (3.98×, 75%) | ✔ |
| Q1 what kind of limit; how the table tells shortage from something else | §1 ¶2 (same panels: network 3.5 vs 47.5; 93% is form) | ✔ |
| Q1 connected to the process (rubric "how marks are lost") | §1 ¶3 (multiply, no compensation, threshold) | ✔ |
| Q2 what pre-training buys, at which counts, vs scratch at same n | §2 ¶3 | ✔ |
| Q3 what the control rules out; what the table would mean without it | §2 ¶2 (79–82%; "would have been credited with all of it") | ✔ |
| Q4 where ordering changes, where SDs don't let you say, bracketed not located | §2 ¶3 ("between 100 and 250"; "cannot be told apart below 250") | ✔ |
| Differences smaller than SD not read | "How this was measured"; throughout | ✔ |

## Part 2 memo (rubric 3, 24 pts)

| Requirement | Where | |
|---|---|---|
| Addressed to Head of Quality; ≤ 2 pages prose + Exhibit 1 | header; PDF 2 pp + p.3 exhibit at 10pt | ✔ |
| Recommendation in first paragraph | ¶1 | ✔ |
| Q1 answered with "the number that settles it" | §1 ¶1 (0.7 MPa² for 750 tests / $3.3M) | ✔ |
| Q2 method at current label count + its error vs incumbent's | §2 "What to deploy now" (3.1 / 1.7 MPa vs 46.9 / 6.8 MPa) | ✔ |
| Q3 a number, either side of it, money at $4,400 vs engineer's 2,000 | §3 (1,200 / $5.28M; 250 vs 1,000 vs 2,000; saves $3.52M) | ✔ |
| Numerate non-modeller reader | RMSE in MPa beside MSE; jargon explained | ✔ |
| Conditions checkable | stopping rules; spec-conditional budget | ✔ |
| Close with what the evidence does not establish | final section before the exhibit | ✔ |

## Evaluation discipline (rubric 4, 8 pts)

| Requirement | Where | |
|---|---|---|
| All comparison on dev | `run.py`; n = 2,000 also on dev | ✔ |
| Recommended pipeline scored once on test, beside dev, difference noted in one sentence | "Held-out check" | ✔ |
| Test not used to select | pipeline pre-registered in NOTES before test was read | ✔ |
| ⚠ Memo calls the two files "comparison extract" / "final extract", never dev / test | Proposed: add "(dev)" and "(test)" once each so a grader can tick criterion 4 at a glance | ⚠ |
| ⚠ Data dictionary: "report [the difference] rather than accounting for it" — memo adds "consistent with that extract's slightly lower spread of strength", which accounts for it | Proposed: drop that clause | ⚠ |

## Reproducibility, communication, process (rubric 5, 10 pts)

| Requirement | Where | |
|---|---|---|
| One command; README says what to run and how long | `analysis/README.md` (`python analysis/run.py`, ~65–70 s) | ✔ |
| No absolute paths; seeds set; only numpy/pandas | `run.py` | ✔ |
| Every memo number from the run | `check_memo_numbers.py`: 102/102 | ✔ |
| Process note ≤ 1 page, specific: delegated / rejected / checked | `ai_process_note.md` (1 page at 10pt) | ✔ |
| ⚠ Process note lacks the session-4 judgments: build vs operate phases, feedback-loop risk → champion/challenger + random audit (mine) | Proposed: fold into the stopping-rule bullet | ⚠ |
| ☐ Runs end to end from a clean copy | final step | ☐ |
| ☐ Sessions exported (session 4), README updated, export read for private content | final step | ☐ |
| ☐ Zip `tasdemir_orcun_a2.zip`: memo.pdf, analysis/ (with outputs), ai_process_note.md, sessions/; no data/, .venv, __pycache__ | final step; whether to include drafts/, expectations.md, part1_answers.md is my call | ☐ |

## Bonus (+4)

| ☐ One extension, with the implication for the recommendation stated | not started | ☐ |
