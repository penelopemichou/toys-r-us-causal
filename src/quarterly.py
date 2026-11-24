"""Turn one company's SEC companyfacts file into a table of calendar-quarter revenue.

Used by check_jumps.py and build_index.py. The rules:

- Revenue tags in REVENUE_TAGS, most preferred first. For each period the most
  preferred tag that has a value is used (some tags are left out per company in
  EXCLUDE_TAGS, e.g. JAKKS's "Revenues" 2013-2015, which is only part of sales).
- A quarter is a period of 80-98 days; a full year 350-380 days.
- Each period gets two values: the FIRST reported (earliest filing) and the
  LATEST (newest filing, after any restatement).
- Calendar quarter = the one whose end is nearest the period end
  (end date minus 15 days, then read off the quarter).
- A missing quarter that ends a fiscal year = full year minus the three
  quarters before it ("q4_derived").
"""

import json
from pathlib import Path

import pandas as pd

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
REVENUE_TAGS = ["RevenueFromContractWithCustomerExcludingAssessedTax", "SalesRevenueNet",
                "Revenues", "SalesRevenueGoodsNet",
                "RevenueFromContractWithCustomerIncludingAssessedTax"]
EXCLUDE_TAGS = {"0001009829": ["Revenues"]}   # JAKKS: "Revenues" is about half of net sales


def load_facts(cik):
    return json.loads((RAW_DIR / f"CIK{cik}.json").read_text())


def revenue_periods(facts, cik):
    """Every revenue value with a start and end date, one row per tag, period and filing."""
    rows = []
    for rank, tag in enumerate(REVENUE_TAGS):
        if tag in EXCLUDE_TAGS.get(cik, []):
            continue
        for v in facts["facts"]["us-gaap"].get(tag, {}).get("units", {}).get("USD", []):
            if "start" in v:
                rows.append({"rank": rank, "tag": tag, "start": v["start"], "end": v["end"],
                             "value": v["val"], "filed": v["filed"], "form": v["form"]})
    df = pd.DataFrame(rows)
    df["start"], df["end"] = pd.to_datetime(df["start"]), pd.to_datetime(df["end"])
    df["filed"] = pd.to_datetime(df["filed"])
    df["days"] = (df["end"] - df["start"]).dt.days
    df["cal_q"] = (df["end"] - pd.Timedelta(days=15)).dt.to_period("Q")
    return df


def summarise(df):
    """One row per period: preferred tag, first and latest value, first filing date."""
    best_rank = df.groupby(["start", "end"])["rank"].transform("min")
    df = df[df["rank"] == best_rank].sort_values("filed")
    out = df.groupby(["start", "end"]).agg(
        tag=("tag", "first"), days=("days", "first"), cal_q=("cal_q", "first"),
        value_first=("value", "first"), value_latest=("value", "last"),
        first_filed=("filed", "first")).reset_index()
    return out


def calendar_quarters(cik):
    """Table indexed by calendar quarter: tag, dates, days, first and latest revenue."""
    periods = summarise(revenue_periods(load_facts(cik), cik))
    q = periods[periods["days"].between(80, 98)].sort_values("first_filed")
    # If two periods map to the same calendar quarter (rare dating errors, e.g. a
    # JAKKS 2016 Q3 fact dated 1 June - 3 Sept in a later 10-K), keep the one filed first.
    q = q.groupby("cal_q").first()
    q["q4_derived"] = False
    years = periods[periods["days"].between(350, 380)].sort_values("first_filed").groupby("cal_q").last()
    for cq, fy in years.iterrows():
        before = [cq - 1, cq - 2, cq - 3]
        if cq not in q.index and all(b in q.index for b in before):
            q.loc[cq] = {"tag": fy["tag"], "start": q.loc[cq - 1, "end"] + pd.Timedelta(days=1),
                         "end": fy["end"], "days": (fy["end"] - q.loc[cq - 1, "end"]).days,
                         "value_first": fy["value_first"] - sum(q.loc[b, "value_first"] for b in before),
                         "value_latest": fy["value_latest"] - sum(q.loc[b, "value_latest"] for b in before),
                         "first_filed": fy["first_filed"], "q4_derived": True}
    q = q.sort_index()
    # Check column: do the four quarters of each fiscal year add up to the full year?
    # (Only where Q4 was reported directly; a derived Q4 adds up by construction.)
    q["fy_sum_gap"] = None
    for cq, fy in years.iterrows():
        four = [cq, cq - 1, cq - 2, cq - 3]
        if all(f in q.index for f in four) and not q.loc[cq, "q4_derived"]:
            q.loc[cq, "fy_sum_gap"] = round(sum(q.loc[f, "value_first"] for f in four)
                                            / fy["value_first"] - 1, 4)
    return q, years
