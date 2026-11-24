# toys-r-us-causal

**What happened to Mattel's and Hasbro's revenue after Toys "R" Us collapsed?**

Toys "R" Us (TRU) filed for bankruptcy in September 2017 and closed its US stores by June 2018. It was one of the biggest customers of the large US toy makers: about 9 % of Hasbro's sales, about 11 % of Mattel's in 2016 and 11.3 % of JAKKS Pacific's in 2017. This project asks how their revenue moved afterwards, compared with similar consumer-products companies that did not sell through TRU.

> **Status:** Session 4 — revenue index built, chart and pre-period trends (`notes/index_findings.md`). No models yet. "What I found" will go at the top of this README at the end.

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
