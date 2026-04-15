import streamlit as st
import pandas as pd
import random
import time

# ==========================================
# 0. 앱 기본 설정 & 고급 디자인(CSS) 적용
# ==========================================
st.set_page_config(page_title="AI 스마트 옷장", page_icon="👗", layout="wide")

# 실제 앱처럼 보이게 상단 메뉴와 하단 워터마크를 숨기고 디자인을 고급화하는 CSS
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stButton>button {
        border-radius: 20px;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        background-color: #f0f2f6;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 1. 세션 상태 (데이터베이스 & 로그인 유지)
# ==========================================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'closet_df' not in st.session_state:
    st.session_state.closet_df = pd.DataFrame({
        'category': ['상의', '하의', '아우터', '하의', '상의', '신발'],
        'name': ['블랙 오버핏 맨투맨', '그레이 와이드 밴딩팬츠', '미니멀 윈드브레이커', '연청 와이드 데님', '스트라이프 옥스퍼드 셔츠', '컨버스 척테일러 1970s'],
        'thickness': [2, 2, 1, 2, 1, 2],
        'color': ['Black', 'Gray', 'Black', 'Light Blue', 'Navy', 'Black']
    })

# ==========================================
# 2. 핵심 알고리즘 (백엔드)
# ==========================================
def get_current_weather():
    return 26.5  # API 연동 자리 (현재는 26.5도로 고정)

def recommend_logic(closet_df, temp):
    # 날씨 기반 1차 필터링
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
    
    # 2차 조합 (상하의 매칭)
    combos = tops.merge(bottoms, how='cross', suffixes=('_top', '_bottom'))
    
    # 신발 매칭 로직
    if not shoes.empty:
        shoe_pick = shoes.sample(n=1).iloc[0]
        combos['name_shoe'] = shoe_pick['name']
        combos['color_shoe'] = shoe_pick['color']
    else:
        combos['name_shoe'] = "기본 화이트 스니커즈 (추천)"
        combos['color_shoe'] = "White"

    # AI 점수 부여
    combos['score'] = [random.randint(85, 99) for _ in range(len(combos))]
    return combos.sort_values(by='score', ascending=False)

# ==========================================
# 3. 화면 구성: 로그인 페이지
# ==========================================
def login_screen():
    st.write("<br><br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    
    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/3255/3255015.png", width=80)
        st.title("Style AI")
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

# ==========================================
# 4. 화면 구성: 메인 앱 페이지
# ==========================================
def main_app():
    # --- 사이드바 (마이페이지) ---
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/4140/4140048.png", width=80)
        st.header("민경 님의 스타일룸")
        st.write("✨ 프리미엄 멤버십")
        st.write("✓ 체형: 모래시계형 / 핏: 오버핏")
        
        st.divider()
        st.subheader("⚙️ 설정")
        st.checkbox("아침 8시 코디 푸시 알림", value=True)
        st.checkbox("알리바바 핫딜 알림", value=True)
        
        st.write("<br><br>", unsafe_allow_html=True)
        if st.button("로그아웃 🚪", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

    # --- 상단 날씨 대시보드 ---
    temp = get_current_weather()
    col_w1, col_w2, col_w3 = st.columns(3)
    col_w1.metric("📍 현재 화순군", f"{temp} °C", "어제보다 2°C 높음")
    col_w2.metric("💧 강수 확률", "0 %", "외출하기 좋은 날씨!", delta_color="normal")
    col_w3.metric("😷 미세먼지", "좋음", "마
