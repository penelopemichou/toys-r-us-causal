# Sensitivity runs (Session 7, 24 Nov 2026)

Made with `src/synth_sensitivity.py` (uses `src/synth_core.py`); printout in `results/synth_sensitivity_log.txt`. The main results, fit rule, window and donor list are unchanged. Before anything else, the script rebuilds the main twins with the shared module and checks that they match `results/synth_fit.csv`. They do.

## 1. Electronic Arts as a 9th donor

| Run | EA weight | Average gap: 8 donors → with EA | Worst quarter: 8 donors → with EA | Verdict with EA |
|---|---|---|---|---|
| Mattel | 0 | 4.56 → 4.56 | 8.47 → 8.47 | no credible twin |
| Hasbro | 0.36 | 7.41 → 6.36 | 9.75 (2017 Q2) → **12.18** (2017 Q1) | no credible twin |
| JAKKS | 0 | 7.73 → 7.73 | 10.82 → 10.82 | no credible twin |
| JAKKS without 2015 Q1 | 0 | 6.65 → 6.65 | 10.12 → 10.12 | no credible twin |

**In plain words:** adding a video-game company changes nothing for the two shrinking toy makers: the method gives EA no weight at all. For Hasbro, the twin becomes 60 % Garmin, 36 % EA and 4 % Deckers. The average gap gets smaller, but the worst quarter moves and gets worse: 2017 Q2 improves (+9.75 → +4.55), while 2017 Q1 goes from −7.34 to −12.18, which breaks the "no quarter off by more than 8" limit. So it still fails. (Corrected 24 Nov 2026: an earlier version said "2017 Q1 gets worse (9.7 → 12.2)", mixing the 2017 Q2 gap before with the 2017 Q1 gap after.) The method minimises the squared gap over the whole pre-period, not the fit rule, so a better average can come with a worse single quarter. No twin "passes only with EA", so that label is not needed.

## 2. 2013 start (Mattel and Hasbro), clean donors only

**Donors left: 6 of 8.** Garmin, Colgate, Clorox, Hershey, WD-40 and Fossil have no quarter in 2014–2015 more than 20 % above or below a year earlier. Deckers (+24 % in 2014 Q2–Q3; UGG distributor bought July 2014; year-end change) and Columbia (+22 to +29 % in 2014; prAna and the China joint venture) are out. The table starts in 2013, so 2013 itself can only be compared forward with 2014.

**Effect on the placebo test:** with 6 donors, a placebo test has 7 units, so the best possible rank is 1 of 7 (about 0.14) instead of 1 of 9 (about 0.11). A shorter list makes even a perfect result weaker.

| Run | Average gap (14 free quarters) | Worst quarter | 2017 Q1 | 2017 Q2 | Weights | Verdict | Placebo rank |
|---|---|---|---|---|---|---|---|
| Mattel, 2013 start | 4.87 | **13.34** (2017 Q1) | −13.3 | +4.5 | Colgate 0.84, Fossil 0.17 | no credible twin | 3/7 |
| Hasbro, 2013 start | 8.53 | **20.83** (2014 Q4) | −7.4 | +10.0 | Garmin 1.00 | no credible twin | 3/7 |

**In plain words:**
- **Mattel:** over 2013–2016 its decline looks a lot like Colgate's (both fall about 5 % a year; for Colgate it was mostly the strong dollar), so the twin is mostly Colgate. The average gap is just above the limit (4.9), but Mattel's sudden 2017 Q1 drop is now 13 points below the twin. Fails.
- **Hasbro:** again the twin is simply Garmin, the fastest grower. It misses badly in 2014 (21 points). Fails.
- Their ranks (3 of 7) are not evidence either way, because neither twin passes.

## What the sensitivity runs change

Nothing. Under every version (8 donors, 9 donors with EA, 2013 start with 6 clean donors), **no toy company gets a credible twin.** The post-period gaps of these runs (Mattel −10 % / −15 %, Hasbro −20 % / −21 %, JAKKS −8 % / −16 %) are for information only, not effects.

## How Claude's prediction did

Run 12 (EA):
1. Hasbro gets a large EA weight (over 0.6) and an average gap of 4–5: **wrong**. EA weight 0.36, average 6.4. "50 % chance of passing": it failed.
2. Mattel and JAKKS give EA under 0.1 and still fail: **right** (weight 0, unchanged).

Run 13 (2013 start):
1. 6 clean donors (those exact six), best rank 1 of 7: **right**.
2. Mattel mostly Colgate + Fossil, fails because of 2017 Q1: **right** (0.84 + 0.17; 2017 Q1 off by 13). Average 5–7: **slightly wrong** (4.9).
3. Hasbro mostly Garmin (over 0.7), fails with average 6–9: **right** (Garmin 1.0, average 8.5).
