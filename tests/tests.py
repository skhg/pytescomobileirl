#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from unittest import TestCase
import json
import types
from pytescomobileirl import *
from datetime import datetime, timedelta

sample_data_dir = "./tests/sampledata/"

class TestBalances(unittest.TestCase):

	def test_balances_init_loadsJson(self):
		with(open(sample_data_dir+"mobile_data_empty.json")) as f:
			balances = Balances(f.read())

	def test_balances_credit_remaining_matches_expected(self):
		with(open(sample_data_dir+"mobile_data_empty.json")) as f:
			balances = Balances(f.read())

			self.assertEqual(balances.credit_remaining, 4.42)

	def test_balances_count_of_services_matches_expected(self):
		with(open(sample_data_dir+"mobile_data_empty.json")) as f:
			balances = Balances(f.read())

			self.assertEqual(len(balances.services), 7)

	def test_balances_active_balances_none_returns_0(self):
		with(open(sample_data_dir+"mobile_data_empty.json")) as f:
			balances = Balances(f.read())

			self.assertEqual(len(list(balances.active_balances())), 0)

	def test_balances_active_balances_2active_returns_2(self):
		with(open(sample_data_dir+"mobile_data_1024_left.json")) as f:
			balances = Balances(f.read())

			self.assertEqual(len(list(balances.active_balances())), 2)

	def test_data_gets_data_balances(self):
		with(open(sample_data_dir+"balances_lots_enabled.json")) as f:
			balances = Balances(f.read())

			self.assertEqual(len(list(balances.data())), 6)

	def test_data_gets_text_balances(self):
		with(open(sample_data_dir+"balances_lots_enabled.json")) as f:
			balances = Balances(f.read())

			self.assertEqual(len(list(balances.text())), 1)

	def test_data_gets_voice_balances(self):
		with(open(sample_data_dir+"balances_lots_enabled.json")) as f:
			balances = Balances(f.read())

			self.assertEqual(len(list(balances.voice())), 1)

	def test_create_svc_maps_type_correctly(self):
		with(open(sample_data_dir+"balances_lots_enabled.json")) as f:
			balances = Balances(f.read())

			self.assertTrue(isinstance(balances.services[0],VoiceBalance))
			

	def test_create_svc_mystery_type_creates_generic_type(self):
		sampleDataWithUnknownType = """
    	{
  "mainBalance" : 14.420000076293945,
  "bonusBalance" : 0.0,
  "lastBillAmount" : 0.0,
  "openBillAmount" : 0.0,
  "webTextBalance" : {
    "nationalSms" : 200,
    "internationalSms" : 50,
    "nationalSmsAllowance" : 200,
    "internationalSmsAllowance" : 50
  },
  "addonBalance" : [ {
    "balance" : 10000.0,
    "expiryDate" : "15-Oct-2017 00:00",
    "serviceBundle" : {
      "name" : "Awarded Voice Balance",
      "paymentProfile" : null,
      "serviceCode" : "AB2",
      "recurring" : false,
      "allowance" : 10000.0,
      "type" : "mystery",
      "unit" : "Min",
      "charge" : 0.0,
      "status" : "ACTIVE",
      "serviceParameters" : { }
    },
    "optin" : true,
    "visible" : null
  }]
  }
    	"""
    	
		balances = Balances(sampleDataWithUnknownType)

		self.assertTrue(isinstance(balances.services[0],GenericBalance))

	def test_remaining_total_for_missing_type_returns_0(self):
		with(open(sample_data_dir+"balances_lots_enabled.json")) as f:
			balances = Balances(f.read())

			self.assertEqual(balances.remaining_total("nonexistent"),0)

	def test_remaining_total_for_data_matches_expected(self):
		with(open(sample_data_dir+"balances_lots_enabled.json")) as f:
			balances = Balances(f.read())

			self.assertEqual(balances.remaining_total("data"),8591.7578125)

	def test_remaining_total_for_958Mb_sample_returns_958(self):
		with(open(sample_data_dir+"mobile_data_958_left.json")) as f:
			balances = Balances(f.read())

			self.assertEqual(balances.remaining_total("data"),958.076171875)

	def test_remaining_total_for_empty_data_matches_expected(self):
		with(open(sample_data_dir+"mobile_data_empty.json")) as f:
			balances = Balances(f.read())

			self.assertEqual(balances.remaining_total("data"),0)









class TestServiceBalance(unittest.TestCase):

	def test_init_convertsKbToMByte(self):
		with(open(sample_data_dir+"balances_lots_enabled.json")) as f:
			jsonFromFile = json.loads(f.read())

			simple_data = jsonFromFile["addonBalance"][2]
			adv_data = simple_data["serviceBundle"]

			aDataBalance = DataBalance(simple_data, adv_data)

			self.assertEqual(aDataBalance.remaining_qty, 1024.0)

	def test_init_Mbyte_remains_as_Mbyte(self):
		with(open(sample_data_dir+"balances_lots_enabled.json")) as f:
			jsonFromFile = json.loads(f.read())

			simple_data = jsonFromFile["addonBalance"][8]
			adv_data = simple_data["serviceBundle"]

			aDataBalance = DataBalance(simple_data, adv_data)

			self.assertEqual(aDataBalance.remaining_qty, 1023.87890625)

	def test_days_remaining_matches_expected(self):
		sampleData = """
    	{
  "mainBalance" : 14.420000076293945,
  "bonusBalance" : 0.0,
  "lastBillAmount" : 0.0,
  "openBillAmount" : 0.0,
  "webTextBalance" : {
    "nationalSms" : 200,
    "internationalSms" : 50,
    "nationalSmsAllowance" : 200,
    "internationalSmsAllowance" : 50
  },
  "addonBalance" : [ {
    "balance" : 10000.0,
    "expiryDate" : "EXPIRYDATE",
    "serviceBundle" : {
      "name" : "Awarded Voice Balance",
      "paymentProfile" : null,
      "serviceCode" : "AB2",
      "recurring" : false,
      "allowance" : 10000.0,
      "type" : "voice",
      "unit" : "Min",
      "charge" : 0.0,
      "status" : "ACTIVE",
      "serviceParameters" : { }
    },
    "optin" : true,
    "visible" : null
  }]
  }
    	"""
    	
		futureDateTime = (datetime.now() + timedelta(days=20)).strftime("%d-%b-%Y %H:%M")

		sampleData = sampleData.replace("EXPIRYDATE",futureDateTime)
		balances = Balances(sampleData)

		self.assertEqual(balances.services[0].days_remaining(),19)

	def test_summary_forvoice_returns_expected(self):
		with(open(sample_data_dir+"balances_lots_enabled.json")) as f:
			jsonFromFile = json.loads(f.read())

			simple = jsonFromFile["addonBalance"][0]
			adv = simple["serviceBundle"]

			aVoiceBalance = VoiceBalance(simple, adv)

			self.assertEqual(aVoiceBalance.summary(),"10,000 Min")

	def test_summary_fortext_returns_expected(self):
		with(open(sample_data_dir+"balances_lots_enabled.json")) as f:
			jsonFromFile = json.loads(f.read())

			simple = jsonFromFile["addonBalance"][1]
			adv = simple["serviceBundle"]

			aTextBalance = TextBalance(simple, adv)

			self.assertEqual(aTextBalance.summary(),"5,000 Msg")

	def test_summary_for_data_over1GB_returns_expected(self):
		with(open(sample_data_dir+"mobile_data_1024_left.json")) as f:
			jsonFromFile = json.loads(f.read())

			simple = jsonFromFile["addonBalance"][8]
			adv = simple["serviceBundle"]

			aBalance = DataBalance(simple, adv)

			self.assertEqual(aBalance.summary(),"1.00 Gb")

	def test_summary_for_data_under1GB_returns_expected(self):
		with(open(sample_data_dir+"mobile_data_958_left.json")) as f:
			jsonFromFile = json.loads(f.read())

			simple = jsonFromFile["addonBalance"][8]
			adv = simple["serviceBundle"]

			aBalance = DataBalance(simple, adv)

			self.assertEqual(aBalance.summary(),"958 Mb")








class TestUsage(unittest.TestCase):

	def test_usage_init_loadsJson(self):
		with(open(sample_data_dir+"usage_full_anonymised.json")) as f:
			usages = Usage(f.read())

	def test_usage_size_has_all_records(self):
		with(open(sample_data_dir+"usage_full_anonymised.json")) as f:
			usages = Usage(f.read())

			self.assertEqual(usages.size(),477)

	def test_usage_voice_has_correct_num_records(self):
		with(open(sample_data_dir+"usage_full_anonymised.json")) as f:
			usages = Usage(f.read())

			self.assertEqual(len(list(usages.voice())),55)

	def test_usage_text_has_correct_num_records(self):
		with(open(sample_data_dir+"usage_full_anonymised.json")) as f:
			usages = Usage(f.read())

			self.assertEqual(len(list(usages.text())),73)

	def test_usage_data_has_correct_num_records(self):
		with(open(sample_data_dir+"usage_full_anonymised.json")) as f:
			usages = Usage(f.read())

			self.assertEqual(len(list(usages.data())),349)

	def test_usage_filter_usage__blank_shows_all_records(self):
		with(open(sample_data_dir+"usage_full_anonymised.json")) as f:
			usages = Usage(f.read())

			self.assertEqual(len(list(usages.filter_by_type())),477)





if __name__ == '__main__':
	unittest.main()










