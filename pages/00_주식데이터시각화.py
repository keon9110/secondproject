import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# 다크모드용 커스텀 CSS 삽입
dark_mode_css = """
<style>
    /* 배경 다크모드 */
    .main {
        background-color: #0e1117;
        color: #d7d7d7;
    }
    /* 헤더 색상 */
    header, .css-18e3th9 {
        background-color: #0e1117;
    }
    /* 차트 배경 */
    .stLineChart > div > div > svg {
        background-color: #0e1117 !important;
    }
    /* 텍스트 색상 */
    .css-1d391kg, .css-1d391kg span {
        color: #d7d7d7;
    }
    /* 선택 박스 배경/글자 색상 */
    div[role="listbox"] {
        background-color: #22272e;
        color: #d7d7d7;
    }
    /* 스크롤바 색상 */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-thumb {
        background-color: #555;
        border-radius: 4px;
    }
</style>
"""

st.markdown(dark_mode_css, unsafe_allow_html=True)

st.title("📊 글로벌 시가총액 Top 10 기업 - 최근 3년 주가 변화 (Dark Mode)")

companies = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Saudi Aramco": "2222.SR",
    "Alphabet (Google)": "GOOG",
    "Amazon": "AMZN",
    "Nvidia": "NVDA",
    "Berkshire Hathaway": "BRK-B",
    "Meta Platforms": "META",
    "Tesla": "TSLA",
    "TSMC": "TSM"
}

end_date = datetime.today()
start_date = end_date - timedelta(days=3*365)

selected_companies = st.multiselect("기업 선택", options=list(companies.keys()), default=list(companies.keys())[:5])

if selected_companies:
    st.write(f"📅 기간: {start_date.date()} ~ {end_date.date()}")
    all_data = pd.DataFrame()

    for name in selected_companies:
        ticker = companies[name]
        try:
            df = yf.download(ticker, start=start_date, end=end_date)
            df = df[['Adj Close']].rename(columns={"Adj Close": name})
            if all_data.empty:
                all_data = df
            else:
                all_data = all_data.join(df, how="outer")
        except Exception as e:
            st.warning(f"{name}의 데이터를 불러오는 데 실패했습니다. 오류: {e}")

    all_data.dropna(inplace=True)
    st.line_chart(all_data)
else:
    st.info("시각화할 기업을 하나 이상 선택하세요.")
