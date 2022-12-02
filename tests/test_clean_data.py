import unittest

import pandas as pd
import logging

import sys
import os

sys.path.append(os.path.abspath(os.path.join("./script")))

from data_clean_handler import CleanData

logging.basicConfig(filename='../logfile.log', filemode='a',
                    encoding='utf-8', level=logging.DEBUG)
try:
    test_data = pd.read_csv('./data/Week1_challenge_data_source.csv')
except BaseException:
    logging.warning('file not found or wrong file format')


class TestCleanData(unittest.TestCase):
    def setUp(self):
        self.clean = CleanData(test_data)
        
    def test_drop_missing_count_greaterthan_20p(self):
        self.assertIsInstance(
            self.clean.drop_missing_count_greaterthan_20p(test_data),pd.DataFrame)
                         
if __name__ == "__main__":
    unittest.main()
    
    
