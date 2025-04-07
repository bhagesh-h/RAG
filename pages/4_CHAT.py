import os
import streamlit as st
from modules.misc_UI import navigation_buttons, chatUI

st.title("GenomeConnect")
st.subheader("AI Powered NGS Querying")


if __name__ == "__main__":
    disable_navigation_dict = {"HOME": False, "LOGIN": True, "FILES": False, "CHAT": True}
    navigation_buttons(disable_navigation_dict)
    chatUI(model="gpt-3.5-turbo", client="test_client")