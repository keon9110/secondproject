import streamlit as st
import folium
from streamlit_folium import st_folium
from folium import IFrame
import requests

# 페이지 설정
st.set_page_config(page_title="도쿄 여행 가이드", layout="wide")
st.markdown(
    """
    <style>
    .stApp {
        background-image: url('https://images.unsplash.com/photo-1556960266-36f73aa3c8b6?ixlib=rb-4.0.3');
        background-size: cover;
        background-attachment: fixed;
    }
    .weather-box {
        position: fixed;
        top: 100px; right: 50px;
        width: 250px;
        background: rgba(255,255,255,0.8);
        padding: 10px; border-radius: 8px;
    }
    </style>""", unsafe_allow_html=True
)

st.title("🇯🇵 도쿄 여행 가이드")
st.markdown("배경📸, 날씨🌤, 관광지📍, 예산💰까지 모두 포함한 앱입니다.")

# 오른쪽 고정 날씨 박스 (폴리움 지도 옆)
st.markdown('<div class="weather-box">', unsafe_allow_html=True)
st.markdown("### 📅 서울 기준 도쿄 7일 날씨")
# (위 forecast UI 삽입)
st.write("")  # placeholder
st.markdown('</div>', unsafe_allow_html=True)

# 관광지 목록 (추가 2곳 포함)
tourist_spots = [
    # 기존 5개...
    {"name":"하라주쿠 타케시타 거리","lat":35.6702,"lon":139.7020,
     "description":"젊음과 패션, 길거리 간식의 메카입니다.",
     "image":"https://upload.wikimedia.org/wikipedia/commons/3/32/Takeshita_Street.jpg",
     "time":"오전~오후 이른 시간",
     "transport":"JR 야마노테선 '하라주쿠 역' 도보 1분",
     "map_link":"https://www.google.com/maps/dir/?api=1&destination=Takeshita+Street",
     "video":"https://www.youtube.com/watch?v=abcd1234"},
    {"name":"우에노 공원","lat":35.7156,"lon":139.7745,
     "description":"넓은 공원, 박물관, 동물원이 있어 하루 코스로 좋습니다.",
     "image":"https://upload.wikimedia.org/wikipedia/commons/6/64/Ueno_Park.jpg",
     "time":"오전~점심",
     "transport":"JR 야마노테선 '우에노 역' 도보 5분",
     "map_link":"https://www.google.com/maps/dir/?api=1&destination=Ueno+Park",
     "video":"https://www.youtube.com/watch?v=efgh5678"},
    # 기존 위 5곳... (생략)
]

# 지도 생성
center = [35.6762, 139.6503]
m = folium.Map(location=center, zoom_start=12)
for spot in tourist_spots:
    html = f"""
    <h4>{spot['name']}</h4>
    <img src="{spot['image']}" width="200"><br>
    <b>시간:</b> {spot['time']}<br>
    <b>교통:</b> {spot['transport']}<br>
    <a href="{spot['map_link']}" target="_blank">📍 길찾기</a><br>
    <a href="{spot['video']}" target="_blank">▶ 영상</a>
    """
    iframe = IFrame(html, 250, 300)
    folium.Marker([spot['lat'], spot['lon']], popup=folium.Popup(iframe),
                  tooltip=spot['name'], icon=folium.Icon(color="blue")).add_to(m)

# 화면 출력 (왼쪽 지도/오른쪽 날씨)
col1, col2 = st.columns([3,1])
with col1:
    st.subheader("🗺 도쿄 주요 관광지")
    st_folium(m, width=700, height=500)

with col2:
    st.subheader("🌦 현재 & 향후 날씨")
    st.write("도쿄의 오늘과 향후 7일간의 날씨를 위쪽 박스에서 확인하세요.")

# 상세 정보 및 예산 계산기
st.subheader("📌 관광지 상세 & 예산 설정")
budget = {}
with st.form("budget"):
    for spot in tourist_spots:
        budget[spot['name']] = st.number_input(
            f"{spot['name']} 입장/체험비 (¥)", min_value=0, value=0)
    budget['교통비'] = st.number_input("하루 교통비 (¥)", min_value=0, value=1000)
    budget['식비'] = st.number_input("하루 식비 (¥)", min_value=0, value=2000)
    submit = st.form_submit_button("예산 계산")

if submit:
    total = sum(budget.values())
    st.success(f"🧾 총 예상 예산: ¥{total:,} 엔")
