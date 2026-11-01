"""
A small multilayer perceptron in numpy, for Assignment 2.

You should not need to open this file. `kestrel.py` wraps everything the
assignment asks for. It is here so that nothing in the pipeline is a black box
you could not inspect if you wanted to.

    MLP(sizes)              e.g. MLP([160, 64, 1]) -- one hidden layer of 64
    .fit(X, Y, ...)         Adam, mini-batch, optional early stopping
    .predict(X)
    .hidden(X, layer=1)     the activations of a hidden layer -- the learned
                            representation, which is what gets frozen and reused
    .copy_body_from(other)  copy all layers except the last, which is how a
                            fine-tuned network is initialised from an encoder

Everything is float64 numpy. No GPU, no autograd; the backward pass is written
out. You are not responsible for it. You ARE responsible for knowing what the
model consumes, produces, and assumes.
"""
import numpy as np


def _relu(z):
    return np.maximum(z, 0.0)


class MLP:
    def __init__(self, sizes, seed=0):
        """sizes = [n_in, n_hidden_1, ..., n_out]."""
        self.sizes = list(sizes)
        rng = np.random.default_rng(seed)
        self.W, self.b = [], []
        for a, b in zip(self.sizes[:-1], self.sizes[1:]):
            # He initialisation
            self.W.append(rng.normal(0, np.sqrt(2.0 / a), (a, b)))
            self.b.append(np.zeros(b))

    # ------------------------------------------------------------------ core
    def _forward(self, X):
        acts = [X]
        h = X
        for i, (W, b) in enumerate(zip(self.W, self.b)):
            z = h @ W + b
            h = z if i == len(self.W) - 1 else _relu(z)   # linear output layer
            acts.append(h)
        return acts

    def predict(self, X):
        return self._forward(np.asarray(X, dtype=float))[-1]

    def hidden(self, X, layer=1):
        """Activations after `layer` hidden layers.  layer=1 is the first.

        This is the learned representation. Handout 9 S3.4 is about which layer
        to take; Assignment 2 fixes it at the first so that every submission's
        table is comparable.
        """
        return self._forward(np.asarray(X, dtype=float))[layer]

    def copy_body_from(self, other):
        """Copy every layer except the last.  Shapes must match.

        This is what turns a pre-trained encoder into the starting point for a
        fine-tuned predictor: the body carries over, the output layer is new.
        """
        n = len(self.W) - 1
        for i in range(n):
            self.W[i] = other.W[i].copy()
            self.b[i] = other.b[i].copy()
        return self

    # ------------------------------------------------------------------- fit
    def fit(self, X, Y, epochs=200, batch_size=64, lr=1e-3, seed=0,
            X_val=None, Y_val=None, patience=None, verbose=False):
        """Mini-batch Adam on mean squared error.

        If X_val/Y_val and `patience` are given, stops when validation MSE has
        not improved for `patience` epochs and restores the best weights.
        Returns a history dict.
        """
        X = np.asarray(X, dtype=float)
        Y = np.asarray(Y, dtype=float)
        if Y.ndim == 1:
            Y = Y[:, None]
        rng = np.random.default_rng(seed)
        n = len(X)

        mW = [np.zeros_like(w) for w in self.W]
        vW = [np.zeros_like(w) for w in self.W]
        mb = [np.zeros_like(b) for b in self.b]
        vb = [np.zeros_like(b) for b in self.b]
        b1, b2, eps, step = 0.9, 0.999, 1e-8, 0

        hist = {"train": [], "val": []}
        best, best_epoch, best_w = np.inf, 0, None

        for ep in range(epochs):
            order = rng.permutation(n)
            for s in range(0, n, batch_size):
                idx = order[s:s + batch_size]
                xb, yb = X[idx], Y[idx]
                acts = self._forward(xb)
                delta = 2.0 * (acts[-1] - yb) / len(idx)
                step += 1
                for i in range(len(self.W) - 1, -1, -1):
                    gW = acts[i].T @ delta
                    gb = delta.sum(axis=0)
                    if i > 0:
                        delta = (delta @ self.W[i].T) * (acts[i] > 0)
                    for g, m, v, p in ((gW, mW, vW, self.W), (gb, mb, vb, self.b)):
                        m[i] = b1 * m[i] + (1 - b1) * g
                        v[i] = b2 * v[i] + (1 - b2) * g * g
                        mh = m[i] / (1 - b1 ** step)
                        vh = v[i] / (1 - b2 ** step)
                        p[i] -= lr * mh / (np.sqrt(vh) + eps)

            tr = float(np.mean((self.predict(X) - Y) ** 2))
            hist["train"].append(tr)
            if X_val is not None:
                Yv = np.asarray(Y_val, dtype=float)
                if Yv.ndim == 1:
                    Yv = Yv[:, None]
                va = float(np.mean((self.predict(X_val) - Yv) ** 2))
                hist["val"].append(va)
                if va < best - 1e-9:
                    best, best_epoch = va, ep
                    best_w = ([w.copy() for w in self.W], [b.copy() for b in self.b])
                elif patience is not None and ep - best_epoch >= patience:
                    if verbose:
                        print(f"early stop at epoch {ep}, best {best:.4f} @ {best_epoch}")
                    break
            if verbose and ep % 20 == 0:
                print(f"epoch {ep:4d}  train {tr:10.4f}"
                      + (f"  val {hist['val'][-1]:10.4f}" if hist["val"] else ""))

        if patience is not None and best_w is not None:
            self.W, self.b = best_w
        hist["best_epoch"] = best_epoch
        return hist
