import unittest

import pandas as pd
import logging

import sys, os

sys.path.append(os.path.abspath(os.path.join("./script")))

from get_dataframe_information import  DataFrameInformation
from get_missing_information import MissingInformation

logging.basicConfig(filename='../logfile.log', filemode='a',
                    encoding='utf-8', level=logging.DEBUG)

try:
    test_data = pd.read_csv('./data/Week1_challenge_data_source.csv')
except BaseException:
    logging.warning('file not found or wrong file format')

class TestGetInformations(unittest.TestCase):
    def setUp(self):
        self.dinfo = DataFrameInformation(test_data)
        self.minfo = MissingInformation(test_data)
     
    def test_get_skewness(self):
        self.assertEqual(self.dinfo.get_skewness(test_data).columns.tolist(), ['skewness'])

    def test_get_skewness_missing_count(self):
        self.assertEqual(self.dinfo.get_skewness_missing_count(test_data).columns.tolist(),
                         ['skewness', 'Missing Values', '% of Total Values','Dtype'])

    def test_missing_values_table(self):
        self.assertEqual(self.minfo.missing_values_table(test_data).columns.tolist(),
                         ['Missing Values', '% of Total Values','Dtype'])

    def test_percent_missing(self):
        self.assertIsNotNone(self.minfo.percent_missing(test_data))
if __name__ == "__main__":
    unittest.main()