The application tier, which may also be referred to as the logic tier, is written in a programming language such as Java and contains the business logic that supports the application�s core functions. The underlying application tier can either be hosted on distributed servers in the cloud or on a dedicated in-house server, depending on how much processing power the application requires.

Layer_data_access was designed to leave the connection to database open until the sub-process (could be preprocessing, or saving json files collected from Twitter API) ends. This is possible to change by accessing to this layer and change the code.

Layer_logic is where the process happens.

Code in extras folder is not used during the collection and preprocess of tweets and dates. This folder contains support code for other types of processes such as extraction of slang dictionary and emoticon and emoji process to create dictionaries.