import streamlit as st
import logging
import io
import os
import pandas as pd
from multipleapp import MultipleApp
from apps import data_information, user_overview, user_engagement,user_experience # import your app modules here


#logging configuration
logging.basicConfig(filename='./logfile.log', filemode='a',
                    encoding='utf-8', level=logging.DEBUG)

# read the file to dataframe
try:
    original_df = pd.read_csv('./data/Week1_challenge_data_source.csv')
    clean_data = pd.read_csv('./data/clean_data.csv')
except BaseException:
    logging.warning('file not found or wrong file format')
    # read the file to dataframe

buffer = io.StringIO()
original_df.info(buf=buffer)
s = buffer.getvalue()
with open("df_info.txt", "w", encoding="utf-8") as f:
    f.write(s)
    

app = MultipleApp()

# Add all your application her

app.add_app("Dataset Information", data_information.data_info, original_df)
app.add_app('User Overview Analysis', user_overview.user_overview, clean_data)
app.add_app('User Engegement Analysis', user_engagement.user_engagement, clean_data)
app.add_app('User Experience Analysis', user_experience.user_experience, original_df)
app.add_app('User Satisfaction Analysis', user_overview.user_overview, clean_data)
# The main app
app.run()
