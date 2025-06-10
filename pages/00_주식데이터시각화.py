import streamlit as st
import yfinance as yf
import pandas as pd
import datetime as dt

st.set_page_config(page_title="글로벌 시총 Top 10 기업 주가 시각화", layout="wide")

st.title("🌐 글로벌 시총 Top 10 기업 주가 변화 (최근 3년)")
st.markdown("데이터 출처: Yahoo Finance | 가격 기준: 일반 종가")

# 최근 3년간의 날짜 범위 설정
end_date = dt.date.today()
start_date = end_date - dt.timedelta(days=3*365)

# 시가총액 기준 글로벌 Top 10 기업 (2025년 기준 추정)
companies = {
    'Apple': 'AAPL',
    'Microsoft': 'MSFT',
    'Saudi Aramco': '2222.SR',
    'Nvidia': 'NVDA',
    'Alphabet (Google)': 'GOOGL',
    'Amazon': 'AMZN',
    'Meta Platforms': 'META',
    'Berkshire Hathaway': 'BRK-B',
    'TSMC': 'TSM',
    'Eli Lilly': 'LLY'
}

# 사용자 선택
selected_companies = st.multiselect("기업 선택:", options=list(companies.keys()), default=list(companies.keys()))

if selected_companies:
    st.write(f"선택한 기업: {', '.join(selected_companies)}")

    # 주가 데이터 다운로드
    tickers = [companies[name] for name in selected_companies]
    data = yf.download(tickers, start=start_date, end=end_date)['Close']  # 일반 종가 사용

    # 시각화
    st.line_chart(data)
else:
    st.warning("하나 이상의 기업을 선택하세요.")
