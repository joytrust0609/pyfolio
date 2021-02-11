# Copyright 2018 QuantRocket LLC - All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# To run: python3 -m unittest discover -s tests/ -p test_quantrocket*.py -t . -v

import matplotlib as mpl
mpl.use("Agg")
import unittest
from unittest.mock import patch
import io
import pandas as pd
import pyfolio
import numpy as np

ZIPLINE_RESULTS = [{'dataframe': 'benchmark',
  'index': 11,
  'date': '2017-12-20 00:00:00+00:00',
  'column': 'benchmark',
  'value': '-0.0005239410483275364'},
 {'dataframe': 'benchmark',
  'index': 12,
  'date': '2017-12-21 00:00:00+00:00',
  'column': 'benchmark',
  'value': '0.0020594728006451124'},
 {'dataframe': 'benchmark',
  'index': 13,
  'date': '2017-12-22 00:00:00+00:00',
  'column': 'benchmark',
  'value': '-0.0002615691586591584'},
 {'dataframe': 'perf',
  'index': 11,
  'date': '2017-12-20 00:00:00+00:00',
  'column': 'algo_volatility',
  'value': '0.03576379162090691'},
 {'dataframe': 'perf',
  'index': 11,
  'date': '2017-12-20 00:00:00+00:00',
  'column': 'algorithm_period_return',
  'value': '0.007330000000000281'},
 {'dataframe': 'perf',
  'index': 11,
  'date': '2017-12-20 00:00:00+00:00',
  'column': 'alpha',
  'value': '0.07047503738968493'},
 {'dataframe': 'perf',
  'index': 11,
  'date': '2017-12-20 00:00:00+00:00',
  'column': 'benchmark_period_return',
  'value': '0.01605688888616008'},
 {'dataframe': 'perf',
  'index': 11,
  'date': '2017-12-20 00:00:00+00:00',
  'column': 'benchmark_volatility',
  'value': '0.06490253936811202'},
 {'dataframe': 'perf',
  'index': 11,
  'date': '2017-12-20 00:00:00+00:00',
  'column': 'beta',
  'value': '0.24809768188900583'},
 {'dataframe': 'perf',
  'index': 11,
  'date': '2017-12-20 00:00:00+00:00',
  'column': 'capital_used',
  'value': '-8325.0'},
 {'dataframe': 'perf',
  'index': 11,
  'date': '2017-12-20 00:00:00+00:00',
  'column': 'current_price',
  'value': '2694.25'},
 {'dataframe': 'perf',
  'index': 11,
  'date': '2017-12-20 00:00:00+00:00',
  'column': 'ending_cash',
  'value': '10073300.0'},
 {'dataframe': 'perf',
  'index': 11,
  'date': '2017-12-20 00:00:00+00:00',
  'column': 'ending_exposure',
  'value': '9968725.0'},
 {'dataframe': 'perf',
  'index': 11,
  'date': '2017-12-20 00:00:00+00:00',
  'column': 'ending_value',
  'value': '0.0'},
 {'dataframe': 'perf',
  'index': 11,
  'date': '2017-12-20 00:00:00+00:00',
  'column': 'excess_return',
  'value': '0.0'},
 {'dataframe': 'perf',
  'index': 11,
  'date': '2017-12-20 00:00:00+00:00',
  'column': 'gross_leverage',
  'value': '0.9896185956935661'},
 {'dataframe': 'perf',
  'index': 11,
  'date': '2017-12-20 00:00:00+00:00',
  'column': 'long_exposure',
  'value': '9968725.0'},
 {'dataframe': 'perf',
  'index': 11,
  'date': '2017-12-20 00:00:00+00:00',
  'column': 'long_mavg',
  'value': '2694.25'},
 {'dataframe': 'perf',
  'index': 11,
  'date': '2017-12-20 00:00:00+00:00',
  'column': 'long_value',
  'value': '0.0'},
 {'dataframe': 'perf',
  'index': 11,
  'date': '2017-12-20 00:00:00+00:00',
  'column': 'longs_count',
  'value': '1'},
 {'dataframe': 'perf',
  'index': 11,
  'date': '2017-12-20 00:00:00+00:00',
  'column': 'max_drawdown',
  'value': '-0.0030531304564729088'},
 {'dataframe': 'perf',
  'index': 11,
  'date': '2017-12-20 00:00:00+00:00',
  'column': 'max_leverage',
  'value': '0.9896271682392471'},
 {'dataframe': 'perf',
  'index': 11,
  'date': '2017-12-20 00:00:00+00:00',
  'column': 'net_leverage',
  'value': '0.9896185956935661'},
 {'dataframe': 'perf',
  'index': 11,
  'date': '2017-12-20 00:00:00+00:00',
  'column': 'orders',
  'value': "[{'filled': 0, 'limit': None, 'commission': 0, 'amount': -74, 'status': 0, 'stop_reached': False, 'dt': Timestamp('2017-12-20 15:20:00+0000', tz='UTC'), 'id': '8b24862c173b48298a369132a78a0443', 'created': Timestamp('2017-12-20 15:20:00+0000', tz='UTC'), 'sid': Future(258973438 [ESH8-201803]), 'reason': None, 'limit_reached': False, 'stop': None}]"},
 {'dataframe': 'perf',
  'index': 11,
  'date': '2017-12-20 00:00:00+00:00',
  'column': 'period_close',
  'value': '2017-12-20 21:00:00+00:00'},
 {'dataframe': 'perf',
  'index': 11,
  'date': '2017-12-20 00:00:00+00:00',
  'column': 'period_label',
  'value': '2017-12'},
 {'dataframe': 'perf',
  'index': 11,
  'date': '2017-12-20 00:00:00+00:00',
  'column': 'period_open',
  'value': '2017-12-20 14:31:00+00:00'},
 {'dataframe': 'perf',
  'index': 11,
  'date': '2017-12-20 00:00:00+00:00',
  'column': 'pnl',
  'value': '-8325.0'},
 {'dataframe': 'perf',
  'index': 11,
  'date': '2017-12-20 00:00:00+00:00',
  'column': 'portfolio_value',
  'value': '10073300.0'},
 {'dataframe': 'perf',
  'index': 11,
  'date': '2017-12-20 00:00:00+00:00',
  'column': 'positions',
  'value': "[{'last_sale_price': 2694.25, 'sid': Future(258973438 [ESH8-201803]), 'cost_basis': 2672.25, 'amount': 74}]"},
 {'dataframe': 'perf',
  'index': 11,
  'date': '2017-12-20 00:00:00+00:00',
  'column': 'returns',
  'value': '-0.0008257597361536195'},
 {'dataframe': 'perf',
  'index': 11,
  'date': '2017-12-20 00:00:00+00:00',
  'column': 'sharpe',
  'value': '4.306058883822183'},
 {'dataframe': 'perf',
  'index': 11,
  'date': '2017-12-20 00:00:00+00:00',
  'column': 'short_exposure',
  'value': '0.0'},
 {'dataframe': 'perf',
  'index': 11,
  'date': '2017-12-20 00:00:00+00:00',
  'column': 'short_mavg',
  'value': '2694.25'},
 {'dataframe': 'perf',
  'index': 11,
  'date': '2017-12-20 00:00:00+00:00',
  'column': 'short_value',
  'value': '0.0'},
 {'dataframe': 'perf',
  'index': 11,
  'date': '2017-12-20 00:00:00+00:00',
  'column': 'shorts_count',
  'value': '0'},
 {'dataframe': 'perf',
  'index': 11,
  'date': '2017-12-20 00:00:00+00:00',
  'column': 'sortino',
  'value': '8.176100431161784'},
 {'dataframe': 'perf',
  'index': 11,
  'date': '2017-12-20 00:00:00+00:00',
  'column': 'starting_cash',
  'value': '10081625.0'},
 {'dataframe': 'perf',
  'index': 11,
  'date': '2017-12-20 00:00:00+00:00',
  'column': 'starting_exposure',
  'value': '9977050.0'},
 {'dataframe': 'perf',
  'index': 11,
  'date': '2017-12-20 00:00:00+00:00',
  'column': 'starting_value',
  'value': '0.0'},
 {'dataframe': 'perf',
  'index': 11,
  'date': '2017-12-20 00:00:00+00:00',
  'column': 'trading_days',
  'value': '12'},
 {'dataframe': 'perf',
  'index': 11,
  'date': '2017-12-20 00:00:00+00:00',
  'column': 'transactions',
  'value': '[]'},
 {'dataframe': 'perf',
  'index': 11,
  'date': '2017-12-20 00:00:00+00:00',
  'column': 'treasury_period_return',
  'value': '0.0'},
 {'dataframe': 'perf',
  'index': 12,
  'date': '2017-12-21 00:00:00+00:00',
  'column': 'algo_volatility',
  'value': '0.036020438482886996'},
 {'dataframe': 'perf',
  'index': 12,
  'date': '2017-12-21 00:00:00+00:00',
  'column': 'algorithm_period_return',
  'value': '0.005387500000000323'},
 {'dataframe': 'perf',
  'index': 12,
  'date': '2017-12-21 00:00:00+00:00',
  'column': 'alpha',
  'value': '0.021222904649307477'},
 {'dataframe': 'perf',
  'index': 12,
  'date': '2017-12-21 00:00:00+00:00',
  'column': 'benchmark_period_return',
  'value': '0.018149430412729206'},
 {'dataframe': 'perf',
  'index': 12,
  'date': '2017-12-21 00:00:00+00:00',
  'column': 'benchmark_volatility',
  'value': '0.06222104294288973'},
 {'dataframe': 'perf',
  'index': 12,
  'date': '2017-12-21 00:00:00+00:00',
  'column': 'beta',
  'value': '0.23824791806971146'},
 {'dataframe': 'perf',
  'index': 12,
  'date': '2017-12-21 00:00:00+00:00',
  'column': 'capital_used',
  'value': '-19425.0'},
 {'dataframe': 'perf',
  'index': 12,
  'date': '2017-12-21 00:00:00+00:00',
  'column': 'current_price',
  'value': '2689.0'},
 {'dataframe': 'perf',
  'index': 12,
  'date': '2017-12-21 00:00:00+00:00',
  'column': 'ending_cash',
  'value': '10053875.0'},
 {'dataframe': 'perf',
  'index': 12,
  'date': '2017-12-21 00:00:00+00:00',
  'column': 'ending_exposure',
  'value': '9949300.0'},
 {'dataframe': 'perf',
  'index': 12,
  'date': '2017-12-21 00:00:00+00:00',
  'column': 'ending_value',
  'value': '0.0'},
 {'dataframe': 'perf',
  'index': 12,
  'date': '2017-12-21 00:00:00+00:00',
  'column': 'excess_return',
  'value': '0.0'},
 {'dataframe': 'perf',
  'index': 12,
  'date': '2017-12-21 00:00:00+00:00',
  'column': 'gross_leverage',
  'value': '0.9895985378771867'},
 {'dataframe': 'perf',
  'index': 12,
  'date': '2017-12-21 00:00:00+00:00',
  'column': 'long_exposure',
  'value': '9949300.0'},
 {'dataframe': 'perf',
  'index': 12,
  'date': '2017-12-21 00:00:00+00:00',
  'column': 'long_mavg',
  'value': '2689.0'},
 {'dataframe': 'perf',
  'index': 12,
  'date': '2017-12-21 00:00:00+00:00',
  'column': 'long_value',
  'value': '0.0'},
 {'dataframe': 'perf',
  'index': 12,
  'date': '2017-12-21 00:00:00+00:00',
  'column': 'longs_count',
  'value': '1'},
 {'dataframe': 'perf',
  'index': 12,
  'date': '2017-12-21 00:00:00+00:00',
  'column': 'max_drawdown',
  'value': '-0.0030531304564729088'},
 {'dataframe': 'perf',
  'index': 12,
  'date': '2017-12-21 00:00:00+00:00',
  'column': 'max_leverage',
  'value': '0.9896271682392471'},
 {'dataframe': 'perf',
  'index': 12,
  'date': '2017-12-21 00:00:00+00:00',
  'column': 'net_leverage',
  'value': '0.9895985378771867'},
 {'dataframe': 'perf',
  'index': 12,
  'date': '2017-12-21 00:00:00+00:00',
  'column': 'orders',
  'value': '[]'},
 {'dataframe': 'perf',
  'index': 12,
  'date': '2017-12-21 00:00:00+00:00',
  'column': 'period_close',
  'value': '2017-12-21 21:00:00+00:00'},
 {'dataframe': 'perf',
  'index': 12,
  'date': '2017-12-21 00:00:00+00:00',
  'column': 'period_label',
  'value': '2017-12'},
 {'dataframe': 'perf',
  'index': 12,
  'date': '2017-12-21 00:00:00+00:00',
  'column': 'period_open',
  'value': '2017-12-21 14:31:00+00:00'},
 {'dataframe': 'perf',
  'index': 12,
  'date': '2017-12-21 00:00:00+00:00',
  'column': 'pnl',
  'value': '-19425.0'},
 {'dataframe': 'perf',
  'index': 12,
  'date': '2017-12-21 00:00:00+00:00',
  'column': 'portfolio_value',
  'value': '10053875.0'},
 {'dataframe': 'perf',
  'index': 12,
  'date': '2017-12-21 00:00:00+00:00',
  'column': 'positions',
  'value': "[{'last_sale_price': 2689.0, 'sid': Future(258973438 [ESH8-201803]), 'cost_basis': 2672.25, 'amount': 74}]"},
 {'dataframe': 'perf',
  'index': 12,
  'date': '2017-12-21 00:00:00+00:00',
  'column': 'returns',
  'value': '-0.00192836508393468'},
 {'dataframe': 'perf',
  'index': 12,
  'date': '2017-12-21 00:00:00+00:00',
  'column': 'sharpe',
  'value': '2.9087415746693663'},
 {'dataframe': 'perf',
  'index': 12,
  'date': '2017-12-21 00:00:00+00:00',
  'column': 'short_exposure',
  'value': '0.0'},
 {'dataframe': 'perf',
  'index': 12,
  'date': '2017-12-21 00:00:00+00:00',
  'column': 'short_mavg',
  'value': '2689.0'},
 {'dataframe': 'perf',
  'index': 12,
  'date': '2017-12-21 00:00:00+00:00',
  'column': 'short_value',
  'value': '0.0'},
 {'dataframe': 'perf',
  'index': 12,
  'date': '2017-12-21 00:00:00+00:00',
  'column': 'shorts_count',
  'value': '0'},
 {'dataframe': 'perf',
  'index': 12,
  'date': '2017-12-21 00:00:00+00:00',
  'column': 'sortino',
  'value': '5.2415300623148005'},
 {'dataframe': 'perf',
  'index': 12,
  'date': '2017-12-21 00:00:00+00:00',
  'column': 'starting_cash',
  'value': '10073300.0'},
 {'dataframe': 'perf',
  'index': 12,
  'date': '2017-12-21 00:00:00+00:00',
  'column': 'starting_exposure',
  'value': '9968725.0'},
 {'dataframe': 'perf',
  'index': 12,
  'date': '2017-12-21 00:00:00+00:00',
  'column': 'starting_value',
  'value': '0.0'},
 {'dataframe': 'perf',
  'index': 12,
  'date': '2017-12-21 00:00:00+00:00',
  'column': 'trading_days',
  'value': '13'},
 {'dataframe': 'perf',
  'index': 12,
  'date': '2017-12-21 00:00:00+00:00',
  'column': 'transactions',
  'value': '[]'},
 {'dataframe': 'perf',
  'index': 12,
  'date': '2017-12-21 00:00:00+00:00',
  'column': 'treasury_period_return',
  'value': '0.0'},
 {'dataframe': 'perf',
  'index': 13,
  'date': '2017-12-22 00:00:00+00:00',
  'column': 'algo_volatility',
  'value': '0.03460782712008343'},
 {'dataframe': 'perf',
  'index': 13,
  'date': '2017-12-22 00:00:00+00:00',
  'column': 'algorithm_period_return',
  'value': '0.005850000000000355'},
 {'dataframe': 'perf',
  'index': 13,
  'date': '2017-12-22 00:00:00+00:00',
  'column': 'alpha',
  'value': '0.030264033339386598'},
 {'dataframe': 'perf',
  'index': 13,
  'date': '2017-12-22 00:00:00+00:00',
  'column': 'benchmark_period_return',
  'value': '0.01788311392282682'},
 {'dataframe': 'perf',
  'index': 13,
  'date': '2017-12-22 00:00:00+00:00',
  'column': 'benchmark_volatility',
  'value': '0.060190105691183875'},
 {'dataframe': 'perf',
  'index': 13,
  'date': '2017-12-22 00:00:00+00:00',
  'column': 'beta',
  'value': '0.2346492469999346'},
 {'dataframe': 'perf',
  'index': 13,
  'date': '2017-12-22 00:00:00+00:00',
  'column': 'capital_used',
  'value': '4625.0'},
 {'dataframe': 'perf',
  'index': 13,
  'date': '2017-12-22 00:00:00+00:00',
  'column': 'current_price',
  'value': '2688.5'},
 {'dataframe': 'perf',
  'index': 13,
  'date': '2017-12-22 00:00:00+00:00',
  'column': 'ending_cash',
  'value': '10058500.0'},
 {'dataframe': 'perf',
  'index': 13,
  'date': '2017-12-22 00:00:00+00:00',
  'column': 'ending_exposure',
  'value': '9947450.0'},
 {'dataframe': 'perf',
  'index': 13,
  'date': '2017-12-22 00:00:00+00:00',
  'column': 'ending_value',
  'value': '0.0'},
 {'dataframe': 'perf',
  'index': 13,
  'date': '2017-12-22 00:00:00+00:00',
  'column': 'excess_return',
  'value': '0.0'},
 {'dataframe': 'perf',
  'index': 13,
  'date': '2017-12-22 00:00:00+00:00',
  'column': 'gross_leverage',
  'value': '0.9889595864194463'},
 {'dataframe': 'perf',
  'index': 13,
  'date': '2017-12-22 00:00:00+00:00',
  'column': 'long_exposure',
  'value': '9947450.0'},
 {'dataframe': 'perf',
  'index': 13,
  'date': '2017-12-22 00:00:00+00:00',
  'column': 'long_mavg',
  'value': '2686.57375'},
 {'dataframe': 'perf',
  'index': 13,
  'date': '2017-12-22 00:00:00+00:00',
  'column': 'long_value',
  'value': '0.0'},
 {'dataframe': 'perf',
  'index': 13,
  'date': '2017-12-22 00:00:00+00:00',
  'column': 'longs_count',
  'value': '1'},
 {'dataframe': 'perf',
  'index': 13,
  'date': '2017-12-22 00:00:00+00:00',
  'column': 'max_drawdown',
  'value': '-0.0030531304564729088'},
 {'dataframe': 'perf',
  'index': 13,
  'date': '2017-12-22 00:00:00+00:00',
  'column': 'max_leverage',
  'value': '0.9896271682392471'},
 {'dataframe': 'perf',
  'index': 13,
  'date': '2017-12-22 00:00:00+00:00',
  'column': 'net_leverage',
  'value': '0.9889595864194463'},
 {'dataframe': 'perf',
  'index': 13,
  'date': '2017-12-22 00:00:00+00:00',
  'column': 'orders',
  'value': "[{'filled': -74, 'limit': None, 'commission': 0.0, 'amount': -74, 'status': 1, 'stop_reached': False, 'dt': Timestamp('2017-12-22 14:31:00+0000', tz='UTC'), 'id': '8b24862c173b48298a369132a78a0443', 'created': Timestamp('2017-12-20 15:20:00+0000', tz='UTC'), 'sid': Future(258973438 [ESH8-201803]), 'reason': None, 'limit_reached': False, 'stop': None}, {'filled': 74, 'limit': None, 'commission': 0.0, 'amount': 74, 'status': 1, 'stop_reached': False, 'dt': Timestamp('2017-12-22 18:48:00+0000', tz='UTC'), 'id': 'f45457ad49ca4b499829b68a2e7c8144', 'created': Timestamp('2017-12-22 18:47:00+0000', tz='UTC'), 'sid': Future(258973438 [ESH8-201803]), 'reason': None, 'limit_reached': False, 'stop': None}]"},
 {'dataframe': 'perf',
  'index': 13,
  'date': '2017-12-22 00:00:00+00:00',
  'column': 'period_close',
  'value': '2017-12-22 21:00:00+00:00'},
 {'dataframe': 'perf',
  'index': 13,
  'date': '2017-12-22 00:00:00+00:00',
  'column': 'period_label',
  'value': '2017-12'},
 {'dataframe': 'perf',
  'index': 13,
  'date': '2017-12-22 00:00:00+00:00',
  'column': 'period_open',
  'value': '2017-12-22 14:31:00+00:00'},
 {'dataframe': 'perf',
  'index': 13,
  'date': '2017-12-22 00:00:00+00:00',
  'column': 'pnl',
  'value': '4625.0'},
 {'dataframe': 'perf',
  'index': 13,
  'date': '2017-12-22 00:00:00+00:00',
  'column': 'portfolio_value',
  'value': '10058500.0'},
 {'dataframe': 'perf',
  'index': 13,
  'date': '2017-12-22 00:00:00+00:00',
  'column': 'positions',
  'value': "[{'last_sale_price': 2688.5, 'sid': Future(258973438 [ESH8-201803]), 'cost_basis': 2686.5, 'amount': 74}]"},
 {'dataframe': 'perf',
  'index': 13,
  'date': '2017-12-22 00:00:00+00:00',
  'column': 'returns',
  'value': '0.0004600216334498253'},
 {'dataframe': 'perf',
  'index': 13,
  'date': '2017-12-22 00:00:00+00:00',
  'column': 'sharpe',
  'value': '3.0504853237181964'},
 {'dataframe': 'perf',
  'index': 13,
  'date': '2017-12-22 00:00:00+00:00',
  'column': 'short_exposure',
  'value': '0.0'},
 {'dataframe': 'perf',
  'index': 13,
  'date': '2017-12-22 00:00:00+00:00',
  'column': 'short_mavg',
  'value': '2687.68'},
 {'dataframe': 'perf',
  'index': 13,
  'date': '2017-12-22 00:00:00+00:00',
  'column': 'short_value',
  'value': '0.0'},
 {'dataframe': 'perf',
  'index': 13,
  'date': '2017-12-22 00:00:00+00:00',
  'column': 'shorts_count',
  'value': '0'},
 {'dataframe': 'perf',
  'index': 13,
  'date': '2017-12-22 00:00:00+00:00',
  'column': 'sortino',
  'value': '5.480744561694047'},
 {'dataframe': 'perf',
  'index': 13,
  'date': '2017-12-22 00:00:00+00:00',
  'column': 'starting_cash',
  'value': '10053875.0'},
 {'dataframe': 'perf',
  'index': 13,
  'date': '2017-12-22 00:00:00+00:00',
  'column': 'starting_exposure',
  'value': '9949300.0'},
 {'dataframe': 'perf',
  'index': 13,
  'date': '2017-12-22 00:00:00+00:00',
  'column': 'starting_value',
  'value': '0.0'},
 {'dataframe': 'perf',
  'index': 13,
  'date': '2017-12-22 00:00:00+00:00',
  'column': 'trading_days',
  'value': '14'},
 {'dataframe': 'perf',
  'index': 13,
  'date': '2017-12-22 00:00:00+00:00',
  'column': 'transactions',
  'value': "[{'sid': Future(258973438 [ESH8-201803]), 'commission': None, 'amount': -74, 'order_id': '8b24862c173b48298a369132a78a0443', 'dt': Timestamp('2017-12-22 14:31:00+0000', tz='UTC'), 'price': 2688.25}, {'sid': Future(258973438 [ESH8-201803]), 'commission': None, 'amount': 74, 'order_id': 'f45457ad49ca4b499829b68a2e7c8144', 'dt': Timestamp('2017-12-22 18:48:00+0000', tz='UTC'), 'price': 2686.5}]"},
 {'dataframe': 'perf',
  'index': 13,
  'date': '2017-12-22 00:00:00+00:00',
  'column': 'treasury_period_return',
  'value': '0.0'},
 {'dataframe': 'positions',
  'index': 3,
  'date': '2017-12-20 00:00:00+00:00',
  'column': 'Future(258973438 [ESH8-201803])',
  'value': '199374.5'},
 {'dataframe': 'positions',
  'index': 3,
  'date': '2017-12-20 00:00:00+00:00',
  'column': 'cash',
  'value': '10073300.0'},
 {'dataframe': 'positions',
  'index': 4,
  'date': '2017-12-21 00:00:00+00:00',
  'column': 'Future(258973438 [ESH8-201803])',
  'value': '198986.0'},
 {'dataframe': 'positions',
  'index': 4,
  'date': '2017-12-21 00:00:00+00:00',
  'column': 'cash',
  'value': '10053875.0'},
 {'dataframe': 'positions',
  'index': 5,
  'date': '2017-12-22 00:00:00+00:00',
  'column': 'Future(258973438 [ESH8-201803])',
  'value': '198949.0'},
 {'dataframe': 'positions',
  'index': 5,
  'date': '2017-12-22 00:00:00+00:00',
  'column': 'cash',
  'value': '10058500.0'},
 {'dataframe': 'returns',
  'index': 11,
  'date': '2017-12-20 00:00:00+00:00',
  'column': 'returns',
  'value': '-0.0008257597361536195'},
 {'dataframe': 'returns',
  'index': 12,
  'date': '2017-12-21 00:00:00+00:00',
  'column': 'returns',
  'value': '-0.00192836508393468'},
 {'dataframe': 'returns',
  'index': 13,
  'date': '2017-12-22 00:00:00+00:00',
  'column': 'returns',
  'value': '0.0004600216334498253'},
 {'dataframe': 'transactions',
  'index': 19,
  'date': '2017-12-22 14:31:00+00:00',
  'column': 'amount',
  'value': '-74'},
 {'dataframe': 'transactions',
  'index': 19,
  'date': '2017-12-22 14:31:00+00:00',
  'column': 'order_id',
  'value': '8b24862c173b48298a369132a78a0443'},
 {'dataframe': 'transactions',
  'index': 19,
  'date': '2017-12-22 14:31:00+00:00',
  'column': 'price',
  'value': '2688.25'},
 {'dataframe': 'transactions',
  'index': 19,
  'date': '2017-12-22 14:31:00+00:00',
  'column': 'sid',
  'value': 'Future(258973438 [ESH8-201803])'},
 {'dataframe': 'transactions',
  'index': 19,
  'date': '2017-12-22 14:31:00+00:00',
  'column': 'symbol',
  'value': 'Future(258973438 [ESH8-201803])'},
 {'dataframe': 'transactions',
  'index': 19,
  'date': '2017-12-22 14:31:00+00:00',
  'column': 'txn_dollars',
  'value': '198930.5'},
 {'dataframe': 'transactions',
  'index': 20,
  'date': '2017-12-22 18:48:00+00:00',
  'column': 'amount',
  'value': '74'},
 {'dataframe': 'transactions',
  'index': 20,
  'date': '2017-12-22 18:48:00+00:00',
  'column': 'order_id',
  'value': 'f45457ad49ca4b499829b68a2e7c8144'},
 {'dataframe': 'transactions',
  'index': 20,
  'date': '2017-12-22 18:48:00+00:00',
  'column': 'price',
  'value': '2686.5'},
 {'dataframe': 'transactions',
  'index': 20,
  'date': '2017-12-22 18:48:00+00:00',
  'column': 'sid',
  'value': 'Future(258973438 [ESH8-201803])'},
 {'dataframe': 'transactions',
  'index': 20,
  'date': '2017-12-22 18:48:00+00:00',
  'column': 'symbol',
  'value': 'Future(258973438 [ESH8-201803])'},
 {'dataframe': 'transactions',
  'index': 20,
  'date': '2017-12-22 18:48:00+00:00',
  'column': 'txn_dollars',
  'value': '-198801.0'}]

class PyFolioFromZiplineTestCase(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    @patch("pyfolio.quantrocket_zipline.create_full_tear_sheet")
    def test_from_zipline_csv_with_padding(self, mock_create_full_tear_sheet):

        f = io.StringIO()
        zipline_results = pd.DataFrame.from_records(ZIPLINE_RESULTS)
        zipline_results.to_csv(f,index=False)
        f.seek(0)

        pyfolio.from_zipline_csv(f)

        tear_sheet_call = mock_create_full_tear_sheet.mock_calls[0]

        _, args, kwargs = tear_sheet_call
        self.assertEqual(len(args), 1)
        returns = args[0]
        self.assertEqual(returns.index.tz.zone, "UTC")

        # returns were padded to len 127 (more than 6 months=126 days)
        self.assertEqual(returns.index.size, 127)
        self.assertTrue((returns.iloc[:124] == 0).all())
        self.assertDictEqual(
            returns.iloc[124:].to_dict(),
            {
                pd.Timestamp('2017-12-20 00:00:00+0000', tz='UTC', freq='B'): -0.0008257597361536195,
                pd.Timestamp('2017-12-21 00:00:00+0000', tz='UTC', freq='B'): -0.00192836508393468,
                pd.Timestamp('2017-12-22 00:00:00+0000', tz='UTC', freq='B'): 0.0004600216334498253
            })

        self.assertEqual(list(kwargs.keys()), ["positions", "transactions", "benchmark_rets"])

        # benchmark_rets were also padded to len 127
        benchmark_rets = kwargs["benchmark_rets"]
        self.assertEqual(benchmark_rets.index.size, 127)
        self.assertTrue((benchmark_rets.iloc[:124] == 0).all())
        self.assertDictEqual(
            benchmark_rets.iloc[124:].to_dict(),
            {
                pd.Timestamp('2017-12-20 00:00:00+0000', tz='UTC', freq='B'): -0.0005239410483275364,
                pd.Timestamp('2017-12-21 00:00:00+0000', tz='UTC', freq='B'): 0.0020594728006451124,
                pd.Timestamp('2017-12-22 00:00:00+0000', tz='UTC', freq='B'): -0.0002615691586591584
            })


        transactions = kwargs["transactions"]
        self.assertDictEqual(
            transactions.to_dict(),
            {
                'amount': {
                    pd.Timestamp('2017-12-22 14:31:00+0000', tz='UTC'): -74,
                    pd.Timestamp('2017-12-22 18:48:00+0000', tz='UTC'): 74
                    },
                'order_id': {
                    pd.Timestamp('2017-12-22 14:31:00+0000', tz='UTC'): '8b24862c173b48298a369132a78a0443',
                    pd.Timestamp('2017-12-22 18:48:00+0000', tz='UTC'): 'f45457ad49ca4b499829b68a2e7c8144'
                    },
                'price': {
                    pd.Timestamp('2017-12-22 14:31:00+0000', tz='UTC'): 2688.25,
                    pd.Timestamp('2017-12-22 18:48:00+0000', tz='UTC'): 2686.5
                    },
                'sid': {
                    pd.Timestamp('2017-12-22 14:31:00+0000', tz='UTC'): 'Future(258973438 [ESH8-201803])',
                    pd.Timestamp('2017-12-22 18:48:00+0000', tz='UTC'): 'Future(258973438 [ESH8-201803])'
                    },
                'symbol': {
                    pd.Timestamp('2017-12-22 14:31:00+0000', tz='UTC'): 'Future(258973438 [ESH8-201803])',
                    pd.Timestamp('2017-12-22 18:48:00+0000', tz='UTC'): 'Future(258973438 [ESH8-201803])'
                    },
                'txn_dollars': {
                    pd.Timestamp('2017-12-22 14:31:00+0000', tz='UTC'): 198930.5,
                    pd.Timestamp('2017-12-22 18:48:00+0000', tz='UTC'): -198801.0
                }
            }
        )

        positions = kwargs["positions"]
        self.assertDictEqual(
            positions.to_dict(),
            {
                'Future(258973438 [ESH8-201803])': {
                    pd.Timestamp('2017-12-20 00:00:00+0000', tz='UTC'): 199374.5,
                    pd.Timestamp('2017-12-21 00:00:00+0000', tz='UTC'): 198986.0,
                    pd.Timestamp('2017-12-22 00:00:00+0000', tz='UTC'): 198949.0
                    },
                'cash': {
                    pd.Timestamp('2017-12-20 00:00:00+0000', tz='UTC'): 10073300.0,
                    pd.Timestamp('2017-12-21 00:00:00+0000', tz='UTC'): 10053875.0,
                    pd.Timestamp('2017-12-22 00:00:00+0000', tz='UTC'): 10058500.0
                }
            }
        )
