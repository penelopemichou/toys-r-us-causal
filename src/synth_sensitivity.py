"""Session 7: two sensitivity runs. The main results are NOT changed.

0. Check: rebuild the main twins with src/synth_core.py and confirm they match
   results/synth_fit.csv (same method, same numbers).
1. EA as a 9th donor: the three twins (and JAKKS without 2015 Q1) refitted with
   Electronic Arts added. Same fit rule first. A twin that passes only because
   EA was added is labelled "passes only with a toy substitute (EA), so not
   credible": video games may have gained from Toys "R" Us closing.
2. 2013 start, Mattel and Hasbro only: pre-period 2013 Q1 - 2017 Q2, donors
   clean in 2013-2014 only. Fit rule on the free quarters (2013-2015 and
   2017 Q1-Q2). Placebo ranks among the remaining donors.

"Clean in 2013-2014" is decided by rules written before looking at the fits:
no quarter of 2014 Q1-2015 Q4 more than 20 % above or below the same quarter a
year earlier, and no acquisition, joint venture or fiscal-year change in
2013-2014 found in notes/jump_check.md (Deckers, Columbia).

Writes results/synth_sensitivity_ea.csv, results/synth_sensitivity_2013.csv,
results/synth_sensitivity_weights.csv, results/synth_sensitivity_2013.png.

Run from the project folder:
    .venv/bin/python src/synth_sensitivity.py
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from synth_core import PROJECT, POST, load_log_index, run

RESULTS = PROJECT / "results"
DONORS = ["Garmin", "Colgate-Palmolive", "Clorox", "Hershey", "WD-40", "Fossil Group",
          "Deckers Outdoor", "Columbia Sportswear"]
EA = "Electronic Arts"
KNOWN_2014_BREAKS = {"Deckers Outdoor": "UGG distributor bought July 2014; year-end change 2014",
                     "Columbia Sportswear": "prAna bought and China joint venture started, 2014"}
rng = np.random.default_rng(0)
pd.set_option("display.width", 220)

LOG = load_log_index("2013Q1", "2019Q4")
PRE = pd.period_range("2015Q1", "2017Q2", freq="Q")
FREE = [q for q in PRE if q.year != 2016]
NO15 = pd.Period("2015Q1")
SPECS = {
    "Mattel": ("Mattel", list(PRE), FREE),
    "Hasbro": ("Hasbro", list(PRE), FREE),
    "JAKKS Pacific": ("JAKKS Pacific", list(PRE), FREE),
    "JAKKS Pacific (without 2015 Q1)": ("JAKKS Pacific", [q for q in PRE if q != NO15], [q for q in FREE if q != NO15]),
}
LOG_MAIN = LOG[pd.period_range("2015Q1", "2019Q4", freq="Q")]

# --- 0. Same numbers as the main results? ------------------------------------------
main_fit = pd.read_csv(RESULTS / "synth_fit.csv").set_index("run")
main = {}
for name, (c, fq, rq) in SPECS.items():
    main[name] = run(LOG_MAIN, c, DONORS, fq, rq, rng)
    assert abs(main[name]["avg_abs_gap"] - main_fit.loc[name, "avg_abs_gap_pts"]) < 0.01
    assert abs(main[name]["max_abs_gap"] - main_fit.loc[name, "max_abs_gap_pts"]) < 0.01
print("Check passed: synth_core.py reproduces the main results (results/synth_fit.csv).\n")

# --- 1. EA as a 9th donor ---------------------------------------------------------------
rows, weight_cols = [], {}
for name, (c, fq, rq) in SPECS.items():
    r = run(LOG_MAIN, c, DONORS + [EA], fq, rq, rng)
    if r["passes"] and not main[name]["passes"]:
        verdict = "passes only with a toy substitute (EA), so not credible"
    else:
        verdict = "credible twin" if r["passes"] else "no credible twin"
    rows.append({"run": name, "ea_weight": round(r["weights"][EA], 3),
                 "avg_abs_gap_8_donors": round(main[name]["avg_abs_gap"], 2),
                 "avg_abs_gap_with_ea": round(r["avg_abs_gap"], 2),
                 "max_abs_gap_8_donors": round(main[name]["max_abs_gap"], 2),
                 "max_abs_gap_with_ea": round(r["max_abs_gap"], 2), "worst_quarter": r["worst_quarter"],
                 "verdict": verdict,
                 "post_mean_pct_for_information": round(100 * (np.exp(r["gap_log"][POST].mean()) - 1), 1)})
    weight_cols[f"{name} + EA"] = r["weights"]
ea = pd.DataFrame(rows)
ea.to_csv(RESULTS / "synth_sensitivity_ea.csv", index=False)
print("1. EA AS A 9TH DONOR (fit rule on the same free quarters as the main run)")
print(ea.drop(columns=["post_mean_pct_for_information"]).to_string(index=False))

# --- 2. 2013 start ----------------------------------------------------------------------
PRE13 = pd.period_range("2013Q1", "2017Q2", freq="Q")
FREE13 = [q for q in PRE13 if q.year != 2016]          # 2013-2015 and 2017 Q1-Q2 (14 quarters)
# Change against the same quarter a year earlier, 2014 Q1 - 2015 Q4 (our table
# starts in 2013, so 2013 itself can only be compared forward, with 2014).
CHECK = pd.period_range("2014Q1", "2015Q4", freq="Q")
yoy = (LOG - LOG.shift(4, axis=1)).loc[:, CHECK]
print("\n2. 2013 START - which donors are clean in 2013-2014?")
clean = []
for d in DONORS:
    big = yoy.loc[d][np.abs(np.exp(yoy.loc[d]) - 1) > 0.20]
    reason = KNOWN_2014_BREAKS.get(d, "")
    jumps = ", ".join(f"{q} {np.exp(v) - 1:+.0%}" for q, v in big.items())
    ok = not reason and big.empty
    if ok:
        clean.append(d)
    print(f"   {d:20s} {'clean' if ok else 'OUT  '}  jumps over 20 %: {jumps or 'none'}"
          f"{'; ' + reason if reason else ''}")
print(f"   -> {len(clean)} donors left; smallest possible placebo rank 1 of {len(clean) + 1} "
      f"(about {1 / (len(clean) + 1):.2f}) instead of 1 of 9 (about 0.11)")

rows13 = []
res13 = {}
for company in ["Mattel", "Hasbro"]:
    r = run(LOG, company, clean, list(PRE13), FREE13, rng)
    res13[company] = r
    late = r["gap_pts"][[pd.Period("2017Q1"), pd.Period("2017Q2")]]
    # Placebo ranks among the clean donors (each from the other clean donors).
    ratios = []
    for d in clean:
        rp = run(LOG, d, [o for o in clean if o != d], list(PRE13), FREE13, rng)
        ratios.append(rp["post_rmspe"] / rp["pre_rmspe"])
    ratio = r["post_rmspe"] / r["pre_rmspe"]
    rank = 1 + sum(x > ratio for x in ratios)
    rows13.append({"run": f"{company} (2013 start)", "donors": len(clean),
                   "avg_abs_gap_14q": round(r["avg_abs_gap"], 2), "max_abs_gap_14q": round(r["max_abs_gap"], 2),
                   "worst_quarter": r["worst_quarter"],
                   "gap_2017Q1": round(late.iloc[0], 2), "gap_2017Q2": round(late.iloc[1], 2),
                   "verdict": "credible twin" if r["passes"] else "no credible twin",
                   "placebo_ratio": round(ratio, 2), "rank": f"{rank}/{len(clean) + 1}",
                   "post_mean_pct_for_information": round(100 * (np.exp(r["gap_log"][POST].mean()) - 1), 1)})
    weight_cols[f"{company} (2013 start)"] = r["weights"]
s13 = pd.DataFrame(rows13)
s13.to_csv(RESULTS / "synth_sensitivity_2013.csv", index=False)
print("\n   Fit rule on 14 free quarters (2013-2015, 2017 Q1-Q2):")
print(s13.drop(columns=["post_mean_pct_for_information"]).to_string(index=False))

weights = pd.DataFrame(weight_cols).reindex(DONORS + [EA]).fillna(0).round(3)
weights.to_csv(RESULTS / "synth_sensitivity_weights.csv", index_label="donor")
print("\nWEIGHTS (0 = not used or not available)")
print(weights.to_string())

print("\nPost-period gaps, FOR INFORMATION ONLY (none of these twins is credible):")
for _, row in pd.concat([ea, s13]).iterrows():
    print(f"   {row['run']:34s} {row['post_mean_pct_for_information']:+.1f} %  [{row['verdict']}]")

# Chart: the 2013-start twins (for information).
TEXT, MUTED = "#0b0b0b", "#52514e"
q = list(LOG.columns)
x = np.arange(len(q))
fig, axes = plt.subplots(1, 2, figsize=(13, 4.6), sharey=True)
for ax, company in zip(axes, ["Mattel", "Hasbro"]):
    r = res13[company]
    ax.plot(x, np.exp(LOG.loc[company].values), color="#2a78d6", lw=2.2, label=company)
    ax.plot(x, np.exp(r["synth_log"].values), color="#eb6834", lw=2, ls="--", label="Twin (clean donors)")
    tr = q.index(pd.Period("2017Q3"))
    ax.axvspan(tr - 0.5, tr + 0.5, color="#f1f0eb", zorder=0)
    ax.axhline(100, color="#d7d6d0", lw=0.8, zorder=0)
    ax.set_xticks(x)
    ax.set_xticklabels([str(p) if p.quarter == 1 else "" for p in q], fontsize=8)
    ax.set_title(f"{company}: avg {r['avg_abs_gap']:.1f}, worst {r['max_abs_gap']:.1f} pts "
                 f"({'passes' if r['passes'] else 'fails'})", loc="left", fontsize=10, color=TEXT)
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    ax.tick_params(colors=MUTED, length=0)
    ax.grid(axis="y", color="#eeede8", lw=0.6)
    ax.legend(loc="lower left", frameon=False, fontsize=8)
axes[0].set_ylabel("Revenue index (same quarter of 2016 = 100)", fontsize=9)
fig.suptitle("Sensitivity: 2013 start, clean donors only", x=0.01, ha="left", fontsize=12, color=TEXT)
fig.text(0.01, 0.9, "For information, not an effect, unless the twin passes the fit rule.",
         fontsize=9, color="#b42318")
fig.tight_layout(rect=(0, 0, 1, 0.88))
fig.savefig(RESULTS / "synth_sensitivity_2013.png", dpi=150)
print("\nSaved results/synth_sensitivity_*.csv and results/synth_sensitivity_2013.png")
