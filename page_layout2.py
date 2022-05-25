from datetime import date, datetime
from urllib.request import DataHandler
from dash import Dash, dash_table, dcc, html
import dash_bootstrap_components as dbc

from data_transform import rough_df, prepare_data
from datatable_chart import style_cell, style_data, style_header, style_filter, \
    style_cell_conditional

slider_style = {'backgroundColor': '#171C2D', 'color': 'grey', 'border': 'none'}

def make_page_layout(df):
    page_layout = \
    html.Div(
        [
            dcc.Store(id='memory-output'),
            dbc.Container(
                [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Img(
                                    src='assets/images/mostransavto_logo.jpg', 
                                    className='logo-image-container',
                                    style={'height': '100%'}
                                )
                            ],
                            id='header-col-logo', 
                            width=1, 
                            align='center'
                            ),
                        dbc.Col(
                            html.H3('Контроль выполнения работ'), 
                            id='header-col-name', 
                            width=4, align='center'),
                        dbc.Col(id='header-col-cards')
                    ],
                    id='header-row',
                    justify='start'
                    ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H3('Дата'),
                                html.Div(
                                        dcc.DatePickerSingle(
                                            id='date-picker',
                                            min_date_allowed=date(2022, 1, 1),
                                            max_date_allowed=datetime.today(),
                                            initial_visible_month=datetime.today(),
                                            date=date(2022, 3, 22), #datetime.today(),
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
                                            dcc.Graph(id='date-bar-chart',), 
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
                                                for i in df.columns], 
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

if __name__ == '__main__':
    print('uncomment')
    # external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    # app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
    # df = rough_df
    # dff = prepare_data(df)
    # app.layout = make_page_layout(dff)
    # app.run_server(debug=True)