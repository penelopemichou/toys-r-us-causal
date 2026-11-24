# The 2014 jumps, checked in the quarterly data (24 Nov 2026)

Made with `src/check_jumps.py` (reads only files already downloaded). "Confirmed" = stated in a 10-K we have (fiscal 2016 or 2017) or visible in the SEC data. "From memory" = not checked in a filing.

| Company | When the jump happens | Does it last? | Cause | Label |
|---|---|---|---|---|
| Columbia Sportswear | 2014 Q1 (+22 %), all of 2014 (+16 to +29 %), still +13 to +17 % in 2015 Q1–Q3, normal from 2015 Q4 | **Yes, a lasting step up.** Calendar-year sales $1,685 m (2013) → $2,101 m (2014) → $2,326 m (2015), then +2 to +4 % a year until 2017 | China joint venture with Swire started operating in 2014; prAna bought in 2014. The SEC data also has "pro forma revenue" facts for 2013–2014, which companies report after an acquisition | **confirmed** (both stated in the 2016 and 2017 10-Ks); how much each added is not stated in what we searched |
| Deckers Outdoor | 2014 Q2 and Q3 (+24 % each); Q4 +7 % | **Yes, the level stays:** 2015 Q2–Q4 only +1 % above 2014, not back down | (a) In July 2014 Deckers bought its UGG distributor in Germany. (b) It moved its year end from December to March (approved Feb 2014; Jan–Mar 2014 was a "transition period"), which changes fiscal labels only, not calendar quarters. (c) The rest is probably UGG growth | (a) and (b) **confirmed** (2016 10-K); size of (a) unknown; (c) **from memory** |
| Logitech | 2014 Q1 −21 % in restated data, but +5 % as first reported | Not a real jump: a **data seam** | Lifesize (video conferencing, 4–6 % of sales) sold in fiscal 2016 and restated as discontinued for past full years, but not for every past quarter. A Q4 worked out as "full year − Q1–Q3" then takes the whole year's Lifesize removal: Jan–Mar 2015 is 17 % too low in restated data, Jan–Mar 2016 11 % too high | Lifesize **confirmed** (2016 and 2017 10-Ks: "treat the Lifesize segment as discontinued operations") |
| JAKKS Pacific | 2014 Q4 (+84 %) and 2015 Q1 (+38 %) | **No, a temporary spike:** 2015 Q4 −36 %, 2016 Q1 −16 %; calendar years $633 m → $810 m → $746 m → $707 m | Probably Disney *Frozen* toys and costumes (holiday 2014). No acquisition is tagged in the SEC data for 2013–2015 | "no acquisition" **confirmed** (SEC data); *Frozen* **from memory** (no JAKKS 10-K downloaded) |

## Logitech from 2015 Q1: not clean

- Restated ("latest") values: Jan–Mar 2015 and Jan–Mar 2016 are distorted by −17 % and +11 % (the seam above), and the 2015 Q2–Q3 quarters are restated (−4 to −5 %) while 2015 Q4 is not.
- First-reported values: no seam inside a fiscal year, but they include Lifesize until it was sold (late 2015), so the series drops by about 4–6 % at the end of 2015, in the middle of the pre-period.
- Either way the series has a break inside 2015 Q1–2017 Q2, so by your rule Logitech is **out**. (A clean series would need the quarterly numbers without Lifesize typed in by hand from the 10-Qs.)

## What this means for the 2015 start

- Columbia: both 2014 events are fully in the numbers by 2015 Q1 (prAna was bought in mid-2014), so its level is comparable from 2015 Q1. Its 2015 growth (+13 to +17 %) still partly includes prAna against quarters before the purchase, but the index compares levels, not growth.
- Deckers: no known event after July 2014; clean from 2015 Q1.
- JAKKS: the *Frozen* spike still lifts 2015 Q1 (index about 119 against 2016 Q1). The JAKKS twin will be harder to fit in the first pre-period quarter.

## How Claude's prediction did

1. Columbia (lasting step up, starts 2014 Q1, causes China JV and prAna, 10-K confirms prAna): **right**, and the 10-K confirms both.
2. Deckers (organic growth, lasting; year-end change only relabels): **partly right**. The level lasts and the year-end change is confirmed, but there was also an acquisition I did not know about (the German UGG distributor, July 2014).
3. Logitech (seam from Lifesize; clean from 2015 Q1): seam **right**; "clean from 2015 Q1" **wrong**. The seam reaches into 2015 and 2016.
4. JAKKS (spike in 2014 Q3–Q4 that does not last, no acquisition): **mostly right**. The spike is in 2014 Q4 and 2015 Q1, not Q3.
