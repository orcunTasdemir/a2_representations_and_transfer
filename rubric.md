# Assignment 2 — grading rubric

100 points, scaled to 10% of the course grade. Up to 4 bonus points for the optional extension.

| # | Criterion | Pts |
|---|---|---:|
| 1 | **Exhibit 1.** All five methods at all four label counts on the dev extract, under the prescribed protocol, including **the control Handout 9 §3.3 requires**. Each cell a mean and a standard deviation over the runs the protocol prescribes for that row (three pre-trained encoders, five label draws). | **30** |
| 2 | **Reading the table.** The four Part 1 questions answered from your own numbers: what kind of limit the incumbent is hitting and how the table distinguishes a data shortage from something else; what pre-training buys and at which label counts; what the random-encoder row rules out; and the crossover stated as a bracket. | **28** |
| 3 | **Recommendation.** All three of the Head of Quality's questions answered, in order, for a reader who is numerate but is not a modeller. A named pipeline with its error and the error it replaces. A budget number, converted to money, with what happens on either side of it. Limitations stated. | **24** |
| 4 | **Evaluation discipline.** Comparison confined to the dev extract. The recommended pipeline scored once on the test extract, that number reported beside its dev counterpart, and the difference acknowledged. | **8** |
| 5 | **Reproducibility, communication and process.** Runs end to end from one command on a clean copy of the folder. Every number in the memo comes from that run. Within length. AI process note specific about what was delegated, what was rejected or corrected, and how the numbers were checked. | **10** |
| **Bonus** | **Optional extension.** One of the three, with the implication for the recommendation stated. Partial credit available; a wrong answer cannot lower your score. | **+4** |

Criteria 1 and 2 are 58 of the 100 points. This assignment is one table and what you can read off it.

---

## How marks are typically lost

None of these is a trick. All are recoverable by re-reading the brief before you submit.

- **The table without the control.** Criterion 1 asks for a specific extra row and the brief says which handout section requires it. A table that omits it cannot support the claim it is being used to make, and cannot score above half marks here.
- **One pre-training run.** A pre-trained encoder is a random object; two runs of the same procedure give different representations. The protocol says three, and says to average.
- **Reading a difference smaller than its standard deviation.** At the smallest label count several rows overlap. Reporting an ordering the experiment cannot resolve is worse than reporting that it cannot resolve it.
- **Announcing a crossover to the decimal.** Four label counts bracket a crossover. They do not locate one.
- **Diagnosing the incumbent as short of data.** Criterion 2 asks what kind of limit it is hitting. The table contains the evidence that settles it; use it rather than asserting.
- **Explaining the incumbent's failure without reference to the process.** The data dictionary records what Process Engineering says about how strength arises. A good answer connects the shape of the failure to that description.
- **Selecting on the test extract.** Choosing the method or the label count by looking at it is a criterion 4 deduction even when the number is right. So is scoring several pipelines on it and reporting the best.
- **Pre-training inside the label loop.** Not a criterion by itself, but it is where nearly all the reported pain on this assignment comes from.
- **A memo that reports the study and never answers the question.** The Head of Quality asked whether to spend $8.8 million. An exhibit and no number is a criterion 3 failure regardless of how good the exhibits are.
- **A generic AI process note.** "Used AI to help write code, verified output" earns nothing under criterion 5.
