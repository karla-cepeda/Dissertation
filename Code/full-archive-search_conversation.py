

import requests
import yaml
import urllib.parse
import os
from os import listdir
from os.path import isfile, join
import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
import calendar
from dateutil.relativedelta import relativedelta
import time
import json

os.chdir(r'E:\Karla\IRELAND v2\DKIT\2nd Semester\Dissertation\Code\search_tweets')

def create_twitter_url(conversation_id, start_date, end_date):

    start_date = "start_time={}".format(start_date)
    end_date = "end_time={}".format(end_date)
        
    max_results = 500
    mrf = "max_results={}".format(max_results)
    
    expansions = "expansions=referenced_tweets.id,author_id&tweet.fields=attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,public_metrics,possibly_sensitive,referenced_tweets,reply_settings,source,text,withheld&user.fields=created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld"
    
    url = "https://api.twitter.com/2/tweets/search/all?query=conversation_id:{}&{}&{}&{}&{}".format(conversation_id, start_date, end_date, mrf, expansions)
    
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
        
    print('Starting process...')
    
    folders = [x for x in os.walk('tweets_health_system')]
    #print(folders[267])
    #input()
    #folders = folders[267:]
    
    for x in np.arange(0,len(folders)):
        folder = folders[x][0]
        files = folders[x][-1]
        index = 0
        
        if len(files) > 0:
            for i in np.arange(0, len(files)):
                if "json" in files[i]:
                    index = i
                    break
    
            f = open(folder+'/'+files[index])
            data = json.load(f)
            f.close()            
                        
            start_date = datetime.strptime(data['data'][0]["created_at"][:10], '%Y-%m-%d') #date(2020,1,1)
            end_date = start_date + timedelta(days=1)
            
            start_date_str = start_date.strftime('%Y-%m-%dT%H:%M:%SZ')
            end_date_str = end_date.strftime('%Y-%m-%dT%H:%M:%SZ')
            start_date_file = start_date.strftime('%Y-%m-%d')
            start_date_folder = start_date.strftime('%Y-%m-%d')
                        
            con_id = []
            for i in data['data']:
                
                con_id = i['conversation_id']
                url = create_twitter_url(con_id, start_date_str, end_date_str)
                    
                res_json = twitter_auth_and_connect(bearer_token, url)
                if 'data' in res_json.keys():
                    total_tweets += len(res_json['data'])
                    save_tweets(res_json, start_date_file, 'tweets_health_system_replies/'+start_date_folder+'/'+str(con_id))
                    
                    print("Total Tweets:", total_tweets, start_date_str)
            
            time.sleep(30)
                    
            
if __name__ == "__main__":
    main()
