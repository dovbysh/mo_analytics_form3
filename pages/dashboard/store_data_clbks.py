import json
import pandas as pd
import os
from datetime import date, datetime
import pytz

from app import app
from dash import Input, Output, State, callback_context
from data_prep.data_scheduling import check_increment_update_time_hourly
from data_prep.data_transform import prepare_data


rough_df = pd.read_feather('fresh_data_dump.feather')
df = prepare_data(rough_df)

@app.callback(
        Output('memory-output', 'data'),
        Output('date-picker', 'min_date_allowed'),
        Output('date-picker', 'max_date_allowed'),
        Output('date-picker', 'initial_visible_month'),
        # Calendar
        Input('date-picker', 'date'), 
        # Main filters
        Input('region-name-filter', 'value'), 
        Input('carrier-filter', 'value'),
        Input('route-num-filter', 'value'),
        Input('park-title-filter', 'value'),
        Input('route-type-filter', 'value'),
        Input('route-regnum-filter', 'value'),
        Input('route-name-filter', 'value'), 
        )
def load_store_data(
        date_value, 
        region_name, 
        carrier, 
        route_num, 
        park_title, 
        route_type, 
        route_regnum, 
        route_name, 
        ):
        
        # load data
        rough_df = pd.read_feather('fresh_data_dump.feather')
        df = prepare_data(rough_df)
        
        # Date picker filtering
        dff = df.loc[date_value.split('T')[0]]
        
        # Combining output
        
        keys = [
                'date_picker', 
                'region_name',
                'carrier',
                'route_num', 
                'park_title', 
                'route_type', 
                'route_regnum', 
                'route_name', 
                'df'
                ]
        values = [
                date_value, 
                region_name, 
                carrier, 
                route_num, 
                park_title, 
                route_type, 
                route_regnum, 
                route_name, 
                dff.to_dict('records')
                ]
        
        dates_range = df.index
        min_date_allowed = dates_range.min().date()
        max_date_allowed = dates_range.max().date()
        initial_visible_month = dates_range.max().date()

        data =  {key: val for key, val in zip(keys, values)}
        return (data, 
                min_date_allowed, 
                max_date_allowed, 
                initial_visible_month)

@app.callback(
        # Outputs
        Output('memory-output2', 'data'),
        # Output('info-container', 'children'), 
        Output('data-table-chart', 'active_cell'), 
        Output('clear_datatable', 'n_clicks'),
        Output('back', 'n_clicks'),
        Output('clear_bar_chart', 'n_clicks'),
        Output('date-bar-chart', 'clickData'),
        Output('data-table-chart', "derived_virtual_selected_rows"),
        # Inputs
        State('data-table-chart', "derived_virtual_data"),
        State('memory-output2', 'data'),
        Input('data-table-chart', 'active_cell'), 
        Input('clear_datatable', 'n_clicks'), 
        Input('back', 'n_clicks'), 
        Input('clear_bar_chart', 'n_clicks'),
        Input('date-bar-chart', 'clickData'),
        State('date-bar-chart', 'hoverData'), 
        Input('data-table-chart', "derived_virtual_selected_rows")
        )
def store_crossfilters(
        datatable_display_data,
        active_cell_filters,
        active_cell, 
        clear_datatable_click, 
        back_datatable_click,
        bar_chart_n_clicks, 
        bar_clickData, 
        bar_hoverData,
        table_sel_rows,
        ):
        
        if not active_cell_filters:
                active_cell_filters = {}
                
        if active_cell:
                selected_row = active_cell['row']
                if 'crr_title' in datatable_display_data[0].keys():
                        active_cell_filters['level_1'] = datatable_display_data[selected_row]['crr_title']
                elif 'rg_title' in datatable_display_data[0].keys():
                        active_cell_filters['level_2'] = datatable_display_data[selected_row]['rg_title']
                elif 'mr_title' in datatable_display_data[0].keys():
                        active_cell_filters['level_3'] = datatable_display_data[selected_row]['mr_title']
                        
        # bar chart filtering by table selected rows
        active_cell_filters['datatable_sel_rows'] = {}
        if table_sel_rows:
                left_col_name = list(datatable_display_data[0].keys())[0]
                active_cell_filters['datatable_sel_rows'][left_col_name] = \
                        [datatable_display_data[sel_row][left_col_name] for sel_row in table_sel_rows]

        if clear_datatable_click:
                  active_cell_filters = {}
                  clear_datatable_click = None
                  
        if back_datatable_click and active_cell_filters:
                del active_cell_filters[list(active_cell_filters.keys())[-1]]
                back_datatable_click = None
        
        active_cell_filters['barchart_clicked_x'] = None
        if bar_clickData:
                 active_cell_filters['barchart_clicked_x'] = bar_clickData["points"][0].get("x", '')
        if bar_chart_n_clicks and active_cell_filters['barchart_clicked_x']:
                active_cell_filters['barchart_clicked_x'] = None
                bar_chart_n_clicks = None
                bar_clickData = None
        
        
        # DEBUG INFO BLOCK    
        # ctx = callback_context
        # ctx_msg = json.dumps({
        #     'states_data': ctx.states["memory-output2.data"],
        #     'triggered': ctx.triggered[:-1],
        #     'inputs-active_cell': ctx.inputs["data-table-chart.active_cell"], 
        #     'sel_rows': ctx.inputs["data-table-chart.derived_virtual_selected_rows"], 
        # #     'vis_data': ctx.states["data-table-chart.derived_virtual_data"]
        #     }, indent=2)
        
        active_cell = None
        
        return (active_cell_filters, 
                # ctx_msg, 
                active_cell, 
                clear_datatable_click, 
                back_datatable_click, 
                bar_chart_n_clicks, 
                bar_clickData, 
                table_sel_rows
                )
