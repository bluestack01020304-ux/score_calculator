import streamlit as st
import dataManager as dataManager
import geminiManager as geminiManager
from dotenv import load_dotenv
import os

import pandas as pd
import numpy as np

dataManager.initialize_data_manager() # 임시
geminiManager.initialize_gemini_manager() # 임시
load_dotenv()
 
# =========================================================================
# 1. 초기 데이터 및 데이터 저장소(session_state) 설정
# =========================================================================
 
# 스팀릿이 새로고침되어도 데이터가 지워지지 않도록 세션 상태에 저장
 
if "logged_in_user" not in st.session_state:
    st.session_state["logged_in_user"] = -1 # -1: 비회원, 0: 관리자, 그 외: 학생
 
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "login"
 
 
# =========================================================================
# 2. 로그인 화면 UI
# =========================================================================

ADMIN_ID = os.getenv("ADMIN_ID")
ADMIN_PW = os.getenv("ADMIN_PW")

def LogInUI():
    st.title("🔒 로그인")
    
    userid = st.text_input("아이디(ID)", key="login_id")
    userpw = st.text_input("비밀번호(PW)", type="password", key="login_pw")
    
    if st.button("로그인", type="primary", use_container_width=True):
        if userid == "":
            st.warning("아이디를 입력해주세요.")
            return
        if userpw == "":
            st.warning("비밀번호를 입력해주세요.")
            return

        if userid == ADMIN_ID and userpw == ADMIN_PW:
            st.success("관리자 로그인 성공!")
            st.session_state["logged_in_user"] = 0
            st.session_state["current_page"] = "main"
            st.rerun()
            return
        
        try:
            login_success = dataManager.executeQuery("SELECT * FROM user WHERE uid='%s' AND pw='%s'", (userid, userpw))
            print(login_success)
            if login_success:
                print("Login Successful")
                print(login_success[0][0])

                st.success("로그인 성공!")
                st.session_state["logged_in_user"] = login_success[0][0]
                st.session_state["current_page"] = "main"
                st.rerun()
                return
            else:
                st.error("로그인 실패. 다시 입력해주세요.")
                return

        except Exception as e:
            print(f"Error during login query: {e}")


    if st.button("비회원 로그인", use_container_width=True):
        #@TODO: 비회원 로그인 버튼을 누르고 난 후 할 상황
        st.session_state["logged_in_user"] = -1
        st.session_state["current_page"] = "main"
        st.rerun()
        return

 
 
# =========================================================================
# 3. 학생 점수 입력 UI (메인 화면 내 토글 형식으로 구현)
# =========================================================================
def ScoreInputUI():
    st.markdown("### 📝 학생 점수 입력")
    
    name = st.text_input("학생 이름", key="input_name")
    num = st.text_input("학번", key="input_num")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        kor = st.text_input("국어 점수", key="input_kor")
    with col2:
        eng = st.text_input("영어 점수", key="input_eng")
    with col3:
        math = st.text_input("수학 점수", key="input_math")
    with col4:
        sci = st.text_input("과학 점수", key="input_sci")
    with col5:
        his = st.text_input("역사 점수", key="input_his")
        
    if st.button("저장하기", type="primary"):
        name = name.strip()
        num = num.strip()
        kor = kor.strip()
        eng = eng.strip()
        math = math.strip()
        sci = sci.strip()
        his = his.strip()
        
        # 모든 칸이 채워졌는지 검사
        cdic = {
            "이름": name,
            "학번": num,
            "국어": int(kor),
            "영어": int(eng),
            "수학": int(math),
            "과학": int(sci),
            "역사": int(his)
        }

        for key, value in cdic.items():
            if value == "":
                print("입력 걸림")
                st.warning(f"{key}를 입력해주세요.")
                return

        for key, value in cdic.items():
            if key == "이름" or key == "학번": continue
            if (value > 100 or value < 0):
                print("값 걸림")
                st.warning(f"{key}의 값이 잘못되었습니다")
                return

        # if name == "" or num == "" or kor == "" or eng == "" or math == "" or sci == "" or his == "":
        #     st.warning("⚠️ 이름과 학번, 모든 과목의 점수를 입력해주세요.")
        #     return
        

        #add studnet
            
        # 입력된 학생의 이름, 학번, 점수를 세션 리스트에 저장
        # st.session_state["STUDENT_DATA"].append({
        #     "이름": name,
        #     "학번": num,
        #     "국어": kor,
        #     "영어": eng,
        #     "수학": math,
        #     "과학": sci,
        #     "역사": his
        # })
        # st.success(f"{name} 학생의 성적이 정상적으로 저장되었습니다.")
        # st.rerun()

# =========================================================================
# 4.총점과 평균
# =========================================================================
 


 # 요약

def ScoreSummary():
    st.markdown("### 📌 성적 통계 요약")

    student_data = None
    try:
        student_data = dataManager.executeQuery(f"SELECT * FROM students WHERE id='{st.session_state['logged_in_user']}'")
    except Exception as e:
        print(f"Error fetching student data: {e}")
        st.error("학생 데이터를 불러오는 중 오류가 발생했습니다.")
        return

    if not student_data:
        st.error("학생 데이터를 찾을 수 없습니다.")
        return

    student_data = student_data[0]

    # with col1:
    #     st.metric(label="국어", value="85점")
    # with col2:
    #     st.metric(label="영어", value="90점")
    # with col3:
    #     st.metric(label="수학", value="95점")
    # with col4:
    #     st.metric(label="과학", value="80점")
    # with col5:
    #     st.metric(label="역사", value="88점")
    # with col6:
    #     st.metric(label="총합", value="438점")
    # with col7:
    #     st.metric(label="평균", value="87.6점")

    st.markdown("---")

    if st.button("📊 성적 그래프 보기", type="primary", use_container_width=True):
        st.markdown("#### 📈 과목별 점수 추이")

        chart_data = pd.DataFrame(
            [85, 90, 95, 80, 88],
            index=["국어", "영어", "수학", "과학", "역사"],
            columns=["점수"],
        )

        st.bar_chart(chart_data)

def AskAiUI():
    st.markdown("### AI에게 물어보기")

    ask = st.text_input("AI에게 성적 물어보기")
    
    if st.button("검색", type="primary"):

        isSpace = ask.strip()
        if isSpace == "":
            st.warning("물어보고 싶은 것을 입력하시오")
            return
        
        response = geminiManager.genarate_response(ask)

        st.info(response)
        return


 
# 4. Main UI
def MainUI():

    if st.session_state["logged_in_user"] == -1:
        #비회원 로그인
        st.title("게스트님 환영합니다!")
    elif st.session_state["logged_in_user"] == 0:
        st.title("관리자님 환영합니다!")
    else:
        student_data = None
        try:
            student_data = dataManager.executeQuery(f"SELECT * FROM students WHERE id='{st.session_state['logged_in_user']}'")

            if student_data:
                student_data = student_data[0]
            else:
                st.error("학생 정보를 찾을 수 없습니다.")
                return
            
        except Exception as e:
            print(f"Error fetching student ID: {e}")
            st.error("학생 정보를 불러오는 중 오류가 발생했습니다.")
            return
        
        st.title(f"👑 {student_data[1]}님 환영합니다!")
    
    # --- 상단 메뉴 버튼 기능 제어용 세션 상태 변수 ---
    if "sub_action" not in st.session_state:
        st.session_state["sub_action"] = None
 
    
    # 학생 점수 입력 & 모든 학생 점수 출력
    row1_col1, row1_col2 = st.columns(2)
    with row1_col1:
        if st.button("📝 학생 점수 입력", use_container_width=True):
            st.session_state["sub_action"] = "input"
    with row1_col2:
        if st.button("📋 모든 학생 점수 출력", use_container_width=True):
            st.session_state["sub_action"] = "print_all"
 
    # 2행: 학생검색 & 총점과 평균
    row2_col1, row2_col2 = st.columns(2)
    with row2_col1:
        if st.button("🔍 학생검색", use_container_width=True):
            st.session_state["sub_action"] = "search"
    with row2_col2:
        if st.button("📊 총점과 평균", use_container_width=True):
            st.session_state["sub_action"] = "calc"
 
    # 3행: 학점 & 석차 나누기
    row3_col1, row3_col2 = st.columns(2)
    with row3_col1:
        if st.button("🅰️ 학점", use_container_width=True):
            st.session_state["sub_action"] = "grade"
    with row3_col2:
        if st.button("👑 석차 나누기", use_container_width=True):
            st.session_state["sub_action"] = "rank"
 
    # 4행: 필터링 & 요약
    row4_col1, row4_col2 = st.columns(2)
    with row4_col1:
        if st.button("⏳ 필터링", use_container_width=True):
            st.session_state["sub_action"] = "filter"
    with row4_col2:
        if st.button("📌 요약", use_container_width=True):
            st.session_state["sub_action"] = "summary"


 
    # 5행: AI 질문하기 (단독 가로 긴 버튼)
    if st.button("🤖 AI 질문하기", use_container_width=True):
        st.session_state["sub_action"] = "ai"
 
    st.markdown("---") # 구별선
 
    # --- 각 버튼 기능 처리부 ---
    action = st.session_state["sub_action"]
    
    if action == "input":   #학생 점수 입력
        if not st.session_state["logged_in_user"] == 0:
            st.warning("⚠️ 학생 점수 입력은 관리자만 이용할 수 있는 기능입니다.")
            return
        
        ScoreInputUI()
        
    elif action == "print_all":        #모든 학생 출력
        if st.session_state["logged_in_user"] != 0:
            st.warning("⚠️ 학생 점수 입력은 관리자만 이용할 수 있는 기능입니다.")
            return
        
        try:
            student_data = dataManager.executeQuery("SELECT * FROM students")

            if student_data:
                st.markdown("### 학생 전체 데이터")
                st.dataframe(student_data, use_container_width=True)
        except Exception as e:
            print(f"Error fetching student ID: {e}")
            st.error("학생 정보를 불러오는 중 오류가 발생했습니다.")
            return
 
    elif action == "search":        #학생 검색
        #@TODO: 학생에 경우 자신만 검색 가능 / 비회원 불가
        if st.session_state["logged_in_user"] == -1:
            st.warning("⚠️ 학생 검색은 로그인한 학생과 관리자만 이용할 수 있는 기능입니다.")
            return
        st.info("안내: 학생 검색 기능입니다.")
 
    elif action == "calc":      #평균과 총점
        st.markdown("### 점수 총점 및 평균")

        # student_data = 
        # if student_data:
        #     student_data = student_data[0]
        #     st.dataframe(student_data, use_container_width=True)
 
    elif action == "grade":
        st.info("안내: 학점 기능입니다.")
 
    elif action == "rank":
        st.info("안내: 석차 나누기 기능입니다.")
 
    elif action == "filter":
        st.info("안내: 필터링 기능입니다.")
 
    elif action == "summary":
        st.info("안내: 요약 기능입니다.")

        ScoreSummary()
 
    elif action == "ai":
        st.info("안내: AI 질문하기 기능입니다.")
        AskAiUI()
 


 
# =========================================================================
# 5. 앱 페이지 라우팅 제어 (로그인 상태창 분기)
# =========================================================================
if st.session_state["current_page"] == "login":
    LogInUI()
elif st.session_state["current_page"] == "main":
    MainUI()