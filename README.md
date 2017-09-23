# pytescomobileirl
[![Build Status](https://travis-ci.org/skhg/pytescomobileirl.svg?branch=master)](https://travis-ci.org/skhg/pytescomobileirl) [![PyPI](https://img.shields.io/pypi/v/pytescomobileirl.svg)](https://pypi.python.org/pypi/pytescomobileirl/) [![Codecov](https://img.shields.io/codecov/c/github/skhg/pytescomobileirl.svg)](https://codecov.io/gh/skhg/pytescomobileirl)

A Python API for accessing your [Tesco Mobile Ireland](http://www.tescomobile.ie) account balance &amp; usage stats. This is an unoffical API and the author/contributors are in no way connected to Tesco or Tesco Mobile. The API provides methods to:
* Get your current balances (€ credit and voice/text/data packages)
* Get your usage records as far back as is available.

For an example of this in use, see my [Tesco Mobile BitBar plugin](https://github.com/skhg/BitBar-Plugins/tree/master/TescoMobileIrl)

## Installation
`pip install pytescomobileirl`

## Usage
It's very easy to use. Try the following to get your balance data:
```python
from pytescomobileirl import *
from pprint import pprint

session = pytescomobileirl.TescoSession()
session.login("<PhoneNumber>","<Password>")
balances = session.get_balances()

my_credit = balances.credit_remaining
my_data = balances.remaining_total("data")

print(my_credit)
print(my_data.summary())
pprint(vars(my_data))
```
returns:
```python
14.28
939 MB
{'balance_expires': datetime.datetime(2017, 10, 15, 0, 0),
 'balance_type': u'data',
 'is_active': True,
 'remaining_qty': 939.181640625,
 'serviceCode': u'AB3',
 'unit': 'MByte'}
 ```
 
 Or to get your usage history enter:
 ```python
 usage = session.get_usage()
 pprint(vars(usage.records[0]))
  ```
  returns:
  ```python
  {'called_number': u'tescomobile.liffeytelecom.com',
 'charge': u'0.0',
 'country_code': None,
 'event_date': datetime.datetime(2017, 9, 23, 13, 33),
 'roaming': False,
 'service_code': u'GPBAS',
 'service_name': u'GPRS Basic Service',
 'unit': u'Bytes',
 'use_type': u'DATA',
 'volume': 119896.0}
 ```
 
 ## Tests
 `python ./tests/tests.py`
 
 ## Contributing
 Fork this repo, make some changes and create a new pull request!
