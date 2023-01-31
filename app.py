from processData import processData, Upgrades

data = [
    "Upgrades",
    "AWI US Armstrong World Raised to Inline at Evercore ISI; PT $80",
    "CARR US Carrier Global Raised to Buy at Mizuho Securities; PT $53",
    "CHCT US Community Healthcare Trust Raised to Buy at Janney Montgomery",
    "TRU US TransUnion Raised to Overweight at Wells Fargo; PT $88",
]


# todays_longs = processData(data)[0]

updata = processData(data)

