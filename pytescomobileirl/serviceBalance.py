#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
import sys


class ServiceBalance:

    def __init__(self, basic_data, adv_data, remaining_qty):
        self.balance_type = adv_data["type"]
        self.is_active = adv_data["status"] == "ACTIVE"
        self.serviceCode = adv_data["serviceCode"]
        self.remaining_qty = remaining_qty
        self.name = adv_data["name"]

        if basic_data["expiryDate"] is not None:
            self.balance_expires = datetime.strptime(basic_data["expiryDate"], "%d-%b-%Y %H:%M")
        else:
            self.balance_expires = None

    def days_remaining(self):
        if self.has_expiry():
            now = datetime.now()
            return int(round(((self.balance_expires) - now).days))
        else:
            return sys.maxsize

    def has_expiry(self):
        return self.balance_expires is not None

    def summary(self):
        return "{:,.0f}".format(self.remaining_qty) + " " + self.unit


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

    def summary(self):
        if self.remaining_qty > 1000:
            return "{:,.2f} GB".format(self.remaining_qty / 1024)
        else:
            return "{:,.0f} MB".format(self.remaining_qty)


class VoiceBalance(ServiceBalance):

    def __init__(self, basic_data, adv_data):
        self.unit = "Min"
        ServiceBalance.__init__(self, basic_data, adv_data, basic_data["balance"])


class TextBalance(ServiceBalance):

    def __init__(self, basic_data, adv_data):
        self.unit = "Msg"
        ServiceBalance.__init__(self, basic_data, adv_data, basic_data["balance"])
