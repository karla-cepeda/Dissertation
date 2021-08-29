# -*- coding: utf-8 -*-
"""
@author: Karla Aniela Cepeda Zapata
@studnetID: d00242569
@institute: Dundalk Institute of Technology
@supervisor: Rajesh Jaswal

"""
import pandas as pd
import mysql.connector
from layer_classes import my_yaml

class myDB(object):    
    def __init__(self, database, local = True):
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
        self.__close_cnx()
        
    def __exit__(self, exc_type, exc_value, traceback):
        self.__close_cnx()
        
    def __close_cnx(self):
        try:
            if self.is_connected():
                self.__db_cnx.close()
            del self.__db_cnx
        except:
            pass
    
    def call_sp(self, stored_name, args=None):      
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
        info_db = None
        if self._results:            
            for result in self._results:
                info_db = result.fetchall()
                
        return info_db
    
    def get_results_dataframe(self):
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
        return self.__db_cnx.is_connected()
