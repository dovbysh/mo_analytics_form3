import pandas as pd

from dash import Input, Output

from app import app
from data_prep.data_transform import group_filter_barchart_data, num_columns
from pages.dashboard.bar_chart_fig import make_bar_chart
from pages.dashboard.datatable_clbks import carrier_cell_filter_register, region_cell_filter_register

from pages.dashboard.store_data_clbks import df

# click_data_filter = None
    
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
