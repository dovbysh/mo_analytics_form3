import pandas as pd

from dash import Input, Output

from app import app
from data_prep.data_transform import groupby_filter_datatable
from pages.dashboard.datatable_fig import dt_columns_all

from pages.dashboard.store_data_clbks import df


carrier_cell_filter_register = None
region_cell_filter_register = None

# Table data callback
@app.callback([
        Output('data-table-chart', 'data'),
        Output('data-table-chart', 'columns'),
        Output('back', 'n_clicks'), 
        Output('clear_datatable', 'n_clicks')],
        Input('memory-output', 'data'),
        Input('back', 'n_clicks'), 
        Input('clear_datatable', 'n_clicks'))
def update_table(store_data, back_button_n_clicks, clear_button_n_clicks):
    
    global clickData_register
    global carrier_cell_filter_register
    global region_cell_filter_register

    # Drilldown columns (click the key -> the new table columns in the dict values)
    drilldown_columns = {
        'crr_title': ['rg_title'],
        'rg_title': ['mr_title', 'mr_num', 'mr_regnum'], 
        'mr_title': ['mr_title', 'mr_num', 'mr_regnum'],
        'mr_num': ['mr_title', 'mr_num', 'mr_regnum'],
        'mr_regnum': ['mr_title', 'mr_num', 'mr_regnum']
    }

    active_cell = store_data['datatable_act_cell']
    datatable_vis_data = store_data['datatable_der_virt_data']

    table_rows = ['crr_title']
    hour = ''
    carrier_filter = ''
    region_filter = ''

    if datatable_vis_data:
        if 'crr_title' in datatable_vis_data[0].keys():
            if active_cell:
                selected_column = active_cell['column_id']
                if selected_column == 'crr_title':
                    table_rows = drilldown_columns['crr_title']
                    selected_row = active_cell['row']
                    carrier_cell_filter_register = datatable_vis_data[selected_row][selected_column]
        elif 'rg_title' in datatable_vis_data[0].keys():
            if not active_cell or active_cell['column_id']=='crr_title':
                table_rows = drilldown_columns['crr_title']
            elif active_cell['column_id'] == 'rg_title':
                table_rows = drilldown_columns['rg_title']
                selected_row = active_cell['row']
                region_cell_filter_register = datatable_vis_data[selected_row]['rg_title']
            else:
                table_rows = drilldown_columns['crr_title']
        elif 'mr_title' in datatable_vis_data[0].keys():
            table_rows = drilldown_columns['rg_title']
            
    
    # Back click button to "drill up"
    if datatable_vis_data:
        if back_button_n_clicks and 'mr_title' in datatable_vis_data[0].keys():
            table_rows = drilldown_columns['crr_title']
            region_cell_filter_register = None
        elif back_button_n_clicks and 'rg_title' in datatable_vis_data[0].keys():
            table_rows = ['crr_title']
            region_cell_filter_register = None
            carrier_cell_filter_register = None
    
    # Filter the datatable by the bar chart hover data
    # if store_data['bar_chart_hoverData']:
    #     hour = store_data['bar_chart_hoverData']['points'][0].get("x", None)
    
    # Filter the datatable by the bar chart click data
    if store_data['bar_chart_clickData']:
        label = store_data['bar_chart_clickData']["points"][0].get("x", '')
        hour, clickData_register = label, label
    
    # clear button click
    if clear_button_n_clicks:
        hour = ''
        table_rows = ['crr_title']
        carrier_cell_filter_register = None
        region_cell_filter_register = None
    
    if not carrier_cell_filter_register:
        carrier_filter = store_data['carrier']
    elif carrier_cell_filter_register and store_data['carrier']:
        carrier_filter = store_data['carrier']
    else:
        carrier_filter = carrier_cell_filter_register
        
    if not region_cell_filter_register:
        region_filter = store_data['region_name']
    elif region_cell_filter_register and store_data['region_name']:
        region_filter = store_data['region_name']
    else:
        region_filter = region_cell_filter_register
        
    # prepare data for datatable
    dff = groupby_filter_datatable(
        df.loc[store_data['date_picker'].split('T')[0]], 
        {
        'hour': hour,
        'rg_title': region_filter, 
        'crr_title': carrier_filter, 
        'mr_num': store_data['route_num'],
        'pk_title': store_data['park_title'],
        'mc_title': store_data['route_type'],
        'mr_regnum': store_data['route_regnum'],
        'mr_title': store_data['route_name'],
        },
        table_rows
    )
    
    # choose columns from all columns data
    dt_columns = []
    for el in dt_columns_all:
        if el['id'] in dff.columns:
            dt_columns.append(el)
    dt_data = dff.sort_values(by='BusFact', ascending=False).to_dict('records')
    
    # style_data_conditional = data_bars(dff, 'BusFact') + data_bars(dff, 'BusPlan') + \
    #     data_bars(dff, '% выполнения') + data_bars(dff, 'NoBus') + data_bars(dff, 'OutBus')
    
    return dt_data, dt_columns, None, None