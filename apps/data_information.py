# import packages
import streamlit as st
import matplotlib.pyplot as plt
import missingno as msno
import pandas as pd
import logging
import sys
import os
import sys

# import custom packages
sys.path.append(os.path.abspath(os.path.join("../script")))
from script.get_missing_information import MissingInformation
from script.get_dataframe_information import DataFrameInformation
from script.data_clean_handler import CleanData
#logging configuration
logging.basicConfig(filename='./logfile.log', filemode='a',
                    encoding='utf-8', level=logging.DEBUG)

def data_info(original_df:pd.DataFrame):
    st.title('Dataset Information')
    st.write('This page show the skewness, missing percentage of the dataset.')
    
    data_info = DataFrameInformation(original_df)
    

    #get those who has missing values
    dataframe_info = data_info.get_skewness_missing_count(
        original_df).astype(str)

    if st.checkbox('Show Data Info'):
        st.subheader('Show data info')
        st.dataframe(dataframe_info)
    
    fig = plt.figure(figsize=(8,6))
    ax1 = fig.add_subplot(1,1,1)
    ax1.set_title('Shows missing data count')
    msno.bar(original_df, fontsize=12, ax=ax1);
    
    st.plotly_chart(fig, width=100)






