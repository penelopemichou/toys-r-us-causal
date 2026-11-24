# Progress

| Session | Date | What | Learned |
|---|---|---|---|
| 1 | 24 Nov 2026 | **Setup and data inventory.** Folder, git repo (no-reply email), Python 3.12 venv, kernel `toys-r-us-causal`, `.gitignore`, `.env` (SEC email, not committed), `CLAUDE.md`, README with honest limits. `src/inventory_sister_data.py` checked the ai-fpa-forecast data (read only): `notes/data_inventory.md`. | Mattel and Hasbro have all 28 quarters 2013–2019; JAKKS is missing; no segment revenue in companyfacts; only 5 of the 20 companies fit the comparison rule. Nothing downloaded. |
| 2 | 24 Nov 2026 | **JAKKS Pacific downloaded and checked.** `src/companies.py` (treated CIKs), `src/download_edgar.py` (downloads only the companies you name), `src/list_revenue_quarters.py` (revenue tags and periods per year). One file: `data/raw/CIK0001009829.json` (3.2 MB, gitignored). | JAKKS has all 28 quarters 2013–2019, tagged directly and adding up to the full year. Its `Revenues` tag for 2013–2015 is only part of sales: never use it. |
