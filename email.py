# three tables

# first
# actual stocks we ordered
# entry price, analyst, price target, new rating, stock price at 9 31, premium, entry price, exit price, entry quantity, exit quantity, PNL (sell/entry)-1 (sell/entry)-1*quantity

# second
# rest of upgrades
# list of stocks that didnt make list
# analyst, pt, rating, stock price at 9 31, premium, twap (get historical twap between 9:32:36), twap sell, PNL (sell/entry)-1 (sell/entry)-1*quantity

# third
# shorts
# one table for all downgrades
# analyst, pt, rating, stock price at 9 31, premium, twap (get historical twap between 9:32:36), twap sell, PNL -(sell/entry)-1 -(sell/entry)-1*quantity


# premium for shorts is
# -(sell - entry)


from ibapi.client import EClient
from ibapi.wrapper import EWrapper, TickerId, TickType, TickAttrib
from ibapi.contract import Contract


class TestApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.price = None

    def error(self, reqId: TickerId, errorCode: int, errorString: str):
        print("Error ", reqId, " ", errorCode, " ", errorString)

    def tickPrice(
        self, reqId: TickerId, tickType: TickType, price: float, attrib: TickAttrib
    ):
        print("hello")
        if tickType == 4:
            self.price = price
            self.disconnect()


app = TestApp()
app.connect("127.0.0.1", 7497, 0)

contract = Contract()
contract.symbol = "SFIX"
contract.secType = "STK"
contract.exchange = "SMART"
contract.currency = "USD"

app.reqMktData(10, contract, "", False, False, [])
app.run()

print("SFIX stock price: ", app.price)
