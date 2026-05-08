import streamlit as st
import google.generativeai as genai
from datetime import datetime

# 1. 페이지 설정 (웹사이트 탭에 보일 이름과 아이콘)
st.set_page_config(page_title="태이와 함께하는 하루", page_icon="👶", layout="centered")

# 2. 보안 설정: 스트림릿 Secrets에서 키를 가져옵니다.
# (아까 스트림릿 Settings -> Secrets에 키를 저장하셨으니 이대로 두시면 됩니다!)
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    st.error("Secrets 설정에서 GOOGLE_API_KEY를 찾을 수 없습니다.")
    st.stop()

# 3. 에러(404) 방지를 위한 정식 경로 설정
genai.configure(api_key=API_KEY, transport='rest')
model = genai.GenerativeModel('gemini-1.5-flash')

# 4. 태이 탄생일 계산 (2025년 11월 23일)
# 사용자 수정 이력을 바탕으로 정확한 날짜를 반영했습니다.
birth_date = datetime(2025, 11, 23) 
today = datetime.now()
days_since_birth = (today - birth_date).days

# 5. 화면 구성 및 스타일링
st.title("👶 태이의 성장 파트너")
st.subheader(f"우리 태이가 세상에 온 지 **{days_since_birth}일**째 되는 날! ❤️")

# 채팅 메시지 저장용 공간
if "messages" not in st.session_state:
    st.session_state.messages = []

# 사이드바 (왼쪽 메뉴)
with st.sidebar:
    st.header("🍼 육아 도우미")
    st.write("태이와 지예를 위해 치윤이가 만들었어!")
    st.markdown("---")
    st.write("📮 **치윤의 메시지**")
    st.info("지예야, 태이 보느라 고생 많지? 내가 퇴근하고 얼른 갈게! 사랑해 ❤️")

# 저장된 채팅 메시지 화면에 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. 질문 입력 및 AI 답변 생성
if prompt := st.chat_input("육아 고민이나 궁금한 점을 물어보세요!"):
    # 사용자 질문 표시
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI 답변 생성 및 표시
    with st.chat_message("assistant"):
        try:
            # 404 에러를 피하기 위해 최신 모델 이름만 사용
            response = model.generate_content(prompt)
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                # 성공 메시지 (치윤 님의 따뜻한 마음 추가)
                st.toast("치윤 님이 지예 님을 응원하고 있어요! 💖")
        except Exception as e:
            st.error("잠시 후 다시 시도해 주세요. (연결 확인 중)")
            print(f"DEBUG: {e}")
