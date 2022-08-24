import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class PlotingUtils:
    def __init__(self,df:pd.DataFrame):
        self.df = df

    def plot_many_hist(self,df: pd.DataFrame, columns, color):
        for i, col in enumerate(columns):
            sns.displot(data=df, x=col, color=color,
                        kde=True, height=7, aspect=2)
            # plt.hist(df[col])
            plt.title(col)
            plt.show()

    def plot_hist(self,df: pd.DataFrame, column: str, color: str) -> None:
        # plt.figure(figsize=(15, 10))
        # fig, ax = plt.subplots(1, figsize=(12, 7))
        sns.displot(data=df, x=column, color=color, kde=True, height=7, aspect=2)
        plt.title(f'Distribution of {column}', size=20, fontweight='bold')
        plt.show()

    def plot_many_count_plot(self, df: pd.DataFrame, columns, amount):
        for col in columns:
            df[col].value_counts()[:amount].plot(
                kind='bar', color=['teal', 'green', 'blue'], title=col)
            plt.show()

    def plot_count(self,df: pd.DataFrame, column: str) -> None:
        plt.figure(figsize=(12, 7))
        sns.countplot(data=df, x=column)
        plt.title(f'Distribution of {column}', size=20, fontweight='bold')
        plt.show()

    def plot_bar(self,df: pd.DataFrame, x_col: str, y_col: str, title: str, xlabel: str, ylabel: str) -> None:
        plt.figure(figsize=(12, 7))
        sns.barplot(data=df, x=x_col, y=y_col)
        plt.title(title, size=20)
        plt.xticks(rotation=75, fontsize=14)
        plt.yticks(fontsize=14)
        plt.xlabel(xlabel, fontsize=16)
        plt.ylabel(ylabel, fontsize=16)
        plt.show()

    def plot_heatmap(self,df: pd.DataFrame, title: str, cbar=False) -> None:
        plt.figure(figsize=(12, 7))
        sns.heatmap(df, annot=True, cmap='viridis', vmin=0,
                    vmax=1, fmt='.2f', linewidths=.7, cbar=cbar)
        plt.title(title, size=18, fontweight='bold')
        plt.sh
        