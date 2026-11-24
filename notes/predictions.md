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

## Session 4 (24 Nov 2026): 2014 jumps, index, chart, trends

### Run 7: where are the 2014 jumps (Columbia, Deckers, Logitech, JAKKS), and is Logitech clean from 2015 Q1?

**Claude's prediction:**

1. **Columbia:** the jump starts in 2014 Q1 and lasts all four quarters of 2014, then growth falls back to single digits in 2015. It is a permanent level shift (the business got bigger), not a one-off spike. Cause: the China joint venture (consolidated from Jan 2014) and prAna (bought mid-2014). The 2016 10-K should confirm at least prAna.
2. **Deckers:** the +24 % in 2014 Q2–Q3 is organic growth (UGG and HOKA) and lasts; the "break" is the year-end change in 2014, which only changes fiscal labels, not calendar quarters. Cause stays "from memory" unless the 10-K mentions it.
3. **Logitech:** the −21 % in 2014 Q1 is a seam: 2013 quarters were never restated without Lifesize, later ones were. From 2015 Q1 the series is clean (one tag, quarters add up to the year, no jumps over 20 %), so Logitech **passes** from 2015 Q1. The 2016 10-K will confirm Lifesize as a discontinued operation.
4. **JAKKS:** the jump is in 2014 Q3–Q4 (Q4 about +80 %), driven by Disney *Frozen* products, and it does **not** persist: 2015 is lower than 2014. Cause "from memory" (no JAKKS 10-K downloaded); the XBRL file shows no big acquisition in 2014.

**Result (Run 7):** see "How Claude's prediction did" in `notes/jump_check.md`. In short: Columbia right; Deckers partly right (missed the July 2014 German distributor purchase); Logitech seam right but "clean from 2015 Q1" wrong; JAKKS spike right but a quarter later than I said (2014 Q4–2015 Q1).

### Run 8: revenue index (2016 = 100), chart of treated vs donors, pre-period trend table

**Claude's prediction** (index = revenue ÷ same quarter of 2016 × 100, first-reported; trend = slope of log index on time, 2015 Q1–2017 Q2, in % per year):

1. **Mattel** falls through the pre-period: index about 105 in 2015, about 95–100 by 2017 Q2; trend about **−4 % a year**. Clear drop after the TRU bankruptcy: index about 85 in 2017 Q4 and 75–85 through 2018–2019.
2. **Hasbro** rises strongly before: index about 85–90 in 2015, about 105 in 2017 Q2; trend about **+10 % a year**, the steepest of all 11 companies. Then a fall to about 85–95 in 2018.
3. **JAKKS** falls before: 2015 Q1 about 119 (the *Frozen* tail), trend about **−6 % a year**; about 80–90 after.
4. **Donors** (pre-period trend): Fossil the steepest fall (about −10 % a year); Colgate slightly negative (strong dollar in 2015); Deckers, WD-40 about flat; Clorox, Hershey +1 to +3 %; Garmin, Columbia +5 to +7 %. So the donors span roughly −10 % to +7 % a year.
5. Consequence I expect for later: **Hasbro's pre-trend lies above every donor**, so no weighted average of donors can follow it (a synthetic control can only average, not extrapolate). Hasbro is the most likely "no credible twin". Mattel and JAKKS lie inside the donor range, with Fossil getting a large weight.
6. Only Hasbro 2017 Q1 has 14 weeks among the 11 companies' quarters in the window; no other quarter is longer than 98 days.

**Result (Run 8):** see "How Claude's prediction did" in `notes/index_findings.md`. In short: the treated companies' levels and trends were right, and Hasbro's pre-trend is above every donor, as predicted. Garmin and Columbia grow more slowly than I said. "Only Hasbro has a 14-week quarter" was wrong: Garmin's 2016 Q4 base quarter does too.

## Session 5 (24 Nov 2026): 53-week quarters, fit rule, DiD event study

### Run 9: which quarters 2013–2019 have 14 weeks (53-week years)?

**Claude's prediction:** a 14-week quarter shows as about 97 days between its start and end date (a 13-week quarter is 90; calendar quarters are 89–92). In 2013–2019 there are exactly **four**: Hasbro 2017 Q1, Garmin 2016 Q4, Fossil 2014 Q1 (all three already seen), plus **one at Electronic Arts** (its year ends on the Saturday nearest 31 March). Mattel, JAKKS, Colgate, Clorox, Hershey, WD-40, Deckers and Columbia use calendar month ends, so none. Hershey's 93–94-day quarters are a few extra days, not an extra week. The donors' fiscal 2016–17 10-Ks will say "53 weeks" for Garmin's 2016 only.

**Result (Run 9):** see `notes/fifty_three_weeks.md`. Four 14-week quarters, as predicted (Hasbro 2017 Q1, Garmin 2016 Q4, Fossil 2014 Q1, EA 2015 Q2), but EA's is visible only in its 10-K text, not in the dates. Fossil's and EA's 10-Ks also mention 53 weeks, not only Garmin's.

### Run 10: DiD event study (log index, 2015 Q1–2019 Q4, reference 2017 Q2), with donor placebos

Model: log index = company effect + quarter effect + a separate "treated × quarter" coefficient for every quarter except 2017 Q2. With one treated group and no gaps, each coefficient equals (treated change since 2017 Q2) − (donor change since 2017 Q2).

**Claude's prediction:**

1. **The pre-period is not flat.** Pooled (3 treated together) it looks fairly flat, because the three cancel out: about +0.05 in 2015, about +0.03 in the four 2016 quarters (all equal, since every index is 100 in 2016), about −0.05 in 2017 Q1. But one by one:
   - Hasbro: 2015 coefficients about −0.20 (its fast pre-growth);
   - JAKKS: 2015 Q1 about +0.35 (the *Frozen* spike);
   - Mattel: 2017 Q1 about −0.18 (its own fall before TRU's bankruptcy).
   All three lie outside most donor placebos in at least one pre-quarter.
2. **Post-period:** pooled average about −0.22 (about −20 %), more than the sanity ceiling of −8 to −11 %. One by one, average after: Mattel about −0.30, Hasbro about −0.27, JAKKS about −0.15.
3. **Placebos:** the donors' own post averages run from about −0.20 (Fossil) to about +0.12 (Garmin, Columbia). Mattel and Hasbro rank 1st and 2nd most negative of the 11; JAKKS is near Fossil (3rd–4th).
4. **Verdict I expect to write:** because the pre-period is not flat, the post-period coefficients **cannot be read as a Toys "R" Us effect**.

**Result (Run 10):** see "How Claude's prediction did" in `notes/event_study.md`. The pre-period is not flat (pooled looks flat only by cancellation), the ranks and the verdict were right, and the post sizes were a bit smaller than I said (pooled −0.185, not −0.22).

## Session 6 (24 Nov 2026): synthetic control (Mixtape Ch 11)

### Run 11: one twin per toy company, fit rule, weights, leave-one-out, placebo ranks

Set-up: twin = weighted average of the 8 donors' log index (weights 0–1, sum 1), fitted on 2015 Q1–2017 Q2 (the 2016 quarters are 100 for everyone, so in practice the 6 free quarters decide). Fit rule on the 6 free quarters: average absolute gap ≤ 4 index points and no quarter off by more than 8. Placebo ratio = post-period error ÷ pre-period error (root mean squared gap), ranked among the treated company and the 8 donor placebos (rank 1 = largest ratio).

**Claude's prediction:**

1. **Mattel: no credible twin.** Its 2017 Q1 (index about 85) is below every donor, so that quarter will be off by about 10–15 points (fails the "≤ 8 in any quarter" rule). Average gap about 4–6. Fossil gets the biggest weight (over 0.4), as the only donor that was falling.
2. **Hasbro: no credible twin**, but closer than I said before. Deckers (noisy, with a high 2017 Q2) plus Columbia and Garmin can partly copy Hasbro's climb. Deckers' weight over 0.5. Average gap about 4–6, one quarter off by about 8–10. I give this a 60 % chance of failing.
3. **JAKKS with 2015 Q1: no credible twin.** 2015 Q1 (119) is above every donor (the highest is about 110), so that quarter will be off by 9 or more. **Without 2015 Q1:** closer but still failing on the average (about 4–5), with Fossil over 0.5.
4. **Leave-one-out:** dropping the largest donor makes every twin clearly worse (average gap up by 2 or more points), because only one or two donors move like each toy company.
5. **Placebo ranks** (of 9): Mattel 2nd, Hasbro 3rd, JAKKS 6th with 2015 Q1 and 4th without it. Well-fitted donors such as Clorox and Colgate have tiny pre-period errors, so even small later moves give them big ratios, and they will rank high. Garmin and Columbia (strong growth after 2017) too.
6. So no toy company gets rank 1 of 9, and with failed twins none of the ranks can be read as an effect anyway.

**Result (Run 11):** see "How Claude's prediction did" in `notes/synthetic_control.md`. All three twins fail, as predicted, and Mattel only just misses. But Hasbro's twin is Garmin (0.99), not Deckers. The ranks were mostly wrong: Mattel 6th, Hasbro 4th, JAKKS 7th, against my 2nd, 3rd and 6th. Leave-one-out worsens the worst quarter but barely changes the average.

## Session 7 (24 Nov 2026): sensitivity runs

### Run 12: EA added as a 9th donor (same fit rule, same window)

**Claude's prediction:**

1. **Hasbro** gets a large EA weight (over 0.6). EA grew about as fast as Hasbro before 2017 (+12 % vs +9 % a year), so the twin gets much closer: average gap about 4–5. I give it a 50 % chance of passing. If it passes, it is "passes only with a toy substitute (EA), so not credible".
2. **Mattel** and **JAKKS** (both shrinking) give EA little or no weight (under 0.1), and their fits barely change: all still fail.

### Run 13: 2013 start (pre-period 2013 Q1–2017 Q2) for Mattel and Hasbro, clean donors only

**Claude's prediction:**

1. Clean in 2013–2014 = no jump over 20 % against the same quarter a year earlier and no known acquisition or break: **6 donors** (Garmin, Colgate, Clorox, Hershey, WD-40, Fossil). Deckers and Columbia drop out (both changed in 2014). So the smallest possible placebo rank becomes **1 of 7** (about 0.14) instead of 1 of 9.
2. **Mattel**: index about 115–120 in 2013, falling to 100 in 2016. Colgate (strong dollar) and Fossil fall too, so the twin is mostly Colgate + Fossil. It still **fails**: average gap about 5–7 over the 14 free quarters, because Mattel's 2017 Q1 drop is still there.
3. **Hasbro**: index about 80–85 in 2013, rising. The twin is again mostly Garmin (over 0.7), and it **fails** (average 6–9).

**Result (Runs 12–13):** see "How Claude's prediction did" in `notes/sensitivity.md`. With EA, Hasbro still fails: EA weight 0.36 (I said over 0.6), and the worst quarter got worse. Mattel and JAKKS ignore EA. With the 2013 start, the 6 clean donors and the 1-of-7 limit were right; Mattel's twin is mostly Colgate and fails on 2017 Q1; Hasbro's is Garmin and fails.
