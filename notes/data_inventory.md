# Data inventory (Session 1, 24 Nov 2026)

What the sister project `~/Documents/ai-fpa-forecast` already has, checked with `src/inventory_sister_data.py` (reads only; changes and downloads nothing). Its quarterly table is `data/processed/revenue_quarterly.csv` there, built from SEC "companyfacts" files in its `data/raw/`.

## 1. Are the treated companies there?

| Company | Raw SEC file | Quarterly revenue table |
|---|---|---|
| Mattel (CIK 0000063276) | yes | yes |
| Hasbro (CIK 0000046080) | yes | yes |
| JAKKS Pacific (CIK 0001009829) | **no** in the sister project; downloaded here on 24 Nov 2026 (`data/raw/CIK0001009829.json`) | not built yet; all 28 quarters available (see below) |

## 2. Quarterly revenue 2013 Q1 – 2019 Q4 (28 quarters)

- **Mattel: 28 of 28.** December year end, calendar quarters. Tags: `SalesRevenueNet` up to 2017, `RevenueFromContractWithCustomerExcludingAssessedTax` from 2018 (the new revenue standard, ASC 606). First-reported and latest revenue differ by at most 0.47 % (2018 Q2).
- **Hasbro: 28 of 28.** Year of 52/53 weeks ending on the last Sunday of December, so Q1 can end on 1 or 2 April. **2017 Q1 has 14 weeks (98 days)** instead of 13: its index vs 2016 Q1 is about 1/13 ≈ 8 % too high from the extra week alone. No restatements in the window.
- All 20 companies have 28 of 28, except Best Buy (27; the sister project starts it in May 2013 after a year-end change). It is a retailer, so it is not used anyway.
- Calendar quarter rule used here: a fiscal quarter goes to the calendar quarter whose end is nearest its own end date. (My first run used "the quarter it ends in", which wrongly showed Hasbro and Cummins with gaps because their Q1 ends in early April.)

### JAKKS Pacific (downloaded 24 Nov 2026)

- December year end, calendar quarters. **28 of 28 quarters** 2013–2019, all tagged directly (Q4 included), and the four quarters add up exactly to the full year every year. No restatements.
- Tags: `SalesRevenueNet` 2013 Q1–2018 Q4, then `RevenueFromContractWithCustomerExcludingAssessedTax` (2019, and overlapping from 2017 Q2 with identical values).
- **Do not use the `Revenues` tag for 2013–2015**: it is about half of net sales (e.g. $302 m vs $633 m in 2013), so it is a part of revenue, not the total.
- Full-year net sales ($ m): 2013 632.9, 2014 810.1, 2015 745.7, 2016 706.6, 2017 613.1, 2018 567.8, 2019 598.6.
- Listed with `src/list_revenue_quarters.py "JAKKS Pacific"`.

## 3. Segment revenue (North America / US & Canada)?

**Not available in the existing data.** The companyfacts files hold only facts *without* XBRL dimensions and *without* company-specific (custom) tags. Segment and geographic revenue are tagged with dimensions (e.g. a "segment" axis with a "North America" member), so they are left out. Searching the Mattel and Hasbro files for regional or segment tag names found nothing usable (one stray Hasbro `RevenuesFromExternalCustomers` quarter).

Ways to get it (each is a download, so not done):
- (a) The XBRL files of each 10-Q and 10-K for 2013–2019 from EDGAR's filing archive: about 28 filings per company. They contain the dimensional segment facts.
- (b) The SEC's "Financial Statement and Notes" data sets (one large zip per quarter, all companies, includes dimensions). Heavier, but one format for everybody.

Segment names also changed over time at some companies, so a segment series needs checking by hand against the 10-Ks.

## 4. Which of the 20 are consumer-products companies?

| Company | Fits the donor-pool rule? | Why |
|---|---|---|
| Mattel, Hasbro | treated | toy makers, sold through TRU |
| Procter & Gamble | **yes** (candidate) | household and personal-care brands sold through big-box retail; June year end, but its quarters end in Sept/Dec/Mar/June = calendar quarters |
| Colgate-Palmolive | **yes** (candidate) | December year end |
| Clorox | **yes** (candidate) | June year end, calendar-aligned quarters |
| Church & Dwight | **yes** (candidate) | December year end |
| General Mills | **yes** (candidate) | May year end: quarters end Aug/Nov/Feb/May, one month off the calendar |
| Williams-Sonoma, Best Buy, Macy's | no | retailers, not makers selling through retailers. They could also have *gained* from TRU's closing (shoppers moving to other stores), which would break the "no spillover" assumption (SUTVA, Mixtape Ch 4). |
| the other 10 | no | tech and industrial |

So **5 usable comparison companies**, against a target of 15–25. All 5 still need the 10-K check that they do not name Toys "R" Us or Babies "R" Us as a customer. P&G sold baby products (Pampers) that Babies "R" Us stocked, so it deserves a careful look.

## 5. What would need downloading (waiting for your yes)

1. ~~JAKKS Pacific companyfacts file~~: **done 24 Nov 2026** (CIK 0001009829 confirmed by the SEC name in the file).
2. **Companyfacts for 10–20 more comparison candidates**, then the 2016 and 2017 10-K text of every candidate to search for "Toys R Us" / "Babies R Us". A first list to screen (not decided; you pick):
   Kimberly-Clark, Edgewell Personal Care, Energizer (check history: spun off in 2015), Spectrum Brands, Central Garden & Pet, Helen of Troy, WD-40, Prestige Consumer Healthcare, Kellogg, Hershey, Campbell Soup, J.M. Smucker, Conagra, McCormick, Mondelez, Hormel, Garmin, Nautilus, Johnson Outdoors, Lifetime Brands.
   Left out on purpose: **Kraft Heinz** (your rule), companies listed after 2013 (Funko, GoPro, Fitbit, Hamilton Beach Brands: no full 2013–2019 data), and makers that likely named TRU/BRU as a big customer (Newell Brands, Summer Infant, Crown Crafts).
3. **Segment revenue** (optional, decide later): option (a) or (b) above, for the treated companies at least.

## How Claude's prediction did

1. JAKKS missing: **right**.
2. Mattel and Hasbro complete: **right** (after fixing my calendar-quarter rule; the first run looked wrong for Hasbro).
3. No usable segment revenue: **right**; there are no custom tags at all in companyfacts.
4. 5 usable comparison companies: **right**.
5. "P&G, Clorox and General Mills are off-calendar": **partly wrong**. P&G and Clorox have June year ends, but their quarters still end on calendar quarter ends; only General Mills is one month off.
