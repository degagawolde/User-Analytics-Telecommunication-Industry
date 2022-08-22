import pandas as pd
import numpy as np

class DataFrameInformation:
    
    def __init__(self,data:pd.DataFrame):
        self.data = data
        
    #calculate the skewness of the dataframe first
    def get_skewness(self):
        skewness = self.data.skew(axis=0, skipna=True)
        df_skewness = pd.DataFrame(skewness)
        df_skewness = df_skewness.rename(
            columns={0: 'skewness'})
        
        return df_skewness

#calculate skewness and missing value table
def get_skewness_missing_count(df_skewness, mis_val_table_ren_columns):
    df = pd.concat([df_skewness, mis_val_table_ren_columns], axis=1)
    df['Dtype'] = df['Dtype'].fillna('float64')
    df['% of Total Values'] = df['% of Total Values'].fillna(0.0)
    df['Missing Values'] = df['Missing Values'].fillna(0)
    df = df.sort_values(by='Missing Values', ascending=False)
    return df


