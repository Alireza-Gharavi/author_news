import pandas as pd
import requests
from time import time
from flask import Flask , request
from flask_restx import Api, Resource                # only working with flask==2.1.2 and Werkzeug==2.1.2

app = Flask(__name__)
api = Api(app)

@api.route('/myapp')
class first(Resource) :
    @api.doc(params={'period': {'description': 'One Day or One Week or One Month or Six Month (d/w/m/m6)', 'in': 'query', 'type': 'str'}})
    @api.doc(params={'currency': {'description': 'currency name (e.x. bitcoin)', 'in': 'query', 'type': 'str'}})

    def get(self) :
        period = (request.args.get('period'))
        currency = (request.args.get('currency'))
        current_time = int(time())

        if period == 'd' :
            period = current_time - 86400
        elif period == 'w' : 
            period = current_time - 604800
        elif period == 'm' :
            period = current_time - 2629743
        elif period == 'm6' :
            period = current_time - (6 * 2629743)

        url = f"https://robonews.robofa.cscloud.ir/Robonews/v1/news/?category=Cryptocurrency&keywords={currency}&from={period}&to={current_time}"
        r = requests.get(url)
        df = pd.json_normalize(r.json())
        result = {'number_of_all_news' : None, 'number_of_positive_news' : None, 'positive_ratio' : None, 'number_of_negative_news' : None, 
                  'negative_ratio' : None, 'number_of_neutral_news' : None,  'neutral_ratio' : None, 'average_sentiment' : None}


        result['number_of_all_news'] = len(df['data'][0])

        result['number_of_positive_news'], result['number_of_negative_news'], result['number_of_neutral_news'] = number_of_news(df['data'][0])

        temp_pos = 0
        temp_neg = 0
        temp_neu = 0

        for i in range(len(df['data'][0])) :
            temp_neg += df['data'][0][i]['Negative']
            temp_pos += df['data'][0][i]['Positive']
            temp_neu += df['data'][0][i]['Neutral']

        result['positive_ratio'] = temp_pos / len(df['data'][0]) * 100
        result['negative_ratio'] = temp_neg / len(df['data'][0]) * 100
        result['neutral_ratio'] = temp_neu / len(df['data'][0]) * 100

        result['average_sentiment'] = result['positive_ratio'] - result['negative_ratio']

        return result

def number_of_news(news):
    pos, neg, neu = 0, 0, 0
    for i in range(len(news)) :
        if news[i]['Positive'] >= news[i]['Negative'] and news[i]['Positive'] >= news[i]['Neutral'] :
            pos += 1
        elif news[i]['Negative'] >= news[i]['Positive'] and news[i]['Negative'] >= news[i]['Neutral'] :
            neg += 1
        elif news[i]['Neutral'] >= news[i]['Negative'] and news[i]['Neutral'] >= news[i]['Positive'] :
            neu += 1
    return pos, neg, neu

app.run(host='0.0.0.0')