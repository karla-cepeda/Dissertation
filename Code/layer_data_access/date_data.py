# -*- coding: utf-8 -*-
"""
@author: Karla Aniela Cepeda Zapata
@studnetID: d00242569
@institute: Dundalk Institute of Technology
@supervisor: Rajesh Jaswal

This module provides access to database that stores dates.

"""
import datetime
from layer_classes import my_database, my_yaml

class data(object):
    def __init__(self, db, local):
        """
        Constructor.
        Class parent. Children below.
        Set up database connection
        
        """
        self._db = my_database.myDB(db, local)
        data._convert_date = lambda dstr: datetime.datetime.strptime(dstr, '%d %B %Y').strftime("%Y-%m-%d")

    def __del__(self):
        del self._db
        
class date_data(data):
    def __init__(self):
        super().__init__('dcovid', True)

        # Get name of stored procedure
        myy = my_yaml.my_yaml_mydb()
        sp_list = myy.get_stored_procedure_names_dcovid()
        date_data.__sp_truncate_tables = sp_list["truncate_table"]
        date_data.__sp_insert_date = sp_list["insert_date"]
        date_data.__sp_insert_reference = sp_list["insert_reference"]
        date_data.__sp_insert_date_reference = sp_list["insert_date_reference"]
        date_data.__sp_get_dates_for_migration = sp_list["get_dates_for_migration"]
        date_data.__sp_get_date_reference_for_migration = sp_list["get_date_reference_for_migration"]
        date_data.__sp_get_reference_for_migration = sp_list["get_reference_for_migration"]
        date_data.__sp_insert_migration = sp_list["insert_migration"]
        date_data.__sp_lookup_date = sp_list["lookup_date"]
        
        del sp_list, myy
    
    def truncate_tables(self):
        self._db.call_sp(self.__sp_truncate_tables)      

    def insert_date(self, date, description):        
        # convert date into correct format
        date_str = data._convert_date(date)
                
        # List of arguments to send to stored procedure
        args = (date_str, description, 1,)
        
        self._db.call_sp(self.__sp_insert_date, args)
        date_id = self._db.get_results()[0][0] # get id created from previous stored procedure
        
        return date_id
    
    def insert_reference(self, ref_description, ref_date_txt, ref_available_from, ref_retrived_txt):
        # Convert date to proper format
        if ref_date_txt:
            ref_date_txt = data._convert_date(ref_date_txt)
          
        # Convert date to proper format
        if ref_retrived_txt:
            ref_retrived_txt = data._convert_date(ref_retrived_txt)
        
        # List of arguments to send to stored procedure
        args = (ref_description, ref_date_txt, ref_available_from, ref_retrived_txt,)
        
        # Insert references
        self._db.call_sp(self.__sp_insert_reference, args)
        reference_id = self._db.get_results()[0][0] # get id created from previous stored procedure
        
        return reference_id
    
    def insert_date_reference(self, date_id, reference_id):
        # List of arguments to send to stored procedure
        args = (date_id, reference_id)
        self._db.call_sp(self.__sp_insert_date_reference, args)

    def get_dates_for_migration(self):
        self._db.call_sp(self.__sp_get_dates_for_migration)        
        results = self._db.get_results_dataframe()        
        return results

    def get_date_reference_for_migration(self):
        self._db.call_sp(self.__sp_get_date_reference_for_migration)
        results = self._db.get_results_dataframe()        
        return results      

    def get_reference_for_migration(self):
        self._db.call_sp(self.__sp_get_reference_for_migration)
        results = self._db.get_results_dataframe()        
        return results     
         
    def insert_migration(self, id):
        self._db.call_sp(self.__sp_insert_migration, (id, ))

    def lookup_date(self, date, description):      
        # convert date into correct format
        date_str = data._convert_date(date)

        args = (str(date_str), description)
        self._db.call_sp(self.__sp_lookup_date, args)
        results = self._db.get_results_dataframe()        
        return results        

class date_data_remote(data):
    def __init__(self):
        super().__init__('tanniest_sentimentanalysis', False)

        # Get name of stored procedure
        myy = my_yaml.my_yaml_mydb()
        sp_list = myy.get_stored_procedure_names_sentimentanalysis()
        date_data_remote.__sp_insert_date = sp_list["insert_date"]
        date_data_remote.__sp_insert_reference = sp_list["insert_reference"]
        date_data_remote.__sp_insert_date_reference = sp_list["insert_date_reference"]
        date_data_remote.__sp_insert_tweet_date = sp_list["insert_tweet_date"]
        
        del sp_list, myy
    
    def insert_date(self, id, date, description, from_ireland):        
        # convert date into correct format
        args = (int(id), date, description, int(from_ireland),)
        self._db.call_sp(self.__sp_insert_date, args)
    
    def insert_reference(self, id, description, date, url, retrieved_date):
        # List of arguments to send to stored procedure
        args = (int(id), description, date, url, retrieved_date,)
        self._db.call_sp(self.__sp_insert_reference, args)
        
    def insert_date_reference(self, date_id, reference_id):
        # List of arguments to send to stored procedure
        args = (int(date_id), int(reference_id))
        self._db.call_sp(self.__sp_insert_date_reference, args)

    def insert_tweet_date(self):
        self._db.call_sp(self.__sp_insert_tweet_date)


    

