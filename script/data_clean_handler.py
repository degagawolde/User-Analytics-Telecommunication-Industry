import numpy as np
import pandas as pd


class CleanData:
    def __init__(self,df:pd.DataFrame):
        self.df = df
        
    def format_float(self,value):
        return f'{value:,.2f}'


    def convert_bytes_to_megabytes(self, df:pd.DataFrame, bytes_data):

        megabyte = 1*10e+5
        df[bytes_data] = df[bytes_data] / megabyte

        return df[bytes_data]

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
    
    def fill_mode(self, df: pd.DataFrame, columns) -> pd.DataFrame:
        for col in columns:
            df[col] = df[col].fillna(df[col].mode()[0])
        return df
