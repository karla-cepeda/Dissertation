
import pandas as pd
import numpy as np
import json 
import re
import yaml
import os

def process_yaml(key_name):
    
    with open("../../credentials/config.yaml", 'r') as file:
        return yaml.safe_load(file)[key_name]


def initial_setup():
    
    path = process_yaml('root_file')
    os.chdir(path['path'])
    
    return None


def count_tweets(data, key_names, folder):
    
    total_tweets = 0
    tweets = data
    found = 0
    
    for k in key_names:
        if k in tweets.keys():
            tweets = tweets[k]
            found += 1
                
    if len(key_names) == found:        
        total_tweets = len(tweets)
                    
    return total_tweets


def main():
    
    total_tweets = 0
    
    tweets_folders = [#'tweets_politics', 'tweets_media', 'tweets_health_system', 
                      #'tweets_politics_replies', 
                      #'tweets_media_replies', 
                      #'tweets_health_system_replies',
                      #'tweets_politics_to', 
                      #'tweets_media_to', 
                      #'tweets_health_system_to',
                      'tweets_general'
                      ]

    for tweet_f in tweets_folders:
        
        folders = [x for x in os.walk('../../tweets/'+tweet_f)]
        
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
                
                total_tweets += count_tweets(data, ['data'], folder)
                total_tweets += count_tweets(data, ['includes','tweets'], folder)
                
            
    print("Total Tweets", total_tweets)                            
                            
         
if __name__ == "__main__":
    
    initial_setup()
    main()

    
    