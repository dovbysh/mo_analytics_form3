import pandas as pd

from dash import Input, Output

from app import app
from pages.dashboard.store_data_clbks import df

# Create data slicers crossfiltering
@app.callback([
    Output('region-name-filter', 'options'), 
    Output('carrier-filter', 'options'),
    Output('route-num-filter', 'options'),
    Output('park-title-filter', 'options'),
    Output('route-type-filter', 'options'),
    Output('route-regnum-filter', 'options'),
    Output('route-name-filter', 'options')
    ],
    Input('memory-output', 'data'))
def update_data_slicers(store_data):
    dff = df.loc[store_data['date_picker'].split('T')[0]]
    
    filter_dict = {
        'rg_title': store_data['region_name'],
        'crr_title': store_data['carrier'],
        'mr_num': store_data['route_num'],
        'pk_title': store_data['park_title'],
        'mc_title': store_data['route_type'],
        'mr_regnum': store_data['route_regnum'],
        'mr_title': store_data['route_name'],
        }    
    
    for key, value in filter_dict.items():
        if not value:
            continue
        dff = dff[dff[key] == value]

    region_name_opts = dff['rg_title'].unique()
    carrier_opts = dff['crr_title'].unique()
    route_num_opts = dff['mr_num'].unique()
    park_title_opts = dff['pk_title'].unique()
    route_type_opts = dff['mc_title'].unique()
    route_regnum_opts = dff['mr_regnum'].unique()
    route_name_opts= dff['mr_title'].unique()
        
    return region_name_opts, carrier_opts, route_num_opts, park_title_opts, route_type_opts, route_regnum_opts, route_name_opts
