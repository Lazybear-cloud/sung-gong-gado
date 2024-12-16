import streamlit as st
import pandas as pd
import math


# 페이지 설정: 와이드 모드로 설정
st.set_page_config(layout="wide")

# Load the Excel file
file_path = '물건리스트.xlsx'
df = pd.read_excel(file_path)

# Streamlit app
st.title("성공가도 경매 물건 리스트📑")

# 데이터 상위 100개 미리보기
st.write("전체 데이터 상위 100개 미리보기:")
st.dataframe(df.head(100))

# Sidebar inputs for filtering
st.sidebar.header("검색 조건")
type_option = df['물건 종류'].dropna().unique()
type = st.sidebar.selectbox("물건 종류", type_option)
region = st.sidebar.selectbox("지역", options=["서울", "경기", "인천"])



# 선택한 ""에 따라 "시/구" 필터링
region_filtered_df = df[df['도/시'] == region]  # "지역" 열을 기준으로 필터링
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

# Session state 초기화
if "filtered_data" not in st.session_state:
    st.session_state["filtered_data"] = None

# 데이터 검색 버튼
if st.sidebar.button("검색"):
    
    # 조건을 동적으로 구성하여 입력된 값에 맞게 필터링
    filtered_data = df[
        (df["종류"].astype(str).str.contains(type, case=False, na=False)) &
        (df["지역"].astype(str).str.contains(region, case=False, na=False)) &
        (df["시/구"].astype(str).str.contains(region1, case=False, na=False)) &
        ((True if region2 == "전체" else df["구/동"].astype(str).str.contains(region2, case=False, na=False))) &
        ((True if not options else df["인수액"].isin(options)))  # 추가 텍스트 조건에 맞는 경우
    ]

    # 결과를 session_state에 저장
    st.session_state["filtered_data"] = filtered_data

#     필터링된 데이터 표시
#     st.header("인수액이 없는 경매 물건 리스트")
#     st.dataframe(filtered_data)
    
#     # 필터링된 데이터의 행 수 출력
#     st.write(f"검색된 물건 개수: {filtered_data.shape[0]}개")

# else:
#     st.write("검색 조건을 설정하고 '데이터 검색' 버튼을 눌러주세요.")


# 필터링된 데이터 표시
if st.session_state["filtered_data"] is not None:
    st.header("인수액이 없는 경매 물건 리스트")
    st.dataframe(st.session_state["filtered_data"])
    
    # 필터링된 데이터의 행 수 출력
    st.write(f"검색된 물건 개수: {st.session_state['filtered_data'].shape[0]}개")
else:
    st.write("검색 조건을 설정하고 '데이터 검색' 버튼을 눌러주세요.")





########################### 수익률 계산기 ###########################
#원리금 상환 함수
def calculate_monthly_payment(principal, annual_rate, months):
    monthly_rate = annual_rate / 12
    monthly_payment = principal * (monthly_rate * (1 + monthly_rate)**months) / ((1 + monthly_rate)**months - 1)
    return monthly_payment

st.write("---")

# 제목
st.title("수익률 계산기💸")


# 연산 선택
option = st.radio("대출 종류를 선택하세요.", ("주택담보대출 MCG", "주택담보대출 MCI", "사업자대출", "임대사업자대출"))


# 입력 받기
col1, col2, col3, col4 = st.columns([1,1,1,1])

Appraisedvalue = col1.number_input("감정가", value=0, step=500000, format="%d")
Bidprice = col2.number_input("입찰가", value=0, step=500000, format="%d")
interestrate = col3.number_input("금리", value=4.0, step=0.1)
smalldeposit = col4.selectbox("소액임차보증금", ["55,000,000", "48,000,000", "28,000,000", "25,000,000"])

Deposit = col1.selectbox("예상 보증금", ["5,000,000", "10,000,000", "20,000,000"])
rent = col2.selectbox("예상 월세", ["400,000", "450,000", "500,000", "550,000", "600,000", "650,000", "700,000", "750,000", "800,000", "850,000", "900,000", "950,000", "1,000,000"])
Repaircost = col3.selectbox("예상 비용", ["3,000,000", "5,000,000", "7,000,000", "10,000,000"])


#소액임차 보증금 정수화
if smalldeposit == "55,000,000":
    smalldeposit_cal = 55000000

elif smalldeposit == "48,000,000":
    smalldeposit_cal = 48000000

elif smalldeposit == "28,000,000":
    smalldeposit_cal = 28000000

elif smalldeposit == "25,000,000":
    smalldeposit_cal = 25000000

#보증금 정수화
if Deposit == "5,000,000":
    Deposit_cal = 5000000

elif Deposit == "10,000,000":
    Deposit_cal = 10000000

elif Deposit == "20,000,000":
    Deposit_cal = 20000000

#수리비 정수화
if Repaircost == "3,000,000":
    Repaircost_cal = 3000000

elif Repaircost == "5,000,000":
    Repaircost_cal = 5000000

elif Repaircost == "7,000,000":
    Repaircost_cal = 7000000

elif Repaircost == "10,000,000":
    Repaircost_cal = 10000000

#월세 정수화
if rent == "400,000":
    rent_cal = 400000

elif rent == "450,000":
    rent_cal = 450000

elif rent == "500,000":
    rent_cal = 500000

elif rent == "550,000":
    rent_cal = 550000

elif rent == "600,000":
    rent_cal = 600000

elif rent == "650,000":
    rent_cal = 650000

elif rent == "700,000":
    rent_cal = 700000

elif rent == "750,000":
    rent_cal = 750000

elif rent == "800,000":
    rent_cal = 800000

elif rent == "850,000":
    rent_cal = 850000

elif rent == "900,000":
    rent_cal = 900000

elif rent == "950,000":
    rent_cal = 950000

elif rent == "1,000,000":
    rent_cal = 1000000

elif rent == "1,050,000":
    rent_cal = 1050000

elif rent == "1,100,000":
    rent_cal = 1100000

elif rent == "1,150,000":
    rent_cal = 1150000

elif rent == "1,200,000":
    rent_cal = 1200000

#대출 금액 계산
if option == "주택담보대출 MCG":
    loan = round(min(Appraisedvalue*0.6, Bidprice*0.8))
    monthly_payment = math.ceil(calculate_monthly_payment(loan, interestrate/100, 480) / 1000)*1000

elif option == "주택담보대출 MCI":
    loan = round(min(Appraisedvalue*0.6, Bidprice*0.8))
    monthly_payment = math.ceil(calculate_monthly_payment(loan, interestrate/100, 360) / 1000)*1000

elif option == "사업자대출":
    loan = round(min(Appraisedvalue*0.6 - smalldeposit_cal, Bidprice*0.7))
    monthly_payment = math.ceil((loan*interestrate/1200)  / 1000)*1000
    
elif option == "임대사업자대출":
    loan = round(min(Appraisedvalue*0.6 - smalldeposit_cal, Bidprice*0.8))
    monthly_payment = math.ceil((loan*interestrate/1200)  / 1000)*1000





Total_investment_amount = (Bidprice + Repaircost_cal) - (loan + Deposit_cal)

rate_of_return = round((rent_cal - monthly_payment)*1200 / Total_investment_amount, 1)
net_rent = rent_cal - monthly_payment


st.markdown("---")

col1, col2 = st.columns([1,2])

col1.subheader("수익률 계산")


if rate_of_return >= 25:
    col2.subheader("훌륭한 가격입니다!😆")

elif rate_of_return >= 18:
    col2.subheader("적정 가격입니다!😃")

elif rate_of_return >= 15:
    col2.subheader("약간 비싼 가격입니다...🤔")

else:
    col2.subheader("다시 생각해보세요!😥")




col1, col2, col3 = st.columns([1,1,1])
col1.write(f"감정가 : {Appraisedvalue:,}원")
col1.write(f"입찰가 : {Bidprice:,}원")
col1.write(f"금리 : {interestrate:.2f}%")
col1.write(f"소액임차보증금 : {smalldeposit:}원")

col2.markdown(f'<p style="color:green; font-weight:bold;">대출 가능 금액 : {loan:,}원</p>', unsafe_allow_html=True)

if option == "주택담보대출 MCG":
    col2.write(f"대출 이자 + 원금 : {monthly_payment:,}원/월")

elif option == "주택담보대출 MCI":
    col2.write(f"대출 이자 + 원금 : {monthly_payment:,}원/월")

elif option == "사업자대출":
    col2.write(f"대출 이자 : {monthly_payment:,}원/월")
    
elif option == "임대사업자대출":
    col2.write(f"대출 이자 : {monthly_payment:,}원/월")




col3.markdown(f'<p style="color:green; font-weight:bold;">총 투자금액 : {Total_investment_amount:,}원</p>', unsafe_allow_html=True)
col3.write(f"순월세 : {net_rent:,}원/월")

if rate_of_return >= 20:
    col3.markdown(f'<p style="color:red;">월세 수익률 : {rate_of_return:,}%</p>', unsafe_allow_html=True)

elif rate_of_return < 20:
    col3.markdown(f'<p style="color:blue; font-weight:bold;">월세 수익률 : {rate_of_return:,}%</p>', unsafe_allow_html=True)

col3.write(f"투자금 회수 기간 : {round(Total_investment_amount/(net_rent*12), 1):,}년")
