import streamlit as st
from utils.ui import navigation_buttons

st.title("LOCAL RAG")
st.subheader("AI Powered PDF Querying")

if __name__ == "__main__":
    navigation_buttons({"HOME": False, "FILES": True, "CHAT": True, "IMAGE": True})

    st.markdown("-------------------------")
    st.markdown("Welcome to **LOCAL RAG** — your personalized companion for understanding PDFs.")
    st.markdown("Powered by advanced Graph **Retrieval-Augmented Generation** (RAG) technology, **LOCAL RAG** enables users to ask questions directly about their data and receive accurate, context-aware answers.") 
    st.markdown("-------------------------")

    name        = st.text_input("Username", placeholder="Enter your user name")
    password    = st.text_input("Password", placeholder="Enter your password", type="password")

    if name=='admin' and password=='admin':
        if st.button("LOGIN"):
            st.switch_page("pages/1_Files.py")
    elif name !='admin' or password != 'admin':
        if st.button("LOGIN"):
            st.warning("Invalid username or password. Please try again.")
            st.markdown("If you don't have an account, please contact the admin to create one.")
            st.markdown("Don't worry, your data is safe with us!")