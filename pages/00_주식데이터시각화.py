import streamlit as st
import yfinance as yf
import pandas as pd
import datetime

st.set_page_config(layout="wide")

# 날짜 설정
today = datetime.date(2025, 6, 10)
three_years_ago = today - datetime.timedelta(days=3 * 365)

st.title("글로벌 시총 Top 10 기업 주가 변화 (최근 3년)")
st.subheader(f"기준일: {today.strftime('%Y년 %m월 %d일')} | 데이터 기간: {three_years_ago.strftime('%Y년 %m월 %d일')} ~ {today.strftime('%Y년 %m월 %d일')}")

# BRK-A → BRK-B 로 대체
top_10_tickers = {
    "AAPL": "Apple Inc.",
    "MSFT": "Microsoft Corp.",
    "GOOGL": "Alphabet Inc. (Class A)",
    "AMZN": "Amazon.com Inc.",
    "NVDA": "NVIDIA Corp.",
    "META": "Meta Platforms Inc.",
    "TSLA": "Tesla Inc.",
    "BRK-B": "Berkshire Hathaway Inc. (Class B)",  # BRK-A는 다운로드 실패 가능
    "JPM": "JPMorgan Chase & Co.",
    "XOM": "Exxon Mobil Corp."
}

@st.cache_data
def get_stock_data(tickers, start_date, end_date):
    data = yf.download(list(tickers.keys()), start=start_date, end=end_date, progress=False, group_by='ticker')
    adj_close = pd.DataFrame()
    
    for ticker in tickers.keys():
        try:
            adj_close[ticker] = data[ticker]['Adj Close']
        except:
            st.warning(f"데이터를 불러오는 데 실패한 티커: {ticker}")
    
    return adj_close

try:
    with st.spinner("주가 데이터를 불러오는 중..."):
        df_adj_close = get_stock_data(top_10_tickers, three_years_ago, today)

    if df_adj_close.empty:
        st.warning("선택한 기간 동안의 주가 데이터를 찾을 수 없습니다. 날짜 범위를 확인해주세요.")
    else:
        # 정규화
        normalized_df = df_adj_close / df_adj_close.iloc[0] * 100
        normalized_df = normalized_df.rename(columns=top_10_tickers)

        st.line_chart(normalized_df)

        st.markdown(
            """
            * 상위 10개 기업은 2025년 6월 10일 현재 기준(예상)으로 선정되었습니다. 실제 순위는 변동될 수 있습니다.
            * 주가는 2022년 6월 10일 시점의 가격을 100% 기준으로 정규화하여 변화율을 나타냅니다.
            * 데이터는 `yfinance`를 통해 제공되며, 시장 상황에 따라 지연되거나 불완전할 수 있습니다.
            """
        )

        st.subheader("개별 기업 주가 데이터 (조정 종가)")
        st.dataframe(df_adj_close.tail())

except Exception as e:
    st.error(f"데이터를 불러오거나 시각화하는 중 오류가 발생했습니다: {e}")
    st.warning("주식 티커를 확인하거나 인터넷 연결 상태를 확인해주세요.")
