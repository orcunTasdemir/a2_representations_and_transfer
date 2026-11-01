"""
Assignment 2 starter -- Kestrel Composites.

Everything you need is here.  You should not have to write a neural network,
a training loop, or a masking routine; you should have to decide what to run,
read the results, and say what they mean.

    from kestrel import *

    Xtr, ytr = load("train")          # gauges (standardised), strength
    Xdev, ydev = load("dev")
    traces = load("traces")           # unlabeled, standardised, no y

    enc = pretrain(traces, seed=0)    # self-supervised, ~10 s
    print(frozen_ridge(enc, Xtr[:100], ytr[:100], Xdev, ydev))

Five things you can do to the data, and nothing else:

    ridge(Xtr, ytr, Xte, yte)             a regularized linear model
    pretrain(pool, seed)                  masked reconstruction -> an encoder
    random_encoder(seed)                  an encoder that was never trained
    frozen_ridge(enc, ...)                freeze the encoder, ridge on top
    supervised(Xtr, ytr, Xte, yte, seed)  train a network end to end,
                                          from scratch or from an encoder

All five return a test MSE on whatever evaluation set you pass, except
`pretrain` and `random_encoder`, which return an encoder.
"""
from pathlib import Path

import numpy as np
import pandas as pd

from mlp import MLP

DATA = Path(__file__).resolve().parents[1] / "data"
TARGET = "strength_mpa"
ID = "panel_id"

FILES = {"train": "labeled_train.csv", "dev": "labeled_dev.csv",
         "test": "labeled_test.csv", "traces": "unlabeled_traces.csv.gz"}

# ---- the protocol, fixed by the brief ------------------------------------
MASK_FRACTION = 0.30      # share of gauges hidden at each pre-training step
ENCODER_SHAPE = (64, 16)  # hidden layers; the representation is the first
PRETRAIN_EPOCHS = 40
PRETRAIN_LR = 3e-3
PRETRAIN_BATCH = 256
HEAD_WIDTH = 64
SCRATCH_LR = 2e-3
FINETUNE_LR = 1e-3        # reduced, as Handout 9 S3.2 prescribes
MAX_EPOCHS = 800
BATCH = 32
PATIENCE = 60
VAL_FRACTION = 0.25
RIDGE_ALPHAS = np.logspace(-2, 5, 40)

LABEL_COUNTS = (50, 100, 250, 1000)
N_REPLICATES = 5       # independent label draws per cell
N_ENCODER_SEEDS = 3    # independent pre-training runs per cell

_STATS = None


def _standardizer():
    """Centre and scale using the TRAINING gauges only.  Computed once."""
    global _STATS
    if _STATS is None:
        raw = pd.read_csv(DATA / FILES["train"])
        G = raw.drop(columns=[ID, TARGET]).to_numpy(float)
        _STATS = (G.mean(0), G.std(0) + 1e-9)
    return _STATS


def load(which):
    """load('train') -> (X, y).   load('traces') -> X.

    X is always standardised with the training-set statistics, so every matrix
    you touch is on the same scale.
    """
    if which not in FILES:
        raise KeyError(f"unknown file {which!r}; options: {sorted(FILES)}")
    df = pd.read_csv(DATA / FILES[which])
    mu, sd = _standardizer()
    X = (df.drop(columns=[c for c in (ID, TARGET) if c in df.columns])
           .to_numpy(float) - mu) / sd
    if TARGET in df.columns:
        return X, df[TARGET].to_numpy(float)
    return X


def gauge_names():
    return [c for c in pd.read_csv(DATA / FILES["train"], nrows=1).columns
            if c not in (ID, TARGET)]


def label_subset(n, replicate):
    """The indices of the n labelled panels for one replicate.

    The brief asks for N_REPLICATES independent draws at each label count,
    because with 50 labels the answer depends on WHICH 50 you happened to
    test.  These indices are fixed by (n, replicate), so everyone's table is
    comparable and yours reproduces.
    """
    rng = np.random.default_rng(9000 + 100 * replicate + n)
    n_train = len(pd.read_csv(DATA / FILES["train"], usecols=[ID]))
    return rng.choice(n_train, n, replace=False)


# ---------------------------------------------------------------- the models
def ridge(Xtr, ytr, Xte, yte, seed=0):
    """Ridge regression.  Penalty chosen on a 75/25 split of the labels."""
    Xtr, Xte = np.asarray(Xtr, float), np.asarray(Xte, float)
    A = np.hstack([Xtr, np.ones((len(Xtr), 1))])
    B = np.hstack([Xte, np.ones((len(Xte), 1))])
    rng = np.random.default_rng(seed)
    o = rng.permutation(len(A))
    cut = max(12, int(0.75 * len(A)))
    fit, val = o[:cut], o[cut:]
    I = np.eye(A.shape[1])
    best, best_a = np.inf, RIDGE_ALPHAS[0]
    for a in RIDGE_ALPHAS:
        W = np.linalg.solve(A[fit].T @ A[fit] + a * I, A[fit].T @ ytr[fit])
        e = np.mean((A[val] @ W - ytr[val]) ** 2)
        if e < best:
            best, best_a = e, a
    W = np.linalg.solve(A.T @ A + best_a * I, A.T @ ytr)
    return float(np.mean((B @ W - yte) ** 2))


def pretrain(pool, seed=0, epochs=PRETRAIN_EPOCHS, mask_fraction=MASK_FRACTION):
    """Self-supervised pre-training: hide gauges, rebuild them.

    No labels are used or needed.  A fresh set of gauges is hidden at every
    epoch -- that re-drawing is what forces the network to learn the process
    rather than memorise one corruption.

    Returns the encoder.  Pre-train ONCE per pool and reuse it; it is by far
    the most expensive thing here (~10 seconds) and nothing about it depends on
    the labels.
    """
    pool = np.asarray(pool, float)
    rng = np.random.default_rng(seed)
    net = MLP([pool.shape[1], *ENCODER_SHAPE, pool.shape[1]], seed=seed)
    for ep in range(epochs):
        corrupted = pool.copy()
        corrupted[rng.random(pool.shape) < mask_fraction] = 0.0
        net.fit(corrupted, pool, epochs=1, batch_size=PRETRAIN_BATCH,
                lr=PRETRAIN_LR, seed=seed * 1000 + ep)
    return net


def random_encoder(seed=99):
    """An encoder of identical shape whose weights were never trained.

    Handout 9 S3.3: without this you cannot tell 'pre-training learned
    something' from 'this architecture makes useful random features'.
    """
    n = len(gauge_names())
    return MLP([n, *ENCODER_SHAPE, n], seed=seed)


def representation(enc, X):
    """The learned features: the encoder's first hidden layer, 64 numbers.

    160 gauges in, 64 learned features out.  Handout 9 S3.4 is about which
    layer to take; the brief fixes it at the first so that everyone's table
    is comparable.
    """
    return enc.hidden(np.asarray(X, float), layer=1)


def frozen_ridge(enc, Xtr, ytr, Xte, yte, seed=0):
    """Freeze the encoder, fit ridge on its representation.  Handout 9 S2.1."""
    return ridge(representation(enc, Xtr), ytr,
                 representation(enc, Xte), yte, seed=seed)


def supervised(Xtr, ytr, Xte, yte, seed=0, encoder=None):
    """Train a network end to end and return its test MSE.

    encoder=None  -> from scratch, at SCRATCH_LR.
    encoder=enc   -> fine-tuning: start from the pre-trained weights and train
                     everything at the reduced FINETUNE_LR.

    The target is centred before fitting and the mean added back afterwards.
    Without that the output layer starts far from the data and, with only 50
    labels and early stopping, never gets there.
    """
    Xtr, Xte = np.asarray(Xtr, float), np.asarray(Xte, float)
    rng = np.random.default_rng(seed)
    o = rng.permutation(len(Xtr))
    cut = max(12, int((1 - VAL_FRACTION) * len(Xtr)))
    fit, val = o[:cut], o[cut:]
    centre = ytr.mean()
    net = MLP([Xtr.shape[1], HEAD_WIDTH, 1], seed=seed)
    if encoder is not None:
        net.copy_body_from(encoder)
    net.fit(Xtr[fit], ytr[fit] - centre, epochs=MAX_EPOCHS, batch_size=BATCH,
            lr=(SCRATCH_LR if encoder is None else FINETUNE_LR), seed=seed,
            X_val=Xtr[val], Y_val=ytr[val] - centre, patience=PATIENCE)
    return float(np.mean((net.predict(Xte).ravel() + centre - yte) ** 2))


if __name__ == "__main__":
    Xtr, ytr = load("train")
    Xdev, ydev = load("dev")
    print(f"train {Xtr.shape}   dev {Xdev.shape}   "
          f"traces {load('traces').shape}")
    print(f"strength: mean {ytr.mean():.1f}  var(dev) {ydev.var():.1f}")
    print("\nsmoke test (n=100, one replicate):")
    i = label_subset(100, 0)
    print(f"  ridge on the 160 gauges    {ridge(Xtr[i], ytr[i], Xdev, ydev):7.1f}")
    enc = pretrain(load("traces"), seed=0)
    print(f"  frozen encoder + ridge     {frozen_ridge(enc, Xtr[i], ytr[i], Xdev, ydev):7.1f}")
    print(f"  frozen random + ridge      "
          f"{frozen_ridge(random_encoder(), Xtr[i], ytr[i], Xdev, ydev):7.1f}")
    print(f"  network from scratch       {supervised(Xtr[i], ytr[i], Xdev, ydev, 0):7.1f}")
