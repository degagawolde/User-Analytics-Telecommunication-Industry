import numpy as np
import pandas as pd


class CleanData:
    def __init__(self,df:pd.DataFrame):
        self.df = df
        
    def format_float(self,value):
        return f'{value:,.2f}'

    def find_agg(self, agg_column: str, agg_metric: str, col_name: str, top: int, order=False) -> pd.DataFrame:

        new_df = self.df.groupby(agg_column)[agg_column].agg(agg_metric).reset_index(name=col_name).\
            sort_values(by=col_name, ascending=order)[:top]

        return new_df

    def convert_bytes_to_megabytes(self, bytes_data):

        megabyte = 1*10e+5
        self.df[bytes_data] = self.df[bytes_data] / megabyte

        return self.df[bytes_data]

    def fix_missing_ffill(self, col):
        self.df[col] = self.df[col].fillna(method='ffill')
        return self.df[col]

    def fix_missing_bfill(self, col):
        self.df[col] = self.df[col].fillna(method='bfill')
        return self.df[col]
