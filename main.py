import streamlit as st
import folium
from streamlit_folium import st_folium
from folium import IFrame

# 관광지 데이터
tourist_spots = [
    {
        "name": "도쿄 타워",
        "lat": 35.6586,
        "lon": 139.7454,
        "description": "도쿄의 상징적 랜드마크. 전망대에서 멋진 야경을 감상할 수 있어요.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/e/e5/Tokyo_Tower_and_around_Skyscrapers.jpg",
        "time": "일몰 후~밤 9시",
        "transport": "도에이 오에도선 '아카반바시 역' 도보 5분",
        "map_link": "https://www.google.com/maps/dir/?api=1&destination=Tokyo+Tower",
        "video": "https://www.youtube.com/watch?v=lBSkLjjViRI"
    },
    {
        "name": "센소지",
        "lat": 35.7148,
        "lon": 139.7967,
        "description": "도쿄에서 가장 오래된 사찰. 가미나리문과 전통 쇼핑거리도 유명합니다.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/f/f0/Sensoji_-_Thunder_Gate_-_2020.jpg",
        "time": "오전 9시~오후 5시",
        "transport": "지하철 긴자선 '아사쿠사 역' 도보 2분",
        "map_link": "https://www.google.com/maps/dir/?api=1&destination=Sensoji+Temple",
        "video": "https://www.youtube.com/watch?v=psWfPoyDwKk"
    },
    {
        "name": "시부야 스크램블",
        "lat": 35.6595,
        "lon": 139.7005,
        "description": "세계에서 가장 유명한 교차로. 인파 속을 걷는 체험은 잊지 못할 순간이에요.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/5/54/Shibuya_Crossing.jpg",
        "time": "해 질 무렵 ~ 밤",
        "transport": "JR 야마노테선 '시부야 역' 바로 앞",
        "map_link": "https://www.google.com/maps/dir/?api=1&destination=Shibuya+Crossing",
        "video": "https://www.youtube.com/watch?v=9QdIcZQ5b1s"
    },
    {
        "name": "메이지 신궁",
        "lat": 35.6764,
        "lon": 139.6993,
        "description": "도심 속 자연 속 고요한 신사. 산책로가 매력적입니다.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/2/2f/Meiji_Shrine_main_building.JPG",
        "time": "아침 일찍 ~ 정오",
        "transport": "JR 야마노테선 '하라주쿠 역' 도보 2분",
        "map_link": "https://www.google.com/maps/dir/?api=1&destination=Meiji+Shrine",
        "video": "https://www.youtube.com/watch?v=3hdmnCdjUuM"
    },
    {
        "name": "도쿄 스카이트리",
        "lat": 35.7100,
        "lon": 139.8107,
        "description": "일본에서 가장 높은 전망대. 주변에 쇼핑몰과 수족관도 있어요.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/f/f2/Tokyo_Skytree_2014_%28cropped%29.jpg",
        "time": "오후 4시~야경 시간",
        "transport": "도쿄 스카이트리역 도보 1분",
        "map_link": "https://www.google.com/maps/dir/?api=1&destination=Tokyo+Skytree",
        "video": "https://www.youtube.com/watch?v=lIJ8q9t5W3A"
    },
]

# 페이지 구성
st.set_page_config(page_title="도쿄 관광 가이드", layout="wide")
st.title("🇯🇵 도쿄 관광 가이드")
st.markdown("지도, 일정, 유튜브 영상, 길찾기 링크와 함께 도쿄 여행을 준비해보세요!")

# 지도 생성
tokyo_center = [35.6762, 139.6503]
m = folium.Map(location=tokyo_center, zoom_start=12)

# 마커 생성
for spot in tourist_spots:
    html = f"""
    <h4>{spot['name']}</h4>
    <img src="{spot['image']}" width="200"><br>
    <b>추천 시간:</b> {spot['time']}<br>
    <b>교통:</b> {spot['transport']}<br>
    <a href="{spot['map_link']}" target="_blank">📍 길찾기(Google Maps)</a><br>
    <a href="{spot['video']}" target="_blank">▶ 유튜브 영상 보기</a>
    """
    iframe = IFrame(html, width=250, height=300)
    popup = folium.Popup(iframe, max_width=250)
    folium.Marker(
        location=[spot["lat"], spot["lon"]],
        popup=popup,
        tooltip=spot["name"],
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(m)

st.subheader("🗺️ 관광지 지도")
st_folium(m, width=800, height=500)

# 관광지 설명
st.subheader("📌 관광지 상세 정보")
for spot in tourist_spots:
    st.markdown(f"### {spot['name']}")
    st.image(spot["image"], use_column_width=True)
    st.markdown(f"**추천 시간:** {spot['time']}")
    st.markdown(f"**교통:** {spot['transport']}")
    st.write(spot["description"])
    st.markdown(f"[📍 길찾기(Google Maps)]({spot['map_link']}) &nbsp;&nbsp;&nbsp; [▶ 유튜브 영상]({spot['video']})", unsafe_allow_html=True)
    st.markdown("---")

# 추천 일정
st.subheader("📅 도쿄 1일 추천 일정")
st.markdown("""
**오전:** 메이지 신궁 → 시부야 스크램블  
**점심:** 시부야에서 식사  
**오후:** 센소지와 아사쿠사 거리  
**저녁:** 도쿄 타워 또는 스카이트리 야경 감상
""")

# 💰 예산 계산기
st.subheader("💰 여행 예산 계산기 (엔 단위)")
with st.form("budget_form"):
    tower = st.number_input("도쿄 타워 입장료 (예: 1200)", min_value=0, value=1200)
    skytree = st.number_input("도쿄 스카이트리 전망대 (예: 2100)", min_value=0, value=2100)
    transport = st.number_input("하루 교통비 (예: 1000)", min_value=0, value=1000)
    food = st.number_input("식비 (예: 2000)", min_value=0, value=2000)
    others = st.number_input("기타 (예: 1000)", min_value=0, value=1000)
    submit = st.form_submit_button("총액 계산")

if submit:
    total = tower + skytree + transport + food + others
    st.success(f"총 예상 예산: ¥{total:,} 엔")

