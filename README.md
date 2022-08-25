# User-Analytics-Telecommunication-Industry

# Objective
- To analysis a telecommunication dataset to identfy weather buying TellCo mobile service provider is profitable or not
# Data Preparation
- The dataset can be found [here](https://docs.google.com/spreadsheets/d/1e1lgy4vHLlJ4zcful66AiORSLWlqMeSe/edit?usp=sharing&ouid=103241713684165615552&rtpof=true&sd=true) and its attribute description [here](https://docs.google.com/spreadsheets/d/1wY7YZwyZ_r_8xMUe_N2ZQled4RjP0_T6/edit?rtpof=true&sd=true#gid=497912695)

- The dataset is provided in excell format which can be read with pandas python library

```
import pandas as pd
df_from_excell = pd.read_excel('../data/Week1_challenge_data_source.xlsx')
```
- After reading the data, we should then identify what column exist and their data type.
- If the data type is wrongly changed to other type it should be casted to the proper type

***Handling Missing*** 

- Drop column with missing value percentage > 30%
```
    def drop_column(self, df: pd.DataFrame, columns) -> pd.DataFrame:
        for col in columns:
            df = df.drop([col], axis=1)
        return df
```
- Fill missing values with mean, median, mode, bfill, ffill, etc
- Mean and median is for numeric column only.
- Mean/Median/Mode Imputation for  less than 3% missing values. mode is good when the data distribution is skewed, and mean.media is good for data that are not skewed.
- For the columns {Start, Start ms,End ms,Dur. (ms).1, Dur. (ms),Avg Bearer TP DL (kbps),Avg Bearer TP UL (kbps), Total DL (Bytes), Avg Bearer TP DL (kbps), ),Total UL (Bytes), Activity Duration DL (ms),Activity Duration UL (ms), End } are related to time/duration and have 1 missing values. droping the row with the missing values will not be a problem
- For the text column(Handset Manufacturer, Handset Type, and last location name) are not numeric, mode filling can be used and we can found their mode easily 

```
    def fill_mode(self, df: pd.DataFrame, columns) -> pd.DataFrame:
        for col in columns:
            df[col] = df[col].fillna(df[col].mode()[0])
        return df
```
# User Overview Analysis
XDR collects and correlates data across email, endpoints, servers, cloud workloads, and networks, enabling visibility and context into advanced threats [here](https://www.cisco.com/c/en/us/products/security/what-is-xdr.html). User behaviour can be tracked through the social media, google, email, youtube, netflix, gaming, other using the XDR session.

***Top 10 Handset Type***
```
handset_count = df['Handset Type'].value_counts()
handset_count[:10].plot(kind='bar', color=['teal', 'green', 'blue','purple','pink'])

```
![top10handset](https://github.com/degagawolde/User-Analytics-Telecommunication-Industry/blob/main/images/top10handset.png)

***Top 3 Handset Manufacturer***
```
handset_manufacturer = df['Handset Manufacturer'].value_counts()
handset_manufacturer[:3].plot(
    kind='bar', color=['teal', 'green', 'blue'])
```
![top3manufacturer](https://github.com/degagawolde/User-Analytics-Telecommunication-Industry/blob/main/images/top3manufacturer.png)

***Top 5 handset type per top 3 manufacturer***
```
handset_man= df[df['Handset Manufacturer'].isin(['Apple','Samsung','Huawei'])]
handset = handset_man.groupby('Handset Manufacturer')['Handset Type'].value_counts()
apple = handset.Apple[:5]
sumsung = handset.Samsung[:5]
huawei = handset.Huawei[:5]
```
```
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
```
![top 5 handset per top 3 manufacturer](https://github.com/degagawolde/User-Analytics-Telecommunication-Industry/blob/main/images/top5hansetpermanufacture.png)

# User Engagement Analysis
User engagement analysis is used to determine how a give user is engeged to a given application. There may be different metrics to determinge the egagement level. For example, total duration of session, total traffic of a session, and frequency of a session can determine user engagement for a telecom service provider. 
1. Duration of a session
```
total_duration = df.groupby('MSISDN/Number').agg(
    {'Dur. (ms)': 'sum'}).reset_index().rename(columns={'Dur. (ms)': 'total_duration'})
```
```
sorted_df = total_duration.sort_values('total_duration',ascending=False)[:10]
sorted_df.plot.bar()
```
![top 10 total duration](https://github.com/degagawolde/User-Analytics-Telecommunication-Industry/blob/main/images/top10duration.png)
# Experience Analytics
# Satisfaction Analysis
