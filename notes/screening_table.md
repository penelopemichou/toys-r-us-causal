# Screening table: 13 comparison candidates (24 Nov 2026)

Rules in `CLAUDE.md`. Made with `src/download_edgar.py`, `src/download_10k.py` and `src/screen_candidates.py`. Machine-readable version: `results/screening_data.csv`; every Toys "R" Us search hit with its context: `results/screening_tru_mentions.txt` (there are none).

Downloaded (all gitignored): 13 companyfacts files in `data/raw/` (2.9–4.6 MB each) and the fiscal-2016 and fiscal-2017 10-Ks in `data/raw/10k/<CIK>/` (26 main documents plus Clorox's six and Escalade's one Exhibit 99, 72 MB). A fiscal year is named after the year it ends in; a year ending on 2 January counts as the year before.

## Rule 3: Toys "R" Us / Babies "R" Us in the 10-Ks

**No company names them, in any spelling, in any of the 33 documents.** The search pattern was first tested on 14 spellings (with and without quotes, curly quotes, apostrophes, dashes, "&", HTML codes) and 3 look-alikes. To check the text came through properly, the same files do name Walmart, Target, Amazon, Best Buy, GameStop and Dick's Sporting Goods. None of them uses the word "toy" at all.

Not naming TRU does not prove a company sold nothing through TRU: 10-Ks usually only name customers above 10 % of sales. TRU did sell video games (Electronic Arts) and some electronics (Garmin, Logitech).

## The table

"Quarters" = calendar quarters 2013 Q1–2019 Q4 found (28 needed). "Jumps" = quarters whose revenue is more than 20 % above or below the same quarter a year earlier.

| Company | Year ends | Quarters | Jumps > 20 % | TRU named | Verdict | Why |
|---|---|---|---|---|---|---|
| Garmin | Dec | 28 | none (max 18 %) | no | **in** | clean; holiday peak; Best Buy, Amazon, Walmart |
| Colgate-Palmolive | Dec | 28 | none (max 9 %) | no | **in** (staple 1) | clean |
| Clorox | June | 28 | none (max 5 %) | no | **in** (staple 2) | clean; one 2013 quarter mixes two tags (1 % off), fix when building |
| Hershey | Dec | 28 | none (max 6 %) | no | **in** (staple 3) | clean; the Amplify purchase (2018) is not visible |
| WD-40 | Aug | 28 | none (max 9 %) | no | **in** | clean data; weak fit for rule 1 (no Q4 peak) |
| Fossil Group | Dec/Jan | 28 | none (max 18 %) | no | **in** | clean; revenue falls steadily from 2015 (a trend, not a jump) |
| Deckers Outdoor | Mar (Dec until 2014) | 28 | 2014 Q2–Q3 (+24 %), 2017 Q2 (+20 %) | no | **in, check** | moved its year end from December to March in 2014; cause of the 2014 jumps not yet checked |
| Columbia Sportswear | Dec | 28 | 2014 Q1–Q4 (+22 to +29 %), 2018 Q2 (+21 %) | no | **your call** | 2014 jumps probably from buying prAna and consolidating its China joint venture (my memory, to check); three years before treatment |
| Logitech | Mar | 28 | 2014 Q1 (−21 %), 2017 Q4 (+22 %) | no | **your call** | 2014 Q1 is probably the seam where 2013 still includes Lifesize (spun off 2016) and later years are restated without it |
| Electronic Arts | Mar | 28 | 7 quarters, up to +42 % | no | **your call** | no acquisition, but very lumpy (game release dates, deferred revenue); video games are close substitutes for toys (spillover risk) |
| iRobot | Dec/Jan | 28 | 9 quarters, incl. 2017 Q4 +54 % | no | **out** (rule 2) | bought its Japan (Apr 2017) and Europe (Oct 2017) distributors, right at the treatment date: revenue jumps from selling direct, not from demand |
| Helen of Troy | Feb | 28 | 2015 Q1 (+21 %) | no | **out** (rule 2) | the later figures drop the Nutritional Supplements business (sold around Dec 2017, about 10 % of sales) but the older quarters still include it: a ~10 % break at the treatment date. Also Hydro Flask (2016). |
| Escalade | Dec | 25 (Q2 2017, 2018, 2019 missing) | 6 quarters | no | **out** (rule 2) | from 2017 its quarters are 12, 16, 12 and 12 weeks long, so Q2 is not comparable; revenue tags disagree; tiny and noisy |

## In plain words

- **In (7):** Garmin, Colgate-Palmolive, Clorox, Hershey, WD-40, Fossil, Deckers (Deckers' 2014 jumps still to check).
- **Your call (3):** Columbia Sportswear, Logitech, Electronic Arts.
- **Out (3):** iRobot, Helen of Troy, Escalade.

So the pool is **7 to 10 companies**. The smallest possible placebo p-value is then 1/8 = 0.125 (7) to 1/11 ≈ 0.09 (10). That is still well short of the 15–25 target and the 1/21 in the design.
