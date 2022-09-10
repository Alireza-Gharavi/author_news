import requests
import datetime, json
import pandas as pd
from flask import request, current_app, abort
from flask_restx import Resource, Namespace
from V1.response import ResponseAPI
from V1.authornews import api


api = Namespace("news_counter", description='news counter routes')



@api.route('/')
class counter(Resource):
    @api.doc(params={'category':{'description': 'Cryptocurrency/Forex/Commodities', 'in':'query', 'type':'str'},
                      'period':{'description': 'one day or one week or one month or six month ( d/w/m/m6 )', 'in':'query', 'type':'str'}
                    })
    
    def get(self):
        try:
            category = request.args.get('category')
            period = (request.args.get('period')).lower()
        except :
            current_app.logger.error('null Argument')
            return ResponseAPI.send(status_code=400, message="can't handle argumnts")
        
        current_time = int(datetime.datetime.now().timestamp())
        result = {}

        category, period = param_calculator(current_time, category, period)

        if category == 0 or period == 0 :
            return ResponseAPI.send(status_code=400,message='Arguments are not correct')

        url = "https://robonews.robofa.cscloud.ir/Robonews/v1/news/"
        payload = {'category':category, 'keywords':'all', 'from':period, 'to':current_time}

        try :
            r = requests.get(url,params=payload)           
        except :
            current_app.logger.error("can't establish connection to robonews.rofa.cscloud.ir")
            return ResponseAPI.send(status_code=403,message="can't establish connection to robonews.rofa.cscloud.ir")

        if not r.ok :
            current_app.logger.error("Unable to connect to robonews.robofa.cscloud.ir/Robonews/v1/news/")
            return ResponseAPI.send(status_code=403, message="Unable to connect to robonews.robofa.cscloud.ir/Robonews/v1/news/")

        if r.json()['status'] != 200 :
            current_app.logger.error("Bad Argument")
            return ResponseAPI.send(status_code=400, message="Bad Argument")

        if len(r.json()['data']) == 0 :
            current_app.logger.warning("no data has been published since then")
            return ResponseAPI.send(status_code=400, message="no data has been published since then")


        try :
            df = pd.json_normalize(r.json()['data'])

            df['author'] = df['author'].fillna(df['provider'])
            df['author'] = df['author'].replace('','Unknown')
            df.fillna(0, inplace=True)

            gk = df.groupby('author')
        except :
            current_app.logger.exception("unknown error in preprocessing data")
            return ResponseAPI.send(status_code=422, message='unknown error occured in preprocessing data')
        
        authors_list = list(gk.author.count().index)

        for i in authors_list :
            result[i] = int(gk.author.count()[i])

        result = sort(result)

        return ResponseAPI.send(status_code=200, message='done successfully', data=json.loads(json.dumps(result, indent=4)))



def sort(res) :
    return dict(sorted(res.items(), key=lambda item: item[1], reverse=True))


def param_calculator(current_time, category, period) :
    one_day = 86400
    l = ['Cryptocurrency', 'Forex', 'Commodities']
    if category not in l :
        current_app.logger.error("bad value for category argument")
        category = 0

    if period == 'd' :
        period = day_func() 
    elif period == 'w' : 
        period = current_time - 7 * one_day
    elif period == 'm' :
        period = current_time - 30 * one_day
    elif period == 'm6' :
        period = current_time - (6 * 30 * one_day)
    else :
        current_app.logger.error("bad value for period argument")
        period = 0
    
    return category, period



def day_func():                                                         # this function is created to calculate the timestamp for today's 00:00 oclock in utc 
    now = datetime.datetime.now(datetime.timezone.utc)
    now = list(now.timetuple())
    now[3:] = [0,0,0]
    start_of_today = datetime.datetime(*now, tzinfo=datetime.timezone.utc)
    start_of_today_timestamp = start_of_today.timestamp() 
    return int(start_of_today_timestamp)