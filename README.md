# Sentiment Analysis on COVID-19 Vaccines in Ireland
### Dissertation 2021
These folders are the Supporting Artifacts from the final MSc in Data Analytics project, including code, demonstration screencast link, source code, designs, output from test runs, test reports, and other files.

## Introduction
This project aims to identify the general sentiment on the Covid-19 vaccines over a specific time to understand the evolution in the Republic of Ireland. A Machine Learning algorithm was trained and tested to classify tweets into positive, negative, or neutral opinions. Knowledge from Programming, Data Architecture, Ethics, Statistics, and Machine Learning modules from MSc in Data Analytics was used throughout the project.

The relevance of the project in the Data Science field relies on the performance of Sentiment Analysis on data collected from Twitter to understand the opinion on the Covid-19 vaccines in Ireland, using Cross Industry Standard Process for Data Mining (CRISP-DM) life-cycle methodology to implement this project.  Additionally, this topic was chosen (i.e., Covid-19 and vaccines) due to its relevance since this is an ongoing worldwide event that concerns not just researchers but also the public.

## Folders 
- **Code**. Contains all code for collection and preprocessing of tweets. Additionally, insertion on database and migration process is included. Other Jupyter notebooks are included for exploration of the dataset, modeling, and analysis of the data.
- **SQL**. It contains SQL files with the structure of the database and store procedures.
- **Model**. It contains the model built using the library sklearn.
- **Dashboard**. Contains the code for the dashboard built using dash and plotly.
- **Dashboard_BI**. This folder contains the first dashboard created with Microsoft Power BI. However, it was not used as the final dashboard since there was an error on the python blocks added after deployment.
- -**Dataset_final**. It contains the Irish and global dataset of tweets. These datasets contain the following columns: created_at, tweet_id, conversation_id, and label.

## Screencast
Screencast recorded to show the functionality and structure of the Python code designed for the final project of MSc in Data Analytics.
Available in: https://web.microsoftstream.com/video/ead11ffc-78ea-4394-97c3-db6ad07d9153.
*Please, see the description of the video before playing)*

## Dashboard
A dashboard deployed to display the results is available in the following link: https://sentimentanalysis-c19v-ie.herokuapp.com. 

## Ethical considerations
The tool used to collect all public tweets from social media Twitter was the developer product Twitter API. After sending the application and then being approved by the Twitter Dev Team,  automatically the applicant is accepting the Developer Agreement,  an agreement made between the developer/researcher and Twitter to conduct the access and use of the data, and "to keep Twitter’s public conversations safe and healthy." Across all of the products, Twitter maintains strict policies and processes to assess how developers are using Twitter data and restrict improper use of this data.  When these policies are violated, actions are appropriately taken, including suspension and termination of access to Twitter API and data products.  Therefore, the main ethical considerations for this project are based on the Developer Agreementfrom Twitter, which are:
- Privacy
- Security
- Anonymization and Potential for Identification of Individuals
- Property and Ownership of Data
