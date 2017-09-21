import unittest
from unittest import TestCase
import json
import types
from pytescomobileirl import *

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

	def test_remaining_total_for_958Mb_sample_matches_expected(self):
		with(open(sample_data_dir+"mobile_data_958_left.json")) as f:
			balances = Balances(f.read())

			self.assertEqual(balances.remaining_total("data"),958.076171875)

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

if __name__ == '__main__':
	unittest.main()