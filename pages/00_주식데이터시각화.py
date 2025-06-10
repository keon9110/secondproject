import streamlit as st
import yfinance as yf
import pandas as pd
import datetime as dt

st.set_page_config(page_title="글로벌 시총 Top 10 기업 주가 변화", layout="wide")

# 다크모드 토글 (사이드바)
dark_mode = st.sidebar.checkbox("🌙 다크 모드", value=False)

# 다크모드용 CSS 스타일
if dark_mode:
    st.markdown(
        """
        <style>
        .main {
            background-color: #0E1117;
            color: #E0E0E0;
        }
        .css-1d391kg {
            background-color: #0E1117;
        }
        .stButton>button {
            background-color: #1E1E1E;
            color: white;
        }
        .css-18e3th9 {
            background-color: #0E1117;
        }
        </style>
        """, unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <style>
        .main {
            background-color: white;
            color: black;
        }
        </style>
        """, unsafe_allow_html=True
    )

st.title("📈 글로벌 시총 Top 10 기업의 주가 변화")
st.markdown("""
최근 **3년 간의 일반 종가** 데이터를 기반으로 시각화했습니다.  
기업을 선택하고, 원하는 날짜 범위를 설정해 보세요.
""")

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

st.sidebar.header("🔧 설정")
selected_companies = st.sidebar.multiselect(
    "기업 선택:",
    options=list(companies.keys()),
    default=list(companies.keys())
)

today = dt.date.today()
default_start = today - dt.timedelta(days=3*365)

start_date = st.sidebar.date_input("시작 날짜", value=default_start, max_value=today)
end_date = st.sidebar.date_input("종료 날짜", value=today, max_value=today)

if start_date >= end_date:
    st.sidebar.error("시작 날짜는 종료 날짜보다 앞서야 합니다.")

log_scale = st.sidebar.checkbox("로그 스케일", value=False)

if selected_companies and start_date < end_date:
    tickers = [companies[name] for name in selected_companies]

    with st.spinner("📡 데이터를 불러오는 중입니다..."):
        raw_data = yf.download(tickers, start=start_date, end=end_date)['Close']
        if isinstance(raw_data, pd.Series):
            raw_data = raw_data.to_frame()
        raw_data.dropna(how='all', inplace=True)

    csv = raw_data.to_csv().encode('utf-8')
    st.download_button(
        label="⬇️ CSV 파일 다운로드",
        data=csv,
        file_name='stock_prices.csv',
        mime='text/csv'
    )

    st.subheader("📊 선택 기업 주가 변화 (일반 종가)")
    st.line_chart(raw_data, use_container_width=True, height=400, log_y=log_scale)

    st.subheader("🔍 기업별 상세 정보")
    tabs = st.tabs(selected_companies)
    for i, company in enumerate(selected_companies):
        ticker = companies[company]
        tab = tabs[i]

        with tab:
            st.markdown(f"### {company} ({ticker})")
            data = raw_data[ticker].dropna()
            st.line_chart(data, use_container_width=True, height=300, log_y=log_scale)

            st.markdown("**주가 통계 요약**")
            stats = {
                '최고가': f"{data.max():,.2f}",
                '최저가': f"{data.min():,.2f}",
                '평균가': f"{data.mean():,.2f}",
                '변동폭 (최고가-최저가)': f"{(data.max()-data.min()):,.2f}",
            }
            st.table(pd.DataFrame(stats, index=[0]).T.rename(columns={0:'값'}))

else:
    st.info("✅ 왼쪽에서 기업을 선택하고 날짜를 지정하세요.")
