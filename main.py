import streamlit as st
import folium
from streamlit_folium import st_folium
from folium import IFrame
from datetime import datetime
import pytz

# 도쿄 현재 날짜
tokyo_tz = pytz.timezone('Asia/Tokyo')
today = datetime.now(tokyo_tz).strftime("%Y년 %m월 %d일 (%A)")

# Streamlit 설정
st.set_page_config(page_title="도쿄 여행 가이드", layout="wide")
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url('https://images.unsplash.com/photo-1586500024866-5c8a0fa2185c?auto=format&fit=crop&w=1600&q=80');
        background-size: cover;
        background-attachment: fixed;
    }}
    </style>
    """, unsafe_allow_html=True
)

st.title("🇯🇵 도쿄 여행 가이드")
st.markdown(f"📅 **오늘 날짜 (도쿄 기준)**: {today}")

# 관광지 데이터
tourist_spots = [
    # 전망
    {
        "name": "도쿄 타워", "lat": 35.6586, "lon": 139.7454,
        "description": "도쿄의 클래식 전망 명소.",
        "category": "전망", "image": "https://upload.wikimedia.org/wikipedia/commons/e/e5/Tokyo_Tower_and_around_Skyscrapers.jpg",
        "time": "일몰 후~밤", "transport": "아카반바시 역 도보 5분",
        "map_link": "https://www.google.com/maps/dir/?api=1&destination=Tokyo+Tower",
        "video": "https://www.youtube.com/watch?v=lBSkLjjViRI"
    },
    {
        "name": "도쿄 스카이트리", "lat": 35.7101, "lon": 139.8107,
        "description": "일본에서 가장 높은 전망대.",
        "category": "전망", "image": "https://upload.wikimedia.org/wikipedia/commons/7/7f/Tokyo_Skytree_2014_%28cropped%29.jpg",
        "time": "오전~저녁", "transport": "스카이트리 역 도보 1분",
        "map_link": "https://www.google.com/maps/dir/?api=1&destination=Tokyo+Skytree",
        "video": "https://www.youtube.com/watch?v=MBtNRAgob8M"
    },
    {
        "name": "롯폰기 힐즈 전망대", "lat": 35.6605, "lon": 139.7292,
        "description": "도심 속 고급 전망대.",
        "category": "전망", "image": "https://upload.wikimedia.org/wikipedia/commons/4/45/Roppongi_Hills.jpg",
        "time": "저녁~밤", "transport": "롯폰기 역 도보 3분",
        "map_link": "https://www.google.com/maps/dir/?api=1&destination=Roppongi+Hills",
        "video": "https://www.youtube.com/watch?v=sdV2Kv9oaJE"
    },

    # 문화
    {
        "name": "센소지", "lat": 35.7148, "lon": 139.7967,
        "description": "가장 오래된 불교 사원.",
        "category": "문화", "image": "https://upload.wikimedia.org/wikipedia/commons/f/f0/Sensoji_-_Thunder_Gate_-_2020.jpg",
        "time": "오전~오후", "transport": "아사쿠사 역 도보 2분",
        "map_link": "https://www.google.com/maps/dir/?api=1&destination=Sensoji+Temple",
        "video": "https://www.youtube.com/watch?v=psWfPoyDwKk"
    },
    {
        "name": "메이지 신궁", "lat": 35.6764, "lon": 139.6993,
        "description": "도쿄의 대표 신사.",
        "category": "문화", "image": "https://upload.wikimedia.org/wikipedia/commons/7/7e/Meiji_Shrine_Main_Building.jpg",
        "time": "오전", "transport": "하라주쿠 역 도보 5분",
        "map_link": "https://www.google.com/maps/dir/?api=1&destination=Meiji+Shrine",
        "video": "https://www.youtube.com/watch?v=wZkRZy7Vv4s"
    },
    {
        "name": "에도 도쿄 박물관", "lat": 35.6961, "lon": 139.7966,
        "description": "에도 시대를 체험하는 공간.",
        "category": "문화", "image": "https://upload.wikimedia.org/wikipedia/commons/b/b7/Edo-Tokyo_Museum_2019.jpg",
        "time": "오후", "transport": "료고쿠 역 도보 2분",
        "map_link": "https://www.google.com/maps/dir/?api=1&destination=Edo+Tokyo+Museum",
        "video": "https://www.youtube.com/watch?v=Oy1aZ4W4et8"
    },

    # 쇼핑
    {
        "name": "시부야 스크램블", "lat": 35.6595, "lon": 139.7005,
        "description": "세계에서 가장 붐비는 교차로.",
        "category": "쇼핑", "image": "https://upload.wikimedia.org/wikipedia/commons/5/54/Shibuya_Crossing.jpg",
        "time": "저녁~밤", "transport": "시부야 역",
        "map_link": "https://www.google.com/maps/dir/?api=1&destination=Shibuya+Crossing",
        "video": "https://www.youtube.com/watch?v=9QdIcZQ5b1s"
    },
    {
        "name": "하라주쿠 타케시타 거리", "lat": 35.6702, "lon": 139.7020,
        "description": "젊은이들의 패션 거리.",
        "category": "쇼핑", "image": "https://upload.wikimedia.org/wikipedia/commons/3/32/Takeshita_Street.jpg",
        "time": "오전~오후", "transport": "하라주쿠 역 도보 1분",
        "map_link": "https://www.google.com/maps/dir/?api=1&destination=Takeshita+Street",
        "video": "https://www.youtube.com/watch?v=abcd1234"
    },
    {
        "name": "긴자 쇼핑 거리", "lat": 35.6717, "lon": 139.7650,
        "description": "고급 브랜드 숍 밀집.",
        "category": "쇼핑", "image": "https://upload.wikimedia.org/wikipedia/commons/9/9d/Ginza_Chuo_dori.jpg",
        "time": "오후~저녁", "transport": "긴자 역 도보 3분",
        "map_link": "https://www.google.com/maps/dir/?api=1&destination=Ginza+Shopping",
        "video": "https://www.youtube.com/watch?v=X6VjGZjlX9I"
    },

    # 공원
    {
        "name": "우에노 공원", "lat": 35.7156, "lon": 139.7745,
        "description": "벚꽃 명소, 동물원 포함.",
        "category": "공원", "image": "https://upload.wikimedia.org/wikipedia/commons/6/64/Ueno_Park.jpg",
        "time": "오전~오후", "transport": "우에노 역 도보 5분",
        "map_link": "https://www.google.com/maps/dir/?api=1&destination=Ueno+Park",
        "video": "https://www.youtube.com/watch?v=wYpbD1tqw38"
    },
    {
        "name": "요요기 공원", "lat": 35.6729, "lon": 139.6949,
        "description": "자연과 시민들의 휴식공간.",
        "category": "공원", "image": "https://upload.wikimedia.org/wikipedia/commons/3/3f/Yoyogi_Park.jpg",
        "time": "오전~오후", "transport": "하라주쿠 역 도보 3분",
        "map_link": "https://www.google.com/maps/dir/?api=1&destination=Yoyogi+Park",
        "video": "https://www.youtube.com/watch?v=9rBSmlAOCMQ"
    },
    {
        "name": "신주쿠 교엔", "lat": 35.6852, "lon": 139.7100,
        "description": "일본 정원과 벚꽃 명소.",
        "category": "공원", "image": "https://upload.wikimedia.org/wikipedia/commons/d/d1/Shinjuku_Gyoen_Park.jpg",
        "time": "오전~오후", "transport": "신주쿠 교엔마에 역 도보 3분",
        "map_link": "https://www.google.com/maps/dir/?api=1&destination=Shinjuku+Gyoen",
        "video": "https://www.youtube.com/watch?v=qMQ6CEMNm5Y"
    },

    # 액티비티
    {
        "name": "디즈니랜드", "lat": 35.6329, "lon": 139.8804,
        "description": "도쿄 대표 테마파크.",
        "category": "액티비티", "image": "https://upload.wikimedia.org/wikipedia/commons/f/f5/Tokyo_Disneyland_Cinderella_Castle.jpg",
        "time": "종일", "transport": "마이하마 역 도보 5분",
        "map_link": "https://www.google.com/maps/dir/?api=1&destination=Tokyo+Disneyland",
        "video": "https://www.youtube.com/watch?v=vvoT5B5JH8Y"
    },
    {
        "name": "팀랩 플래닛", "lat": 35.6427, "lon": 139.7966,
        "description": "몰입형 디지털 아트 체험.",
        "category": "액티비티", "image": "https://upload.wikimedia.org/wikipedia/commons/4/4f/Teamlab_planets_tokyo_20180817.jpg",
        "time": "오후~저녁", "transport": "토요스 역 도보 5분",
        "map_link": "https://www.google.com/maps/dir/?api=1&destination=TeamLab+Planets",
        "video": "https://www.youtube.com/watch?v=tMujgZSuhkY"
    },
    {
        "name": "마리오카트 거리질주", "lat": 35.6595, "lon": 139.7005,
        "description": "도쿄 도심을 달리는 고카트 체험.",
        "category": "액티비티", "image": "https://upload.wikimedia.org/wikipedia/commons/8/87/Mario_Kart_Tokyo.jpg",
        "time": "오후~저녁", "transport": "시부야 역", 
        "map_link": "https://www.google.com/maps/dir/?api=1&destination=Shibuya+Street+Kart",
        "video": "https://www.youtube.com/watch?v=0KJ_VZPr7vU"
    },
]

# 필터
categories = sorted(set([s["category"] for s in tourist_spots]))
selected_category = st.selectbox("🔍 관광지 종류로 보기", ["전체"] + categories)
filtered_spots = tourist_spots if selected_category == "전체" else [s for s in tourist_spots if s["category"] == selected_category]

# 지도
m = folium.Map(location=[35.6762, 139.6503], zoom_start=11)
for spot in filtered_spots:
    html = f"""
    <h4>{spot['name']}</h4>
    <img src="{spot['image']}" width="200"><br>
    <b>카테고리:</b> {spot['category']}<br>
    <b>시간:</b> {spot['time']}<br>
    <b>교통:</b> {spot['transport']}<br>
    <a href="{spot['map_link']}" target="_blank">📍 길찾기</a><br>
    <a href="{spot['video']}" target="_blank">▶ 유튜브 보기</a>
    """
    iframe = IFrame(html, 250, 300)
    folium.Marker(
        location=[spot["lat"], spot["lon"]],
        popup=folium.Popup(iframe),
        tooltip=spot["name"],
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)

col1, col2 = st.columns([3, 1])
with col1:
    st.subheader("🗺️ 관광지 지도")
    st_folium(m, width=700, height=500)
with col2:
    st.subheader("🌤 도쿄 날씨")
    st.write("👉 [도쿄 날씨 예보 보러가기](https://weather.com/weather/tenday/l/Tokyo+Japan)")

# 관광지 설명
st.subheader("📍 관광지 상세 설명")
for spot in filtered_spots:
    st.markdown(f"### {spot['name']}")
    st.image(spot["image"], use_column_width=True)
    st.markdown(f"**카테고리:** {spot['category']}  \n**시간:** {spot['time']}  \n**교통:** {spot['transport']}")
    st.write(spot["description"])
    st.markdown(f"[📍 길찾기]({spot['map_link']}) | [▶ 유튜브]({spot['video']})", unsafe_allow_html=True)
    st.markdown("---")

# 예산 계산기
st.subheader("💰 예산 계산기 (체험 선택)")
with st.form("budget"):
    selected_items = st.multiselect("체험할 장소 선택", [s["name"] for s in tourist_spots], default=[])
    transport = st.number_input("교통비 (1일 기준)", value=1000)
    food = st.number_input("식비 (1일 기준)", value=2000)
    extra = st.number_input("기타 비용", value=1000)
    total = 0
    spot_costs = {name: st.number_input(f"{name} 입장료", value=1000) for name in selected_items}
    if st.form_submit_button("총 예산 계산"):
        total = sum(spot_costs.values()) + transport + food + extra
        st.success(f"총 예상 경비: ¥{total:,} 엔")
