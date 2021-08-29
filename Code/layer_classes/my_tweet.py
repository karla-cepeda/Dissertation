# -*- coding: utf-8 -*-
"""
@author: Karla Aniela Cepeda Zapata
@studnetID: d00242569
@institute: Dundalk Institute of Technology
@supervisor: Rajesh Jaswal

"""
import sys
import requests
import urllib
import time
from datetime import datetime, date
import joblib

import re
import string
import spacy
import preprocessor as pp
from ekphrasis.classes.preprocessor import TextPreProcessor
from ekphrasis.dicts.emoticons import emoticons
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
from html import unescape
from text_to_num import alpha2digit
import enchant

# For sentiment analysis
from nltk.sentiment.vader import SentimentIntensityAnalyzer
#import nltk
#nltk.download('vader_lexicon')

from layer_classes import my_yaml, my_expressions

class my_collector(object):    
    def __init__(self):    
        # Record number of requests
        my_collector.__requests = 0
        
        # Configs
        myy = my_yaml.my_yaml()
        bearer_token = myy.get_value("config", "search_tweets_api", "bearer_token")
        my_collector.__config = myy.get_value("config", "search_tweets_api", "config")         
        my_collector.__headers = {"Authorization": "Bearer {}".format(bearer_token)}
        del myy, bearer_token
    
    def __del__(self):
        del my_collector.__headers
    
    @staticmethod
    def get_tweets(query, expansions, start_time, end_time = None, is_conversation = False):
        url = my_collector.__create_url(query, expansions, start_time, end_time, is_conversation)
        return my_collector.__auth_and_connect(url)
    
    def __create_url(query, expansions, start_time, end_time, is_conversation):
        # Check lenght as for Academic Reserach track product, queries would have a lenght no longer than 1024.
        if len(query) > int(my_collector.__config["max_query_len"]):
            print(query)
            raise ValueError("Query built excits the max lenght allowed")
        
        # Query
        query_str = "query={}".format(urllib.parse.quote(query))
        
        # Num of results from response
        max_results_str = 'max_results={}'.format(my_collector.__config["max_results"])
        
        # Expantions
        expansions_str = "expansions={}".format(expansions)
        
        # Dates
        # Y-m-dTH:M:SZ format
        tweet_format_date = lambda d: d.strftime('%Y-%m-%dT%H:%M:%SZ')
        start_date_str = "start_time={}".format(tweet_format_date(start_time))
        end_date_str = ""
        
        is_today = False
        # Stay in the same day
        if start_time == date.today():
            is_today = True
        
        if not (is_conversation or is_today):
            if end_time:
                end_date_str = "end_time={}".format(tweet_format_date(end_time))
            else:
                raise ValueError("No end time specified.")
            
            url = "https://api.twitter.com/2/tweets/search/all?{}&{}&{}&{}&{}".format(query_str, max_results_str, start_date_str, end_date_str, expansions_str)
        
        else:
            url = "https://api.twitter.com/2/tweets/search/all?{}&{}&{}&{}".format(query_str, max_results_str, start_date_str, expansions_str)

        return url
        
    def __auth_and_connect(url):
        try_request = 0
        answer = None
        if int(my_collector.__requests) >= int(my_collector.__config["max_requests"]):
            # Academic reserch tracker for full-archive has a rate limit of 300 requests / 15 min
            # It is needed to wait for 15 minutes and then keep collecting
            print(datetime.today())
            print("Waiting for 15 minutes as 300 requests (max) have been called to API...")
            my_collector.__requests = 0
            time.sleep(900)
        
        while True:
            try:
                response = requests.request("GET", url, headers = my_collector.__headers)
                res_json = response.json()
                my_collector.__requests += 1
                break
            
            except:
                err = sys.exc_info()
                print(err)
                # Just try three times, if so ask user what to do
                if try_request > 3:
                    while answer not in ["1", "0"]:
                        answer = input("(1) Try again (three attempts)? (0) Exit?")
                        print(type(answer))
                    if answer == "1":
                        try_request = 0 # continue
                        answer = None
                    else:
                        raise ValueError(err) 
                        # exit
                print("Tyring again...")
                time.sleep(10) # wait for 15 sec
                try_request += 1                
        
        time.sleep(1) # wait a sec
        
        return res_json

class my_preprocessor(object):    
    def __init__(self):
        """This class is designed for preprocessing of tweets. This involves cleaning, normalization and tokenization"""
        # List of words and synonyms of an specific word.
        # Keywords to be threated as stopwords for tokenization
        pp.set_options(pp.OPT.EMOJI, pp.OPT.SMILEY)
  
        my_preprocessor._stop_words = stopwords.words('english')
        my_preprocessor.__normalized_objects = ['url', 'email', 'phone', 'user', 'time', 'date', 'money', 'percent']
        my_preprocessor.__annotate_objects = {"elongated", "repeated"}
        
        # This would be used for hashtag extraction and clea and normalized the sentence.
        #  This code ws taken from https://github.com/cbaziotis/ekphrasis
        #  Cite: DataStories at SemEval-2017 Task 4: Deep LSTM with Attention for Message-level and Topic-based Sentiment Analysis
        my_preprocessor._text_processor = TextPreProcessor(
            
            normalize = my_preprocessor.__normalized_objects,
            annotate = my_preprocessor.__annotate_objects,
                
            # fix HTML tokens
            fix_html = True,
            fix_text = False,
            
            # corpus from which the word statistics are going to be used 
            # for word segmentation 
            segmenter = "twitter", 
            
            # corpus from which the word statistics are going to be used 
            # for spell correction
            corrector = "twitter", 
            
            unpack_hashtags = False,  # perform word segmentation on hashtags  
            unpack_contractions = True,  # Unpack contractions (can't -> can not)
            spell_correction = True,  # spell correction for elongated words
            spell_correct_elong = False, # spell correction for elongated words   
            
        )   
        
        my_preprocessor.__hashtags = TextPreProcessor(
            # terms that will be annotated
            annotate = {"hashtag"},        
              
            # corpus from which the word statistics are going to be used 
            # for word segmentation 
            segmenter = "twitter", 
            
            # perform word segmentation on hashtags        
            unpack_hashtags = True,         
            
        )
        
        # NLP global variable would be use dfor stop words and lemma convertion.
        my_preprocessor.__nlp = spacy.load('en_core_web_md')                      
        my_preprocessor.__en_dict = enchant.Dict("en_US")
                
        #ABB_PIPE_ = AbbreviationDetector(NLP_)
        #NLP_.add_pipe(ABB_PIPE_)
    
    def __del__(self):
        del my_preprocessor.__nlp, my_preprocessor.__en_dict, my_preprocessor.__hashtags
        del my_preprocessor._text_processor
    
    # Clean name of user that is display on screen
    @staticmethod
    def clean_basic(text):
        """
        Static method
        Basic process of cleaning for short text such as username or hashtag strings.

        Parameters
        ----------
        text : String
            Short text such as user name or hashtag to clean.

        Returns
        -------
        text : String
            Cleaned short text.

        """
        # Convert all anmed and numeric character references in strings 
        text = unescape(text)
        
        # Remove ASCII characters
        text = re.sub(r'[^\x00-\x7F]+','', text)
        
        # Remove punctuation
        text = re.sub(r'[^\w\s]', '', text)
        
        # Remove extra spaces
        text = re.sub(r'(\s+)', ' ', text)
        
        # Remove spaces from beginning and end
        text = text.strip()
        
        return text        
    
    @staticmethod
    def clean_tweet(tweet):
        """
        Static method
        Cleaning tweet by doing the following:
        Removing: URLS, emails, phone, dates, mentions
        Dealing with contractions
        Remove accented characters.
        Dealing with hashtags
        
        As this is just a cleaning process, puntation would remain.
        Hashtags would be processed too (if multiple words, splitting process)
        Emojis and emoticons would be translated into respective meaning

        Parameters
        ----------
        tweet : String
            Tweet string to be cleaned.

        Returns
        -------
        tweet : String
            Cleaned tweet.

        """
        # Convert all anmed and numeric character references in strings 
        tweet = unescape(tweet)
        
        # Word to number convertion
        tweet = alpha2digit(tweet, 'en')
        
        # Replace accented characters
        tweet = my_preprocessor.__replace_dictionary(tweet, my_expressions._accented_vowels, True, False)
        
        # Remove RT @Mentions: pattern
        tweet = re.sub(r'RT\s@(\w+):', '', tweet, flags = re.IGNORECASE)
        
        # Remove number
        pattern = r"\d+[stndhr]{1,2}"
        tweet = re.sub(pattern, "", tweet)   
        del pattern

        # Remove number
        # Phone numbers
        pattern =  r"[+]?\s?\d+[\d\-\s]+\d"
        tweet = re.sub(pattern, "", tweet)   
        del pattern

        # Remove Digits except covid-19
        tweet = re.sub(r"(?:((covid.?19)|(c19)|(sars.?cov.?2?)|(mrna.?1273)|(bnt.?162(b2)?)|(AZD.?1222)|(NVX.?CoV.?2373))|[\d]+)(?=\D|$)", r"\1", tweet, flags = re.IGNORECASE)
        
        # Remove other items, indicated on pattern
        tweet = my_preprocessor._text_processor.pre_process_doc(tweet)
        
        pattern = r"<(" + "|".join(my_preprocessor.__normalized_objects) + r")>"
        tweet = re.sub(pattern, "", tweet)   
        del pattern

        # Other annotations
        pattern = r"<(" + "|".join(my_preprocessor.__annotate_objects) + r")>"
        tweet = re.sub(pattern, "", tweet)        
        del pattern
        
         # Replace emoticons  
        tweet = my_preprocessor.__replace_dictionary(tweet, emoticons, False, True)
        tweet = my_preprocessor.__replace_dictionary(tweet, my_expressions._emoticons, False, True)
        
        # Replace emojis
        tweet = my_preprocessor.__replace_dictionary(tweet, my_expressions._emojis, False, True)
            
        # Clean emojis
        tweet = pp.clean(tweet)
        
        # Remove interjections by their meaning
        # Avaiable from: https://www.vidarholen.net/contents/interjections/
        tweet = re.sub(r'\bhm+!*\b', '', tweet, flags = re.IGNORECASE)
        tweet = re.sub(r'\bgrr+!*\b', '', tweet, flags = re.IGNORECASE)
        tweet = re.sub(r'\bh(ar)?umph!*\b', '', tweet, flags = re.IGNORECASE)
        tweet = re.sub(r'\b(h[ae])+h?\b', '', tweet, flags = re.IGNORECASE)
        tweet = re.sub(r'\bhuh\b', '', tweet, flags = re.IGNORECASE)
        tweet = re.sub(r'\b((hurrah)|(hooray)|(huzzah))!*\b', '', tweet, flags = re.IGNORECASE)
        tweet = re.sub(r'\b((ick)|(yuck)|(ich)|(yak)|(yuck)|(ew{1,})|(blech)|(bleh))!*\b', '', tweet, flags = re.IGNORECASE)
        tweet = re.sub(r'\bm?eh\b', '', tweet, flags = re.IGNORECASE)
        tweet = re.sub(r'\b((m{1,}hm)|(uh-hu)|(yay)|(ye+a+h))!*\b', '', tweet, flags = re.IGNORECASE)
        tweet = re.sub(r'\bw+o+w+!*\b', '', tweet, flags = re.IGNORECASE)
        tweet = re.sub(r'\b((wa+h)|(boo+-?hoo+))!*\b', '', tweet, flags = re.IGNORECASE)
        tweet = re.sub(r'\bwho+a+!*\b', '', tweet, flags = re.IGNORECASE)
        tweet = re.sub(r'\b((uhh+)|(uhm)|(err+)|(umm+))!*\b', '', tweet, flags = re.IGNORECASE)
        tweet = re.sub(r'\b((shh+)|(hush)|(shush))!*\b', '', tweet, flags = re.IGNORECASE)
        tweet = re.sub(r'\b((ouch)|(ow+)|(yeow))!*\b', '', tweet, flags = re.IGNORECASE)
        tweet = re.sub(r'\b((pff+[th]?)|(pss+h))!*\b', '', tweet, flags = re.IGNORECASE)
        tweet = re.sub(r'\b((argh)|(augh))!*\b', '', tweet, flags = re.IGNORECASE)
        tweet = re.sub(r'\b(n+a+h+!*)\b', '', tweet, flags = re.IGNORECASE)        
        tweet = re.sub(r'\boh!*\b', '', tweet, flags = re.IGNORECASE)  
        tweet = re.sub(r'\boo+h!*\b', '', tweet, flags = re.IGNORECASE)  
        tweet = re.sub(r'\b(wh)?oo+ps!*\b', '', tweet, flags = re.IGNORECASE)  
        tweet = re.sub(r'\bphe+w!*\b', '', tweet, flags = re.IGNORECASE)  
        tweet = re.sub(r'\b[uo]h[ -]oh!*\b', '', tweet, flags = re.IGNORECASE)  
        tweet = re.sub(r'\b((zing)|(badum tish))!*\b', '', tweet, flags = re.IGNORECASE)  
        tweet = re.sub(r'\b[oa]hh+\b', '', tweet, flags = re.IGNORECASE)
        tweet = re.sub(r'\b((aa+hh+)|(ee+k))\b', '', tweet, flags = re.IGNORECASE)
        tweet = re.sub(r'\ba-?ha\b', '', tweet, flags = re.IGNORECASE)
        tweet = re.sub(r'\bahem\b', '', tweet, flags = re.IGNORECASE)
        tweet = re.sub(r'\bboo+h?\b', '', tweet, flags = re.IGNORECASE)
        tweet = re.sub(r'\bbrr+h?!\b', '', tweet, flags = re.IGNORECASE)
        tweet = re.sub(r'\bdu+h+!*\b', '', tweet, flags = re.IGNORECASE)
        tweet = re.sub(r'\b[bm][wu]ahaha!*\b', '', tweet, flags = re.IGNORECASE)
        tweet = re.sub(r'\bshoo+!*\b', '', tweet, flags = re.IGNORECASE)
        tweet = re.sub(r'\bwoo+h+oo+!*\b', '', tweet, flags = re.IGNORECASE)
        tweet = re.sub(r'\b(yeah\s?)*\b', '', tweet, flags = re.IGNORECASE)
        tweet = re.sub(r'\b(blah\s?)*\b', '', tweet, flags = re.IGNORECASE)
        tweet = re.sub(r'\b(bah\s?)*\b', '', tweet, flags = re.IGNORECASE)
        
        # Replace censored words by real meaning
        tweet = re.sub(r'\bf[#*]{2}([keding]{1,4})\b', r'fuc\1', tweet, flags = re.IGNORECASE) 
        tweet = re.sub(r'\bc[#*]{2}t\b', 'cunt', tweet, flags = re.IGNORECASE)
        tweet = re.sub(r's[#*]{2}([keding]{1,4})\b', r'shit\1', tweet, flags = re.IGNORECASE)
        tweet = re.sub(r'\bt[#*]{2}t\b', 'twat', tweet, flags = re.IGNORECASE)
        tweet = re.sub(r'\bb[#*]{2}((ks)|(ox)|(ix))\b', 'bollocks', tweet, flags = re.IGNORECASE)
        tweet = re.sub(r'\bp[#*]{2}k\b', 'prick', tweet, flags = re.IGNORECASE)
        tweet = re.sub(r'\bar[#*]{2}\b', 'asshole', tweet, flags = re.IGNORECASE)
        tweet = re.sub(r'\bh[#*]{2}e\b', 'hore', tweet, flags = re.IGNORECASE)
        tweet = re.sub(r'\bd[#*]{2}([keding]{1,4})\b', r'dic\1', tweet, flags = re.IGNORECASE)
        tweet = re.sub(r'\btr[#*]{2}p\b', 'trap', tweet, flags = re.IGNORECASE)
        tweet = re.sub(r'\bf[#*]{2,}\b', 'fuck', tweet, flags = re.IGNORECASE)
        tweet = re.sub(r'\bc[#*]{2,}\b', 'cunt', tweet, flags = re.IGNORECASE)
        tweet = re.sub(r's[#*]{2,}\b', 'shit', tweet, flags = re.IGNORECASE)
        tweet = re.sub(r'\bt[#*]{2,}\b', 'twat', tweet, flags = re.IGNORECASE)
        tweet = re.sub(r'\bb[#*]{2,}\b', 'bollox', tweet, flags = re.IGNORECASE)
        tweet = re.sub(r'\bp[#*]{2,}\b', 'prick', tweet, flags = re.IGNORECASE)
        tweet = re.sub(r'\bar[#*]{2,}\b', 'asshole' , tweet, flags = re.IGNORECASE)
        tweet = re.sub(r'\bh[#*]{2,}\b', 'hore', tweet, flags = re.IGNORECASE)
        tweet = re.sub(r'\bd[#*]{2,}\b', 'dick', tweet, flags = re.IGNORECASE)
        
        # Replace slang
        tweet = my_preprocessor.__replace_dictionary(tweet, my_expressions._slangs, True, True)
        
        # Remove special html characters
        tweet = BeautifulSoup(unescape(tweet), 'lxml').text
        
        # Remove ASCII characters
        tweet = re.sub(r'[^\x00-\x7F]+',' ', tweet)
        
        # Remove extra spaces
        tweet = re.sub(r'(\s+)', ' ', tweet)
        
        # Remove spaces from beginning and end
        tweet = tweet.strip()
        
        return tweet

    @staticmethod
    def __replace_dictionary(tweet, dictionary, replace, by_word):
        for k, v in dictionary.items():
            if by_word:
                if replace:
                    tweet = re.sub(r'\b'+re.escape(k)+r'\b', v, tweet)

                else:
                    tweet = re.sub(r'\b'+re.escape(k)+r'\b', '', tweet)

            else:
                if replace:
                    tweet = tweet.replace(k, v)                    

                else:
                    tweet = tweet.replace(k, ' ')

        return tweet
 
    @staticmethod
    def normalize_tweet(tweet):
        """
        Normalize tweets by removing numbers, percentages, money, puntuation, stop words and lemmatization process

        Parameters
        ----------
        tweet : String
            Tweet string. This sohould be a cleaned tweet to let this methodo to perform better.
        
        Returns
        -------
        tweet : String
            Tweet string normalized.

        """
        # Lowercase
        tweet = tweet.lower()
        
        # Normalize covid19 and sars cov words with covid
        tweet = re.sub(r"\b((covid.?19)|(sars.?cov.?2?))\b", r"covid", tweet, flags = re.IGNORECASE)
        
        # When expanding hashtags there is a problem with covid word, 
        #  i could not find a way to add covid in the vocabulary list from
        #  this specific library, so i decided to loop through all tokens,
        #  look up for hashtags and fix the wrong expantion on covid        
        tweet_lst = list()
        for t in tweet.split():
            word = t
            if "#" in t:
                word = my_preprocessor.__hashtags.pre_process_doc(t)
                if "covid" in t:
                    word = re.sub(r"<hashtag>(.+)(co\s?vid)(.+)</hashtag>", r"\1 covid \3", word, flags = re.IGNORECASE)
                else:
                    word = re.sub(r"</?hashtag>", "", word, flags = re.IGNORECASE)
            word = re.sub(r'(\s+)', ' ', word)
            word = word.strip()
            tweet_lst.append(word)    
        tweet = " ".join(tweet_lst)  
        del tweet_lst
        
        # Remove keywords from collector process
        for k in my_preprocessor.__my_keywords:
            tweet = re.sub(r'\b'+k+r'\b', ' ', tweet, flags = re.IGNORECASE)
        
        # Possesion remplacement
        tweet = tweet.replace("'s", '')
        
        # Remove Punctuations
        tweet = re.sub(r'[' + re.escape(string.punctuation) + r']', ' ', tweet)
        
        # Remove extra spaces
        tweet = re.sub(r'(\s+)', ' ', tweet)
        
        # Lemmatization process
        doc = my_preprocessor.__nlp(tweet)        
        tweet_lst = list()
        for token in doc:
            new_token = token.text.strip()
            if len(new_token.replace(' ', '')) < 2:
                continue
            
            if (new_token in my_preprocessor._stop_words or token.is_stop) and new_token not in ['not', 'no']:
                continue
            
            if not my_preprocessor.__en_dict.check(new_token):
                continue
            
            new_token = token.lemma_            
            tweet_lst.append(new_token)

        return tweet_lst         
    
    @staticmethod
    def get_hashtags(tweet):
        """
        Extract all hashtags (no duplicated items)

        Parameters
        ----------
        tweet : String
            Tweet string to extract hashtags.
        
        Returns
        -------
        hashtags : List of dictionaries
            List of hashtags found in tweet string. Return two parts: the original and the cleaned text.

        """
        # Convert all anmed and numeric character references in strings 
        tweet = unescape(tweet)
        
        # Start process of extraction
        hashtags = list()
        for t in tweet.split():
            word = t
            if "#" in t:
                word = my_preprocessor.__hashtags.pre_process_doc(word)
                # There is a problem with covid word, need to be fixed manually
                if "covid" in t:
                    word = re.sub(r"<hashtag>(\s|.+)(co\s?vid)(\s|.+)</hashtag>", r"\1 covid \3", word)
                else:
                    word = re.sub(r"</?hashtag>", "", word)
            else:
                continue
            word = my_preprocessor.clean_basic(word)
            h = {'original':t.replace("#", ''), 'cleaned':word}
            
            if h not in hashtags:
                hashtags.append(h)
        
        return hashtags

class my_keywords(object):
    def __init__(self):
        myy = my_yaml.my_yaml_tweet()
        my_keywords.__my_keywords = myy.get_keywords_covid_vaccine()
        my_keywords.__my_keywords_pharma = myy.get_keywords_covid_vaccine_pharma()
        del myy

    @staticmethod
    def __get_keywords(tweet, keywords):
        # Remove keywords from collector process
        keywords_lst = list()
        for k in keywords:
            if len(re.findall(r'\b'+re.escape(k)+r'\b', tweet, flags = re.IGNORECASE)) > 0:
                keywords_lst.append(k)
        return keywords_lst
    
    @staticmethod
    def get_all_keywords(tweet):
        covid_vaccine = my_keywords.__get_keywords(tweet, my_keywords.__my_keywords)
        covid_vaccine_pharma = my_keywords.__get_keywords(tweet, my_keywords.__my_keywords_pharma)
        
        return covid_vaccine, covid_vaccine_pharma

class my_lexicon_labeller(object):
    def __init__(self):
        my_lexicon_labeller.__sentiment_analyzer = SentimentIntensityAnalyzer()

    def __del__(self):
        del my_lexicon_labeller.__sentiment_analyzer, my_lexicon_labeller.__my_keywords

    @staticmethod
    def __polarity_scores(tweet):
        return my_lexicon_labeller.__sentiment_analyzer.polarity_scores(tweet)
    
    @staticmethod
    def __simple_cleaning(tweet):
        tweet = re.sub(r'["#$%&\'()*+,-/:;<=>@[\\]^_`{|}~]', '', tweet) # except !?.
        return tweet.lower()

    @staticmethod
    def get_polarity_score(tweet):
        # Set preprossesing configurations
        # Quick cleaning to get polarity score
        tweet = my_lexicon_labeller.__simple_cleaning(tweet)

        # Check if tweet has characters and replacing spaces
        if len(tweet.replace(' ', '')) == 0:
            return 0, 'neutral'

        # Get polarity score
        score = my_lexicon_labeller.__polarity_scores(tweet)
        threshold = 0.05        
        tem = 0 # neutral
        label = 'neutral'
        
        if score['compound'] >= threshold:
            tem = 1 # positive
            label = 'positive'
        elif score['compound'] <= -threshold:
            tem = 2 # negative
            label = 'negative'

        return tem, label

class my_labeller(object):
    def __init__(self):        
        my_labeller.__sentiment_model = joblib.load('../model/my_sentiment_model.sav') 

    def __del__(self):
        del my_labeller.__sentiment_model

    @staticmethod
    def get_polarity_score(tweet):
        # Set preprossesing configurations
        # No cleaning process needed, as tweet must be sent cleaned and normalized.
        # Check if tweet has characters and replacing spaces
        if len(tweet.replace(' ', '')) == 0:
            return 0, 'neutral'

        label = my_labeller.__sentiment_model.predict([tweet])[0]
        tem = 0
        if label == 'positive':
            tem = 1 # positive
        elif label == 'negative':
            tem = 2 # negative

        return tem, label



        