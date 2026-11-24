# CLAUDE.md — toys-r-us-causal

## What this repo is

Project 4, my first causal-inference project. **Question:** what happened to Mattel's and Hasbro's revenue after Toys "R" Us (TRU) collapsed (bankruptcy Sept 2017, US stores closed by June 2018), compared with similar consumer companies that did not sell through TRU?

You (Claude) write the code. I'm a beginner in Python but comfortable with statistics. I just finished *Causal Inference: The Mixtape* (Cunningham): explain every method by its chapter.

## Rules (follow every session)

- **Public SEC data only (SEC EDGAR).** Never anything from my thesis, TomTom or Kraft Heinz. Never copy anything from my thesis folders or my other projects (only ai-fpa-forecast's public SEC data may be read).
- **One small step at a time.** Explain the code in simple words, and say every time where files go.
- **Claude's prediction first.** Before each run, write your own prediction and save it in `notes/predictions.md`, labelled "Claude's prediction". Don't ask me for one.
- **No downloads without my yes.** Say what you want to download (which files, from where) and wait.
- **Ask me before every git push.** Ask before installing anything new.
- **Honest limits stay in the README.** At the end, "What I found" goes at the top of the README.

## Design (locked in Session 0, 24 Nov 2026)

- **Treated:** Mattel, Hasbro, JAKKS Pacific. TRU share of sales: Hasbro about 9 %; Mattel 11 % in 2016 and about 8–9 % in 2017; JAKKS 11.3 % in 2017.
- **Comparison (donor pool):** US-listed 10-K filers, consumer products sold mostly via big-box retail and Amazon, full quarterly data 2013–2019, whose 10-K does not name Toys "R" Us or Babies "R" Us as a customer. Aim for 15–25 names. Start from the consumer companies in the 20-company ai-fpa-forecast set, then add 10–15 more.
- **Screening rules (24 Nov 2026):**
  1. Prefer discretionary consumer-products makers with a Q4 (holiday) peak, sold through big-box retail and Amazon. At most 2–3 staples.
  2. Drop any company with a big acquisition, merger, spin-off or IPO in 2013–2019 that makes revenue jump, or without full quarterly data 2013 Q1–2019 Q4.
  3. Download the SEC companyfacts file plus the 2016 and 2017 10-Ks. Search every spelling of Toys R Us and Babies R Us (with and without quotes, apostrophes and "&"). Drop any company that names them as a customer.
- **First treated quarter:** 2017 Q4. 2017 Q3 is a transition quarter: left out of the main run, tested as a sensitivity check.
- **Window:** 2013 Q1 to 2019 Q4.
- **Outcome:** quarterly net revenue as an index = each quarter ÷ the same quarter of 2016 × 100. Use logs.
- **Methods:**
  1. Difference-in-differences first, as a warm-up (Mixtape Ch 9, DiD basics; Ch 10 covers the more complex DiD designs). Plot the pre-trends (event-study plot).
  2. Synthetic control (Mixtape Ch 11), one per treated company, with placebo (in-space) tests.
  - Chapter numbers follow the edition I read: Ch 9 = DiD basics, Ch 10 = complex DiD, Ch 11 = synthetic control.
- **Hasbro 2017 Q1 has 14 weeks** (98 days, other quarters 13). Main run: use its revenue × 13/14. Keep the unadjusted number as a check. (Fixed 24 Nov 2026.)
- **No segment revenue for now** (North America / US & Canada). Consolidated net revenue only.
- **Sanity ceiling:** TRU was about 8–11 % of sales, so the direct hit is at most roughly −8 to −11 % even with zero replacement by other retailers.

## Honest limits (must appear in the README)

- Only 2–3 treated companies. With 20 comparison companies the smallest possible placebo p-value is about 1/21.
- No clean comparison group inside toys (every big US toy maker sold through TRU).
- Mattel's own problems at the same time (Barbie and other brands, its own shipment cuts to retailers).
- Revenue is net of replacement: sales lost at TRU may have moved to Amazon, Walmart and Target.
- Consolidated revenue includes international sales and currency effects (TRU's collapse was mostly a US/UK event).

## Data

- Source: SEC EDGAR XBRL "companyfacts" API, `https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json`.
- The SEC requires a User-Agent header with a name and email. The email is read from `.env` (gitignored; see `.env.example`). Never commit it. Stay under 10 requests per second.
- `data/raw/` holds downloaded JSON and is gitignored. `data/processed/` holds the tables we build.
- The sister project `~/Documents/ai-fpa-forecast` already has companyfacts files and a quarterly revenue table for 20 companies. Read it, never modify it. Its revenue rules (tags, fiscal quarters, Q4 = full year − Q1–Q3) are in its `CLAUDE.md` and `src/build_quarterly.py`.
- Data inventory (Session 1): `notes/data_inventory.md`.

## Setup (same as ai-fpa-forecast)

- Python 3.12 (Homebrew, `/opt/homebrew/bin/python3.12`) venv in `.venv/`. Not the Mac's built-in Python 3.9. Run things with `.venv/bin/python`, or activate first: `source .venv/bin/activate`.
- Packages: `requirements.txt` (pinned to the same versions as ai-fpa-forecast).
- Jupyter kernel `toys-r-us-causal` ("Python 3.12 (toys-r-us-causal)"), installed inside the venv. Run notebooks with it, e.g. `jupyter nbconvert --execute --ExecutePreprocessor.kernel_name=toys-r-us-causal …`. A user-level `python3` kernel in `~/Library/Jupyter/kernels/` points to another project's venv: don't use it.
- Git commits use my GitHub no-reply address (`92033020+penelopemichou@users.noreply.github.com`), set in this repo's local git config. Public repo: `github.com/penelopemichou/toys-r-us-causal`.

## After each session

Update `PROGRESS.md` (session log) and `README.md` (status), commit, then ask me before pushing.
