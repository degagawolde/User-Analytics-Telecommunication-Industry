# import packages
import missingno as msno
import matplotlib.pyplot as plt
import plotly.express as px
from sklearn.cluster import KMeans
import streamlit as st

import os
import sys
import logging
import numpy as np
import pandas as pd


#logging configuration
logging.basicConfig(filename='../logfile.log', filemode='a',
                    encoding='utf-8', level=logging.DEBUG)


def user_satisfaction(df: pd.DataFrame):
    st.title('User Satisfaction Analysis')
    try:
        eng_df = pd.read_csv('./data/user_engagement_score.csv')
        exp_df = pd.read_csv('./data/user_experience_score.csv')
    except BaseException:
        logging.error('file not found or wrong format')
        
    df = eng_df.merge(exp_df,on='MSISDN/Number')
    df['satisfaction_score'] = df['experience_score'] + df['engagement_score']
    df['satisfaction_score'] = df['satisfaction_score'].apply(lambda x: x/2)

    st.write('### Top 10 most satisfied user')
    dat_df = df[['MSISDN/Number', 'satisfaction_score']
                ].sort_values('satisfaction_score', ascending=False)
    
    st.bar_chart(dat_df[:10], x='MSISDN/Number', y='satisfaction_score')
    
    eng_exp = df[['engagement_score', 'experience_score']]

    normalized_df = (eng_exp-eng_exp.mean())/eng_exp.std()

    Kmean = KMeans(n_clusters=2)
    Kmean.fit(normalized_df)

    centroids = Kmean.cluster_centers_
    
    fig = plt.figure()
    ax = fig.add_subplot(111)

    
    ax.scatter(normalized_df['engagement_score'], normalized_df['experience_score'],
                c=Kmean.labels_.astype(float), s=50, alpha=0.5)

    ax.scatter(centroids[:, 0], centroids[:, 1], c='red', s=50)
    ax.set_xlabel('engagement_score')
    ax.set_ylabel('experience_score')
    
    st.write(fig)
