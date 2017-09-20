import json
from . import ServiceBalance

class Balances:

    def __init__(self, json_blob):
        self.services = []
        self.__process_json(json_blob)

    def __process_json(self, json_blob):
        balance_data = json.loads(json_blob)

        self.credit_remaining = round(balance_data["mainBalance"], 2)

        for addon in balance_data["addonBalance"]:
            self.services.append(ServiceBalance(addon))

    def filter_balances(self, type):
        for bal in self.services:
            if bal.type() == type and bal.active():
                yield bal

    def data(self):
        return self.filter_balances("data")

    def text(self):
        return self.filter_balances("text")

    def voice(self):
        return self.filter_balances("voice")

    def data_remaining(self):
        data_tot = 0
        for bal in self.data():
            data_tot += bal.remaining_balance()
        return int(round(data_tot))


