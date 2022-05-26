import json
import requests
from datetime import datetime, timedelta
import pandas as pd
import os
from time import sleep
from tqdm.auto import tqdm

from data_prep.df_optimizers import optimize

host = "http://149.126.169.223:4410"

method_dict = {
    'getMarshWorkResult': {'path': '/mta/getMarshWorkResult.php', 'params': {'fmt': 'json', 'nd_from': '', 'nd_to': ''}}, 
    'getHourBusState': {'path': '/mta/getHourBusState.php', 'params': {'fmt': 'json', 'nd': 0}}, 
    'getHourWorkResult': {'path': '/mta/getHourWorkResult.php', 'params': {'fmt': 'json', 'nd': 0}}, 
}

method = list(method_dict.keys())[1]

def get_data(host, 
             method,
             method_dict,
             start_date=datetime.today()-timedelta(days=3), 
             end_date=datetime.today()):
    
    headers = {
    'Content-type': 'application/json',
    'Authorization': 'Basic UE9XUkJJOlBPV1JCSQ==', 
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.90 Safari/537.36'
    }
    
    url = host + method_dict[method]['path']
    if method == 'getMarshWorkResult':
        method_dict[method]['params']['nd_from'] = start_date.strftime('%Y-%m-%d')
        method_dict[method]['params']['nd_to'] = end_date.strftime('%Y-%m-%d')
        r = requests.get(
            url=url, 
            headers=headers, 
            params=method_dict[method]['params'], 
            timeout=5
            )
        print(f'Status code {r.status_code}')
        data = r.json()
        return data
        
    else:
        date_range = (end_date - start_date)
        print(f'Start date {start_date}')
        print(f'End date {end_date}')
        print(f'Date range {date_range.days}')
        day_list = [start_date + timedelta(days=i) for i in range(date_range.days + 1)]
        data = []
        for day in tqdm(day_list, position=0, leave=True):
            method_dict[method]['params']['nd'] = day
            try:
                r = requests.get(
                    url=url, 
                    headers=headers, 
                    params=method_dict[method]['params'], 
                    timeout=10
                    )
                # print(f'Status code in loop {r.status_code}')
            except requests.ConnectTimeout as e:
                print(e)
            data += r.json()
            sleep(1) 
        return data

def store_data(data, filename='data_archive.feather'):
    df = pd.DataFrame(data=data)
    df = optimize(df, ['NariadDate'])
    df.to_feather(filename)
    
def load_data_from_file(filename='data_archive.feater'):
    data = pd.read_feather(filename)
    data = optimize(data, ['NariadDate'])
    return data

def update_data(initial_days_offset=10, days_offset=3):
    if 'data_archive.feather' not in os.listdir('./'):
        start_date = datetime.today() - timedelta(days=initial_days_offset)
        end_date = datetime.today()
        archive_data = get_data(host, method, method_dict, start_date, end_date)
        store_data(archive_data, 'data_archive.feather')
        print(f'Download {initial_days_offset} days archive data')
        df_archive = pd.DataFrame(data=archive_data)
    else:
        archive_data = load_data_from_file('data_archive.feather')
        df_archive = archive_data #pd.DataFrame(data=archive_data)
        
    start_date = datetime.today() - timedelta(days=days_offset)
    end_date = datetime.today()
    
    increment_data = get_data(host, method, method_dict, start_date, end_date)
    print(f'Download last {days_offset} days data')
    
    df_increment = pd.DataFrame(data=increment_data)
    df_increment = optimize(df_increment, ['NariadDate'])
    
    print(' --------------- DF archive --------------- ')
    print(df_archive)
    print(' --------------- DF increment --------------- ')
    print(df_increment)
    
    df_updated = pd.concat([df_archive, df_increment], axis=0, ignore_index=True).\
        drop_duplicates(['NariadDate','minIndex', 'rg_id', 'mr_id', 'crr_id'],keep='last').reset_index(drop=True)
    
    df_updated = optimize(df_updated, ['NariadDate'])
    df_updated.to_feather('fresh_data_dump.feather')

    return df_updated

if __name__ == '__main__':
    df = update_data()
    print(' --------------- DF TOTAL --------------- ')
    print(df)