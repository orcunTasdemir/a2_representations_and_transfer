"""
Check that every number in memo.md comes from the run.

    python analysis/check_memo_numbers.py

Run after `python analysis/run.py`. Collects every number printed in
analysis/outputs/ and every number written in memo.md, and lists the memo
numbers that no output produces at the precision the memo states them
(so 74.9% in the output supports "75%" in the memo). Dollar amounts written
as "$5.28M" are compared in dollars. Numbers given by the brief itself (costs,
file sizes, the protocol) are allowed explicitly below.

Not part of run.py on purpose: a clean copy with no memo still runs end to end.
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MEMO = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE.parent / "memo.md"
OUT = HERE / "outputs"

# Given by the brief or the protocol, not produced by the analysis.
FROM_BRIEF = {"2026", "3", "160", "64", "30", "20,000", "2,000", "4,400", "1,000",
              "50", "100", "250", "500", "1,200", "200", "8.8M", "8.8", "1", "2", "40"}

NUM = re.compile(r"\$?\d[\d,]*(?:\.\d+)?M?")


def as_value(tok):
    """'$5.28M' -> (5280000.0, -4); '74.9' -> (74.9, 1); '1,000' -> (1000.0, 0)."""
    t = tok.lstrip("$").replace(",", "")
    if t.endswith("M"):
        x = float(t[:-1])
        decimals = len(t[:-1].split(".")[1]) if "." in t else 0
        return x * 1e6, decimals - 6
    decimals = len(t.split(".")[1]) if "." in t else 0
    return float(t), decimals


def output_values():
    vals = []
    for f in OUT.iterdir():
        if f.suffix in (".txt", ".md", ".csv"):
            for tok in NUM.findall(f.read_text()):
                try:
                    x, _ = as_value(tok)
                except ValueError:
                    continue
                vals.append(x)
                vals.append(x * 100)  # shares stored as fractions in the CSVs
    return vals


def main():
    text = MEMO.read_text()
    text = re.sub(r"\*\*Date:\*\*[^*]*", "", text)        # the date line
    text = re.sub(r"`[^`]*`", "", text)                    # file paths
    produced = output_values()
    missing, checked = [], 0
    for tok in sorted(set(NUM.findall(text))):
        bare = tok.lstrip("$")
        if bare in FROM_BRIEF:
            continue
        x, d = as_value(tok)
        checked += 1
        if not any(round(y, d) == round(x, d) for y in produced):
            missing.append(tok)
    print(f"memo numbers checked against analysis/outputs/: {checked}")
    if missing:
        print("NOT FOUND in outputs:", ", ".join(missing))
        sys.exit(1)
    print("all found")


if __name__ == "__main__":
    main()
