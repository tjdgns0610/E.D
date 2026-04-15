import streamlit as st
import pandas as pd
import requests
import json
import random

# ==========================================
# [Backend] 1. 기상청 API 연동 및 데이터 처리
# ==========================================
def get_current_weather():
    return 26.5  # 현재 기온 26.5도 가정

# ==========================================
# [Backend] 2. AI 추천 및 필터링 로직
# ==========================================
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
# [Frontend] 3. 앱 화면 구성 (Streamlit)
# ==========================================
def main():
    st.set_page_config(page_title="AI 스마트 옷장", layout="wide")
    
    st.title("👗 AI 스마트 옷장 & 다이렉트 샵")
    temp = get_current_weather()
    st.subheader(f"현재 화순군 기온: {temp}°C | ☀️ 오늘은 시원한 코디가 좋겠네요!")

    # 민경 님의 진짜 옷 데이터 (빈칸 들여쓰기 완벽 적용 완료!)
    closet_data = {
        'category': ['상의', '하의', '아우터', '하의', '상의'],
        'name': ['검정색 무지 맨투맨', '회색 조거팬츠', '바람막이 자켓', '연청 데님', '스트라이프 셔츠'],
        'thickness': [2, 2, 1, 2, 1],
        'color': ['Black', 'Gray', 'Black', 'Light Blue', 'Navy']
    }
    df_closet = pd.DataFrame(closet_data)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.write("### ✨ 오늘의 AI 추천 코디")
        recommendations = recommend_logic(df_closet, temp)
        
        if recommendations is not None:
            top_pick = recommendations.iloc[0]
            st.info(f"**추천 1위 (매칭 점수: {top_pick['score']}점)**")
            st.success(f"상 의: {top_pick['name_top']} ({top_pick['color_top']})")
            st.success(f"하 의: {top_pick['name_bottom']} ({top_pick['color_bottom']})")
        else:
            st.warning("현재 날씨에 맞는 옷이 옷장에 부족합니다!")

    with col2:
        st.write("### 🛍️ 다이렉트 샵 (추천 아이템)")
        st.write("오늘 코디에 어울리는 아이템을 알리바바 공식 스토어에서 찾아왔어요.")
        st.image("https://via.placeholder.com/150", caption="화이트 레더 스니커즈 (소싱가: 15,000원)")
        if st.button("장바구니 담기"):
            st.toast("아이템이 담겼습니다!")

    st.divider()
    st.write("### 📊 내 옷장 데이터 분석")
    color_counts = df_closet['color'].value_counts()
    st.bar_chart(color_counts)
    st.caption("내 옷장에 가장 많은 색상은 무엇일까요?")

if __name__ == "__main__":
    main()
