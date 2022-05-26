from datetime import date
from dash import Dash, Input, Output, callback_context
import dash_bootstrap_components as dbc
from dash import dash_table
from dash.exceptions import PreventUpdate


import json

from bar_chart import make_bar_chart
from data_transform import prepare_data, filter_groupby_df, rough_df, filter_columns, num_columns
from page_layout import make_page_layout

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

df = prepare_data(rough_df)
app.layout = make_page_layout(df)

@app.callback(
        [Output('date-bar-chart', 'figure'), 
         Output('data-table-chart', 'data'),
         Output('data-table-chart', 'columns'),
         Output('clear', 'n_clicks'),
        #  Output('info-container', 'children'), 
         Output('date-bar-chart', 'clickData')],
        
        Input('date-picker', 'date'), 
        Input('region-name-filter', 'value'), 
        Input('carrier-filter', 'value'),
        Input('route-num-filter', 'value'),
        Input('park-title-filter', 'value'),
        Input('route-type-filter', 'value'),
        Input('route-regnum-filter', 'value'),
        Input('route-name-filter', 'value'),
        Input('date-bar-chart', 'clickData'),
        Input('clear', 'n_clicks'), 
    )
def update_graph(date_value, region_name, carrier,route_num, park_title, route_type, route_regnum, 
                 route_name, clickData, n_clicks):
    
    ctx = callback_context
    day_num = date.fromisoformat(date_value).day
    
    dff = filter_groupby_df(
        df[df['day']==day_num], 
        {
        'rg_title': region_name,
        'crr_title': carrier,
        'mr_num': route_num,
        'pk_title': park_title,
        'mc_title': route_type,
        'mr_regnum': route_regnum,
        'mr_title': route_name,
        },
        num_columns
    )
    
    # fig1 = make_subplots(specs=[[{'secondary_y': True}]])
    
    bar_chart_fig = make_bar_chart(dff)
    
    # fig1 = px.bar(dff, x='Час', y=['BusPlan', 'BusFact'])
    plan_fact_y_values = (dff['BusFact'] / dff['BusPlan']).tolist()
    plan_fact_x_values = dff['Час'].tolist()   
    # fig3 = px.scatter(x=plan_fact_x_values, y=plan_fact_y_values)
    
    dt_columns = [{"name": i, "id": i} for i in dff.columns]
    dt_data = dff.to_dict('records')
    
    if clickData:
        hour = clickData["points"][0].get("label", None)
        dt_data = dff.query(f'Час == {hour}').to_dict('records')

    clickData_new = clickData
    if n_clicks:
        dt_data = dff.to_dict('records')
        clickData_new = None
        n_clicks = None
    
    # ctx_msg = json.dumps({
    #     'states': ctx.states,
    #     'triggered': ctx.triggered,
    #     'inputs': ctx.inputs
    # }, indent=2)
    
    return bar_chart_fig, dt_data, dt_columns, n_clicks, clickData_new

if __name__ == '__main__':
    app.run_server(debug=True)