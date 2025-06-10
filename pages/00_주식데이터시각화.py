import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date, timedelta

st.set_page_config(page_title="글로벌 시총 Top 10 기업 주가 변화", layout="wide")

# 기업 리스트, 티커, 설명 (간략)
top_10_companies = {
    "Apple": {"ticker": "AAPL", "desc": "미국의 대표 IT 기업, 아이폰 제조사."},
    "Microsoft": {"ticker": "MSFT", "desc": "세계 최대 소프트웨어 기업."},
    "Saudi Aramco": {"ticker": "2222.SR", "desc": "사우디 아라비아 국영 석유 회사."},
    "Alphabet (Google)": {"ticker": "GOOGL", "desc": "구글의 모회사, 검색 및 광고 분야 세계 1위."},
    "Amazon": {"ticker": "AMZN", "desc": "세계 최대 전자상거래 및 클라우드 기업."},
    "NVIDIA": {"ticker": "NVDA", "desc": "그래픽 칩 및 AI 반도체 선두 업체."},
    "Berkshire Hathaway": {"ticker": "BRK-B", "desc": "워렌 버핏의 투자 지주회사."},
    "Meta (Facebook)": {"ticker": "META", "desc": "페이스북 및 인스타그램 운영 기업."},
    "TSMC": {"ticker": "TSM", "desc": "세계 최대 반도체 파운드리 업체 (대만)."},
    "Eli Lilly": {"ticker": "LLY", "desc": "미국의 글로벌 제약 기업."}
}

# 다국어 지원 - 영어 / 한국어
lang = st.sidebar.radio("언어 선택 / Choose Language", ("한국어", "English"))

if lang == "한국어":
    title = "📊 글로벌 시가총액 Top 10 기업의 주가 변화 (최근 3년간)"
    select_text = "기업을 선택하세요 (복수 선택 가능):"
    stock_change_text = "최근 3년간 주가 변화 (종가 기준)"
    market_cap_text = "시가총액 (최근)"
    perc_change_text = "3년간 수익률 (%)"
    select_scale = "그래프 스케일 선택"
    linear = "선형 (Linear)"
    log = "로그 (Logarithmic)"
    desc_title = "기업 설명"
else:
    title = "📊 Top 10 Global Companies by Market Cap Stock Price Change (Last 3 Years)"
    select_text = "Select companies (multiple):"
    stock_change_text = "Stock Price Change (Adjusted Close)"
    market_cap_text = "Market Cap (Latest)"
    perc_change_text = "3-Year Return (%)"
    select_scale = "Select graph scale"
    linear = "Linear"
    log = "Logarithmic"
    desc_title = "Company Description"

st.title(title)

# 날짜 범위 설정 (최근 3년)
end_date = date.today()
start_date = end_date - timedelta(days=3 * 365)

# 사이드바에 기업 선택 및 설명 표시
selected_companies = st.sidebar.multiselect(select_text, list(top_10_companies.keys()), default=list(top_10_companies.keys()))

st.sidebar.markdown(f"### {desc_title}")
for c in selected_companies:
    st.sidebar.markdown(f"**{c}**: {top_10_companies[c]['desc']}")

# 그래프 스케일 선택
scale = st.sidebar.radio(select_scale, (linear, log))

if selected_companies:
    # 빈 데이터프레임으로 합치기
    combined_df = pd.DataFrame()

    # 시가총액과 수익률 데이터 저장용
    market_caps = {}
    returns = {}

    for company in selected_companies:
        ticker = top_10_companies[company]["ticker"]
        data = yf.download(ticker, start=start_date, end=end_date)
        if data.empty:
            st.warning(f"{company} 데이터가 없습니다.")
            continue

        # 시가총액 최근 데이터 (주가 * 발행주식수) - yfinance로는 info에 있음
        try:
            info = yf.Ticker(ticker).info
            market_caps[company] = info.get('marketCap', None)
        except:
            market_caps[company] = None

        # 수익률 계산
        start_price = data["Adj Close"].iloc[0]
        end_price = data["Adj Close"].iloc[-1]
        returns[company] = ((end_price - start_price) / start_price) * 100

        # 합치기
        temp_df = data[["Adj Close"]].copy()
        temp_df.columns = [company]
        combined_df = pd.concat([combined_df, temp_df], axis=1)

    # 차트 그리기
    st.subheader(stock_change_text)

    fig, ax = plt.subplots(figsize=(14, 7))
    if scale == linear:
        for col in combined_df.columns:
            ax.plot(combined_df.index, combined_df[col], label=col)
        ax.set_yscale('linear')
    else:
        for col in combined_df.columns:
            ax.plot(combined_df.index, combined_df[col], label=col)
        ax.set_yscale('log')

    ax.set_xlabel("Date")
    ax.set_ylabel("Adjusted Close Price (USD)")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

    # 시가총액 및 수익률 테이블 표시
    st.subheader(f"{market_cap_text} & {perc_change_text}")

    summary_df = pd.DataFrame({
        "Market Cap (USD Trillion)": [mc / 1e12 if mc else None for mc in market_caps.values()],
        "3-Year Return (%)": [round(r, 2) for r in returns.values()]
    }, index=market_caps.keys())

    st.dataframe(summary_df.style.format({
        "Market Cap (USD Trillion)": "{:.3f}",
        "3-Year Return (%)": "{:.2f}"
    }))
else:
    st.info("최소 한 개의 회사를 선택해주세요.")
