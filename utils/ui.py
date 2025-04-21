import os
import streamlit as st
# from modules.simple_rag import RAGDescriptionChain
# from modules.simple_rag import ImageDescriptionChain
# from modules.parse_image import parseImage
from streamlit_image_select import image_select

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
    try:
        for files in os.listdir(path):
            if files.endswith(".jpg"):
                valid_files.append(os.path.join(path,files))
    except:
        valid_files = path
    img = image_select("", valid_files, index=0)
    st.session_state['image'] = parseImage(img).tob64()
    return img


def chatUI(models, image='', response=''):
    
    if "model" not in st.session_state: st.session_state["model"] = "gemma3:4b"
    if "messages" not in st.session_state: st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
   
    if prompt := st.chat_input(f"Ask {st.session_state['model']} about your reports!"):
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            if not response:
                response = "Oops! I am not able to answer this question. Please try again."

            with st.spinner(f"Thinking... ", show_time=True):
                if image:
                    client          = ImageDescriptionChain(model=st.session_state["model"], temperature=0)
                    response        = st.write(client.query(prompt, image))
                else:
                    client      = RAGDescriptionChain(retrieved_doc='', metadata='', query_text=prompt, llm_model=st.session_state["model"])
                    response    = st.write(client.query_ollama())
                    
        st.session_state.messages.append({"role": "assistant", "content": response})