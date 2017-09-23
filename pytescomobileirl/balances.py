#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from datetime import datetime
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

    def __create_summary_balance(self, svc_type, unit, remaining_total, max_expiry):
        formatted_expiry = max_expiry.strftime("%d-%b-%Y %H:%M")

        dummyBalanceJson = """
        {
    "balance" : """+str(remaining_total)+""",
    "expiryDate" : \""""+formatted_expiry+"""\",
    "serviceBundle" : {
      "name" : "Summary",
      "paymentProfile" : null,
      "serviceCode" : "Summary",
      "recurring" : false,
      "allowance" : """+ str(remaining_total) +""",
      "type" : \"""" + svc_type + """\",
      "unit" : \""""+ unit + """\",
      "charge" : 0.0,
      "status" : "ACTIVE",
      "serviceParameters" : { }
    },
    "optin" : true,
    "visible" : null
  }"""

        loadedJson = json.loads(dummyBalanceJson)

        return self.__create_svc(loadedJson)

    def remaining_total(self, svc_type):
        
        balances_available = list(self.active_balances(svc_type))

        if(len(balances_available)) is 0:            
            return self.__create_summary_balance(svc_type, "unit", 0.0, datetime.now())
        elif(len(balances_available)) is 1:
            return balances_available[0]
        else:
            total = 0.0
            max_expiry = datetime.now()
            unit = ""

            for bal in self.active_balances(svc_type):
                total += bal.remaining_qty
                unit = bal.unit
                max_expiry = max(max_expiry,bal.balance_expires)

            return self.__create_summary_balance(svc_type, unit, total, max_expiry)

