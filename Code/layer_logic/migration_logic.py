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

class date_migrate(object):
    def __init__(self):
        """
        Constructor.
        
        """
        date_migrate.__dated_local = date_data.date_data() # Create access to local database
        date_migrate.__dated_remote = date_data.date_data_remote() #  Create access to remote database
        
    def __del__(self):
        # Delete access objects
        del date_migrate.__dated_local
        del date_migrate.__dated_remote
    
    @staticmethod
    def start_process():
        """
        Starts the migration process of date data.

        Returns
        -------
        None.

        """
        print("Start date migration to remote db.")
        df_dates = date_migrate.__dated_local.get_dates_for_migration()
        df_dates_references = date_migrate.__dated_local.get_date_reference_for_migration()
        df_references = date_migrate.__dated_local.get_reference_for_migration()
        
        if not df_dates is None:
            # Copy all data from dates that havent been copied to remote db
            for i in range(len(df_dates)):            
                date_migrate.__dated_remote.insert_date(**{c: df_dates.loc[i,c] for c in df_dates.columns})
            
            for i in range(len(df_dates_references)):
                date_migrate.__dated_remote.insert_date_reference(**{c: df_dates_references.loc[i,c] for c in df_dates_references.columns})

            for i in range(len(df_references)):
                date_migrate.__dated_remote.insert_reference(**{c: df_references.loc[i,c] for c in df_references.columns})

            # Insert tweets and dates relation
            date_migrate.__dated_remote.insert_tweet_date()
        
            # Register ids inserted in database
            ids = df_dates.id
            for i in ids:
                date_migrate.__dated_local.insert_migration(i)
                print("date", i, "has been inserted into remote db")

        else:
            print("No dates to migrate.")

        print("Migration process has been completed.")


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


                
