# Collection and preprocess of tweets
This folder contains all the code used for the collection, cleaning, and normalization of tweets. Additionally, insertion and upgrade processes to the database are included.

A three-layer architecture was used to organize the code. This architecture is a well-established software application that organizes applications into three logical and physical computing tiers: 
- **Presentation layer**. This is the user interface. In this project, for collection and preprocess, the console is used to show the process. The files that are used as presentation are: **inicial_collection.py** and **daily_collection.py**.
- **Logic layer**.  This is where Data is processed. This is where the process happens. It was designed to leave the connection to the database open until the sub-process (preprocessing or saving JSON files collected from Twitter API) ends. This is possible to change by accessing this layer and change the code. In this folder, **layer_logic** contains all the code related to this layer.
- ** Data access layer**. This is where Data is stored and managed. In this folder, **layer_data_access** contains all the code related to this layer.

Other layers:
- **Class layer**. It includes different classes and methods.
- **Configuration layer**. It includes constant values and credentials to Twitter API and database. These last files were not included, but others include constants.

Other folders:
- **Extra**. This folder is not used during the collection and preprocessing of tweets and dates. This folder contains support code for other types of processes such as extraction of slang dictionaries and emoticon and emoji processes to create dictionaries.

This architecture was chosen to organize the code well.

# Explorationa and Modelling
Files that are not using this architecture, but access the data through the layer data_access, are:
- analysis_process.ipybn ==> contains code used to explore the Irish tweets already labeled.
- exploration_process.ipybn ==> contains code to create graphs and visualizations to explore Irish tweets.
- exploration_labelling_process.ipybn ==> contains code to create graphs and visualizations to explore data.
- modelling_process.ipybn ==> contains the process done to create model.

# How to use this code
*No credentials from databases and Twitter API provided. To get access to Twitter API, you must apply to get access in https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api*
- Download the folder to the machine. 
- Verify that all required libraries are installed into the machine, listing below.
- Run scrips to create the database. See below.

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
Set up database running SQL scripts located in https://github.com/karla-cepeda/Dissertation/tree/main/SQL/local.
- **twitter.sql** contains the structure of the database.
- **stored_procedures.sql* contains the sp used for the dashboard and the daily collection of dates.
