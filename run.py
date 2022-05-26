from datetime import datetime
import json
import pandas as pd

from dash import Dash, Input, Output, callback_context
import dash_bootstrap_components as dbc

from bar_chart import make_bar_chart
from data_transform import prepare_data, group_filter_barchart_data, groupby_filter_datatable, rough_df, num_columns
from datatable_chart import data_bars,  dt_columns_all
from page_layout2 import make_page_layout


external_stylesheets = 'assets/bootstrap-grid.min.css'

app = Dash(__name__, 
           external_stylesheets=[external_stylesheets])
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

# df = prepare_data(rough_df)
app.layout = make_page_layout()

i = 0
clickData_register = None
hoverData_register = None
carrier_cell_filter_register = None
region_cell_filter_register = None

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
    
    values = [date_value, region_name, carrier, route_num, park_title, route_type, 
            route_regnum, route_name, table_virt_data,table_sel_rows, table_active_cell, 
            bar_chart_n_clicks, bar_clickData, bar_hoverData]
    
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
            ]
    
    rough_df=pd.read_feather('fresh_data_dump.feather')
    
    global df
    df = prepare_data(rough_df).loc[date_value.split('T')[0]]
    
    output = {key: val for key, val in zip(keys, values)}
    
    ctx = callback_context
    ctx_msg = json.dumps({
        'states': ctx.states,
        'triggered': ctx.triggered,
        'inputs': ctx.inputs
        }, indent=2)
    global i
    
    # print(f'-------------STAGE {i + 1}---------------')

    i += 1
    # print(ctx_msg)
    # str(json.loads(ctx_msg).get('inputs'))
        
    return output, None, None #, table_active_cell

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
def crossfilter_data_slicers(store_data):
    
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

# Bar_chart callback
@app.callback([
    Output('date-bar-chart', 'figure')],
    Input('memory-output', 'data'))
def update_bar_chart(store_data):   
    hour = ''
    click_data_filter = hour
    
    # set hour filter if hover on any bar in the chart
    if store_data['bar_chart_hoverData']:
        hour = store_data['bar_chart_hoverData']["points"][0].get("x", None)
    
    # set hour filter and opacity modifier if click on any bar in the chart
    if store_data['bar_chart_clickData']:
        hour = store_data['bar_chart_clickData']["points"][0].get("x", '')
        click_data_filter = hour
    
    # clear hour / opacity filters if the clear button has clicked
    if store_data['clear_bar_chart_n_clicks']:
        hour = ''
        click_data_filter = hour
    
    # filters from datatable by carrier (without drilldown)
    table_selected_filter = []
    if store_data['datatable_der_virt_sel_rows']:
        visible_cols = set(store_data['datatable_der_virt_data'][0])
        selected_column = list(visible_cols & set(['crr_title', 'rg_title', 'mr_title']))[0]
        print(f'Selecter rows = {store_data["datatable_der_virt_sel_rows"]}')
        print(f'Selected cols = {selected_column}')
        for row in store_data['datatable_der_virt_sel_rows']:
            table_selected_filter.append(store_data['datatable_der_virt_data'][row][selected_column])
        dff = df[df[selected_column].isin(table_selected_filter)]
    else:
        dff = df
        
    if carrier_cell_filter_register:
        dff = dff.query(f'crr_title == "{carrier_cell_filter_register}"')
    if region_cell_filter_register:
        dff = dff.query(f'rg_title == "{region_cell_filter_register}"')
        
    
    # finally filter source dataframe    
    dff = group_filter_barchart_data(
        dff.loc[store_data['date_picker'].split('T')[0]], 
        {
        'rg_title': store_data['region_name'],
        'crr_title': store_data['carrier'],
        'mr_num': store_data['route_num'],
        'pk_title': store_data['park_title'],
        'mc_title': store_data['route_type'],
        'mr_regnum': store_data['route_regnum'],
        'mr_title': store_data['route_name'],
        },
        num_columns
    )
    # create bar chart figure for callback output
    bar_chart_fig = make_bar_chart(dff)
    global i
    # print(f'-------------STAGE BAR ChART {i}---------------')
    # print(f'ClickData =  {click_data_filter}')
    
    # change opacity if any bar has been clicked
    if click_data_filter:
        for i in range(len(bar_chart_fig["data"])):
            bar_chart_fig["data"][i]["marker"]["opacity"] = [1 if c == click_data_filter else 0.5 for c in bar_chart_fig["data"][0]["x"]]
    
    return (bar_chart_fig, )

# Bar clean button callback
@app.callback([
    Output('clear_bar_chart', 'n_clicks'), 
    Output('date-bar-chart', 'clickData'), 
    Output('date-bar-chart', 'hoverData')], 
    Input('clear_bar_chart', 'n_clicks'), 
    Input('date-bar-chart', 'clickData'),
    Input('date-bar-chart', 'hoverData'))
def update_clear_barchart_button(n_clicks, bar_chart_click_data, bar_chart_hover_data,):
    if not n_clicks:
        return None, bar_chart_click_data, bar_chart_hover_data
    bar_chart_click_data = None
    return None, None, None

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


if __name__ == '__main__':
    app.run_server(debug=True)