# Revenue index, chart and pre-period trends (24 Nov 2026)

Made with `src/build_index.py`. No models. Files:
- `data/processed/revenue_quarterly.csv`: revenue (first reported and restated) and the index for 12 companies, 2013 Q1–2019 Q4, 336 rows, no missing quarters.
- `results/index_treated_vs_donors.png`: the chart.
- `results/pretrend_table.csv`: the table below.

Index = revenue ÷ revenue in the same quarter of 2016 × 100 (first reported; Hasbro 2017 Q1 × 13/14). Mattel's and Hasbro's SEC files were copied from `~/Documents/ai-fpa-forecast/data/raw/` (downloaded there on 16 Nov 2026), not downloaded again.

## Pre-period trend table (2015 Q1 – 2017 Q2)

"Trend" = slope of the log index against time, in % per year. "Wobble" = how far the quarters sit from that straight line (standard deviation, roughly in index points).

| Company | Group | Trend % / year | Wobble | Index 2015 Q1 | 2017 Q2 | 2017 Q3 | Mean after (2017 Q4–2019 Q4) | 2019 Q4 |
|---|---|---|---|---|---|---|---|---|
| Mattel | treated | −4.8 | 5.9 | 106.1 | 101.8 | 86.9 | 83.6 | 80.3 |
| Hasbro | treated | **+9.1** | 4.5 | 85.8 | 110.6 | 106.7 | 94.1 | 87.6 |
| JAKKS Pacific | treated | −7.3 | 7.6 | 119.2 | 84.8 | 86.7 | 81.8 | 91.3 |
| Garmin | donor | +4.3 | 2.6 | 93.8 | 100.7 | 102.9 | 116.2 | 128.1 |
| Colgate-Palmolive | donor | −3.5 | 1.5 | 108.2 | 99.5 | 102.8 | 103.0 | 107.9 |
| Clorox | donor | +2.9 | 1.5 | 98.2 | 102.9 | 104.0 | 104.9 | 103.1 |
| Hershey | donor | +0.7 | 2.9 | 106.0 | 101.5 | 101.5 | 105.3 | 105.0 |
| WD-40 | donor | +1.2 | 2.9 | 102.9 | 101.8 | 99.4 | 110.2 | 110.4 |
| Fossil Group | donor | −8.9 | 3.2 | 109.9 | 87.1 | 93.3 | 80.2 | 74.2 |
| Deckers Outdoor | donor | +2.1 | **9.9** | 90.0 | 120.3 | 99.3 | 119.1 | 123.5 |
| Columbia Sportswear | donor | +3.4 | 2.8 | 91.2 | 102.6 | 100.2 | 121.9 | 133.1 |
| Electronic Arts | sensitivity only | +10.8 | 4.2 | 90.6 | 114.0 | 106.8 | 116.1 | 138.6 |

## What I see, in plain words

1. **Before TRU's bankruptcy, the three toy companies were already going different ways.** Mattel was shrinking (about −5 % a year), JAKKS shrinking faster (−7 %, coming down from its 2014–15 *Frozen* peak), and Hasbro growing fast (+9 %).
2. **After 2017 Q3, all three end up below where they were in 2016**: Mattel about 84 on average, JAKKS about 82, Hasbro about 94. Over the same time the donors' median rises to about 105–113. So the raw gap between toy makers and donors is about 20–30 index points.
3. **That raw gap is far bigger than TRU alone can explain.** TRU was 8–11 % of sales, so even with no replacement the direct hit is at most about −8 to −11 %. This is a raw comparison, not an estimate. It already says much of the fall must come from something else, such as Mattel's own problems, or from the donors simply growing.
4. **Mattel was hit before the bankruptcy.** Its 2017 Q1 index is 85 (−15 % against 2016 Q1) in the pre-period, then 102 in 2017 Q2. Its own trouble started before TRU's bankruptcy.
5. **Hasbro will be hard to copy.** Its pre-trend (+9 %) is above every donor (the highest is Garmin, +4 %). A synthetic control is a weighted average of donors, so it can't climb faster than the fastest donor. Hasbro is the most likely "no credible twin". (Only EA, which is excluded as a donor, grows as fast.)
6. **Mattel and JAKKS sit inside the donors' range.** Fossil (−9 %) and Colgate (−3.5 %) are the only falling donors, so they will probably carry most of the weight.
7. **Deckers is noisy** (wobble 9.9): its 2016 Q2 was unusually weak, so every later Q2 looks high against it (up to about 150).

## Two things you should know before the models

- **The 14-week rule also matters for Garmin.** Garmin's 2016 Q4 has 14 weeks (97 days). It is a *base* quarter, so every Garmin Q4 index is about 7 % too low (each Q4 divided by a quarter one week too long). Your 13/14 rule covers only Hasbro 2017 Q1, so I did **not** adjust Garmin. Fossil 2014 Q1 is also 14 weeks, but it is outside the main window. Hershey has three quarters of 93–94 days (a few extra days, not a full week).
- **The index is 100 for every company in all four quarters of 2016, by construction.** So 4 of the 10 pre-period quarters fit perfectly for any twin, and the fit rule's "average gap ≤ 4 points" is really decided by the other 6 quarters (2015 Q1–Q4, 2017 Q1–Q2). An average of ≤ 4 over 10 quarters allows an average of about 6.7 over those 6. One way out: judge the fit on the 6 non-2016 quarters only. Your call; I changed nothing.

First reported and restated revenue never differ by more than 2 % in 2015–2019 for these 12 companies, so the "first reported" choice does not change the picture here.

## How Claude's prediction did

1. Mattel (about 105 → 95–100, −4 %/yr, about 85 after): **right** (106 → 102, −4.8 %/yr, 84 after).
2. Hasbro (+10 %/yr, steepest; about 85–95 after): **right** (+9.1 %/yr, 94 after). It is the steepest of the 11; only EA is steeper.
3. JAKKS (2015 Q1 about 119, −6 %/yr, 80–90 after): **right** (119.2, −7.3 %/yr, 82 after).
4. Donor trends from about −10 % to +7 %: **mostly right**. Fossil steepest fall (−8.9 %) and Colgate slightly negative were right, but Garmin and Columbia grow more slowly than I said (+4.3 and +3.4 %, not +5 to +7 %).
5. Hasbro above every donor; Mattel and JAKKS inside the range: **right**.
6. "Only Hasbro 2017 Q1 has 14 weeks": **wrong**. Garmin 2016 Q4 (a base quarter) and Fossil 2014 Q1 also do.
