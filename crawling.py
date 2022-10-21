import requests
from datetime import datetime, timedelta
import pandas as pd
import os
import json
import time
from pathlib import Path

def date_range(start:str, end:str) -> list:
    start = datetime.strptime(start, "%Y-%m-%d")
    end = datetime.strptime(end, "%Y-%m-%d")
    dates = [(start + timedelta(days=i)).strftime("%Y%m%d") for i in range((end-start).days+1)]
    return dates


def crawling_seoul_climate(api_key:str, start_day:str, end_day:str) -> pd.DataFrame:

    fine_dust_api_result_data_dict = dict()
    dates = date_range(start_day, end_day)
    list_of_df = [] 
    
    for day in dates:

        url = f'http://openAPI.seoul.go.kr:8088/{api_key}/json/DailyAverageCityAir/1/25/{day}'
        response = requests.get(url)
        response_json = response.json()
        fine_dust_api_result_data_dict[day] = response_json['DailyAverageCityAir']['row']

        for i in fine_dust_api_result_data_dict[day]:
          df = pd.DataFrame.from_dict(i, orient='index')
          list_of_df.append(df)
        

    df_accum = pd.concat(list_of_df, axis=1) 
    
    return df_accum


def get_apikey(key_name:str, json_filename="secret.json") -> str:

    BASE_DIR = Path(__file__).resolve().parent
    json_filepath = os.path.join(BASE_DIR, json_filename)

    if(not os.path.isfile(json_filepath)):
        print("JSON File Not Found")
        raise FileNotFoundError

    with open(json_filepath) as f:
        json_p = json.loads(f.read())

    try:
        value=json_p[key_name]
        return value

    except KeyError:
        error_msg = "ERROR: Unvalid Key"
        return error_msg


def save_climate_data_to_csv():
    start = time.time()
    API_KEY = get_apikey("SEOUL_CLIMATE_API_KEY", json_filename="secret.json")
    start_day = "2020-08-01"
    last_day = "2021-08-01"
    fine_dust_data_df = crawling_seoul_climate(API_KEY, start_day, last_day)
    # fine_dust_data_df = fine_dust_data_df.T
    fine_dust_data_df.to_csv('./result.csv', sep=',', na_rep='NaN')
    print("실행 시간 :", time.time() - start)


save_climate_data_to_csv()