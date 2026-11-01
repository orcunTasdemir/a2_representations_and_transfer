# Exporting your AI session history

**IDS 575: Machine Learning and Statistical Methods for Business Analytics · Fall 2026**

Every assignment requires the complete exported history of every AI session you used. This sheet
explains how, for both approved agents.

> **Export at the end of each working session, not at the end of the assignment.** Both tools have
> some way of losing history — a retention window, a clipboard that chokes on a long conversation.
> If you wait until the night before the deadline, some of what you need may no longer exist.

> **Before you submit, open your export and read it.** Agent transcripts embed the full contents of
> files the agent read and the full output of commands it ran. Work in a clean folder that contains
> only course material.

---

## What goes in `sessions/`

```
sessions/
  README.md              which agent, how many sessions, anything the export omits
  codex/                 one file per session
  claude-code/           one file per session
```

You will normally have only one of those two subfolders. `sessions/README.md` is required either way
and can be three lines.

---

## 1. Codex

### The app

Open the session, use **Copy as Markdown** from the conversation menu, and paste into a file:

```
sessions/codex/a1-session-1.md
```

That is the whole procedure. Name the files in the order you worked; the names do not matter beyond
being distinguishable.

Two cautions:

- **It goes to the clipboard, not to a file.** Paste it somewhere immediately. A plain text editor is
  safer than Word, which has been reported to struggle with very long conversations.
- **Do it per session, while the session is open.** There is no bulk export.

### The CLI

Inside a session, `/copy` puts the conversation on the clipboard; paste it into a `.md` file the same
way.

### The transcript on disk — your backup

Codex also writes a full rollout file per session:

```
~/.codex/sessions/YYYY/MM/DD/rollout-<timestamp>-<session-uuid>.jsonl
```

Copy them if you want a belt-and-braces record:

```bash
mkdir -p sessions/codex
cp ~/.codex/sessions/2026/09/11/rollout-*.jsonl sessions/codex/
```

This is the complete log — more complete than the Markdown copy, which renders the conversation
rather than recording every tool call. **The Markdown is what I ask for. The JSONL is what saves you
if the Markdown copy failed and you did not notice.** Submitting both is fine and never penalised.

Two settings to check before you start:

- If `~/.codex/config.toml` contains `[history] persistence = "none"`, your history is being
  suppressed. Set it back to `"save-all"` (the default).
- Do not run assignment work with `--ephemeral`, which skips session persistence.

**Check the size before you attach.** Rollout files can get large, because they store repeated
context snapshots and raw tool output:

```bash
du -h sessions/codex/*
```

If the folder is over about 50 MB, zip it and say so in `sessions/README.md`.

---

## 2. Claude Code

### Option A — the raw transcript

Transcripts are stored as JSONL at:

```
~/.claude/projects/<encoded-project-path>/<session-id>.jsonl
```

`<encoded-project-path>` is your working directory with every non-alphanumeric character replaced by
`-`. Run `/status` inside a session to get the session ID; that ID is the filename. To see every
session you have, `claude --resume` opens an interactive picker.

### Option B — the readable export

From inside a session: `/export sessions/claude-code/a1-session-1.txt`

### Retention

Claude Code deletes transcripts after **30 days** by default. Copy the file into your assignment
folder at the end of each session rather than relying on the retention setting.

---

## `sessions/README.md` — templates

Ordinary case:

```markdown
# AI sessions for Assignment 1

Agent used: Codex app (4 sessions)

- codex/ : 4 Markdown exports, complete. Rollout JSONL for the same four sessions
           also included.
```

With a gap:

```markdown
# AI sessions for Assignment 1

Agent used: Claude Code (5 sessions)

- claude-code/ : 4 JSONL transcripts, complete. A fifth session on 18 September
                 was lost before I exported it; it was about half an hour, spent
                 debugging the grouped-fold split, and its result is in run_a2.py.
```

---

## If a command here does not match what you see

Both tools change quickly. If a path or a menu item on this sheet is not where it says it is,
**do not skip the export** — find the equivalent, do it, and say in `sessions/README.md` what you did
instead. Reporting that a documented step does not work is helpful and will not cost you marks.
