from processData import processData, Upgrades
from parseData import main
import csv
import datetime

data = []
with open(f'market_data/{datetime.date.today()}.csv') as file:
    csv_reader = csv.reader(file, delimiter=',')
    for row in csv_reader:
        data.append(row)

todays_longs = processData(data[1:])

main(todays_longs)
