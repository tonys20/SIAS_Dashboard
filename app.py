import streamlit as st
import yfinance as yf 
import pandas as pd 
import os
import datetime
import plotly.express as px

tickers_df = pd.read_csv('TICKERS2.csv')
sectors_ls = tickers_df.SECTOR.unique()
tickers_dic = {sectors_ls[i]:list(tickers_df[tickers_df['SECTOR']==sectors_ls[i]]['TICKER']) for i in range(len(sectors_ls))}

@st.cache
def get_target(sector):
    today = datetime.date.today()
    output = pd.DataFrame()
    for ticker in tickers_dic[sector]:
        output[f'{ticker} Adj Close'] = yf.download(tickers = ticker, start ='1999-11-30', end =str(today), interval ='1d')['Adj Close']
    return output
df = get_target('Industrials')

def ret_calc(df):
    output = pd.DataFrame()
    for col in df.columns:
        output[f'{col} return'] = df[col]/df[col].shift(1)-1
        output['sector_return'] = df.sum(axis = 1)
    return output
ret_df = ret_calc(df)
st.write(ret_df)