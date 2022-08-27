from sqlalchemy import create_engine
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join("../script")))
from read_file import read_csv_excel_file


class HandleMysql:
    def __init__(self,user,password,host,database):
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        
    def create_connection(self):
        connections_path = "mysql+pymysql://"+self.user+":"+self.password+"@"+self.host+"/"+self.database
        engine = create_engine(connections_path)
        return engine.connect()
    
    def insert_into_db(self,data:pd.DataFrame,table_name:str):
        conn = self.create_connection()
        data.to_sql(table_name,conn,if_exists='append')

if __name__ == "__main__":
    eng_df = read_csv_excel_file('./data/user_engagement_score.csv')
    exp_df = read_csv_excel_file('./data/user_experience_score.csv')
    df = eng_df.merge(exp_df, on='MSISDN/Number')
    df['satisfaction_score'] = df['experience_score'] + df['engagement_score']
    df['satisfaction_score'] = df['satisfaction_score'].apply(lambda x: x/2)
    
        # conn = engine.connect()
    data = df[['MSISDN/Number', 'engagement_score',
            'experience_score', 'satisfaction_score']]
    handle_mysql = HandleMysql(user='root',password='root#123',host='localhost',database='telecom_data')
    handle_mysql.insert_into_db(data=data,table_name='user_satisfaction')
     