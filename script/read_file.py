import pandas as pd
import logging

logging.basicConfig(filename='../logfile.log', filemode='a',
                    encoding='utf-8', level=logging.DEBUG)

def read_csv_excel_file(file_path:str)->pd.DataFrame:
    print(file_path)
    try:
        if file_path.split('.')[-1] == 'csv':
            df_from_file = pd.read_csv(file_path)
        if file_path.split('.')[-1] == 'xlsx':
            df_from_file = pd.read_excel(file_path)
    except BaseException:
        logging.warning('file not found or wrong file format')
    
    return df_from_file
