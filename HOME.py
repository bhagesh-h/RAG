import os
import streamlit as st
from modules.misc_UI import navigation_buttons

st.title("GenomeConnect")
st.subheader("AI Powered NGS Querying")

if __name__ == "__main__":
    disable_navigation_dict = {"HOME": False, "LOGIN": False, "FILES": True, "CHAT": True, "IMAGES": True}
    navigation_buttons(disable_navigation_dict)

    st.markdown("-------------------------")
    st.markdown("Welcome to **GenomeConnect** — your personalized companion for understanding genomic reports.")
    st.markdown("Powered by advanced **Retrieval-Augmented Generation** (RAG) technology, **GenomeConnect** enables users to ask questions directly about their genetic data and receive accurate, context-aware answers.") 
    st.markdown("Whether you're seeking clarity on variants, insights into your health, or support interpreting complex findings, **GenomeConnect** is here to bridge the gap between raw data and meaningful understanding.")
    st.markdown("-------------------------")
    
    if st.button("Proceed To Login"):
        st.switch_page("pages/LOGIN.py")
        