from datetime import datetime, timedelta
from inspect import FullArgSpec
from dash import dash_table, dcc, html, Input, Output
import dash_bootstrap_components as dbc

from app import app
from data_prep.data_transform import rough_df, prepare_data
from pages.dashboard.datatable_fig import style_cell, style_data, style_header, style_filter, style_cell_conditional


dates_range = prepare_data(rough_df).index
data_table_columns = prepare_data(rough_df).columns

slider_style = {'backgroundColor': '#171C2D', 'color': 'grey', 'border': 'none'}

def make_dashboard_layout():
    page_layout = \
    html.Div(
        [
            dcc.Location(id='dashboard', refresh=True),
            dcc.Store(id='memory-output'),
            dcc.Store(id='memory-output2'),
            html.Div(
                [
                    dbc.Row(
                        [
                        dbc.Col(
                            [
                                html.H3('Дата'),
                                html.Div(
                                        dcc.DatePickerSingle(
                                            id='date-picker',
                                            min_date_allowed=dates_range.min().date(),
                                            max_date_allowed=dates_range.max().date(),
                                            initial_visible_month=dates_range.max().date(),
                                            date=dates_range.max().date(),
                                            display_format='DD-MM-YYYY',
                                        ),
                                    id='date-picker-Container'),
                                
                                html.Div([
                                html.H3('Регион'),
                                dcc.Dropdown(options=[], value='', id='region-name-filter', placeholder='введите регион',
                                            style=slider_style),  
                                html.H3('Перевозчик'),  
                                dcc.Dropdown(options=[], value='', id='carrier-filter', optionHeight=70, 
                                            placeholder='выберете перевозчика', style=slider_style),
                                html.H3('№ маршрута'),      
                                dcc.Dropdown(options=[], value='', id='route-num-filter', placeholder='введите № маршрута',
                                            style=slider_style),
                                html.H3('Парк'),          
                                dcc.Dropdown(options=[], value='', id='park-title-filter', placeholder='введите название парка',
                                            style=slider_style),
                                html.H3('Тип маршрута'),         
                                dcc.Dropdown(options=[], value='', id='route-type-filter', placeholder='введите тип марш-та',
                                            style=slider_style),
                                html.H3('Реестровый № маршрута'),
                                dcc.Dropdown(options=[], value='', id='route-regnum-filter', placeholder='введите реест. № марш-та',
                                            style=slider_style),
                                html.H3('Название маршрута'),            
                                dcc.Dropdown(options=[], value='', id='route-name-filter', optionHeight=70, 
                                            placeholder='Название марш-та', style=slider_style)],
                                id='data-slicers')  
                            ],
                            id='main-col-slicers', 
                            xs=12,
                            md=3, 
                            align='top'),
                        dbc.Col(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(html.H3('Выпуск автобусов по часам'), width=10, align='center'),
                                        dbc.Col(html.Button(' Очистить ', id='clear_bar_chart'), width=2, align='center')],
                                            id='bar-header-row', 
                                            justify='center', 
                                            align='center'), 
                                        dbc.Col(
                                            # dcc.Graph(id='date-bar-chart',), 
                                            dbc.Spinner(dcc.Graph(id="date-bar-chart", config={'doubleClick': 'reset+autosize'}), 
                                                            fullscreen=True, delay_show=500, delay_hide=1000, color='rgb(254, 209, 35)',
                                                            fullscreen_style={'backgroundColor': '#111320'}, ),
                                            width=12, 
                                            align='center'),
                                dbc.Row(
                                    [
                                        dbc.Col(html.H3('Данные по перевозчикам / маршрутам'), width=9, align='center'),
                                        dbc.Col(html.Button(' << ', id='back'), width=1, align='center'), 
                                        dbc.Col(html.Button(' Очистить  ', id='clear_datatable'), width=2, align='center'),
                                    ],
                                    id='table-header-row', 
                                    justify='between'),
                                html.Div(
                                        dash_table.DataTable(
                                            columns=[{"name": i, "id": i} 
                                                for i in data_table_columns], 
                                            id='data-table-chart', 
                                            # editable=True,
                                            # filter_action="native",
                                            sort_action="native",
                                            sort_mode="multi",
                                            column_selectable="single",
                                            row_selectable="multi",
                                            # row_deletable=True,
                                            selected_columns=[],
                                            selected_rows=[],
                                            page_action="native",
                                            page_current=0,
                                            page_size=10,
                                            style_table={'overflowX': 'auto'},
                                            style_filter=style_filter,
                                            style_header=style_header,
                                            style_data=style_data,
                                            style_cell=style_cell, 
                                            style_as_list_view=True, 
                                            style_cell_conditional=style_cell_conditional
                                            ),
                                         id='data-table'
                                         )
                            ],
                            id='main-col-visuals',
                            xs=12,
                            md=9),
                        ],
                    id='main-data-row')
                ],
            id='main-container',
            ),
            dbc.Row(html.Div(id='info-container')),
        ],
        id='main-block', 
        className='main-block'
    )
    
    return page_layout


# Create callbacks
@app.callback(Output('dashboard', 'pathname'),
              [Input('back-button', 'n_clicks')])
def logout_dashboard(n_clicks):
    if n_clicks > 0:
        return '/'

if __name__ == '__main__':
    print('uncomment')
    # external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    # app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
    # df = rough_df
    # dff = prepare_data(df)
    # app.layout = make_page_layout(dff)
    # app.run_server(debug=True)
