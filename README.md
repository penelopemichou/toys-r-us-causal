# toys-r-us-causal

**What happened to Mattel's and Hasbro's revenue after Toys "R" Us collapsed?**

## What I found

**Short answer:** with public revenue data and these comparison companies, I can't separate what Toys "R" Us did to Mattel, Hasbro and JAKKS from everything else that happened to them.

- **No convincing match for any of the three toy companies.** For each one I looked for the mix of 8 comparison companies that best followed its revenue before 2017. A match had to stay within 4 points of the company's revenue index (2016 = 100) on average, and within 8 in every quarter, a rule set before running. None did: the average misses were Mattel 4.6, Hasbro 7.4 and JAKKS 7.7 (6.7 without its unusual 2015 Q1).
- **Nothing stands out against "fake" toy companies.** When each comparison company is treated as if it had lost Toys "R" Us, Hasbro ranks 4th of 9, Mattel 6th and JAKKS 7th for how far it drifted from its match after 2017. The matches were not credible, so this is a weak check, and even 1st of 9 would only mean 'most unusual of nine' (about 0.11).
- **The toy companies did fall behind, but they were already moving differently before.** After mid-2017 the three together fell further behind the comparison companies than any of the 56 groups of three comparison companies did. Before then they were not moving in step with them, so this describes the toy companies; it does not measure what Toys "R" Us did. The 56 groups share the same 8 comparison companies, so they are not 56 independent tests; I don't turn 'more than all 56' into a significance claim.
- **At face value, the drop for Mattel and Hasbro is too big for Toys "R" Us alone.** Relative to the comparison companies they fell about 22% and 19% after mid-2017, roughly twice the 8-11% of sales Toys "R" Us represented (JAKKS's 9% fits inside it). That ceiling assumes no sales were replaced elsewhere and ignores indirect effects, and the before-period was not flat, so this only says other things were going on too.

## Background

Toys "R" Us (TRU) filed for bankruptcy in September 2017 and closed its US stores by June 2018. It was one of the biggest customers of the large US toy makers: about 9 % of Hasbro's sales, about 11 % of Mattel's in 2016 and 11.3 % of JAKKS Pacific's in 2017. This project asks how their revenue moved afterwards, compared with similar consumer-products companies that did not sell through TRU.

> **Status:** Finished (24 Nov 2026): difference-in-differences, synthetic control and two sensitivity runs done. Details: `notes/event_study.md`, `notes/synthetic_control.md`, `notes/sensitivity.md`.

## Plan

- **Data:** public SEC EDGAR filings only (XBRL "companyfacts"), quarterly net revenue as first reported. Main window: pre-period 2015 Q1 – 2017 Q2, post-period 2017 Q4 – 2019 Q4 (2013 start as a check for Mattel and Hasbro).
- **Treated companies:** Mattel, Hasbro, JAKKS Pacific.
- **Comparison companies (8):** Garmin, Colgate-Palmolive, Clorox, Hershey, WD-40, Fossil, Deckers Outdoor, Columbia Sportswear: consumer-products makers whose 10-K does not name Toys "R" Us or Babies "R" Us, with no big acquisition or break in 2015–2019 (screen: `notes/screening_table.md`). Electronic Arts only in one sensitivity run.
- **Fit rule (fixed before any model):** a synthetic twin counts only if its average gap to the treated company over the pre-period is at most 4 index points and no quarter is off by more than 8; otherwise "no credible twin".
- **Outcome:** log of revenue indexed to the same quarter of 2016 (= 100).
- **First treated quarter:** 2017 Q4 (2017 Q3 is a transition quarter, tested separately).
- **Methods:** difference-in-differences with a pre-trend (event-study) plot first, then synthetic control for each treated company with placebo tests. Chapters refer to *Causal Inference: The Mixtape* (Cunningham, 2021).
- **Sanity ceiling:** with TRU at 8–11 % of sales, the direct hit is at most about −8 to −11 %, even if no other retailer replaced those sales.

## Honest limits

- Only 2–3 treated companies, and a small comparison pool: 8 companies passed the screen (the plan was 15–25). A placebo test then has about 9 units (1 treated + 8 comparison), so the smallest possible placebo p-value is about 1/9 ≈ 0.1. **This project reports ranks, not statistical significance.**
- The main pre-period is short: 2015 Q1 – 2017 Q2 (10 quarters), because several companies have a jump or break in 2014.
- "Does not name Toys "R" Us in its 10-K" is not the same as "sold nothing through Toys "R" Us": 10-Ks usually name only customers above 10 % of sales.
- No clean comparison group inside toys: every large US toy maker sold through TRU.
- Mattel had its own problems at the same time (weak Barbie and other brands, its own cuts to retailer shipments).
- Revenue is net of replacement: sales lost at TRU may have moved to Amazon, Walmart and Target.
- Consolidated revenue includes international sales and currency effects; TRU's collapse was mainly a US (and UK) event.

## Setup

```bash
/opt/homebrew/bin/python3.12 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python -m ipykernel install --sys-prefix --name toys-r-us-causal --display-name "Python 3.12 (toys-r-us-causal)"
cp .env.example .env   # then put your own email in .env (the SEC asks for one)
```

## Folders

- `src/` scripts · `notebooks/` notebooks · `data/raw/` SEC downloads (not on GitHub) · `data/processed/` tables we build · `results/` charts and tables · `notes/` predictions and data notes
