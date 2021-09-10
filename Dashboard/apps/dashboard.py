
#import dash
import dash
import dash_table
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
import numpy as np
import re

from app import app

from layer_data_access import tweet_data, date_data
from layer_classes import my_yaml

# Global values
#colors = ['#636EFA','#EF553B','#00CC96', '#AB63FA', '#FFA15A', '#1c1cbd']
colors = px.colors.qualitative.Plotly
image_filename = 'assets/green_arrow_long.svg'

#encoded_image = base64.b64encode(open(image_filename, 'rb').read()).decode() 
# Global variables
my_color = ['rgba(225, 192, 39', 'rgba(206, 27, 40', 'rgba(12, 206, 73']

def get_distribution_labels(tweets_df, date_df, cond, rule = 'D'):
    
    if not cond is None:
        df = tweets_df[cond].copy()
    else:
        df = tweets_df.copy()

    df = df[['created_at', 'label', 'tweet_id']].groupby(['created_at', 'label']).count().reset_index().copy()
    tweets_time_pos_df = df[df.label == 'positive'][['created_at','tweet_id']].copy()
    tweets_time_neg_df = df[df.label == 'negative'][['created_at','tweet_id']].copy()
    tweets_time_neu_df = df[df.label == 'neutral'][['created_at','tweet_id']].copy()
    
    if rule == 'D':
        date_df2 = date_df.drop_duplicates(subset=['created_at'], keep='last').copy()
        date_df2['description'] = date_df2['description'].apply(split_text, n=50)
        date_df2.created_at = pd.to_datetime(date_df2.created_at).dt.date

        df2 = df[['created_at', 'tweet_id']].groupby('created_at').count().reset_index().copy()
        df2.created_at = pd.to_datetime(df2.created_at).dt.date

        tweets_time_df = pd.merge(df2, date_df2, on='created_at',how='left')
        tweets_time_df['description'] = tweets_time_df['description'].fillna("No found")

    else:
        df.created_at = pd.to_datetime(df.created_at)
        tweets_time_pos_df.created_at = pd.to_datetime(tweets_time_pos_df.created_at)
        tweets_time_neg_df.created_at = pd.to_datetime(tweets_time_neg_df.created_at)
        tweets_time_neu_df.created_at = pd.to_datetime(tweets_time_neu_df.created_at)

        tweets_time_df = df.set_index('created_at').resample(rule).sum()
        tweets_time_pos_df = tweets_time_pos_df.set_index('created_at').resample(rule).sum()
        tweets_time_neg_df = tweets_time_neg_df.set_index('created_at').resample(rule).sum()
        tweets_time_neu_df = tweets_time_neu_df.set_index('created_at').resample(rule).sum()

        tweets_time_df.reset_index(inplace = True)
        tweets_time_pos_df.reset_index(inplace = True)
        tweets_time_neg_df.reset_index(inplace = True)
        tweets_time_neu_df.reset_index(inplace = True)
    
    return tweets_time_df, tweets_time_pos_df, tweets_time_neg_df, tweets_time_neu_df


def show_tweets_sentiment(tweets_df, date_df, cond, title, rule = 'D'):    
    tweets_time_df, tweets_time_pos_df, tweets_time_neg_df, tweets_time_neu_df = get_distribution_labels(tweets_df, date_df, cond, rule)
    include_event = False
    showrange_visible = False
    
    if rule == 'D':
        max_display = tweets_time_df.created_at.max()
        min_display = tweets_time_df.created_at.max() - relativedelta(months=6)
        include_event = True
        showrange_visible = True

    else:
        max_display = tweets_time_df.created_at.max()
        min_display = tweets_time_df.created_at.min()

    layout = go.Layout(
        dragmode='pan',
        xaxis=dict(
            range=[min_display, max_display]
        )
    )
    
    fig = go.Figure(layout = layout)                     
    fig.add_trace(go.Scatter(x=tweets_time_pos_df.created_at, y=tweets_time_pos_df.tweet_id,
                        mode='lines',
                        name='Positive',
                        line={'color':my_color[2] + ',0.7)'}))
    fig.add_trace(go.Scatter(x=tweets_time_neg_df.created_at, y=tweets_time_neg_df.tweet_id,
                        mode="lines",
                        name='Negative',
                        line={'color': my_color[1] + ',0.8)'}))  
    fig.add_trace(go.Scatter(x=tweets_time_neu_df.created_at, y=tweets_time_neu_df.tweet_id,
                        mode="lines",
                        name='Neutral',
                        line={'color':my_color[0] + ',0.9)'})) 

    if include_event:    
        fig.add_trace(go.Scatter(x=tweets_time_df.created_at, y=tweets_time_df.tweet_id,
                        mode='none',
                        name = "",
                        text = tweets_time_df['description'],
                        hovertemplate = 'Event: '+
                        '<b>%{text}</b>',))

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

    fig.update_xaxes(rangeslider_visible = showrange_visible)
    return fig


def split_text(a_string, n):
    split_strings = []
    for index in range(0, len(a_string), n):
        split_strings.append(a_string[index : index + n].strip())
    return "<br>".join(split_strings)


def get_monthly_numbers(df):
    df2 = df[['created_at','tweet_id']].copy()
    df2.created_at = pd.to_datetime(df2.created_at)
    df2 = df2.set_index('created_at').resample('M').sum()
    df2.reset_index(inplace = True)
    return df2


def pie_chart(tweets_df, cond, title):
    df = get_distribution(tweets_df, cond)
    fig = px.pie(df, values='tweet_id', names='label')

    fig.update_traces(textinfo='label+percent',
                    textfont_size=15,
                    marker={'colors': ['#CE1B28', '#E1C027', '#0CCE49']},
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


def get_distribution(tweets_df, cond):
    if not cond is None:
        df = tweets_df[cond].copy()
    else:
        df = tweets_df.copy()
    tweets_time_df = df[['label', 'tweet_id']].groupby(['label']).count().reset_index().copy()
    
    return tweets_time_df


def seven_days(tweets_df, cond):
    # lets check components of time series
    if not cond is None:
        series = tweets_df[cond][['created_at', 'label', 'tweet_id']].groupby(['created_at', 'label']).count().reset_index()
    else:
        series = tweets_df[['created_at', 'label', 'tweet_id']].groupby(['created_at', 'label']).count().reset_index()

    series.created_at = pd.to_datetime(series.created_at)
    series = series.set_index('created_at')
    series = series.pivot(columns='label', values='tweet_id')
    series.fillna(0, inplace=True)
    series = series.resample(rule='W').sum()
    series = series.reset_index()
    
    return series


def max_sentiment(tweets_df, cond):   
    df = seven_days(tweets_df, cond)
    
    # Global sentiment
    max_sent = df.iloc[-1,:]
    global_sent = df.sum()
        
    return max_sent, global_sent


# Configurations
myy = my_yaml.my_yaml_tweet()
default_config = myy.get_default_prep_config()   
is_insert_data_after = default_config["is_insert_data_after"]
date_insert_data_after = datetime.datetime.strptime(default_config["date_insert_data_after"], '%Y,%m,%d').date()
del myy, default_config

setdates_style = {"display":"none"}
message_tooltip = "Welcome to the dashboard!\nThis is the data collected for the final project{} of the MSc in DA. {}data is collected everyday at 23:50."

if bool(is_insert_data_after):
    setdates_style = {'display':'inicial'}
    message_tooltip = message_tooltip.format(" from 1 January 2020 to 13 August 2021", 'After the inicial collection, ')
else:
    message_tooltip = message_tooltip.format("", 'The ')

layout = html.Div(children=[   
                
                dcc.ConfirmDialog(
                        id='confirm',
                        message='Danger danger! Are you sure you want to continue?',
                    ),

                dbc.Row(children=[
                        html.Div(children=[html.Button(id='openid',
                                                   children=[html.Img(src='assets/info-circle-fill.svg', style={'width':'30px'} )],
                                                   className='position-fixed', style={'right':'10px', 'z-index':'1000000', 'border': 'none', 'width': 'auto', 'margin': '0', 'padding': '0'}
                                                   ),]
                             ),
                        
                        dbc.Tooltip(children=[message_tooltip],
                        target="openid",
                        style={'font-size':'12px'}
                        ),
                        
                        dbc.Col(children=[html.H1("Dashboard", 
                                                  style={'textAlign': 'center', 'color': 'black', 'margin-bottom': '0px'}, 
                                                  className='display-4'),
                                          html.H4("Sentiment Analysis on COVID-19 vaccines in Ireland", 
                                                  style={'textAlign': 'center', 'color':'gray', 'margin-top': '0px', 'font-size':'20px'}, 
                                                  className='display-4')], 
                                className="col-sm-12", md=3
                                ),         
                        ], justify="center"),
                    
                dbc.Row([
                            dbc.Col([
                                      html.H4('Sentiment over time', style={'textAlign': 'center', }),
                                      dcc.Graph(id='overtimeline')
                                    ], className="col-9"),
                            dbc.Col(id='summ',
                                    className="col-3")
                            
                        ], justify="center"),
                
                dbc.Row(dbc.Col(id='loctblid', style={'padding-bottom':'20px'}), className="col")

])

# Get data from database
da = tweet_data.tweet_data_remote()
tweets_df = da.get_tweets()
date_df = da.get_dates()
#date_reference_df = da.get_date_reference()
del da

cond = tweets_df['active'] == 1 # Empty tweets
tweets_df = tweets_df[cond].copy()

# Change column names from date
date_df.columns = ['id', 'created_at', 'description']

# Remove time from created_at
tweets_df.created_at = pd.to_datetime(tweets_df.created_at).dt.date
date_df.created_at = pd.to_datetime(date_df.created_at).dt.date

# Check batches collected
pattern = r'^(from_)(.*)?'
normalized = lambda b: re.sub(pattern, r'\2',b).replace("_c", "").replace("_public_figures", "")
tweets_df.batch_name = tweets_df.batch_name.apply(normalized)

normalized2 = lambda b: "others" if ("conversation" in b) | ("covid" in b) | ("to" in b) else b
tweets_df.batch_name = tweets_df.batch_name.apply(normalized2)
batch_names2 = tweets_df.batch_name.unique().tolist()

fullnames = {'gov':'Government', 'media': 'Media', 'health': 'Health Department', 'politicalp':'Political Party', 'others': 'Others'}

batch_name4 = [{'label': '  ' + fullnames[batch_names2[b]], 'value': str(b)} for b in range(len(batch_names2))]
batch_name4.append({'label':'All', 'value':"-1"})

datestrformat = lambda d: d.strftime("%b\n%y")
dateformat = lambda d: d.strftime("%Y-%m-%d")

min_date = '2020-01-01'
max_date = dateformat(tweets_df.created_at.max())

daterange = html.Div([
                    html.P("Date range", style={"font-size":"15px", "margin-top":"15px"}),
                    dcc.DatePickerRange(
                        id='perioddate',
                        start_date_placeholder_text="Start Period",
                        end_date_placeholder_text="End Period",
                        calendar_orientation='vertical',
                        min_date_allowed=min_date,
                        max_date_allowed=max_date,
                        start_date=min_date,
                        end_date=max_date,
                        initial_visible_month=min_date,
                        minimum_nights=30,
                        display_format='DD/MM/YYYY',
                        style={'display':'inline', 'font-size':'12px'}
                    ),
                    html.Button('Reset dates', id='resetdates', n_clicks=0),
                    html.Button('Set dates as in Report', id='setdates', n_clicks=0, style=setdates_style),
    ])

batch_names3 = html.Div([
                html.P("Type of usernames", style={"font-size":"15px", "margin-top":"15px"}),
                dcc.RadioItems(
                    id="batchnames",
                    options=batch_name4,
                    value="-1",
                    style={"font-size":"12px"}
                ) 
    ])

vaccines_name = {'Pfizer':['pfizer', 'biotech', 'btn162', 'comirnaty'], 'Aztrasenecan':['vaxzeria', 'oxford', 'astra', 'azd1222'], 'Moderna':['moderna'], 'J&J':['j&j', 'johnson', 'janssen']}
lst_name = list(vaccines_name.keys())
vaccines_name2 = [{'label': '  ' + lst_name[b], 'value': str(b)} for b in range(len(lst_name))]
vaccines_name2.append({'label':'All', 'value':"-1"})

vaccines_name1 = html.Div([
                html.P("Vaccines", style={"font-size":"15px", "margin-top":"15px"}),
                dcc.RadioItems(
                    id="vaccinenames",
                    options=vaccines_name2,
                    value="-1",
                    style={"font-size":"12px"}
                ) 
    ])

basis1 = {'Daily': 'D', 'Weekly': 'W', 'Monthly':'M', 'Quarterly':'Q'}
lst_basis = list(basis1.keys())
basis2 = [{'label': '  ' + lst_basis[b], 'value': str(b)} for b in range(len(lst_basis))]
basis3 = html.Div([
                html.P("Basis", style={"font-size":"15px", "margin-top":"15px"}),
                dcc.RadioItems(
                    id="basisid",
                    options=basis2,
                    value="0",
                    style={"font-size":"12px"}
                ) 
    ])

filters = html.Div(['Filters', daterange, basis3, batch_names3, vaccines_name1, html.Button('Clean filters', id='cleanfilters', n_clicks=0),])

@app.callback(
    [Output(component_id='summ', component_property='children'),
     Output(component_id='overtimeline', component_property='figure'),
     Output('confirm', 'displayed'),
     Output('confirm', 'message'),
     Output('resetdates', 'n_clicks'),
     Output('cleanfilters', 'n_clicks'),
     Output('perioddate', 'start_date'),
     Output('perioddate', 'end_date'),
     Output('batchnames', 'value'),
     Output('vaccinenames', 'value'),
     Output('loctblid', 'children'),
     Output('basisid', 'value'),
     Output('setdates', 'n_clicks'),
     
     ],
    
    [Input(component_id='perioddate', component_property='start_date'),
     Input(component_id='perioddate', component_property='end_date'),
     Input(component_id='batchnames', component_property='value'),
     Input(component_id='vaccinenames', component_property='value'),
     Input(component_id='resetdates', component_property='n_clicks'),
     Input(component_id='cleanfilters', component_property='n_clicks'),
     Input(component_id='basisid', component_property='value'),
     Input(component_id='setdates', component_property='n_clicks'),
     
     ]
    
)
def update_graphs(start_date, end_date, options, vaccines, n_clicks, cleanfilters, basis, n_clicks2):    
    
    global tweets_df, date_df
    global lst_name
    global min_date, max_date
    global date_insert_data_after
    
    if int(n_clicks) > 0:
        start_date = pd.to_datetime(min_date).date()
        end_date = pd.to_datetime(max_date).date()
    
    elif int(n_clicks2) > 0:
        start_date = pd.to_datetime(start_date).date()
        end_date = date_insert_data_after - timedelta(days=1)
        
    elif int(cleanfilters) > 0:
        start_date = pd.to_datetime(min_date).date()
        end_date = pd.to_datetime(max_date).date()
        vaccines = "-1"
        options = "-1"
        basis = "0"
        
    else:
        start_date = pd.to_datetime(start_date).date()
        end_date = pd.to_datetime(end_date).date()
    
    # Remove all tweets with no characters
    # Empty tweets would be classified as neutral as the lack of verbs/words with sentiment
    cond = tweets_df['active'] == 1 # Empty tweets
    tweets_df = tweets_df[cond].copy()
    
    # Another condition but for filters
    cond = (tweets_df.created_at <= end_date) & (tweets_df.created_at >= start_date)
    
    if int(options) > -1:
        cond1 = tweets_df.batch_name == batch_names2[int(options)]                
        cond = cond & cond1
        
    if int(vaccines) > -1:
        cond1 = [False for r in range(0,len(tweets_df))]
        name = lst_name[int(vaccines)]
        for v in vaccines_name[name]:
            cond1 = cond1 | (tweets_df.keywords_pharma.str.contains(v))
        
        cond2 = tweets_df.tweet_id == tweets_df.conversation_id
        cond3 = tweets_df.conversation_id.isin(tweets_df[cond1 & cond2].conversation_id.unique())
        
        cond = cond & cond3
        
    if len(tweets_df[cond]) == 0:
        return [{}, {}, True, "No data found!", 0, 0, start_date, end_date, options, vaccines, {}, basis]
    
    rule = basis1[lst_basis[int(basis)]]
    
    # Get positive, negative and neutral segmentation
    # Monthly
    fig = show_tweets_sentiment(tweets_df, date_df, cond, "<br>Daily tweets", rule = rule)
    
    # Pie chart
    fig2 = pie_chart(tweets_df, cond, "")
        
    max_sent, global_sent = max_sentiment(tweets_df, cond)
    if len(global_sent) == 2:
        global_label = global_sent.index[1]
    else:
        global_label = global_sent.idxmax()
    
    if len(max_sent) == 2:
        last_label = max_sent.index[1]
    else:
        last_label = pd.to_numeric(max_sent[1:]).idxmax()
    last_date = max_sent['created_at']
    
    colors = {'negative': 'danger', 'positive': 'success', 'neutral': 'warning'}
   
    summ = [
             dbc.Row(dbc.Col(
                html.Tbody(
                    html.Tr(
                        html.Td([
                                 dbc.Alert(global_label, color=colors[global_label], style={'font-size': '20px !important', 'margin':'0 !important'}), 
                                 html.P("Global sentiment", className="mb-0"),
                                 html.P(start_date.strftime('%Y-%m-%d') + " to " + end_date.strftime('%Y-%m-%d'), className="mb-0, addmargin")
                                 ], style={'width':'100%', 'border': 'none', 'font-size':'10px', 'text-align':'center'}
                        ), style={'width':'100%', 'border': 'none'}
                    ),
                ), className = 'col-auto'
            ), className = 'justify-content-center'),
             
            dbc.Row(dbc.Col(
                html.Tbody(
                    html.Tr(
                         html.Td([
                                  dbc.Alert(last_label, color=colors[last_label], style={'font-size': '20px !important', 'margin':'0 !important'}), 
                                  html.P("Last weekly sentiment", className="mb-0"),
                                  html.P((last_date - timedelta(days=7)).strftime('%Y-%m-%d') + " to " + last_date.strftime('%Y-%m-%d'), className="mb-0, addmargin")
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
                                 html.Span("  {:,}".format(len(tweets_df[cond])), className="mb-0", style={" margin-left":'20px !important', 'font-size':'20px !important'}),
                                 html.P("Tweets", className="mb-0", style={'border': 'none', 'font-size':'10px', 'text-align':'center'}),
                                ], style={'width':'100%', 'border': 'none'}
                        ), style={'width':'100%', 'border': 'none'}
                    )
                ), className = 'col-auto'
            ), className = 'justify-content-center'),
            
            dbc.Row(dbc.Col([            
                    html.H4('Distribution', style={'textAlign': 'center', }),
                    dcc.Graph(id='overtimepie', figure = fig2)                    
                    ]), 
            )
            
    ]
    
    #if basis == "0":
    cond = (date_df.created_at <= end_date) & (date_df.created_at >= start_date)
    date_df2 = date_df[cond].sort_values('created_at', ascending=False).copy()
    figtblbat = go.Figure(data=[go.Table(
            columnwidth = [10,40],
            header=dict(values=['Date', 'Event'],
                        fill_color='darkred',
                        font=dict(color='white', size=12),
                        align='left'),
            cells=dict(values=[
                                date_df2.created_at,
                                date_df2.description
                              ],
                       align='left'))
            ])
        
    figtblbat.update_layout(
        height=200,
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0,
            pad=0
        ),
        paper_bgcolor="White",
    )
    figtbl = dcc.Graph(figure=figtblbat)
    #else:
    #    figtbl = [{}]
    
    return [summ, fig, False, "", 0, 0, start_date, end_date, options, vaccines, figtbl, basis, 0]