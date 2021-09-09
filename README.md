# Sentiment Analysis on COVID-19 Vaccines in Ireland
### Dissertation 2021

Here Supporting Artifacts including code, demonstration screencast link, source code, designs, output from test runs, test reports and other files.

## Introduction
This project aims to identify the general sentiment on the Covid-19 vaccines over a specifictime to understand the evolution of this in the Republic of Ireland. A Machine Learning algorithm will be trained and tested to classify tweets into positive, negative, or neutral opinions.Knowledge from Programming, Data Architecture, Ethics, Statistics, and Machine Learningmodules from MSc in Data Analytics will be used throughout the project.

The relevance of the project in the Data Science field relies on the performance of SentimentAnalysis on data collected from Twitter to understand the opinion on the Covid-19 vaccinesin the Republic of Ireland, using Cross-Industry Standard Process for Data Mining (CRISP-DM) life-cycle methodology to implement this project.  Additionally, this topic was chosen (i.e., Covid-19 and vaccines) due to its relevance since this is an ongoing worldwide eventthat concerns not just researchers but the public as well.

## Folders
- **Code**. Contains all code for collection and preprocess of tweets. Additionally, insertion on database and migration process is included. Other Jupyter notebooks are included for exploration of the dataset, modelling and analysis of the data.
- **SQL**. Contains sql files with the structure of the database and store procedures.
- **Model**. Contains the model built using the library sklearn.
- **Dashboard**. Contains the code for the dashboard built using dash and plotly.
- **Dashboard_BI**. This folder contains a Power BI file. This is the first dashboard coded, however not used as there is an error on the python blockes added after deployment.
- -**Dataset_final**. Contains the Irish and global dataset of tweets. These datasets just contains the following columns: created_at, tweet_id, conversation_id and label.

## Ethical considerations
The tool used to collect all public tweets from the social media Twitter was the developerproduct Twitter API. After sending the application and then approved by the Twitter Dev Team,  automatically the applicant is accepting the Developer Agreement,  an agreementmade between the developer/researcher and Twitter to conduct the access and use of the data, and "to keep Twitter’s public conversations safe and healthy".  Across all of the products, Twitter maintains strict policies and processes to assess how developers are usingTwitter data, and restrict improper use of this data.  When these policies are violated, ac-tions are appropriately taken, which can include suspension and termination of access toTwitter’s API and data products.  Therefore, the main ethical considerations for this projectare based on theDeveloper Agreementfrom Twitter, which are:
- Privacy
- Security
- Anonymization and/or Potential for Identification of Individuals
- Property and Ownership of Data
