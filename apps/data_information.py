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
#logging configuration
logging.basicConfig(filename='./logfile.log', filemode='a',
                    encoding='utf-8', level=logging.DEBUG)

def data_info(df:pd.DataFrame):
    st.title('Dataset Information')
    st.write('This page show the skewness, missing percentage of the dataset.')
    
    data_info = DataFrameInformation(df)
    miss_info = MissingInformation(df)
    
    #get those who has missing values
    dataframe_info = data_info.get_skewness_missing_count(df).astype(str)
    mis_val_table_ren_columns = miss_info.missing_values_table(df)
    
    st.write("Your selected dataframe has " + str(df.shape[1]) + " columns.\n"
    "There are " + str(mis_val_table_ren_columns.shape[0]) +
    " columns that have missing values.")

    # if st.checkbox('Show Data Info'):
    st.dataframe(dataframe_info)
    
    fig = plt.figure(figsize=(8,6))
    ax1 = fig.add_subplot(1,1,1)
    ax1.set_title('### Shows missing data count')
    msno.bar(df, fontsize=12, ax=ax1)
    
    st.plotly_chart(fig, width=100)






