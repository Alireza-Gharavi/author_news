import pandas as pd
import requests, json
import datetime
from flask import request, current_app
from flask_restx import Resource, Namespace
from V1.response import ResponseAPI


api = Namespace('stat_calculator', description='authornews routes')

@api.route('/')
class first(Resource) :
    @api.doc(params={'currency': {'description': 'currency name (e.x. bitcoin)', 'in': 'query', 'type': 'str'},
                     'period': {'description': 'One Day or One Week or One Month or Six Month (d/w/m/m6)', 'in': 'query', 'type': 'str'}})
    
    def get(self) :
        # Anbaee : Please add exception handling for these parametrs   ==> solved
        try :
            period = (request.args.get('period')).lower()                
            currency = (request.args.get('currency')).lower()                       
        except : 
            current_app.logger.error("null Argument")
            return ResponseAPI.send(status_code=400, message="can't handle arguments")


        
        current_time = int(datetime.datetime.now().timestamp())
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

        url = "https://robonews.robofa.cscloud.ir/Robonews/v1/news/"
        payload = {'category':'Cryptocurrency', 'keywords':currency, 'from':period, 'to':current_time}
        
        r = requests.get(url,params=payload)           
        
        if not r.ok :
            current_app.logger.error("Unable to connect to robonews.robofa.cscloud.ir/Robonews/v1/news/")
            return ResponseAPI.send(status_code=403, message="Unable to connect to robonews.robofa.cscloud.ir/Robonews/v1/news/")


        if r.json()['status'] != 200 :
            current_app.logger.error("Bad Argument")
            return ResponseAPI.send(status_code=400, message="Bad Argument")
        if len(r.json()['data']) == 0 :
            current_app.logger.error("no data has been received")
            return ResponseAPI.send(status_code=400, message='Bad Argument or nothing has been published since then')

        try :
            df = pd.json_normalize(r.json()['data'])

            df['author'] = df["author"].fillna(df["provider"])                                         # handling None values in dataframe
            df['author'] = df["author"].replace('',"Unknown")
            df.fillna(0, inplace=True)

            gk = df.groupby('author')
        
        except :
            current_app.logger.exception('Unknown error occured in preprocessing data')
            return ResponseAPI.send(status_code=422, message='Unknown error occured in preprocessing data')


        authors_list =  list(gk.author.count().index)
        
        for i in authors_list :
            result[i] = stat_calculator(i, gk)
        
        sorting_df = pd.DataFrame.from_dict(result, orient='index')                                 # first turn resulting dictionary into a dataframe (used orient=index to make the author's names as index of our new dataframe) in order -->
        sorting_df = sorting_df.sort_values(by='number_of_all_news', ascending=False)               #-->to sort the output by column 'number_of_all_news' and then convert it again to json format in order to output it by swagger
        temp_res = sorting_df.to_json(orient='index')                                               

        return ResponseAPI.send(status_code=200, message="done successfully", data=json.loads(temp_res))

def stat_calculator(author_name, gk) :                                                              # a function in order to calculate the values of columns of output table 

# Anbaee : Multiple groupby causes your code responds slowly.  ==>  solved

    author_stats = {'author' : None, 'number_of_all_news' : None, 'number_of_positive_news' : None, 'positive_ratio' : None, 'number_of_negative_news' : None, 
                  'negative_ratio' : None, 'number_of_neutral_news' : None,  'neutral_ratio' : None, 'average_sentiment' : None}

    author_stats['author'] = author_name
    author_stats['number_of_all_news'] = gk.author.count()[author_name]
    author_name_grouped = gk.get_group(author_name)
    try :
        author_stats['positive_ratio'] = round((author_name_grouped.Positive.sum() / author_stats['number_of_all_news'] * 100), 4)             
    except : 
        author_stats['positive_ratio'] = 0
    try :        
        author_stats['negative_ratio'] = round((author_name_grouped.Negative.sum() / author_stats['number_of_all_news'] * 100), 4)             
    except :    
        author_stats['negative_ratio'] = 0
    try :
        author_stats['neutral_ratio']  = round((author_name_grouped.Neutral.sum()  / author_stats['number_of_all_news'] * 100), 4)             
    except :
        author_stats['neutral_ratio'] = 0

    author_stats['number_of_positive_news'], author_stats['number_of_negative_news'], author_stats['number_of_neutral_news'] = number_of_news(author_name, gk) 

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



def day_func():                                                         # this function is created to calculate the timestamp for today's 00:00 oclock in utc 
    now = datetime.datetime.now(datetime.timezone.utc)
    now = list(now.timetuple())
    now[3:] = [0,0,0]
    start_of_today = datetime.datetime(*now, tzinfo=datetime.timezone.utc)
    start_of_today_timestamp = start_of_today.timestamp() 
    return int(start_of_today_timestamp)
