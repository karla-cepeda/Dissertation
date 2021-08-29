# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 15:04:56 2021

@author: acjimenez
"""
import os
os.chdir('../') # Move to root folder

import pandas as pd
import re
import requests
import json
from bs4 import BeautifulSoup
from ekphrasis.dicts.emoticons import emoticons
import emojis as emos

# -------------- SLANGS
abbr_dict={}

#Function to get the Slangs from https://www.noslang.com/dictionary/
def get_dictionary(alpha):
    global abbr_dict
    url = r'https://www.noslang.com/dictionary/'+alpha
    r = requests.get(url)
    html_doc = r.text
    soup = BeautifulSoup(html_doc,'html.parser')
    
    for i in soup.findAll('div',{'class':'dictionary-word'}): 
        abbr = i.find('abbr')['title']
        abbr_dict[i.find('span').text[:-2]] = abbr
            
link_dict=[]
#Generating a-z
for one in range(97,123):
    link_dict.append(chr(one))
link_dict.append("#")

#Creating Links for https://www.noslang.com/dictionary/a...https://www.noslang.com/dictionary/b....etc
for i in link_dict:
    get_dictionary(i)

# Finally writing into a json file
with open('layer_configurations/slang_acronyms.json','w') as file:
    jsonDict=json.dump(abbr_dict,file)
    

# --------------------------------- EMOTICONS
# Get emoticons (different to emojis)
emoticons_df = pd.read_excel("extras/dictionary_emoticons.xlsx", sheet_name=[0,1,2,3],  na_values=['NaN', ' NaN', 'NaN ', '', None])
my_emoticons = dict()        
for v in emoticons_df.values():
    for i in range(len(v)):
        e = v.loc[i].dropna()
        value = e[-1]
        lst = e.tolist()
        lst.remove(value)
        
        for l in lst:
            emotic = l.strip()
            if emotic not in my_emoticons.keys() and emotic not in emoticons.keys():
                my_emoticons[emotic] = "<" + value.lower().strip() + ">"

# Finally writing into a json file
with open('layer_configurations/emoticons.json','w') as file:
    jsonDict=json.dump(my_emoticons, file)
    
    
# ---------------------------- EMOJIS
emojis_df = pd.read_excel("extras/dictionary_emojis.xlsx", sheet_name=[0,1,2,3,4],  na_values=['NaN', ' NaN', 'NaN ', '', None])
my_emojis = dict()

for i in range(len(emojis_df)):
    emojis_df[i]['Emoji'] = emojis_df[i]['Emoji'].apply(lambda l: emos.get(l))
    
    for i2 in range(len(emojis_df[i])):
        emojis2 = emojis_df[i].iloc[i2,0]
        meaning2 = emojis_df[i].iloc[i2,1]
        for e in emojis2:
            for e2 in re.split(r'\.*', e):
                if e2 not in my_emojis.keys():
                    if emojis.count(e2) > 0:
                        my_emojis[e2] = meaning2

# Finally writing into a json file
with open('layer_configurations/emojis.json','w') as file:
    jsonDict=json.dump(my_emojis, file)
            
            
