import configparser
from sqlalchemy import create_engine

db_config = configparser.ConfigParser()
db_config.read('/Users/max/Yandex.Disk.localized/Documents/Scripts/dashboards/config.txt')

engine = create_engine(db_config.get('database', 'con'))