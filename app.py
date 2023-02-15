import streamlit as st
import yfinance as yf 
import pandas as pd 
import os

tickers = pd.read_csv('TICKERS.csv')
st.write(tickers)