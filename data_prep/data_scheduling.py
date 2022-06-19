from datetime import datetime
import os

import pytz


timezone = pytz.timezone('Europe/Moscow')
# today = datetime.now().astimezone(timezone)

def remove_archive(filename):
    if filename not in os.listdir():
        os.remove(filename)

def check_archive_update_time(time: str = '3:00'):
    today = datetime.now().astimezone(timezone)
    current_hour = today.hour
    current_minute = today.minute
    return f'{current_hour}:{current_minute}' == time

def check_increment_update_time_hourly(minutes_to_update: int=2) -> bool:
    today = datetime.now().astimezone(timezone)
    return not (today.minute % minutes_to_update)
    
if __name__ == '__main__':
    print(check_archive_update_time('14:32'))