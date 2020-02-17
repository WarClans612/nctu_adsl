from data_extractor import PixnetArticle
from operator import itemgetter
import json
import time
import math
from datetime import date

now_time = time.time() 
time_interval = {'week':1,'month':3,'3_month':10,'year':30,'3_year':100}

def scoring_function(hit,post_time):
    if(hit <1):
        hit = 1
    post_date = date.fromtimestamp(post_time)
    now_date = date.fromtimestamp(now_time)
    elapse_days = (now_date - post_date).days
    if(elapse_days <1):
        return 0
    return float(hit)/math.log(elapse_days,1.5)




data_gen = PixnetArticle()

score_dict = {}
for data_str in data_gen:
    data = json.loads(data_str)
    score_dict[data['url']] = scoring_function(data['hits'],data['post_at'])
    if(scoring_function(data['hits'],data['post_at'])==0):
            print(data['url'],date.fromtimestamp(data['post_at']),data['post_at'])
    #print(scoring_function(data['hits'],data['post_at']),date.fromtimestamp(data['post_at']))
#with open('popularity/url_popularity.json', 'w') as outfile:
#    json.dump(score_dict, outfile,ensure_ascii=False)
