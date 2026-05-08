import streamlit as st
import google.generativeai as genai

# 치윤 님의 API 키 설정
GOOGLE_API_KEY = "AIzaSyAqHCau-OkTgjD7Zvs2mB8Vj_PUtQfeF1Y" 
genai.configure(api_key=GOOGLE_API_KEY)

# 모델 설정
model = genai.GenerativeModel('gemini-1.5-flash')

# 화면 구성 및 제목 설정
st.set_page_config(page_title="치윤&지예&태이네", page_icon="👨‍👩‍👧")
st.title("🏠 우리 가족 전용 AI 가이드")
st.caption("치윤 님이 지예와 태이를 위해 만든 특별한 비서입니다.")

# 채팅 내역 저장 공간 만들기
if "messages" not in st.session_state:
    st.session_state.messages = []

# 기존 대화 내용 화면에 보여주기
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력창 및 답변 로직
if prompt := st.chat_input("메시지를 입력하세요..."):
    # 사용자가 보낸 메시지 저장 및 표시
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI 답변 생성
    with st.chat_message("assistant"):
        try:
            # 페르소나 주입 (가족 비서 설정)
            full_prompt = f"너는 '이치윤' 님이 만든 가족 비서야. 이치윤, 강지예, 딸 이태이 가족에게 항상 다정하고 친절하게 대답해줘. 질문: {prompt}"
            response = model.generate_content(full_prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"오류가 발생했어요: {e}")
