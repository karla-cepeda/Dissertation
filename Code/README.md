# Collection and preprocess of tweets
This folder contains all the code used for collection, cleaning and normalization of tweets. Additionally, insertion and upgrade process to database are included.

To organize the code, a three-layer architecture has been used. This is a well-established software application architecture that organizes applications into three logical and physical computing tiers: 
- **Presentation layer**. This is the user interface. In this project, for collection and preprocess it is used the console to show the process. The files that are used as presentation are: **inicial_collection.py** and **daily_collection.py**.
- **Logic layer**.  This is were data is processed. This is were the process happens. It was designed to leave the connection to database open until the sub-process (could be preprocessing, or saving json files collected from Twitter API) ends. This is possible to change by accessing to this layer and change the code. In this folder, **layer_logic** contains all the code related to this layer.
- **Data access layer**. This is were data is stored and managed. In this folder, **layer_data_access** contains all the code related to this layer.

Other layers:
- **Class layer**. Includes different classes and methods.

Other folders:
- **Extra**. This folder is not used during the collection and preprocess of tweets and dates. This folder contains support code for other types of processes such as extraction of slang dictionary and emoticon and emoji process to create dictionaries.

This architecture was chosen to organize well the code.

# Explorationa and Modelling

Files that are not using this architecture, but access the data through the layer data_access, are:
- analysis_process.ipybn
- exploration_process.ipybn
- exploration_labelling_process.ipybn
- modelling_process.ipybn
