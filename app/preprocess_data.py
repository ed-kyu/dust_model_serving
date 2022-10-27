import pandas as pd
import yaml
import datetime as dt
import os
from pathlib import Path

def make_map_dict(values):
    map_dict = {}
    cnt = 0
    for region in values:
        map_dict[region] = cnt
        cnt += 1
    return map_dict


def preprocess_data():
    file_path = Path(__file__).resolve().parent
    with open(os.path.join(file_path.parent, 'config.yaml'), 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    start_day = config['CRAWLING_START_DAY']
    last_day = config['CRAWLING_LAST_DAY']
    df = pd.read_csv(os.path.join(file_path.parent, f'dust_data_{start_day}_to_{last_day}.csv'), index_col=0)

    df = df.rename(columns={
        'MSRDT_DE': '날짜',
        'MSRRGN_NM': '지역권',
        'MSRSTE_NM': '지역',
    })

    df['날짜'] = df['날짜'].astype(str)
    df['날짜'] = pd.to_datetime(df['날짜'])

    date_to_range_dict = dict()

    df['날짜'].iloc[0], df['날짜'].iloc[-1]
    start_day = df['날짜'].iloc[0]
    end_day = df['날짜'].iloc[-1]
    dates = pd.date_range(start_day,end_day,freq='D')

    for i, date in enumerate(dates):
        date_to_range_dict[date] = i

    df['날짜'] = df['날짜'].map(date_to_range_dict)

    df1 = df[(df['PM10'] != 0.0) & (df['PM10'] < 250)]
    df1 = df1[(df1['CO'] < 3)]

    # not_number_list = ['지역권', '지역']
    region_set = set(df1['지역권'].values)
    city_set = set(df1['지역'].values)
    region_set, city_set

    map_1 = make_map_dict(region_set)
    map_2 = make_map_dict(city_set)

    df2 = df1.copy()
    df2['지역권'] = df2['지역권'].map(map_1)
    df2['지역'] = df2['지역'].map(map_2)

    df_test_lst = []
    for i in range(25):
        # df_test = df2[df2['지역']==9] # 강남구
        df_test = df2[df2['지역']==i]
        df_test_lst.append(df_test)

    return df_test_lst


if __name__ == '__main__':
    
    preprocess_data()