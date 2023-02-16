import streamlit as st
import yfinance as yf 
import pandas as pd 
import os
import datetime
import plotly.express as px
from PIL import Image
from full_fred.fred import Fred

tickers_df = pd.read_csv('TICKERS2.csv')
sectors_ls = tickers_df.SECTOR.unique()
tickers_dic = {sectors_ls[i]:list(tickers_df[tickers_df['SECTOR']==sectors_ls[i]]['TICKER']) for i in range(len(sectors_ls))}
fred = Fred('FRED API Key.txt')
fred.set_api_key_file('FRED API Key.txt')
fred.env_api_key_found()
benchmark_df = pd.read_csv('benchmark.csv')
benchmark_df['SHARES'] = pd.to_numeric(benchmark_df['SHARES'])
st.write(benchmark_df)

@st.cache
def get_target(sector):
    today = datetime.date.today()
    output = pd.DataFrame()
    for ticker in tickers_dic[sector]:
        try:
            output[f'{ticker} Adj Close'] = yf.download(tickers = ticker, start ='1999-11-30', end =str(today), interval ='1d')['Adj Close']
            share_count = benchmark_df[benchmark_df['TICKER'] == ticker]
            output[f'{ticker}_market_val'] = output[f'{ticker} Adj Close']*int(share_count['SHARES'])
            output.drop(columns = [f'{ticker} Adj Close'], inplace=True)
        except KeyError:
            pass
        except TypeError:
            pass
    return output

# Macro Indicators from Fred
fred_dic = {'Industrials': ['DGORDER', 'INDPRO','PPIACO'],
            'Consumer Discretionary':['PCE', 'DSPI'],
            'Consumer Staples': ['DFXARC1M027SBEA', 'CPIUFDNS', 'A229RX0A048NBEA'],
            'Health Care':['HLTHSCPCHCSA', 'CPIMEDSL'],
            'Information Technology':['AITINO', 'AITITI', 'PCU5182105182105'],
            'Communication Services':['DCOMRC1A027NBEA', 'CUSR0000SAE2','DSPIC96']}


@st.cache
def get_series(dic):
    output = {}
    for sector in dic.keys():
        output[sector]={}
        for id in dic[sector]:
            output[sector][id] = fred.get_series_df(id).drop(columns = ['realtime_start', 'realtime_end']).set_index('date', inplace=False)
    return output

macro_dic = get_series(fred_dic)

with st.sidebar:
    sector_selected = st.selectbox('Choose Sector:',sectors_ls)


    start_time =st.date_input(
        'From:',
        value = datetime.date(2022, 2, 10),
        min_value = datetime.date(1999, 11, 30),
        max_value = datetime.date.today()
    )

    end_time = st.date_input(
        'To:',
        value = datetime.date(2023, 2, 15),
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

'''
accum=dict()

for sector in sectors_ls:
    accum[sector] = get_target(sector)
'''

df = get_target(sector_selected)
st.write(df)

custom_df = df.loc[str(start_time): str(end_time)]
ret_df = ret_calc(custom_df)

ticker_display = pd.DataFrame(tickers_dic[sector_selected])
if chart_type == 'cumulative':
    yvar = 'cum_return'
    y_label = f'Cumulative Return for {sector_selected} sector'
elif chart_type == 'daily':
    yvar = 'sector_return'
    y_label = f'Daily Return for {sector_selected} sector'

tab1, tab2, tab3 = st.tabs(['Overview', 'Macro', 'Portfolio Holdings'])
with tab1:
    page1_title = '<p style="font-family:Courier; color:Black; font-size: 42px;">Dashboard Under Development</p>'
    st.markdown(page1_title, unsafe_allow_html=True)
    col1, col2 = st.columns([3,1])
    with col1:
        st.header('Returns and Charts')
        st.write('df view for dev only')
        st.write(ret_df)
        fig = px.line(ret_df, y = yvar, color_discrete_sequence=["#8B0000"]).update_layout(yaxis_title=y_label)
        st.write('daily return chart will add more widgets')
        st.plotly_chart(fig)
        fig = px.histogram(ret_df, x='sector_return', histnorm = 'probability density', marginal='box', color_discrete_sequence=["#8B0000"]).update_layout(xaxis_title ='Daily Return')
        st.write('daily return distribution in time range selected')
        st.plotly_chart(fig)
        
    with col2:
        st.header('Ticker List')
        st.write(ticker_display)

with tab2:
    st.write('Nothing here yet')
    st.write('Macroeconomic indicators, release schedules and news')
    
with tab3:
    st.write('Nothing here yet')
    st.write('ITD chart, fundamentals and some other cool stuff')

