import json

with open("constants/tickers.json", "r") as f:
    interested_tickers = json.load(f)

with open("constants/weights.json", "r") as g:
    weights = json.load(g)

with open("constants/brokers.json", "r") as h:
    brokers = json.load(h)


class Upgrades:

    def __init__(self, ticker, weight, analyst, price_target):
        self.ticker = ticker[0]
        self.interest = ticker[1]
        self.weight = weight
        self.analyst = analyst
        self.price_target = price_target
        self.current_price = None
        self.premium = 0
        self.allowance = 0

    def generateFromText(self, ticker, interest, current_price, premium):
        self.ticker = ticker
        self.interest = interest
        self.current_price = current_price
        self.premium = premium


def processData(data):
    upgrades = []
    downgrades = []
    count = 0
    current_grade = ""
    while count < len(data):
        # print(data[count])
        upgrades.append(get_terms(data[count]))
        # if data[count] == "Upgrades" or data[count] == "Downgrades":
        #     current_grade = data[count]
        # if current_grade == "Upgrades" and data[count] != "Upgrades":
        #     upgrades.append(get_terms(data[count]))
        # elif current_grade == "Downgrades" and data[count] != "Downgrades":
        #     downgrades.append(get_terms(data[count]))
        count += 1

    todays_longs = process_grades(upgrades, "upgrades")
    return [todays_longs]


def get_terms(phrase):
    [ticker, interest] = get_ticker(phrase[0], interested_tickers)
    [weight, broker] = get_broker_and_weight(phrase[1], brokers)
    price_target = get_price_target(phrase[1])
    if not price_target or weight == "HOLD":
        return

    return {
        "ticker": (ticker, interest),
        "weight": weight,
        "broker": broker,
        "price_target": price_target,
    }


def get_ticker(line, interested_tickers):
    potential_ticker = line.strip()
    for ticker in interested_tickers["tickers"]:
        if ticker == potential_ticker:
            return [ticker, True]
    return [potential_ticker, False]


def get_broker_and_weight(phrase, brokers):
    phrase = phrase.upper()

    if "EQUAL" in phrase and "EQUAL-" not in phrase:
        phrase = phrase.split(" ")
        equal_ind = phrase.index("EQUAL")
        weight_ind = phrase.index("WEIGHT")
        if equal_ind + 1 == weight_ind:
            phrase.pop(equal_ind)
            phrase.pop(equal_ind)
            phrase.append("EQUAL-WEIGHT")
        phrase = (" ").join(phrase)

    bank = None

    for key in weights:
        (found, weight) = check_weights(weights[key], key, phrase)
        if found:
            break

    broker = phrase.split("AT")[1].split(";")[0]

    return [weight, broker]


def check_weights(arr, term, phrase):
    for category in arr:
        for weight in arr[category]:
            if weight in phrase:
                return (True, category)
    return (False, None)


def get_price_target(phrase):
    if "PT $" not in phrase:
        return
    phrase = phrase.split(" ")
    return int(phrase[-1].split("$")[1])


def process_grades(arr, grade):
    options = []
    if grade == "upgrades":
        for check in arr:
            if not check:
                pass
            else:
                options.append(
                    Upgrades(
                        check["ticker"],
                        check["weight"],
                        check["broker"],
                        check["price_target"],
                    ))
    return options
