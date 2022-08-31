import pandas as pd
import numpy as np
import requests, json
from time import time
from flask import request
from flask_restx import Api, Resource, Namespace


api = Namespace('Authornews-Api', description='authorews routes')

@api.route('/')
class first(Resource) :
    @api.doc(params={'period': {'description': 'One Day or One Week or One Month or Six Month (d/w/m/m6)', 'in': 'query', 'type': 'str'},
                     'currency': {'description': 'currency name (e.x. bitcoin)', 'in': 'query', 'type': 'str'}})
    
    def get(self) :
        period = (request.args.get('period'))                           #exception handling
        currency = (request.args.get('currency'))                       #exception handling
        current_time = int(time())
        one_day = 86400
        result = {}

        if period == 'd' :
            period = current_time - one_day 
        elif period == 'w' : 
            period = current_time - 7 * one_day
        elif period == 'm' :
            period = current_time - 30 * one_day
        elif period == 'm6' :
            period = current_time - (6 * 30 * one_day)

        url = f"https://robonews.robofa.cscloud.ir/Robonews/v1/news/?category=Cryptocurrency&keywords={currency}&from={period}&to={current_time}"
        r = requests.get(url)           #exception hadling
        
        df = pd.json_normalize(r.json()['data'])
        
        gk = df.groupby('author')
        
        authors_list =  list(gk.author.count().index)
        
        for i in authors_list :
            result[i] = stat_calculator(i, gk)

        temp_res = json.dumps(result, cls=NpEncoder , indent=3)             
        return json.loads(temp_res)

def stat_calculator(author_name, gk) :

    author_stats = {'author' : None, 'number_of_all_news' : None, 'number_of_positive_news' : None, 'positive_ratio' : None, 'number_of_negative_news' : None, 
                  'negative_ratio' : None, 'number_of_neutral_news' : None,  'neutral_ratio' : None, 'average_sentiment' : None}

    author_stats['author'] = author_name
    author_stats['number_of_all_news'] = gk.author.count()[author_name]
    author_stats['positive_ratio'] = round((gk.get_group(author_name).Positive.sum() / author_stats['number_of_all_news'] * 100), 4)              #exception handling
    author_stats['negative_ratio'] = round((gk.get_group(author_name).Negative.sum() / author_stats['number_of_all_news'] * 100), 4)              #exception handling
    author_stats['neutral_ratio']  = round((gk.get_group(author_name).Neutral.sum()  / author_stats['number_of_all_news'] * 100), 4)              #exception handling

    author_stats['number_of_positive_news'] ,author_stats['number_of_negative_news'] ,author_stats['number_of_neutral_news'] = number_of_news(author_name , gk) 

    author_stats['average_sentiment'] = round(author_stats['positive_ratio'] - author_stats['negative_ratio'], 4)

    return author_stats             


        

def number_of_news(author_name , gk):
    pos, neg, neu = 0, 0, 0
    temp_df = gk.get_group(author_name)[['Positive', 'Negative', 'Neutral']] 
    
    for i in list( temp_df.index ):
        if temp_df.loc[i].idxmax() == "Positive" : 
            pos += 1
        if temp_df.loc[i].idxmax() == "Negative" :
            neg += 1
        if temp_df.loc[i].idxmax() == "Neutral" :
            neu += 1  
    return pos, neg, neu




class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.rounding):
            return round(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)
