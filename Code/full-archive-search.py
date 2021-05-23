

import requests
import yaml
import urllib.parse
import os
import pandas as pd
from datetime import datetime, date, timedelta
import calendar
from dateutil.relativedelta import relativedelta
import time
import json

os.chdir(r'E:\Karla\IRELAND v2\DKIT\2nd Semester\Dissertation\Code\search_tweets')

def create_twitter_url(start_date, end_date):

    words = '(vaccine OR vaccines OR vaccinated OR vaccination OR dose OR doses OR injection OR pfizer OR moderna OR NIAID OR astra OR astrazeneca OR oxford OR BioNTech OR "mRNA-1273" OR "johnson & johnson" OR "j&j" OR #vaccine OR #vaccines OR #vaccinated OR #AstraZeneca OR #pfizer OR #Moderna) (covid OR corona OR coronavirus OR covid19 OR "covid-19" OR virus OR "sars-cov-2" OR "sars cov 2" OR nCoV OR #covid19 OR #covid)'
    place = '(#ireland OR #dublin OR #galway OR #cork OR place:dublin OR place:cork OR place:galway OR place_country:IE)'
    language = 'lang:en'
    config =  "-is:nullcast"
    q = "{} {} {} {}".format(words, place, language, config)
    
    max_results = 500
    mrf = "max_results={}".format(max_results)
    
    start_date = "start_time={}".format(start_date)
    end_date = "end_time={}".format(end_date)
    
    expansions = "expansions=referenced_tweets.id,author_id,geo.place_id&tweet.fields=attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,public_metrics,possibly_sensitive,referenced_tweets,reply_settings,source,text,withheld&user.fields=created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld&place.fields=country,id,name"
    
    url = "https://api.twitter.com/2/tweets/search/all?query={}&{}&{}&{}&{}".format(urllib.parse.quote(q), mrf, start_date, end_date, expansions)
    
    return url


def process_yaml():
    with open("config.yaml") as file:
        return yaml.safe_load(file)

def create_bearer_token(data):
    return data["search_tweets_api"]["bearer_token"]

def twitter_auth_and_connect(bearer_token, url):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    response = requests.request("GET", url, headers=headers)
    return response.json()

def save_tweets(data, filename, foldername):
    
    #header = True
    #tweets = pd.DataFrame(data['data'], columns=data['data'][0].keys())
    
    folders = foldername.split('/')
    folder_lst = []
    
    for f in folders:        
        folder_lst.append(f)            
        if not os.path.exists('/'.join(folder_lst)):
            os.mkdir('/'.join(folder_lst))
    
    if type(data) is dict:
        for key in data.keys():
            data2 = data[key]
            if type(data2) is list:
                cols = data2[0].keys()
                file = pd.DataFrame(data2, columns=cols)
                file.to_csv(foldername+'/'+key+'_'+filename+'.csv', mode='w', index=False, header=True, encoding='utf-8-sig')
                
            else:
                save_tweets(data2, filename, foldername)
                    
    with open(foldername+'/'+filename+'.json', 'w') as f:
        json.dump(data, f)

def main():
    total_tweets = 0
    
    data = process_yaml()
    bearer_token = create_bearer_token(data)
    
    
    start_date = date(2020,1,1)
    end_date = start_date + timedelta(days=1)
    
    last_date = date.today()
    
    print('Starting process...')
    
    while start_date <= last_date:  

        # Y-m-dTH:M:SZ
        start_date_str = start_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        end_date_str = end_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        start_date_file = start_date.strftime('%Y-%m-%d')
        start_date_folder = start_date.strftime('%Y-%m-%d')
        
        url = create_twitter_url(start_date_str, end_date_str)
        #print('processing URL:', url)
        res_json = twitter_auth_and_connect(bearer_token, url)        
        if 'data' in res_json.keys():
            total_tweets += len(res_json['data'])
            save_tweets(res_json, start_date_file, 'tweets_general/'+start_date_folder)
            print("Total Tweets:", total_tweets, start_date_str)
            time.sleep(30)
        else:
            print("Total Tweets:", total_tweets, start_date_str)
       
        start_date += timedelta(days=1)
        end_date = start_date + timedelta(days=1)        
            
    print("Total Tweets:", total_tweets)
    print('Process has completed.')

if __name__ == "__main__":
    main()
