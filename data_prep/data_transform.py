import pandas as pd

from loguru import logger
from data_prep.df_optimizers import optimize

# rough_df = pd.read_excel(io='/Users/max/Yandex.Disk.localized/Job/Проекты/МНОГОГО/Smart Movista/Аналитика/Данные КВР.xlsx', 
#                    skiprows=1, 
#                    usecols=list(range(1, 21))
# )

rough_df=pd.read_feather('fresh_data_dump.feather')


data_filter_columns = ['mr_num', 'mr_title', 'mr_regnum','mc_title', 
                  'crr_title', 'pk_title', 'rg_title']
date_time_columns = ['day', 'hour']
num_columns = ['BusPlan', 'BusFact', 'NoBus', 'OutBus']


# Rough data preparation
@logger.catch()
def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = optimize(df, ['NariadDate'])
    df.index = df['NariadDate']
    df['day'] = df.index.day
    df['day'] = df['day'].astype('int8')
    # df['day'] = df['day'].astype('int8')
    df['hour'] = (df['minIndex']/60).astype('int8')
    # df['hour'] = df['hour'].astype('int8')
    df.drop('NariadDate', axis=1, inplace=True)
    
    df = df[date_time_columns + data_filter_columns + num_columns]
    
    return df

# Bar chart data grouping and filtering
def group_filter_barchart_data(
    df: pd.DataFrame, 
    by_dict: dict, 
    num_columns: list) -> pd.DataFrame:
    
    df = df.copy()
    date_time_filt_cols = date_time_columns.copy()
    
    filter_query = ''
    for key, val in by_dict.items():
        if val:
            if isinstance(val, list):
                operator = 'in'
            else:
                operator = '=='
            if isinstance(by_dict[key], str):
                filter_query += f'{key} {operator} "{val}" & '
            else:
                filter_query += f'{key} {operator} {val} & '
    
    if len(filter_query) > 2:
        filter_query = filter_query[:-3]
        df = df.query(filter_query)
        
    grouped_df = df.groupby(date_time_filt_cols, observed=True)[num_columns].sum().reset_index()
    
    return grouped_df

# Data table data grouping and filtering
def groupby_filter_datatable(
    df: pd.DataFrame, 
    filter_by: dict,
    group_columns: list) -> pd.DataFrame:
    
    dff = df.copy()
    
    filter_query = ''
    for key, val in filter_by.items():
      if val:
            if isinstance(filter_by[key], str):
                filter_query += f'{key} == "{val}" & '
            else:
                filter_query += f'{key} == {val} & '
    
    if len(filter_query.split()) > 2:
        filter_query = filter_query[:-3]
        dff = dff.query(filter_query)
        
    grouped_dff = dff.groupby(group_columns, observed=True)[num_columns].sum().reset_index()
    grouped_dff['% выполнения'] = grouped_dff['BusFact'] / grouped_dff['BusPlan']
    
    return grouped_dff


if __name__ == '__main__':
    print('Filtered data')
    df = prepare_data(rough_df)
    df = df.loc['2022-05-20']
    print(df.info(memory_usage=True))
    print(df.sample(15))
    print('-----------------------------------')
    
    print('Output group_filter_barchart_data')
    grouped_df = group_filter_barchart_data(df, {'crr_title': '', 'mr_num': '010'}, num_columns)
    print(grouped_df.info(memory_usage=True))
    print(grouped_df)
    print('-----------------------------------')
    
    print('Output groupby_filter_datatable')
    grouped_df = groupby_filter_datatable(df, {'hour': 17}, ['crr_title'])
    print(grouped_df.info(memory_usage=True))
    print(grouped_df)