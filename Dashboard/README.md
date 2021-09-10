# How to use this code
* No credentials from remote database provided *
- Download the folder to the machine. 
- Verify that all required libraries are installed into the machine, listing below.
- Run scrips to create database, see below.

## Requirements
Libraries:
- dash
- dash.dependencies
- dash_core_components
- dash_html_components
- dash_bootstrap_components
- pandas
- mysql.connector
- yaml
- re
- datetime

## Database
Set up database running sql scripts located in https://github.com/karla-cepeda/Dissertation/tree/main/SQL/remote.
- **twitter.sql** contains the structure of the database.
- **stored_procedures.sql* contains the sp used for the dashborad and for daily collection of dates.
