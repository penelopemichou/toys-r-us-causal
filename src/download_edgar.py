"""Download SEC EDGAR "companyfacts" JSON files for the companies you name.

A companyfacts file holds every number a company has tagged in its filings
(10-Q, 10-K, ...), for every period, together with the filing it came from.
Each file is saved unchanged in data/raw/ (gitignored, so not on GitHub).

You name the companies on the command line, so nothing is downloaded by
accident. Files already in data/raw/ are kept, unless you add --refresh.

Run from the project folder, for example:
    .venv/bin/python src/download_edgar.py "JAKKS Pacific"
"""

import json
import sys
import time
from pathlib import Path

import requests

from companies import ALL_COMPANIES

# --- 1. Settings --------------------------------------------------------
PROJECT = Path(__file__).resolve().parent.parent   # the folder above src/
RAW_DIR = PROJECT / "data" / "raw"
URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"

# The SEC allows at most 10 requests per second; 0.5 s between requests = 2 per second.
PAUSE_SECONDS = 0.5


# --- 2. Read the email from .env -----------------------------------------
def read_email():
    """Return SEC_EMAIL from the .env file (a simple NAME=value file)."""
    env_file = PROJECT / ".env"
    if not env_file.exists():
        raise SystemExit("No .env file. Copy .env.example to .env and add your email.")
    for line in env_file.read_text().splitlines():
        if line.startswith("SEC_EMAIL="):
            return line.split("=", 1)[1].strip()
    raise SystemExit("SEC_EMAIL is missing from .env")


# --- 3. Download each company you named ------------------------------------
def main():
    names = [a for a in sys.argv[1:] if not a.startswith("--")]
    refresh = "--refresh" in sys.argv
    unknown = [n for n in names if n not in ALL_COMPANIES]
    if not names or unknown:
        raise SystemExit(f"Name one or more of: {list(ALL_COMPANIES)}. Unknown: {unknown}")

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    # The SEC asks every program to say who it is: a name and an email.
    headers = {"User-Agent": f"Penelope Michou {read_email()}"}

    for name in names:
        cik = ALL_COMPANIES[name]
        out_file = RAW_DIR / f"CIK{cik}.json"
        if out_file.exists() and not refresh:
            print(f"{name:<20} -> data/raw/{out_file.name}  already downloaded, kept")
            continue
        response = requests.get(URL.format(cik=cik), headers=headers, timeout=60)
        response.raise_for_status()   # stop with an error if the SEC says no

        out_file.write_bytes(response.content)   # save exactly what we got

        # A quick look inside, so we know the file is the company we wanted.
        data = json.loads(response.content)
        n_tags = len(data["facts"].get("us-gaap", {}))
        size_mb = len(response.content) / 1_000_000
        print(f"{name:<20} -> data/raw/{out_file.name}  {size_mb:4.1f} MB, "
              f"SEC name: {data['entityName']!r}, {n_tags} us-gaap tags")
        time.sleep(PAUSE_SECONDS)


if __name__ == "__main__":
    main()
