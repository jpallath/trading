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


class IBApi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def error(self, reqId: TickerId, errorCode: int, errorString: str):
        print("Error: ", reqId, " ", errorCode, " ", errorString)

    def tickPrice(
        self, reqId: TickerId, tickType: TickType, price: float, attrib: TickAttrib
    ):
        if tickType == 4:
            self.price = price

    # def realtimeBar(self, reqId, time, open_, high, low, close, volume, wap, count):
    #     bot.on_bar_update(reqId, time, open_, high, low, close, volume, wap, count)


class Bot:
    ib = None

    def __init__(self, upgrade):
        self.ib = IBApi()
        self.ib.connect("127.0.0.1", 7497, 1)
        ib_thread = threading.Thread(target=self.run_loop, daemon=True)
        ib_thread.start()
        t.sleep(1)
        self.ids = []
        self.ticker = upgrade.ticker
        self.interest = upgrade.interest
        self.weight = upgrade.weight
        self.analyst = upgrade.analyst
        self.price_target = upgrade.price_target
        # the openprice is 15% above print
        # PT/stockPrice - 1
        # 115

    def run_loop(self):
        self.ib.run

    def determine_price_targets(self):
        tickerId = self.ticker + str(len(self.ids))
        self.ids.append(tickerId)

        contract = Contract()
        contract.symbol = self.ticker
        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.currency = "USD"
        t.sleep(3)

        try:
            # put 9:31
            value = self.ib.reqMktData(tickerId, contract, "", False, True, [])
            # (1000, a, "", True, False, [])
            # self.ib.reqMktData
            print(self.ticker)
            print(value)
            if (self.price_target / value) - 1 > 0.15:
                self.premium = (self.price_target / value) - 1
                return True
        except Exception:
            return False

        return False

    def buy_stocks(self, symbol):

        tickerId = self.ticker + str(len(self.ids))
        self.ids.append(tickerId)
        order = Order()
        order.orderType = "MKT"
        order.action = "BUY"
        # quantity = #total/len(available_tickers)/price of stock
        # order.totalQuantity = quantity
        # add accountbalance/len(available_tickers)

        contract = Contract()
        contract.symbol = symbol.upper()
        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.currency = "USD"
        # self.ib.placeOrder(tickerId, contract, order,9:32, 9:36)  # <-- make this TWAP
        # when returned get number of tickers

    def sell_stocks(self, symbol):
        # call to see how many shares of stock of we have on this bot
        tickerId = self.ticker + str(len(self.ids))
        self.ids.append(tickerId)
        order = Order()
        order.orderType = "MKT"
        order.action = "SELL"
        # quantity = 1
        # order.totalQuantity = quantity
        # sell stocks that we actually own

        # a check to determine if we have total shares

        contract = Contract()
        contract.symbol = symbol.upper()
        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.currency = "USD"
        # self.ib.placeOrder(tickerId, contract, order, 10:30, 11:00) # Make this TWAP

    # def on_bar_update(self, reqId, time, open_, high, low, close, volume, wap, count):
    #     print(reqId)


def main(data):
    accountBalance = getAccountBalance

    available_bots = []

    # i need to make a check if the available bots go over 10 bots, need logic to cut this
    # if over 15% keep if not drop but send in account email summary
    for x in todaysLongs:
        bot = Bot(x)
        above_fifteen = bot.determine_price_targets()
        # above_fifteen = loop.run_until_complete(bot.determine_price_targets())
        if above_fifteen:
            available_bots.append(bot)

    # reorder and filter
    available_bots = filter_and_reorder(available_bots)

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


def getAccountBalance():
    values = ib.accountValues()

    for v in values:
        if v.tag == "CashBalance" and v.currency == "BASE":
            total = v.value

    return total


def filter_and_reorder(bots):
    bots.sort(key=lambda bot: bot.premium)
    if len(bots) > 10:
        return bots[:10]
    return bots


todaysLongs = processData(
    data=[
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
)[0]

main(todaysLongs)
