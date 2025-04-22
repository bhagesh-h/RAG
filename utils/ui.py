import os
import streamlit as st
# from modules.simple_rag import RAGDescriptionChain
# from modules.simple_rag import ImageDescriptionChain
# from modules.parse_image import parseImage
from streamlit_image_select import image_select
from utils.parse import parseImage

def navigation_buttons(disable_navigation_dict):
    col1, col2, col3, col4 = st.columns(4, border=True, gap="small", vertical_alignment="top")
    # disable_navigation_dict = {"HOME": False, "LOGIN": False, "FILES": True, "CHAT": True, "IMAGE": True}
    with col1: st.page_link(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app.py"), label="HOME", icon="🏠", disabled=disable_navigation_dict["HOME"])
    with col2: st.page_link(os.path.join("pages","1_Files.py"), label="FILES", icon="2️⃣", disabled=disable_navigation_dict["FILES"])
    with col3: st.page_link(os.path.join("pages","2_Chat.py"), label="CHAT", icon="3️⃣", disabled=disable_navigation_dict["CHAT"])
    with col4: st.page_link(os.path.join("pages","3_Image.py"), label="IMAGE", icon="4️⃣", disabled=disable_navigation_dict["IMAGE"])

def fileSelectorUI(path):
    valid_files = []
    for files in os.listdir(path):
        if files.endswith(".pdf"):
            valid_files.append(files)
    options = st.multiselect("PLEASE SELECT FILE/S TO PROCEED", set(valid_files), placeholder="Your files here!")
    st.session_state['files'] = [os.path.join(path, option) for option in options]

def imageSelectorUI(path):
    valid_files = []
    for files in os.listdir(path):
        if files.endswith(".jpg"):
            valid_files.append(os.path.join(path,files))
    if len(valid_files) > 0:
        img = image_select("", valid_files, index=0)
        return img, parseImage(img).tob64()