import streamlit as st
import yfinance as yf
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta

st.title("글로벌 시총 Top 10 기업 최근 3년 주가 변화")

# Top 10 티커 리스트
tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "BRK-B", "META", "UNH", "JPM"]

# 기간 설정 (최근 3년)
end_date = datetime.today()
start_date = end_date - timedelta(days=3*365)

# 데이터를 담을 빈 데이터프레임 생성
all_data = pd.DataFrame()

# 각 기업의 데이터 불러오기
for ticker in tickers:
    df = yf.download(ticker, start=start_date, end=end_date)[["Close"]]
    df = df.reset_index()
    df["Ticker"] = ticker
    all_data = pd.concat([all_data, df])

# 그래프 그리기 (인터랙티브한 plotly)
fig = px.line(
    all_data,
    x="Date",
    y="Close",
    color="Ticker",
    title="글로벌 시총 Top 10 기업 최근 3년 주가 변화",
    labels={"Close": "종가", "Date": "날짜", "Ticker": "기업"},
)

st.plotly_chart(fig)
