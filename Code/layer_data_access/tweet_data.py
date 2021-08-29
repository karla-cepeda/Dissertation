# -*- coding: utf-8 -*-
"""
@author: Karla Aniela Cepeda Zapata
@studnetID: d00242569
@institute: Dundalk Institute of Technology
@supervisor: Rajesh Jaswal

"""
import datetime
from layer_classes import my_database, my_yaml

class data(object):    
    def __init__(self, db, local):
        # Set up data base connection
        self._db = my_database.myDB(db, local)
        data._date_format = lambda d: d.replace('T', ' ').replace('Z', '')   
        data._convert_date = lambda dstr: dstr.strftime("%Y-%m-%d %H:%M:%S")   

    def __del__(self):
        del self._db
    
class tweet_data(data):
    def __init__(self):
        super().__init__('twitter', True)

        # Get name of stored procedure
        myy = my_yaml.my_yaml_mydb()
        sp_list = myy.get_stored_procedure_names_twitter()
        tweet_data.__sp_truncate_tables = sp_list["truncate_table"]
        tweet_data.__sp_insert_hashtag = sp_list["insert_hashtag"]
        tweet_data.__sp_insert_place = sp_list["insert_place"]
        tweet_data.__sp_insert_referenced_tweet = sp_list["insert_referenced_tweet"]
        tweet_data.__sp_insert_tweet = sp_list["insert_tweet"]
        tweet_data.__sp_insert_user = sp_list["insert_user"]
        tweet_data.__sp_lookup_tweet = sp_list["lookup_tweet"]
        tweet_data.__sp_lookup_conversation_id = sp_list["lookup_conversation_id"]   
        tweet_data.__sp_insert_log_file = sp_list["insert_log_file"]
        tweet_data.__sp_get_log_file = sp_list["get_log_file"]
        tweet_data.__sp_update_log_file = sp_list["update_log_file"]
        tweet_data.__sp_truncate_log_file = sp_list["truncate_log_file"]
        tweet_data.__sp_get_all_tweets = sp_list['get_all_tweets']
        tweet_data.__sp_update_tweets_active = sp_list['update_tweets_active']
        tweet_data.__sp_insert_polarity = sp_list['insert_polarity']
        tweet_data.__sp_update_duplicated_tweet = sp_list['update_duplicated_tweet']
        tweet_data.__sp_truncate_log_file_label = sp_list['truncate_log_file_label']
        tweet_data.__sp_get_unlabelled_tweets = sp_list['get_unlabelled_tweets']        
        tweet_data.__sp_get_tweets_train_test = sp_list['get_tweets_train_test']
        tweet_data.__sp_get_tweets_for_migration = sp_list["get_tweets_for_migration"]
        tweet_data.__sp_insert_migration = sp_list["insert_migration"]
        tweet_data.__sp_get_tweet_keywords = sp_list["get_tweet_keywords"]
        tweet_data.__sp_insert_keywords = sp_list["insert_keywords"]
        
        # Dispose variables
        del myy, sp_list
        
    def truncate_table(self):        
        self._db.call_sp(tweet_data.__sp_truncate_tables)

    def insert_place(self, place_id, name, country):        
        # Preparing arguments to send to db
        args = (str(place_id), name, country,)    
        
        # call and send parameter to stored procedure
        #  to insert place
        self._db.call_sp(tweet_data.__sp_insert_place,  args)
        
    def insert_user(self, author_id, username, name, verified, created_at):
        created_at = data._date_format(created_at)
        args = (str(author_id), username, name, verified, created_at,)
                    
        # call and send parameter to stored procedure
        #  to insert place    
        self._db.call_sp(tweet_data.__sp_insert_user, args)
        
    def get_tweet(self, tweet_id):
        args = (str(tweet_id),)
        self._db.call_sp(tweet_data.__sp_lookup_tweet, args)
        results = self._db.get_results_dataframe()        
        return results
    
    def insert_tweet(self, tweet_id, text_original, text_cleaned, text_normalized, author_id, conversation_id, in_reply_to_user_id, lang, created_at, place_id, batch_name, key_name):
        created_at = data._date_format(created_at)
        args = (str(tweet_id), text_original, text_cleaned, text_normalized, str(author_id), str(conversation_id), in_reply_to_user_id, lang, created_at, place_id, batch_name, key_name)
        self._db.call_sp(tweet_data.__sp_insert_tweet, args)
        
    def insert_referenced_tweet(self, tweet_id, reference_id, reference_type):
        args = (str(tweet_id), str(reference_id), reference_type,)
        self._db.call_sp(tweet_data.__sp_insert_referenced_tweet, args)
        
    def insert_hashtag(self, hashtag, cleaned_hashtag, tweet_id):
        args = (hashtag, cleaned_hashtag, str(tweet_id),)
        self._db.call_sp(tweet_data.__sp_insert_hashtag, args)
        
    def truncate_log_files(self):
        self._db.call_sp(tweet_data.__sp_truncate_log_file)
        
    def insert_log_files(self, path, filename, extention, total_tweets):
        self._db.call_sp(tweet_data.__sp_insert_log_file, (path, filename, extention, total_tweets,))

    def get_log_files(self, preprocessed = -1, labelled = -1):
        self._db.call_sp(tweet_data.__sp_get_log_file, (preprocessed, labelled,))
        results = self._db.get_results_dataframe()
        return results
    
    def update_log_files(self, id_, path, filename, preprocessed = -1, labelled = -1):
        self._db.call_sp(tweet_data.__sp_update_log_file, (id_, path, filename, preprocessed, labelled))

    def get_all_tweets(self):
        self._db.call_sp(tweet_data.__sp_get_all_tweets)
        results = self._db.get_results_dataframe()
        return results
        
    def update_tweets_active(self, tweet_id, active = 0):
        self._db.call_sp(tweet_data.__sp_update_tweets_active, (tweet_id, active,))
        
    def insert_tweet_polarity_score(self, tweet_id, tem, label):
        self._db.call_sp(tweet_data.__sp_insert_polarity, (tweet_id, tem, label))
        
    def update_duplicated_tweet(self, tweet_id):
        self._db.call_sp(tweet_data.__sp_update_duplicated_tweet, (tweet_id,))      
        
    def truncate_log_file_label(self):
        self._db.call_sp(tweet_data.__sp_truncate_log_file_label)
        
    def get_unlabelled_tweets(self, get_global = True):
        self._db.call_sp(tweet_data.__sp_get_unlabelled_tweets, (get_global,))
        results = self._db.get_results_dataframe()
        return results

    def get_tweets_train_test(self):
        self._db.call_sp(tweet_data.__sp_get_tweets_train_test)
        results = self._db.get_results_dataframe()        
        return results

    def get_tweets_for_migration(self):
        self._db.call_sp(tweet_data.__sp_get_tweets_for_migration)
        results = self._db.get_results_dataframe()        
        return results
        
    def insert_migration(self, tweet_id):
        self._db.call_sp(tweet_data.__sp_insert_migration, (tweet_id,))
    
    def get_tweet_keywords(self):
        self._db.call_sp(tweet_data.__sp_get_tweet_keywords)
        results = self._db.get_results_dataframe()        
        return results 

    def insert_keywords(self, tweet_id, keywords, keywords_pharm):
        self._db.call_sp(tweet_data.__sp_insert_keywords, (tweet_id, keywords, keywords_pharm,))

class tweet_data_remote(data):
    def __init__(self):
        super().__init__('tanniest_sentimentanalysis', False)
   
        # Get name of stored procedure
        myy = my_yaml.my_yaml_mydb()
        sp_list = myy.get_stored_procedure_names_sentimentanalysis()
        tweet_data_remote.__sp_insert_tweet = sp_list["insert_tweet"]
        tweet_data_remote.__sp_get_tweets = sp_list["get_tweets"]
        tweet_data_remote.__sp_get_dates = sp_list["get_dates"]
        tweet_data_remote.__sp_get_date_reference = sp_list["get_date_reference"]
                
        # Dispose variables
        del myy, sp_list

    def insert_tweet(self, tweet_id, created_at, label_id, label, batch_name, keywords, keywords_pharm, tweet_type):
        created_at_txt = data._convert_date(created_at)
        args = (str(tweet_id), created_at_txt, int(label_id), str(label), str(batch_name), str(keywords), str(keywords_pharm), str(tweet_type))
        self._db.call_sp(self.__sp_insert_tweet, args)

    def get_tweets(self):
        self._db.call_sp(self.__sp_get_tweets)
        results = self._db.get_results_dataframe()        
        return results

    def get_dates(self):
        self._db.call_sp(self.__sp_get_dates)
        results = self._db.get_results_dataframe()        
        return results   
    
    def get_date_reference(self):
        self._db.call_sp(self.__sp_get_date_reference)
        results = self._db.get_results_dataframe()        
        return results   
        