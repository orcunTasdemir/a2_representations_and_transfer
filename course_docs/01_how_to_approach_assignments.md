# How to approach the assignments

**IDS 575: Machine Learning and Statistical Methods for Business Analytics · Fall 2026**
Read this once before Assignment 1, and re-read §5 before each submission.

---

## 1. What is being graded

You have a coding agent (`05_setting_up_your_agent.md`). It can write a modeling pipeline faster
than you can describe one, so writing the pipeline is not the skill being assessed.

What is assessed is the part that stays yours:

- deciding what question is actually being asked
- noticing when an answer is too good
- knowing what evidence would settle a disagreement
- saying what the evidence does and does not support

The broad goal of these assignments is to help you become comfortable working with AI to define and implement machine learning pipelines in a business context. To do that, you need a certain level of competency in the core concepts of machine learning. And imparting that competency is the broad goal of the course. 

Each assignment is preparation for an in-person exam where you will have none of these tools. If you
finish an assignment and could not explain your headline number on paper, it has not done its job.

---

## 2. What every assignment looks like

A business situation, a dataset, and **an analysis someone else has already done** — an analyst, a
contractor, an engineer. That analysis is plausible, arithmetically correct, but also wrong. Your task is
not "build a model." It is "understand what is wrong, why it is wrong, establish what is true, and say what should be done."

Four things are submitted every time:

| | |
|---|---|
| `memo.pdf` or `memo.md` | To a named business reader. Length limit stated per assignment, and enforced. |
| `analysis/` | Your code. Runs end to end from one command. |
| `ai_process_note.md` | One page. What you delegated, what you rejected, how you checked. |
| `sessions/` | Complete exported history of every AI session used. |

---

## 3. A working order that tends to go well

**Read the brief and the data dictionary yourself first.** The dictionaries record how each column
is produced and *when*. That timing information decides which columns you may use, and it is easier
to take in before a model exists to distract you.

**Write down what you expect before you compute anything.** What is the base rate? What order of
magnitude should the effect be? What would a suspiciously good result look like? Two minutes of this
is what makes you able to be surprised, and being surprised is how you find things.

**Get a baseline before you get a model.** Every assignment has a do-nothing answer — predict the
majority class, predict the mean, keep the current price. Compute it. It is the denominator for
everything that follows and the number most often missing from an agent's output.

**Change one thing at a time.** Where an assignment asks for an audit trail — one row per problem,
one fix, and the resulting number — build it as you go rather than reconstructing it at the end. It
is also your best defence against an agent that quietly fixed three things at once.

---

## 4. Working with your agent

The assignments are graded lightly, and in principle, you can delegate the majority of work to AI. However, this goes against the course's learning goals and will make you struggle in the in-person assessments. Hence, the following strategy is recommended for optimal learning.

**Delegate the work, not the judgment.** Good to hand over: "write a grouped cross-validation split
by member_id", "sweep the ridge penalty over the grid and plot train and validation error". Not good
to hand over: "tell me whether this model is good enough to deploy", "write the recommendation."
The second list is the assignment.

**Give it the business context, not just the file.** An agent told "predict churn from this CSV" will
optimise accuracy. An agent told what an offer costs and what a retained member is worth will do
something quite different. The context is in the brief; pass it along.

**Ask it to argue against itself.** "What would have to be true for this estimate to be wrong?" and
"What is the strongest objection to this conclusion?" are the two highest-yield prompts in the course.

**Be suspicious of agreement.** If the first answer confirms what you expected and nothing errored,
slow down rather than speed up.

**Do not let it choose the evaluation design.** Splits, metrics, units of analysis, and what counts as
held out are the graded content of this course. An agent will pick a sensible default, and these
datasets are built to punish sensible defaults.

**If you do not understand what it produced, stop.** Get it explained or throw it out. You are
responsible for every line and may be asked in class to explain any of it.

**Export your session before you close it** (`03_exporting_your_session_history.md`). The Codex app
copies to the clipboard rather than to a file, so paste it somewhere immediately.

---

## 5. The memo

Written to a named person who has a decision to make and will read the first paragraph carefully and
the rest quickly.

- **Lead with the recommendation.** Not the method, not the data cleaning.
- **Give the number, then the number it replaces.** "The honest estimate is X, not the Y in the
  current proposal, and the gap is mostly Z."
- **Quantify the uncertainty once, plainly, and move on.** A memo that never commits is not useful.
- **State conditions so someone could check them.** "Deploy if corporate accounts stay under 15% of
  the book" is a recommendation. "Deploy with caution" is not.
- **Respect the length limit.** Exhibits do not count against prose length; prose does.

---

## 6. Before you submit

Full list in `04_submission_checklist.md`. The five that matter most:

- [ ] The analysis runs end to end, from a clean copy of the folder, with one command.
- [ ] Every number in the memo comes from that run.
- [ ] Every session is exported into `sessions/`, complete and unedited.
- [ ] The process note names specific things you rejected or corrected. If you rejected nothing all
      assignment, think about that before writing it down.
- [ ] You can explain any part of the submission out loud, without notes.

That last item is not decorative. You may be asked to explain or modify a piece of your submitted
work in a short oral check. 
