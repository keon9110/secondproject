import streamlit as st
import folium
from streamlit_folium import st_folium
from folium import IFrame
from datetime import datetime
import pytz

# 날짜 설정 (도쿄 기준)
tokyo_tz = pytz.timezone('Asia/Tokyo')
today = datetime.now(tokyo_tz).strftime("%Y년 %m월 %d일 (%A)")

# 페이지 설정
st.set_page_config(page_title="도쿄 여행 가이드", layout="wide")
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url('https://images.unsplash.com/photo-1586500024866-5c8a0fa2185c?auto=format&fit=crop&w=1600&q=80');
        background-size: cover;
        background-attachment: fixed;
    }}
    .weather-box {{
        position: fixed;
        top: 100px; right: 50px;
        width: 250px;
        background: rgba(255,255,255,0.85);
        padding: 10px; border-radius: 10px;
    }}
    </style>
    """, unsafe_allow_html=True
)

st.title("🇯🇵 도쿄 여행 가이드")
st.markdown(f"📅 **오늘 날짜 (도쿄 기준)**: {today}")

# 관광지 데이터
tourist_spots = [
    {
        "name": "도쿄 타워",
        "lat": 35.6586,
        "lon": 139.7454,
        "description": "도쿄의 상징적인 전망 타워.",
        "category": "전망",
        "image": "https://upload.wikimedia.org/wikipedia/commons/e/e5/Tokyo_Tower_and_around_Skyscrapers.jpg",
        "time": "일몰 후~밤",
        "transport": "아카반바시 역 도보 5분",
        "map_link": "https://www.google.com/maps/dir/?api=1&destination=Tokyo+Tower",
        "video": "https://www.youtube.com/watch?v=lBSkLjjViRI"
    },
    {
        "name": "센소지",
        "lat": 35.7148,
        "lon": 139.7967,
        "description": "가장 오래된 절, 문화 명소.",
        "category": "문화",
        "image": "https://upload.wikimedia.org/wikipedia/commons/f/f0/Sensoji_-_Thunder_Gate_-_2020.jpg",
        "time": "오전~오후",
        "transport": "아사쿠사 역 도보 2분",
        "map_link": "https://www.google.com/maps/dir/?api=1&destination=Sensoji+Temple",
        "video": "https://www.youtube.com/watch?v=psWfPoyDwKk"
    },
    {
        "name": "시부야 스크램블",
        "lat": 35.6595,
        "lon": 139.7005,
        "description": "세계적으로 유명한 교차로. 쇼핑과 식사에 적합.",
        "category": "쇼핑",
        "image": "https://upload.wikimedia.org/wikipedia/commons/5/54/Shibuya_Crossing.jpg",
        "time": "저녁~밤",
        "transport": "시부야 역 앞",
        "map_link": "https://www.google.com/maps/dir/?api=1&destination=Shibuya+Crossing",
        "video": "https://www.youtube.com/watch?v=9QdIcZQ5b1s"
    },
    {
        "name": "우에노 공원",
        "lat": 35.7156,
        "lon": 139.7745,
        "description": "넓은 공원과 박물관, 여유로운 산책 추천.",
        "category": "공원",
        "image": "https://upload.wikimedia.org/wikipedia/commons/6/64/Ueno_Park.jpg",
        "time": "오전~오후",
        "transport": "우에노 역 도보 5분",
        "map_link": "https://www.google.com/maps/dir/?api=1&destination=Ueno+Park",
        "video": "https://www.youtube.com/watch?v=efgh5678"
    },
    {
        "name": "하라주쿠 타케시타 거리",
        "lat": 35.6702,
        "lon": 139.7020,
        "description": "젊은이들의 패션과 간식 거리.",
        "category": "쇼핑",
        "image": "https://upload.wikimedia.org/wikipedia/commons/3/32/Takeshita_Street.jpg",
        "time": "오전~이른 오후",
        "transport": "하라주쿠 역 도보 1분",
        "map_link": "https://www.google.com/maps/dir/?api=1&destination=Takeshita+Street",
        "video": "https://www.youtube.com/watch?v=abcd1234"
    },
]

# 관광지 카테고리 필터
categories = sorted(set([s['category'] for s in tourist_spots]))
selected_category = st.selectbox("🔍 관광지 종류로 보기", ["전체"] + categories)

filtered_spots = tourist_spots if selected_category == "전체" else [
    s for s in tourist_spots if s["category"] == selected_category
]

# 지도 출력
center = [35.6762, 139.6503]
m = folium.Map(location=center, zoom_start=12)

for spot in filtered_spots:
    html = f"""
    <h4>{spot['name']}</h4>
    <img src="{spot['image']}" width="200"><br>
    <b>카테고리:</b> {spot['category']}<br>
    <b>추천 시간:</b> {spot['time']}<br>
    <b>교통:</b> {spot['transport']}<br>
    <a href="{spot['map_link']}" target="_blank">📍 길찾기</a><br>
    <a href="{spot['video']}" target="_blank">▶ 유튜브 보기</a>
    """
    iframe = IFrame(html, 250, 300)
    folium.Marker(
        location=[spot["lat"], spot["lon"]],
        popup=folium.Popup(iframe),
        tooltip=spot["name"],
        icon=folium.Icon(color="green", icon="info-sign")
    ).add_to(m)

col1, col2 = st.columns([3, 1])
with col1:
    st.subheader("🗺️ 관광지 지도")
    st_folium(m, width=700, height=500)

with col2:
    st.subheader("🌤 도쿄 날씨")
    st.write("👉 [도쿄 7일 예보 보러가기](https://weather.com/weather/tenday/l/Tokyo+Japan)")

# 관광지 설명
st.subheader("📍 관광지 설명")
for spot in filtered_spots:
    st.markdown(f"### {spot['name']}")
    st.image(spot["image"], use_column_width=True)
    st.markdown(f"**카테고리:** {spot['category']}  \n**시간:** {spot['time']}  \n**교통:** {spot['transport']}")
    st.write(spot["description"])
    st.markdown(f"[📍 길찾기]({spot['map_link']}) | [▶ 유튜브]({spot['video']})", unsafe_allow_html=True)
    st.markdown("---")

# 예산 계산기
st.subheader("💰 예산 계산기 (선택 항목별)")
with st.form("budget"):
    selected_items = st.multiselect(
        "체험할 항목 선택", [s["name"] for s in tourist_spots], default=[]
    )
    transport = st.number_input("하루 교통비", value=1000)
    food = st.number_input("하루 식비", value=2000)
    extra = st.number_input("기타 경비", value=1000)
    total = 0
    spot_costs = {name: st.number_input(f"{name} 입장료", value=1000) for name in selected_items}
    if st.form_submit_button("총 예산 계산"):
        total = sum(spot_costs.values()) + transport + food + extra
        st.success(f"총 예산: ¥{total:,} 엔")
