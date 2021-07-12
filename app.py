import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from scraper import TweetCollector
from config import api_key, api_secret

tweets = TweetCollector(api_key, api_secret)
data = tweets.get_tweets('#ETH','en',1000)
data = tweets.find_sentiment(data)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

polarity_fig = px.histogram(data, 'polarity')
subjectivity_fig = px.histogram(data, 'subjectivity')

app.layout = html.Div(children=[

    html.H1(children='Crypto Sentiment Analyser'),

    dcc.Dropdown(
        id='slct-crypto',
        options=[
            {'label':'Ethereum','value':'#ETH'},
            {'label':'Bitcoin','value':'#BTC'},
            {'label':'Chainlink','value':'#LINK'},
            {'label':'Ada','value':'#ADA'}
        ]
    ),

    html.Div(children='''
        Ethereum
    '''),

    dcc.Graph(
        id='polarity_fig',
        figure=polarity_fig
    ),

    dcc.Graph(
        id='subjectivity_fig',
        figure=subjectivity_fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True, host = '127.0.0.1')