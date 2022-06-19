import requests
from datetime import datetime, timedelta
import pandas as pd
import os
from time import sleep
from tqdm.auto import tqdm
from data_prep.data_scheduling import check_archive_update_time, check_increment_update_time_hourly
from data_prep.data_scheduling import timezone

from data_prep.df_optimizers import optimize
from main_config import ARCHIVE_DATA_FILENAME, FRESH_DATA_FILENAME, GET_DATA_UPDATE_INTERVAL, \
    INCREMENT_DAYS_OFFSET, INITIAL_DAYS_OFFSET

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
        try:
            r = requests.get(
                url=url, 
                headers=headers, 
                params=method_dict[method]['params'], 
                timeout=10
                )
            print(f'Status code {r.status_code}')
            data = r.json()
            return data
        except requests.exceptions.ReadTimeout as re:
            print(re)
            return {}
        except requests.exceptions.ConnectTimeout as ce:
            print(ce)
            return {}
        
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
                data += r.json()
                # print(f'Status code in loop {r.status_code}')
            except requests.exceptions.ReadTimeout as re:
                print(re)
                continue
            except requests.exceptions.ConnectTimeout as ce:
                print(ce)
                continue
            sleep(1) 
        return data

def store_data(data, filename=ARCHIVE_DATA_FILENAME):
    df = pd.DataFrame(data=data)
    df = optimize(df, ['NariadDate']).reset_index()
    df.to_feather(filename)
    
def load_data_from_file(filename=ARCHIVE_DATA_FILENAME):
    data = pd.read_feather(filename)
    data = optimize(data, ['NariadDate'])
    return data

    
def is_arch_data_uptodate(filename=ARCHIVE_DATA_FILENAME):
    data = pd.read_feather(filename)
    if len(data):
        today = datetime.now().astimezone(timezone)
        if data['NariadDate'].iloc[-1].day == today.day:
            print('Data archive up to date')
            return True
    print('Data archive is outdated')
    return False
    

def update_data(
    initial_days_offset=INITIAL_DAYS_OFFSET, 
    increment_days_offset=INCREMENT_DAYS_OFFSET, 
    data_arch=ARCHIVE_DATA_FILENAME, 
    data_fresh=FRESH_DATA_FILENAME):
    if data_fresh not in os.listdir('./') or check_increment_update_time_hourly():
        if data_arch not in os.listdir('./') or check_archive_update_time() or not is_arch_data_uptodate():
            start_date = datetime.today() - timedelta(days=initial_days_offset)
            end_date = datetime.today()
            archive_data = get_data(host, method, method_dict, start_date, end_date)
            store_data(archive_data, data_arch)
            print(f'Download {initial_days_offset} days archive data')
            df_archive = pd.DataFrame(data=archive_data)
        else:
            archive_data = load_data_from_file(data_arch)
            df_archive = archive_data #pd.DataFrame(data=archive_data)
        
        start_date = datetime.today() - timedelta(days=increment_days_offset)
        end_date = datetime.today()
        increment_data = get_data(host, method, method_dict, start_date, end_date)
        print(f'Download last {increment_days_offset} days data')
    
        df_increment = pd.DataFrame(data=increment_data)
        df_increment = optimize(df_increment, ['NariadDate'])
    
        print(' --------------- DF archive --------------- ')
        print(df_archive)
        print(' --------------- DF increment --------------- ')
        print(df_increment)
    
        df_updated = pd.concat([df_archive, df_increment], axis=0, ignore_index=True)\
            .drop_duplicates(['NariadDate','minIndex', 'rg_id', 'mr_id', 'crr_id'],keep='last').reset_index(drop=True)
        df_updated = optimize(df_updated, ['NariadDate'])
        df_updated.to_feather(FRESH_DATA_FILENAME)

        return df_updated

if __name__ == '__main__':
    while True:
        update_data()
        sleep(GET_DATA_UPDATE_INTERVAL)