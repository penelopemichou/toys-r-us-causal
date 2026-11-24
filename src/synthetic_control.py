"""Synthetic control (Mixtape Ch 11): one "twin" per toy company.

The twin is a weighted average of the 8 donors' log revenue index, with
weights between 0 and 1 that add up to 1. The weights are chosen so that the
twin follows the toy company as closely as possible in the pre-period
(2015 Q1 - 2017 Q2). The 2016 quarters are 100 for every company (that is how
the index is built), so in practice the 6 free quarters decide the weights.

Order of work (as decided before running):
  1. Fit each twin and apply the FIT RULE on the 6 free pre-quarters:
     average absolute gap <= 4 index points AND no quarter off by more than 8.
     The 2017 Q1-Q2 gap is also reported on its own.
  2. Donor weights; leave-one-out (refit without the largest-weight donor).
  3. Placebo in space: each donor gets a twin from the other 7; every company
     is ranked by (post-period error / pre-period error).
  4. Only then the post-period gaps: as an estimate for twins that pass the
     fit rule, and "for information, not an effect" for twins that fail.
JAKKS is run twice: with and without its flagged 2015 Q1.

The weights are found with numpy only (projected gradient descent on the
"weights between 0 and 1 adding to 1" set), and checked two ways (optimality
conditions and 20,000 random weight sets).

Writes (all in results/):
  synth_fit.csv, synth_weights.csv, synth_leave_one_out.csv,
  synth_placebo_ratios.csv, synth_gaps.csv,
  synth_credible.png (only if a twin passes), synth_for_information.png,
  synth_placebo_ratios.png

Run from the project folder:
    .venv/bin/python src/synthetic_control.py
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

PROJECT = Path(__file__).resolve().parent.parent
RESULTS = PROJECT / "results"
TREATED = ["Mattel", "Hasbro", "JAKKS Pacific"]
DONORS = ["Garmin", "Colgate-Palmolive", "Clorox", "Hershey", "WD-40", "Fossil Group",
          "Deckers Outdoor", "Columbia Sportswear"]
QUARTERS = pd.period_range("2015Q1", "2019Q4", freq="Q")
PRE = pd.period_range("2015Q1", "2017Q2", freq="Q")
FREE = [q for q in PRE if q.year != 2016]                  # 2015 Q1-Q4, 2017 Q1-Q2
LATE_PRE = [pd.Period("2017Q1"), pd.Period("2017Q2")]
TRANSITION = pd.Period("2017Q3")
POST = pd.period_range("2017Q4", "2019Q4", freq="Q")
MAX_AVG_GAP, MAX_ONE_GAP = 4.0, 8.0                        # the fit rule, in index points

data = pd.read_csv(PROJECT / "data" / "processed" / "revenue_quarterly.csv")
data["quarter_p"] = pd.PeriodIndex(data["quarter"], freq="Q")
LOG = data.pivot(index="company", columns="quarter_p", values="log_index")[QUARTERS]


# --- 1. The weight solver ----------------------------------------------------
def project_to_simplex(v):
    """Closest point to v whose entries are >= 0 and add up to 1."""
    u = np.sort(v)[::-1]
    css = np.cumsum(u) - 1
    k = np.nonzero(u - css / np.arange(1, len(v) + 1) > 0)[0][-1]
    return np.maximum(v - css[k] / (k + 1), 0)


def fit_weights(y1, Y0, steps=50_000):
    """Weights w (>= 0, sum 1) that make Y0 @ w as close as possible to y1.

    y1: the toy company's pre-period values; Y0: the donors' (one column each).
    Projected gradient descent: take a small step downhill, then pull the
    weights back into the allowed set; repeat. The problem is convex, so this
    reaches the best weights.
    Every log index is about ln(100) = 4.6, which makes the problem badly
    balanced and slow. Because the weights add up to 1, subtracting the same
    number from every value changes nothing in the answer, so we subtract ln(100).
    """
    y1, Y0 = y1 - np.log(100), Y0 - np.log(100)
    L = 2 * np.linalg.eigvalsh(Y0.T @ Y0).max()     # step size from the curvature
    w = np.full(Y0.shape[1], 1 / Y0.shape[1])
    z, t = w.copy(), 1.0
    for _ in range(steps):                          # accelerated version (FISTA)
        w_new = project_to_simplex(z - 2 * Y0.T @ (Y0 @ z - y1) / L)
        t_new = (1 + np.sqrt(1 + 4 * t * t)) / 2
        z = w_new + (t - 1) / t_new * (w_new - w)
        w, t = w_new, t_new
    w[w < 1e-6] = 0
    return w / w.sum()


def check_weights(y1, Y0, w, rng):
    """Two checks that w really is the best: optimality conditions and random tries."""
    y1, Y0 = y1 - np.log(100), Y0 - np.log(100)     # same shift as in fit_weights
    loss = lambda v: np.sum((Y0 @ v - y1) ** 2)
    g = 2 * Y0.T @ (Y0 @ w - y1)
    used = w > 0
    # At the best point, every donor with weight > 0 has the same (smallest) slope.
    kkt_ok = np.ptp(g[used]) < 1e-5 and (g[~used] >= g[used].min() - 1e-5).all()
    random_w = rng.dirichlet(np.ones(len(w)) * 0.5, size=20_000)
    random_best = ((random_w @ Y0.T - y1) ** 2).sum(axis=1).min()
    return kkt_ok and loss(w) <= random_best + 1e-12


# --- 2. One synthetic-control run --------------------------------------------
def run(treated, donors, fit_quarters, rule_quarters, rng):
    """Fit a twin for `treated` from `donors`; return weights, gaps and errors."""
    y1 = LOG.loc[treated, fit_quarters].values
    Y0 = LOG.loc[donors, fit_quarters].values.T
    w = fit_weights(y1, Y0)
    assert check_weights(y1, Y0, w, rng), f"weight check failed for {treated}"
    synth_log = pd.Series(LOG.loc[donors].values.T @ w, index=QUARTERS)
    actual_log = LOG.loc[treated]
    # Gaps in index points (index = exp(log index)) and in log points.
    gap_pts = np.exp(actual_log) - np.exp(synth_log)
    gap_log = actual_log - synth_log
    rule_gaps = gap_pts[rule_quarters].abs()
    rmspe = lambda qs: np.sqrt((gap_log[qs] ** 2).mean())
    return {
        "weights": pd.Series(w, index=donors),
        "synth_log": synth_log, "gap_pts": gap_pts, "gap_log": gap_log,
        "avg_abs_gap": rule_gaps.mean(), "max_abs_gap": rule_gaps.max(),
        "worst_quarter": str(rule_gaps.idxmax()),
        "passes": bool(rule_gaps.mean() <= MAX_AVG_GAP and rule_gaps.max() <= MAX_ONE_GAP),
        "gap_2017Q1": gap_pts[LATE_PRE[0]], "gap_2017Q2": gap_pts[LATE_PRE[1]],
        "pre_rmspe": rmspe(rule_quarters), "post_rmspe": rmspe(list(POST)),
    }


rng = np.random.default_rng(0)
FREE_NO_15Q1 = [q for q in FREE if q != pd.Period("2015Q1")]
SPECS = {   # run name -> (company, fit quarters, fit-rule quarters)
    "Mattel": ("Mattel", list(PRE), FREE),
    "Hasbro": ("Hasbro", list(PRE), FREE),
    "JAKKS Pacific": ("JAKKS Pacific", list(PRE), FREE),
    "JAKKS Pacific (without 2015 Q1)": ("JAKKS Pacific", [q for q in PRE if q != pd.Period("2015Q1")], FREE_NO_15Q1),
}
results = {name: run(c, DONORS, fq, rq, rng) for name, (c, fq, rq) in SPECS.items()}

# --- Step 1: the fit rule, before anything about the post-period -------------
fit = pd.DataFrame([{
    "run": name, "fit_rule_quarters": len(SPECS[name][2]),
    "avg_abs_gap_pts": round(r["avg_abs_gap"], 2), "max_abs_gap_pts": round(r["max_abs_gap"], 2),
    "worst_quarter": r["worst_quarter"],
    "gap_2017Q1_pts": round(r["gap_2017Q1"], 2), "gap_2017Q2_pts": round(r["gap_2017Q2"], 2),
    "gap_2015Q1_pts": round(r["gap_pts"][pd.Period("2015Q1")], 2),
    "verdict": "credible twin" if r["passes"] else "no credible twin",
} for name, r in results.items()])
fit.to_csv(RESULTS / "synth_fit.csv", index=False)
pd.set_option("display.width", 220)
print("STEP 1 - FIT RULE (pre-period only; gaps = toy company minus twin, index points)")
print(fit.to_string(index=False))

# --- Step 2: weights and leave-one-out ---------------------------------------
weights = pd.DataFrame({name: r["weights"] for name, r in results.items()}).round(3)
weights.to_csv(RESULTS / "synth_weights.csv", index_label="donor")
print("\nSTEP 2 - DONOR WEIGHTS (each column adds up to 1)")
print(weights.to_string())

loo_rows = []
for name, r in results.items():
    company, fq, rq = SPECS[name]
    top = r["weights"].idxmax()
    r2 = run(company, [d for d in DONORS if d != top], fq, rq, rng)
    loo_rows.append({"run": name, "left_out": top, "left_out_weight": round(r["weights"][top], 3),
                     "avg_abs_gap_before": round(r["avg_abs_gap"], 2), "avg_abs_gap_after": round(r2["avg_abs_gap"], 2),
                     "max_abs_gap_before": round(r["max_abs_gap"], 2), "max_abs_gap_after": round(r2["max_abs_gap"], 2),
                     "verdict_after": "credible twin" if r2["passes"] else "no credible twin",
                     "new_weights": ", ".join(f"{d} {v:.2f}" for d, v in r2["weights"][r2["weights"] > 0]
                                              .sort_values(ascending=False).items()),
                     "post_mean_log_gap_after": round(r2["gap_log"][POST].mean(), 3)})
loo = pd.DataFrame(loo_rows)
loo.to_csv(RESULTS / "synth_leave_one_out.csv", index=False)
print("\nLEAVE-ONE-OUT (refit without the largest-weight donor; pre-period fit)")
print(loo.drop(columns=["post_mean_log_gap_after"]).to_string(index=False))

# --- Step 3: placebo in space --------------------------------------------------
def placebo_ratios(fit_quarters, rule_quarters):
    out = {}
    for d in DONORS:
        r = run(d, [o for o in DONORS if o != d], fit_quarters, rule_quarters, rng)
        out[d] = (r["post_rmspe"] / r["pre_rmspe"], r["passes"], r["pre_rmspe"], r["post_rmspe"])
    return out

placebo_main = placebo_ratios(list(PRE), FREE)
placebo_no15 = placebo_ratios(SPECS["JAKKS Pacific (without 2015 Q1)"][1], FREE_NO_15Q1)
rank_rows = []
for name, r in results.items():
    pool = placebo_no15 if "without" in name else placebo_main
    ratio = r["post_rmspe"] / r["pre_rmspe"]
    all_ratios = [ratio] + [v[0] for v in pool.values()]
    rank = 1 + sum(x > ratio for x in all_ratios[1:])
    rank_rows.append({"run": name, "pre_rmspe": round(r["pre_rmspe"], 4), "post_rmspe": round(r["post_rmspe"], 4),
                      "ratio": round(ratio, 2), "rank_of_9": rank, "share_as_extreme": f"{rank}/9",
                      "twin": "credible" if r["passes"] else "no credible twin"})
ranks = pd.DataFrame(rank_rows)
plac = pd.DataFrame([{"donor": d, "ratio": round(v[0], 2), "pre_rmspe": round(v[2], 4), "post_rmspe": round(v[3], 4),
                      "twin_passes_fit_rule": v[1]} for d, v in placebo_main.items()]).sort_values("ratio", ascending=False)
pd.concat([ranks.assign(kind="treated"), plac.rename(columns={"donor": "run"}).assign(kind="placebo")]) \
    .to_csv(RESULTS / "synth_placebo_ratios.csv", index=False)
print("\nSTEP 3 - PLACEBO IN SPACE: ratio = post-period error / pre-period error (rank 1 = largest of 9)")
print(ranks.to_string(index=False))
print("Donor placebos (main pre-period):")
print(plac.to_string(index=False))

# --- Step 4: post-period gaps, labelled by the fit rule ------------------------
gaps = pd.DataFrame({name: r["gap_pts"] for name, r in results.items()})
gaps.index = gaps.index.astype(str)
gaps.round(2).to_csv(RESULTS / "synth_gaps.csv", index_label="quarter")
print("\nSTEP 4 - POST-PERIOD GAP (2017 Q4-2019 Q4), toy company minus twin")
for name, r in results.items():
    label = "ESTIMATE" if r["passes"] else "FOR INFORMATION, NOT AN EFFECT (no credible twin)"
    m = r["gap_log"][POST].mean()
    print(f"  {name:34s} mean {r['gap_pts'][POST].mean():6.1f} index points, "
          f"{100 * (np.exp(m) - 1):6.1f} %  [{label}]")

# --- Charts ----------------------------------------------------------------------
TEXT, MUTED, GRID = "#0b0b0b", "#52514e", "#eeede8"
ACTUAL, TWIN = "#2a78d6", "#eb6834"      # categorical slots 1 and 2
x = np.arange(len(QUARTERS))
xl = [str(q) if q.quarter == 1 else "" for q in QUARTERS]
tr_x = list(QUARTERS).index(TRANSITION)


def path_chart(names, title, file_name, banner=None):
    fig, axes = plt.subplots(1, len(names), figsize=(5 * len(names), 4.8), sharey=True, squeeze=False)
    for ax, name in zip(axes[0], names):
        r = results[name]
        company = SPECS[name][0]
        ax.plot(x, np.exp(LOG.loc[company].values), color=ACTUAL, lw=2.2, label=company)
        ax.plot(x, np.exp(r["synth_log"].values), color=TWIN, lw=2, ls="--", label="Twin (weighted donors)")
        ax.axvspan(tr_x - 0.5, tr_x + 0.5, color="#f1f0eb", zorder=0)
        ax.axhline(100, color="#d7d6d0", lw=0.8, zorder=0)
        ax.set_title(f"{name}\nfit: avg {r['avg_abs_gap']:.1f}, worst {r['max_abs_gap']:.1f} pts "
                     f"({'passes' if r['passes'] else 'fails'})", loc="left", fontsize=10, color=TEXT)
        ax.set_xticks(x)
        ax.set_xticklabels(xl, fontsize=8)
        ax.grid(axis="y", color=GRID, lw=0.6)
        for s in ["top", "right"]:
            ax.spines[s].set_visible(False)
        ax.tick_params(colors=MUTED, length=0)
        ax.legend(loc="lower left", frameon=False, fontsize=8)
    axes[0][0].set_ylabel("Revenue index (same quarter of 2016 = 100)", fontsize=9)
    fig.suptitle(title, x=0.01, ha="left", fontsize=12, color=TEXT)
    if banner:
        fig.text(0.01, 0.905, banner, fontsize=10, color="#b42318", ha="left")
    fig.tight_layout(rect=(0, 0, 1, 0.86 if banner else 0.92))
    fig.savefig(RESULTS / file_name, dpi=150)
    plt.close(fig)


passed = [n for n, r in results.items() if r["passes"]]
failed = [n for n, r in results.items() if not r["passes"]]
if passed:
    path_chart(passed, "Synthetic control: toy companies with a credible twin (2017 Q3 shaded = transition)",
               "synth_credible.png")
    print("Saved results/synth_credible.png")
if failed:
    path_chart(failed, "Synthetic control: NO CREDIBLE TWIN (fails the fit rule)", "synth_for_information.png",
               banner="For information, not an effect: the twin does not follow the company before 2017 Q3, "
                      "so the gap after it cannot be read as a Toys \"R\" Us effect.")
    print("Saved results/synth_for_information.png")

# Placebo ratio chart (main pre-period): one bar per unit, sorted.
fig, ax = plt.subplots(figsize=(9, 4.6))
items = [(n, results[n]["post_rmspe"] / results[n]["pre_rmspe"], "treated", results[n]["passes"])
         for n in ["Mattel", "Hasbro", "JAKKS Pacific"]] + \
        [(d, v[0], "placebo", v[1]) for d, v in placebo_main.items()]
items.sort(key=lambda it: it[1])
for i, (n, ratio, kind, ok) in enumerate(items):
    ax.barh(i, ratio, color=ACTUAL if kind == "treated" else "#b9b8b2", height=0.6)
    note = "" if kind == "placebo" else ("  (credible twin)" if ok else "  (no credible twin: not an effect)")
    ax.text(ratio + 0.1, i, f"{ratio:.1f}{note}", va="center", fontsize=8, color=TEXT)
ax.set_yticks(range(len(items)))
ax.set_yticklabels([it[0] for it in items], fontsize=9)
ax.set_xlabel("Post-period error ÷ pre-period error (bigger = later gap large compared with the fit before)", fontsize=9)
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
ax.tick_params(colors=MUTED, length=0)
ax.set_title("Placebo in space: toy companies (blue) among the 8 donor placebos (gray)", loc="left",
             fontsize=11, color=TEXT)
ax.set_xlim(0, max(it[1] for it in items) * 1.3)
fig.tight_layout()
fig.savefig(RESULTS / "synth_placebo_ratios.png", dpi=150)
print("Saved results/synth_placebo_ratios.png")
