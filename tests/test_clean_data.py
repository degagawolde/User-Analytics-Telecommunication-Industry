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
    test_data = pd.read_excel('../data/Week1_challenge_data_source.xlsx')
except BaseException:
    logging.warning('file not found or wrong file format')


class TestCleanData(unittest.TestCase):
    def setUp(self):
        self.dinfo = CleanData(test_data)
    
    
