"""
Assignment 2, Part 1 -- Exhibit 1 and the checks behind it.

    python analysis/run.py

Pre-trains the three encoders once, then fits every method at every label
count and label draw, scoring each run on labeled_dev.csv. labeled_test.csv is
not touched here.

Writes to analysis/outputs/:
    exhibit1_runs.csv      one row per run (n, draw, method, encoder, dev MSE)
    exhibit1.csv           one row per cell: mean, SD, number of runs
    exhibit1.md            the same table, formatted
    checks.txt             the three sanity checks
"""
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "starter"))

from kestrel import (DATA, FILES, ID, LABEL_COUNTS, MASK_FRACTION,  # noqa: E402
                     N_ENCODER_SEEDS, N_REPLICATES, frozen_ridge, label_subset,
                     load, pretrain, random_encoder, ridge, supervised)

OUT = Path(__file__).resolve().parent / "outputs"
OUT.mkdir(exist_ok=True)

# Display order of Exhibit 1. The mean baseline is a reference line, not a method.
METHODS = ["ridge_raw", "frozen_pretrained", "frozen_random", "scratch", "finetuned"]
LABELS = {
    "ridge_raw": "Ridge on the 160 raw gauges (incumbent)",
    "frozen_pretrained": "Frozen pre-trained encoder + ridge",
    "frozen_random": "Frozen random encoder + ridge (control)",
    "scratch": "Network from scratch",
    "finetuned": "Fine-tuned encoder",
    "mean_baseline": "Reference: predict the mean of the n labels, no gauges",
}

log_lines = []


def log(msg=""):
    print(msg, flush=True)
    log_lines.append(msg)


# ---- check 2: no panel in two files ----------------------------------------
def check_no_overlap():
    ids = {k: set(pd.read_csv(DATA / f, usecols=[ID])[ID]) for k, f in FILES.items()}
    names = list(ids)
    worst = 0
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            k = len(ids[a] & ids[b])
            worst = max(worst, k)
            log(f"  {a:>6} & {b:<6} shared panel_ids: {k}")
    log(f"  sizes: " + ", ".join(f"{k} {len(v)}" for k, v in ids.items()))
    return worst == 0


# ---- check 1: did pre-training learn anything? -----------------------------
def masked_reconstruction_mse(enc, X, seed=12345):
    """Hide MASK_FRACTION of the gauges, rebuild them, score the hidden ones only.

    Gauges only -- no strength values are used. The same mask for every encoder.
    """
    mask = np.random.default_rng(seed).random(X.shape) < MASK_FRACTION
    corrupted = X.copy()
    corrupted[mask] = 0.0
    return float(np.mean((enc.predict(corrupted)[mask] - X[mask]) ** 2)), mask


def run_cell(n, r, Xtr, ytr, Xdev, ydev, encoders, rand_enc):
    """Every method on the same n panels of draw r. Returns a list of run records."""
    idx = label_subset(n, r)
    X, y = Xtr[idx], ytr[idx]
    rows = []

    def add(method, mse, encoder=""):
        rows.append({"n": n, "draw": r, "method": method,
                     "encoder": encoder, "dev_mse": mse})

    add("mean_baseline", float(np.mean((y.mean() - ydev) ** 2)))
    add("ridge_raw", ridge(X, y, Xdev, ydev, seed=r))
    for e, enc in enumerate(encoders):
        add("frozen_pretrained", frozen_ridge(enc, X, y, Xdev, ydev, seed=r), e)
    add("frozen_random", frozen_ridge(rand_enc, X, y, Xdev, ydev, seed=r))
    add("scratch", supervised(X, y, Xdev, ydev, seed=r))
    e = r % N_ENCODER_SEEDS
    add("finetuned", supervised(X, y, Xdev, ydev, seed=r, encoder=encoders[e]), e)
    return rows


# Pairs read in Part 1, as (a, b): the gap is mean(a) - mean(b).
PAIRS = [("frozen_pretrained", "scratch"),       # Q2, Q4
         ("finetuned", "scratch"),               # Q2
         ("frozen_random", "ridge_raw"),         # Q3: the architecture alone
         ("frozen_pretrained", "frozen_random"),  # Q3: what pre-training learned
         ("ridge_raw", "scratch")]               # Q1: same panels, flexible model


def part1_numbers(cells):
    """The derived numbers the Part 1 reading uses, so each comes from this run.

    Rule A (the brief's wording): a gap is read only if it exceeds the larger
    of the two cells' SDs.
    """
    m = cells.set_index(["method", "n"])
    rows = []
    for a, b in PAIRS:
        for n in LABEL_COUNTS:
            A, B = m.loc[(a, n)], m.loc[(b, n)]
            gap = A["mean"] - B["mean"]
            larger = max(A["sd"], B["sd"])
            rows.append({"a": a, "b": b, "n": n, "mean_a": A["mean"], "sd_a": A["sd"],
                         "mean_b": B["mean"], "sd_b": B["sd"], "gap": gap,
                         "larger_sd": larger, "rule_a": abs(gap) > larger})
    comp = pd.DataFrame(rows)
    comp.to_csv(OUT / "part1_comparisons.csv", index=False)
    log("\nPart 1 comparisons -- gap = mean(a) - mean(b); Rule A: |gap| > larger SD")
    for (a, b), g in comp.groupby(["a", "b"], sort=False):
        log(f"  {a} - {b}")
        for _, r in g.iterrows():
            log(f"    n={r.n:<5} gap {r.gap:6.1f}  larger SD {r.larger_sd:5.1f}"
                f"  Rule A {'yes' if r.rule_a else 'no'}")

    # Q3: split the raw -> pre-trained gain into its two steps.
    split = []
    for n in LABEL_COUNTS:
        raw, rnd, pre = (m.loc[(k, n), "mean"]
                         for k in ("ridge_raw", "frozen_random", "frozen_pretrained"))
        split.append({"n": n, "total": raw - pre, "architecture": raw - rnd,
                      "pretraining": rnd - pre,
                      "architecture_share": (raw - rnd) / (raw - pre)})
    split = pd.DataFrame(split)
    split.to_csv(OUT / "part1_split.csv", index=False)
    log("\nQ3 -- raw ridge -> pre-trained gain: architecture alone vs pre-training")
    for _, r in split.iterrows():
        log(f"  n={int(r.n):<5} total {r.total:5.1f}  architecture {r.architecture:5.1f}"
            f" ({r.architecture_share:.0%})  pre-training {r.pretraining:4.1f}")

    # Q1: the incumbent against the mean and against a flexible model.
    log("\nQ1 -- the incumbent")
    for n in LABEL_COUNTS:
        base, rid = m.loc[("mean_baseline", n), "mean"], m.loc[("ridge_raw", n), "mean"]
        log(f"  n={n:<5} mean-baseline / ridge {base / rid:.2f}x"
            f"  ridge explains {1 - rid / base:.1%} of the variation")
    r250, r1000 = m.loc[("ridge_raw", 250), "mean"], m.loc[("ridge_raw", 1000), "mean"]
    s1000 = m.loc[("scratch", 1000), "mean"]
    log(f"  ridge 250 -> 1000 improvement: {r250 - r1000:.1f}")
    log(f"  ridge - scratch at 1000: {r1000 - s1000:.1f} = {(r1000 - s1000) / r1000:.0%}"
        f" of ridge's error")


def main():
    t0 = time.time()
    Xtr, ytr = load("train")
    Xdev, ydev = load("dev")
    traces = load("traces")
    log(f"train {Xtr.shape}  dev {Xdev.shape}  traces {traces.shape}")

    log("\nCheck 2 -- no panel appears in two files")
    ok_overlap = check_no_overlap()
    log(f"  -> {'PASS' if ok_overlap else 'FAIL'}")

    # ---- pre-train once per seed, outside the label loop -------------------
    log(f"\nPre-training {N_ENCODER_SEEDS} encoders on {len(traces)} unlabelled traces")
    encoders = []
    for s in range(N_ENCODER_SEEDS):
        t = time.time()
        encoders.append(pretrain(traces, seed=s))
        log(f"  encoder {s}: {time.time() - t:.1f} s")
    rand_enc = random_encoder()

    log("\nCheck 1 -- masked reconstruction on dev gauges (hidden gauges only;"
        " standardised units, so predicting 0 = the training mean)")
    for s, enc in enumerate(encoders):
        log(f"  pre-trained encoder {s}: {masked_reconstruction_mse(enc, Xdev)[0]:.3f}")
    rand_mse, mask = masked_reconstruction_mse(rand_enc, Xdev)
    log(f"  random encoder:        {rand_mse:.3f}")
    log(f"  predict 0 (no model):  {float(np.mean(Xdev[mask] ** 2)):.3f}")

    # ---- Exhibit 1: the two nested loops ----------------------------------
    log("\nExhibit 1 -- fitting")
    runs = []
    for n in LABEL_COUNTS:
        t = time.time()
        for r in range(N_REPLICATES):
            runs += run_cell(n, r, Xtr, ytr, Xdev, ydev, encoders, rand_enc)
        log(f"  n={n:<5} {time.time() - t:6.1f} s")
    runs = pd.DataFrame(runs)
    runs.to_csv(OUT / "exhibit1_runs.csv", index=False)

    cells = (runs.groupby(["method", "n"])["dev_mse"]
                 .agg(mean="mean", sd="std", runs="count").reset_index())
    cells.to_csv(OUT / "exhibit1.csv", index=False)

    header = "| Method | " + " | ".join(f"n = {n}" for n in LABEL_COUNTS) + " | Runs/cell |"
    lines = [header, "|---|" + "---:|" * (len(LABEL_COUNTS) + 1)]
    for m in METHODS + ["mean_baseline"]:
        c = cells[cells.method == m].set_index("n")
        vals = " | ".join(f"{c.loc[n, 'mean']:.1f} ± {c.loc[n, 'sd']:.1f}"
                          for n in LABEL_COUNTS)
        lines.append(f"| {LABELS[m]} | {vals} | {int(c['runs'].iloc[0])} |")
    table = "\n".join(lines)
    (OUT / "exhibit1.md").write_text(
        "Exhibit 1. Dev MSE (MPa²), mean ± SD over runs. Lower is better.\n\n"
        + table + "\n")
    log("\n" + table)

    part1_numbers(cells)

    # ---- check 3: same numbers on a re-run --------------------------------
    log("\nCheck 3 -- re-run pre-training (seed 0) and cell n=50, draw 0")
    enc0_again = pretrain(traces, seed=0)
    same_enc = all(np.array_equal(a, b) for a, b in zip(encoders[0].W, enc0_again.W))
    log(f"  encoder 0 weights identical: {same_enc}")
    again = pd.DataFrame(run_cell(50, 0, Xtr, ytr, Xdev, ydev, encoders, rand_enc))
    first = runs[(runs.n == 50) & (runs.draw == 0)].reset_index(drop=True)
    same_runs = np.array_equal(first.dev_mse.to_numpy(), again.dev_mse.to_numpy())
    log(f"  all {len(again)} dev MSEs identical: {same_runs}")
    log(f"  -> {'PASS' if same_enc and same_runs else 'FAIL'}")

    log(f"\nTotal time {time.time() - t0:.0f} s")
    (OUT / "checks.txt").write_text("\n".join(log_lines) + "\n")


if __name__ == "__main__":
    main()
