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

## Session 2 (24 Nov 2026): JAKKS Pacific

### Run 3: download the JAKKS companyfacts file (CIK 0001009829)

**Claude's prediction:** one file of about 1–3 MB lands in `data/raw/CIK0001009829.json`; the SEC name inside is "JAKKS PACIFIC INC" (which confirms the CIK); it has a few hundred us-gaap tags, fewer than Mattel (527) because JAKKS is a smaller company.

### Run 4: which revenue values does the JAKKS file have for 2013–2019?

**Claude's prediction:**

1. December year end, quarters ending in March, June, September and December.
2. Revenue tagged as `SalesRevenueNet` up to 2017 and `RevenueFromContractWithCustomerExcludingAssessedTax` from 2018 (the new revenue standard), like Mattel.
3. Q1–Q3 tagged directly every year 2013–2019 and a full-year value every year, so Q4 can be worked out (full year − Q1–Q3) and **all 28 quarters can be built**. Some Q4s may also be tagged directly.
4. Full-year net sales roughly (from memory, could be off by 10 %): 2013 about $630 m, 2014 about $810 m, 2015 about $745 m, 2016 about $705 m, 2017 about $615 m, 2018 about $570 m, 2019 about $600 m. So JAKKS falls about 13 % in 2017 and again in 2018, more than the TRU share alone (11.3 %) would explain.

**Result (written after Runs 3 and 4):**

- Run 3: 3.2 MB, SEC name "JAKKS PACIFIC INC" (CIK confirmed), 552 us-gaap tags. File size and name **right**. Tag count **wrong**: more than Mattel's 527, not fewer.
- Run 4, point 1 (December year end, calendar quarters): **right**.
- Point 2 (tags): **partly wrong**. `SalesRevenueNet` runs 2013 Q1–2018 Q4. `RevenueFromContractWithCustomerExcludingAssessedTax` starts at 2017 Q2 (as prior-year figures in the 2018 filings) and is the only tag for 2019. There is also a `Revenues` tag for 2013–2015 worth only about half of net sales (e.g. $302 m vs $633 m in 2013). It is not total revenue and must not be used.
- Point 3 (all 28 quarters): **right, and better than expected**. Q4 is tagged directly every year, and the four quarters add up exactly to the full year in all seven years. First-reported and latest values are the same, so there are no restatements.
- Point 4 (full-year sales): **right within 1 %**: 632.9, 810.1, 745.7, 706.6, 613.1, 567.8, 598.6 ($ m, 2013–2019). That is −13.2 % in 2017 and −7.4 % in 2018.

## Session 3 (24 Nov 2026): screening the 13 comparison candidates

### Run 5: download 13 companyfacts files and the 2016 and 2017 10-Ks

**Claude's prediction:** all 13 CIKs in `src/companies.py` (typed from memory) are right, so each SEC name matches the company. 13 companyfacts files of 1–5 MB. Two 10-Ks per company (26), 1–3 MB each. One or two companies (Colgate, Hershey or Clorox) attach an Exhibit 13 annual report, which is downloaded too. No errors from the SEC.

### Run 6: the screen (rule 2 data, rule 3 Toys "R" Us mentions)

**Claude's prediction:**

1. The pattern test passes.
2. **Rule 2, data:** 12 of 13 have all 28 quarters 2013–2019. Escalade (small company) is the most likely to have a gap. Year-on-year jumps over 20 % show up for iRobot (fast growth plus the 2017 distributor purchases), Helen of Troy (Hydro Flask, 2016) and possibly Electronic Arts (release timing); none for Colgate, Clorox, Hershey.
3. **Rule 3, Toys "R" Us:** named as a customer by **Escalade** (games and sporting goods sold through toy stores) and possibly **Electronic Arts** (TRU sold games). Mentions, if any, at Logitech or Garmin are only in passing. **No mentions** for Colgate, Clorox, Hershey, WD-40, Deckers, Columbia, Fossil. So about 11 candidates survive rule 3, before you decide on the borderline names.

**Result (written after Runs 5 and 6):**

- Run 5: all 13 CIKs **right**. Companyfacts files 2.9–4.6 MB: **right**. 10-Ks 0.3–6.8 MB: **partly wrong** (I said 1–3 MB). Only Clorox (and Escalade) attach exhibits, as Exhibit 99 not 13: **partly wrong**. "No errors": **wrong**. The download script needed three fixes: older filings sit in a second list; years ending on 2 January belong to the year before; the SEC's filing index pages exist under different names for different filings.
- Run 6, point 1 (pattern test passes): **right**.
- Point 2: 12 of 13 with all 28 quarters, Escalade the gap: **right**. Jumps for iRobot, Helen of Troy, EA and none for Colgate, Clorox, Hershey: **right**. But I missed the jumps at Columbia, Deckers and Logitech.
- Point 3: **wrong**. Nobody names Toys "R" Us or Babies "R" Us, not even Escalade or EA. Rule 3 drops no one.
