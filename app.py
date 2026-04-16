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
    
    /* E.D 타이틀 로고 */
    .ed-title {
        font-size: 80px !important;
        font-weight: 900;
        text-align: center;
        margin-bottom: -20px;
        letter-spacing: -5px;
    }
    
    /* 하단 버튼을 동그랗고 예쁘게 만드는 CSS */
    .stButton > button {
        border-radius: 30px; /* 버튼을 둥글게 */
        height: 60px;
        font-size: 16px;
        font-weight: bold;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px); /* 마우스 올리면 살짝 뜸 */
        border-color: black;
        color: black;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. 상태 관리 (데이터 & 페이지 기억) ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# [NEW!] 현재 어떤 화면에 있는지 기억하는 변수
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

# --- 5. 메인 앱 (페이지 라우팅 및 하단 네비게이션) ---
def main_app():
    # 5-1. 현재 선택된 페이지의 내용을 먼저 보여줍니다.
    if st.session_state.current_page == '홈':
        st.subheader("🏠 E.D 투데이 픽")
        temp = get_current_weather()
        recommendations = recommend_logic(st.session_state.closet_df, temp)
        if recommendations is not None:
            top_pick = recommendations.iloc[0]
            with st.container(border=True):
                st.metric("Perfect Match Score", f"{top_pick['score']} / 100")
                st.write(f"👕 **{top_pick['name_top']}**")
                st.write(f"👖 **{top_pick['name_bottom']}**")
                st.write(f"👟 **{top_pick['name_shoe']}**")
        else:
            st.warning("옷이 부족합니다. 새 옷을 등록해주세요!")
            
        st.write("---")
        st.subheader("🖤 무신사 추천 아이템")
        with st.container(border=True):
            st.image("https://image.msscdn.net/mfile_s01/2021/08/26/104111/1418701.jpg", caption="[무신사 스탠다드] 릴렉스 핏 반팔 티셔츠")
            st.link_button("무신사에서 바로 구매하기 🛒", url="https://www.musinsa.com", type="primary", use_container_width=True)

    elif st.session_state.current_page == '날씨':
        st.subheader("⛅ 오늘의 날씨 브리핑")
        temp = get_current_weather()
        col_w1, col_w2, col_w3 = st.columns(3)
        col_w1.metric("📍 화순군 기온", f"{temp} °C", "어제보다 2°C 높음")
        col_w2.metric("💧 강수 확률", "0 %")
        col_w3.metric("😷 미세먼지", "좋음")
        st.info("💡 **E.D 코멘트:** 오늘은 야외 활동하기 좋은 날씨입니다. 가벼운 외투나 반팔을 추천합니다!")

    elif st.session_state.current_page == '옷장':
        st.subheader("🗄️ 내 옷장 데이터베이스")
        st.dataframe(st.session_state.closet_df, use_container_width=True, hide_index=True)

    elif st.session_state.current_page == '등록':
        st.subheader("📸 새 아이템 등록하기")
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
                new_color = st.selectbox("메인 색상", ["White", "Black", "Gray"])
                new_thick = st.slider("두께감 (1:여름, 3:겨울)", 1, 3, 2)
                if st.form_submit_button("저장하기", type="primary", use_container_width=True):
                    new_item = pd.DataFrame({'category': [new_category], 'name': [new_name], 'thickness': [new_thick], 'color': [new_color]})
                    st.session_state.closet_df = pd.concat([st.session_state.closet_df, new_item], ignore_index=True)
                    st.success("등록 완료!")

    # 5-2. 화면 맨 아래에 하단 네비게이션 바(동그란 버튼 4개) 생성
    st.write("<br><br>", unsafe_allow_html=True) # 위 콘텐츠와 간격 띄우기
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
