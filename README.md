# toys-r-us-causal

**What happened to Mattel's and Hasbro's revenue after Toys "R" Us collapsed?**

Toys "R" Us (TRU) filed for bankruptcy in September 2017 and closed its US stores by June 2018. It was one of the biggest customers of the large US toy makers: about 9 % of Hasbro's sales, about 11 % of Mattel's in 2016 and 11.3 % of JAKKS Pacific's in 2017. This project asks how their revenue moved afterwards, compared with similar consumer-products companies that did not sell through TRU.

> **Status:** Session 1 — setup and data inventory. No results yet. "What I found" will go at the top of this README at the end.

## Plan

- **Data:** public SEC EDGAR filings only (XBRL "companyfacts"), quarterly net revenue 2013 Q1 – 2019 Q4.
- **Treated companies:** Mattel, Hasbro, JAKKS Pacific.
- **Comparison companies:** US-listed consumer-products companies sold mostly through big-box retail and Amazon, whose 10-K does not name Toys "R" Us or Babies "R" Us as a customer (aim: 15–25).
- **Outcome:** log of revenue indexed to the same quarter of 2016 (= 100).
- **First treated quarter:** 2017 Q4 (2017 Q3 is a transition quarter, tested separately).
- **Methods:** difference-in-differences with a pre-trend (event-study) plot first, then synthetic control for each treated company with placebo tests. Chapters refer to *Causal Inference: The Mixtape* (Cunningham, 2021).
- **Sanity ceiling:** with TRU at 8–11 % of sales, the direct hit is at most about −8 to −11 %, even if no other retailer replaced those sales.

## Honest limits

- Only 2–3 treated companies. With 20 comparison companies the smallest possible placebo p-value is about 1/21.
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
