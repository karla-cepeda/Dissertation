# -*- coding: utf-8 -*-
"""
@author: Karla Aniela Cepeda Zapata
@studnetID: d00242569
@institute: Dundalk Institute of Technology
@supervisor: Rajesh Jaswal


DESCRIPTION.
This class contains all methods needed to connect and close connection to database.
Also included functions to work with stored procedures.

It also includes functinalitly to connect to local or remote database, depending on the process.

"""
import pandas as pd
import mysql.connector
from layer_classes import my_yaml

class myDB(object):       
    def __init__(self, database, local = True):
        """
        Class constructure

        Parameters
        ----------
        database : Dictionary
            DESCRIPTION. Information of database, including password and username.
        local : Bool, optional
            DESCRIPTION. Flag that indicates if database is local or remote. The default is True.

        Returns
        -------
        None.

        """
        myy = my_yaml.my_yaml_config()
        if local:
            config = myy.get_mysql_conn()
        else:
            config = myy.get_mysql_conn_hostgator()

        config['database'] = database
        self.__db_cnx = mysql.connector.connect(**config)
        del myy, config

    def __enter__(self):
        return self
    
    def __del__(self):
        """
        Close connection to database.

        Returns
        -------
        None.

        """
        self.__close_cnx()
        
    def __exit__(self, exc_type, exc_value, traceback):
        self.__close_cnx()
        
    def __close_cnx(self):
        """
        If connection is open, this is closed.

        Returns
        -------
        None.

        """
        try:
            if self.is_connected():
                self.__db_cnx.close()
            del self.__db_cnx
        except:
            pass
    
    def call_sp(self, stored_name, args=None):    
        """
        This is used to call a stored procedure. This could be used to look up for information,
        insert information, upgrade specific data, and so on.

        Parameters
        ----------
        stored_name : string
            DESCRIPTION. Name of the stored procedure
        args : List, optional
            DESCRIPTION. Arguments that will be send to the stored procedure. If None, no parameters
            will be sent. The default is None.

        Returns
        -------
        None.

        """
        
        try:
            db_cur = self.__db_cnx.cursor()  
            if args:
                db_cur.callproc(stored_name, args)
            else:
                db_cur.callproc(stored_name)
            self._results = db_cur.stored_results()
            db_cur.close()
            self.__db_cnx.commit()
            
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            self.__close_cnx()
            raise
        
    def get_results(self): 
        """
        Return the results in a list of tuples.

        Returns
        -------
        info_db : List of tuples
            DESCRIPTION. Result of the stored procedure.

        """
        
        info_db = None
        if self._results:            
            for result in self._results:
                info_db = result.fetchall()
                
        return info_db
    
    def get_results_dataframe(self):
        """
        Return the results in a dataframe format

        Returns
        -------
        df : Dataframe
            DESCRIPTION. Result of the stored procedure.

        """
        
        df = None
        if self._results: 
            info_db = None
            desc = None
            cols = list()
            
            for result in self._results:
                desc = result.description
                info_db = result.fetchall()
            
            if info_db and desc:
                for i in desc:
                    cols.append(i[0])
            
                df = pd.DataFrame(info_db, columns=cols)
        
        return df
            
    def is_connected(self):
        """
        Return a value if connection is still open

        Returns
        -------
        Bool
            DESCRIPTION. Check if connection is open

        """
        return self.__db_cnx.is_connected()
