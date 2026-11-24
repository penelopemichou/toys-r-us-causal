"""Download the 10-K annual reports for 2016 and 2017 of the companies you name.

Steps for each company:
  1. Ask the SEC for the company's list of filings (the "submissions" file).
  2. Pick the 10-Ks for fiscal years 2016 and 2017. A fiscal year is named
     after the year in which it ends; a year ending on 2 January 2016 counts
     as fiscal 2015 (we take 15 days off the end date before reading the year).
  3. Download the main 10-K document, and any Exhibit 13 or 99 (some companies
     put their annual report there instead of in the main document).

Files go to data/raw/10k/<CIK>/ (gitignored), saved exactly as received.
Files already there are kept.

Run from the project folder, for example:
    .venv/bin/python src/download_10k.py Garmin "Electronic Arts"
"""

import json
import re
import sys
import time
from datetime import date, timedelta
from pathlib import Path

import requests

from companies import ALL_COMPANIES
from download_edgar import read_email

PROJECT = Path(__file__).resolve().parent.parent
OUT_DIR = PROJECT / "data" / "raw" / "10k"
SUBMISSIONS_URL = "https://data.sec.gov/submissions/CIK{cik}.json"
ARCHIVE_URL = "https://www.sec.gov/Archives/edgar/data/{cik_int}/{acc}/{file}"
OLDER_URL = "https://data.sec.gov/submissions/{name}"
YEARS = ("2016", "2017")
PAUSE_SECONDS = 0.5   # 2 requests per second, far below the SEC's limit of 10


def fiscal_year(report_date):
    """'2016-01-02' -> '2015'; '2016-12-31' -> '2016' (15 days back, then the year)."""
    return str((date.fromisoformat(report_date) - timedelta(days=15)).year)


def get(url, headers):
    """Download one URL politely; stop with an error if the SEC says no."""
    time.sleep(PAUSE_SECONDS)
    response = requests.get(url, headers=headers, timeout=60)
    response.raise_for_status()
    return response.content


def list_files(base, accession, headers):
    """Names of the files in one filing's folder (from whichever index page exists)."""
    try:
        return [i["name"] for i in json.loads(get(base + "index.json", headers))["directory"]["item"]]
    except requests.HTTPError:
        pass
    for page in (f"{accession}-index.htm", f"{accession}-index.html"):
        try:
            text = get(base + page, headers).decode("latin-1")
        except requests.HTTPError:
            continue
        return sorted(set(re.findall(r'href="/Archives/edgar/data/\d+/\d+/([^"/]+)"', text)))
    raise SystemExit(f"No index page found for {base}")


def main():
    names = sys.argv[1:]
    unknown = [n for n in names if n not in ALL_COMPANIES]
    if not names or unknown:
        raise SystemExit(f"Name one or more of: {list(ALL_COMPANIES)}. Unknown: {unknown}")
    headers = {"User-Agent": f"Penelope Michou {read_email()}"}

    for name in names:
        cik = ALL_COMPANIES[name]
        folder = OUT_DIR / cik
        folder.mkdir(parents=True, exist_ok=True)

        # 1. The list of the company's filings, as parallel lists. Big filers
        #    keep their older filings in extra files, listed under "files".
        sub = json.loads(get(SUBMISSIONS_URL.format(cik=cik), headers))["filings"]
        tables = [sub["recent"]]
        for extra in sub["files"]:
            tables.append(json.loads(get(OLDER_URL.format(name=extra["name"]), headers)))
        filings = [dict(zip(t, row)) for t in tables for row in zip(*t.values())]

        # 2. Original 10-Ks (not amendments) for fiscal years 2016 and 2017.
        tenks = [f for f in filings if f["form"] == "10-K" and fiscal_year(f["reportDate"]) in YEARS]
        if len(tenks) != 2:
            print(f"{name}: expected 2 10-Ks for {YEARS}, found {len(tenks)}")

        for f in sorted(tenks, key=lambda f: f["reportDate"]):
            acc = f["accessionNumber"].replace("-", "")
            base = ARCHIVE_URL.format(cik_int=int(cik), acc=acc, file="")

            # 3. List the files in the filing. The SEC offers three index pages,
            #    but not every filing has all three, so try them in turn.
            #    Exhibits 13 and 99 are then found by their file name, e.g.
            #    "ex13.htm", "exhibit99-1.htm", "clx-ex99_1.htm".
            file_names = list_files(base, f["accessionNumber"], headers)
            docs = [(f["primaryDocument"], "10-K")]
            for file_name in file_names:
                found = re.search(r"ex(?:hibit)?[-_]?(13|99)", file_name, flags=re.I)
                if found and file_name.lower().endswith((".htm", ".html", ".txt")):
                    docs.append((file_name, f"EX-{found.group(1)}"))

            for file_name, doc_type in docs:
                out_file = folder / f"{f['reportDate']}_{doc_type}_{file_name}"
                if out_file.exists():
                    print(f"{name:<20} {out_file.name}  already downloaded, kept")
                    continue
                content = get(base + file_name, headers)
                out_file.write_bytes(content)
                print(f"{name:<20} {f['reportDate']} {doc_type:<6} filed {f['filingDate']}  "
                      f"-> data/raw/10k/{cik}/{out_file.name}  {len(content)/1e6:4.1f} MB")


if __name__ == "__main__":
    main()
