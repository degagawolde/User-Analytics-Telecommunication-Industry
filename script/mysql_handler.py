from sqlalchemy import create_engine
from read_file import read_csv_excel_file

connections_path = "mysql+pymysql://root:root#123@localhost/telecom_data"
engine = create_engine(connections_path)

eng_df = read_csv_excel_file('../data/user_engagement_score.csv')
exp_df = read_csv_excel_file('../data/user_experience_score.csv')

df = eng_df.merge(exp_df, on='MSISDN/Number')

df['satisfaction_score'] = df['experience_score'] + df['engagement_score']
df['satisfaction_score'] = df['satisfaction_score'].apply(lambda x: x/2)

# conn = engine.connect()
data = df[['MSISDN/Number', 'engagement_score',
           'experience_score', 'satisfaction_score']]
data.to_sql('eng_exp_sat',engine.connect(),if_exists='append')
