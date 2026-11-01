# Submission format and checklist

**IDS 575: Machine Learning and Statistical Methods for Business Analytics · Fall 2026**
Applies to all three assignments.

---

## What you submit

One archive named `lastname_firstname_aN.zip`, uploaded to Canvas by the deadline on the stated date.

Assignments 1 and 2 are due on class days, at **6:00 PM Central** — half an hour before class, so everything is in before we meet. Assignment 3 falls on a Sunday and is due at **11:59 PM Central**. Each brief states its own deadline on the first line.

```
lastname_firstname_a1/
  memo.pdf                  or memo.md
  analysis/
    run.sh                  or run.py — the one command
    README.md               what to run, what it produces, roughly how long
    <your code>
    outputs/                figures, tables, saved numbers
  ai_process_note.md
  sessions/
    README.md
    codex/  or  claude-code/
```

Do not include the `data/` folder — the graders have it. Do not include virtual environments, `__pycache__`, or model checkpoints.

---

## The four pieces

### `memo.pdf`

Addressed to the business reader named in the assignment. Length limits are per assignment (see each brief; A1 carries two memo sections, A3 allows 3 pages) plus the stated number of exhibits. Exhibits do not count against the prose limit.

Lead with the recommendation. Give the number and the number it replaces. State conditions in a form someone could check.

### `analysis/`

Must run end to end on a clean copy of the assignment folder with **one command**. State the command in `analysis/README.md`. If it takes more than about ten minutes, say so and say why.

Assume the grader has Python 3.10+, numpy, pandas, scikit-learn and matplotlib and nothing else. If you need something further, list it in `analysis/README.md`. Do not require a GPU.

Every number in your memo must come from this run.

### `ai_process_note.md`

One page maximum. Three things:

1. **What you delegated.** The substantive tasks, not "helped with code."
2. **What you changed or rejected, and why.** Specific instances. If you rejected nothing at all across an entire assignment, say so and say why you think that was.
3. **How you checked the final numbers.** What you recomputed, what you compared against, what you would still not bet on.

Generic notes score zero on this criterion. "Used Claude Code to write the analysis, reviewed the output, verified it was correct" is a generic note.

### `sessions/`

Complete exported history of every AI session used, per `03_exporting_your_session_history.md`, with a `README.md` naming the agent and disclosing anything the exports omit.

---

## Checklist

**Analysis**

- [ ] Runs from a clean copy of the folder with one command
- [ ] No absolute paths from your machine
- [ ] No dependency the grader will not have, or it is listed
- [ ] Random seeds set, so the numbers reproduce
- [ ] Every memo number appears in the run output or in `analysis/outputs/`

**Memo**

- [ ] Within the length limit
- [ ] Recommendation in the first paragraph
- [ ] Every required exhibit present and numbered as the brief numbers it
- [ ] Uncertainty stated once, plainly
- [ ] Any condition on the recommendation is checkable
- [ ] Addressed to the reader the brief names

**Process note**

- [ ] Names specific delegated tasks
- [ ] Names at least one specific thing you corrected or rejected, with the reason
- [ ] Says how the final numbers were verified, not just that they were

**Sessions**

- [ ] Every session exported
- [ ] Exports are unedited
- [ ] `sessions/README.md` names the agent and any gaps
- [ ] You have opened the export and confirmed it contains nothing private

**Yourself**

- [ ] You can explain any part of the submission out loud, without notes
- [ ] You could reconstruct the central argument on paper, with no tools
- [ ] There is no number in the memo you could not defend if asked where it came from

---

## Late work

Per the course outline: within 24 hours, −20%. 24 to 48 hours, −40%. Beyond 48 hours, no credit. Extensions for serious circumstances must be arranged in advance where possible.

A partial submission on time is worth substantially more than a complete one two days late. If you are running short, submit the memo and the analysis you have, and say in the process note what is missing.

---

## Ownership checks

The instructor may ask you to explain a piece of your submitted work, or to make a small modification to it, in class or in a brief oral check. These are short and are not adversarial. They exist so that assignment credit reflects your own judgment. Prepare for them by not submitting anything you do not understand.
