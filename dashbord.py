# import packages
import missingno as msno
import pandas as pd
import logging
import sys
import os
import re
import io

# import custom packages
sys.path.append(os.path.abspath(os.path.join("./script")))
from data_clean_handler import CleanData
from get_dataframe_information import DataFrameInformation
from get_missing_information import MissingInformation

#logging configuration
logging.basicConfig(filename='./logfile.log',filemode='a',
                    encoding='utf-8', level=logging.DEBUG)
                
# read the file to dataframe
try:
    original_df = pd.read_csv('./data/Week1_challenge_data_source.csv')
except BaseException:
    logging.warning('file not found or wrong file format')

buffer = io.StringIO()
original_df.info(buf=buffer)
s = buffer.getvalue()
with open("df_info.txt", "w", encoding="utf-8") as f:
    f.write(s)
    
# use the customer data
cleaner = CleanData(original_df)
miss_info = MissingInformation(original_df)
data_info = DataFrameInformation(original_df)

#get those who has missing values
dataframe_info =  data_info.get_dataframe_information(original_df)

msno.heatmap(df_from_excell)
msno.matrix(df_from_excell)

#casting dtype
to_string = ['IMEI', 'IMSI', 'MSISDN/Number']
clean_data = cleaner.convert_dtype(original_df,to_string,'category')

# handle missing


#handle outliers 

# user overview

# calculate engagement

# calculate experience


# calculate satisfaction


# save to mysql database

