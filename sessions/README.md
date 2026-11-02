# AI sessions for Assignment 2

Agent used: Claude Code (VS Code extension, macOS)

- `claude-code/` : raw `.jsonl` transcript per session, copied verbatim from
  `~/.claude/projects/<encoded-path>/`, plus a readable `.txt` rendered by
  `render_transcript.py` (`/export` is not available in the VS Code
  extension; see the A1 note in that script). The `.jsonl` is authoritative.

## Sessions

| File | Dates | Machine | Topic |
|---|---|---|---|
| `a2-session-0-failed` | 2026-10-21 | macOS | Failed start: my opening message, answered only by "OAuth session expired". No work done. Included for completeness. |
| `a2-session-1` | 2026-10-20 → 2026-11-02 | macOS | Setup; protocol and pre-training concepts; eight expectations written; `analysis/run.py` and Exhibit 1; all four Part 1 questions read and settled (`part1_answers.md`). |

## Known gaps

Each transcript is copied from disk near the end of its session, so it stops
a few messages short of the true end: the export itself and the commit that
follows it. Those are visible in the git history.
