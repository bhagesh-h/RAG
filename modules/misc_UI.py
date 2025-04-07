import os
import streamlit as st
from modules import misc_ollama as ollama

# Navigation buttons for the app
def navigation_buttons(disable_navigation_dict):
    col1, col2, col3, col4 = st.columns(4, border=True, gap="small", vertical_alignment="top")
    # disable_navigation_dict = {"HOME": False, "LOGIN": False, "FILES": True, "CHAT": True}
    with col1: st.page_link("HOME.py",          label="HOME",   icon="🏠", disabled=disable_navigation_dict["HOME"])
    with col2: st.page_link("pages/2_LOGIN.py", label="LOGIN",  icon="1️⃣", disabled=disable_navigation_dict["LOGIN"])
    with col3: st.page_link("pages/3_FILES.py", label="FILES",  icon="2️⃣", disabled=disable_navigation_dict["FILES"])
    with col4: st.page_link("pages/4_CHAT.py",  label="CHAT",   icon="3️⃣", disabled=disable_navigation_dict["CHAT"])

def chatUI(model,client=''):
    ollamaFunc = ollama.ollamaFunc(model=model, embedding_model="all-minilm")
    ollamaFunc.pull_model()
    st.warning('AI GENERATED CONTENT PLEASE VEREIFY BEFORE USAGE!', icon="⚠️")
    client = "test_client"  
    if "model" not in st.session_state: st.session_state["model"] = "gpt-3.5-turbo"
    if "messages" not in st.session_state: st.session_state.messages = []
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
   
    if prompt := st.chat_input(f"Ask {model} about your reports!"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            stream = {
                "model": st.session_state["model"],
                "messages": [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                "stream":True,
            }
            response = st.write_stream(stream.values())
        st.session_state.messages.append({"role": "assistant", "content": response})