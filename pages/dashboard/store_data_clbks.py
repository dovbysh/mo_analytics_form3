import pandas as pd
from os import curdir

from app import app
from dash import Input, Output, callback_context
from data_prep.data_transform import prepare_data


@app.callback([
Output('memory-output', 'data'),
Output('info-container', 'children'), 
Output('data-table-chart', 'active_cell'), 
],
# Calendar
Input('date-picker', 'date'), 
# Filters
Input('region-name-filter', 'value'), 
Input('carrier-filter', 'value'),
Input('route-num-filter', 'value'),
Input('park-title-filter', 'value'),
Input('route-type-filter', 'value'),
Input('route-regnum-filter', 'value'),
Input('route-name-filter', 'value'), 
# DataTable data
Input('data-table-chart', "derived_virtual_data"),
Input('data-table-chart', "derived_virtual_selected_rows"), 
Input('data-table-chart', 'active_cell'), 
# Input('data-table-chart', 'data'),
# Input('clear_datatable', 'n_clicks'), 
Input('clear_bar_chart', 'n_clicks'),
# Input('back', 'n_clicks'), 
# Bar chart Data
# Input('date-bar-chart', 'figure'), 
Input('date-bar-chart', 'clickData'),
Input('date-bar-chart', 'hoverData')
)
def store_filter_data(date_value, region_name, carrier, route_num, park_title, 
                route_type, route_regnum, route_name, table_virt_data,
                table_sel_rows, table_active_cell,
                bar_chart_n_clicks, bar_clickData, bar_hoverData):

        keys = ['date_picker', 
                'region_name',
                'carrier',
                'route_num', 
                'park_title', 
                'route_type', 
                'route_regnum', 
                'route_name', 
                'datatable_der_virt_data', 
                'datatable_der_virt_sel_rows', 
                'datatable_act_cell', 
                # 'clear_datatable_n_clicks',
                'clear_bar_chart_n_clicks',
                # 'back_n_clicks', 
                'bar_chart_clickData',
                'bar_chart_hoverData', 
                'df',
                ]

        rough_df = pd.read_feather('fresh_data_dump.feather')
        df = prepare_data(rough_df).loc[date_value.split('T')[0]]
        df.reset_index(inplace=True)

        values = [date_value, region_name, carrier, route_num, park_title, route_type, 
        route_regnum, route_name, table_virt_data,table_sel_rows, table_active_cell, 
        bar_chart_n_clicks, bar_clickData, bar_hoverData, df.to_dict('records')]

        output = {key: val for key, val in zip(keys, values)}

        # ctx = callback_context
        # ctx_msg = json.dumps({
        #     'states': ctx.states,
        #     'triggered': ctx.triggered,
        #     'inputs': ctx.inputs
        #     }, indent=2)
                
        return output, None, None #, table_active_cell