# Predictions

Each prediction is written and saved **before** the run it is about.

## Session 1 (24 Nov 2026)

### Run 1: create the .venv, install packages, register the kernel

**Claude's prediction:** the venv runs Python 3.12.16 (Homebrew); pip installs numpy 2.4.6, pandas 2.3.3, requests 2.32.3, matplotlib 3.9.4 and jupyter 1.1.1 without errors; `jupyter kernelspec list` then shows a kernel named `toys-r-us-causal` inside this project's `.venv`, next to the stale user-level `python3`.

### Run 2: inventory of the SEC data in ~/Documents/ai-fpa-forecast

**Claude's prediction:**

1. Mattel and Hasbro are in the 20-company set; **JAKKS Pacific is not** (it is not in `src/companies.py` there), so its companyfacts file must be downloaded.
2. Mattel and Hasbro have all 28 quarters 2013 Q1–2019 Q4 in `revenue_quarterly.csv` (that table runs from 2008 with no gaps for the original companies).
3. **No segment revenue** (North America / US & Canada) is usable: the companyfacts API leaves out facts with XBRL dimensions (axes and members), and that is where segment numbers are tagged. At most a few undimensioned custom tags will turn up, and they will not cover 2013–2019 cleanly. Segment revenue would need the 10-K/10-Q filings themselves (or the SEC's Financial Statement and Notes data sets).
4. Consumer-products companies among the 20: Mattel and Hasbro (treated), plus the five FMCG names (Procter & Gamble, Colgate-Palmolive, Clorox, Church & Dwight, General Mills). Williams-Sonoma, Best Buy and Macy's are retailers, not makers selling through big-box retail, so they do not fit the donor-pool rule. That leaves **5 usable comparison companies**, far short of the 15–25 target.
5. Three of the five (P&G, Clorox, General Mills) have fiscal years that do not end in December, so their quarters are off-calendar by one or two months.
