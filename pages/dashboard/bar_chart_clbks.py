import pandas as pd

from dash import Input, Output

from app import app
from data_prep.data_transform import group_filter_barchart_data, num_columns
from pages.dashboard.bar_chart_fig import make_bar_chart
    
    
# Bar_chart callback
@app.callback([
    Output('date-bar-chart', 'figure')],
    Input('memory-output', 'data'),
    Input('memory-output2', 'data'))
def update_bar_chart(store_data, active_cell_filters):
    
    # from pages.dashboard.datatable_clbks import carrier_cell_filter_register, region_cell_filter_register
    
    dff = pd.DataFrame(store_data['df'])
    carrier_filter = active_cell_filters.get('level_1', None)
    region_filter = active_cell_filters.get('level_2', None)
    route_filter = active_cell_filters.get('level_3', None)
    
    barchart_clicked_x = active_cell_filters.get('barchart_clicked_x', '')
    
    datatable_sel_rows_filter = active_cell_filters.get('datatable_sel_rows', None)
    if datatable_sel_rows_filter:
        col_name = list(datatable_sel_rows_filter.keys())[0]
        if col_name == 'crr_title':
            carrier_filter = datatable_sel_rows_filter[col_name]
        elif col_name == 'rg_title':
            region_filter = datatable_sel_rows_filter[col_name]
        elif col_name == 'mr_title':
            route_filter = datatable_sel_rows_filter[col_name]
        
    # finally filter source dataframe
    dff = group_filter_barchart_data(
        dff,
        {
        'rg_title': store_data['region_name'] if store_data['region_name'] else region_filter, 
        'crr_title': store_data['carrier'] if store_data['carrier'] else carrier_filter, 
        'mr_num': store_data['route_num'],
        'pk_title': store_data['park_title'],
        'mc_title': store_data['route_type'],
        'mr_regnum': store_data['route_regnum'],
        'mr_title': store_data['route_name'] if store_data['route_name'] else route_filter,
        },
        num_columns
    )
            
    # create bar chart figure for callback output
    bar_chart_fig = make_bar_chart(dff)
    
    # change opacity if any bar has been clicked
    if barchart_clicked_x:
        for i in range(len(bar_chart_fig["data"])):
            bar_chart_fig["data"][i]["marker"]["opacity"] = [1 if c == barchart_clicked_x else 0.5 for c in bar_chart_fig["data"][0]["x"]]
    
    return (bar_chart_fig, )