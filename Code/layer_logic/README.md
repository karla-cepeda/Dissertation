This layer contains all the logic to carry out different processes such as cleaning, collection, migration of the data to a remote database, and so on.

-**date_logic.py**. This python scritp contains the process to scrap the website Wikipedia that contains important dates and events related to covid in Ireland.
-**tweet_logic.py**. This module is used to carry out some processes on tweets. In general: cleaning, normalization, collection, labelling, and getting list of keywords.
-**migration_logic.py**. Contains the process to migrate specific tweet data into a remote database that will be used for a dashboard to show off the results.