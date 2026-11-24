"""Check the 2014 jumps (Columbia, Deckers, Logitech, JAKKS) and Logitech from 2015 Q1.

For each company it prints, per calendar quarter 2013 Q1 - 2016 Q4:
the tag, the period dates, the first-reported and latest revenue, and growth
against the same quarter a year earlier. Then yearly totals (does the jump
last?), and evidence about the cause from files we already have:
  - the 10-Ks in data/raw/10k/ (searched for key words), and
  - acquisition facts in the companyfacts file.
Nothing is downloaded.

Run from the project folder:
    .venv/bin/python src/check_jumps.py
"""

import re
from pathlib import Path

import pandas as pd

from companies import ALL_COMPANIES
from quarterly import calendar_quarters, load_facts
from screen_candidates import clean_text

TENK_DIR = Path(__file__).resolve().parent.parent / "data" / "raw" / "10k"
KEYWORDS = {
    "Columbia Sportswear": ["prAna", "joint venture"],
    "Deckers Outdoor": ["transition period", "change in fiscal year", "changed its fiscal year"],
    "Logitech": ["Lifesize", "discontinued operation"],
    "JAKKS Pacific": [],   # no JAKKS 10-K downloaded
}
pd.set_option("display.width", 220)

for name, words in KEYWORDS.items():
    cik = ALL_COMPANIES[name]
    q, _ = calendar_quarters(cik)
    q["yoy_latest"] = q["value_latest"] / q["value_latest"].shift(4) - 1
    q["yoy_first"] = q["value_first"] / q["value_first"].shift(4) - 1
    q["restated"] = (q["value_latest"] / q["value_first"] - 1).round(3)
    show = q.loc[pd.Period("2013Q1"):pd.Period("2016Q4")].copy()
    for c in ["value_first", "value_latest"]:
        show[c] = (show[c] / 1e6).round(1)
    for c in ["yoy_latest", "yoy_first"]:
        show[c] = show[c].map(lambda x: f"{x:+.0%}" if pd.notna(x) else "")
    print(f"\n==================== {name} ($ millions)")
    print(show[["tag", "start", "end", "days", "value_first", "value_latest", "restated",
                "yoy_latest", "yoy_first", "q4_derived"]].to_string())

    # Does the jump last? Sum the four calendar quarters of each year.
    yearly = q.groupby(q.index.year)["value_latest"].agg(["sum", "count"])
    yearly = yearly[yearly["count"] == 4]
    print("  Calendar-year totals ($ m), latest values:",
          {y: round(s / 1e6) for y, s in yearly["sum"].loc[2012:2019].items()})

    # Evidence 1: acquisition facts in the companyfacts file, 2013-2015.
    facts = load_facts(cik)["facts"]["us-gaap"]
    acq = []
    for tag, info in facts.items():
        if tag.startswith(("BusinessAcquisition", "PaymentsToAcquireBusinesses", "BusinessCombination")):
            for unit, vals in info["units"].items():
                for v in vals:
                    if v["end"][:4] in ("2013", "2014", "2015") and unit == "USD" and v["val"] > 0:
                        acq.append((tag, v.get("start", ""), v["end"], round(v["val"] / 1e6, 1)))
    acq = sorted(set(acq), key=lambda a: (a[2], a[0]))
    print(f"  Acquisition facts 2013-2015 ({len(acq)}):")
    for a in acq[:12]:
        print("    ", a)

    # Evidence 2: key words in the 10-Ks we already have.
    for f in sorted((TENK_DIR / cik).glob("*10-K*")) if (TENK_DIR / cik).exists() else []:
        text = clean_text(f.read_bytes())
        for w in words:
            hits = [m.start() for m in re.finditer(re.escape(w), text, flags=re.I)]
            print(f"  {f.name[:10]} '{w}': {len(hits)} hits")
            for h in hits[:2]:
                print("      ~", text[max(0, h - 200):h + 250])

# Logitech from 2015 Q1: one tag? quarters add up? jumps over 20 %?
q, _ = calendar_quarters(ALL_COMPANIES["Logitech"])
w = q.loc[pd.Period("2015Q1"):pd.Period("2019Q4")]
yoy = (q["value_latest"] / q["value_latest"].shift(4) - 1).loc[pd.Period("2015Q1"):pd.Period("2019Q4")]
print("\n==================== Logitech from 2015 Q1")
print("  quarters:", len(w), "| tags:", sorted(w["tag"].unique()), "| Q4 derived:", int(w["q4_derived"].sum()))
print("  largest restatement (latest vs first):", f"{(w['value_latest'] / w['value_first'] - 1).abs().max():.1%}")
print("  four quarters vs full year (gap):", w["fy_sum_gap"].dropna().to_dict())
print("  growth vs a year earlier:", {str(k): f"{v:+.0%}" for k, v in yoy.items()})
