import streamlit as st
import pandas as pd
import random
import time

# --- 1. 앱 기본 설정 & UI CSS ---
st.set_page_config(page_title="E.D - 스마트 옷장", page_icon="⬛", layout="wide")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .ed-title {
        font-size: 80px !important;
        font-weight: 900;
        text-align: center;
        margin-bottom: -20px;
        letter-spacing: -5px;
    }
    
    .stButton > button {
        border-radius: 30px;
        height: 60px;
        font-size: 16px;
        font-weight: bold;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        border-color: black;
        color: black;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. 상태 관리 ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_page' not in st.session_state:
    st.session_state.current_page = '홈'

if 'closet_df' not in st.session_state:
    st.session_state.closet_df = pd.DataFrame({
        'category': ['상의', '하의', '아우터', '하의', '상의', '신발'],
        'name': ['블랙 오버핏 맨투맨', '그레이 조거팬츠', '경량 바람막이', '와이드 흑청 데님', '화이트 무지 반팔', '나이키 에어포스'],
        'thickness': [2, 2, 1, 2, 1, 2],
        'color': ['Black', 'Gray', 'Black', 'Black', 'White', 'White']
    })

# --- 3. 로직 함수 ---
def get_current_weather():
    return 26.5

def recommend_logic(closet_df, temp):
    if temp >= 25:
        filtered = closet_df[closet_df['thickness'] == 1]
    elif temp <= 10:
        filtered = closet_df[closet_df['thickness'] == 3]
    else:
        filtered = closet_df[closet_df['thickness'] == 2]
    
    tops = filtered[filtered['category'] == '상의']
    bottoms = filtered[filtered['category'] == '하의']
    shoes = closet_df[closet_df['category'] == '신발'] 
    
    if tops.empty or bottoms.empty:
        return None
    
    combos = tops.merge(bottoms, how='cross', suffixes=('_top', '_bottom'))
    
    if not shoes.empty:
        shoe_pick = shoes.sample(n=1).iloc[0]
        combos['name_shoe'] = shoe_pick['name']
        combos['color_shoe'] = shoe_pick['color']
    else:
        combos['name_shoe'] = "기본 스니커즈"
        combos['color_shoe'] = "White"

    combos['score'] = [random.randint(85, 99) for _ in range(len(combos))]
    return combos.sort_values(by='score', ascending=False)

# --- 4. 로그인 화면 ---
def login_screen():
    st.write("<br><br><br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<p class='ed-title'>E.D</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:gray; margin-bottom: 50px;'>Every Day, Every Dress.</p>", unsafe_allow_html=True)
        with st.container(border=True):
            st.write("#### 🔒 간편 로그인")
            if st.button("🌐 Google 계정으로 1초 만에 시작", type="primary", use_container_width=True):
                st.session_state.logged_in = True
                st.rerun()

# --- 5. 메인 앱 화면 ---
def main_app():
    # [상단 헤더 영역] 어느 페이지에 있든 로고가 작게 보이도록 디테일 추가
    st.markdown("<h2 style='text-align: center; margin-top: -20px;'>E.D</h2>", unsafe_allow_html=True)
    
    if st.session_state.current_page == '홈':
        st.write("#### 👋 안녕하세요, 민경 님!")
        st.caption("민경 님의 완벽한 하루를 위해 준비한 투데이 픽입니다.")
        temp = get_current_weather()
        recommendations = recommend_logic(st.session_state.closet_df, temp)
        
        if recommendations is not None:
            top_pick = recommendations.iloc[0]
            with st.container(border=True):
                st.metric("✨ Perfect Match Score", f"{top_pick['score']} / 100", "현재 화순군 날씨에 최적화됨")
                st.write(f"👕 **상의:** {top_pick['name_top']} ({top_pick['color_top']})")
                st.write(f"👖 **하의:** {top_pick['name_bottom']} ({top_pick['color_bottom']})")
                st.write(f"👟 **신발:** {top_pick['name_shoe']} ({top_pick['color_shoe']})")
        else:
            st.warning("옷이 부족합니다. 새 옷을 등록해주세요!")
            
        st.write("---")
        st.write("#### 🖤 E.D x 무신사 추천")
        with st.container(border=True):
            st.image("https://image.msscdn.net/mfile_s01/2021/08/26/104111/1418701.jpg", caption="[무신사 스탠다드] 릴렉스 핏 반팔 티셔츠")
            st.link_button("무신사에서 바로 구매하기 🛒", url="https://www.musinsa.com", type="primary", use_container_width=True)

    elif st.session_state.current_page == '날씨':
        st.write("#### ⛅ 시간대별 날씨 브리핑")
        temp = get_current_weather()
        
        col_w1, col_w2, col_w3 = st.columns(3)
        col_w1.metric("📍 화순군 기온", f"{temp} °C", "어제보다 2°C 높음")
        col_w2.metric("💧 강수 확률", "0 %")
        col_w3.metric("😷 미세먼지", "좋음")
        
        # [NEW!] 시간대별 기온 그래프 디테일 추가
        st.write("##### 📈 오늘 하루 기온 변화")
        weather_data = pd.DataFrame({
            '시간': ['09:00', '12:00', '15:00', '18:00', '21:00'],
            '기온(°C)': [18, 24, 26.5, 22, 19]
        }).set_index('시간')
        st.area_chart(weather_data)
        
        st.info("💡 **E.D 코멘트:** 낮에는 덥지만 저녁에는 쌀쌀해집니다. 가벼운 아우터를 하나 챙기시는 것을 권장합니다.")

    elif st.session_state.current_page == '옷장':
        st.write("#### 🗄️ 내 옷장 데이터베이스")
        st.caption(f"현재 총 {len(st.session_state.closet_df)}개의 아이템이 등록되어 있습니다.")
        
        # [NEW!] 옷장 요약 디테일
        col_stat1, col_stat2 = st.columns(2)
        with col_stat1:
            st.write("**카테고리별 비중**")
            st.bar_chart(st.session_state.closet_df['category'].value_counts())
        with col_stat2:
            st.write("**컬러별 비중**")
            st.bar_chart(st.session_state.closet_df['color'].value_counts())
            
        st.dataframe(st.session_state.closet_df, use_container_width=True, hide_index=True)

    elif st.session_state.current_page == '등록':
        st.write("#### 📸 새 아이템 등록하기")
        upload_mode = st.radio("업로드 방식", ["카메라", "갤러리"], horizontal=True)
        if upload_mode == "카메라":
            uploaded_image = st.camera_input("카메라 실행")
        else:
            uploaded_image = st.file_uploader("사진 업로드", type=['png', 'jpg'])

        if uploaded_image is not None:
            st.image(uploaded_image, width=200)
            with st.form("add_item_form", border=True):
                new_name = st.text_input("아이템 애칭", "새로 산 옷")
                new_category = st.selectbox("카테고리", ["상의", "하의", "아우터", "신발", "액세서리"])
                new_color = st.selectbox("메인 색상", ["White", "Black", "Gray", "Navy", "Beige"])
                new_thick = st.slider("두께감 (1:여름, 3:겨울)", 1, 3, 2)
                if st.form_submit_button("저장하기", type="primary", use_container_width=True):
                    new_item = pd.DataFrame({'category': [new_category], 'name': [new_name], 'thickness': [new_thick], 'color': [new_color]})
                    st.session_state.closet_df = pd.concat([st.session_state.closet_df, new_item], ignore_index=True)
                    st.success("등록 완료!")

    # --- 하단 네비게이션 바 ---
    st.write("<br><br><br>", unsafe_allow_html=True) 
    st.divider()
    col_nav1, col_nav2, col_nav3, col_nav4 = st.columns(4)
    with col_nav1:
        if st.button("🏠 홈", use_container_width=True):
            st.session_state.current_page = '홈'
            st.rerun()
    with col_nav2:
        if st.button("⛅ 날씨", use_container_width=True):
            st.session_state.current_page = '날씨'
            st.rerun()
    with col_nav3:
        if st.button("🗄️ 옷장", use_container_width=True):
            st.session_state.current_page = '옷장'
            st.rerun()
    with col_nav4:
        if st.button("📸 등록", use_container_width=True):
            st.session_state.current_page = '등록'
            st.rerun()

# --- 6. 앱 시작 ---
if st.session_state.logged_in:
    main_app()
else:
    login_screen()
