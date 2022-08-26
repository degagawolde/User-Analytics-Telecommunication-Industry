
# import packages
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


def user_engagement(df: pd.DataFrame):
    st.title('User Engegement Analysis')
#    st.write('show s')

    st.write('preparing data...')
    df = df.dropna()
 
    to_string = ['IMEI', 'IMSI', 'MSISDN/Number']

    for col in to_string:
        df[col] = df[col].astype('category')
        
    to_string = ['IMEI', 'IMSI', 'MSISDN/Number']

    for col in to_string:
        df[col] = df[col].astype('category')
    
    cleaner = CleanData(df)
    datainfo = DataFrameInformation(df)
        
    df = cleaner.handle_outliers(df,0.25,0.25)
    
    total_duration = df.groupby('MSISDN/Number').agg(
        {'Dur. (ms)': 'sum'}).reset_index().rename(columns={'Dur. (ms)': 'total_duration'})
    
    dl_columns = datainfo.get_column_with_string(df, 'DL \(Bytes\)')

    total_download = df.groupby(
        'MSISDN/Number').agg({c: 'sum' for c in dl_columns}).sum(axis=1)
    total_download = pd.DataFrame(total_download).reset_index().rename(
        columns={0: 'total_download'})

    ul_columns = datainfo.get_column_with_string(df, 'UL \(Bytes\)')
    total_upload = df.groupby(
        'MSISDN/Number').agg({c: 'sum' for c in ul_columns}).sum(axis=1)
    total_upload = pd.DataFrame(total_upload).reset_index().rename(
        columns={0: 'total_upload'})

    total_traffic = total_download.merge(total_upload, on='MSISDN/Number')
    
    total_data = pd.DataFrame(total_traffic['MSISDN/Number'])
    total_data['total_data'] = total_traffic['total_download'] + \
            total_traffic['total_upload']

    total_freq = df.groupby('MSISDN/Number').agg(
        {'Bearer Id': 'count'}).reset_index().rename(columns={'Bearer Id': 'total_freq'})

    new_df = total_data.merge(total_duration, on='MSISDN/Number')
    new_df = new_df.merge(total_freq, on='MSISDN/Number')
    new_df = new_df.select_dtypes(exclude='category')
    
    normalized_df = (new_df - new_df.mean())/new_df.std()
    
    Kmean = KMeans(n_clusters=3)
    Kmean.fit(normalized_df)

    centroids = Kmean.cluster_centers_
    
    # fig = px.scatter_3d(centroids_df, x=0, y=1, z=2, color=[3, 3, 3])
    fig = px.scatter_3d(normalized_df, x='total_data', y='total_duration', z='total_freq',
                        color=Kmean.labels_.astype(float))

    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
    st.write(fig)
