import pandas as pd
import requests, json
import datetime
from time import time
from flask import request
from flask_restx import Api, Resource, Namespace


api = Namespace('Authornews-Api', description='authornews routes')

@api.route('/')
class first(Resource) :
    @api.doc(params={'currency': {'description': 'currency name (e.x. bitcoin)', 'in': 'query', 'type': 'str'},
                     'period': {'description': 'One Day or One Week or One Month or Six Month (d/w/m/m6)', 'in': 'query', 'type': 'str'}})
    
    def get(self) :
        period = (request.args.get('period'))                           #exception handling
        currency = (request.args.get('currency'))                       #exception handling
        current_time = int(time())
        one_day = 86400
        result = {}

        if period == 'd' :
            period = day_func() 
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
        
        sorting_df = pd.DataFrame.from_dict(result, orient='index')                                 #first turn resulting dictionary into a dataframe (used orient=index to make the author's names as index of our new dataframe) in order -->
        sorting_df = sorting_df.sort_values(by='number_of_all_news', ascending=False)               #-->to sort the output by column 'number_of_all_news' and then convert it again to json format in order to output it by swagger
        temp_res = sorting_df.to_json(orient='index')                                               

        return json.loads(temp_res)

def stat_calculator(author_name, gk) :                                  # a function in order to calculate the values of columns of output table 

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


        

def number_of_news(author_name , gk):                                   # another function to help stat_calculator to calculate what it have to
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



def day_func():                                     #this function is created to calculate the timestamp for today's 00:00 oclock in utc 
    now = datetime.datetime.now(datetime.timezone.utc)
    now = list(now.timetuple())
    now[3:] = [0,0,0]
    start_of_today = datetime.datetime(*now, tzinfo=datetime.timezone.utc)
    start_of_today_timestamp = start_of_today.timestamp() 
    return int(start_of_today_timestamp)