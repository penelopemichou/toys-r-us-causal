"""Build the revenue index, one chart and the pre-period trend table. No models.

Steps:
  1. Quarterly revenue, as first reported, 2013 Q1 - 2019 Q4, for the 3 treated
     companies, the 8 donors and Electronic Arts (sensitivity only).
     Every 14-week quarter (53-week years) is scaled by 13/14 in the main series.
  2. Index = revenue / revenue in the same quarter of 2016 x 100. Dividing by the
     same quarter removes the seasonal pattern (Q4 is always the big quarter).
     log_index = natural log of the index (the outcome the models will use).
  3. Chart: each treated company against the 8 donors, 2015 Q1 - 2019 Q4.
  4. Pre-period trend (2015 Q1 - 2017 Q2): the slope of log_index on time,
     turned into "% per year", plus how far the quarters wander around that line.

Writes:
  data/processed/revenue_quarterly.csv   revenue and index, one row per company and quarter
  results/index_treated_vs_donors.png    the chart
  results/pretrend_table.csv             the trend table

Run from the project folder:
    .venv/bin/python src/build_index.py
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")   # draw to a file, no window
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from companies import ALL_COMPANIES, TREATED
from quarterly import calendar_quarters

PROJECT = Path(__file__).resolve().parent.parent
DONORS = ["Garmin", "Colgate-Palmolive", "Clorox", "Hershey", "WD-40", "Fossil Group",
          "Deckers Outdoor", "Columbia Sportswear"]
SENSITIVITY = ["Electronic Arts"]
COMPANIES = list(TREATED) + DONORS + SENSITIVITY
WINDOW = pd.period_range("2013Q1", "2019Q4", freq="Q")
PRE = pd.period_range("2015Q1", "2017Q2", freq="Q")       # main pre-period (10 quarters)
TRANSITION = pd.Period("2017Q3")
POST = pd.period_range("2017Q4", "2019Q4", freq="Q")      # post-period (9 quarters)
FOURTEEN_WEEK_QUARTERS = {("Hasbro", "2017Q1"), ("Garmin", "2016Q4"),
                          ("Fossil Group", "2014Q1"), ("Electronic Arts", "2015Q2")}
FLAGGED = {("JAKKS Pacific", "2015Q1"): "inside the 2014-15 Frozen spike"}

# --- 1. Quarterly revenue ----------------------------------------------------
rows = []
for name in COMPANIES:
    q, _ = calendar_quarters(ALL_COMPANIES[name])
    q = q.loc[q.index.isin(WINDOW)]
    missing = sorted(set(WINDOW) - set(q.index))
    if missing:
        print(f"WARNING {name}: missing {[str(m) for m in missing]}")
    for cq, r in q.iterrows():
        rows.append({"company": name, "group": "treated" if name in TREATED else
                     ("donor" if name in DONORS else "sensitivity"),
                     "quarter": str(cq), "period_start": r["start"].date(), "period_end": r["end"].date(),
                     "days": r["days"], "tag": r["tag"], "q4_derived": r["q4_derived"],
                     "revenue_first_reported": r["value_first"], "revenue_latest": r["value_latest"]})
df = pd.DataFrame(rows)
df["quarter_p"] = pd.PeriodIndex(df["quarter"], freq="Q")

# The main revenue series: first reported, every 14-week quarter x 13/14.
# The list comes from src/scan_53_weeks.py (notes/fifty_three_weeks.md). EA's
# quarter cannot be seen in the dates (EA labels quarters by month end), so a
# written list is used, and the dates are checked against it below.
df["revenue_main"] = df["revenue_first_reported"].astype(float)
df["fourteen_weeks"] = [(c, q) in FOURTEEN_WEEK_QUARTERS for c, q in zip(df["company"], df["quarter"])]
df.loc[df["fourteen_weeks"], "revenue_main"] *= 13 / 14
unlisted = df[(df["days"] >= 95) & ~df["fourteen_weeks"]]
if len(unlisted):
    raise SystemExit(f"14-week quarters missing from the list: {unlisted[['company', 'quarter']].values.tolist()}")
print("Scaled by 13/14:", df.loc[df["fourteen_weeks"], ["company", "quarter"]].values.tolist())

# --- 2. The index -----------------------------------------------------------
# For each company and quarter of the year (Q1..Q4), divide by that quarter in 2016.
df["qtr_of_year"] = df["quarter_p"].dt.quarter
base = df[df["quarter_p"].dt.year == 2016].set_index(["company", "qtr_of_year"])["revenue_main"]
df["index"] = 100 * df["revenue_main"] / df.set_index(["company", "qtr_of_year"]).index.map(base)
df["log_index"] = np.log(df["index"])
df["flag"] = [FLAGGED.get((c, q), "") for c, q in zip(df["company"], df["quarter"])]
# The same index without the 13/14 adjustment and with restated revenue, as checks.
base_first = df[df["quarter_p"].dt.year == 2016].set_index(["company", "qtr_of_year"])["revenue_first_reported"]
df["index_unadjusted"] = 100 * df["revenue_first_reported"] / df.set_index(["company", "qtr_of_year"]).index.map(base_first)
base_latest = df[df["quarter_p"].dt.year == 2016].set_index(["company", "qtr_of_year"])["revenue_latest"]
df["index_latest"] = 100 * df["revenue_latest"] / df.set_index(["company", "qtr_of_year"]).index.map(base_latest)

out = df.drop(columns=["quarter_p", "qtr_of_year"])
out.to_csv(PROJECT / "data" / "processed" / "revenue_quarterly.csv", index=False)
print(f"Saved data/processed/revenue_quarterly.csv: {len(out)} rows, {out['company'].nunique()} companies")

# How different are first-reported and restated figures (pre and post window)?
gap = (df["revenue_latest"] / df["revenue_first_reported"] - 1).abs()
big = df.loc[(gap > 0.02) & df["quarter_p"].isin(PRE.union(POST)), ["company", "quarter"]]
print("Quarters 2015-2019 where restated differs from first reported by > 2 %:",
      big.groupby("company")["quarter"].apply(list).to_dict())

# --- 3. Pre-period trend table ----------------------------------------------
def trend_line(pre):
    """Slope (% per year) and wobble of log_index on time; time in years from 2015 Q1."""
    t = np.array([(p - PRE[0]).n for p in pre["quarter_p"]]) / 4
    slope, intercept = np.polyfit(t, pre["log_index"], 1)
    resid = pre["log_index"] - (intercept + slope * t)
    return round(100 * (np.exp(slope) - 1), 1), round(100 * resid.std(ddof=2), 1)


trend_rows = []
for name, g in df.groupby("company", sort=False):
    pre = g[g["quarter_p"].isin(PRE)].sort_values("quarter_p")
    trend_pct, wobble = trend_line(pre)
    # Without flagged quarters (JAKKS 2015 Q1), as a second trend.
    clean = pre[pre["flag"] == ""]
    trend_clean = trend_line(clean)[0] if len(clean) < len(pre) else trend_pct
    post = g[g["quarter_p"].isin(POST)]
    trend_rows.append({
        "company": name, "group": pre["group"].iloc[0],
        "pre_trend_pct_per_year": trend_pct,
        "pre_trend_without_flagged": trend_clean,
        "pre_wobble_sd_index_pts": wobble,   # spread around the line, about index points
        "index_2015Q1": round(pre["index"].iloc[0], 1),
        "index_2017Q2": round(pre["index"].iloc[-1], 1),
        "index_2017Q3": round(g.loc[g["quarter_p"] == TRANSITION, "index"].iloc[0], 1),
        "mean_index_post": round(post["index"].mean(), 1),
        "index_2019Q4": round(post["index"].iloc[-1], 1),
    })
trend = pd.DataFrame(trend_rows)
trend.to_csv(PROJECT / "results" / "pretrend_table.csv", index=False)
pd.set_option("display.width", 200)
print("\nPre-period trend table (2015 Q1 - 2017 Q2):")
print(trend.to_string(index=False))

# --- 4. The chart ------------------------------------------------------------
# Small multiples: one panel per treated company, the 8 donors behind it in gray.
SERIES_1 = "#2a78d6"     # treated company (categorical slot 1, reference palette)
DONOR_GRAY = "#b9b8b2"   # each donor, recessive
MEDIAN_INK = "#52514e"   # donor median (secondary text ink)
TEXT = "#0b0b0b"
plot_q = pd.period_range("2015Q1", "2019Q4", freq="Q")
x = np.arange(len(plot_q))
labels = [str(p) if p.quarter == 1 else "" for p in plot_q]
wide = df.pivot(index="quarter_p", columns="company", values="index").loc[plot_q]

fig, axes = plt.subplots(1, 3, figsize=(15, 4.8), sharey=True)
for ax, name in zip(axes, TREATED):
    for d in DONORS:
        ax.plot(x, wide[d], color=DONOR_GRAY, lw=1, zorder=1)
    ax.plot(x, wide[DONORS].median(axis=1), color=MEDIAN_INK, lw=1.5, ls="--", zorder=2)
    ax.plot(x, wide[name], color=SERIES_1, lw=2.2, zorder=3)
    t_pos = list(plot_q).index(TRANSITION)
    ax.axvspan(t_pos - 0.5, t_pos + 0.5, color="#e8e7e2", zorder=0)   # 2017 Q3 transition
    ax.axhline(100, color="#d7d6d0", lw=0.8, zorder=0)
    ax.set_yscale("log")
    ax.set_yticks([60, 70, 80, 90, 100, 110, 120, 130, 140, 150])
    ax.set_yticklabels(["60", "70", "80", "90", "100", "110", "120", "130", "140", "150"])
    ax.minorticks_off()
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=9, color=TEXT)
    ax.set_title(name, loc="left", fontsize=12, color=TEXT)
    for side in ["top", "right"]:
        ax.spines[side].set_visible(False)
    ax.tick_params(colors="#52514e", length=0)
    ax.grid(axis="y", color="#eeede8", lw=0.6)
axes[0].set_ylabel("Revenue index (same quarter of 2016 = 100, log scale)", fontsize=10)
axes[0].text(t_pos, 61, "2017 Q3\ntransition", ha="center", va="bottom", fontsize=8, color="#52514e")
handles = [plt.Line2D([], [], color=SERIES_1, lw=2.2), plt.Line2D([], [], color=MEDIAN_INK, lw=1.5, ls="--"),
           plt.Line2D([], [], color=DONOR_GRAY, lw=1)]
fig.legend(handles, ["Treated company", "Median of the 8 donors", "Each donor"],
           loc="upper right", ncol=3, frameon=False, fontsize=10)
fig.suptitle("Revenue index: Mattel, Hasbro and JAKKS against 8 comparison companies, 2015-2019",
             x=0.01, ha="left", fontsize=13, color=TEXT)
fig.tight_layout(rect=(0, 0, 1, 0.92))
fig.savefig(PROJECT / "results" / "index_treated_vs_donors.png", dpi=150)
print("Saved results/index_treated_vs_donors.png and results/pretrend_table.csv")
