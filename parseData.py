import ibapi
from ibapi.client import EClient
from ibapi.wrapper import EWrapper, TickerId, TickType, TickAttrib

from ibapi.contract import Contract
from ibapi.order import *

import threading
import time as t
import pandas

from processData import Upgrades, processData
import schedule
import pytz
from datetime import datetime, time

from bot import IBApi, Watch_Bot


def above_fifteen(market, target):
    if ((target / market) - 1 >= .15): return True
    return False


def filter_and_reorder(bots):
    bots.sort(key=lambda bot: bot.premium)
    if len(bots) > 10:
        return [bots[:10], bots[10:]]
    return [bots, []]


def generateAvailableBotsFile(available):
    myfile = open('available_bots.txt', 'w')
    for x in available:
        fileLine = (
            f'{x.ticker},{x.interest},{x.weight},{x.analyst},{x.price_target},{x.current_price},{x.premium},\n'
        ).replace(" ", "")
        myfile.write(fileLine)


def generateFilteredBotsFile(filtered):
    myfile = open('filtered_bots.txt', 'w')
    for x in filtered:
        fileLine = (
            f'{x.ticker}, {x.interest}, {x.weight}, {x.analyst},{x.price_target},{x.current_price},{x.premium}, \n'
        ).replace(" ", "")
        myfile.write(fileLine)

    myfile.close()


def main(data):

    available_bots = []
    filtered_data = []

    watchBot = Watch_Bot()

    for x in data[0]:
        x.current_price = watchBot.get_current_price(x)
        x.premium = x.price_target / x.current_price - 1
        if above_fifteen(x.current_price, x.price_target):
            available_bots.append(x)
        else:
            filtered_data.append(x)

    [available_bots,
     filtered_data_bots_plus] = filter_and_reorder(available_bots)

    filtered_data.extend(filtered_data_bots_plus)

    generateAvailableBotsFile(available_bots)
    generateFilteredBotsFile(filtered_data)
    watchBot.end()


# todaysLongs = processData(data=[
#     "Upgrades",
#     "AWI US Armstrong World Raised to Inline at Evercore ISI; PT $80",
#     "CARR US Carrier Global Raised to Buy at Mizuho Securities; PT $53",
#     "CHCT US Community Healthcare Trust Raised to Buy at Janney Montgomery",
#     "TRU US TransUnion Raised to Overweight at Wells Fargo; PT $88",
# ])[0]

# main(todaysLongs)

# schedule_buy_jobs(available_bots)
# new_york_time = pytz.timezone("America/New_York")
# exit_time = time(9, 36)
# while True:
#     schedule.run_pending()
#     time.sleep(1)
#     if datetime.now(new_york_time).time() > exit_time:
#         break

# schedule_sell_jobs(available_bots)
# sell_exit_time = time(10, 45)
# while True:
#     schedule.run_pending()
#     time.sleep()
#     if datetime.now(new_york_time).time() > sell_exit_time:
#         break

# make this a cron job!
# 9:32AM - 9:36AM

# sell 10:30am -> 10:45am


def buy_job(bots):
    for y in bots:
        y.buy_stocks()


def schedule_buy_jobs(bots):
    new_york = pytz.timezone("America/New_York")
    schedule.every().day.at("9:32").do(buy_job).using(new_york)


def sell_stocks(bots):
    for y in bots:
        y.sell_stocks()


def schedule_sell_stocks(bots):
    new_york = pytz.timezone("America/New_York")
    schedule.every().day.at("10:30").do(sell_job).using(new_york)
