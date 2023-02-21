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


def main():

    trader = Watch_Bot()
    balance = trader.get_account_balance()

    tickers_and_market_prices = trader.sellStock()


main()