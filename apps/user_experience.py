
# import packages
from asyncore import write
from turtle import width
from script.data_clean_handler import CleanData
from script.get_dataframe_information import DataFrameInformation
from script.ploting_utils import PlotingUtils
import streamlit as st
from sklearn.cluster import KMeans
from scipy.stats.mstats import winsorize
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
    missing_df = dinfo.get_skewness_missing_count(selected_df).astype(str)
    st.dataframe(missing_df)


    cleaner = CleanData(selected_df)
    #replace the missing wiht mode

    selected_df = cleaner.fill_mode(selected_df.copy(), selected_columns[1:])

    # drop the rows with null after mode fillinåg
    selected_df = selected_df.dropna(axis=0)
    
 

    selected_columns = selected_df.select_dtypes(include='float64').columns
    for col in selected_columns:
        selected_df[col] = winsorize(selected_df[col], (0.01, 0.15))

    # for col in selected_df.columns.tolist()[1:-1]:
    #     st.bar_chart(selected_df[col])#.plot(kind='box', title=col, figsize=(10, 6))
    agg_df = selected_df.groupby(
            'MSISDN/Number').agg({col: 'sum' for col in selected_df.columns[1:-1]}).reset_index()
    paired_columns = [
        ['TCP DL Retrans. Vol (Bytes)',	'TCP UL Retrans. Vol (Bytes)'],
        ['Avg RTT DL (ms)',	'Avg RTT UL (ms)'],
        ['Avg Bearer TP UL (kbps)',	'Avg Bearer TP DL (kbps)']]

    total_df = pd.DataFrame()

    total_df['MSISDN/Number'] = agg_df['MSISDN/Number']

    total_df[paired_columns[0][0].split(
        ' ')[0]] = agg_df[paired_columns[0][0]] + agg_df[paired_columns[0][1]]
    total_df[paired_columns[1][0].split(
        ' ')[1]] = agg_df[paired_columns[1][0]] + agg_df[paired_columns[1][1]]
    total_df[paired_columns[2][0].split(
        ' ')[1]] = agg_df[paired_columns[2][0]] + agg_df[paired_columns[2][1]]

    total_df = total_df.rename(columns={'RTT': 'Average RTT'})
    total_df = total_df.rename(columns={'Bearer': 'Average Throughput'})

    for col in total_df.columns[1:]:
        st.bar_chart(total_df.sort_values(col, ascending=False)[
            col][:10])#.plot(kind='bar', title=col)
    total_df = total_df.set_index('MSISDN/Number')
    normalized_df = (total_df - total_df.mean())/total_df.std()

    Kmean = KMeans(n_clusters=3)
    Kmean.fit(normalized_df)

    centroids = Kmean.cluster_centers_
    st.write(str(centroids))
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    x_vals = normalized_df['TCP']
    y_vals = normalized_df['Average RTT']
    z_vals = normalized_df['Average Throughput']

    # # Plot the values

    # ax.scatter(centroids_df[0], centroids_df[1], centroids_df[2], c='red', s=100)
    ax.scatter(x_vals, y_vals, z_vals,
               c=Kmean.labels_.astype(float), s=50, alpha=0.5)

    ax.set_xlabel('TCP Retransmission')
    ax.set_ylabel('Average RTT')
    ax.set_zlabel('Averate Throughput')
    st.write(fig)
