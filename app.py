import os
import streamlit as st

st.title("GenomeConnect")
st.subheader("AI Powered NGS Querying")

# Test App

st.page_link("app.py", label="Home", icon="🏠")
st.page_link("pages/login.py", label="Login", icon="1️⃣")
st.page_link("pages/pickInput.py", label="Pick Files", icon="2️⃣", disabled=True)
st.page_link("pages/chatUI.py", label="Chat", icon="3️⃣", disabled=True)

def chatUI(model,client):
    # st.info('We appreciate your engagement! Please note, this demo is designed to process a maximum of 10 interactions and may be unavailable if too many people use the service concurrently. Thank you for your understanding.', icon="ℹ️")
    client = "test_client"  

    if "model" not in st.session_state:
        st.session_state["model"] = "gpt-3.5-turbo"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Any queries about your report?"):
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

# LOGIN PAGE

# RAG PAGE

# QnA PAGE

# MAIN FUNCTION
def main():
    chatUI(model="gpt-3.5-turbo", client="test_client")
    pass

if __name__ == "__main__":
    # Initialize the app
    main()