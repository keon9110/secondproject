import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# 여기에 고정 테마 설정 (기본 라이트)
st.set_page_config(
    page_title="글로벌 시가총액 Top 10 기업",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="auto",
    theme={"base": "light"},
)

# 다크모드 체크박스
dark_mode = st.sidebar.checkbox("🌙 다크모드", value=False)

if dark_mode:
    st.sidebar.warning("다크모드 적용을 위해 페이지를 새로고침해주세요 (F5).")

st.title("📊 글로벌 시가총액 Top 10 기업 - 최근 3년 주가 변화")

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
