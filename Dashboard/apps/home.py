import dash
import dash_html_components as html
import dash_bootstrap_components as dbc

from app import app

layout = html.Div([
    dbc.Container([
        html.Div([
            
            html.H1("Welcome to\nSentiment Analysis on COVID-19 vaccines in Ireland", className="text-center mb-5 mt-5"),
            html.H3("Dissertation project", className="lead"),
            html.Hr(),
            html.P("This APP shows real-time data extracted from the Twitter API. This is a Dissertation project delivered on 10th Sep 2021.", className='lead'),
            dbc.Button("Get started!", color="danger", href='/dashboard', className="mr-1"),
            
        ],className='jumbotron'),

    
    
        html.Div([
            html.H3("Brief Description of data"),
            html.P("The data consists of tweets collected from Twitter API."),
            html.H3("Purpose of the application"),
            html.P("This app has been designed to show the sentiment in Ireland towards COVID-19 vaccines. This APP is aimed at the public, thus the dashboard has been designed as simple as possible for better understanding."),
            ], style={'text-align':'center'}),
    
        html.Div([
            
                 html.H3("Access to original data and code"),
                 dbc.Row([
                     
                     dbc.Col([
                         
                         dbc.Card(
                             [
                                 dbc.CardImg(src="../assets/project_image.png", top=True),
                                 dbc.CardBody([
                
                                         html.H4("As data was extracted from Twitter API, you have you _ to their _."),
                                         dbc.Button("Twitter data", 
                                                    color="danger", 
                                                    href="https://data.smartdublin.ie/dataset/moby-bikes", 
                                                    className="mr-1")
                     
                                    ])
                         
                            ])
                     
                     ],),
                     
                 
                     dbc.Col([
                         dbc.Card(
                                 [
                                     dbc.CardImg(src="../assets/github.png", top=True),
                                     dbc.CardBody(
                                        [
                                            
                                                 html.H4("Access the code used\n\nto build this dashboard and collected data from Twitter API. If needed, request access to d00242569."),
                                                 dbc.Button("GitHub", 
                                                            color="danger", 
                                                            href="https://github.com/karla-cepeda/Workspace/tree/master/Data%20Visualization/Assignment%202", 
                                                            className="mr-1"),
                                                 
                                                 ],),
                             
                                 ])
                                     
                         ])
                     
                
                ],),
        ]),
        
        
        html.Div([
            html.H3("Licence Statement"),
            html.P(" "),
            html.P(" ")
            
            ], style={'text-align':'center', 'margin-top':'50px'}),
        
    ], className='container-narrow text-center'),
    
])
    
