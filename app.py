import streamlit as st
import yfinance as yf 
import pandas as pd 
import os

tickers_df = pd.read_csv('TICKERS.csv')
sectors_ls = tickers_df.SECTOR.unique()
tickers_dic = {sectors_ls[i]:tickers_df[tickers_df['TICKER']==sectors_ls[i]] for i in range(len(sectors_ls))}
st.write(tickers_dic)
st.write(tickers_df)