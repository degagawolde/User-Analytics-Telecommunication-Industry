import streamlit as st
import logging
import io
import os
import pandas as pd
from multipleapp import MultiApp
from apps import data_information  # import your app modules here


#logging configuration
logging.basicConfig(filename='./logfile.log', filemode='a',
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
    

app = MultiApp()

# Add all your application her


app.add_app("Dataset Information", data_information.data_info(original_df=original_df))

# The main app
app.run()
