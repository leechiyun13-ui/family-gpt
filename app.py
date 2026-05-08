import streamlit as st
import google.generativeai as genai
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(page_title="태이와 함께하는 하루", page_icon="👶", layout="centered")

# 2. 보안 설정 (Secrets 확인)
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
except Exception:
    st.error("Secrets 설정에서 GOOGLE_API_KEY를 찾을 수 없습니다. Streamlit Settings를 확인해주세요.")
    st.stop()

# 3. AI 모델 연결 설정 (최신 표준 방식)
# transport='rest'를 제거하고 기본 연결을 사용하여 안정성을 높였습니다.
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 4. 태이 탄생일 계산 (2025년 11월 23일)
# 치윤 님의 요청에 따른 정확한 날짜입니다.
birth_date = datetime(2025, 11, 23)
today = datetime.now()
days_since_birth = (today - birth_date).days

# 5. 화면 구성
st.title("👶 태이의 성장 파트너")
st.subheader(f"우리 태이가 세상에 온 지 **{days_since_birth}일**째 되는 날! ❤️")

# 채팅 메시지 저장
if "messages" not in st.session_state:
    st.session_state.messages = []

# 사이드바 설정
with st.sidebar:
    st.header("🍼 육아 도우미")
    st.write("태이와 지예를 위해 치윤이가 만들었어!")
    st.markdown("---")
    st.write("📮 **치윤의 메시지**")
    st.info("지예야, 태이 보느라 고생 많지? 내가 퇴근하고 얼른 갈게! 사랑해 ❤️")

# 기존 대화 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. 질문 입력 및 답변 생성
if prompt := st.chat_input("육아 고민이나 궁금한 점을 물어보세요!"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # AI에게 답변 요청
            response = model.generate_content(prompt)
            if response and response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                st.toast("치윤 님이 지예 님을 응원하고 있어요! 💖")
        except Exception as e:
            # 에러 발생 시 상세 메시지 출력 (디버깅용)
            st.error("AI 연결에 잠시 문제가 생겼습니다. 잠시 후 다시 시도해주세요.")
            st.info("팁: 스트림릿 관리 화면에서 'Reboot App'을 눌러보세요!")
