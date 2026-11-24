"""The companies in this project and their SEC ID numbers (CIKs).

A CIK is the SEC's ID number for a company, always written with 10 digits.
Treated = sold a lot through Toys "R" Us (share of sales in brackets).
Candidates = possible comparison companies, still being screened
(rules in CLAUDE.md; shortlist in notes/screening_shortlist.md).
"""

TREATED = {
    "Mattel":        "0000063276",   # TRU about 11 % of sales in 2016, 8-9 % in 2017
    "Hasbro":        "0000046080",   # TRU about 9 %
    "JAKKS Pacific": "0001009829",   # TRU 11.3 % in 2017
}

# Approved for the download and 10-K screen on 24 Nov 2026.
CANDIDATES = {
    # "in" after rules 1-2
    "Garmin":              "0001121788",
    "Colgate-Palmolive":   "0000021665",
    "Clorox":              "0000021076",
    "Hershey":             "0000047111",
    # borderline
    "Helen of Troy":       "0000916789",
    "WD-40":               "0000105132",
    # extra discretionary makers
    "Logitech":            "0001032975",
    "Electronic Arts":     "0000712515",
    "iRobot":              "0001159167",
    "Deckers Outdoor":     "0000910521",
    "Columbia Sportswear": "0001050797",
    "Fossil Group":        "0000883569",
    "Escalade":            "0000033488",
}

ALL_COMPANIES = {**TREATED, **CANDIDATES}
