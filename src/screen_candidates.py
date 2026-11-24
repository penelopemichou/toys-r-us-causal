"""Screen the comparison candidates (rules 2 and 3 in CLAUDE.md).

Rule 2, data part: does the SEC companyfacts file give all 28 calendar
quarters 2013 Q1 - 2019 Q4? And are there big jumps in revenue (a sign of
an acquisition, merger or spin-off)?

Rule 3: do the 2016 and 2017 10-Ks mention Toys "R" Us or Babies "R" Us,
in any spelling? Every mention is printed with the text around it, so a
person can read whether it names them as a customer.

Only reads files in data/raw/ (downloaded earlier). Writes:
    results/screening_data.csv        one row per company (rule 2)
    results/screening_tru_mentions.txt every mention with its context (rule 3)

Run from the project folder:
    .venv/bin/python src/screen_candidates.py
"""

import html
import json
import re
from pathlib import Path

import pandas as pd

from companies import CANDIDATES

PROJECT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT / "data" / "raw"
RESULTS = PROJECT / "results"

# Revenue tags, most preferred first. A quarter takes its value from the
# first tag in this list that has it.
REVENUE_TAGS = ["RevenueFromContractWithCustomerExcludingAssessedTax", "SalesRevenueNet",
                "Revenues", "SalesRevenueGoodsNet",
                "RevenueFromContractWithCustomerIncludingAssessedTax"]
WINDOW = pd.period_range("2013Q1", "2019Q4", freq="Q")

# --- The search pattern for rule 3 ---------------------------------------
# "toys" or "babies", then up to 8 characters that are not letters or digits
# (spaces, quotes, apostrophes, dashes, "&" ...), then "r", then again up to
# 8 such characters, then "us". \W means "not a letter, digit or underscore".
TRU_PATTERN = re.compile(r"\b(toys|babies)\W{0,8}r\W{0,8}us\b", re.IGNORECASE)

# Test the pattern on the spellings we know of, before trusting it.
MUST_MATCH = ['Toys "R" Us', "Toys R Us", "Toys 'R' Us", "Toys“R”Us", "Toys ‘R’ Us",
              "Toys-R-Us", "ToysRUs", "Toys R’ Us", "Babies \"R\" Us", "Babies R Us",
              "TOYS “R” US", "Toys & R Us", "Toys \"R\" Us-Delaware", "toys&quot;r&quot;us"]
MUST_NOT_MATCH = ["toys are used", "toys, our users", "babies require us"]


def clean_text(raw_bytes):
    """Turn an HTML or text filing into plain text."""
    text = raw_bytes.decode("utf-8", errors="replace")
    text = re.sub(r"<[^>]+>", " ", text)          # drop HTML tags
    text = html.unescape(html.unescape(text))      # &quot; -> ", &#8220; -> “ (twice for &amp;quot;)
    return re.sub(r"\s+", " ", text)               # squeeze spaces and line breaks


def test_pattern():
    for s in MUST_MATCH:
        assert TRU_PATTERN.search(clean_text(s.encode())), f"pattern misses: {s}"
    for s in MUST_NOT_MATCH:
        assert not TRU_PATTERN.search(s), f"pattern wrongly matches: {s}"
    print(f"Pattern test passed: {len(MUST_MATCH)} spellings found, {len(MUST_NOT_MATCH)} look-alikes ignored.\n")


# --- Rule 2: quarters and jumps ---------------------------------------------
def revenue_quarters(facts):
    """Return (quarter table, full-year table) from a companyfacts file."""
    rows = []
    for rank, tag in enumerate(REVENUE_TAGS):
        for v in facts["facts"]["us-gaap"].get(tag, {}).get("units", {}).get("USD", []):
            if "start" in v:
                rows.append({"rank": rank, "tag": tag, "start": v["start"], "end": v["end"],
                             "value": v["val"], "filed": v["filed"]})
    df = pd.DataFrame(rows)
    df["start"], df["end"] = pd.to_datetime(df["start"]), pd.to_datetime(df["end"])
    df["days"] = (df["end"] - df["start"]).dt.days
    # Latest filed value per tag and period, then the most preferred tag per period.
    df = df.sort_values("filed").groupby(["rank", "start", "end"]).last().reset_index()
    df = df.sort_values("rank").groupby(["start", "end"]).first().reset_index()
    # Calendar quarter whose end is nearest the period end (see inventory_sister_data.py).
    df["cal_q"] = (df["end"] - pd.Timedelta(days=15)).dt.to_period("Q")
    quarters = df[df["days"].between(80, 98)].sort_values("filed").groupby("cal_q").last()
    years = df[df["days"].between(350, 380)].sort_values("filed").groupby("cal_q").last()
    return quarters, years


def screen_data(name, cik):
    facts = json.loads((RAW_DIR / f"CIK{cik}.json").read_text())
    quarters, years = revenue_quarters(facts)
    value = quarters["value"].to_dict()
    derived = []
    # A missing quarter that ends a fiscal year = full year minus the three quarters before it.
    for q in WINDOW:
        if q not in value and q in years.index:
            before = [q - 1, q - 2, q - 3]
            if all(b in value for b in before):
                value[q] = years.loc[q, "value"] - sum(value[b] for b in before)
                derived.append(str(q))
    # Check: do four quarters add up to the full year (within 1 %)?
    bad_sums = []
    for q in years.index:
        four = [q, q - 1, q - 2, q - 3]
        if q in WINDOW and all(f in value for f in four) and str(q) not in derived:
            total = sum(value[f] for f in four)
            if abs(total / years.loc[q, "value"] - 1) > 0.01:
                bad_sums.append(str(q))
    missing = [str(q) for q in WINDOW if q not in value]
    # Same quarter last year growth, to spot jumps from acquisitions or spin-offs.
    s = pd.Series({q: value[q] for q in WINDOW if q in value}).sort_index()
    growth = (s / s.shift(4) - 1).dropna()
    big = growth[growth.abs() > 0.20]
    fy_months = sorted(years.loc[years.index.isin(WINDOW), "end"].dt.month.unique().tolist())
    return {
        "company": name, "sec_name": facts["entityName"],
        "fy_end_months": fy_months,
        "quarters_found": len(s), "missing": " ".join(missing),
        "q4_derived": len(derived), "sums_off_by_over_1pct": " ".join(bad_sums),
        "max_abs_yoy_growth": round(growth.abs().max(), 3) if len(growth) else None,
        "quarters_over_20pct_yoy": " ".join(f"{q}:{g:+.0%}" for q, g in big.items()),
        "tags_used": " ".join(sorted(quarters.loc[quarters.index.isin(WINDOW), "tag"].unique())),
    }


# --- Rule 3: Toys "R" Us mentions -------------------------------------------
def screen_10ks(name, cik, out):
    files = sorted((RAW_DIR / "10k" / cik).glob("*"))
    n_mentions = 0
    for f in files:
        text = clean_text(f.read_bytes())
        hits = list(TRU_PATTERN.finditer(text))
        # "TRU" on its own, in capitals, as an extra check (could be an abbreviation).
        tru_abbrev = re.findall(r"\bTRU\b", text)
        n_mentions += len(hits)
        out.write(f"\n=== {name} | {f.name} | {len(text):,} characters | "
                  f"{len(hits)} mentions | 'TRU' alone: {len(tru_abbrev)}\n")
        for h in hits:
            out.write(f"  ...{text[max(0, h.start() - 300):h.end() + 300]}...\n\n")
    return {"tenk_files": len(files), "tru_mentions": n_mentions}


def main():
    test_pattern()
    RESULTS.mkdir(exist_ok=True)
    rows = []
    with open(RESULTS / "screening_tru_mentions.txt", "w") as out:
        for name, cik in CANDIDATES.items():
            row = screen_data(name, cik)
            row.update(screen_10ks(name, cik, out))
            rows.append(row)
    table = pd.DataFrame(rows)
    table.to_csv(RESULTS / "screening_data.csv", index=False)
    pd.set_option("display.width", 250, "display.max_colwidth", 70)
    print(table.drop(columns=["sec_name", "tags_used"]).to_string(index=False))
    print("\nSEC names:", dict(zip(table["company"], table["sec_name"])))
    print("\nSaved: results/screening_data.csv and results/screening_tru_mentions.txt")


if __name__ == "__main__":
    main()
