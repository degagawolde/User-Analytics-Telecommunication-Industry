
# import packages
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

# import custom packages
sys.path.append(os.path.abspath(os.path.join("../script")))
from script.data_clean_handler import CleanData
from script.get_dataframe_information import DataFrameInformation

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
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Generate the values
    x_vals = normalized_df['total_data']
    y_vals = normalized_df['total_duration']
    z_vals = normalized_df['total_freq']

    # # Plot the values

    # ax.scatter(centroids_df[0], centroids_df[1], centroids_df[2], c='red', s=100)
    ax.scatter(x_vals, y_vals, z_vals,
            c=Kmean.labels_.astype(float), s=50, alpha=0.5)

    ax.set_xlabel('total data')
    ax.set_ylabel('total duration')
    ax.set_zlabel('total freq')
    st.write(fig)
    
    st.write('### Elbow Method***')
    st.write("In the Elbow method, the the number of clusters(K) is varied from 1 – n. For each value of K, we  calculate WCSS(Within-Cluster Sum of Square), it is also called inertia. WCSS is the sum of squared distance between each point and the centroid in a cluster. When we plot the WCSS with the K value, the plot looks like an Elbow. As the number of clusters increases, the WCSS value will start to decrease. WCSS value is largest when K=1. When we analyze the graph we can see that the graph will rapidly change at a point and thus creating an elbow shape. From this point, the graph starts to move almost parallel to the X-axis. The K value corresponding to this point is the optimal K value or an optimal number of clusters.")
             
    st.image("https://editor.analyticsvidhya.com/uploads/43191elbow_img%20(1).png",width=400)
    st.write("1. Distortion: It is calculated as the average of the squared distances from the cluster centers of the respective clusters. Typically, the Euclidean distance metric is used.")
    st.write("2. Inertia: It is the sum of squared distances of samples to their closest cluster center.")

    st.write("We iterate the values of k from 1 to 9 and calculate the values of distortions for each value of k and calculate the distortion and inertia for each value of k in the given range.")
    st.write("To determine the optimal number of clusters, we have to select the value of k at the “elbow” ie the point after which the distortion/inertia start decreasing in a linear fashion. Thus for the given data, we conclude that the optimal number of clusters for the data is 3.")
    
    selected_columns = datainfo.get_column_with_string(df, 'Bytes')
    app_df = df[['MSISDN/Number']+selected_columns]
    
    paired_columns = []
    for i in range(len(selected_columns)//2):
        paired_columns.append([selected_columns[2*i], selected_columns[2*i+1]])
        
    agg_app_df = app_df.groupby(
        'MSISDN/Number').agg({c: 'sum' for c in selected_columns})

    agg_app_df = agg_app_df.reset_index()
    
    total_df = pd.DataFrame()

    total_df['MSISDN/Number'] = agg_app_df['MSISDN/Number']
    for col in paired_columns:
        total_df[col[0].split(' ')[0]] = agg_app_df[col[0]] + agg_app_df[col[1]]
    
    st.write("### 2. Top 10 most engaged user per application")
    for col in total_df.columns[1:]:
        df = total_df.sort_values(col, ascending=False)[
            col][:10]
        st.bar_chart(df)
        
    st.write("### 3. Top 3 most used applitaction")
    sum_df = total_df.loc[:, total_df.columns != 'MSISDN/Number']

    sum_df = sum_df.loc[:, sum_df.columns != 'Total']
    sum_df = pd.DataFrame(sum_df.sum(), columns=['sum'])
    st.bar_chart(sum_df[:3])
        
