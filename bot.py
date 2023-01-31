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


class IBApi(EWrapper, EClient):

    def __init__(self):
        EClient.__init__(self, self)
        self.balance = None
        self.done = False
        self.price = None

    def error(self, reqId: TickerId, errorCode: int, errorString: str):
        print("Error: ", reqId, " ", errorCode, " ", errorString)

    def tickPrice(self, reqId: TickerId, tickType: TickType, price: float,
                  attrib: TickAttrib):
        if tickType == 2:
            self.price = price

    def accountSummary(self, reqId, account, tag, value, currency):
        if tag == "TotalCashValue":
            self.balance = float(value)
            self.done = True
            return self.balance

    # def realtimeBar(self, reqId, time, open_, high, low, close, volume, wap, count):
    #     bot.on_bar_update(reqId, time, open_, high, low, close, volume, wap, count)


class Watch_Bot:

    def __init__(self):
        self.ib = IBApi()
        self.ib.connect("127.0.0.1", 7497, 1)
        self.reqId = 0
        t.sleep(1)

    def run_loop(self):
        self.ib.run

    def currentReqId(self):
        self.reqId = self.reqId + 1
        return self.reqId

    def get_account_balance(self):
        reqId = self.currentReqId()
        self.ib.reqAccountSummary(reqId, "All", "TotalCashValue")
        thread = threading.Thread(target=self.ib.run, daemon=True)
        thread.start()
        while not self.ib.balance:
            t.sleep(1)
        return self.ib.balance

    def determine_price_targets(self, upgrade):
        reqId = self.currentReqId()
        contract = Contract()
        contract.symbol = upgrade.ticker
        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.currency = "USD"

        self.ib.reqMarketDataType(2)
        self.ib.reqMktData(reqId, contract, '', False, False, [])

        thread = threading.Thread(target=self.ib.run, daemon=True)
        thread.start()
        while not self.ib.price:
            t.sleep(1)

        response = self.ib.price
        self.ib.price = None
        return response


# class Bot:
#     ib = None

#     def __init__(self, upgrade):
#         self.ib = IBApi()
#         self.ib.connect("127.0.0.1", 7497, 1)
#         # ib_thread = threading.Thread(target=self.run_loop, daemon=True)
#         # ib_thread.start()
#         t.sleep(1)
#         self.ids = []
#         self.ticker = upgrade.ticker
#         self.interest = upgrade.interest
#         self.weight = upgrade.weight
#         self.analyst = upgrade.analyst
#         self.price_target = upgrade.price_target
#         # the openprice is 15% above print
#         # PT/stockPrice - 1
#         # 115

#     def run_loop(self):
#         self.ib.run

#     def determine_price_targets(self, numberId):
#         reqId = numberId + 9
#         contract = Contract()
#         contract.symbol = self.ticker
#         contract.secType = "STK"
#         contract.exchange = "SMART"
#         contract.currency = "USD"

#         self.ib.reqMarketDataType(2)
#         self.ib.reqMktData(reqId, contract, '', False, False, [])

#         thread = threading.Thread(target=self.ib.run, daemon=True)
#         thread.start()
#         while True:
#             t.sleep(5)
#             print(self.ticker)
#             print(self.ib.price)

#         # try:
#         # put 9:31
#         # t.sleep(10)

#         # while not self.ib.done:
#         #     self.ib.run()

#         # (1000, a, "", True, False, [])
#         # self.ib.reqMktData
#         # if (self.price_target / value) - 1 > 0.15:
#         #     self.premium = (self.price_target / value) - 1
#         #     return True
#         # except Exception:
#         #     print(Exception)
#         #     return False

#         return False

#     def buy_stocks(self, symbol):

#         tickerId = self.ticker + str(len(self.ids))
#         self.ids.append(tickerId)
#         order = Order()
#         order.orderType = "MKT"
#         order.action = "BUY"
#         # quantity = #total/len(available_tickers)/price of stock
#         # order.totalQuantity = quantity
#         # add accountbalance/len(available_tickers)

#         contract = Contract()
#         contract.symbol = symbol.upper()
#         contract.secType = "STK"
#         contract.exchange = "SMART"
#         contract.currency = "USD"
#         # self.ib.placeOrder(tickerId, contract, order,9:32, 9:36)  # <-- make this TWAP
#         # when returned get number of tickers

#     def sell_stocks(self, symbol):
#         # call to see how many shares of stock of we have on this bot
#         tickerId = self.ticker + str(len(self.ids))
#         self.ids.append(tickerId)
#         order = Order()
#         order.orderType = "MKT"
#         order.action = "SELL"
#         # quantity = 1
#         # order.totalQuantity = quantity
#         # sell stocks that we actually own

#         # a check to determine if we have total shares

#         contract = Contract()
#         contract.symbol = symbol.upper()
#         contract.secType = "STK"
#         contract.exchange = "SMART"
#         contract.currency = "USD"
#         # self.ib.placeOrder(tickerId, contract, order, 10:30, 11:00) # Make this TWAP

#     # def on_bar_update(self, reqId, time, open_, high, low, close, volume, wap, count):
#     #     print(reqId)