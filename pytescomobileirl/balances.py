import json
from . import ServiceBalance
from .serviceBalance import DataBalance
from .serviceBalance import VoiceBalance
from .serviceBalance import TextBalance
from .serviceBalance import GenericBalance

class Balances:
    __mapping = {"data": DataBalance, "voice": VoiceBalance, "text": TextBalance }

    def __init__(self, json_blob):
        self.services = []
        self.__process_json(json_blob)

    def __process_json(self, json_blob):
        balance_data = json.loads(json_blob)

        self.credit_remaining = round(balance_data["mainBalance"], 2)

        for addon in balance_data["addonBalance"]:
            newService = self.__create_svc(addon)
            self.services.append(newService)

    def __create_svc(self, balance_data):
        adv_data = balance_data["serviceBundle"]
        serviceType = adv_data["type"]

        if serviceType in Balances.__mapping:
            return Balances.__mapping[serviceType](balance_data, adv_data)
        else:
            return GenericBalance(balance_data, adv_data)

    def active_balances(self, svc_type = None):
        for bal in self.services:
            if bal.is_active and (bal.balance_type == svc_type or svc_type is None) :
                yield bal

    def data(self):
        return self.active_balances("data")

    def text(self):
        return self.active_balances("text")

    def voice(self):
        return self.active_balances("voice")

    def remaining_total(self, svc_type):
        total = 0.0
        for bal in self.active_balances(svc_type):
            total += bal.remaining_qty
        return total

