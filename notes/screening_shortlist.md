# Comparison companies: shortlist after rules 1–2 (24 Nov 2026)

**Status: before any download.** Rules 1 and 2 (in `CLAUDE.md`) applied from Claude's own knowledge of each company's history. Every fact below is still to be checked: rule 2's "full quarterly data 2013 Q1–2019 Q4" in the SEC file, rule 3 (Toys "R" Us / Babies "R" Us named as a customer) in the 2016 and 2017 10-Ks. Revenue jumps are rough sizes (share of annual revenue).

Screened: the 20 candidates from `notes/data_inventory.md` plus the 5 consumer companies already in the ai-fpa-forecast set.

## In (go to the download and 10-K screen)

| Company | Type | Why in | Watch out |
|---|---|---|---|
| Garmin | discretionary | GPS watches, fitness and car devices; holiday (Q4) peak; sold through Best Buy, Amazon, Walmart; no big acquisition | 52/53-week year (like Hasbro): check for 14-week quarters |
| Colgate-Palmolive | staple 1 | no big acquisition or spin-off; December year end | mostly international (about 80 %): strong currency effects |
| Clorox | staple 2 | acquisitions small (Renew Life 2016, Nutranext 2018, about 3 % each) | June year end, but quarters end on calendar quarter ends |
| Hershey | staple 3 | chocolate; Halloween and holiday peak (Q3–Q4); sold mainly through big-box and grocery | Amplify Snack (Jan 2018, about 5 %): borderline, check the size |

## Borderline (your call)

| Company | Why borderline |
|---|---|
| Helen of Troy | discretionary (OXO, Hydro Flask, Braun, Honeywell fans), holiday peak, Walmart/Amazon. But Hydro Flask (March 2016) added roughly 10–15 %, and its year ends in February, so quarters end May/Aug/Nov/Feb (two months off the calendar). |
| WD-40 | no acquisitions, steady data. But no Q4 peak, sold a lot through hardware/auto stores and about half abroad, so a weak fit for rule 1. |

## Out

| Company | Rule | Reason |
|---|---|---|
| Kimberly-Clark | 2 | spun off Halyard Health (Oct 2014, about 8 % of revenue); also Huggies were a Babies "R" Us product |
| Edgewell Personal Care | 2 | the old Energizer Holdings; spun off the battery business in 2015 (revenue about halved) |
| Energizer Holdings | 2 | new company from the 2015 spin-off (no 10-Qs before 2015); bought Spectrum's batteries and auto care in 2019 |
| Spectrum Brands | 2 | merged with HRG Group (2018); sold batteries (2019); Armored AutoGroup (2015) |
| Central Garden & Pet | 1, 2 | spring/summer peak (garden); several acquisitions |
| Prestige Consumer Healthcare | 2 | Insight (2014), DenTek (2016), C.B. Fleet (2017, about +30 %) |
| Kellogg | 2 | sold Keebler cookies (2019) |
| Campbell Soup | 2 | Snyder's-Lance (2018, about +30 %) |
| J.M. Smucker | 2 | Big Heart Pet Brands (2015, about +40 %), Ainsworth (2018) |
| Conagra | 2 | spun off Lamb Weston (2016), bought Pinnacle Foods (2018) |
| McCormick | 2 | RB Foods / French's (Aug 2017, about +10 %), right at the treatment date |
| Mondelez | 2 | coffee business moved to JDE (2015, a large drop) |
| Hormel | 1, 2 | much of its sales go to foodservice, not big-box; several acquisitions (Applegate 2015, Justin's 2016, Columbus 2017) |
| Nautilus | 2 | Octane Fitness (Dec 2015, about +30 %) |
| Johnson Outdoors | 1 | fishing and camping: spring/summer peak, not Q4 |
| Lifetime Brands | 2 | Filament Brands / Wilton (2018, about +30–40 %) |
| Procter & Gamble | 1, 2 | staple cap reached; also sold Duracell (2016) and beauty brands to Coty (2016), with restatements up to 13 % |
| Church & Dwight | 1, 2 | staple cap reached; Water Pik (Aug 2017, about +8 %) right at the treatment date |
| General Mills | 1, 2 | staple cap reached; Blue Buffalo (2018, about +8 %); quarters one month off the calendar |

## The problem: too few

That leaves **4 in + 2 borderline = 4–6 companies**, far below the 15–25 target. With 6 comparison companies the smallest possible placebo p-value is 1/7 ≈ 0.14, so a placebo test could never reject at 10 %.

The original list of 20 was too heavy on food and household staples, which rule 1 now caps at 3. **Extra discretionary makers worth screening** (same caveat: from memory, all to check):

| Company | Why it might fit | Risk to check |
|---|---|---|
| Logitech | mice, keyboards, headsets; holiday peak; Best Buy, Amazon, Walmart; files a 10-K | Lifesize spin-off (2016, restated as discontinued); small acquisitions (Jaybird 2016, Astro 2017, Blue 2018) |
| Electronic Arts | video games; holiday peak; sold through GameStop, Walmart, Amazon and online | games are a close substitute for toys (spillover risk); shift to digital sales; TRU sold video games, so check the 10-Ks |
| iRobot | Roomba; holiday peak; Amazon and big-box | bought its Japan and Europe distributors (2017), which raises reported revenue; sold its defence unit (2016) |
| Deckers Outdoor (UGG) | holiday peak; department stores, Amazon, own stores | March year end; not mainly big-box |
| Columbia Sportswear | autumn/holiday peak | department and sporting-goods stores, own stores; prAna (2014, about 5 %) |
| Fossil Group | watches; holiday peak | mostly department stores and own shops, not big-box |
| Escalade | sporting goods and indoor games; big-box | small company; may well have sold through TRU (check carefully) |

Already ruled out from this group: GoPro, Fitbit, Funko, Sonos, Roku, Yeti, Hamilton Beach Brands, Vista Outdoor (listed after 2013); Netgear (Arlo spin-off 2018); Activision (King, 2016); Take-Two (lumpy release years); ZAGG (mophie, 2016); Turtle Beach (2014 merger); Skullcandy (taken private 2016); Newell, Summer Infant, Crown Crafts, Carter's (likely named TRU/BRU as a customer).

Even with all seven extras, the pool would be about 11–13 before rule 3 removes anyone.

## What the download would be (waiting for your yes)

For each company you approve: 1 companyfacts JSON from `data.sec.gov` (1–5 MB), plus its 2016 and 2017 10-K main documents from the SEC archive (about 1–3 MB each), so about 3 files per company. Saved to `data/raw/` (companyfacts) and `data/raw/10k/` (10-Ks), both gitignored. At 2 requests per second it takes under a minute.
