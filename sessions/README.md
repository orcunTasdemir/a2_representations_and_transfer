# AI sessions for Assignment 2

Agent used: Claude Code (VS Code extension, macOS)

- `claude-code/` : raw `.jsonl` transcript per session, copied verbatim from
  `~/.claude/projects/<encoded-path>/`, plus a readable `.txt` rendered by
  `render_transcript.py` (`/export` is not available in the VS Code
  extension). The `.jsonl` is authoritative.

## Sessions

A session here is a working block that I ended with an explicit "close the
session" (export, notes, commit). Times are US Central.

| File | Dates | Topic |
|---|---|---|
| `a2-session-0-failed` | Oct 20 | Failed start: my opening message, answered only by "OAuth session expired". No work done. Its own conversation (`f6aacc42…`). |
| `a2-session-1` | Oct 20 → Nov 1 (ends 10:09 PM) | Setup; protocol and pre-training concepts; eight expectations written; `analysis/run.py` and Exhibit 1; Part 1 Q1. |
| `a2-session-2` | Nov 1 → Nov 2 (ends 12:21 AM) | Part 1 Q2–Q4 read and settled (`part1_answers.md`); Part 1 numbers moved into `run.py`. |
| `a2-session-3` | Nov 2 → Nov 3 | Memo decisions (n = 2,000 run, deployment choice, test pipeline fixed then scored once, staged budget); memo and process note written; sessions relabelled. |

Sessions 1–3 are one VS Code conversation (`0c849d9a…`) worked in three
times, so each file is the whole conversation as it stood at that session's
close: `a2-session-2.jsonl` contains `a2-session-1.jsonl` as its opening
part, and `a2-session-3.jsonl` contains `a2-session-2.jsonl`. Verified in
Python as byte-exact prefixes (516 ⊂ 806 ⊂ 1,554+ records). All three are
submitted unedited rather than only the last, because each is what existed
at the end of its session.

The `a2-session-1` snapshot was overwritten once during the work (re-exported
at the session-2 close under the old label) and restored byte-for-byte from
the repository history (commit `16ff5ec`) when the sessions were relabelled.

## Known gaps

Each transcript is copied from disk near the end of its session, so it stops
a few messages short of the true end: the export itself and the commit that
follows it. Those are visible in the git history.
