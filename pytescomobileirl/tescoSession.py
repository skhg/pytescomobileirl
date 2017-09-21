#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from . import Balances
from . import Usage

class TescoSession:

    def __init__(self):
        self.__base_url = "https://my.tescomobile.ie/tmi-selfcare-web/"
        self.__login_url = self.__base_url+"j_spring_security_check"
        self.__logout_url = self.__base_url+"j_spring_security_logout"
        self.__balance_url = self.__base_url+"rest/customer/v2/balance"
        self.__usage_url = self.__base_url+"rest/usage/1/"

        self.__session = requests.session()

    def login(self, phone_num, password):
        login_details = {'j_username': phone_num, 'j_password': password}

        try:
            login_result = self.__session.post(self.__login_url, data=login_details)
        except:
            return False

        return login_result.ok

    def logout(self):
        self.__session.get(self.__logout_url)
        self.__session.close()

    def get_balances(self):
        json_balances = self.__session.get(self.__balance_url).content

        return Balances(json_balances)

    def get_usage(self, limit=20):
        json_usage_record = self.__session.get(self.__usage_url+str(limit)).content

        return Usage(json_usage_record)