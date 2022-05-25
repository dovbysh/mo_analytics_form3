from datetime import date, datetime
from dash import Dash, dash_table, dcc, html
import dash_bootstrap_components as dbc

from data_transform import rough_df, prepare_data
from datatable_chart import style_cell, style_data, style_header, style_filter, \
    style_cell_conditional

slider_style = {'backgroundColor': '#171C2D', 'color': 'grey', 'border': 'none'}

def make_page_layout(df):
    page_layout = dbc.Container(
        [
            dcc.Store(id='memory-output'),
            # Header
            dbc.Row(
                dbc.Col(
                    html.H3('My dashboard'), 
                    width=10,
                ),
                justify='center'
            ),
            
            # Main block           
            dbc.Row(
                [
                    # Data slicers column
                    dbc.Col(
                        [
                            dbc.Row(
                                html.H5('Срезы')
                            ),
                            dbc.Row(
                            # Date picker
                                    html.Div(
                                    dcc.DatePickerSingle(
                                        id='date-picker',
                                        min_date_allowed=date(2022, 1, 1),
                                        max_date_allowed=datetime.today(),
                                        initial_visible_month=datetime.today(),
                                        date=date(2022, 3, 22) #datetime.today(),
                                        ),
                                        id='date-picker-Container',
                                        className='date-picker'
                                    ), 
                                ),
                            # Data filters
                            dbc.Row(
                                html.Div(
                                    [
                                        dcc.Dropdown(options=[], value='', id='region-name-filter', placeholder='Регион',
                                                    style=slider_style),    
                                        dcc.Dropdown(options=[], value='', id='carrier-filter', optionHeight=70, 
                                                    placeholder='Перевозчик', style=slider_style),      
                                        dcc.Dropdown(options=[], value='', id='route-num-filter', placeholder='№ маршрута',
                                                    style=slider_style),          
                                        dcc.Dropdown(options=[], value='', id='park-title-filter', placeholder='Парк',
                                                    style=slider_style),         
                                        dcc.Dropdown(options=[], value='', id='route-type-filter', placeholder='Тип марш-та',
                                                    style=slider_style),
                                        dcc.Dropdown(options=[], value='', id='route-regnum-filter', placeholder='Реест. № марш-та',
                                                    style=slider_style),            
                                        dcc.Dropdown(options=[], value='', id='route-name-filter', optionHeight=70, 
                                                    placeholder='Название марш-та', style=slider_style)
                                    ], 
                                    id='data-slicers', 
                                ),
                            )
                        ],
                        sm=12, 
                        md=12,
                        lg=4,
                ),
                    # Charts area
                    dbc.Col(
                        [
                            dbc.Row(
                                html.H5('Выпуск автобусов по часам')
                            ),
                            dbc.Row([
                                dbc.Col(html.Button(id='clear_bar_chart', children='Очистить')),
                                dcc.Graph(
                                    id='date-bar-chart', 
                                    # hoverData={'points': [{'customdata': 'hover'}]}, 
                                    # clickData = {'points': [{'customdata': 'clicks'}]},
                                    style={'maxHeight': '350px'},
                                    ), 
                            ]),
                            dbc.Row(
                                html.H5('Данные по перевозчикам / маршрутам')
                            ),
                            dbc.Row([
                                dbc.Col(html.Button(id='clear_datatable', children='Очистить')), 
                                dbc.Col(html.Button(id='back', children='Назад'))
                                ]),
                            dbc.Row(
                                html.Div(
                                    [   
                                        dash_table.DataTable(
                                            columns=[{"name": i, "id": i} 
                                                        for i in prepare_data(rough_df).columns], 
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
                                            style_cell_conditional=style_cell_conditional)
                                    ],
                                    id='data-table'
                                ),
                                ),
                            dbc.Row(html.Div(id='info-container'))
                        ],
                        sm=12, 
                        md=12,
                        lg=8,
                    ),
                ],
                justify='center' 
                )
        ],
        fluid=True,
        className='main-block'
    )
    return page_layout

if __name__ == '__main__':
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
    df = rough_df
    dff = prepare_data(df)
    app.layout = make_page_layout(dff)
    app.run_server(debug=True)