import streamlit as st
import yfinance as yf 
import pandas as pd 
import os

tickers_df = pd.read_csv('TICKERS.csv')
tickers_ls = tickers_df.SECTOR.unique()
st.write(tickers_ls)
st.write(tickers_df)