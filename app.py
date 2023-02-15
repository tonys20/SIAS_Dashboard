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
with st.sidebar:
    sector_selected = st.selectbox('Choose Sector:',sectors_ls)


    start_time =st.date_input(
        'From:',
        value = datetime.date(1999, 11, 30),
        min_value = datetime.date(1999, 11, 30),
        max_value = datetime.date.today()
    )

    end_time = st.date_input(
        'To:',
        value = datetime.date(1999, 11, 30),
        min_value = datetime.date(1999, 11, 30),
        max_value = datetime.date.today()
    )

def ret_calc(df):
    output = pd.DataFrame()
    for col in df.columns:
        output[f'{col} return'] = df[col]/df[col].shift(1)-1
        output['sector_return'] = df.sum(axis = 1)/df.sum(axis = 1).shift(1) - 1
        output['cum_return'] = df.sum(axis = 1)/df.sum(axis = 1)[0] - 1
    return output

df = get_target(sector_selected)
custom_df = df.loc[str(start_time): str(end_time)]
ret_df = ret_calc(custom_df)
st.write(ret_df)

charts_ls = ['cumulative', 'daily']
fig = px.line(ret_df, y = 'cum_return')
st.plotly_chart(fig)