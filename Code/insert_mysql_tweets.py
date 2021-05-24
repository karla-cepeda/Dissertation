
import pandas as pd
import numpy as np
import json 
import re
import yaml

import mysql.connector

import nltk
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords

#!pip install contractions
import contractions

#!pip install tweet-preprocessor
# https://pypi.org/project/tweet-preprocessor/
import preprocessor as p 

import os

# nltk.download
# nltk.download('wordnet')
# nltk.download('stopwords')


def process_yaml(key_name):
    
    with open("../../credentials/config.yaml", 'r') as file:
        return yaml.safe_load(file)[key_name]


def initial_setup():
    
    path = process_yaml('root_file')
    os.chdir(path['path'])
    
    p.set_options(p.OPT.URL, p.OPT.MENTION, p.OPT.RESERVED, p.OPT.EMOJI, p.OPT.SMILEY)

    return None


def call_sp(storedp, args):
    
    config = process_yaml('mysql_conn')
    
    cnx = mysql.connector.connect(**config)
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


def get_hashtags(tweet):    
    
    # Remove accented characters
    tweet = remove_accents(tweet)
    
    # Get hashtags
    h = re.findall(r"#(\w+)", tweet)
    
    hashtag = [x.lower().strip().replace(' ', '') for x in h]
      
    return set(hashtag) 


def remove_accents(tweet):
    
    # https://stackoverflow.com/questions/37978225/replace-some-accented-letters-from-word-in-python
    accented = {'à': 'a', 'á': 'a', 'â': 'a', 'ã': 'a',
                'é': 'e', 'ê': 'e',
                'í': 'i',
                'ó': 'o', 'ô': 'o', 'õ': 'o',
                'ú': 'u', 'ü': 'u',
                
                'À': 'A', 'Á': 'A', 'Â': 'A', 'Ã': 'A',
                'É': 'E', 'Ê': 'E',
                'Í': 'I',
                'Ó': 'O', 'Ô': 'O', 'Õ': 'O',
                'Ú': 'U', 'Ü': 'U'
                }

    new_tweet = ''.join([accented[t] if t in accented else t for t in tweet])
    
    return new_tweet


def preprocess_data(tweet):

    # Expanding contractions
    tweet = contractions.fix(tweet)
    
    # Remove accented characters
    tweet = remove_accents(tweet)
    
    # Remove ASCII characters
    tweet = re.sub(r'[^\x00-\x7F]+',' ', tweet)

    # text-cleaning: URLs, Mentions, emojis.
    tweet = p.clean(tweet)

    # Remove Digits except covid-19
    tweet = re.sub(r"(?:((C|c)(O|o)(V|v)(I|i)(D|d).?19)|\d+)(?=\D|$)", r"\1", tweet)
    
    # Replace covid variant words with covid19
    tweet = re.sub(r"((C|c)(O|o)(V|v)(I|i)(D|d).?19)", r"covid", tweet)
    
    # Lower strings
    tweet = tweet.lower()
    
    # Remove Punctuations
    # https://www.analyticsvidhya.com/blog/2018/07/hands-on-sentiment-analysis-dataset-python/
    # https://stackoverflow.com/questions/64719706/cleaning-twitter-data-pandas-python
    tweet = re.sub(r'[^a-zA-Z#]', ' ', (tweet))
    
    # Removing all special characters
    #tweet = re.sub(r'[^\w\s]', ' ', (tweet))
    
    # Remove spaces
    tweet = tweet.strip()
    
    # Remove double spaces
    tweet = tweet.replace('  ', ' ')
    
    # Lemmatization + Tokenization 
    # https://towardsdatascience.com/basic-tweet-preprocessing-in-python-efd8360d529e
    lemmatizer = nltk.stem.WordNetLemmatizer()
    w_token = TweetTokenizer()
    token_tweet = [lemmatizer.lemmatize(w) for w in w_token.tokenize(tweet)]    
    
    # Removing stop words
    #words = set(nltk.corpus.words.words())
    stop_words = set(stopwords.words('english'))
    token_tweet = [i for i in token_tweet if i not in stop_words]
        
    return tweet, token_tweet
    

def insert_tweet(data, key_names, folder):
    
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
            conversation_id = tweet['conversation_id']
            
            text_original = tweet['text'].encode('utf-8')
            hashtags = get_hashtags(tweet['text'])
            text_cleaned, text_token = preprocess_data(tweet['text'])
            
            author_id = tweet['author_id']
            lang = tweet['lang']
            created_at = tweet['created_at'].replace('T', ' ').replace('Z', '')
            
            if "geo" in tweet.keys():
                if "place_id" in tweet['geo']:
                    place_id = tweet['geo']['place_id']
            else:
                place_id = None
                        
            if "referenced_tweets" in tweet.keys():
                if tweet['referenced_tweets'] is not None:
                    refered_type = tweet['referenced_tweets'][0]['type']
                    refered_id = tweet['referenced_tweets'][0]['id']                            
                
            else:
                refered_type = None
                refered_id = None
            
            
            results = call_sp('lookup_tweet', (str(tweet_id),
                                               str(text_original),
                                               text_cleaned,
                                               ', '.join(text_token),
                                               )
                              )
            
            if type(results) == pd.core.frame.DataFrame:
                if len(results) == 0:
                    # Insert tweet
                    call_sp('insert_tweet', (str(tweet_id),
                                             str(text_original),
                                             str(text_cleaned),
                                             ', '.join(text_token),
                                             str(author_id),
                                             str(conversation_id),
                                             str(lang),
                                             str(created_at),
                                             place_id,
                                             folder.replace('../../tweets/', ''),
                                             key_names[-1]
                                             )
                            )
                    
                    # Insert refered tweet
                    if refered_id is not None:
                        call_sp('insert_referenced_tweet', (str(tweet_id),
                                                            str(refered_id),
                                                            refered_type,
                                                            )
                                )
                    
                    
                    
                    # Insert hashtags
                    if len(hashtags) > 0:
                        for h in hashtags:
                            call_sp('insert_hashtag', (h, 
                                                       str(tweet_id),
                                                       )
                                    )
                    
                    total_tweets +=1
                    
    return total_tweets


def insert_user(data, folder):
    
    if 'includes' in data.keys():
        if 'users' in data['includes'].keys():
            users = data['includes']['users']
            
            for user in users:
                
                author_id = user['id']
                username = user['username']
                name = p.clean(user['name'])
                verified = user['verified']
                created_at = user['created_at'].replace('T', ' ').replace('Z', '')
                                
                call_sp('insert_user', (str(author_id),
                                        username,
                                        name,
                                        verified,
                                        created_at,
                                        )
                        )


def insert_place(data, folder):
    
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
    
    tweets_folders = ['tweets_politics', 'tweets_media', 'tweets_health_system', 
                      'tweets_politics_replies', 'tweets_media_replies', 'tweets_health_system_replies',
                      'tweets_politics_to', 'tweets_media_to', 'tweets_health_system_to',
                      'tweets_general']

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
                
                total_tweets += insert_tweet(data, ['data'], folder)
                total_tweets += insert_tweet(data, ['includes','tweets'], folder)
                insert_user(data, folder)
                insert_place(data, folder)
                
                print("Tweets inserted", total_tweets, folder)                            
                            
         
if __name__ == "__main__":
    
    initial_setup()
    main()

    
    