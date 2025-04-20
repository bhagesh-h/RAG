import os
import streamlit as st
from modules.misc_UI import navigation_buttons

st.title("GenomeConnect")
st.subheader("AI Powered NGS Querying")

if __name__ == "__main__":
    disable_navigation_dict = {"HOME": False, "LOGIN": True, "FILES": True, "CHAT": True, "IMAGES": True}
    navigation_buttons(disable_navigation_dict)

    name = st.text_input("Username", placeholder="Enter your username")
    password = st.text_input("Password", placeholder="Enter your password", type="password")

    if name=='admin' and password=='admin':
        if st.button("LOGIN"):
            st.switch_page("pages/FILES.py")
    elif name !='admin' or password != 'admin':
        if st.button("LOGIN"):
            st.warning("Invalid username or password. Please try again.")
            st.markdown("If you don't have an account, please contact the administrator to create one.")
            st.markdown("Don't worry, your data is safe with us!")