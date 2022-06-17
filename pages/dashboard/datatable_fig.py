from dash.dash_table.Format import Format, Align
from dash.dash_table import FormatTemplate

style_cell = {
    # 'backgroundColor': '#171C2D', 
    # 'color': 'white', 
    'borderTopColor': 'blue'}
style_data = {
    'fontFamily': 'Helvetica', 
    'fontSize': '12px', 
    # 'borderBottom': 'solid 1px #0E0F18', 
    # 'borderTop': 'solid 1px #0E0F18',
    'whiteSpace': 'normal', 
    'height': 'auto'}
style_header = {'fontFamily': 'Helvetica', 'fontSize': '14px','border': 'none', 'padding': '3px'}
style_filter = {'fontFamily': 'Helvetica', 'fontSize': '12px', 'border': 'none', 'color': 'white'}
style_cell_conditional=[
        {
            'if': {'column_id': c},
            'textAlign': 'left'
        } for c in ['crr_title', 'rg_title', 'mr_title']
    ]
style_cell_conditional.append({'if': {'column_id': 'crr_title'}, 'width': '25%'})
style_cell_conditional.append({'if': {'column_id': 'mr_title'}, 'width': '40%'})

dt_columns_all = [
    dict(id='rg_title', name='Регион', type='text'), 
    dict(id='crr_title', name='Перевозчик', type='text'),
    dict(id='mr_title', name='Название марш-та', type='text'),  
    dict(id='mr_num', name='№ марш-та'), 
    dict(id='pk_title', name='Парк', type='text'), 
    dict(id='mc_title', name='Тип марш-та', type='text'), 
    dict(id='mr_regnum', name='Реестр.№ марш-та'), 
    dict(id='Час', name='Час', type='numeric', format=Format(group=True).decimal_delimiter(value=' ').align(Align.right)), 
    dict(id='day', name='День', format=Format(group=True)), 
    dict(id='BusFact', name='Факт выпуска', type='numeric', format=Format(group=True).group_delimiter(' ').align(Align.right)),
    dict(id='BusPlan', name='План выпуска', type='numeric', format=Format(group=True).group_delimiter(' ').align(Align.right)),
    dict(id='NoBus', name='Невыпуск', type='numeric', format=Format(group=True).group_delimiter(' ').align(Align.right)),
    dict(id='OutBus', name='Сход', type='numeric', format=Format(group=True).group_delimiter(' ').align(Align.right)), 
    dict(id='% выполнения', name='% выполнения', type='numeric', format=FormatTemplate.percentage(0).align(Align.right)),
]

def data_bars(df, column, start_color='rgb(255, 255, 255)', end_color='rgb(106, 170, 215)'):
    n_bins = 100
    bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)] # list [0, 0,01, ..., 0.99, 1]
    ranges = [
        ((df[column].max() - df[column].min()) * i) + df[column].min()
        for i in bounds
    ] # list [min, min+1%, ..., min+99%, max]
    styles = []
    for i in range(1, len(bounds)):
        min_bound = ranges[i - 1] # min + 28%
        max_bound = ranges[i] # min + 29%
        max_bound_percentage = bounds[i] * 100 # 29%
        styles.append({
            'if': {
                'filter_query': (
                    '{{{column}}} >= {min_bound}' +
                    (' && {{{column}}} < {max_bound}' if (i < len(bounds) - 1) else '')
                ).format(column=column, min_bound=min_bound, max_bound=max_bound),
                'column_id': column
                },
            'background': (
                """
                    linear-gradient(90deg,
                    rgb(255, 255, 255) 0%,
                    {end_color} {max_bound_percentage}%,
                    {start_color} {max_bound_percentage}%,
                    rgb(255, 255, 255) 0%)
                """.format(max_bound_percentage=max_bound_percentage,
                           end_color = end_color,
                           start_color=start_color)
            ),
            'paddingBottom': 2,
            'paddingTop': 2, 
            })

    return styles