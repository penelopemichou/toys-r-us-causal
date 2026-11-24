"""Which revenue numbers does a company's companyfacts file have for 2013-2019?

For each revenue tag it shows, per year, how many quarter-long values
(80-98 days) and whether a full-year value (350-380 days) exists.
A December-year-end company usually tags Q1, Q2 and Q3 directly in its 10-Qs;
Q4 is then full year minus the first three quarters.

Run from the project folder, for example:
    .venv/bin/python src/list_revenue_quarters.py "JAKKS Pacific"
"""

import json
import sys
from pathlib import Path

import pandas as pd

from companies import ALL_COMPANIES

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
REVENUE_TAGS = ["Revenues", "SalesRevenueNet", "SalesRevenueGoodsNet",
                "RevenueFromContractWithCustomerExcludingAssessedTax",
                "RevenueFromContractWithCustomerIncludingAssessedTax"]
YEARS = range(2013, 2020)

name = sys.argv[1]
facts = json.loads((RAW_DIR / f"CIK{ALL_COMPANIES[name]}.json").read_text())
print(f"{facts['entityName']}: taxonomies {list(facts['facts'])}")

# Put every revenue value into one table: tag, start, end, value, form, filed date.
rows = []
for tag in REVENUE_TAGS:
    info = facts["facts"]["us-gaap"].get(tag)
    if info is None:
        continue
    for v in info["units"].get("USD", []):
        if "start" in v:
            rows.append({"tag": tag, "start": v["start"], "end": v["end"], "value": v["val"],
                         "form": v["form"], "filed": v["filed"]})
df = pd.DataFrame(rows)
df["start"], df["end"] = pd.to_datetime(df["start"]), pd.to_datetime(df["end"])
df["days"] = (df["end"] - df["start"]).dt.days
df = df.drop_duplicates(["tag", "start", "end", "value"])

# Summary per tag and year: distinct quarter periods and full-year periods ending in that year.
print("\nPer tag: distinct quarter-long periods / full-year periods, by year the period ends")
for tag, g in df.groupby("tag"):
    cells = []
    for y in YEARS:
        gy = g[g["end"].dt.year == y]
        nq = gy[gy["days"].between(80, 98)]["end"].nunique()
        nfy = gy[gy["days"].between(350, 380)]["end"].nunique()
        cells.append(f"{y}: {nq}q/{nfy}fy")
    print(f"  {tag}\n    " + "  ".join(cells))

# The full-year values, and the quarter month-ends seen, to spot the fiscal calendar.
fy = df[df["days"].between(350, 380) & df["end"].dt.year.isin(YEARS)]
print("\nFull-year values (USD millions), first value seen per period:")
print(fy.sort_values("filed").groupby("end").first()[["tag", "value", "form", "filed"]]
        .assign(value=lambda d: (d["value"] / 1e6).round(1)).to_string())
q = df[df["days"].between(80, 98) & df["end"].dt.year.isin(YEARS)]
print("\nMonths in which quarters end:", sorted(q["end"].dt.month.unique()))
