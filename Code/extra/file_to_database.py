# -*- coding: utf-8 -*-
"""
@author: Karla Aniela Cepeda Zapata
@studnetID: d00242569
@institute: Dundalk Institute of Technology
@supervisor: Rajesh Jaswal

"""

import os
os.chdir("../") # move to folder where layer_classes module is located.

from datetime import datetime
import json
from layer_classes import my_database

__json_files = []

def __get_file(directory_name):
    global __json_files
    entries = os.listdir(directory_name)
    for entry in entries:
        path = os.path.join(directory_name, entry)
        if os.path.isfile(path):
            if entry.endswith('.json'):
                total_tweets = 0
                with open(path) as file:
                    data = json.load(file)  
                    if "meta" in data.keys():
                        total_tweets = data['meta']['result_count']
                __json_files.append({'path':directory_name, 'filename':entry.replace('.json', ''), 'total_tweets':total_tweets, 'created_at':datetime.fromtimestamp(os.path.getctime(path))})
        if os.path.isdir(path):
            if entry not in __json_files:
                __get_file(path)
                
                
__get_file("..\\dataset")
__db = my_database.myDB('twitter')

try:
    for f in __json_files:
        args = (f['path'], f['filename'], '.json', f['total_tweets'], f['created_at'].strftime("%Y-%m-%d %H:%M:%S"))
        __db.call_sp("insert_log_file", args)
        print(f['path'], f['filename'])
except:
    raise ValueError("Error while inserting information")
finally:
    del __db, __json_files