# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 09:48:14 2021

@author: acjimenez
"""
import requests
import yaml
import urllib.parse
import os

os.chdir(r'E:\Karla\IRELAND v2\DKIT\2nd Semester\Dissertation\Code\search_tweets')

username = 'fiannafailparty' #'sinnfeinireland' #'fiannafailparty' #'Independent_ie' #'rte'

def create_twitter_url():
    words = '(vaccine OR vaccines OR pfizer) (covid OR corona OR coronavirus OR covid19 OR "covid-19")'
    handle = "from:"+username
    config =  "is:verified -is:nullcast -is:retweet"
    q = "{} {} {}".format(words, handle, config)
    
    max_results = 10
    mrf = "max_results={}".format(max_results)    
    
    url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}&tweet.fields=created_at".format(urllib.parse.quote(q), mrf)
    
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

def save_tweets(data):
    
    header = True
    tweets = pd.DataFrame(res_json['data'], columns=res_json['data'][0].keys())
    tweets['username'] = username
    
    if os.path.exists('tweets.csv'):
        header = False
            
    tweets.to_csv('tweets.csv', mode='a', index=False, header=header)


def main():
    url = create_twitter_url()
    #url = create_retweet_url()
    data = process_yaml()
    bearer_token = create_bearer_token(data)
    res_json = twitter_auth_and_connect(bearer_token, url)
    save_tweets(res_json)
    

if __name__ == "__main__":
    main()