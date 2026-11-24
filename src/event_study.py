"""DiD warm-up: an event study on the log revenue index (Mixtape Ch 9).

The model, for company i in quarter t (2015 Q1 - 2019 Q4):

    log_index[i,t] = a[i] + b[t] + sum over quarters k (not 2017 Q2) of
                     beta[k] * treated[i] * (t == k) + error

  a[i]    company effect (each company's own level)
  b[t]    quarter effect (what moves all companies in that quarter)
  beta[k] how much further the treated group moved than the donors between
          the reference quarter 2017 Q2 and quarter k.

Before 2017 Q3 the betas should be about zero ("parallel pre-trends"). If they
are not, the betas after 2017 Q3 cannot be read as a Toys "R" Us effect.

Three treated companies are too few to trust regression standard errors
(Mixtape Ch 9 on inference with few treated clusters), so none are shown.
Instead every donor is run as a fake "treated" company against the other 7
(a placebo), and the treated coefficients are compared with those placebos.

Runs: pooled (Mattel + Hasbro + JAKKS vs 8 donors); each treated company alone
vs the 8 donors; each donor alone vs the other 7 donors.

Writes:
  results/event_study_coefficients.csv   every coefficient of every run
  results/event_study_summary.csv        pre and post averages and ranks
  results/event_study.png                the chart

Run from the project folder:
    .venv/bin/python src/event_study.py
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

PROJECT = Path(__file__).resolve().parent.parent
TREATED = ["Mattel", "Hasbro", "JAKKS Pacific"]
DONORS = ["Garmin", "Colgate-Palmolive", "Clorox", "Hershey", "WD-40", "Fossil Group",
          "Deckers Outdoor", "Columbia Sportswear"]
QUARTERS = pd.period_range("2015Q1", "2019Q4", freq="Q")
REF = pd.Period("2017Q2")
TRANSITION = pd.Period("2017Q3")
FREE_PRE = [p for p in pd.period_range("2015Q1", "2017Q1", freq="Q") if p.year != 2016]   # 2015 Q1-Q4, 2017 Q1
POST = pd.period_range("2017Q4", "2019Q4", freq="Q")

data = pd.read_csv(PROJECT / "data" / "processed" / "revenue_quarterly.csv")
data["quarter_p"] = pd.PeriodIndex(data["quarter"], freq="Q")
y_wide = data.pivot(index="company", columns="quarter_p", values="log_index")[QUARTERS]


def event_study(treated, controls):
    """Least-squares event study. Returns beta for every quarter (0 at the reference)."""
    units = treated + controls
    y = y_wide.loc[units]
    rows, target = [], []
    others = [q for q in QUARTERS if q != REF]
    for i, unit in enumerate(units):
        for t, q in enumerate(QUARTERS):
            x = np.zeros(len(units) + len(QUARTERS) - 1 + len(others))
            x[i] = 1                                         # company effect
            if t > 0:
                x[len(units) + t - 1] = 1                    # quarter effect (first quarter = baseline)
            if unit in treated and q != REF:
                x[len(units) + len(QUARTERS) - 1 + others.index(q)] = 1   # treated x quarter
            rows.append(x)
            target.append(y.loc[unit, q])
    coef, *_ = np.linalg.lstsq(np.array(rows), np.array(target), rcond=None)
    betas = pd.Series(coef[len(units) + len(QUARTERS) - 1:], index=others)
    betas[REF] = 0.0
    betas = betas.sort_index()
    # Check: with no gaps this equals the difference in mean changes since 2017 Q2.
    change = y.sub(y[REF], axis=0)
    by_hand = change.loc[treated].mean() - change.loc[controls].mean()
    assert np.allclose(betas.values, by_hand.values), "regression and hand calculation disagree"
    return betas


runs = {"Treated (pooled)": ("pooled", event_study(TREATED, DONORS))}
for t in TREATED:
    runs[t] = ("treated", event_study([t], DONORS))
for d in DONORS:
    runs[d] = ("placebo", event_study([d], [o for o in DONORS if o != d]))

coefs = pd.DataFrame({name: b for name, (_, b) in runs.items()}).T
coefs.columns = [str(c) for c in coefs.columns]
coefs.insert(0, "run", [kind for kind, _ in runs.values()])
coefs.round(4).to_csv(PROJECT / "results" / "event_study_coefficients.csv", index_label="company")

# --- Summary: is the pre-period flat? how big is the post-period? -----------
summary = []
for name, (kind, b) in runs.items():
    pre = b[FREE_PRE]
    summary.append({
        "company": name, "run": kind,
        "pre_mean": round(pre.mean(), 3),
        "pre_max_abs": round(pre.abs().max(), 3),
        "pre_max_abs_quarter": str(pre.abs().idxmax()),
        "coef_2017Q1": round(b[pd.Period("2017Q1")], 3),
        "coef_2016_all_quarters": round(b[pd.Period("2016Q1")], 3),
        "coef_2017Q3_transition": round(b[TRANSITION], 3),
        "post_mean": round(b[POST].mean(), 3),
        "post_mean_pct": round(100 * (np.exp(b[POST].mean()) - 1), 1),
    })
summary = pd.DataFrame(summary)
# Ranks among the 11 single-company runs (3 treated + 8 placebos), 1 = most negative.
single = summary["run"] != "pooled"
summary.loc[single, "post_rank_of_11"] = summary.loc[single, "post_mean"].rank().astype(int)
summary.loc[single, "pre_max_abs_rank_of_11"] = summary.loc[single, "pre_max_abs"].rank(ascending=False).astype(int)
summary.to_csv(PROJECT / "results" / "event_study_summary.csv", index=False)
pd.set_option("display.width", 220)
print("Free pre-quarters:", [str(p) for p in FREE_PRE], "| reference 2017Q2 | post 2017Q4-2019Q4")
print(summary.to_string(index=False))

# Pooled treated vs the spread of the 8 placebos, quarter by quarter.
placebo = pd.DataFrame({d: runs[d][1] for d in DONORS})
pooled = runs["Treated (pooled)"][1]
print("\nPooled coefficient and the placebo range, by quarter:")
print(pd.DataFrame({"pooled": pooled, "placebo_min": placebo.min(axis=1), "placebo_max": placebo.max(axis=1)})
      .round(3).T.to_string())

# --- A like-for-like placebo for the pooled run -------------------------------
# The pooled run averages 3 companies, which is smoother than any single donor.
# So also run every group of 3 donors (56 groups) against the other 5 donors.
from itertools import combinations
groups = []
for trio in combinations(DONORS, 3):
    b = event_study(list(trio), [d for d in DONORS if d not in trio])
    groups.append({"group": " + ".join(trio), "pre_max_abs": b[FREE_PRE].abs().max(), "post_mean": b[POST].mean()})
groups = pd.DataFrame(groups)
groups.round(4).to_csv(PROJECT / "results" / "event_study_three_donor_placebos.csv", index=False)
p_pre, p_post = pooled[FREE_PRE].abs().max(), pooled[POST].mean()
print(f"\nPooled treated: pre max |coef| = {p_pre:.3f}, post mean = {p_post:.3f}")
print(f"56 three-donor placebos: pre max |coef| from {groups['pre_max_abs'].min():.3f} to {groups['pre_max_abs'].max():.3f}; "
      f"{(groups['pre_max_abs'] <= p_pre).sum()} of 56 are as flat or flatter before")
print(f"  post mean from {groups['post_mean'].min():.3f} to {groups['post_mean'].max():.3f}; "
      f"{(groups['post_mean'] <= p_post).sum()} of 56 are as negative or more after")

# --- Chart ------------------------------------------------------------------
TEXT, MUTED, GRID = "#0b0b0b", "#52514e", "#eeede8"
BAND, PLACEBO = "#e3e2dc", "#b9b8b2"
COLORS = {"Mattel": "#2a78d6", "Hasbro": "#eb6834", "JAKKS Pacific": "#1baf7a"}   # categorical slots 1-3
x = np.arange(len(QUARTERS))
xl = [str(q) if q.quarter == 1 else "" for q in QUARTERS]
ref_x, tr_x = list(QUARTERS).index(REF), list(QUARTERS).index(TRANSITION)

fig, axes = plt.subplots(1, 2, figsize=(15, 5.2), sharey=True)
for ax in axes:
    ax.axhline(0, color="#a9a8a1", lw=0.9, zorder=1)
    ax.axvspan(tr_x - 0.5, tr_x + 0.5, color="#f1f0eb", zorder=0)
    ax.axvline(ref_x, color="#a9a8a1", lw=0.8, ls=":", zorder=1)
    ax.set_xticks(x)
    ax.set_xticklabels(xl, fontsize=9)
    ax.grid(axis="y", color=GRID, lw=0.6)
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    ax.tick_params(colors=MUTED, length=0)

ax = axes[0]
ax.fill_between(x, placebo.min(axis=1), placebo.max(axis=1), color=BAND, zorder=1,
                label="Range of the 8 donor placebos")
ax.plot(x, pooled.values, color=TEXT, lw=2, marker="o", ms=4, zorder=3, label="Mattel + Hasbro + JAKKS (pooled)")
ax.set_title("Pooled treated vs the placebo range", loc="left", fontsize=12, color=TEXT)
ax.set_ylabel("Coefficient (log points vs 2017 Q2;\n0.1 ≈ +10 %)", fontsize=10)
ax.legend(loc="lower left", frameon=False, fontsize=9)
ax.text(ref_x, ax.get_ylim()[1] if False else 0.47, "ref.\n2017 Q2", ha="center", va="top", fontsize=8, color=MUTED)

ax = axes[1]
for d in DONORS:
    ax.plot(x, placebo[d].values, color=PLACEBO, lw=1, zorder=2)
for t in TREATED:
    ax.plot(x, runs[t][1].values, color=COLORS[t], lw=2, marker="o", ms=4, zorder=3, label=t)
# End labels, pushed apart so they never overlap (at least 0.05 apart).
ends = sorted((runs[t][1].values[-1], t) for t in TREATED)
placed = []
for value, t in ends:
    y_pos = max(value, placed[-1] + 0.05) if placed else value
    placed.append(y_pos)
    ax.text(x[-1] + 0.3, y_pos, t, color=TEXT, fontsize=9, va="center")
ax.plot([], [], color=PLACEBO, lw=1, label="Each donor as a placebo")
ax.legend(loc="lower left", frameon=False, fontsize=9)
ax.set_title("Each treated company vs each donor placebo", loc="left", fontsize=12, color=TEXT)
ax.set_xlim(-0.5, len(x) + 2.5)
ax.text(tr_x, 0.47, "2017 Q3\ntransition", ha="center", va="top", fontsize=8, color=MUTED)
axes[0].set_ylim(-0.6, 0.5)

fig.suptitle("Event study on the log revenue index, 2015-2019 (reference quarter 2017 Q2)",
             x=0.01, ha="left", fontsize=13, color=TEXT)
fig.tight_layout(rect=(0, 0, 1, 0.94))
fig.savefig(PROJECT / "results" / "event_study.png", dpi=150)
print("\nSaved results/event_study.png, results/event_study_coefficients.csv, results/event_study_summary.csv")
