# 14-week quarters (53-week years), 2013–2019 (24 Nov 2026)

Made with `src/scan_53_weeks.py`: quarter start and end dates from the SEC data (13 weeks = 90 days from start to end date, 14 weeks = 97), plus a search of the fiscal 2016–17 10-Ks already on disk. Nothing downloaded.

| Company | 14-week quarter | Evidence |
|---|---|---|
| Hasbro | 2017 Q1 (26 Dec 2016 – 2 Apr 2017) | dates (97 days; fiscal 2017 = 370 days). No Hasbro 10-K on disk. |
| Garmin | 2016 Q4 (25 Sep – 31 Dec 2016), **a base quarter** | dates (97 days) and 10-K: "Fiscal year 2016 contains 53 weeks" |
| Fossil Group | 2014 Q1 (29 Dec 2013 – 5 Apr 2014) | dates (97 days) and 10-K: fiscal 2014 had 53 weeks, "with the additional week included in the first quarter" |
| Electronic Arts | 2015 Q2 (fiscal Q1 2016, Apr–Jun 2015) | **10-K only**: fiscal 2016 "contained 53 weeks", and the June 2016 quarter had "13 weeks … as compared to 14 weeks in the prior fiscal year". EA dates its quarters by calendar month ends, so the SEC dates show 91 days. |

None for Mattel, JAKKS, Colgate, Clorox, WD-40, Deckers and Columbia (their quarters end on calendar month ends: 89–92 days). Hershey's quarters run 87–94 days because they end on Sundays inside a calendar year ending 31 December. That is a few days, not an extra week, so they are not adjusted.

Limit: for Mattel, Hasbro and JAKKS we have no 10-Ks on disk, so we rely on the dates alone. A company that labels its quarters by month end (as EA does) could hide a 14-week quarter from the dates. Mattel's and JAKKS's fiscal years are calendar years, so this cannot happen for them; Hasbro's dates are true week ends.

All four are scaled by 13/14 in the main run (`FOURTEEN_WEEK_QUARTERS` in `src/build_index.py`); the unadjusted index is kept as `index_unadjusted`.

## How Claude's prediction did

Four 14-week quarters (Hasbro 2017 Q1, Garmin 2016 Q4, Fossil 2014 Q1, one at EA): **right**. None at the calendar-month companies and Hershey's 93–94 days not an extra week: **right**. "Only Garmin's 10-K mentions 53 weeks": **wrong**, Fossil's and EA's do too. And I did not foresee that EA's dates would hide its 14-week quarter.
