import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from backend.main import chat 
from backend.main import ChatRequest

st.set_page_config(page_title="Smart Kitchen Helper", layout="wide")

css_path = os.path.join(os.path.dirname(__file__), "style.css")

with open(css_path) as css:
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
            json={"question": prompt, "chat_history": st.session_state.chat_history}

            request = ChatRequest(**json)
        
            response = chat(request)

            if response:
                answer = response["answer"]
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": answer
                })
                st.markdown(answer)
            else:
                st.error("Something went wrong! Please check the backend.")