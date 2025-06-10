import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# 다크모드 선택
dark_mode = st.sidebar.checkbox("🌙 다크모드", value=False)

# 페이지 테마 설정 (한번만 호출 가능, 그래서 체크박스가 반응하려면 페이지 재실행 필요)
if dark_mode:
    st.set_page_config(page_title="글로벌 시가총액 Top 10 기업", page_icon="📊", layout="wide", initial_sidebar_state="auto", 
                       theme={"base": "dark"})
else:
    st.set_page_config(page_title="글로벌 시가총액 Top 10 기업", page_icon="📊", layout="wide", initial_sidebar_state="auto", 
                       theme={"base": "light"})

st.title("📊 글로벌 시가총액 Top 10 기업 - 최근 3년 주가 변화")

# 시가총액 상위 10개 기업과 티커
companies = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Saudi Aramco": "2222.SR",  # 사우디 증시
    "Alphabet (Google)": "GOOG",
    "Amazon": "AMZN",
    "Nvidia": "NVDA",
    "Berkshire Hathaway": "BRK-B",
    "Meta Platforms": "META",
    "Tesla": "TSLA",
    "TSMC": "TSM"
}

# 최근 3년 기간 설정
end_date = datetime.today()
start_date = end_date - timedelta(days=3*365)

# 사용자 선택
selected_companies = st.multiselect("기업 선택", options=list(companies.keys()), default=list(companies.keys())[:5])

# 주가 데이터 가져오기
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

    # NaN 제거
    all_data.dropna(inplace=True)

    # 시각화
    st.line_chart(all_data)
else:
    st.info("시각화할 기업을 하나 이상 선택하세요.")
