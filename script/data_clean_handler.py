import numpy as np
import pandas as pd



def format_float(value):
    return f'{value:,.2f}'

def find_agg(df: pd.DataFrame, agg_column: str, agg_metric: str, col_name: str, top: int, order=False) -> pd.DataFrame:

    new_df = df.groupby(agg_column)[agg_column].agg(agg_metric).reset_index(name=col_name).\
        sort_values(by=col_name, ascending=order)[:top]

    return new_df

def convert_bytes_to_megabytes(df, bytes_data):
    """
        This function takes the dataframe and the column which has the bytes values
        returns the megabytesof that value
        
        Args:
        -----
        df: dataframe
        bytes_data: column with bytes values
        
        Returns:
        --------
        A series
    """

    megabyte = 1*10e+5
    df[bytes_data] = df[bytes_data] / megabyte

    return df[bytes_data]


def fix_missing_ffill(df, col):
    df[col] = df[col].fillna(method='ffill')
    return df[col]


def fix_missing_bfill(df, col):
    df[col] = df[col].fillna(method='bfill')
    return df[col]
