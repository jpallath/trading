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


def determineAllowance(upgrade, balance, length):
    ratio = min(.25, 1 / length)
    upgrade.allowance = balance * ratio
    print(upgrade.allowance)


def main():
    myfile = open('available_bots.txt', 'r')
    upgrades = []
    for line in myfile:
        data = line.split(",")
        upgrade = Upgrades(data[0], data[2], data[3], data[4])
        upgrade.generateFromText(data[0], data[1], data[5], data[6])
        upgrades.append(upgrade)

    trader = Watch_Bot()
    balance = trader.get_account_balance()

    for up in upgrades:
        determineAllowance(up, balance, len(upgrades))
    trader.buyStocks(upgrades)


main()