import streamlit as st
import pandas as pd

# 페이지 설정: 와이드 모드로 설정
st.set_page_config(layout="wide")

# Load the Excel file
file_path = '물건리스트.xlsx'
df = pd.read_excel(file_path)

# Streamlit app
st.title("성공가도 경매 물건 리스트")

# 데이터 상위 100개 미리보기
st.write("전체 데이터 상위 100개 미리보기:")
st.dataframe(df.head(100))

# Sidebar inputs for filtering
st.sidebar.header("검색 조건")
type = st.sidebar.selectbox("종류", options=["아파트", "다세대/빌라", "오피스텔", "상업용기타", "주택", "근린주택", "다가구 주택", "근린상가", "근린시설"])
region = st.sidebar.selectbox("지역", options=["서울", "경기", "인천"])



# 선택한 "지역"에 따라 "시/구" 필터링
region_filtered_df = df[df['지역'] == region]  # "지역" 열을 기준으로 필터링
region1_options = sorted(region_filtered_df['시/구'].dropna().unique())  # "시/구" 값 정렬

# "시/구" 선택 박스 생성
region1 = st.sidebar.selectbox("시/구를 선택하세요", region1_options)


# 선택한 "지역"에 따라 "구/동" 필터링
region1_filtered_df = df[df['시/구'] == region1]  # "시/구" 열을 기준으로 필터링
region2_options = ["전체"] + sorted(region1_filtered_df['구/동'].dropna().unique())  # "구/동" 값 정렬

# "구/동" 선택 박스 생성
region2 = st.sidebar.selectbox("구/동를 선택하세요", region2_options)


# 인수액 필터링 조건 설정
options = st.sidebar.multiselect("인수액 조건", options=["인수액 : 없음", "임차인현황 자료가 없습니다."])

# 데이터 검색 버튼
if st.sidebar.button("데이터 검색"):
    # 조건을 동적으로 구성하여 입력된 값에 맞게 필터링
    filtered_data = df[
        (df["종류"].astype(str).str.contains(type, case=False, na=False)) &
        (df["지역"].astype(str).str.contains(region, case=False, na=False)) &
        (df["시/구"].astype(str).str.contains(region1, case=False, na=False)) &
        ((True if region2 == "전체" else df["구/동"].astype(str).str.contains(region2, case=False, na=False))) &
        ((True if not options else df["인수액"].isin(options)))  # 추가 텍스트 조건에 맞는 경우
    ]

    # 필터링된 데이터 표시
    st.header("인수액이 없는 경매 물건 리스트")
    st.dataframe(filtered_data)

    # 필터링된 데이터의 행 수 출력
    st.write(f"검색된 물건 개수: {filtered_data.shape[0]}개")

else:
    st.write("검색 조건을 설정하고 '데이터 검색' 버튼을 눌러주세요.")
