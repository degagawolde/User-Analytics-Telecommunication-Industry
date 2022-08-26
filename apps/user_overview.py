
# import packages
from sklearn.decomposition import PCA
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
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
from script.ploting_utils import PlotingUtils
from script.data_clean_handler import CleanData

#logging configuration
logging.basicConfig(filename='../logfile.log',filemode='a',
                    encoding='utf-8', level=logging.DEBUG)
                    
def user_overview(clean_data:pd.DataFrame):
    st.title('User Overview Analysis')
#    st.write('show s')
    
    st.write('preparing data...')
    clean_data = clean_data.dropna()
        
    # use the customer data
    cleaner = CleanData(clean_data)
    pltu = PlotingUtils(clean_data)

    #casting dtype
    to_string = ['IMEI', 'IMSI', 'MSISDN/Number']
    clean_data = cleaner.convert_dtype(clean_data,to_string,'category')

    # plot top 1o handset
    handset_count = clean_data['Handset Type'].value_counts()
    df = pd.DataFrame(handset_count[:10])
    st.write('Shows most used top 10 handset type')
    st.bar_chart(df)
    
    handset_manufacturer = clean_data['Handset Manufacturer'].value_counts()
    df = pd.DataFrame(handset_manufacturer[:3])
    st.write('Shows the top 3 handset manufacturer')
    st.bar_chart(df)
    
    handset_man= clean_data[clean_data['Handset Manufacturer'].isin(['Apple','Samsung','Huawei'])]
    handset = handset_man.groupby('Handset Manufacturer')['Handset Type'].value_counts()
    apple = handset.Apple[:5]
    sumsung = handset.Samsung[:5]
    huawei = handset.Huawei[:5]
    
    fig, ax = plt.subplots(1, 3)

    ax[0].bar(apple.keys(), apple.values, tick_label=apple.keys(),
              width=.5, color=['blue', 'green', 'orange'])
    ax[0].set_title('Apple')
    ax[0].tick_params(axis='x', labelrotation=90)

    ax[1].bar(sumsung.keys(), sumsung.values, tick_label=sumsung.keys(),
              width=0.8, color=['blue', 'green', 'orange'])
    ax[1].set_title('Sumsung')
    ax[1].tick_params(axis='x', labelrotation=90)

    ax[2].bar(huawei.keys(), huawei.values, tick_label=huawei.keys(),
              width=0.8, color=['blue', 'green', 'orange'])
    ax[2].set_title('Huawei')
    ax[2].tick_params(axis='x', labelrotation=90)
    plt.subplots_adjust(left=0.2, right=0.99,
                        bottom=0.2, top=0.6,
                        wspace=0.6, hspace=0.4)

    st.write('### Top 5 handsets per top 3 manufacturers')
    st.write(fig)

    st.write('### Numerical Column Correlation')
    numerical_df = clean_data.select_dtypes(include='float64')
    corr = numerical_df.corr()
    
    fig, ax = plt.subplots()
    # plot the heatmap
    sns.heatmap(corr, cmap='Blues',
                xticklabels=corr.columns,
                yticklabels=corr.columns,ax=ax)
   
    st.write(fig)
    
    plt.rcParams["figure.figsize"] = (12, 6)

   # You must normalize the data before applying the fit method
    df_normalized = (numerical_df - numerical_df.mean()) / numerical_df.std()
    pca = PCA(n_components=numerical_df.shape[1])
    principalDf = pca.fit_transform(df_normalized)

    principalDf = pd.DataFrame(data=principalDf, columns=['PC%s' % _ for _ in range(
        len(df_normalized.columns))])

    st.write("### Dimensionality Reduction")
    st.write("###### Out of the 36 columns, we select 27 that can replace 99% of the information")
    fig, ax = plt.subplots()
    xi = np.arange(1, 37, step=1)
    y = np.cumsum(pca.explained_variance_ratio_)

    plt.ylim(0.0, 1.1)
    plt.plot(xi, y, marker='o', linestyle='--', color='b')

    plt.xlabel('Number of Components')
    # change from 0-based array index to 1-based human-readable label
    plt.xticks(np.arange(0, 37, step=1))
    plt.ylabel('Cumulative variance (%)')
    plt.title('The number of components needed to explain variance')

    plt.axhline(y=0.99, color='r', linestyle='-')
    plt.text(0.5, 0.95, '99% cut-off threshold', color='red', fontsize=16)

    ax.grid(axis='x')
    st.write(fig)
