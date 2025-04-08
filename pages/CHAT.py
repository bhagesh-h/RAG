import os
import streamlit as st
import pages.FILES as files
from modules.misc_UI import navigation_buttons, chatUI

st.title("GenomeConnect")
st.subheader("AI Powered NGS Querying")

image1 = "https://m.media-amazon.com/images/I/41sHexVm4NL._AC_US60_SCLZZZZZZZ__.jpg"
image2 = "https://m.media-amazon.com/images/I/41YNaNTqJoL._AC_US60_SCLZZZZZZZ__.jpg"
image3 = "https://m.media-amazon.com/images/I/41t1HM8UN8L._AC_US60_SCLZZZZZZZ__.jpg"
image4 = "https://m.media-amazon.com/images/I/41UuyU7HsPL._AC_US60_SCLZZZZZZZ__.jpg"
image5 = "https://m.media-amazon.com/images/I/31XThr46I6L._AC_US60_SCLZZZZZZZ__.jpg"
image_list = [image1, image2, image3, image4, image5]

models=["gemma3:4b","all-minilm"]

if __name__ == "__main__":
    st.write(st.session_state['files'])
    disable_navigation_dict = {"HOME": False, "LOGIN": True, "FILES": False, "CHAT": True}
    navigation_buttons(disable_navigation_dict)
    chatUI(models, client="test_client")