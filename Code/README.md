# Collection and preprocess of tweets
This folder contains all the code used for collection, cleaning and normalization of tweets. Additionally, insertion and upgrade process to database are included.

To organize the code, a three-layer architecture has been used. This is a well-established software application architecture that organizes applications into three logical and physical computing tiers: 
- **Presentation layer**. This is the user interface. In this project, for collection and preprocess it is used the console to show the process. The files that are used as presentation are: **inicial_collection.py** and **daily_collection.py**.
- **Logic layer**.  This is were data is processed. This is were the process happens. It was designed to leave the connection to database open until the sub-process (could be preprocessing, or saving json files collected from Twitter API) ends. This is possible to change by accessing to this layer and change the code. In this folder, **layer_logic** contains all the code related to this layer.
- **Data access layer**. This is were data is stored and managed. In this folder, **layer_data_access** contains all the code related to this layer.

Other layers:
- **Class layer**. Includes different classes and methods.
- **Configureation layer**. Includes constant values and credentials to Twitter API and database. These last files were not included, but others that include constants.

Other folders:
- **Extra**. This folder is not used during the collection and preprocess of tweets and dates. This folder contains support code for other types of processes such as extraction of slang dictionary and emoticon and emoji process to create dictionaries.

This architecture was chosen to organize well the code.

# Explorationa and Modelling
Files that are not using this architecture, but access the data through the layer data_access, are:
- analysis_process.ipybn ==> contains code used to explore the irish tweets already labelled.
- exploration_process.ipybn ==> contains code to create graphs and visualizations to explore irish tweets.
- exploration_labelling_process.ipybn ==> contains code to create graphs and visualizations to explore data.
- modelling_process.ipybn ==> contains the process done to create model.

# How to use this code
*No credentials from databases and Twitter API provided. Too get access to Twitter API, you must apply to get access in https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api*
- Download the folder to the machine. 
- Verify that all required libraries are installed into the machine, listing below.
- Run scrips to create database, see below.

## Requirements
Libraries:
- pandas
- mysql
- yaml
- re
- datetime
- sys
- requests
- urllib
- time
- joblib
- string
- spacy
- preprocessor
- ekphrasis
- nltk
- bs4
- html
- text_to_num
- enchant
- json
- os
- sklearn
- plotly
- matplotlib
- seaborn

## Database
Set up database running sql scripts located in https://github.com/karla-cepeda/Dissertation/tree/main/SQL/local.
- **twitter.sql** contains the structure of the database.
- **stored_procedures.sql* contains the sp used for the dashborad and for daily collection of dates.
