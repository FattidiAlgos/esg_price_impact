import json
import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
from pandas_datareader import data as wb

def get_price(ticker : str, start : datetime, end : datetime) -> pd.DataFrame:
    return wb.DataReader(ticker, start = start, end = end, data_source='yahoo').reset_index()

def readJson(json_path, json_file):
    with open(f'{json_path}/{json_file}') as f:
        return json.load(f)

def load_news(path : str) -> pd.DataFrame:
    listdf = []
    for filejson in os.listdir(path):
        mydf = pd.DataFrame()
        myjson = readJson(path, filejson)
        mydf['date'] = [myjson['date']]
        mydf['category'] = [myjson['category']]
        mydf['title'] = [myjson['title']]
        mydf['text'] = [myjson['text']]
        listdf.append(mydf)

    res = pd.concat(listdf).reset_index(drop=True)
    res['Date'] = pd.to_datetime(res['date'], format='%Y%m%d')
    return res.drop(columns='date')


def filter_news(name : str, news_dataset : pd.DataFrame):
    return news_dataset.loc[news_dataset['title'].str.contains(name, case=0)]

def concat(x):
    return " / ".join(x)

def plotCandle(df):
    fig = go.Figure(data=[go.Candlestick(x=pd.to_datetime(df['Date']),
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'])])
    newsdf = pd.pivot_table(df.loc[df['title'].notna()], index='Date', values=['Open', 'title'], aggfunc={'Open' : np.mean,
                                                                                                          'title' : concat}).reset_index()
    for row in newsdf.iterrows():
        fig.add_annotation(x=pd.to_datetime(row[1]['Date']), 
                           y=row[1]['Open'],
            text=row[1]['title'],
            showarrow=True,
            textangle = 90,
            arrowhead=1)
    
    fig.show()