import streamlit as st
import pandas as pd
import random
import time

st.set_page_config(page_title="AI 스마트 옷장", page_icon="👗", layout="wide")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'closet_df' not in st.session_state:
    st.session_state.closet_df = pd.DataFrame({
        'category': ['상의', '하의', '아우터', '하의', '상의', '신발'],
        'name': ['블랙 맨투맨', '그레이 조거팬츠', '바람막이', '연청 데님', '스트라이프 셔츠', '컨버스 블랙'],
        'thickness': [2, 2, 1, 2, 1, 2],
        'color': ['Black', 'Gray', 'Black', 'Light Blue', 'Navy', 'Black']
    })

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

def login_screen():
    st.write("<br><br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.title("👗 Style AI")
        st.write("당신의 날씨, 당신의 핏. 완벽한 하루를 위한 스타일링.")
        st.divider()
        with st.container(border=True):
            st.write("#### 🔒 간편 로그인")
            st.text_input("이메일 주소", placeholder="example@gmail.com")
            st.text_input("비밀번호", type="password", placeholder="••••••••")
            if st.button("앱 시작하기 🚀", type="primary", use_container_width=True):
                st.session_state.logged_in = True
                st.rerun()
            st.write("---")
            if st.button("🌐 Google 계정으로 1초 만에 시작", use_container_width=True):
                st.session_state.logged_in = True
                st.rerun()

def main_app():
    with st.sidebar:
        st.header("민경 님의 스타일룸")
        st.write("✨ 프리미엄 멤버십")
        st.divider()
        if st.button("로그아웃 🚪", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

    temp = get_current_weather()
    col_w1, col_w2, col_w3 = st.columns(3)
    col_w1.metric("📍 현재 기온", f"{temp} °C")
    col_w2.metric("💧 강수 확률", "0 %")
    col_w3.metric("😷 미세먼지", "좋음")
    st.write("---")

    tab1, tab2, tab3 = st.tabs(["🏠 홈 (투데이 픽)", "📸 옷장 채우기", "🗄️ 내 옷장 관리"])

    with tab1:
        col1, col2 = st.columns([1.5, 1.2])
        with col1:
            st.subheader("✨ AI 추천 OOTD")
            recommendations = recommend_logic(st.session_state.closet_df, temp)
            if recommendations is not None:
                top_pick = recommendations.iloc[0]
                with st.container(border=True):
                    st.metric("Perfect Match Score", f"{top_pick['score']} / 100")
                    st.write(f"👕 **[상의]** {top_pick['name_top']} ({top_pick['color_top']})")
                    st.write(f"👖 **[하의]** {top_pick['name_bottom']} ({top_pick['color_bottom']})")
                    st.write(f"👟 **[신발]** {top_pick['name_shoe']} ({top_pick['color_shoe']})")
            else:
                st.warning("옷이 부족합니다.")
        with col2:
            st.subheader("🛍️ 쇼핑 추천")
            with st.container(border=True):
                st.write("**[소싱 제안] 썸머 라이트 볼캡**")
                if st.button("앱에서 바로 구매 (12,900원) 🛒", type="primary", use_container_width=True):
                    st.toast("장바구니에 담겼습니다!")

    with tab2:
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
                new_color = st.selectbox("메인 색상", ["White", "Black", "Gray", "Navy", "Beige", "Blue", "Red"])
                new_thick = st.slider("두께감 (1:여름용, 2:사계절, 3:겨울용)", 1, 3, 2)
                if st.form_submit_button("내 옷장에 쏙! 저장하기", type="primary", use_container_width=True):
                    new_item = pd.DataFrame({'category': [new_category], 'name': [new_name], 'thickness': [new_thick], 'color': [new_color]})
                    st.session_state.closet_df = pd.concat([st.session_state.closet_df, new_item], ignore_index=True)
                    st.success("등록 완료!")

    with tab3:
        st.subheader("🗄️ 내 옷장 데이터베이스")
        st.dataframe(st.session_state.closet_df, use_container_width=True, hide_index=True)

if st.session_state.logged_in:
    main_app()
else:
    login_screen()
