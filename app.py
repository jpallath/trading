from processData import processData, Upgrades

data = [
    "Analyst Rating Changes",
    "Since Close of Previous Session",
    "Upgrades",
    "LULU US Lululemon Raised to Overweight at Wells Fargo; PT $380",
    "SFIX US Stitch Fix Raised to Equal Weight at Wells Fargo; PT $4",
    "Downgrades",
    "BBWI US Bath & Body Works Cut to Equal-Weight at Wells Fargo; PT $46",
    "REAL US RealReal Cut to Equal-Weight at Wells Fargo; PT $2",
    "ULTA US Ulta Beauty Cut to Underweight at Wells Fargo; PT $400",
    "VFC US VF Corp Cut to Underweight at Wells Fargo; PT $24",
]


todays_longs = processData(data)[0]
