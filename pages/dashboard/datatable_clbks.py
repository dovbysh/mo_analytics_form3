from ast import In
import pandas as pd

from dash import Input, Output, State

from app import app
from data_prep.data_transform import groupby_filter_datatable
from pages.dashboard.datatable_fig import dt_columns_all

@app.callback(
        Output('data-table-chart', 'data'),
        Output('data-table-chart', 'columns'),
        Input('memory-output2', 'data'),
        Input('memory-output', 'data'),
        State('data-table-chart', "derived_virtual_data"),
        )
def update_table(
    active_cell_filters,
    store_data, 
    datatable_display_data
    ):
    
    df = pd.DataFrame(store_data['df'])
    drilldown_columns = {
        'crr_title': ['rg_title'],
        'rg_title': ['mr_title', 'mr_num', 'mr_regnum'], 
        'mr_title': ['mr_title', 'mr_num', 'mr_regnum'],
        'mr_num': ['mr_title', 'mr_num', 'mr_regnum'],
        'mr_regnum': ['mr_title', 'mr_num', 'mr_regnum']
    }
    table_groupper_column = ['crr_title']
    hour = ''    
    carrier_filter = active_cell_filters.get('level_1', None)
    region_filter = active_cell_filters.get('level_2', None)
    route_filter = active_cell_filters.get('level_3', None)
    hour = active_cell_filters.get('barchart_clicked_x', '')
            
    if datatable_display_data:
        if route_filter:
            table_groupper_column = drilldown_columns['rg_title']
        elif region_filter:
            table_groupper_column = drilldown_columns['rg_title']
        elif carrier_filter:
            table_groupper_column = drilldown_columns['crr_title']

        # prepare data for datatable
    dff = groupby_filter_datatable(
        df,
        {
        'hour': hour,
        'rg_title': store_data['region_name'] if store_data['region_name'] else region_filter, 
        'crr_title': store_data['carrier'] if store_data['carrier'] else carrier_filter, 
        'mr_num': store_data['route_num'],
        'pk_title': store_data['park_title'],
        'mc_title': store_data['route_type'],
        'mr_regnum': store_data['route_regnum'],
        'mr_title': store_data['route_name'],
        },
        table_groupper_column
    )
    
    dt_columns = []
    for el in dt_columns_all:
        if el['id'] in dff.columns:
            dt_columns.append(el)
    dt_data = dff.sort_values(by='BusFact', ascending=False).to_dict('records')
    
    # style_data_conditional = data_bars(dff, 'BusFact') + data_bars(dff, 'BusPlan') + \
    #     data_bars(dff, '% выполнения') + data_bars(dff, 'NoBus') + data_bars(dff, 'OutBus')
    
    return dt_data, dt_columns