import streamlit as st
import folium
from streamlit_folium import st_folium
from folium import IFrame

# 페이지 기본 설정
st.set_page_config(page_title="도쿄 관광 가이드", layout="wide")
st.title("🇯🇵 도쿄 주요 관광지 가이드")
st.markdown("도쿄의 명소를 지도와 함께 살펴보고, 추천 일정과 방문 팁도 확인해보세요!")

# 관광지 데이터
tourist_spots = [
    {
        "name": "도쿄 타워",
        "lat": 35.6586,
        "lon": 139.7454,
        "description": "도쿄의 상징적인 랜드마크로, 전망대에서 야경이 특히 아름답습니다.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/e/e5/Tokyo_Tower_and_around_Skyscrapers.jpg",
        "time": "일몰 후~밤 9시",
        "transport": "도에이 오에도선 '아카반바시 역' 도보 5분"
    },
    {
        "name": "센소지",
        "lat": 35.7148,
        "lon": 139.7967,
        "description": "도쿄에서 가장 오래된 절로, 전통적인 분위기와 쇼핑을 동시에 즐길 수 있습니다.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/f/f0/Sensoji_-_Thunder_Gate_-_2020.jpg",
        "time": "오전 9시~오후 5시",
        "transport": "지하철 긴자선 '아사쿠사 역' 도보 2분"
    },
    {
        "name": "시부야 스크램블 교차로",
        "lat": 35.6595,
        "lon": 139.7005,
        "description": "수백 명의 사람들이 동시에 건너는 도쿄의 상징적인 거리 풍경입니다.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/5/54/Shibuya_Crossing.jpg",
        "time": "해 질 무렵 ~ 밤",
        "transport": "JR 야마노테선 '시부야 역' 바로 앞"
    },
    {
        "name": "메이지 신궁",
        "lat": 35.6764,
        "lon": 139.6993,
        "description": "도심 속 숲에 둘러싸인 조용한 신사로, 산책과 참배에 적합한 장소입니다.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/2/2f/Meiji_Shrine_main_building.JPG",
        "time": "아침 일찍 ~ 정오",
        "transport": "JR 야마노테선 '하라주쿠 역' 도보 2분"
    },
    {
        "name": "도쿄 스카이트리",
        "lat": 35.7100,
        "lon": 139.8107,
        "description": "일본에서 가장 높은 전망대로, 도쿄 전경을 한눈에 볼 수 있습니다.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/f/f2/Tokyo_Skytree_2014_%28cropped%29.jpg",
        "time": "오후 4시~일몰 이후",
        "transport": "도쿄 스카이트리역 도보 1분"
    },
]

# 지도 생성
tokyo_center = [35.6762, 139.6503]
m = folium.Map(location=tokyo_center, zoom_start=12)

# 마커 추가
for spot in tourist_spots:
    html = f"""
    <h4>{spot['name']}</h4>
    <img src="{spot['image']}" width="200"><br>
    <b>추천 시간:</b> {spot['time']}<br>
    <b>교통:</b> {spot['transport']}<br>
    <p>{spot['description']}</p>
    """
    iframe = IFrame(html, width=250, height=300)
    popup = folium.Popup(iframe, max_width=250)
    folium.Marker(
        location=[spot["lat"], spot["lon"]],
        popup=popup,
        tooltip=spot["name"],
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)

# 지도 출력
st.subheader("🗺️ 도쿄 관광지 위치 지도")
st_data = st_folium(m, width=800, height=500)

# 관광지 목록과 설명
st.subheader("📌 관광지 상세 가이드")
for spot in tourist_spots:
    st.markdown(f"### {spot['name']}")
    st.image(spot["image"], use_column_width=True)
    st.markdown(f"**추천 방문 시간:** {spot['time']}")
    st.markdown(f"**대중교통:** {spot['transport']}")
    st.write(spot["description"])
    st.markdown("---")

# 추천 일정
st.subheader("📅 추천 1일 여행 코스 예시")
st.markdown("""
- **오전:** 메이지 신궁 → 시부야 스크램블 교차로  
- **점심:** 시부야 근처 라멘 또는 회전초밥  
- **오후:** 센소지와 나카미세 거리 산책  
- **저녁:** 도쿄 타워 전망대 또는 도쿄 스카이트리 야경 감상  
""")
