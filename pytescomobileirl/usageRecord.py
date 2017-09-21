#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
import json
import pprint

class UsageRecord:

    def __init__(self, record):
		self.service_name = record["serviceName"]
		self.service_code = record["serviceCode"]
		self.event_date = datetime.strptime(record["eventDate"], "%d-%b-%Y %H:%M")
		self.called_number = record["calledNumber"]
		self.country_code = record["countryCode"]
		self.volume = record["volume"]
		self.unit = record["volumeUnit"]
		self.charge = record["charge"]
		self.use_type = record["type"]
		self.roaming = record["roaming"]