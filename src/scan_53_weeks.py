"""Find 14-week quarters (years of 53 weeks) for every company, 2013-2019.

Two sources, nothing downloaded:
  1. The SEC data: every quarter's start and end date. A 13-week quarter is
     90 days from start to end date, a 14-week quarter 97. Calendar quarters
     are 89-92. We list every quarter of 95 days or more, and every full year
     of 368 days or more (a 53-week year is 370).
  2. The 10-Ks we already have (fiscal 2016-2017 for the donors and EA):
     searched for "53 weeks", "53-week" and "fifty-three".

Run from the project folder:
    .venv/bin/python src/scan_53_weeks.py
"""

import re
from pathlib import Path

import pandas as pd

from companies import ALL_COMPANIES
from quarterly import calendar_quarters
from screen_candidates import clean_text

COMPANIES = ["Mattel", "Hasbro", "JAKKS Pacific", "Garmin", "Colgate-Palmolive", "Clorox", "Hershey",
             "WD-40", "Fossil Group", "Deckers Outdoor", "Columbia Sportswear", "Electronic Arts"]
TENK_DIR = Path(__file__).resolve().parent.parent / "data" / "raw" / "10k"
WINDOW = pd.period_range("2013Q1", "2019Q4", freq="Q")
PATTERN = re.compile(r"53[- ]weeks?|fifty[- ]three[- ]weeks?", re.I)

for name in COMPANIES:
    cik = ALL_COMPANIES[name]
    q, years = calendar_quarters(cik)
    q = q.loc[q.index.isin(WINDOW)]
    long_q = q[q["days"] >= 95]
    years = years[(years["end"].dt.year >= 2013) & (years["end"].dt.year <= 2019)]
    long_y = years[(years["end"] - years["start"]).dt.days >= 368]
    print(f"\n{name}: quarter lengths {q['days'].min()}-{q['days'].max()} days")
    for cq, r in long_q.iterrows():
        print(f"   14-week quarter? {cq}: {r['start'].date()} to {r['end'].date()} = {r['days']} days"
              f"{' (Q4 worked out from the full year)' if r['q4_derived'] else ''}")
    for _, r in long_y.iterrows():
        print(f"   53-week year?    {r['start'].date()} to {r['end'].date()} = {(r['end'] - r['start']).days} days")
    folder = TENK_DIR / cik
    for f in sorted(folder.glob("*10-K*")) if folder.exists() else []:
        text = clean_text(f.read_bytes())
        hits = [text[max(0, m.start() - 150):m.end() + 100] for m in PATTERN.finditer(text)]
        print(f"   10-K {f.name[:10]}: {len(hits)} mentions of 53 weeks")
        for h in hits[:2]:
            print("      ~", h)
