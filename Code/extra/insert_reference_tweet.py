
import pandas as pd
import json 
import yaml

import mysql.connector
import os

#!pip install tweet-preprocessor
# https://pypi.org/project/tweet-preprocessor/
import preprocessor as p 

from datetime import datetime, date

os.chdir(r"E:\Karla\IRELAND v2\DKIT\2nd Semester\Dissertation\code_old\search_tweets_bkup\Code")


def process_yaml(key_name):
    
    with open("../../config.yaml", 'r') as file:
        return yaml.safe_load(file)[key_name]

def call_sp(storedp, args):
    
    config = process_yaml('mysql_conn')
    
    cnx = mysql.connector.connect(**config, database='twitter')
    cursor = cnx.cursor()
    
    cursor.callproc(storedp, args)
    
    info_db = None
    desc = None
    
    for result in cursor.stored_results():
        desc = result.description
        info_db = result.fetchall()
    
    cursor.close()
    cnx.commit()
    cnx.close()
    
    cols = list()
    if desc is not None:
        for i in desc:
            cols.append(i[0])
    
        return pd.DataFrame(info_db, columns=cols)
    else:
        return 0

def insert_tweet_reference(data, key_names):
    
    total_tweets = 0
    tweets = data
    found = 0
    
    for k in key_names:
        if k in tweets.keys():
            tweets = tweets[k]
            found += 1
                
    if len(key_names) == found:
        
        for tweet in tweets:
                            
            tweet_id = tweet['id']
            created_at = tweet['created_at'].replace('T', ' ').replace('Z', '') # 2020-03-10
            
            if (datetime.strptime(created_at.split(" ")[0], '%Y-%m-%d').date() > date(2021,7,18)) & (datetime.strptime(created_at.split(" ")[0], '%Y-%m-%d').date() < date(2021,8,6)):
                
                if "referenced_tweets" in tweet.keys():
                    if tweet['referenced_tweets'] is not None:
                        refered_type = tweet['referenced_tweets'][0]['type']
                        refered_id = tweet['referenced_tweets'][0]['id']                            
                    
                else:
                    refered_type = None
                    refered_id = None
                
        
                # Insert refered tweet
                if refered_id is not None:
                    call_sp('insert_referenced_tweet', (str(tweet_id),
                                                        str(refered_id),
                                                        refered_type,
                                                        )
                            )
                
                
                """
                # Insert hashtags
                if len(hashtags) > 0:
                    for h in hashtags:
                        call_sp('insert_hashtag', (h, 
                                                   str(tweet_id),
                                                   )
                                )
                
                """
                print(tweet_id, created_at) 
                    
    return total_tweets

def insert_user(data):
    
    if 'includes' in data.keys():
        if 'users' in data['includes'].keys():
            users = data['includes']['users']
            
            for user in users:
                
                author_id = user['id']
                username = user['username']
                name = p.clean(user['name'])
                verified = user['verified']
                created_at = user['created_at'].replace('T', ' ').replace('Z', '')
                
                
                if created_at:
                    call_sp('insert_user', (str(author_id),
                                            username,
                                            name,
                                            verified,
                                            created_at,
                                            )
                            )

def insert_place(data):
    
    if 'includes' in data.keys():
        if 'places' in data['includes'].keys():
            places = data['includes']['places']
            
            for place in places:
                place_id = place['id']
                name = place['name']
                country = place['country']
                
                call_sp('insert_place', (str(place_id),
                                        name,
                                        country,
                                        )
                        )

def main():
    
    total_tweets = 0
    
    for root, directories, filenames in os.walk(r'E:\Karla\IRELAND v2\DKIT\2nd Semester\Dissertation\Project\dataset'): 
        
        for filename in filenames:
        
            f = open(os.path.join(root,filename))
            data = json.load(f)
            f.close()
            
            total_tweets += insert_tweet_reference(data, ['data'])
            total_tweets += insert_tweet_reference(data, ['includes','tweets'])
            #insert_user(data)
            #insert_place(data)
                                       
                            
         
if __name__ == "__main__":
    
    main()

    
    