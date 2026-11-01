# CLAUDE.md

IDS 575 Fall 2026, Assignment 2 (Kestrel Composites, learned representations
and transfer). Due Thursday November 5, 6:00 PM Central.

## Read these first

`README.md` and `rubric.md` in this folder are the authoritative brief and
grading criteria. `assignment2.pdf` contains the same brief. `data/DATA_DICTIONARY.md`
is short and meant to be read. Read them rather than relying on anything
restated here. Where this file and the brief disagree, the brief wins.

`course_docs/` holds the course-wide policy, approach, export and
submission documents. They apply to this assignment. `handouts/` holds the
lecture handouts; Handout 9 (`lecture09_transfer_learning.pdf`) is the one
the brief cites by section, Handout 6 the background.

Read `NOTES.md` at the start of every session.

## Hard rules

- **Never read a data file into the conversation.** No `cat`, `head`,
  `print(df)`, or pasted CSV contents. Write code that reads the file and
  reports numbers back.
- **Never modify a supplied data file or the starter code.** The protocol is
  fixed in `starter/kestrel.py`; import it, do not edit it. The negative
  strengths are deliberate and stay in.
- **Never select on the test extract.** Every comparison is on
  `labeled_dev.csv`. `labeled_test.csv` is scored once, on the one pipeline I
  recommend, after the recommendation is fixed.
- **Never state a number you have not produced by running code.**
- **Never make the course judgments for me.** Evaluation design, how to read
  the table, what kind of limit the incumbent hits, the crossover bracket,
  the recommended pipeline and the budget number are mine. Lay out the
  options and what each implies, then wait.
- **Stop if I cannot explain what you produced.** I may be asked to explain
  or modify any line of this submission.

## Drafting

Course policy permits AI help drafting the memo "provided the judgments in
it are yours and you can defend them." So: draft any deliverable on request,
prose and exhibits included. For the recommendation and any verdict, I state
the judgment first in my own words; you then put it into prose. Nothing goes
in a draft that I cannot defend in an oral check.

## Requirements the submission must meet

- `analysis/` runs end to end from one command on a clean copy. No absolute
  paths. Seeds set.
- Grader has Python 3.10+, numpy, pandas, scikit-learn, matplotlib and
  nothing else. Anything further goes in `analysis/README.md`. No GPU.
- Outputs go to `analysis/outputs/`.
- Use `starter/kestrel.py` (`load`, `label_subset`, `ridge`, `pretrain`,
  `random_encoder`, `frozen_ridge`, `supervised`) rather than reimplementing.
- Pre-train the three encoders once, outside the label loop.
- Memo: at most 2 pages of prose plus Exhibit 1. Process note: at most 1 page.

## Working habits

- Baseline before model (here: predict the mean strength).
- Write down expectations before computing.
- When I reach a conclusion, argue against it: what would have to be true
  for it to be wrong, and what the strongest objection is.
- Say so when a result looks too good, or when a gap is smaller than its SD.
- One work block per session, one topic.

## End of every session

1. Export the transcript to `sessions/claude-code/` (raw JSONL copy plus
   `sessions/render_transcript.py` for the readable `.txt`; `/export` does
   not work in the VS Code extension).
2. Remind me what to record in `ai_process_note.md`: what was delegated,
   what I changed or rejected and why, how numbers were checked.
3. Append to `NOTES.md`: what was done, the current open question, any
   decision I made, and any number produced with where it came from.

Transcripts embed full file contents and command output. Keep this folder
free of anything private.
