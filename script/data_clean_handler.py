import numpy as np
import pandas as pd

import sys, os

import logging

sys.path.append(os.path.abspath(os.path.join("./script")))


from get_dataframe_information import DataFrameInformation

class CleanData:
    def __init__(self,df:pd.DataFrame):
        self.df = df
        logging.basicConfig(filename='../logfile.log', filemode='a',
                            encoding='utf-8', level=logging.DEBUG)
        
    def format_float(self,value):
        return f'{value:,.2f}'

    def convert_bytes_to_megabytes(self, df:pd.DataFrame, columns):

        megabyte = 1*10e+5
        for col in columns:
            df[col] = df[col] / megabyte
        return df 

    def fix_missing_ffill(self, df: pd.DataFrame,col):
        df[col] = df[col].fillna(method='ffill')
        return df[col]
  
    def fix_missing_bfill(self, df: pd.DataFrame, col):
        df[col] = df[col].fillna(method='bfill')
        return df[col]
    
    def drop_column(self, df: pd.DataFrame, columns) -> pd.DataFrame:
        for col in columns:
            df = df.drop([col], axis=1)
        return df

    def drop_missing_count_greaterthan_20p(self,data:pd.DataFrame):
        data_info = DataFrameInformation(data)
        df = data_info.get_skewness_missing_count(data)
        not_fill = df[(df['% of Total Values'] >= 20.0)].index.tolist()
        df_clean = self.drop_column(data, not_fill)
         
        return df_clean
    
    def fill_mode(self, df: pd.DataFrame, columns) -> pd.DataFrame:
        for col in columns:
            df[col] = df[col].fillna(df[col].mode()[0])
        return df

    def fix_outlier(self,df:pd.DataFrame, columns):
        for column in columns:
            df[column] = np.where(df[column] > df[column].quantile(
                0.95), df[column].median(), df[column])
            
        return df
