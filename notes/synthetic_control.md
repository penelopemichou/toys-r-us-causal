# Synthetic control (Session 6, 24 Nov 2026)

Mixtape Ch 11. Made with `src/synthetic_control.py`; full printout in `results/synth_run_log.txt`. Nothing downloaded, nothing installed: the weights are found with numpy and each set is checked two ways (optimality conditions, and no better result among 20,000 random weight sets).

## How it works, in plain words

For each toy company we build a "twin": a weighted average of the 8 donors' log revenue index, with weights between 0 and 1 that add up to 1. The weights are chosen so the twin follows the toy company as closely as possible from 2015 Q1 to 2017 Q2. If the twin follows well before, its path after 2017 Q3 is our best guess of what would have happened without TRU's collapse. Before that can be trusted, the twin must pass the fit rule (fixed in CLAUDE.md before any run): average gap ≤ 4 index points and no quarter off by more than 8, on the 6 free pre-quarters.

## Step 1: the fit rule (checked before looking at any post-period gap)

Gap = toy company − twin, in index points.

| Run | Average gap (≤ 4) | Worst quarter (≤ 8) | 2017 Q1 | 2017 Q2 | Verdict |
|---|---|---|---|---|---|
| Mattel | 4.56 | 8.47 (2017 Q1) | −8.5 | +5.5 | **no credible twin** (just misses both limits) |
| Hasbro | 7.41 | 9.75 (2017 Q2) | −7.3 | +9.7 | **no credible twin** |
| JAKKS Pacific | 7.73 | 10.82 (2015 Q1) | +5.2 | −7.5 | **no credible twin** |
| JAKKS Pacific, without 2015 Q1 (5 quarters) | 6.65 | 10.12 (2015 Q2) | +3.6 | −9.2 | **no credible twin** (2015 Q1, not fitted: +18.4) |

**No toy company gets a credible twin from these 8 donors.** Mattel comes closest. Its twin tracks 2015–2016 well but cannot copy Mattel's sudden drop in 2017 Q1 and rebound in 2017 Q2.

For comparison, 6 of the 8 donors *do* get a twin that passes the rule when built from the other 7 (all except Fossil and Deckers). So the method can work for ordinary consumer companies; the toy companies just don't move like any mix of them.

## Step 2: the weights, and what they mean

| Donor | Mattel | Hasbro | JAKKS | JAKKS without 2015 Q1 |
|---|---|---|---|---|
| Garmin | – | **0.99** | – | – |
| Colgate-Palmolive | – | – | – | – |
| Clorox | – | – | – | – |
| Hershey | – | – | 0.38 | – |
| WD-40 | 0.23 | – | – | – |
| Fossil Group | **0.57** | – | **0.62** | **0.54** |
| Deckers Outdoor | 0.20 | 0.01 | – | – |
| Columbia Sportswear | – | – | – | 0.47 |

- **Mattel's twin** is 57 % Fossil, 23 % WD-40, 20 % Deckers. Fossil is there because it is the one donor that was shrinking like Mattel. WD-40 steadies the mix, and Deckers adds wobble.
- **Hasbro's twin is really just Garmin (99 %).** Hasbro grew faster before 2017 than any donor. The weights can't go above 1 or below 0, so the closest the method can get is to put everything on the fastest grower, Garmin, and that still isn't close enough. A "twin" that is one other company is not a real synthetic control.
- **JAKKS's twin** is mostly Fossil (shrinking), plus Hershey with 2015 Q1, or Columbia without it.
- Colgate and Clorox, the two staples that fit each other best, get no weight at all: their revenue was too steady to look like a toy company's.

**Leave-one-out** (refit without the largest-weight donor):

| Run | Left out | Worst quarter before → after | Average before → after | New twin |
|---|---|---|---|---|
| Mattel | Fossil (0.57) | 8.5 → **15.4** | 4.6 → 4.2 | Colgate 0.76, WD-40 0.14, Deckers 0.10 |
| Hasbro | Garmin (0.99) | 9.7 → 11.0 | 7.4 → 8.4 | Clorox 0.81, Columbia 0.18 |
| JAKKS | Fossil (0.62) | 10.8 → **15.5** | 7.7 → 8.8 | Colgate 0.61, Hershey 0.39 |
| JAKKS without 2015 Q1 | Fossil (0.54) | 10.1 → **16.8** | 6.7 → 7.6 | Columbia 0.69, Colgate 0.31 |

The twins do fall apart. Without Fossil, the Mattel and JAKKS twins miss their worst quarter by 15–17 points. Each twin leans on one donor, so it is fragile.

## Step 3: placebo in space, and what the ranks mean

Each donor gets its own twin from the other 7, as if it had been "treated". For every company: ratio = (typical gap after 2017 Q3) ÷ (typical gap before), both measured as root mean squared log gaps. A big ratio means the company left its twin's path after 2017 much more than it did before. Rank 1 of 9 = the biggest ratio among the toy company and the 8 donors.

| Run | Ratio | Rank of 9 |
|---|---|---|
| Hasbro | 3.4 | 4 |
| Mattel | 2.1 | 6 |
| JAKKS Pacific | 1.8 | 7 |
| JAKKS Pacific, without 2015 Q1 | 2.8 | 7 (against placebos also fitted without 2015 Q1) |
| Donor placebos | Clorox 8.7, Garmin 4.2, Fossil 3.6, Colgate 2.4, Columbia 2.2, WD-40 1.9, Hershey 1.3, Deckers 1.1 | |

- Rank 6 of 9 for Mattel means 5 of the 8 donors moved away from *their* twins (relative to how well they were fitted) more than Mattel did. Nothing about the toy companies stands out.
- The best possible result would have been rank 1 of 9 (about 0.11). That would still not be "significant" in the usual sense; it would only mean "the most unusual of 9".
- The ratio rewards a good pre-period fit. Clorox ranks first because its twin fits almost perfectly before (pre error 0.01), so a modest move afterwards gives a huge ratio. The toy companies have poor pre-period fits, which shrinks their ratios. Since none of their twins passes the fit rule, their ranks cannot be read as evidence for or against an effect.

## Step 4: post-period gaps: for information, not an effect

The chart is `results/synth_for_information.png`. No twin passed, so there is no `synth_credible.png`.

| Run | Average gap 2017 Q4–2019 Q4 |
|---|---|
| Mattel | −9.5 index points (about −10 %) |
| Hasbro | −24.9 points (about −21 %), mostly because Garmin, its one-company "twin", grew fast in 2018–19 |
| JAKKS | −7.0 points (about −8 %) |
| JAKKS without 2015 Q1 | −15.3 points (about −16 %) |

These are **not** Toys "R" Us effects: the twins did not follow the companies before 2017 Q3. They are shown only so you can see what the method would have said.

## Bottom line

With these 8 donors, synthetic control gives **no credible twin** for Mattel, Hasbro or JAKKS, so it gives no estimate of TRU's effect. This matches the event study: the toy companies were not moving like these consumer companies before 2017 Q3.

## How Claude's prediction did

1. Mattel no credible twin, Fossil the biggest weight (> 0.4), average 4–6: **right** (4.56, Fossil 0.57). The 2017 Q1 miss was smaller than I said (8.5, not 10–15); it only just fails.
2. Hasbro no credible twin, worst quarter 8–10: **right** (9.75). Deckers over 0.5: **wrong**, it is Garmin at 0.99. Average 4–6: **wrong** (7.4).
3. JAKKS fails with 2015 Q1, that quarter off by 9+: **right** (10.8). Without 2015 Q1 fails with Fossil over 0.5: **right** (0.54), but the average was worse than I said (6.7, not 4–5).
4. Leave-one-out makes every twin clearly worse: **right for the worst quarter** (+1 to +7 points). **Wrong for the average**: it rises about 1 point, not 2+, and for Mattel it even falls slightly.
5. Ranks: Mattel 2nd, Hasbro 3rd, JAKKS 6th / 4th: **mostly wrong**. They are Mattel 6th, Hasbro 4th, JAKKS 7th / 7th. Clorox and Garmin near the top: **right**.
6. No toy company ranks 1st: **right**.
