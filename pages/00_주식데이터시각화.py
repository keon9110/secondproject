import streamlit as st
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta

st.title("글로벌 시총 Top 10 기업 주가 변화 시각화")

# 사이드바에 입력 UI 배치
st.sidebar.header("조회 옵션")

# 기업 리스트
tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "BRK-B", "META", "UNH", "JPM"]

# 날짜 기본값 및 제한 (최대 5년)
default_end = datetime.today()
max_range = timedelta(days=5*365)
default_start = default_end - timedelta(days=3*365)

col1, col2 = st.sidebar.columns(2)
with col1:
    start_date = st.date_input("시작 날짜", value=default_start, max_value=default_end, key="start")
with col2:
    end_date = st.date_input("끝 날짜", value=default_end, max_value=default_end, key="end")

if start_date > end_date:
    st.sidebar.error("시작 날짜는 종료 날짜보다 이전이어야 합니다.")
    st.stop()

if (end_date - start_date) > max_range:
    st.sidebar.error("최대 5년까지 선택 가능합니다.")
    st.stop()

selected_tickers = st.sidebar.multiselect(
    "기업 선택 (최소 1개 이상)",
    tickers,
    default=tickers
)

if len(selected_tickers) == 0:
    st.sidebar.error("최소 1개의 기업을 선택해 주세요.")
    st.stop()

price_type = st.sidebar.selectbox(
    "가격 유형 선택",
    ["Close", "Open", "High", "Low", "Volume"]
)

chart_type = st.sidebar.selectbox(
    "그래프 유형 선택",
    ["선 그래프", "캔들스틱 차트"]
)

# 본문 영역: 데이터 처리 및 그래프 출력
with st.spinner("데이터 다운로드 중..."):
    all_data = pd.DataFrame()
    for ticker in selected_tickers:
        df = yf.download(ticker, start=start_date, end=end_date)
        if df.empty:
            st.warning(f"{ticker} 데이터가 없습니다.")
            continue
        df = df.reset_index()
        df["Ticker"] = ticker
        all_data = pd.concat([all_data, df])

if all_data.empty:
    st.warning("선택한 조건에 맞는 데이터가 없습니다.")
    st.stop()

# 본문 그래프 영역
st.markdown(f"### 선택한 기업들의 {price_type} 주가 변화 ({start_date} ~ {end_date})")

if chart_type == "선 그래프":
    fig = px.line(
        all_data,
        x="Date",
        y=price_type,
        color="Ticker",
        labels={price_type: price_type, "Date": "날짜", "Ticker": "기업"},
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)

else:  # 캔들스틱 차트
    if len(selected_tickers) > 1:
        st.error("캔들스틱 차트는 하나의 기업만 선택해 주세요.")
        st.stop()

    df = all_data[all_data["Ticker"] == selected_tickers[0]]
    fig = go.Figure(data=[go.Candlestick(
        x=df['Date'],
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name=selected_tickers[0]
    )])

    fig.update_layout(
        title=f"{selected_tickers[0]} 캔들스틱 차트",
        xaxis_title="날짜",
        yaxis_title="가격",
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)
