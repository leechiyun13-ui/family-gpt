import streamlit as st
import google.generativeai as genai
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(page_title="태이와 함께하는 하루", page_icon="👶", layout="centered")

# 2. API 설정 (새로 보내주신 키를 넣었습니다)
API_KEY = "AIzaSyCWy2OubVl96B5-i_dyqBdzYbA2vCHEjNg"

# [핵심] 정식 버전(v1) 주소를 사용하도록 강제 설정하여 404 에러를 방지합니다.
genai.configure(api_key=API_KEY, transport='rest')

# 모델명을 'gemini-1.5-flash'로 설정합니다.
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. 태이 탄생일 계산 (2025년 11월 23일)
birth_date = datetime(2025, 11, 23) 
today = datetime.now()
days_since_birth = (today - birth_date).days

# 4. 스타일링 (CSS)
st.markdown("""
    <style>
    .main { background-color: #fff9f9; }
    .stChatMessage { border-radius: 15px; }
    .stButton>button { width: 100%; border-radius: 10px; background-color: #ff9a9e; color: white; font-weight: bold; height: 3.5em; }
    .stInfo { background-color: #ffe4e1; border: none; color: #5d5d5d; border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# 5. 메인 헤더
st.title("👶 태이의 성장 파트너")
st.subheader(f"우리 태이가 세상에 온 지 **{days_since_birth}일**째 되는 날! ❤️")
st.info("지예 님, 오늘도 태이와 함께하느라 정말 고생 많으셨어요. 치윤 님이 늘 곁에서 응원하고 있어요!")

# 6. 채팅 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 7. 사이드바
with st.sidebar:
    st.header("🍼 육아 도움말")
    if st.button("🧼 태이 목욕 팁"):
        st.session_state.messages.append({"role": "user", "content": "아기 목욕시킬 때 주의할 점 알려줘"})
    if st.button("💤 아기 수면 교육"):
        st.session_state.messages.append({"role": "user", "content": "아기 통잠 자게 하는 꿀팁 알려줘"})
    
    st.markdown("---")
    st.write("📮 **치윤 님의 마음**")
    st.write("지예야, 태이 보느라 밥은 챙겨 먹었어? 내가 퇴근하고 얼른 갈게! 사랑해 ❤️")

# 8. 대화 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 9. 질문 입력 및 AI 답변 생성
if prompt := st.chat_input("육아 고민이나 궁금한 점을 편하게 물어보세요!"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        full_prompt = f"""
        너는 '이치윤'이 아내 '강지예'를 위해 만든 다정한 육아 비서야.
        태이가 생후 {days_since_birth}일째라는 점을 참고해서 공감하며 답변해줘.
        끝에는 반드시 "치윤 님이 지예 님을 정말 사랑한대요! ❤️"라고 해줘.
        질문: {prompt}
        """
        try:
            # 답변 생성 시도
            response = model.generate_content(full_prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"연결 상태를 확인 중입니다: {e}")
            st.info("API 키가 활성화되는 데 1~2분 정도 걸릴 수 있습니다. 잠시 후 다시 시도해 주세요.")
