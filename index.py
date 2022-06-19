from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
from flask_login import logout_user, current_user
from importlib_metadata import always_iterable

from app import app
from pages.dashboard import dashboard
from pages import login, login_fd, logout


header = html.Div(
    className='row',
    children=html.Div(
        className='container-width',
        style={'height': '100%'},
        children=[
            dbc.Row(
                    [
                        dbc.Col(
                            html.Img(
                                    src='assets/images/mostransavto_logo.jpg', 
                                    className='logo-image-container',
                                    style={'height': '100%'}
                            ),
                            id='header-col-logo', 
                            xs=1,
                            sm=1,
                            align='center', 
                            ),
                        dbc.Col(
                            html.H3('Контроль выполнения работ'), 
                            id='header-col-name', 
                            sm=6, xs=11, align='left'),
                        # dbc.Col(id='header-col-cards',sm=5, xs=1), 
                        # dbc.Col(
                        #     html.Div(
                        #         className='links', 
                        #         children=[
                        #             html.Div(id='user-name', className='link'),
                        #             html.Div(id='logout', className='link')
                        #             ], 
                        #         ),
                        #     id='header-col-links', 
                        #     sm=2, xs=2, align='right'
                        #     ), 
                        dbc.Col(html.Div(id='user-name', className='link'), sm=3, xs=8, align='right'), 
                        dbc.Col(html.Div(id='logout', className='link'), sm=2, xs=4, align='right'),
                        ],
                    id='header-row',
                    
                    # justify='start', 
                    ),
            
            # html.Img(
            #     src='assets/images/mostransavto_logo.jpg',
            #     className='logo'
            # ),
            # html.Div(className='links', children=[
            #     html.Div(id='user-name', className='link'),
            #     html.Div(id='logout', className='link')
            # ])
        ]
    )
)

app.layout = dbc.Container(
    [
        header,
        html.Div([
            html.Div(
                html.Div(id='page-content', className='content'),
                className='content-container'
            ),
        ], className='container-width'),
        dcc.Location(id='url', refresh=False),
    ]
)


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return login.layout
    elif pathname == '/login':
        return login.layout
    elif pathname == '/dashboard':
        if current_user.is_authenticated:
            return dashboard.layout
        else:
            return login_fd.layout
    elif pathname == '/logout':
        if current_user.is_authenticated:
            logout_user()
            return logout.layout
        else:
            return logout.layout
    else:
        return '404'


@app.callback(
    Output('user-name', 'children'),
    [Input('page-content', 'children')])
def cur_user(input1):
    if current_user.is_authenticated:
        return html.Div('Current user: ' + current_user.username)
        # 'User authenticated' return username in get_id()
    else:
        return ''


@app.callback(
    Output('logout', 'children'),
    [Input('page-content', 'children')])
def user_logout(input1):
    if current_user.is_authenticated:
        return html.A('Logout', href='/logout')
    else:
        return ''
