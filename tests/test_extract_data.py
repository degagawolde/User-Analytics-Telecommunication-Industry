import unittest

import pandas as pd
import logging

import sys, os

sys.path.append(os.path.abspath(os.path.join("./script")))
from get_dataframe_information import get_skewness_missing_count, DataFrameInformation
from get_missing_information import missing_values_table, percent_missing

logging.basicConfig(filename='/logfile.log', filemode='a',
                    encoding='utf-8', level=logging.DEBUG)

try:
    test_data = pd.read_excel('../data/Week1_challenge_data_source.xlsx')
except BaseException:
    logging.warning('file not found or wrong file format')

class TestGetInformations(unittest.TestCase):
    def setUp(self):
        self.dinfo = DataFrameInformation(test_data)
    
    def test_get_skewness(self):
        self.assertEqual(self.dinfo.get_skewness().iloc[0], 0.000968)
if __name__ == "__main__":
    unittest.main() 