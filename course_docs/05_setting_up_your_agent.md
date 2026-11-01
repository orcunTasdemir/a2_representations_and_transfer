# Setting up your coding agent

**IDS 575: Machine Learning and Statistical Methods for Business Analytics · Fall 2026**
Do this in the first week, before Assignment 1. It takes about twenty minutes.

---

## The short version

**This course uses one of two coding agents: the Codex app or Claude Code.**
**No other coding agent may be used on course work.**
**Codex has a free path, so nobody needs to spend money to complete an assignment.**

---

## 1. Choosing between the two

Either is fine, and you do not need both. Pick one and stay with it for an assignment; switching
mid-assignment just makes your `sessions/` folder harder to assemble.

| | **Codex** | **Claude Code** |
|---|---|---|
| Cost | **Free path.** The Free plan plus the $100 student credit grant, below. | Requires a Claude plan that includes it, or pay-as-you-go API credits. |
| Form | Desktop app, CLI, or IDE extension | CLI |
| Transcript export | *Copy as Markdown* from the conversation menu, one click | `/export`, plus a complete JSONL transcript on disk |

**If cost matters at all, use Codex.** The free plan and the student grant cover this course
comfortably, and nothing in any assignment needs more than that.

## 2. What you need

1. **For Codex:** a ChatGPT account — the **Free plan is sufficient** — and the Codex app or CLI.
2. **For Claude Code:** a Claude account on a plan that includes Claude Code, and the CLI installed.
3. Either way: Python 3.10+ with numpy, pandas, scikit-learn and matplotlib.

## 3. Claim the student credits (Codex)

OpenAI grants **$100 in Codex credits to verified students** at degree-granting universities in the
US and Canada. UIC qualifies.

1. Sign in to ChatGPT, then start verification from the Codex for Students page
   (`developers.openai.com/community/students`).
2. Verify with your **@uic.edu** address. Verification is handled by SheerID and is usually instant.
3. The credits are applied automatically to that account.

Three things to know:

- **They expire twelve months after the grant date.** That is well past the end of this course.
- **They are ChatGPT credits usable in Codex**, not API credits. You do not need an API key, and you
  should not create one for this course.
- **One grant per student**, and it is tied to the account you verified with. Verify on the account
  you will actually use.

**If verification fails** — you are outside the US or Canada at the moment you claim, your school
type is not recognised, or anything else — **email me.** Do not buy a subscription to work around it.

## 4. Verify the workflow

Do the setup exercise in `setup_exercise/` before Assignment 1. It is ungraded, takes about fifteen
minutes, and checks three things:

- Python runs and has the packages the course needs;
- your agent runs and can read a file in the folder you are working in;
- you can export a session transcript and find it afterwards.

If any of the three does not work, that is what the exercise is for. Bring it to me in week two, not
the night before Assignment 1 is due.

## 5. Staying inside the budget

Free-plan usage plus the grant covers the three assignments comfortably, but that assumes you are
not wasting it. Four habits, in order of how much they matter:

**Never let the agent read a data file into the conversation.** `member_months.csv` is 33,000 rows.
Pasting it, or letting the agent `cat` it, can burn more of your allowance in one message than a
whole working session should. Have the agent *write code that reads the file* and report back the
numbers. The data dictionaries are short and are meant to be read; the CSVs are not.

**Match the model to the task.** Use a cheaper model for routine work — writing a loop, fixing an
import, reformatting a table. Save the strongest model for the things that need it: debugging
something you do not understand, or arguing with you about an evaluation design. The difference in
cost between the top and bottom models is more than twentyfold, and most of what you will ask for
does not need the top one.

**Start a new session for each work block, and keep it on one topic.** A single session that runs
all week re-sends its whole history with every message. Three focused sessions cost far less than
one sprawling one, and they are easier to export and easier for me to read.

**Don't re-run the expensive things.** Cache what you compute. `analyst_model.py` produces the same
numbers every time; run it once and save the output rather than asking the agent to re-run it in
every session.

**Check your balance after Assignment 1.** If you are more than a third of the way through the
grant, tell me — either you are working in a way that is costing you unnecessarily and I can help,
or my estimate was wrong and I need to know.

**If you run out, email me.** 

## 6. Why only these two

Not because nothing else works. Because when everyone uses one of two tools, the setup instructions
apply to everyone, the transcript format is one I can read quickly, a question in class about "why
did it do that" has an answer that helps the whole room, and the audit trail every submission
depends on is one I can actually verify. Both approved tools produce a complete, exportable session
history; that is the property the course requires and it is not universal.
