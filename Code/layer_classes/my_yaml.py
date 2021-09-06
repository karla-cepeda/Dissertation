# -*- coding: utf-8 -*-
"""
@author: Karla Aniela Cepeda Zapata
@studnetID: d00242569
@institute: Dundalk Institute of Technology
@supervisor: Rajesh Jaswal

Contains methods to access to yaml files located in code/layer_configurations. 
Yaml files can be seen like dictionary structures in Python, therefore it was easy to 
 use this type of file in the project.

"""
import yaml
import re

class my_yaml(object):
    """
    Parent class. 
    Children classes below.
    
    """
    def __init__(self):
        """
        Constructor.
        Set by deafult were is all yaml files.
        """
        self._path = 'layer_configurations/'
        self._extention = '.yaml'
        
    def get_value(self, filename, rootname, keyname): 
        """
        Generic method to access to data in a yaml file.

        Parameters
        ----------
        filename : string
            DESCRIPTION. Name of the file yaml
        rootname : string
            DESCRIPTION. Name of the section in the file yaml to be accessed
        keyname : string
            DESCRIPTION. Name of the data to be accessed

        Returns
        -------
        value : string

        """
        data = self.get_data(filename, rootname)
        value = data[keyname]
        del data
        return value
        
    def get_data(self, filename, rootname):
        """
        Generic method to acces to data in a yaml file.

        Parameters
        ----------
        filename : string
            DESCRIPTION. Name of the file yaml
        rootname : string
            DESCRIPTION. Name of the section in the file yaml to be accessed

        Returns
        -------
        List of dictionary
            DESCRIPTION. Data from yaml, returned as a dictionary object.

        """
        pattern = re.compile(r'(\s|^)({0})$'.format(self._extention), flags=re.IGNORECASE)
        if pattern.search(filename):
            filename = re.sub(pattern, '', filename)
        with open(self._path + filename +  self._extention) as file:
            data = yaml.safe_load(file)
            
        return data[rootname]
    
class my_yaml_tweet(my_yaml):
    def __init__(self):
        """
        Constructor.
        Return information related to tweets.
        
        """
        super().__init__()
        self._filename = "myTweet"
        
    def get_keywords(self):
        """
        Return all keywords used to build the querys for the Twitter API calls.
        
        """
        return super().get_data(self._filename, "keywords")
    
    def get_bacthes(self):
        """
        Return configuration to build the queries to be send to the endpoint.
        
        """
        return super().get_data(self._filename, "config_batches")
    
    def get_keywords_covid_vaccine(self):
        """
        Return a list of keywords used on the batches.
        
        """
        data = self.get_keywords()        
        keywords = list()
        keywords.extend(data['vaccine'])
        keywords.extend(data['covid'])
        keywords.extend(data['place'])
        keywords = [k.replace("#", "").replace("place:", "") for k in keywords]
        keywords = set(keywords)
        
        return keywords
    
    def get_keywords_covid_vaccine_pharma(self):
        """
        Return a list of vaccine keywords used on the batches.
        
        """
        data = self.get_keywords()        
        keywords = list()
        keywords.extend(data['cvaccine'])
        keywords = set(keywords)
        
        return keywords
    
    def get_username_covid_vaccine(self):
        """
        Return a list of users used on the batches.
        
        """
        data = self.get_keywords()        
        usernames = dict()
        usernames['media'] = data['media']
        usernames['political_parties'] = data['political_parties']
        usernames['gov_public_figures'] = data['gov_public_figures']
        usernames['gov_departments'] = data['gov_departments']
        usernames['gov_health_departments'] = data['gov_health_departments']
        usernames['health_public_figures'] = data['health_public_figures']

        return usernames
    
    def get_repositories(self):
        """
        Return default repository to save json response form twitter api.
        
        """
        return super().get_data(self._filename, "repositories")
        
    def get_default_config(self):
        """
        Return default configuration for the collection process.
        
        """
        return super().get_data(self._filename, "collection_config")
        
class my_yaml_config(my_yaml):
    def __init__(self):
        """
        Constructor.
        Return information related to the database such as password and username.
        
        """
        super().__init__()
        self._filename = "config"
    
    def get_mysql_conn(self):
        # Local database username and password.
        return super().get_data(self._filename, "mysql_conn")

    def get_azure_conn(self):
        # Azure credentials.
        return super().get_data(self._filename, "azure_conn")

    def get_mysql_conn_hostgator(self):
        # Remote database username and password.
        return super().get_data(self._filename, "mysql_conn_hostgator")
    
class my_yaml_mydb(my_yaml):
    def __init__(self):
        """
        Constructor.
        list of all stored procedures used in the local and remote databases.
        
        """
        super().__init__()
        self._filename = "mydb"
        
    def get_stored_procedure_names_twitter(self):
        # Local database
        return super().get_value(self._filename, "stored_procedures", "twitter")
    
    def get_stored_procedure_names_dcovid(self):
        # Local database
        return super().get_value(self._filename, "stored_procedures", "dcovid")
        
    def get_stored_procedure_names_sentimentanalysis(self):
        # Remote database
        return super().get_value(self._filename, "stored_procedures_hostgator", "sentimentanalysis")