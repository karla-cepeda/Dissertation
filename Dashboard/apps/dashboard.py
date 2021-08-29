
#import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta

import plotly.express as px
import plotly.graph_objects as go
#import geopandas as gpd

import pandas as pd
from app import app
import numpy as np

from layer_data_access import tweet_data, date_data

# Global values
#colors = ['#636EFA','#EF553B','#00CC96', '#AB63FA', '#FFA15A', '#1c1cbd']
colors = px.colors.qualitative.Plotly
image_filename = 'assets/green_arrow_long.svg'

#encoded_image = base64.b64encode(open(image_filename, 'rb').read()).decode() 

now = (datetime.datetime.now() - timedelta(days=1)).date()

datestrformat = lambda d: d.strftime("%b\n%y")
dateformat = lambda d: d.strftime("%Y-%m-%d")
date_list = pd.date_range(start='2020-01-01', end=now, freq='MS').tolist()
dictlist = dict()

for i in range(len(date_list)):
    dictlist[i] = datestrformat(date_list[i])

min_date = min(range(len(date_list)))
max_date = max(range(len(date_list)))
slidertool = dcc.RangeSlider(
                    id='sliderid',
                    min=min_date,
                    max=max_date,
                    value=[min_date, max_date],
                    step=1,
                    marks=dictlist,
                    allowCross=False,
                )  

def show_tweets_sentiment(tweets_time_df, tweets_time_neu_df, tweets_time_pos_df, tweets_time_neg_df, scale = 'Daily', showrangevisible = False):
    if scale == 'Daily':
        max_display = tweets_time_df.created_at.max()
        min_display = tweets_time_df.created_at.max() - relativedelta(months=1)
    
    else:
        max_display = tweets_time_df.created_at.max()
        min_display = (tweets_time_df.created_at.max() - relativedelta(months=12))

    layout = go.Layout(
        dragmode='pan',
        xaxis=dict(
            range=[min_display, max_display]
        )
    )
    
    fig = go.Figure(layout = layout)
    fig.add_trace(go.Scatter(x=tweets_time_neu_df.created_at, y=tweets_time_neu_df.tweet_id,
                        mode='lines', 
                        name='Neutral',
                        line={'color':'#E1C027'}))
    fig.add_trace(go.Scatter(x=tweets_time_pos_df.created_at, y=tweets_time_pos_df.tweet_id,
                        mode='lines',
                        name='Positive',
                        line={'color':'#0CCE49'}))
    fig.add_trace(go.Scatter(x=tweets_time_neg_df.created_at, y=tweets_time_neg_df.tweet_id,
                        mode='lines',
                        name='Negative',
                        line={'color':'#CE1B28'}))
    
    fig.update_xaxes(showticklabels = True,
                     tickformat = '%B<br>%Y',
                     )
    
    fig.update_layout(
        template = 'plotly_white',
        hovermode="x unified",
        height=500,
        autosize=True,
        margin=dict(
            l=10,
            r=10,
            b=0,
            t=0,
            pad=0
        ),
        title=None,
        legend={
                'orientation':"h",
                'yanchor':"bottom",
                'y': 1.02,
                'xanchor':"right",
                'x':1},
        xaxis_title="",
        yaxis_title="Tweets",)

    fig.update_xaxes(rangeslider_visible = showrangevisible)
    return fig

def get_monthly_numbers(df):
    df2 = df[['created_at','tweet_id']].copy()
    df2.created_at = pd.to_datetime(df2.created_at)
    df2 = df2.set_index('created_at').resample('M').sum()
    df2.reset_index(inplace = True)
    return df2

def show_tweets_pie(df):
    fig = px.pie(df, values='tweet_id', names='label')

    fig.update_traces(textinfo='label+percent',
                      textfont_size=15,
                      marker={'colors':['#CE1B28', '#E1C027', '#0CCE49']},
                      hovertemplate = None,
                      hoverinfo='skip',
                      showlegend = False,   
                    )
    fig.update_layout(template = 'plotly_white',
                      autosize=True,
                      height=200,
                      margin=dict(
                        l=0,
                        r=0,
                        b=0,
                        t=0,
                        pad=0
                      ),
                      title=None,
                      )

    return fig

da = tweet_data.tweet_data_remote()
tweets_df = da.get_tweets()
dates_df = da.get_dates()
date_reference_df = da.get_date_reference()
del da

# Convert datetime into date
tweets_df.created_at = tweets_df.created_at.dt.date
tweets_time_df = tweets_df[['created_at', 'label', 'tweet_id']].groupby(['created_at', 'label']).count().reset_index()

# Get positive, negative and neutral segmentation
# Monthly
tweets_time_df2 = get_monthly_numbers(tweets_time_df)
tweets_time_pos_df = get_monthly_numbers(tweets_time_df[tweets_time_df.label == 'positive'].copy())
tweets_time_neg_df = get_monthly_numbers(tweets_time_df[tweets_time_df.label == 'negative'].copy())
tweets_time_neu_df = get_monthly_numbers(tweets_time_df[tweets_time_df.label == 'neutral'].copy())
fig = show_tweets_sentiment(tweets_time_df2, tweets_time_neu_df, tweets_time_pos_df, tweets_time_neg_df, "Monthly")

tweets_time_df3 = tweets_df[['label', 'tweet_id']].groupby('label').count().reset_index()
fig2 = show_tweets_pie(tweets_time_df3)

max_date = tweets_df.created_at.max()
min_date = tweets_df.created_at.min()

cond = tweets_df.label.isin(['negative', 'positive'])
cond2 = tweets_df.created_at == max_date

# Global sentiment
tweet_df1 = tweets_df[cond][['label','tweet_id']].groupby('label').count()
max_label1 = tweet_df1.idxmax().values[0]
if max_label1 == 'negative':
    color1 = 'danger'
else:
    color1 = 'success'

# Last sentiment
tweet_df2 = tweets_df[cond & cond2][['label','tweet_id']].groupby('label').count()
max_label2 = tweet_df1.idxmax().values[0]
if max_label2 == 'negative':
    color2 = 'danger'
else:
    color2 = 'success'

summ = [
         dbc.Row(dbc.Col(
            html.Tbody(
                html.Tr(
                    html.Td([
                             dbc.Alert(max_label1, color=color1, style={'font-size': '20px !important', 'margin':'0 !important'}), 
                             html.P("Global sentiment", className="mb-0"),
                             html.P(min_date.strftime('%Y-%m-%d') + " to " + max_date.strftime('%Y-%m-%d'), className="mb-0, addmargin")
                             ], style={'width':'100%', 'border': 'none', 'font-size':'10px', 'text-align':'center'}
                    ), style={'width':'100%', 'border': 'none'}
                ),
            ), className = 'col-auto'
        ), className = 'justify-content-center'),
        dbc.Row(dbc.Col(
            html.Tbody(
                html.Tr(
                     html.Td([
                              dbc.Alert(max_label2, color=color2, style={'font-size': '20px !important', 'margin':'0 !important'}), 
                              html.P("Last sentiment", className="mb-0"),
                              html.P(max_date.strftime('%Y-%m-%d'), className="mb-0, addmargin")
                             ], style={'width':'100%', 'border': 'none', 'font-size':'10px', 'text-align':'center'}
                    ), style={'width':'100%', 'border': 'none'}
                )
            ), className = 'col-auto'
        ), className = 'justify-content-center'),
        dbc.Row(dbc.Col(
            html.Tbody(
                html.Tr(
                    html.Td([
                             html.Img(src="/assets/logo-rond-twitter.png", height="60px", style={'vertical-align': 'middle'}),
                             html.Span("{:,}".format(len(tweets_df)), className="mb-0", style={" margin-left":'20px !important', 'font-size':'20px !important'}),
                             html.P("Tweets", className="mb-0", style={'border': 'none', 'font-size':'10px', 'text-align':'center'}),
                            ], style={'width':'100%', 'border': 'none'}
                    ), style={'width':'100%', 'border': 'none'}
                )
            ), className = 'col-auto'
        ), className = 'justify-content-center'),
        dbc.Row(dbc.Col([            
                html.H4('Distribution', style={'textAlign': 'center', }),
                dcc.Graph(id='overTime', figure = fig2)                    
                ]), 
        )
]

filters = html.Div(['filters'])

layout = html.Div(children=[   
            
                dbc.Row(children=[
                        html.Div(children=[html.Button(id='openid',
                                                   children=[html.Img(src='assets/info-circle-fill.svg', style={'width':'30px'} )],
                                                   className='position-fixed', style={'right':'10px', 'z-index':'1000000', 'border': 'none', 'width': 'auto', 'margin': '0', 'padding': '0'}
                                                   ),]
                             ),
                        
                        dbc.Tooltip(children=["Welcome to the dashboard!"
                                              " This is just a summary about location and status of bikes."
                                              " For details, access to Map, Bikes and Rentals section."],
                                    target="openid",
                                    style={'font-size':'12px'}
                                    ),
                        
                        dbc.Col(children=[html.H1("Dashboard", 
                                                  style={'textAlign': 'center', 'color': 'black', 'margin-bottom': '0px'}, 
                                                  className='display-4'),
                                          html.H4("COVID-19 vaccine sentiment in Ireland", 
                                                  style={'textAlign': 'center', 'color':'gray', 'margin-top': '0px', 'font-size':'20px'}, 
                                                  className='display-4')], 
                                className="col-sm-12", md=3
                                ),         
                        ], justify="center"),
                    
                #dbc.Row(summ, id='summary', style={'margin-top':'30px'}),
                
                dbc.Row([
                            #Header span the whole row
                            #className: Often used with CSS to style elements with common properties.
                            html.P("Filter by hour:"),
                            dbc.Col(slidertool, style={'padding-top':'10px'})
                            ], style={'margin-top':'10px', 'padding-left':'30px'}),
                
                dbc.Row([
                            dbc.Col([
                                      html.H4('Sentiment over time', style={'textAlign': 'center', }),
                                      dcc.Graph(id='overTime', figure = fig)
                                    ], className="col-9"),
                            dbc.Col(summ,
                                    className="col-3")
                            
                        ], justify="center"),

])
