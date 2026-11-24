"""The synthetic-control building blocks, shared by the sensitivity runs.

Same method as src/synthetic_control.py (the main results), written so the
quarters and donors can change. src/synth_sensitivity.py first rebuilds the
main results with this module and checks they match results/synth_fit.csv.
"""

from pathlib import Path

import numpy as np
import pandas as pd

PROJECT = Path(__file__).resolve().parent.parent
POST = pd.period_range("2017Q4", "2019Q4", freq="Q")
MAX_AVG_GAP, MAX_ONE_GAP = 4.0, 8.0          # the fit rule, in index points


def load_log_index(first="2013Q1", last="2019Q4"):
    """Log revenue index, one row per company, one column per quarter."""
    data = pd.read_csv(PROJECT / "data" / "processed" / "revenue_quarterly.csv")
    data["quarter_p"] = pd.PeriodIndex(data["quarter"], freq="Q")
    quarters = pd.period_range(first, last, freq="Q")
    return data.pivot(index="company", columns="quarter_p", values="log_index")[quarters]


def project_to_simplex(v):
    """Closest point to v whose entries are >= 0 and add up to 1."""
    u = np.sort(v)[::-1]
    css = np.cumsum(u) - 1
    k = np.nonzero(u - css / np.arange(1, len(v) + 1) > 0)[0][-1]
    return np.maximum(v - css[k] / (k + 1), 0)


def fit_weights(y1, Y0, steps=50_000):
    """Weights (>= 0, sum 1) making Y0 @ w closest to y1 (accelerated projected gradient)."""
    y1, Y0 = y1 - np.log(100), Y0 - np.log(100)   # same answer, better balanced
    L = 2 * np.linalg.eigvalsh(Y0.T @ Y0).max()
    w = np.full(Y0.shape[1], 1 / Y0.shape[1])
    z, t = w.copy(), 1.0
    for _ in range(steps):
        w_new = project_to_simplex(z - 2 * Y0.T @ (Y0 @ z - y1) / L)
        t_new = (1 + np.sqrt(1 + 4 * t * t)) / 2
        z = w_new + (t - 1) / t_new * (w_new - w)
        w, t = w_new, t_new
    w[w < 1e-6] = 0
    return w / w.sum()


def check_weights(y1, Y0, w, rng):
    """Optimality conditions hold, and no random weight set does better."""
    y1, Y0 = y1 - np.log(100), Y0 - np.log(100)
    g = 2 * Y0.T @ (Y0 @ w - y1)
    used = w > 0
    kkt_ok = np.ptp(g[used]) < 1e-5 and (g[~used] >= g[used].min() - 1e-5).all()
    random_w = rng.dirichlet(np.ones(len(w)) * 0.5, size=20_000)
    random_best = ((random_w @ Y0.T - y1) ** 2).sum(axis=1).min()
    return kkt_ok and np.sum((Y0 @ w - y1) ** 2) <= random_best + 1e-12


def run(LOG, treated, donors, fit_quarters, rule_quarters, rng):
    """Fit a twin; return weights, gaps (index points and log points) and the fit-rule verdict."""
    y1 = LOG.loc[treated, fit_quarters].values
    Y0 = LOG.loc[donors, fit_quarters].values.T
    w = fit_weights(y1, Y0)
    assert check_weights(y1, Y0, w, rng), f"weight check failed for {treated}"
    synth_log = pd.Series(LOG.loc[donors].values.T @ w, index=LOG.columns)
    gap_pts = np.exp(LOG.loc[treated]) - np.exp(synth_log)
    gap_log = LOG.loc[treated] - synth_log
    rule_gaps = gap_pts[rule_quarters].abs()
    rmspe = lambda qs: np.sqrt((gap_log[qs] ** 2).mean())
    return {"weights": pd.Series(w, index=donors), "synth_log": synth_log,
            "gap_pts": gap_pts, "gap_log": gap_log,
            "avg_abs_gap": rule_gaps.mean(), "max_abs_gap": rule_gaps.max(),
            "worst_quarter": str(rule_gaps.idxmax()),
            "passes": bool(rule_gaps.mean() <= MAX_AVG_GAP and rule_gaps.max() <= MAX_ONE_GAP),
            "pre_rmspe": rmspe(rule_quarters), "post_rmspe": rmspe(list(POST))}
