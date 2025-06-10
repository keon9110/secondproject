import streamlit as st
import folium
from streamlit_folium import st_folium

# 관광지 정보 리스트
tourist_spots = [
    {
        "name": "시드니 오페라 하우스",
        "location": [-33.8568, 151.2153],
        "description": "시드니의 아이콘인 오페라 하우스는 세계적으로 유명한 공연 예술 센터입니다. 유니크한 디자인과 항구 전망이 매력입니다.",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/3/3e/Sydney_Opera_House_-_Dec_2008.jpg"
    },
    {
        "name": "그레이트 배리어 리프",
        "location": [-18.2871, 147.6992],
        "description": "세계 최대 산호초 지대로, 다이빙과 스노클링의 성지입니다. 유네스코 세계유산에도 등재되어 있어요.",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/6/6e/Great_Barrier_Reef_-_Flickr_-_eutrophication_%26_hypoxia_%281%29.jpg"
    },
    {
        "name": "울룰루 (에어즈 록)",
        "location": [-25.3444, 131.0369],
        "description": "호주의 붉은 심장부에 위치한 거대한 바위산으로, 원주민 문화의 성지이자 장엄한 일몰로 유명합니다.",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/f/f0/Uluru_Ayers_Rock_Red_Centre_Australia.jpg"
    },
    {
        "name": "멜버른",
        "location": [-37.8136, 144.9631],
        "description": "예술과 커피의 도시 멜버른은 세련된 골목길, 트램 문화, 그리고 다양한 축제로 유명합니다.",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/2/2e/Melbourne_City_Skyline_Australia.jpg"
    },
    {
        "name": "타즈마니아 크레이들 마운틴",
        "location": [-41.6836, 145.9378],
        "description": "웅장한 산과 맑은 호수, 다양한 야생동물을 만날 수 있는 트레킹 명소입니다.",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/6/6e/Cradle_Mountain_-_November_2007.jpg"
    },
    {
        "name": "골드 코스트",
        "location": [-28.0167, 153.4000],
        "description": "반짝이는 해변과 끝없는 서핑 파도, 테마파크로 가득한 가족 여행 명소입니다.",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/8/8d/Gold_Coast_Q1_building.jpg"
    }
]

st.set_page_config(page_title="호주 관광 가이드", layout="wide")
st.title("🇦🇺 호주의 주요 관광지 가이드")
st.write("호주의 아름답고 다양한 관광 명소를 소개합니다. 지도를 클릭하거나 아래 설명을 확인해보세요!")

# Folium 지도 생성
m = folium.Map(location=[-25.0, 133.0], zoom_start=4)

# 마커 추가
for spot in tourist_spots:
    popup_html = f"""
    <b>{spot['name']}</b><br>
    <img src="{spot['image_url']}" width="200"><br>
    <p>{spot['description']}</p>
    """
    folium.Marker(
        location=spot['location'],
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=spot['name'],
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)

# Folium 지도 출력
st.subheader("📍 관광지 위치 지도")
st_data = st_folium(m, width=1000, height=600)

# 관광지 설명
st.subheader("🌟 상세 가이드")
for spot in tourist_spots:
    st.markdown(f"### {spot['name']}")
    st.image(spot["image_url"], width=600)
    st.write(spot["description"])
    st.markdown("---")
