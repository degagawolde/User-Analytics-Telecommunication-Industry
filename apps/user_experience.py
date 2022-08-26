
# import packages
from asyncore import write
from turtle import width
from script.data_clean_handler import CleanData
from script.get_dataframe_information import DataFrameInformation
from script.ploting_utils import PlotingUtils
import streamlit as st
from sklearn.cluster import KMeans
import plotly.express as px
import matplotlib.pyplot as plt
import missingno as msno
import pandas as pd
import numpy as np
import logging
import sys
import os
import re
import io

# import custom packages
sys.path.append(os.path.abspath(os.path.join("../script")))

#logging configuration
logging.basicConfig(filename='../logfile.log', filemode='a',
                    encoding='utf-8', level=logging.DEBUG)


def user_experience(df: pd.DataFrame):
    st.title('User Experience Analysis')

    to_string = ['MSISDN/Number', 'Handset Type']

    for col in to_string:
        df[col] = df[col].astype('category')
        
    selected_columns = [
        'MSISDN/Number',
        'TCP DL Retrans. Vol (Bytes)',
        'TCP UL Retrans. Vol (Bytes)',
        'Avg RTT DL (ms)', 'Avg RTT UL (ms)',
        'Avg Bearer TP UL (kbps)', 'Avg Bearer TP DL (kbps)',
        'Handset Type']
    
    selected_df = df[selected_columns]

    dinfo = DataFrameInformation(selected_df)
    missing_df = dinfo.get_skewness_missing_count(selected_df)
    st.dataframe(missing_df.astype(str))


    cleaner = CleanData(selected_df)
    #replace the missing wiht mode

    selected_df = cleaner.fill_mode(selected_df.copy(), selected_columns[1:])

    # drop the rows with null after mode fillinåg
    selected_df = selected_df.dropna(axis=0)
    selected_df.info()
