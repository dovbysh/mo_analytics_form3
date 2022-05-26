from datetime import datetime
import os

import pytz


timezone = pytz.timezone('Europe/Moscow')
today = datetime.now().astimezone(timezone)

def remove_archive(filename):
    os.remove(filename)

def check_archive_update_time(time: str = '3:00'):
    current_hour = today.hour
    current_minute = today.minute
    
    return f'{current_hour}:{current_minute}' == time

    
if __name__ == '__main__':
    print(check_archive_update_time('14:32'))