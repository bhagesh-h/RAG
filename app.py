import streamlit as st
from utils.ui import navigation_buttons

st.title("GenomeConnect")
st.subheader("AI Powered NGS Querying")

if __name__ == "__main__":
    navigation_buttons({"HOME": False, "FILES": True, "CHAT": True, "IMAGE": True})

    st.markdown("-------------------------")
    st.markdown("Welcome to **GenomeConnect** — your personalized companion for understanding genomic reports.")
    st.markdown("Powered by advanced Graph **Retrieval-Augmented Generation** (RAG) technology, **GenomeConnect** enables users to ask questions directly about their genetic data and receive accurate, context-aware answers.") 
    st.markdown("Whether you're seeking clarity on variants, insights into your health, or support interpreting complex findings, **GenomeConnect** is here to bridge the gap between raw data and meaningful understanding.")
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