# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 16:02:26 2021

@author: Karla Aniela Cepeda Zapata
@studnetID: d00242569
@institute: Dundalk Institute of Technology
@supervisor: Rajesh Jaswal

This python scritp contains the process to scrap the website Wikipedia that contains 
important dates and events related to covid in Ireland.

"""
import pandas as pd
import numpy as np

import requests
from bs4 import BeautifulSoup
import datetime
import re

from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

from layer_data_access import date_data

class date_logic(object):
    def __init__(self):
        """
        Costructor.
        Preparing variables for environment
        Global variables
        
        """
        print("Prepering global variables...")
        month_list = date_logic.__get_month_list()
        date_logic.__PATTERN_DATE_ = re.compile("\d{1,2}\s("+"|".join(month_list)+")\s?–?\s?")
        date_logic.__PATTERN_RETRIVE_ = re.compile("\.\sRetrieved\s\d{2}\s("+"|".join(month_list)+")\s\d{4}\.$")
        date_logic.__PATTERN_DATE_REF_ = re.compile("\.?\s\(?\d{1,2}\s("+"|".join(month_list)+")\s\d{4}\)?")
        date_logic.__PATTERN_REFERENCE_ = re.compile("\[\d{1,4}\]")
        del month_list

    @staticmethod
    def __get_month_list():
        # Get list of months
        month_list = []
        for i in range(1,13):
            month_list.append(datetime.date(2008, i, 1).strftime('%B'))        
        return month_list

    @staticmethod
    def __is_date_pattern(text):       
        # Check patterns sent
        return date_logic.__PATTERN_DATE_.match(text)

    @staticmethod
    def __remove_empty_item_list(lst):
        # Remove empty items from list
        return list(filter(None, lst))

    @staticmethod
    def __get_url_main_list():
        """
        Get urls from wikipedia for scrapping process  

        Returns
        -------
        href_lst : List
            DESCRIPTION. List of all pages that contain dates and events from covid in Ireland.

        """
        url = r'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_the_Republic_of_Ireland'
        r = requests.get(url)
        html_doc = r.text
        soup = BeautifulSoup(html_doc, 'lxml')
        
        url_lst = soup.find("ul").find_all("a")
        href_lst = []
        
        for url in url_lst:
            href_lst.append(url["href"])
        
        return href_lst

    @staticmethod
    def __capitalize_first_word_sentence(text):
        """
        Capitalize first word of a sentence

        Parameters
        ----------
        text : String
            DESCRIPTION. Description of the event in a date.

        Returns
        -------
        String
            DESCRIPTION. Capitalize description.

        """
        words = text.split()
        first_word = words[0].capitalize()
        rest_words = " ".join(words[1:])    
        return first_word + " " + rest_words

    @staticmethod
    def __clean_text(text):
        """
        Clean text removing date, references

        Parameters
        ----------
        text : String
            DESCRIPTION. Description of the event in a date.

        Returns
        -------
        text : string
            DESCRIPTION. Cleaned description of the event.

        """
        date_index = re.match(date_logic.__PATTERN_DATE_, text)
        if date_index:
            text = text[date_index.span()[1]:]
            
        text = date_logic.__PATTERN_REFERENCE_.sub("", text)            
        text = date_logic.__capitalize_first_word_sentence(text)
        
        return text

    @staticmethod
    def __is_case_death_text(text):
        """
        
        Check if text contains figures of new confirmed cases and deaths
         as this is no relevant information for the timeline

        Parameters
        ----------
        text : String
            DESCRIPTION. Description of the event in a date.

        Returns
        -------
        bool
            DESCRIPTION. Indicates if general text has been found

        """
        examples = ["more case was confirmed bringing the total to",
                    "new cases were reported, bringing the total to",
                    "new cases were confirmed, bringing the total cases in the country to",
                    "a further cases and deaths (including 3 probable deaths) were reported, and deaths previously reported were reclassified as unrelated to COVID-19, bringing the totals to cases and deaths",
                    "a further cases and death were reported, bringing the totals to cases and deaths",
                    "previously notified case was de-notified",
                    "A further cases and deaths were reported, bringing the totals to cases and deaths.",
                    "A further cases were reported, however data relating to the number of COVID-19 deaths and total number of cases were not available due to the HSE cyberattack.",
                    "new cases were confirmed.",
                    "The total number of cases stood at with deaths."]
        
        sentences = sent_tokenize(text)
        num_examples = len(examples)
        sentences_duplicated = 0
        for s in sentences:
            examples.append(s)
        
        tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        sparse_matrix = tfidf_vectorizer.fit_transform(examples)
        
        # Get similarity score
        cosine_sim = linear_kernel(sparse_matrix, sparse_matrix)
        similarity = pd.DataFrame(cosine_sim).iloc[:num_examples,num_examples:] # convert to dataframe
        
        # Loop on each column
        for index in np.arange(similarity.shape[1]):
            # Convert to numpy array
            a = np.array(similarity.iloc[:,index])
            # Select just values where similarity is greater than 0.4
            if len(np.where(a>0.4)[0])>0:
                sentences_duplicated += 1
        
        # If same number of setences were identified as duplicated, it is a sentences telling just number of cases
        # therefore, there is no relevant information.
        if len(sentences) == sentences_duplicated:
            return True

        return False

    @staticmethod
    def __get_reference_info(soup, date):
        """
        Get reference from date processed  

        Parameters
        ----------
        soup : beautiful soup object
            DESCRIPTION. Contains all html structure of the url accessed
        date : datetime
            DESCRIPTION. Date in process.

        Returns
        -------
        ref_list : TYPE
            DESCRIPTION.

        """
        ref_list = []
        for a in date.find_all("a"):
            href = a["href"].replace("#", "").strip()
            ref = soup.find("li", {"id": href})
            
            if ref:
                ref_dic = {}
                for c in ref.find_all("cite"):
                    ref_text = c.text
                    
                    # Get description
                    ref_description = date_logic.__PATTERN_RETRIVE_.sub("", ref_text)
                    
                    # Get original URL reference
                    ref_available_from = c.find("a")["href"]
                    
                    # Get date of access
                    ref_retrived_index = date_logic.__PATTERN_RETRIVE_.search(ref_text)
                    if ref_retrived_index:
                        ref_retrived_txt = ref_text[ref_retrived_index.span()[0]:ref_retrived_index.span()[1]].replace(".", "").replace("Retrieved", "").strip()
                    else:
                        ref_retrived_txt = None
                        
                    # Get date of reference
                    ref_date_index = date_logic.__PATTERN_DATE_REF_.search(ref_description)
                    if ref_date_index:
                        ref_date_txt = ref_description[ref_date_index.span()[0]:ref_date_index.span()[1]]
                        ref_date_txt = ref_date_txt.replace("(", "").replace(")", "").replace(".", "").strip()
                        
                        # Remove date of reference from description
                        ref_description = date_logic.__PATTERN_DATE_REF_.sub("", ref_description)

                    else:
                        ref_date_txt = None
                    
                    # Create dictionary with all reference information
                    ref_dic["ref_description"] = ref_description
                    ref_dic["ref_available_from"] = ref_available_from
                    ref_dic["ref_retrived_txt"] = ref_retrived_txt
                    ref_dic["ref_date_txt"] = ref_date_txt
                    
                    # Add to list, as there could be more references for one date.
                    ref_list.append(ref_dic)
                    
        return ref_list
    
    @staticmethod
    def __get_date_references(soup, date, date_txt):
        """
        Process to get cleaned description, and references        

        Parameters
        ----------
        soup : beautiful soup object
            DESCRIPTION. Contains all html structure of the url accessed
        date : datetime
            DESCRIPTION. Date in process.
        date_txt : stirng
            DESCRIPTION. Date in process, but in string format

        Returns
        -------
        date_dict : dictionary
            DESCRIPTION. date and list of references.

        """
        ref_list = []
        date_dict = {}
        date_description_text = date_logic.__clean_text(date.text)
        
        # Find out if text contains figures (no relevant info)
        if date_logic.__is_case_death_text(date_description_text):
            return None
        
        # Find references
        ref_list = date_logic.__get_reference_info(soup, date)
        
        # Final object containing all data related to date
        date_dict["date"] = date_txt
        date_dict["description"] = date_description_text
        date_dict["references"] = ref_list
        
        return date_dict
    
    @staticmethod
    def start_dates_process():
        """
        Get dates from wikipedia urls        

        Returns
        -------
        None.

        """
        # Start dates collection process
        print("Dates collection process has started...")    
        href_lst = date_logic.__get_url_main_list()
        url_root = r'https://en.wikipedia.org'
        dates_list = []
        
        for h in href_lst:
            url = url_root + h
            r = requests.get(url)
            html_doc = r.text
            soup = BeautifulSoup(html_doc, 'lxml')
                
            # Get all list items
            date_lists = soup.find_all("ul")
            
            # Extract year from url
            year_index = re.search(".*\(.*-?.*_?(\d{4})\).*", h)
            year_txt = year_index.group(1)
            
            for date in date_lists:        
                if not date_logic.__is_date_pattern(date.text):
                    continue
                            
                for date2 in date.find_all("li"):
                    if not date_logic.__is_date_pattern(date2.text):
                        continue
                    
                    # Get date string from text
                    date_index = re.match(date_logic.__PATTERN_DATE_, date2.text).span()
                    date_txt = date2.text[date_index[0]:date_index[1]].replace(" – ", "").replace("\n", "") + " " + year_txt
                    
                    if date2.find("ul"):
                        contains_more_ul = False
                        index = 0
                        number_ul = 0
                        for date3 in date2.find("ul").find_all("li"):
                            if not contains_more_ul:
                                # Add new date
                                new_date = date_logic.__get_date_references(soup, date3, date_txt)
                                if new_date:
                                    dates_list.append(new_date)
                                else:
                                    continue
                                
                                # Verify if there is no sub lists as these may be added before, leading to duplication
                                if date3.find("ul"):
                                    # Get all elements within list
                                    results = re.findall("<li>.*</li>", str(date3.find("ul")))
                                    
                                    # Get number of elements within list
                                    number_ul = len(results)
                                    
                                    # Element processed contained list
                                    contains_more_ul = True
                                    
                            else:
                                # Skip sub lists as this information was previously added
                                if index < number_ul:
                                    index += 1
                                    continue
                                else:
                                    # No more bullet points to skip
                                    # Reset all information
                                    contains_more_ul = False
                                    index = 0
                                    number_ul = 0    
                                
                    else:
                        # Add new date
                        new_date = date_logic.__get_date_references(soup, date2, date_txt)
                        if new_date:
                            dates_list.append(new_date)                
                        else:
                            continue
                
                print(len(dates_list), "cumulative block(s)...")
                
        print("All dates have been collected.")

        date_logic.__start_insert_db(dates_list) 
        print("Process has been complited.")
    
    @staticmethod
    def __start_insert_db(dates_list):
        """
        Insert collection result into database

        Parameters
        ----------
        dates_list : list
            DESCRIPTION. List of dates and descriptions.

        Returns
        -------
        None.

        """
        # Start processing to database
        print("Saving to database...")
        print("Insertion process has started...")
        
        # Access to data
        dd = date_data.date_data()
        
        for d in dates_list:
            # Lookup up date exists in database
            results = dd.lookup_date(d["date"], d["description"])
            if type(results) == pd.core.frame.DataFrame:
                if len(results) > 0:
                    # tweet already exists, no need to insert
                    continue
                
            # Insert date
            references = d["references"]
            date_id = dd.insert_date(d["date"], d["description"])
                        
            # Start reference(s) process
            for r in references:
                # Insert reference
                reference_id = dd.insert_reference(r["ref_description"], r["ref_date_txt"], r["ref_available_from"], r["ref_retrived_txt"])
                                
                # Insert relationship between date and reference
                dd.insert_date_reference(date_id, reference_id)
            
            print(d["date"], "date with description", d["description"][:10], " has been inserted into database")

        # Close connextion for next insertion
        del dd
            
        print("All dates and references have been inserted.")