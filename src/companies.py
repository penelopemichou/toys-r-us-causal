"""The companies in this project and their SEC ID numbers (CIKs).

A CIK is the SEC's ID number for a company, always written with 10 digits.
Treated = sold a lot through Toys "R" Us (share of sales in brackets).
Comparison companies will be added after the 10-K screen.
"""

TREATED = {
    "Mattel":        "0000063276",   # TRU about 11 % of sales in 2016, 8-9 % in 2017
    "Hasbro":        "0000046080",   # TRU about 9 %
    "JAKKS Pacific": "0001009829",   # TRU 11.3 % in 2017
}

COMPARISON = {}

ALL_COMPANIES = {**TREATED, **COMPARISON}
