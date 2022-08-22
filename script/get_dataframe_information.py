import pandas as pd
import numpy as np

import sys, os

sys.path.append(os.path.abspath(os.path.join("./script")))

from get_missing_information import MissingInformation
class DataFrameInformation:
    
    def __init__(self,data:pd.DataFrame):
        self.data = data
        
    #calculate the skewness of the dataframe first
    def get_skewness(self,data:pd.DataFrame):
        skewness = data.skew(axis=0, skipna=True)
        df_skewness = pd.DataFrame(skewness)
        df_skewness = df_skewness.rename(
            columns={0: 'skewness'})
        
        return df_skewness

    #calculate skewness and missing value table
    def get_skewness_missing_count(self,data:pd.DataFrame):
        df_skewness = self.get_skewness(data)
        minfo = MissingInformation(data)
        
        mis_val_table_ren_columns = minfo.missing_values_table(data)
        df = pd.concat([df_skewness, mis_val_table_ren_columns], axis=1)
        df['Dtype'] = df['Dtype'].fillna('float64')
        df['% of Total Values'] = df['% of Total Values'].fillna(0.0)
        df['Missing Values'] = df['Missing Values'].fillna(0)
        df = df.sort_values(by='Missing Values', ascending=False)
        return df


