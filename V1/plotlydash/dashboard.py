from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import requests
import pandas as pd

def init_dashboard(server):

    def data(category='Cryptocurrency', period='w'):                            # this function used for providing data for graphh
        url = 'https://api.staging.authornews.robofanews.cscloud.ir/AuthorNews/v1/news_counter/'
        payload = {'category' : category, 'period' : period}
        try :
            res = requests.get(url,params=payload)

            df = pd.DataFrame()
            dic = res.json()['data']

            if res.json()['data'] == None :
                df['authors'] = 'NO ONE'
                df['number_of_news'] = 0
                return df

            df['authors'] = dic.keys()
            df['number_of_news'] = dic.values()

            return df.loc[:20]
        except :
            print(f'unable to access {url} api')
            exit(1)

    df = data()

    

    marks = ['one Day', 'one Week', 'one Month', 'six Month']

    dash_app = Dash(server=server, routes_pathname_prefix='/AuthorNews/v1/dashboard/')



    dash_app.layout = html.Div(children = [
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


    @dash_app.callback(
        Output('counter-graph', 'figure'),
        Input('period-slider', 'value'),
        Input('category-dropdown', 'value'))
    def update_graph(period_slider, category):
        if period_slider == 0 :
            period = 'd'
        elif period_slider == 1 :
            period = 'w'
        elif period_slider == 2 :
            period = 'm'
        elif period_slider == 3 :
            period = 'm6'

        df = data(category = category, period = period)
        fig = px.bar(df, x = 'authors', y = 'number_of_news', height=800)
        fig.update_layout(transition_duration=500)

        return fig

    return dash_app.server    
