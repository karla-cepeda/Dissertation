# -*- coding: utf-8 -*-
"""
@author: Karla Aniela Cepeda Zapata
@studnetID: d00242569
@institute: Dundalk Institute of Technology
@supervisor: Rajesh Jaswal

"""
import yaml
import re

class my_yaml(object):
    def __init__(self):
        self._path = 'layer_configurations/'
        self._extention = '.yaml'
        
    def get_value(self, filename, rootname, keyname):    
        data = self.get_data(filename, rootname)
        value = data[keyname]
        del data
        return value
        
    def get_data(self, filename, rootname):
        pattern = re.compile(r'(\s|^)({0})$'.format(self._extention), flags=re.IGNORECASE)
        if pattern.search(filename):
            filename = re.sub(pattern, '', filename)
        with open(self._path + filename +  self._extention) as file:
            data = yaml.safe_load(file)
        return data[rootname]
    
class my_yaml_tweet(my_yaml):
    def __init__(self):
        super().__init__()
        self._filename = "myTweet"
        
    def get_keywords(self):
        return super().get_data(self._filename, "keywords")
    
    def get_bacthes(self):
        return super().get_data(self._filename, "config_batches")
    
    def get_keywords_covid_vaccine(self):
        data = self.get_keywords()        
        keywords = list()
        keywords.extend(data['vaccine'])
        keywords.extend(data['covid'])
        keywords.extend(data['place'])
        keywords = [k.replace("#", "").replace("place:", "") for k in keywords]
        keywords = set(keywords)
        
        return keywords
    
    def get_keywords_covid_vaccine_pharma(self):
        data = self.get_keywords()        
        keywords = list()
        keywords.extend(data['cvaccine'])
        keywords = set(keywords)
        
        return keywords
    
    def get_username_covid_vaccine(self):
        data = self.get_keywords()        
        usernames = dict()
        usernames['media'] = data['media']
        usernames['political_parties'] = data['political_parties']
        usernames['gov_public_figures'] = data['gov_public_figures']
        usernames['gov_departments'] = data['gov_departments']
        usernames['health_public_figures'] = data['health_public_figures']

        return usernames
    
    def get_repositories(self):
        return super().get_data(self._filename, "repositories")
        
    def get_default_config(self):
        return super().get_data(self._filename, "collection_config")
        
class my_yaml_config(my_yaml):
    def __init__(self):
        super().__init__()
        self._filename = "config"
    
    def get_mysql_conn(self):
        return super().get_data(self._filename, "mysql_conn")

    def get_azure_conn(self):
        return super().get_data(self._filename, "azure_conn")

    def get_mysql_conn_hostgator(self):
        return super().get_data(self._filename, "mysql_conn_hostgator")
    
class my_yaml_mydb(my_yaml):
    def __init__(self):
        super().__init__()
        self._filename = "mydb"
        
    def get_stored_procedure_names_twitter(self):
        return super().get_value(self._filename, "stored_procedures", "twitter")
    
    def get_stored_procedure_names_dcovid(self):
        return super().get_value(self._filename, "stored_procedures", "dcovid")
        
    def get_stored_procedure_names_sentimentanalysis(self):
        return super().get_value(self._filename, "stored_procedures_hostgator", "sentimentanalysis")