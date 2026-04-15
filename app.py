import streamlit as st
import pandas as pd
import random
import time  # AI 로딩 화면을 위한 시간 라이브러리

# ==========================================
# 0. 앱의 기억력 설정 (데이터베이스 역할)
# ==========================================
# 앱을 처음 켰을 때만 기본 옷장을 세팅하고, 이후에는 추가된 옷을 기억합니다.
if 'closet_df' not in st.session_state:
    st.session_state.closet_df = pd.DataFrame({
        'category': ['상의', '하의', '아우터', '하의', '상의'],
        'name': ['검정색 무지 맨투맨', '회색 조거팬츠', '바람막이 자켓', '연청 데님', '스트라이프 셔츠'],
        'thickness': [2, 2, 1, 2, 1],
        'color': ['Black', 'Gray', 'Black', 'Light Blue', 'Navy']
    })

# ==========================================
# 1. 백엔드 로직 (API & 추천)
# ==========================================
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
    
    if tops.empty or bottoms.empty:
        return None
    
    combos = tops.merge(bottoms, how='cross', suffixes=('_top', '_bottom'))
    combos['score'] = [random.randint(80, 99) for _ in range(len(combos))]
    return combos.sort_values(by='score', ascending=False)

# ==========================================
# 2. 앱 화면 구성 (프론트엔드)
# ==========================================
def main():
    st.set_page_config(page_title="AI 스마트 옷장", layout="wide")
    st.title("👗 AI 스마트 옷장 & 다이렉트 샵")
    
    # 탭(Tab) 메뉴를 만들어서 화면을 3개로 나눕니다.
    tab1, tab2, tab3 = st.tabs(["🏠 오늘의 코디", "➕ 옷 등록하기", "📊 내 옷장 보기"])

    # ------------------------------------
    # [탭 1] 메인 화면 (추천 & 쇼핑)
    # ------------------------------------
    with tab1:
        temp = get_current_weather()
        st.subheader(f"현재 기온: {temp}°C | ☀️ 오늘은 시원한 코디가 좋겠네요!")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.write("### ✨ AI 추천 코디")
            # 세션 스테이트(기억력)에 있는 옷장 데이터를 가져와서 추천합니다.
            recommendations = recommend_logic(st.session_state.closet_df, temp)
            
            if recommendations is not None:
                top_pick = recommendations.iloc[0]
                st.info(f"**추천 1위 (매칭 점수: {top_pick['score']}점)**")
                st.success(f"상 의: {top_pick['name_top']} ({top_pick['color_top']})")
                st.success(f"하 의: {top_pick['name_bottom']} ({top_pick['color_bottom']})")
            else:
                st.warning("현재 날씨에 맞는 옷이 옷장에 부족합니다! '옷 등록하기' 탭에서 옷을 추가해보세요.")

        with col2:
            st.write("### 🛍️ 다이렉트 샵 추천")
            st.image("https://via.placeholder.com/150", caption="화이트 레더 스니커즈 (15,000원)")
            if st.button("장바구니 담기"):
                st.toast("아이템이 담겼습니다!")

    # ------------------------------------
    # [탭 2] 사진/QR로 옷 등록하기 (신규 기능!)
    # ------------------------------------
    with tab2:
        st.header("📸 내 옷장에 새 옷 넣기")
        st.write("스마트폰 카메라로 옷이나 쇼핑몰 QR코드를 찍어보세요!")
        
        # 입력 방식 선택 (라디오 버튼)
        upload_mode = st.radio("등록 방식 선택", ["사진 촬영하기", "갤러리에서 사진/QR 업로드"])
        
        uploaded_image = None
        if upload_mode == "사진 촬영하기":
            uploaded_image = st.camera_input("카메라로 옷을 찍어주세요")
        else:
            uploaded_image = st.file_uploader("옷 사진이나 QR코드를 올려주세요", type=['png', 'jpg', 'jpeg'])

        # 사진이 올라왔을 때의 작동 로직
        if uploaded_image is not None:
            st.image(uploaded_image, width=300, caption="업로드된 이미지")
            
            # AI 분석하는 척하는 로딩 화면 (실제 서비스에선 여기에 컴퓨터 비전 AI 연결)
            with st.spinner("AI가 옷의 종류와 색상을 분석 중입니다..."):
                time.sleep(2) # 2초 동안 멈춤
                
            st.success("✨ AI 분석 완료! 아래 내용을 확인하고 저장해주세요.")
            
            # 사용자가 데이터를 확인하고 수정할 수 있는 입력 폼
            with st.form("add_clothes_form"):
                st.write("#### 상세 정보 입력")
                # AI가 임의로 추천한 값들을 기본값(value, index)으로 세팅
                new_name = st.text_input("옷 애칭", value="새로 산 화이트 반팔티")
                new_category = st.selectbox("카테고리", ["상의", "하의", "아우터", "신발", "액세서리"], index=0)
                new_color = st.selectbox("메인 색상", ["White", "Black", "Gray", "Navy", "Beige", "Blue"], index=0)
                new_thick = st.slider("두께감 (1:얇음, 2:보통, 3:두꺼움)", 1, 3, 1)
                
                # 등록 버튼
                submit_btn = st.form_submit_button("옷장에 추가하기")
                
                if submit_btn:
                    # 새로운 옷 데이터를 딕셔너리 형태로 만듦
                    new_item = pd.DataFrame({
                        'category': [new_category],
                        'name': [new_name],
                        'thickness': [new_thick],
                        'color': [new_color]
                    })
                    # 기존 옷장 데이터(session_state)에 방금 만든 데이터를 합침
                    st.session_state.closet_df = pd.concat([st.session_state.closet_df, new_item], ignore_index=True)
                    st.success(f"🎉 '{new_name}'이(가) 옷장에 성공적으로 들어갔습니다!")

    # ------------------------------------
    # [탭 3] 내 옷장 전체 보기 & 데이터 분석
    # ------------------------------------
    with tab3:
        st.header("🗄️ 현재 내 옷장")
        # 현재 옷장에 있는 모든 옷을 표(Table) 형태로 보여줌
        st.dataframe(st.session_state.closet_df, use_container_width=True)
        
        st.divider()
        st.write("### 📊 옷장 컬러 통계")
        color_counts = st.session_state.closet_df['color'].value_counts()
        st.bar_chart(color_counts)

if __name__ == "__main__":
    main()
with st.sidebar:
    st.header("⚙️ 내 정보 설정")
    st.write("여기에 내 체형이나 선호 스타일을 미리 입력해둘 수 있습니다.")
    st.button("로그아웃")
with st.expander("👉 기상청 실시간 날씨 데이터 자세히 보기"):
    st.write("현재 풍속: 2.5m/s")
    st.write("오늘 강수 확률: 0%")
    st.write("미세먼지: 좋음")
