import os
import streamlit as st
from modules.misc_UI import navigation_buttons

st.title("GenomeConnect")
st.subheader("AI Powered NGS Querying")


if __name__ == "__main__":
    disable_navigation_dict = {"HOME": False, "LOGIN": False, "FILES": True, "CHAT": True}
    navigation_buttons(disable_navigation_dict)