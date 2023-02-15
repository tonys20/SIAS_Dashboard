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
        value = datetime.date(2022, 12, 30),
        min_value = datetime.date(1999, 11, 30),
        max_value = datetime.date.today()
    )
    charts_ls = ['cumulative', 'daily']
    chart_type = st.selectbox('chart type', charts_ls)

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

if chart_type == 'cumulative':
    yvar = 'cum_return'
    y_label = f'Cumulative Return for {sector_selected}'
elif chart_type == 'daily':
    yvar = 'sector_return'
    y_label = f'Daily Return for {sector_selected}'

fig = px.line(ret_df, y = yvar, color_discrete_sequence=["#8B0000"]).update_layout(yaxis_title=y_label)
st.plotly_chart(fig)