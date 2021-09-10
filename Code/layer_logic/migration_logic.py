# -*- coding: utf-8 -*-
"""
@author: Karla Aniela Cepeda Zapata
@studnetID: d00242569
@institute: Dundalk Institute of Technology
@supervisor: Rajesh Jaswal

Contains the process to migrate specific tweet data into a remote database that will 
be used for a dashboard to show off the results.

"""
from layer_data_access import tweet_data, date_data

class tweet_migrate(object):
    def __init__(self):
        tweet_migrate.__tweetd_local = tweet_data.tweet_data()
        tweet_migrate.__tweetd_remote = tweet_data.tweet_data_remote()
        
    def __del__(self):
        del tweet_migrate.__tweetd_local
        del tweet_migrate.__tweetd_remote
    
    @staticmethod
    def start_process():
        """
        Starts the migration process tweets data.
        Not all information is copied, just tweet_id, label, created_at, batch_name and keywords.

        Returns
        -------
        None.

        """
        print("Start tweet migration to remote db.")
        df_tweets = tweet_migrate.__tweetd_local.get_tweets_for_migration()
        
        if not df_tweets is None:
            # Copy all data from dates that havent been copied to remote db
            for i in range(len(df_tweets)):       
                tweet_migrate.__tweetd_remote.insert_tweet(**{c: df_tweets.loc[i,c] for c in df_tweets.columns})
            
            # Register ids inserted in database
            ids = df_tweets.tweet_id
            for i in ids:
                tweet_migrate.__tweetd_local.insert_migration(str(i))
                print("tweet", i, "has been inserted into remote db")

        else:
            print("No tweets to migrate.")

        print("Migration process has been completed.")


                
