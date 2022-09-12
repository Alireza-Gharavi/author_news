from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import requests
import pandas as pd




def data(category='Cryptocurrency', period='w'):                            # this function used for providing data for graphh
    url = 'https://api.staging.authornews.robofanews.cscloud.ir/AuthorNews/v1/news_counter/'
    #url = 'http://127.0.0.1:5000/AuthorNews/v1/news_counter'
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







def register_callbacks(dashapp):
    @dashapp.callback(
        Output('counter-graph', 'figure'),
        Input('period-slider', 'value'),
        Input('category-dropdown', 'value'))
    def update_graph(period_slider, category):
        df = data()
        if period_slider == 0 :
            period = 'd'
        elif period_slider == 1 :
            period = 'w'
        elif period_slider == 2 :
            period = 'm'
        elif period_slider == 3 :
            period = 'm6'

        df = data(category = category, period = period)
        fig = px.bar(df, x = 'authors', y = 'number_of_news', height=800, opacity=0.5, orientation='v',
                 color_discrete_sequence=['red'], text='number_of_news',
                 labels={'authors' : 'Authors', 'number_of_news':'Number of Published News'},
                 title='Number of Published News by Authors',
                 template='ggplot2')
        fig.update_layout(transition_duration=500)

        return fig
