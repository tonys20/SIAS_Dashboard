import streamlit as st
import yfinance as yf 
import pandas as pd 


def get_tickers():
    targetdir = os.path.join(os.getcwd(), 'tickers')
    ticker_dic ={}
    for filename in filter(lambda p: p.endswith('txt'), os.listdir(targetdir)):
        filepath =os.path.join(targetdir, filename)
        with open(filepath, mode='r') as f:
            lines = f.readlines()
        ticker_dic[filename.strip('.txt')]=[ticker.strip('\n') for ticker in lines]
    return ticker_dic
tickers = get_tickers()
sectors = list(tickers.keys())
st.write(sectors)