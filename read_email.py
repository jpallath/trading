import json
import boto3
import datetime
import csv

s3 = boto3.client('s3')
ses = boto3.client('ses')
bucket_name = 'coffeeandstock'
prefix = 'stocks'


def getObject():
    files = s3.list_objects(Bucket=bucket_name, Prefix=prefix)
    sorted_files = sorted(files["Contents"],
                          key=lambda x: x['LastModified'],
                          reverse=True)
    file = sorted_files[0]['Key']

    obj = s3.get_object(Bucket=bucket_name,
                        Key=file)['Body'].read().decode('utf-8')

    obj = obj.split("---------- Forwarded message ---------")[1].split(
        'Since Close of Previous Session')[1].split('\n')

    return obj


def generateCsvAndShip(arr):
    header = ['ticker', 'phrase']
    with open(f'market_data/{datetime.date.today()}.csv',
              'w',
              encoding='UTF8',
              newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        # writer.writerows(arr)
        for item in arr:
            if "PT $" not in item: continue
            writer.writerow(item.split("|"))
            # writer.writerow(f'{ticker}, {phrase}')
        return


def main():
    file = getObject()

    foundUpgrades = False
    foundDowngrades = False
    upgrades = []
    ship = []

    for line in file:
        if foundUpgrades and not foundDowngrades:
            if "Downgrades" not in line:
                upgrades.append(line)
        if "Upgrades\r" in line:
            foundUpgrades = True
        if "Downgrades\r" in line:
            foundDowngrades = True

    upgrades = [x for x in upgrades if x != "\n"]

    # print(upgrades)

    for i in range(0, len(upgrades), 3):
        if "<" in upgrades[i] and "US" in upgrades[i]:
            ticker = upgrades[i].split("<")[0].split(" ")[0]
            phrase = upgrades[i + 1]
            ship.append(f'{ticker} | {phrase}')

    generateCsvAndShip(ship)
    return


main()
