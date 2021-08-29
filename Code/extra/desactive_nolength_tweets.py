
import pandas as pd
import yaml

import mysql.connector
import os

os.chdir(r"E:\Karla\IRELAND v2\DKIT\2nd Semester\Dissertation\code_old\search_tweets_bkup\Code")

def process_yaml(key_name):
    
    with open("../../config.yaml", 'r') as file:
        return yaml.safe_load(file)[key_name]

def call_sp(storedp, args):
    
    config = process_yaml('mysql_conn')
    
    cnx = mysql.connector.connect(**config, database='twitter')
    cursor = cnx.cursor()
    
    if args is None:
        cursor.callproc(storedp)
    else:
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

def count_length(tweet):
    return len(tweet.replace(' ', ''))

def main():
        
    tweets = call_sp('get_all_tweets', None)
    
    tweets['count_length'] = tweets['normalized_text'].apply(count_length)
    cond = tweets['count_length'] <= 2
    tweets_desactiva = tweets[cond].copy().reset_index(drop=True)
       
    for index in range(len(tweets_desactiva)):
        tweet_id = tweets_desactiva.loc[index,'tweet_id']
        
        call_sp('update_tweets_active', (str(tweet_id), 0,))
                                    
         
if __name__ == "__main__":
    
    main()

    
    