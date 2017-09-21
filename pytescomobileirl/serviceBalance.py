#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

class ServiceBalance:

    def __init__(self, basic_data, adv_data, remaining_qty):
        self.balance_type = adv_data["type"]
        self.is_active = adv_data["status"] == "ACTIVE"
        self.serviceCode = adv_data["serviceCode"]
        self.remaining_qty = remaining_qty

        if basic_data["expiryDate"] is not None:
            self.balance_expires = datetime.strptime(basic_data["expiryDate"], "%d-%b-%Y %H:%M")
        else:
            self.balance_expires = None

    def days_remaining(self):
        now = datetime.now()
        return int(round(((self.balance_expires) - now).days))

class GenericBalance(ServiceBalance):

    def __init__(self, basic_data, adv_data):
        self.unit = adv_data["unit"]
        ServiceBalance.__init__(self, basic_data, adv_data, basic_data["balance"])

class DataBalance(ServiceBalance):

    def __init__(self, basic_data, adv_data):
        self.unit = "MByte"

        normalised_qty = self.__normalise_value(basic_data["balance"], adv_data["unit"])

        ServiceBalance.__init__(self, basic_data, adv_data, normalised_qty)

    def __normalise_value(self, start_value, unit):
        if unit == "kB":
            return start_value / 1024
        elif unit == "GByte":
            return start_value * 1024
        else:
            return start_value

class VoiceBalance(ServiceBalance):

    def __init__(self, basic_data, adv_data):
        self.unit = "Min"
        ServiceBalance.__init__(self, basic_data, adv_data, basic_data["balance"])

class TextBalance(ServiceBalance):

    def __init__(self, basic_data, adv_data):
        self.unit = "Msg"
        ServiceBalance.__init__(self, basic_data, adv_data, basic_data["balance"])
