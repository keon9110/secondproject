import streamlit as st
import yfinance as yf
import pandas as pd
import datetime

st.set_page_config(layout="wide")

# 오늘 날짜 (2025년 6월 10일로 가정)
today = datetime.date(2025, 6, 10)
# 3년 전 날짜
three_years_ago = today - datetime.timedelta(days=3 * 365) # 대략적인 3년

st.title("글로벌 시총 Top 10 기업 주가 변화 (최근 3년)")
st.subheader(f"기준일: 2025년 6월 10일 | 데이터 기간: {three_years_ago.strftime('%Y년 %m월 %d일')} ~ {today.strftime('%Y년 %m월 %d일')}")

# 글로벌 시총 Top 10 기업 (2025년 6월 10일 현재 기준, 실제 변동 가능성 있음)
# 실제 시총 Top 10은 실시간으로 변동되므로, 여기서는 대표적인 초대형 기술 기업 위주로 선정합니다.
# 정확한 Top 10을 얻으려면 별도의 API를 사용해야 하지만, yfinance만으로 구현하기 위해 수동으로 선정합니다.
# 만약 더 정확한 Top 10을 원하시면, 별도의 스크래핑 또는 유료 API 사용이 필요합니다.
top_10_tickers = {
    "AAPL": "Apple Inc.",
    "MSFT": "Microsoft Corp.",
    "GOOGL": "Alphabet Inc. (Class A)",
    "AMZN": "Amazon.com Inc.",
    "NVDA": "NVIDIA Corp.",
    "META": "Meta Platforms Inc.",
    "TSLA": "Tesla Inc.",
    "BRK-A": "Berkshire Hathaway Inc. (Class A)", # BRK-B를 더 많이 거래
    "JPM": "JPMorgan Chase & Co.",
    "XOM": "Exxon Mobil Corp."
}

@st.cache_data
def get_stock_data(tickers, start_date, end_date):
    data = yf.download(list(tickers.keys()), start=start_date, end=end_date)
    return data['Adj Close']

try:
    with st.spinner("주가 데이터를 불러오는 중..."):
        df_adj_close = get_stock_data(top_10_tickers, three_years_ago, today)

    if df_adj_close.empty:
        st.warning("선택한 기간 동안의 주가 데이터를 찾을 수 없습니다. 날짜 범위를 확인해주세요.")
    else:
        # 첫날 주가로 정규화 (100% 기준으로 변화율 계산)
        normalized_df = df_adj_close / df_adj_close.iloc[0] * 100

        # 컬럼 이름 변경 (티커 -> 기업명)
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
        st.dataframe(df_adj_close.tail()) # 최근 5일치 데이터만 표시

except Exception as e:
    st.error(f"데이터를 불러오거나 시각화하는 중 오류가 발생했습니다: {e}")
    st.warning("주식 티커를 확인하거나 인터넷 연결 상태를 확인해주세요.")
