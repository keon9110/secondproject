import streamlit as st
import yfinance as yf
import pandas as pd
import datetime as dt

st.set_page_config(page_title="글로벌 시총 Top 10 기업 주가 변화", layout="wide")

st.title("📈 글로벌 시총 Top 10 기업의 주가 변화")
st.markdown("""
최근 **3년 간의 일반 종가** 데이터를 기반으로 시각화했습니다.  
기업을 선택하고, 원하는 날짜 범위를 설정해 보세요.
""")

# 글로벌 시총 Top 10 기업 (2025년 기준)
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

# --- Sidebar ---
st.sidebar.header("🔧 설정")
selected_companies = st.sidebar.multiselect(
    "기업 선택:",
    options=list(companies.keys()),
    default=list(companies.keys())
)

# 날짜 범위 설정
today = dt.date.today()
default_start = today - dt.timedelta(days=3*365)

start_date = st.sidebar.date_input("시작 날짜", value=default_start, max_value=today)
end_date = st.sidebar.date_input("종료 날짜", value=today, max_value=today)

if start_date >= end_date:
    st.sidebar.error("시작 날짜는 종료 날짜보다 앞서야 합니다.")

# --- 데이터 불러오기 및 시각화 ---
if selected_companies and start_date < end_date:
    tickers = [companies[name] for name in selected_companies]

    with st.spinner("📡 데이터를 불러오는 중입니다..."):
        raw_data = yf.download(tickers, start=start_date, end=end_date)['Close']
        if isinstance(raw_data, pd.Series):
            raw_data = raw_data.to_frame()

        raw_data.dropna(how='all', inplace=True)

    st.subheader("📊 주가 변화 (일반 종가 기준)")
    st.line_chart(raw_data)
else:
    st.info("✅ 왼쪽에서 기업을 선택하고 날짜를 지정하세요.")
