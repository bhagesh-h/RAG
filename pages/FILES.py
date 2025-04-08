import os
import streamlit as st
from modules.misc_UI import navigation_buttons
from modules.misc_UI import fileSelectorUI

st.title("GenomeConnect")
st.subheader("AI Powered NGS Querying")

path = "/mnt/c/Users/bhage/Documents/code/RAG/test_data"
files = []

if __name__ == "__main__":
    disable_navigation_dict = {"HOME": False, "LOGIN": False, "FILES": True, "CHAT": True}
    navigation_buttons(disable_navigation_dict)
    files = fileSelectorUI(path=path)
    
    