import unittest
from unittest import TestCase
import json
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

if __name__ == '__main__':
	unittest.main()