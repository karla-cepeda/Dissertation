# -*- coding: utf-8 -*-
"""
@author: Karla Aniela Cepeda Zapata
@studnetID: d00242569
@institute: Dundalk Institute of Technology
@supervisor: Rajesh Jaswal

"""
import schedule
import time
from datetime import datetime

from layer_logic import tweet_logic, date_logic, migration_logic

def job():
    # Collection of data and save raw format
    print(datetime.today(), "Starting daily process...")
    tweetc = tweet_logic.collection(inicial_collection = False)
    tweetc.start_process()
    del tweetc

    # Preprocess and insert into database
    tweetp = tweet_logic.preparation()
    tweetp.start_process(truncate_tables = False)
    del tweetp
    
    # Keywords
    tweetk = tweet_logic.keywords()
    tweetk.start_process()
    del tweetk
    
    # Deactive tweets with length less or equal to 2
    # This has to be executed first so tweets no labelled are processed.
    tweetda = tweet_logic.deactive_process()
    tweetda.start_process()
    del tweetda

    # Label process using SVM algorithm
    tweetl = tweet_logic.label_process(lexicon_based = False)
    tweetl.start_process()
    del tweetl

    # Get covid dates dates
    datec = date_logic.date_logic()
    datec.start_dates_process()
    del datec
    
    # Migration from local database to remote
    tweet_migration = migration_logic.tweet_migrate()
    tweet_migration.start_process()
    del tweet_migration

    print(datetime.today(), "Daily process completed.")

schedule.every().day.at("23:50").do(job)
print("Process has been scheduled...")
while True:
    # run_pending
    schedule.run_pending()
    time.sleep(1)