#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import logging
from . import Balances
from . import Usage


class TescoSession:

    def __init__(self):
        self.__base_url = "https://my.tescomobile.ie/tmi-selfcare-web/"
        self.__login_url = self.__base_url + "j_spring_security_check"
        self.__logout_url = self.__base_url + "j_spring_security_logout"
        self.__balance_url = self.__base_url + "rest/customer/v2/balance"
        self.__usage_url = self.__base_url + "rest/usage/1/"

        self.__session = requests.session()

    def login(self, phone_num, password):
        login_details = {'j_username': phone_num, 'j_password': password}

        logging.debug("Attempt to login")
        logging.debug(login_details)
        try:
            login_result = self.__session.post(self.__login_url, data=login_details)
            logging.debug(login_result)
        except requests.exceptions.RequestException as e:
            logging.error(e)
            return False

        return login_result.ok

    def logout(self):
        logout_result = self.__session.get(self.__logout_url)
        logging.debug(logout_result)

        self.__session.close()

    def get_balances(self):
        json_balances = self.__session.get(self.__balance_url).content
        logging.debug(json_balances)

        return Balances(json_balances)

    def get_usage(self, limit=20):
        json_usage_record = self.__session.get(self.__usage_url + str(limit)).content
        logging.debug(json_usage_record)

        return Usage(json_usage_record)
