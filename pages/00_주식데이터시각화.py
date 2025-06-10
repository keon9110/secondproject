import streamlit as st
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(layout="wide") # 페이지 전체 너비 사용

st.title("글로벌 시총 Top 10 기업 주가 변화 시각화")
st.markdown("전 세계 시가총액 상위 10개 기업의 주가 데이터를 조회하고 다양한 방식으로 시각화합니다.")

# --- 사이드바에 입력 UI 배치 ---
st.sidebar.header("조회 옵션")

# 기업 리스트 (2024년 6월 기준 주요 시총 상위 기업)
# 야후 파이낸스 티커 기준
tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "BRK-B", "META", "UNH", "JPM"]
ticker_names = {
    "AAPL": "Apple",
    "MSFT": "Microsoft",
    "GOOGL": "Alphabet (Google)",
    "AMZN": "Amazon",
    "NVDA": "NVIDIA",
    "TSLA": "Tesla",
    "BRK-B": "Berkshire Hathaway",
    "META": "Meta Platforms",
    "UNH": "UnitedHealth Group",
    "JPM": "JPMorgan Chase"
}

# 날짜 기본값 및 제한 (최대 5년)
default_end = datetime.today()
max_range = timedelta(days=5*365) # 약 5년
default_start = default_end - timedelta(days=3*365) # 기본 3년

col1, col2 = st.sidebar.columns(2)
with col1:
    start_date = st.date_input("시작 날짜", value=default_start, max_value=default_end, key="start")
with col2:
    end_date = st.date_input("끝 날짜", value=default_end, max_value=default_end, key="end")

# 날짜 유효성 검사
if start_date > end_date:
    st.sidebar.error("시작 날짜는 종료 날짜보다 이전이어야 합니다.")
    st.stop()

if (end_date - start_date) > max_range:
    st.sidebar.error("최대 5년까지의 데이터를 조회할 수 있습니다.")
    st.stop()

selected_tickers = st.sidebar.multiselect(
    "기업 선택 (최소 1개 이상)",
    options=tickers,
    format_func=lambda x: f"{x} ({ticker_names[x]})", # 티커 옆에 회사명 표시
    default=tickers # 기본적으로 모두 선택
)

# 기업 선택 유효성 검사
if len(selected_tickers) == 0:
    st.sidebar.warning("최소 1개의 기업을 선택해 주세요.")
    st.stop()

price_type = st.sidebar.selectbox(
    "가격 유형 선택",
    ["Close", "Open", "High", "Low", "Volume", "Adj Close"], # Adj Close 추가
    help="* **Close**: 종가, * **Open**: 시가, * **High**: 고가, * **Low**: 저가, * **Volume**: 거래량, * **Adj Close**: 수정 종가 (배당, 분할 등 반영)"
)

chart_type = st.sidebar.selectbox(
    "그래프 유형 선택",
    ["선 그래프", "캔들스틱 차트"]
)

# --- 본문 영역: 데이터 처리 및 그래프 출력 ---
st.markdown("---")

# **MODIFIED DATA DOWNLOAD LOGIC**
with st.spinner("선택하신 기간과 기업의 주가 데이터를 다운로드 중입니다..."):
    # Use yf.download to get data for multiple tickers at once
    # This automatically handles the columns correctly, usually with a MultiIndex
    try:
        # download multiple tickers at once. This returns a MultiIndex DataFrame
        # where the first level is the metric (Close, High, etc.) and the second is the ticker.
        data_yf = yf.download(selected_tickers, start=start_date, end=end_date)
        
        if data_yf.empty:
            st.warning("선택하신 기간에 데이터가 없습니다. 날짜 범위나 기업을 다시 확인해 주세요.")
            st.stop()

        # To prepare for Plotly Express's 'long' format, we need to melt the DataFrame.
        # First, ensure 'Date' is a column, not index.
        data_yf = data_yf.reset_index()

        # Melt the DataFrame to long format
        # id_vars: columns to keep as identifiers
        # var_name: name for the new column holding the old column names (e.g., 'Close', 'High')
        # value_name: name for the new column holding the actual values
        # The columns are MultiIndex, so we need to flatten them first if not using specific levels
        # A common way to flatten MultiIndex columns is to create a new list of strings
        
        # Flatten MultiIndex columns to single strings, e.g., 'Close_AAPL', 'High_MSFT'
        # Or, ideally, prepare for melting.
        
        # Let's pivot slightly differently to get Tickers as top level columns easily
        # We want 'Date', 'Ticker', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'
        
        # Method 1: Using stack() to get long format (more robust for multiple tickers)
        # stack() converts the innermost level of column labels into part of the index.
        # This will give us a DataFrame with an outer index of Date and an inner index of the metric,
        # and then columns of the ticker. We then unstack the ticker and melt again.
        
        # Simpler approach: Iterate and concat, then melt
        all_data_list = []
        for ticker in selected_tickers:
            # yf.download when called with a single ticker already returns flat columns
            df_single = yf.download(ticker, start=start_date, end=end_date)
            if not df_single.empty:
                df_single = df_single.reset_index()
                df_single["Ticker"] = ticker
                all_data_list.append(df_single)
        
        if not all_data_list:
            st.warning("선택하신 기간에 데이터가 없습니다. 날짜 범위나 기업을 다시 확인해 주세요.")
            st.stop()

        # Concatenate all single-ticker dataframes
        # This results in 'Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'Ticker'
        # Which is the perfect 'long' format for Plotly Express
        all_data = pd.concat(all_data_list, ignore_index=True)

    except Exception as e:
        st.error(f"데이터 다운로드 또는 처리 중 오류가 발생했습니다: {e}")
        st.stop()

# --- DEBUGGING SECTION ---
st.subheader("🛠️ 디버깅 정보 (개발 시에만 보임)")
st.write(f"selected_tickers: {selected_tickers}")
st.write(f"price_type: {price_type}")
st.write(f"chart_type: {chart_type}")
st.write("--- all_data DataFrame 정보 ---")
st.write(f"all_data.empty: {all_data.empty}")
if not all_data.empty:
    st.write(f"all_data.shape: {all_data.shape}")
    st.write(f"all_data.columns: {all_data.columns.tolist()}")
    st.dataframe(all_data.head()) # Show first few rows
    st.dataframe(all_data.tail()) # Show last few rows
else:
    st.write("all_data DataFrame is empty after download.")
st.write("-----------------------------")
# --- END DEBUGGING SECTION ---


if all_data.empty: # This check is now redundant if the above `if not all_data_list` handles it, but good to keep
    st.warning("선택한 조건에 맞는 데이터가 없습니다. 날짜 범위나 기업을 다시 확인해 주세요.")
    st.stop()

# --- 그래프 그리기 ---
st.markdown(f"### 선택한 기업들의 **{price_type}** 주가 변화 ({start_date} ~ {end_date})")

# 선택된 가격 유형 컬럼이 데이터프레임에 있는지 확인 (Robustness fix)
if price_type not in all_data.columns:
    st.error(f"선택하신 가격 유형 **'{price_type}'**에 해당하는 데이터가 존재하지 않습니다. 다른 유형을 선택해 주세요.")
    st.stop()

if chart_type == "선 그래프":
    # Plotly Express를 사용하여 선 그래프 생성
    # Check if 'Date' column is datetime type, if not, convert it
    if 'Date' in all_data.columns and not pd.api.types.is_datetime64_any_dtype(all_data['Date']):
        st.warning("Date 컬럼이 datetime 타입이 아닙니다. 변환을 시도합니다.")
        try:
            all_data['Date'] = pd.to_datetime(all_data['Date'])
        except Exception as e:
            st.error(f"Date 컬럼을 datetime으로 변환하는 데 실패했습니다: {e}")
            st.stop()

    fig = px.line(
        all_data,
        x="Date",
        y=price_type,
        color="Ticker",
        labels={
            price_type: f"{price_type} (USD)" if price_type != "Volume" else "Volume",
            "Date": "날짜",
            "Ticker": "기업"
        },
        title=f"주가 {price_type} 추이",
        hover_name="Ticker", # 툴팁에 기업 이름 표시
        template="plotly_white" # 깔끔한 템플릿
    )
    # y축 포맷 설정 (Volume이 아닐 경우 달러 표시)
    if price_type != "Volume":
        fig.update_yaxes(tickformat="$,.2f")
    fig.update_layout(hovermode="x unified") # 마우스 오버 시 모든 라인에 대한 정보 표시
    st.plotly_chart(fig, use_container_width=True)

else:  # 캔들스틱 차트
    if len(selected_tickers) > 1:
        st.warning("캔들스틱 차트는 **하나의 기업만 선택**했을 때만 표시할 수 있습니다.")
        st.stop()

    # 단일 기업 선택 시 캔들스틱 차트 생성
    # We still need to filter for the single selected ticker here
    selected_ticker_df = all_data[all_data["Ticker"] == selected_tickers[0]]

    # Ensure Date column is datetime type
    if 'Date' in selected_ticker_df.columns and not pd.api.types.is_datetime64_any_dtype(selected_ticker_df['Date']):
        st.warning("캔들스틱 차트: Date 컬럼이 datetime 타입이 아닙니다. 변환을 시도합니다.")
        try:
            selected_ticker_df['Date'] = pd.to_datetime(selected_ticker_df['Date'])
        except Exception as e:
            st.error(f"캔들스틱 차트: Date 컬럼을 datetime으로 변환하는 데 실패했습니다: {e}")
            st.stop()


    # 캔들스틱 차트는 Open, High, Low, Close가 반드시 필요
    required_cols = ["Open", "High", "Low", "Close"]
    if not all(col in selected_ticker_df.columns for col in required_cols):
        st.error(f"캔들스틱 차트를 그리기 위한 **Open, High, Low, Close** 데이터가 부족합니다.")
        st.stop()

    fig = go.Figure(data=[go.Candlestick(
        x=selected_ticker_df['Date'],
        open=selected_ticker_df['Open'],
        high=selected_ticker_df['High'],
        low=selected_ticker_df['Low'],
        close=selected_ticker_df['Close'],
        name=f"{ticker_names[selected_tickers[0]]} ({selected_tickers[0]})"
    )])

    fig.update_layout(
        title=f"**{ticker_names[selected_tickers[0]]} ({selected_tickers[0]})** 캔들스틱 차트",
        xaxis_title="날짜",
        yaxis_title="가격 (USD)",
        xaxis_rangeslider_visible=False, # 하단 범위 슬라이더 숨기기
        template="plotly_white"
    )
    fig.update_yaxes(tickformat="$,.2f") # y축 포맷 달러 표시
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("데이터는 [Yahoo Finance](https://finance.yahoo.com/)에서 제공됩니다.")
