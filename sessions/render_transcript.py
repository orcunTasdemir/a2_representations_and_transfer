"""Render a Claude Code JSONL transcript as readable text.

The VS Code extension has no /export command (checked 2026-09-17; the CLI has
no export subcommand either), so this reproduces Option B of
course_docs/03_exporting_your_session_history.md from the Option A raw file.

Usage:
    python sessions/render_transcript.py <session>.jsonl <output>.txt

Nothing is truncated: tool calls and their full output are included, matching
what /export would have written.
"""
import json
import sys
from pathlib import Path

RULE = "=" * 78


def describe_image(block):
    """An embedded image, as a labelled placeholder.

    The base64 payload of a screenshot or a rendered PDF page can be a
    megabyte on one line, which makes the readable rendering unreadable --
    in this project's transcripts it was 93% of the file.  Nothing is
    concealed: the media type and the payload size are stated, and the
    authoritative .jsonl beside this file still holds every byte.
    """
    src = block.get("source") or {}
    data = src.get("data", "")
    return "[image omitted from the readable rendering: %s, %s base64 chars; " \
           "the full payload is in the .jsonl]" % (
               src.get("media_type", "unknown type"), f"{len(data):,}")


def render_block(block):
    """One content block -> list of text lines."""
    kind = block.get("type")
    if kind == "text":
        return [block.get("text", "")]
    if kind == "thinking":
        return ["[thinking]", block.get("thinking", "")]
    if kind == "tool_use":
        args = json.dumps(block.get("input", {}), indent=2, ensure_ascii=False)
        return ["[tool_use: %s]" % block.get("name", "?"), args]
    if kind == "image":
        return [describe_image(block)]
    if kind == "tool_result":
        content = block.get("content", "")
        if isinstance(content, list):
            parts = []
            for item in content:
                if isinstance(item, dict) and item.get("type") == "text":
                    parts.append(item.get("text", ""))
                elif isinstance(item, dict) and item.get("type") == "image":
                    parts.append(describe_image(item))
                else:
                    parts.append(json.dumps(item, ensure_ascii=False))
            content = "\n".join(parts)
        return ["[tool_result]", str(content)]
    return ["[%s]" % kind, json.dumps(block, ensure_ascii=False)]


def render_message(record):
    """One JSONL record -> list of text lines, or [] to skip."""
    role = record.get("type")
    if role not in ("user", "assistant", "system"):
        return []
    message = record.get("message") or {}
    content = message.get("content", record.get("content", ""))
    lines = []
    if isinstance(content, str):
        lines.append(content)
    elif isinstance(content, list):
        for block in content:
            if isinstance(block, dict):
                lines.extend(render_block(block))
            else:
                lines.append(str(block))
    if not any(line.strip() for line in lines):
        return []
    header = "%s  [%s]" % (role.upper(), record.get("timestamp", "no timestamp"))
    return [RULE, header, RULE, ""] + lines + [""]


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    src, dest = Path(sys.argv[1]), Path(sys.argv[2])
    out, kept, skipped = [], 0, 0
    with src.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                skipped += 1
                continue
            rendered = render_message(record)
            if rendered:
                out.extend(rendered)
                kept += 1
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text("\n".join(out), encoding="utf-8")
    print("%s -> %s" % (src.name, dest))
    print("messages rendered: %d, unparseable lines: %d" % (kept, skipped))


if __name__ == "__main__":
    main()
