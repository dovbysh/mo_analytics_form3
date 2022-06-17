import plotly.graph_objects as go
from plotly.subplots import make_subplots


def make_bar_chart(dff):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Bar(
            x=dff['hour'], y=dff['BusFact'], 
            name="Выпуск автобусов", 
            marker={'color': '#2A85C5', 'opacity': 0.7, 'line': {'width': 0}}, 
            textfont={'color': 'rgb(255, 255, 255)'},
            text=dff['BusFact'], 
            textposition='auto'
            ),
        secondary_y=False
        )
    
    fig.add_trace(
        go.Bar(
            x=dff['hour'], 
            y=(dff['BusPlan']-dff['BusFact']-dff['OutBus']), 
            name="Невыпуск", 
            marker={'color': '#BCBCBB', 'opacity': 1, 'line': {'width': 0}}, 
            textfont={'color': 'rgb(255, 255, 255)'},
            text=(dff['BusPlan']-dff['BusFact']-dff['OutBus']), 
            textposition='auto'
            ),
        secondary_y=False
        )
    
    fig.add_trace(
        go.Bar(
            x=dff['hour'], 
            y=dff['OutBus'], 
            name="Сход", 
            marker={'color': '#EB5B39', 'opacity': 1, 'line': {'width': 0}}, 
            textfont={'color': 'rgb(255, 255, 255)'},
            text=dff['OutBus'], 
            textposition='auto'
            ),
        secondary_y=False
        )
    
    fig.add_trace(
        go.Scatter(
            x=dff['hour'], 
            y=dff['BusFact']/dff['BusPlan'], 
            yaxis='y2',
            name="% выполнения рейсов", 
            marker={'color': '#2A85C4', 'opacity': 1, 'line': {'width': 0}},
            mode='markers+lines', 
            textfont={'color': 'rgb(255, 255, 255)'},
            # text=(dff['BusFact']/dff['BusPlan']), 
            line_shape='spline',
            hovertemplate="%{y}"
            ),
            secondary_y=True,
        )
    # fig.update_traces(hovertemplate=None)
    # fig.update_layout(hovermode="x")
    
    fig.update_layout(yaxis=dict(showgrid=False), yaxis2=dict(showgrid=False, tickformat=',.0%'))
    
    fig.update_layout(barmode='stack', 
                      paper_bgcolor='white', #'#171C2D',
                      plot_bgcolor='white', #'#171C2D', 
                    #   font_color='rgb(255,255,255)', 
                      legend={'orientation': 'h', 
                              'xanchor': 'center',
                              'x': .5},
                      margin={'l': 70, 'r': 70, 't': 50, 'b': 50}, 
                      ), 
    return fig