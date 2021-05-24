#!/usr/bin/env python
# coding: utf-8

# In[31]:


import json
import os
import pandas as pd


# In[32]:


def readJson(json_path, json_file):
    with open(f'{json_path}/{json_file}') as f:
        return json.load(f)


# In[33]:


listdf = []


# In[34]:


for filejson in os.listdir('json'):
    mydf = pd.DataFrame()
    myjson = readJson('json', filejson)
    mydf['date'] = [myjson['date']]
    mydf['category'] = [myjson['category']]
    mydf['title'] = [myjson['title']]
    mydf['text'] = [myjson['text']]
    listdf.append(mydf)


# In[35]:


newsDataset = pd.concat(listdf)


# In[50]:


mairenews = newsDataset.loc[newsDataset['title'].str.contains('maire', case=0)]
mairenews


# In[58]:


maireprices = pd.read_csv(os.path.join('prices', 'MT.MI.csv'))
maireprices['Date'] = maireprices['Date'].apply(lambda x : x.replace("-", ''))
maireprices


# In[63]:


result = mairenews.rename(columns={'date':'Date'}).merge(maireprices, how='right')


# In[102]:


import plotly.graph_objects as go

import pandas as pd
from datetime import datetime

def plotCandle(df):
    fig = go.Figure(data=[go.Candlestick(x=pd.to_datetime(df['Date']),
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'])])
    
    newsdf = df.loc[df['title'].notna()]
   
    for row in newsdf.iterrows():
        fig.add_annotation(x=pd.to_datetime(row[1]['Date']), 
                           y=row[1]['Open'],
            text=row[1]['title'],
            showarrow=True,
            arrowhead=1)
    
    fig.show()


# In[103]:


plotCandle(result)


# In[101]:


row[1]['Date']


# In[ ]:




