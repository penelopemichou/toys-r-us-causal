# DiD warm-up: event study (Session 5, 24 Nov 2026)

Made with `src/event_study.py`. Files: `results/event_study.png`, `results/event_study_coefficients.csv` (every coefficient), `results/event_study_summary.csv`, `results/event_study_three_donor_placebos.csv`.

## What was run (Mixtape Ch 9)

Outcome: log revenue index (same quarter of 2016 = 100; 14-week quarters × 13/14), 2015 Q1–2019 Q4, 11 companies.

log index = company effect + quarter effect + one "treated × quarter" coefficient per quarter, except the reference quarter 2017 Q2 (= 0).

A coefficient of −0.20 means: between 2017 Q2 and that quarter, the treated company's revenue index fell 0.20 log points (about 18 %) more than the donors'. With no gaps in the data this is exactly (treated change since 2017 Q2) − (average donor change since 2017 Q2); the script checks that the regression and this hand calculation agree.

- **Pooled:** Mattel + Hasbro + JAKKS vs the 8 donors.
- **One by one:** each treated company vs the 8 donors.
- **Placebos:** each donor vs the other 7 donors, as if it had been treated. For the pooled run there is also a like-for-like placebo: every group of 3 donors (56 groups) vs the other 5.
- **No standard errors.** With 3 treated companies they can't be trusted; the placebos take their place.

"Free" pre-quarters = 2015 Q1–Q4 and 2017 Q1. (2016 is 100 for everyone by construction, so the four 2016 coefficients are all equal; 2017 Q2 is the reference.)

## Results

| Run | Largest pre-period coefficient (size, quarter) | 2017 Q1 | Average after (2017 Q4–2019 Q4) | ≈ % | Rank after (1 = most negative of 11) |
|---|---|---|---|---|---|
| Pooled (3 treated) | 0.06 (2015 Q1) | −0.04 | −0.185 | −17 % | more negative than all 56 three-donor placebos |
| Mattel | −0.17 (2017 Q1) | −0.17 | −0.247 | −22 % | 1 |
| Hasbro | −0.23 (2015 Q1); 2015 all about −0.20 | −0.14 | −0.215 | −19 % | 2 |
| JAKKS Pacific | +0.36 (2015 Q1); 2016 +0.18 | +0.17 | −0.091 | −9 % | 4 |
| Fossil (placebo) | +0.29 (2015 Q1) | +0.04 | −0.156 | −14 % | 3 |
| Deckers (placebo) | −0.31 (2015 Q1) | −0.22 | −0.080 | −8 % | 5 |
| Clorox, Colgate, Hershey (placebos) | 0.07–0.12 | about +0.03 | −0.02 to −0.04 | −2 to −4 % | 6–8 |
| WD-40, Garmin, Columbia (placebos) | 0.07–0.11 | about +0.03 | +0.03 to +0.14 | +4 to +15 % | 9–11 |

## Are the pre-period coefficients flat? In plain words: **no**

- **Pooled, they look flat** (between −0.04 and +0.06, well inside the placebo range). **But that is the three companies cancelling each other out**, not three flat lines:
  - **Hasbro** sits about −0.20 below zero all through 2015. It grew about 20 % faster than the donors before the bankruptcy.
  - **JAKKS** sits +0.36 in 2015 Q1 and about +0.18 through 2016. It was coming down from its *Frozen* peak, faster than the donors.
  - **Mattel** is flat in 2015–2016 but drops to −0.17 in 2017 Q1, before the bankruptcy. Its own trouble started early.
- Each treated company is outside 7 of the 8 donor placebos in at least one pre-quarter (JAKKS outside all 8 in 2015 Q1).
- Two donors (Fossil, Deckers) are not flat before either. The comparison group itself is mixed.

**So the post-period coefficients cannot be read as a Toys "R" Us effect.** The treated companies were not moving in parallel with the donors before 2017 Q3 (parallel pre-trends, the key DiD assumption in Mixtape Ch 9, fails one by one). Pooling hides this rather than fixing it.

## What the post-period shows (description only, not an effect)

- After 2017 Q3 all three fall relative to the donors: Mattel about −22 %, Hasbro −19 %, JAKKS −9 % on average. Pooled −17 %, more negative than every group of 3 donors.
- Mattel and Hasbro have the two most negative post averages of all 11 companies.
- These sizes (−17 to −22 %) are about twice the sanity ceiling (TRU was 8–11 % of sales, so at most about −8 to −11 % even with zero replacement). Most of the fall must come from something else: Mattel's own decline (already visible in 2017 Q1), Hasbro losing its fast pre-2017 growth, and donors like Garmin and Columbia growing.
- JAKKS's −9 % is within the ceiling, but its pre-period is the least flat of all.

## How Claude's prediction did

1. Pre-period not flat, and pooled looks flat only because the three cancel: **right**. Numbers close: pooled +0.06 (2015 Q1), +0.03 (2016), −0.04 (2017 Q1); Hasbro about −0.20 in 2015; JAKKS +0.36 in 2015 Q1; Mattel −0.17 in 2017 Q1. Each outside most placebos in at least one pre-quarter: **right**.
2. Post averages: **right in direction, a bit too large in size**. Pooled −0.185 (I said −0.22), Mattel −0.25 (−0.30), Hasbro −0.22 (−0.27), JAKKS −0.09 (−0.15).
3. Placebo range from Fossil −0.16 to Garmin/Columbia +0.13/+0.14, and ranks Mattel 1, Hasbro 2, JAKKS 4: **right**.
4. Verdict (cannot read as a TRU effect): **right**.
