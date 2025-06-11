import streamlit as st
import requests

st.set_page_config(page_title="Smart Kitchen Helper", layout="wide")

with open("style.css") as css:
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)

st.markdown(
    "<h3 style='font-size:32px;'>🍽️ Smart Kitchen Helper - "
    "<a href='https://www.linkedin.com/in/prince-khunt-linked-in/' target='_blank'>k_prince</a></h3>",
    unsafe_allow_html=True
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about any recipes"):
    st.session_state.chat_history.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = requests.post(
                "http://localhost:8000/chat",
                json={"question": prompt, "chat_history": st.session_state.chat_history}
            )

            if response.status_code == 200:
                answer = response.json()["answer"]
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": answer
                })
                st.markdown(answer)
            else:
                st.error("Something went wrong! Please check the backend.")