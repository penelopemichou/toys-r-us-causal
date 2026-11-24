"""Session 1: what SEC data does the sister project already have?

This script only READS files in ~/Documents/ai-fpa-forecast. It changes
nothing there and downloads nothing. It prints the answers to four questions:

  1. Are Mattel, Hasbro and JAKKS Pacific in the 20-company set?
  2. Is quarterly revenue 2013 Q1 - 2019 Q4 complete for each company?
  3. Is there segment revenue (North America / US & Canada) in the SEC files?
  4. Which companies are consumer-products companies?

Run from this project folder:
    .venv/bin/python src/inventory_sister_data.py
"""

import json
from pathlib import Path

import pandas as pd

# --- 1. Where the sister project's files are --------------------------------
SISTER = Path.home() / "Documents" / "ai-fpa-forecast"
QUARTERLY_CSV = SISTER / "data" / "processed" / "revenue_quarterly.csv"
RAW_DIR = SISTER / "data" / "raw"

# The SEC's ID numbers (CIKs) of our three treated companies.
TREATED = {"Mattel": "0000063276", "Hasbro": "0000046080", "JAKKS Pacific": "0001009829"}

# --- 2. Question 1: which companies are there? ------------------------------
# Each raw file is called CIK##########.json, so the file names tell us which
# companies were downloaded.
downloaded = {p.stem.replace("CIK", "") for p in RAW_DIR.glob("CIK*.json")}
table = pd.read_csv(QUARTERLY_CSV, parse_dates=["period_end"])

print("QUESTION 1: are the treated companies in the sister data?")
for name, cik in TREATED.items():
    in_raw = cik in downloaded
    in_table = name in set(table["company"])
    print(f"  {name:14s} raw SEC file: {'yes' if in_raw else 'NO'}   quarterly table: {'yes' if in_table else 'NO'}")

# --- 3. Question 2: are 2013 Q1 - 2019 Q4 complete? -------------------------
# Our design uses CALENDAR quarters. A company's fiscal quarter is placed in
# the calendar quarter whose end is NEAREST to the quarter's own end date.
# Why "nearest": Hasbro and Cummins count their year in weeks, so their first
# quarter can end on 2 April. Moving the date back 15 days before reading off
# the calendar quarter puts 2 April in Q1 (and 30 Sept stays in Q3).
table["cal_quarter"] = (table["period_end"] - pd.Timedelta(days=15)).dt.to_period("Q")
window = pd.period_range("2013Q1", "2019Q4", freq="Q")   # 28 quarters

print("\nQUESTION 2: quarters 2013 Q1 - 2019 Q4 (28 needed)")
print(f"  {'company':18s} {'have':>4s} {'missing':>8s}  fiscal year ends   first/last quarter in table")
rows = []
for company, g in table.groupby("company"):
    in_window = g[g["cal_quarter"].isin(window)]
    missing = sorted(set(window) - set(in_window["cal_quarter"]))
    # Fiscal year end month = the month in which fiscal Q4 quarters end (most common).
    fy_end = g.loc[g["fiscal_quarter"] == 4, "period_end"].dt.month_name().mode().iloc[0]
    dupes = in_window["cal_quarter"].duplicated().sum()
    rows.append((company, len(in_window), missing, fy_end, dupes))
    note = f"  {len(missing)} missing: {[str(m) for m in missing]}" if missing else ""
    if dupes:
        note += f"  ({dupes} calendar quarters appear twice)"
    print(f"  {company:18s} {len(in_window):4d} {len(missing):8d}  {fy_end:16s}  "
          f"{g['cal_quarter'].min()} - {g['cal_quarter'].max()}{note}")

# How much first-reported and latest revenue differ for the treated two in the window.
print("\n  Restatements in the window (first reported vs latest, largest gap):")
for company in ["Mattel", "Hasbro"]:
    g = table[(table["company"] == company) & table["cal_quarter"].isin(window)]
    gap = (g["revenue_latest"] / g["revenue_first_reported"] - 1).abs()
    worst = g.loc[gap.idxmax()]
    print(f"  {company}: largest gap {gap.max():.2%} in {worst['cal_quarter']}; "
          f"tags used: {sorted(g['source_tag'].unique())}")

# --- 4. Question 3: segment revenue? -----------------------------------------
# A companyfacts file lists every tag ("concept") the company used, grouped by
# taxonomy: us-gaap = the standard list, dei = cover-page facts, and a company's
# own custom tags would have their own prefix. We search the tag names for
# anything that looks regional or like a segment.
WORDS = ["northamerica", "unitedstates", "domestic", "canada", "segment",
         "geograph", "region", "international", "externalcustomer"]

print("\nQUESTION 3: any segment / regional revenue tags in the raw SEC files?")
for name in ["Mattel", "Hasbro"]:
    facts = json.loads((RAW_DIR / f"CIK{TREATED[name]}.json").read_text())["facts"]
    print(f"  {name}: taxonomies in file = {list(facts)}")
    for taxonomy, tags in facts.items():
        for tag, info in tags.items():
            if any(w in tag.lower() for w in WORDS):
                # Count quarterly (80-98 day) values inside 2013-2019.
                n_q = 0
                for unit_values in info["units"].values():
                    for v in unit_values:
                        if "start" in v and v["end"][:4] in {str(y) for y in range(2013, 2020)}:
                            days = (pd.Timestamp(v["end"]) - pd.Timestamp(v["start"])).days
                            n_q += 80 <= days <= 98
                print(f"    {taxonomy}:{tag}  (quarter-length values ending 2013-2019: {n_q})")

# --- 5. Question 4: consumer-products companies? ------------------------------
# The sister project's own types and one-line reasons, read from its companies.py.
# We read the file as text and run it, so we do not have to import it.
namespace = {}
exec((SISTER / "src" / "companies.py").read_text(), namespace)
print("\nQUESTION 4: the 20 companies, their type and one-line description")
for company, (ctype, _, reason) in namespace["COMPANIES"].items():
    print(f"  {company:18s} {ctype:20s} {reason}")
