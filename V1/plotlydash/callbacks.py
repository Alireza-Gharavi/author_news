import plotly.express as px
import requests
import pandas as pd

from dash import Input, Output
from plotly import colors
from plotly.subplots import make_subplots




def data(category='Cryptocurrency',currency='all', period='w'):                            # this function used for providing data for graphh
    url = 'https://api.staging.authornews.robofanews.cscloud.ir/AuthorNews/v1/stat_calculator/'
    #url = "http://127.0.0.1:5000/AuthorNews/v1/stat_calculator/"
    payload = {'category':category,'currency/keyword':currency, 'period':period}
    try :
        res = requests.get(url,params=payload)
        # print(res.url)
        df = pd.DataFrame()
        df = pd.DataFrame(res.json()['data'].values())
        if res.json()['data'] == None :
            return False
        # df = pd.DataFrame(dic.values())
        return df[:20]
    except :
        print(f'unable to access {url} api')
        exit(1)







def register_callbacks(dashapp):
    @dashapp.callback(
        Output('fig1', 'figure'),
        Output('fig6', 'figure'),
        Output('fig7', 'figure'),
        Output('fig8', 'figure'),
        Output('fig12', 'figure'),
        Output('fig4', 'figure'),
        Output('fig10', 'figure'),
        Output('fig9', 'figure'),
        Output('fig13', 'figure'),
        Output('fig14', 'figure'),
        Input('period-slider', 'value'),
        Input('keyword_input', 'value'),
        Input('category-dropdown', 'value'))
    def update_graph(period_slider, keyword, category):
        if period_slider == 0 :
            period = 'd'
        elif period_slider == 1 :
            period = 'w'
        elif period_slider == 2 :
            period = 'm'
        elif period_slider == 3 :
            period = 'm6'

        df = data(category=category, currency = keyword, period = period)

#----------------------------------------------------------------------------------------------------------

        fig1 = px.bar(df, x='author', y='number_of_all_news', color='average_sentiment', height=600, opacity=0.9, 
              range_color=[-0.7,0.7], color_continuous_scale=colors.sequential.gray, text='average_sentiment',                                    #other range colors at https://plotly.com/python/builtin-colorscales/
              labels={'author':"Author", 'number_of_all_news':'Number of News', 'average_sentiment':'Avg Sentiment'})

        fig1.update_layout(template='ggplot2', paper_bgcolor='rgb(211, 211, 211)', plot_bgcolor='rgb(211, 211, 211)')

#----------------------------------------------------------------------------------------------------------

        fig6 = make_subplots(rows=1, cols=1, y_title='Avg Sentiment')
        fig6.add_bar(name='Positive', x=df['author'], y=df['positive_ratio'],
                       marker_color='DarkOliveGreen', opacity=0.9, offsetgroup=1, customdata=df['positive_ratio'],
                       hovertemplate="<b>Positive Ratio: </b> %{customdata}")
        fig6.add_bar(name='Neutral', x=df['author'], y=df['neutral_ratio'],
                              marker_color='SlateBlue', opacity=0.5, offsetgroup=1, customdata=df['neutral_ratio'], 
                              hovertemplate="<b>Neutral Ratio: </b> %{customdata}", base=df['positive_ratio'])
        fig6.add_bar(name='Negative', x=df['author'], y=df['negative_ratio'],
                              marker_color='OrangeRed', opacity=1, offsetgroup=1, customdata=df['negative_ratio'],
                              hovertemplate="<b>Negative Ratio: </b> %{customdata}<br>", base=df['positive_ratio']+df['neutral_ratio'])

        fig6.update_layout(template='ggplot2', paper_bgcolor='rgb(211, 211, 211)', plot_bgcolor='rgb(211, 211, 211)')

#----------------------------------------------------------------------------------------------------------

        fig7 = make_subplots(rows=1, cols=1, y_title='Negative Ratio  /  Positive Ratio')

        fig7.add_bar(name="Positive", x=df['author'], y=df['positive_ratio'], opacity=0.8, marker_color='DarkOliveGreen', offsetgroup=1)
        fig7.add_bar(name="Negative", x=df['author'], y=-1*df['negative_ratio'], opacity=1, marker_color='OrangeRed', offsetgroup=1)

        fig7.update_layout(template='ggplot2', paper_bgcolor='rgb(211, 211, 211)', plot_bgcolor='rgb(211, 211, 211)')

#----------------------------------------------------------------------------------------------------------

        fig8 = make_subplots(rows=1, cols=1, y_title='Number of News')
        
        
        fig8.add_bar(name="Number of Positive News", x=df[:15]['author'], y=df[:15]['number_of_positive_news'], opacity=0.9, marker_color='DarkOliveGreen')
        fig8.add_bar(name="Number of Neutral News", x=df[:15]['author'], y=df[:15]['number_of_neutral_news'], opacity=0.6, marker_color='SlateBlue')
        fig8.add_bar(name="Number of Negative News", x=df[:15]['author'], y=df[:15]['number_of_negative_news'], opacity=1, marker_color='OrangeRed')
        
        fig8.update_layout(template='ggplot2', paper_bgcolor='rgb(211, 211, 211)', plot_bgcolor='rgb(211, 211, 211)')

#----------------------------------------------------------------------------------------------------------

        fig12 = make_subplots(rows=1, cols=1, x_title='Number of News')
        
        fig12.add_bar(name="Number of Positive News", x=df[:15]['number_of_positive_news'], y=df[:15]['author'], 
                      offsetgroup=1, opacity=0.9 , marker_color='DarkOliveGreen', orientation='h', customdata=df['number_of_positive_news'],
                      hovertemplate="<b>Number of Positive News: </b> %{customdata}")

        fig12.add_bar(name='Number of Neutral News', x=df[:15]['number_of_neutral_news'], y=df[:15]['author'], 
                      offsetgroup=1, opacity=0.6, marker_color='SlateBlue', orientation='h', base=df[:15]['number_of_positive_news'],
                      customdata=df['number_of_neutral_news'], hovertemplate="<b>Number of Neutral News: </b> %{customdata}")

        fig12.add_bar(name='Number of Negative News', x=df[:15]['number_of_negative_news'], y=df[:15]['author'], 
                      offsetgroup=1, opacity=0.9, marker_color='OrangeRed', orientation='h', base=df[:15]['number_of_positive_news']+df[:15]['number_of_neutral_news'],
                      customdata=df['number_of_negative_news'], hovertemplate="<b>Number of Negative News: </b> %{customdata}")

        fig12.update_layout(height=800, template='ggplot2', paper_bgcolor='rgb(211, 211, 211)', plot_bgcolor='rgb(211, 211, 211)')

#----------------------------------------------------------------------------------------------------------

        fig4 = make_subplots(rows=1, cols=1, y_title="Number of News")

        fig4.add_scatter(name='Positive', x=df[:15]['author'], y=df[:15]['number_of_positive_news'], mode='markers', 
                         marker=dict(size=df[:15]['positive_ratio']*80, color='DarkOliveGreen'), customdata=df[['number_of_positive_news','positive_ratio']], 
                         hovertemplate="<b>%{x}</b><br><b>Number of Positive News: </b> %{customdata[0]}<br><b>Positve Ratio: </b> %{customdata[1]}")

        fig4.add_scatter(name='Negative', x=df[:15]['author'], y=df[:15]['number_of_negative_news'], mode='markers', 
                         marker=dict(size=df[:15]['negative_ratio']*80, color='OrangeRed'), customdata=df[['number_of_negative_news', 'negative_ratio']], 
                         hovertemplate="<b>%{x}</b><br><b>Number of Negative News: </b> %{customdata[0]}<br><b>Negative Ratio: </b> %{customdata[1]}")

        fig4.add_scatter(name='Neutral', x=df[:15]['author'], y=df[:15]['number_of_neutral_news'], mode='markers', 
                         marker=dict(size=df[:15]['neutral_ratio']*80, color='SlateBlue'), customdata=df[['number_of_neutral_news', 'neutral_ratio']],
                         hovertemplate="<b>%{x}</b><br><b>Number of Neutral News: </b> %{customdata[0]}<br><b>Neutral Ratio: </b> %{customdata[1]}")

        fig4.update_layout(template='ggplot2', paper_bgcolor='rgb(211, 211, 211)', plot_bgcolor='rgb(211, 211, 211)')

#----------------------------------------------------------------------------------------------------------

        fig10 = px.pie(df[:5],values='number_of_all_news',names='author', hole=0.3, color_discrete_sequence=px.colors.sequential.RdBu, labels={'author':'Author Name', 'number_of_all_news':'Number of News'})
        fig10.update_traces(textinfo="percent+label")
        fig10.update_layout(template='ggplot2', paper_bgcolor='rgb(211, 211, 211)', plot_bgcolor='rgb(211, 211, 211)',
                           annotations=[dict(text='News', x=0.5, y=0.5, font_size=20, showarrow=False)])

#----------------------------------------------------------------------------------------------------------

        lst = [df['positive_ratio'].sum(), df['neutral_ratio'].sum() , df['negative_ratio'].sum() ]
        names = ['Positve', 'Neutral', 'Negative']
        weights_df = pd.DataFrame(zip(names, lst), index=['pos', 'neu', 'neg'], columns=['names', 'ratios'])



        fig9 = px.pie(weights_df, values='ratios', names='names', color='names', hole=0.3, 
             #color_discrete_sequence=['SlateBlue', 'DarkOliveGreen', 'OrangeRed'])
             color_discrete_map={'Positve':'DarkOliveGreen', 'Neutral': 'SlateBlue', 'Negative':'OrangeRed'})
        
        fig9.update_traces(textinfo="percent+label", marker=dict(line=dict(color='#000000', width=4)), rotation=90)
        fig9.update_layout(template='ggplot2', paper_bgcolor='rgb(211, 211, 211)', plot_bgcolor='rgb(211, 211, 211)',
                           annotations=[dict(text='Weights', x=0.5, y=0.5, font_size=20, showarrow=False)])

#----------------------------------------------------------------------------------------------------------

        cons = 5

        vals = [[ df['number_of_positive_news'][i], df['number_of_neutral_news'][i], df['number_of_negative_news'][i]] for i in range(cons)]
        parns = [ [df['author'][i], df['author'][i], df['author'][i]] for i in range(cons) ]

        t_vals = []
        t_parns = []

        for i in vals:
            for j in i :
                t_vals.append(j)

        for i in parns:
            for j in i:
                t_parns.append(j)

        dit = dict(
            character=[ 'Positive', 'Neutral','Negative' ]*cons,
            parents = t_parns,
            values =  t_vals
            )

        df13 = pd.DataFrame(dit)

        fig13 = px.sunburst(df13, path=['parents','character'], values='values', color='character', color_discrete_map={'Positive':'DarkOliveGreen', 'Neutral':'SlateBlue' , 'Negative':'OrangeRed'} ,color_discrete_sequence=px.colors.sequential.Brwnyl)
        fig13.update_layout(template='ggplot2', paper_bgcolor='rgb(211, 211, 211)', plot_bgcolor='rgb(211, 211, 211)')


#----------------------------------------------------------------------------------------------------------

        cons = 5

        vals = [[ df['number_of_positive_news'][i], df['number_of_negative_news'][i]] for i in range(cons)]
        parns = [ [df['author'][i], df['author'][i]] for i in range(cons) ]

        t_vals = []
        t_parns = []

        for i in vals:
            for j in i :
                t_vals.append(j)

        for i in parns:
            for j in i:
                t_parns.append(j)

        dit = dict(
            character=[ 'Positive','Negative' ]*cons,
            parents = t_parns,
            values =  t_vals
            )

        df14 = pd.DataFrame(dit)


        fig14 = px.sunburst(df14, path=['parents','character'], color='character', values='values', color_discrete_map={'Positive':'DarkOliveGreen','Negative':'OrangeRed'}, color_discrete_sequence=px.colors.sequential.Brwnyl)
        fig14.update_layout(template='ggplot2', paper_bgcolor='rgb(211, 211, 211)', plot_bgcolor='rgb(211, 211, 211)')

#----------------------------------------------------------------------------------------------------------

        
        return fig1, fig6, fig7, fig8, fig12, fig4, fig10, fig9, fig13, fig14
