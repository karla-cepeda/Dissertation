# -*- coding: utf-8 -*-
"""
@author: Karla Aniela Cepeda Zapata
@studnetID: d00242569
@institute: Dundalk Institute of Technology
@supervisor: Rajesh Jaswal

This module is used to carry out some processes on tweets. 
In general: cleaning, normalization, collection, labelling, and getting list of keywords.

"""
import pandas as pd
import os
import json
from datetime import datetime, date, timedelta

from layer_classes import my_tweet, my_yaml
from layer_data_access import tweet_data

class tweet_logic(object):
    def __init__(self):
        """
        Constrcutor.
        Parent class. 
        Children class below.
        """
        tweet_logic._data = tweet_data.tweet_data() # To access data to from database
        
    def __del__(self):
        del tweet_logic._data

class collection(tweet_logic):    
    def __init__(self, inicial_collection):  
        """
        Constructor.

        Parameters
        ----------
        inicial_collection : Bool
            DESCRIPTION. Indicates if the collection process is an inicial process or daily collector.

        Returns
        -------
        None.

        """
        super().__init__()
        
        # Date
        collection.__short_date_str = lambda d: d.strftime('%Y-%m-%d')
        
        # Configs
        myy = my_yaml.my_yaml_tweet()
        default_config = myy.get_default_config()     
        if inicial_collection:
            collection.__start_date_default = datetime.strptime(default_config["deafult_start_date"], '%Y,%m,%d').date()
        else:
            collection.__start_date_default = date.today()
        
        # Data requested to be returned to json response.
        collection.__expansions_default = default_config["expansions"]
        collection.__collect_conversations_default = default_config["collect_conversations"]
        collection.__query_config_default = default_config["query_config"]
        
        collection.__operator =  myy.get_keywords() # List of words and synonyms of an specific word.
        collection.__batches = myy.get_bacthes() # List of convination of operator that were enlisted above.
        
        repositories = myy.get_repositories()
        collection.__repository_name = repositories['main']
        collection.__repository_conversations = os.path.join(repositories['main'], 'conversations')
        
        # Tweet object
        collection.__tweetc = my_tweet.my_collector()
        
        # Conversations list
        collection.__conversations = list()
        
        # Inicial collection
        collection.__inicial_collection = inicial_collection
        
        del myy, repositories, default_config
        
    def __del__(self):
        super().__del__()
        del collection.__tweetc
    
    @staticmethod
    def start_process(truncate_log_file = False):    
        """
        This method starts the collection process, depending on parameter sent to constructor, this will behave
        as a daily collector (gathering tweets from today) or as an inicial collection (gathering tweets from a specific period).

        Parameters
        ----------
        truncate_log_file : Bool, optional
            DESCRIPTION. Indicates if the table log_file in local database is gonna be truncated (delete content). 
            The default is False.

        Returns
        -------
        None.

        """
        print("Starting collection process...")
        
        # Truncate log files
        if collection.__inicial_collection and truncate_log_file:
            tweet_logic._data.truncate_log_files()
        
        # Build query from batch specifications
        for batch_name, v in collection.__batches.items():
            print("Building query process...")
            query_txt = ""
            start_date = collection.__start_date_default
            get_conversation =  bool(collection.__collect_conversations_default)
            expansions = collection.__expansions_default
            for q2 in v:
                # Check if there is no more configurations to add into query
                if type(q2) is dict:
                    word = list(q2.keys())[0]
                    value = list(q2.values())[0]
                    if word == "extra_config":
                        query_txt += value
                    elif word == "-":
                        query_txt += "-" + (" " + word).join(collection.__operator[value]) + " "
                    elif word == "date" and collection.__inicial_collection:
                        # Only if historical information is required
                        start_date = datetime.strptime(value, '%Y,%m,%d').date()
                    elif word == "conversation":
                        get_conversation = bool(value)
                    elif word == "expansions":
                        expansions = value
                    else:
                        if type(value) == list:
                            separator = " " + word
                            query_txt2 = ""
                            for v in value:
                                query_txt2 += word + " OR ".join(separator.join(collection.__operator[v]).split()) 
                            query_txt += "(" + query_txt2 + ") "
                            del query_txt2

                        else:
                            separator = " " + word
                            query_txt += "(" + word + " OR ".join(separator.join(collection.__operator[value]).split()) + ") "
                else:
                    query_txt += "(" + " OR ".join(collection.__operator[q2]) + ") "
            
            query_txt = query_txt.strip()
            config =  collection.__query_config_default
            language = 'lang:en'
            query_txt = "{} {} {}".format(query_txt, config, language)
            query_txt = query_txt.strip()
            print(batch_name, "batch ready to collect tweets.")
            print("Start collection of batch", batch_name, "...")
            
            collection.__get_tweets(batch_name, start_date, query_txt, expansions, get_conversation)
            
        print("Process has been complited.")        
    
    def __get_tweets(batch_name, start_time, query, expansions, collect_conversetion=False):
        """
        Get tweets according to the query built.

        Parameters
        ----------
        batch_name : String
            DESCRIPTION. Name of the batch in process.
        start_time : Datetime
            DESCRIPTION. Start date to collect tweets.
        query : String
            DESCRIPTION. Query to be sent to the endpoint.
        expansions : String
            DESCRIPTION. Indicates data that will be added when getting the json response.
        collect_conversetion : Bool, optional
            DESCRIPTION. Indicates if the process will collect a conversation. The default is False.

        Returns
        -------
        None.

        """
        path = os.path.join(collection.__repository_name, batch_name)
        end_time = start_time + timedelta(days=1)    
        count_tweets = 0
        count_conv = 0
        count_all = 0
        total_tweets = 0
        
        while start_time <= date.today():   
            # Tweets
            filename = collection.__short_date_str(start_time)
            results = collection.__tweetc.get_tweets(query, expansions, start_time, end_time)
            count_tweets = collection.__get_count_tweets(results, batch_name, filename)
            collection.__save_response(path, filename, ".json", results, count_tweets)     
                        
            if collect_conversetion:
                # Conversations within tweets collected.
                conversations = collection.__get_idConversations(results)
                results_conv = None
                for c in conversations:
                    query_conv = "conversation_id:{}".format(c)
                    path_conv = os.path.join(collection.__repository_conversations, batch_name)
                    filename = c
                    results_conv = collection.__tweetc.get_tweets(query_conv, expansions, start_time, is_conversation = True)
                    count_conv = collection.__get_count_tweets(results_conv, batch_name, filename)
                    collection.__save_response(path_conv, filename, ".json", results_conv, count_conv)                
                del results_conv
            
            count_all = count_tweets + count_conv
            if count_all > 0:
                total_tweets += count_all
                print(datetime.today(), "Batch:", batch_name, "Date:", collection.__short_date_str(start_time), "-", collection.__short_date_str(end_time), "Count tweets:", count_all, "Total tweets:", total_tweets)
                
            # Next day
            start_time += timedelta(days=1)
            end_time = start_time + timedelta(days=1)
            
            del results, filename
    
    def __get_count_tweets(data, batch_name, filename):
        """
        Count the number of tweets within a json response.

        Parameters
        ----------
        data : dictionary
            DESCRIPTION. This contains the response from the twitter api.
        batch_name : string
            DESCRIPTION. Name of the batch in process.
        filename : string
            DESCRIPTION. Name of the filename that has been used to save the response in a json file in machine.

        Returns
        -------
        Integer
            DESCRIPTION. Number of tweets in data

        """
        if 'meta' in data.keys():
            return int(data['meta']['result_count'])
        else:
            if 'error' in data.keys():
                print(data, batch_name, filename)
                input("Click ENTER to conitnue")
            return 0
    
    def __get_idConversations(res_json):
        """
        Get the conversation_id from response, this is to collect the tweets within a conversation.

        Parameters
        ----------
        res_json : directory
            DESCRIPTION. response from twiter api

        Returns
        -------
        idConversations_lst : list
            DESCRIPTION. List of all conversation ids 

        """
        idConversations_lst = list()
        if "data" in res_json.keys():
            for d in res_json["data"]:
                if "conversation_id" in d.keys():
                    if d['conversation_id'] not in idConversations_lst and d['conversation_id'] not in collection.__conversations:
                        idConversations_lst.append(d['conversation_id'])
                        collection.__conversations.append(d['conversation_id'])
        
        return idConversations_lst

    def __save_response(path, filename, extention, res_json, total_tweets):
        """
        Save the response in the machine as a "raw" format.

        Parameters
        ----------
        path : string
            DESCRIPTION. Path were the file will be saved.
        filename : string
            DESCRIPTION. Name of the file
        extention : string
            DESCRIPTION. Type of file, this will be most of the cases .json
        res_json : directory
            DESCRIPTION. Respose from Twitter API.
        total_tweets : integer
            DESCRIPTION. Total number of tweets.

        Returns
        -------
        None.

        """
        if total_tweets > 0:
            collection.__create_repository(path)        
            with open(os.path.join(path, filename + extention), 'w') as f:
                json.dump(res_json, f)
            tweet_logic._data.insert_log_files(path, filename, extention, total_tweets)

    def __create_repository(path):
        """
        Create files to save response from Twitter API
        
        """
        folders = ""
        for f in os.path.split(path):
            folders = os.path.join(folders, f)
            if not os.path.exists(folders):
                os.mkdir(folders)

class preparation(tweet_logic):
    def __init__(self):   
        """
        Constructor.
        Process to clean, normalize, insert tweets into local database.
        Additionally, it insert information related to users, places and referenced tweets.
        
        """
        super().__init__()
        
        # Count number of tweets processed
        preparation.__total_tweets = 0
        preparation.__count_tweets = 0
        preparation.__json_files = []
        
        # Configurations
        myy = my_yaml.my_yaml_tweet()    
        repositories = myy.get_repositories()
        preparation.__repository_main = repositories['main']
        batches = myy.get_bacthes()
        preparation.__folder_name = batches.keys()
        del myy, repositories, batches   
    
        # Cleaning tweeter
        preparation.__my_preprocessor = my_tweet.my_preprocessor()
        
    def __del__(self):
        super().__del__()
        del preparation.__my_preprocessor
        
    # Insert tweet into database
    #  only if does not exist on db
    def __insert_tweet(tweets, key_names, batch_name):
        """
        Insert tweet into local database.
        Cleaning and Normalization process are carried out before insertion process.

        Parameters
        ----------
        tweets : dataframe
            DESCRIPTION. Tweet. This contains cleaned and normalized columns.
        key_names : string
            DESCRIPTION. What section the tweet came from, as in the reponse there are tweets in the "data" section and in "tweets" section.
        batch_name : string
            DESCRIPTION. Name of the batch in process.

        Returns
        -------
        None.

        """
        found_keys = 0
        for k in key_names:
            if k in tweets.keys():
                tweets = tweets[k]
                found_keys += 1
                    
        if len(key_names) == found_keys:
            for tweet in tweets:
                # Get id of tweet
                tweet_id = tweet['id']
                results = tweet_logic._data.get_tweet(tweet_id)
                if type(results) == pd.core.frame.DataFrame:
                    if len(results) > 0:
                        # tweet already exists, no need to insert
                        continue
                
                # Tweet does not exists on database, insert into database get conversation id            
                # Prepare text to insert into database
                cleaned_text = preparation.__my_preprocessor.clean_tweet(tweet['text'])
                normalize_tweet = " ".join(preparation.__my_preprocessor.normalize_tweet(cleaned_text))
                                
                in_reply_to_user_id = None
                if "in_reply_to_user_id" in tweet.keys():
                    in_reply_to_user_id = tweet['in_reply_to_user_id']
                
                place_id = None
                if "geo" in tweet.keys():
                    if "place_id" in tweet['geo']:
                        place_id = tweet['geo']['place_id']
                
                # Insert tweet
                tweet_logic._data.insert_tweet(tweet_id, 
                                               str(tweet['text'].encode('utf-8')),
                                               cleaned_text,
                                               normalize_tweet,
                                               tweet['author_id'], 
                                               tweet['conversation_id'], 
                                               in_reply_to_user_id, 
                                               tweet['lang'], 
                                               tweet['created_at'], 
                                               place_id, 
                                               batch_name, 
                                               key_names[-1])
                preparation.__total_tweets += 1
                preparation.__count_tweets += 1
                
                # Insert refered tweet
                reference_type = None
                reference_id = None 
                if "referenced_tweets" in tweet.keys():
                    if tweet['referenced_tweets'] is not None:
                        reference_id = tweet['referenced_tweets'][0]['id']
                        reference_type = tweet['referenced_tweets'][0]['type']
                        tweet_logic._data.insert_referenced_tweet(tweet_id, reference_id, reference_type)
                
                # Insert hashtags
                hashtags = preparation.__my_preprocessor.get_hashtags(tweet['text'])
                if len(hashtags) > 0:
                    for h in hashtags:
                        cleaned = None
                        original = None
                        if type(h) is dict:
                            cleaned = h.pop('cleaned', None)
                            original = h.pop('original', None)
                        else:
                            original = h
                        original = preparation.__my_preprocessor.clean_basic(original)
                        tweet_logic._data.insert_hashtag(original, cleaned, tweet_id)
                
                del results#, hashtags, 
                del cleaned_text, normalize_tweet

    # Insert user into database
    #  only if does not exist on db
    def __insert_user(data):    
        """
        Insert user into database.

        Parameters
        ----------
        data : dictioanry
            DESCRIPTION. response from twitter api

        Returns
        -------
        None.

        """
        if 'includes' in data.keys():
            if 'users' in data['includes'].keys():
                users = data['includes']['users']
                for user in users:
                    name = preparation.__my_preprocessor.clean_basic(user['name'])
                    tweet_logic._data.insert_user(user['id'],
                                                    user['username'],
                                                    name,
                                                    user['verified'],
                                                    user['created_at'])
    
    # Insert place into database
    #  only if it does not exist on db
    def __insert_place(data):    
        """
        Insert place into database.

        Parameters
        ----------
        data : dictioanry
            DESCRIPTION. response from twitter api

        Returns
        -------
        None.

        """
        if 'includes' in data.keys():
            if 'places' in data['includes'].keys():
                places = data['includes']['places']                        
                for place in places:
                    tweet_logic._data.insert_place(place['id'], 
                                              place['name'], 
                                              place['country'])
        
    @staticmethod
    def start_process(truncate_tables = True):
        """
        Preprocess the data and insert it into the database.

        Parameters
        ----------
        truncate_tables : Bool, optional
            DESCRIPTION. Indicates if it is needed to truncate tables (delete content) from local database.
            The default is True.

        Returns
        -------
        None.

        """
        print(datetime.today(), "Starting cleaning and insertion process...")        
        # Truncate tables
        if truncate_tables:
            tweet_logic._data.truncate_table()
        
        # Get all json files
        jfiles_df = tweet_logic._data.get_log_files(preprocessed = 0)
        
        for i in range(len(jfiles_df)):
            id_ = jfiles_df.loc[i, 'id']
            path = jfiles_df.loc[i,'path']
            filename = jfiles_df.loc[i,'filename']
            extention = jfiles_df.loc[i,'extention']
            full_path = os.path.join(path, filename + extention)
            with open(full_path) as file:
                data = json.load(file)
            
            # Start insertion process
            batch_name = path.replace("..\\dataset\\", '')
            preparation.__count_tweets = 0
            preparation.__insert_tweet(data, ['data'], batch_name)
            preparation.__insert_tweet(data, ['includes','tweets'], batch_name)
            preparation.__insert_user(data)
            preparation.__insert_place(data) 
            
            # Indicate that file has been processed
            tweet_logic._data.update_log_files(int(id_), str(path), str(filename), preprocessed = 1)
            
            print(datetime.today(), "tweets inserted:", preparation.__count_tweets, "Total:", preparation.__total_tweets, "Batch:", batch_name, filename)
            
        print("Process has been complited.")

class keywords(tweet_logic):
    def __init__(self):
        """
        Constructor.
        
        """
        super().__init__()
        # For labelling process
        keywords.__keywords_process = my_tweet.my_keywords()
    
    def __del__(self):
        super().__del__()
        del preparation.__keywords_process

    @staticmethod
    def start_process():
        """
        Start the process to get the keywords within a tweet according to the keywords in the batches.

        Returns
        -------
        None.

        """
        print(datetime.today(), "Starting keywords process")
        df_tweets = tweet_logic._data.get_tweet_keywords()

        # Upgrade sentiment into label
        if not df_tweets is None:
            count_tweets = len(df_tweets)
            for index in range(count_tweets):
                row_df = df_tweets.iloc[index]
                tweet_id = row_df['tweet_id']
                cleaned_text = row_df['cleaned_text']
                key_cvaccine, key_pharma = keywords.__keywords_process.get_all_keywords(cleaned_text)
                tweet_logic._data.insert_keywords(str(tweet_id), ", ".join(key_cvaccine), ", ".join(key_pharma))

                end1 = '\n'
                if index+1 != count_tweets:
                    end1 = '\r'

                print(str(index+1)+"/"+str(count_tweets), "tweets has been updated", end = end1)

        else:
            print("No tweets have been found for upgrade.")

        print(datetime.today(), "Process has been completed.")

class label_process(tweet_logic):
    def __init__(self, lexicon_based):
        """
        Constructor.
        This starts the labelling process.
                

        Parameters
        ----------
        lexicon_based : Bool
            DESCRIPTION. Define if the labelling process will be done by a lexico approach or using the model built.

        Returns
        -------
        None.

        """
        super().__init__()

        # For labelling process
        if lexicon_based:
            # Using VADER libary for tweet classification
            label_process.__my_label = my_tweet.my_lexicon_labeller()
        else:
            # Using own ML algorithm designed previously
            #  using covid_vaccine_global batch for training
            label_process.__my_label = my_tweet.my_labeller()

        label_process.__lexicon_based = lexicon_based
    
    @staticmethod
    def count_length(tweet):
        """
        Count the number of characters, excluding blank spaces.
        
        """
        return len(tweet.replace(' ', ''))

    @staticmethod
    def start_process(): 
        """
        Start the process of labelling, depending if it is lexicon approach or using the model.

        Returns
        -------
        None.

        """
        if label_process.__lexicon_based:
            print(datetime.today(), "Starting labelling process using VADER...")
        else:
            print(datetime.today(), "Starting labelling process using SVM algorithm...")

        if label_process.__lexicon_based:
            # Get all tweets
            # For lexicon based labelling, original text must be sent as there is a basic cleaning process for this.
            tweets = tweet_logic._data.get_unlabelled_tweets(1)
            column_name = 'cleaned_text'

        else:
            # Get ie tweets
            # This labelling process is done using own model, thus normalized text must be sent for classification.
            tweets = tweet_logic._data.get_unlabelled_tweets(0)
            column_name = 'normalized_text'

        # Upgrade sentiment into label
        count_tweets = len(tweets)
        for index in range(count_tweets):
            row_df = tweets.iloc[index]
            tweet_id = row_df['tweet_id']
            text = row_df[column_name]
            
            tem, label = label_process.__my_label.get_polarity_score(text)
            tweet_logic._data.insert_tweet_polarity_score(str(tweet_id), tem, label)
            
            end1 = '\n'
            if index+1 != count_tweets:
                end1 = '\r'

            print(str(index+1) + "/" + str(count_tweets), "tweets have been labelled", end = end1)

        print(datetime.today(), "Process has been complited.")

class deactive_process(tweet_logic):
    def __init__(self):
        """
        Constructor.        

        """
        super().__init__()
    
    @staticmethod
    def count_length(tweet):
        return len(tweet.replace(' ', ''))

    @staticmethod
    def start_process(): 
        """
        If the tweet has a length less or equal to 2, this tweet will be classified as empty and
        deleted digitally from database.

        Returns
        -------
        None.

        """
        print(datetime.today(), "Starting deactivation of tweets process ...")
    	
        # To avoid selecting all tweets, just select the one that have not been labelled
        tweets = tweet_logic._data.get_unlabelled_tweets(0)
        
        tweets['count_length'] = tweets['normalized_text'].apply(deactive_process.count_length)
        cond = tweets['count_length'] <= 2
        tweets_deactivate = tweets[cond].copy().reset_index(drop=True)
        
        # Upgrade sentiment into label
        count_tweets = len(tweets_deactivate)
        for index in range(count_tweets):
            row_df = tweets.iloc[index]
            tweet_id = row_df['tweet_id']            
            tweet_logic._data.update_tweets_active(str(tweet_id), 0)
            
            end1 = '\n'
            if index+1 != count_tweets:
                end1 = '\r'

            print(str(index+1) + "/" + str(count_tweets), "tweets have deactivated", end = end1)

        print(datetime.today(), "Process has been complited.")


