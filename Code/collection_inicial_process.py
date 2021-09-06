# -*- coding: utf-8 -*-
"""
@author: Karla Aniela Cepeda Zapata
@studnetID: d00242569
@institute: Dundalk Institute of Technology
@supervisor: Rajesh Jaswal

"""
from layer_logic import tweet_logic

def main():  
    
    # Collection of data and save raw format
    tweetc = tweet_logic.collection(inicial_collection = True)
    tweetc.start_process(truncate_log_file = True)
    del tweetc
    
    # Preprocess and insert into database
    tweetp = tweet_logic.preparation()
    tweetp.start_process(truncate_tables = True)
    del tweetp

    # Keywords
    tweetk = tweet_logic.keywords()
    tweetk.start_process()
    del tweetk
    
    # Label process
    # For labelling process, just covid_vaccine_global would be labelled
    #  other tweets would be done by using a own model 
    tweetl = tweet_logic.label_process(lexicon_based = True)
    tweetl.start_process()
    del tweetl
    
if __name__ == "__main__":
    main()
