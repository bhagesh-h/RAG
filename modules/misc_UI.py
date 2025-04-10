import os
import streamlit as st
from modules import misc_ollama as ollama
from modules.simple_rag import RAGDescriptionChain
from modules.simple_rag import ImageDescriptionChain
from modules.parse_image import parseImage

def navigation_buttons(disable_navigation_dict):
    col1, col2, col3, col4, col5 = st.columns(5, border=True, gap="small", vertical_alignment="top")
    # disable_navigation_dict = {"HOME": False, "LOGIN": False, "FILES": True, "CHAT": True}
    with col1: st.page_link("HOME.py",          label="HOME",   icon="🏠", disabled=disable_navigation_dict["HOME"])
    with col2: st.page_link("pages/LOGIN.py", label="LOGIN",  icon="1️⃣", disabled=disable_navigation_dict["LOGIN"])
    with col3: st.page_link("pages/FILES.py", label="FILES",  icon="2️⃣", disabled=disable_navigation_dict["FILES"])
    with col4: st.page_link("pages/CHAT.py",  label="CHAT",   icon="3️⃣", disabled=disable_navigation_dict["CHAT"])
    with col5: st.page_link("pages/IMAGES.py",  label="IMAGES",   icon="4️⃣", disabled=disable_navigation_dict["IMAGES"])


def fileSelectorUI(path=os.getcwd()):
    valid_files = []
    for files in os.listdir(path):
        if files.endswith(".pdf") or files.endswith(".html"):
            valid_files.append(os.path.join(path, files))
    options = st.multiselect(
        "How would you like to be contacted?",
        set(valid_files),
        placeholder="Select a file",
    )
    st.session_state['files'] = options

def imageSelectorUI(path=''):
    from streamlit_image_select import image_select
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
    # st.warning('AI generated content!', icon="⚠️")

    # col1, col2, col3 = st.columns(3, gap="small", vertical_alignment="top")
    # with col1: 
    #     model = st.selectbox("Pick Model", models)
    
    # ollamaFunc = ollama.ollamaFunc(model=model, embedding_model="all-minilm")
    
    # with st.spinner(f"Downloading model: {model}", show_time=True):
    #    ollamaFunc.pull_model()
    
    if "model" not in st.session_state: st.session_state["model"] = "gemma3:4b"
    if "messages" not in st.session_state: st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
   
    if prompt := st.chat_input(f"Ask {st.session_state["model"]} about your reports!"):
        
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