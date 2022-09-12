from dash import Dash, dcc, html



marks = ['one Day', 'one Week', 'one Month', 'six Month']

Layout = html.Div(children = [
    html.H2(children="News Counter Graph"),
    html.H4(children="Categories"),
    dcc.Dropdown(
        ['Cryptocurrency', 'Forex', 'Commodities'],
        'Cryptocurrency',
        id = 'category-dropdown'
    ),
    html.H4(children='Periods'),
    dcc.Slider(0, 3, marks={i: marks[i] for i in range(4)}, value=1, id='period-slider'),
    dcc.Graph(id = 'counter-graph')
])