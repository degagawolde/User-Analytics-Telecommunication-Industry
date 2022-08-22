import pandas as pd
import numpy as np

class MissingInformation:
    def __init__(self,df:pd.DataFrame):
        self.df = df
        
    def missing_values_table(self,df:pd.DataFrame)->pd.DataFrame:
        # Total missing values
        mis_val = df.isnull().sum()

        # Percentage of missing values
        mis_val_percent = 100 * df.isnull().sum() / len(df)

        # dtype of missing values
        mis_val_dtype = df.dtypes

        # Make a table with the results
        mis_val_table = pd.concat(
            [mis_val, mis_val_percent, mis_val_dtype], axis=1)

        # Rename the columns
        mis_val_table_ren_columns = mis_val_table.rename(
            columns={0: 'Missing Values', 1: '% of Total Values', 2: 'Dtype'})

        # Sort the table by percentage of missing descending
        mis_val_table_ren_columns = mis_val_table_ren_columns[
            mis_val_table_ren_columns.iloc[:, 1] != 0].sort_values(
            '% of Total Values', ascending=False).round(1)

        # Print some summary information
        print("Your selected dataframe has " + str(df.shape[1]) + " columns.\n"
            "There are " + str(mis_val_table_ren_columns.shape[0]) +
            " columns that have missing values.")

        # Return the dataframe with missing information
        return mis_val_table_ren_columns

    def percent_missing(self,df:pd.DataFrame):

        # Calculate total number of cells in dataframe
        totalCells = np.product(df.shape)

        # Count number of missing values per column
        missingCount = df.isnull().sum()

        # Calculate total number of missing values
        totalMissing = missingCount.sum()

        return totalCells, missingCount, totalMissing
