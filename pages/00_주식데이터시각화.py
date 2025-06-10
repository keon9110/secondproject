import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(layout="wide")

# 날짜 설정
today = datetime(2025, 6, 10)
three_years_ago = today - timedelta(days=3 * 365)

st.title("글로벌 시총 Top 10 기업 주가 변화 (최근 3년)")
st.subheader(f"기준일: {today.strftime('%Y년 %m월 %d일')} | 데이터 기간: {three_years_ago.strftime('%Y년 %m월 %d일')} ~ {today.strftime('%Y년 %m월 %d일')}")

# 티커 정의
top_10_tickers = {
    "AAPL": "Apple Inc.",
    "MSFT": "Microsoft Corp.",
    "GOOGL": "Alphabet Inc. (Class A)",
    "AMZN": "Amazon.com Inc.",
    "NVDA": "NVIDIA Corp.",
    "META": "Meta Platforms Inc.",
    "TSLA": "Tesla Inc.",
    "BRK-B": "Berkshire Hathaway Inc. (Class B)",
    "JPM": "JPMorgan Chase & Co.",
    "XOM": "Exxon Mobil Corp."
}

@st.cache_data
def fetch_all_stock_data(tickers, start, end):
    result_df = pd.DataFrame()
    for ticker in tickers:
        try:
            data = yf.download(ticker, start=start, end=end, progress=False)
            if not data.empty:
                result_df[ticker] = data['Adj Close']
            else:
                st.warning(f"데이터를 불러오는 데 실패한 티커: {ticker} (빈 데이터)")
        except Exception as e:
            st.warning(f"데이터를 불러오는 데 실패한 티커: {ticker} - {e}")
    return result_df

try:
    with st.spinner("주가 데이터를 불러오는 중..."):
        stock_data = fetch_all_stock_data(top_10_tickers.keys(), three_years_ago, today)

    if stock_data.empty:
        st.error("주가 데이터를 가져오는 데 완전히 실패했습니다.")
    else:
        # 정규화
        normalized_data = stock_data / stock_data.iloc[0] * 100
        normalized_data.rename(columns=top_10_tickers, inplace=True)

        st.line_chart(normalized_data)

        st.subheader("최근 주가 (조정 종가 기준)")
        st.dataframe(stock_data.tail())

        st.markdown("""
        - 주가는 첫날 기준(2022년 6월 10일)을 100으로 정규화하여 표시됩니다.
        - 데이터 출처: Yahoo Finance via `yfinance`
        - 일부 티커는 데이터 불러오기 실패 가능성이 있으므로 개별 경고로 표시됩니다.
        """)

except Exception as e:
    st.error(f"오류 발생: {e}")
