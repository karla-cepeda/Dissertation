import dash
import dash_html_components as html
import dash_bootstrap_components as dbc

from app import app

layout = html.Div([
    dbc.Container([
        html.Div([
            
            html.H3("Welcome to"),
            html.H1("Sentiment Analysis on COVID-19 vaccines in Ireland", className="text-center mb-5 mt-5"),
            html.H3("Dissertation project - MSc in Data Analytics", className="lead"),
            html.H3("Karla Cepeda - D00242569", className="lead"),
            html.H3("Dundalk Institute of Technology (DkIT)", className="lead"),
            html.Hr(),
                        
            html.P("This APP shows data extracted from the Twitter API and labeled using a Machine Learning algorithm."),
            html.P("This project aims to identify the general sentiment on the Covid-19 vaccines in Ireland, collecting tweets from1 January 2020to13 August 2021. A Machine Learning (ML) algorithm was trained and tested to classify tweets into positive, negative, or neutral opinions. Knowledge from Programming, Data Architecture, Ethics, Statistics, and Machine Learning modules from MSc in Data Analytics was used throughout the project. Table 1.1 summarizes the scope1of the research and the goals."),            
            html.P("The relevance of the project in the Data Science field relies on the performance of Sentiment Analysis on data collected from Twitter to understand the opinion on the Covid-19vaccines in the Republic of Ireland, using the Cross-Industry Standard Process for DataMining (CRISP-DM) life-cycle methodology to implement this project. Additionally, this topic was chosen (i.e., Covid-19 and vaccines) due to its relevance since this is an ongoing worldwide event that concerns researchers and the public."),            
            html.P("This project was delivered on the 14th of Sep, 2021."),

            dbc.Button("Get started!", color="danger", href='/dashboard', className="mr-1"),
            
        ],className='jumbotron'),

    
    
        html.Div([
            html.H3("Brief Description of data"),
            html.P("The data consists of tweets collected from Twitter API. The initial collection was done from 1 January 2020 to 13 August 2021, and a daily collector was coded to gather daily tweets at 11:55 p.m"),
            html.H3("Purpose of the application"),
            html.P("This app has been designed to show the sentiment in Ireland towards COVID-19 vaccines. This APP is aimed at the public. Thus, the dashboard has been designed as simply as possible for better understanding."),
            ], style={'text-align':'center'}),
    
        html.Div([
            
                 html.H3("Access to original data and code"),
                 dbc.Row([
                     
                     dbc.Col([
                         
                         dbc.Card(
                             [
                                 dbc.CardImg(src="../assets/project_image.png", top=True),
                                 dbc.CardBody([
                
                                         html.H4("Two datasets are available: the global tweets dataset and the Irish tweets dataset. CSV file format. Important to see ethical considerations below."),
                                         dbc.Button("Twitter data", 
                                                    color="danger", 
                                                    href="https://github.com/karla-cepeda/Dissertation/tree/main/dataset_final", 
                                                    className="mr-1")
                     
                                    ])
                         
                            ])
                     
                     ],),
                     
                 
                     dbc.Col([
                         dbc.Card(
                                 [
                                     dbc.CardImg(src="../assets/github.png", top=True, style={'height': '276px'}),
                                     dbc.CardBody(
                                        [
                                            
                                                 html.H4("Access the code used\n\nto build this dashboard and collected data from Twitter API. If needed, request access to d00242569."),
                                                 dbc.Button("GitHub", 
                                                            color="danger", 
                                                            href="https://github.com/karla-cepeda/Dissertation/tree/main/Code", 
                                                            className="mr-1"),
                                                 
                                                 ],),
                             
                                 ])
                                     
                         ])
                     
                
                ],),
        ]),
        
        
        html.Div([
            html.H3("Licence Statement"),
            html.P("Note that by downloading the Twitter data you agree to abide by the Twitter terms of service (https://twitter.com/tos), and in particular you agree not to redistribute the data and to delete tweets that are marked deleted in the future. You MUST NOT re-distribute the tweets, the annotations or the corpus obtained, as this violates the Twitter Terms of Use."),
            
            ], style={'text-align':'center', 'margin-top':'50px'}),
        
    ], className='container-narrow text-center'),
    
])
    
