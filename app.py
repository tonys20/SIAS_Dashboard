import streamlit as st
import yfinance as yf 
import pandas as pd 
import os

tickers_df = pd.read_csv('TICKERS.csv')
tickers_ls = tickers_df.SECTOR.unique()
tickers_dic = {ticker_ls[i]:tickers_df[df[TICKER]==ticker_ls[i]] for i in len(tickers_ls)}
st.write(tickers_dic)
st.write(tickers_df)