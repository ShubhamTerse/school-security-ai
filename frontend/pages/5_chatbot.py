import streamlit as st
import requests

API_URL = "https://school-security-ai.onrender.com/api"

if "token" not in st.session_state or not st.session_state.token:
    st.warning("Please log in from the main page.")
    st.stop()

headers = {"Authorization": f"Bearer {st.session_state.token}"}

st.title("Ask Security AI")
st.write("Ask questions about school security policies, procedures, and past incidents.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What should I do during a fire emergency?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            res = requests.post(f"{API_URL}/ai/chat", json={"question": prompt}, headers=headers)
            if res.status_code == 200:
                answer = res.json().get("answer", "No answer returned.")
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                st.error("Failed to connect to the AI service.")
