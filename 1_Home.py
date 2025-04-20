import os
import yaml
import streamlit as st
from utils.ui import navigation_buttons
from modules.simple_rag import RAGDescriptionChain
from modules.simple_rag import ImageDescriptionChain

from modules import misc_ollama as ollama
import shutil

st.title("GenomeConnect")
st.subheader("AI Powered NGS Querying")

models=["gemma3:4b"]

script_path = os.path.dirname(os.path.abspath(__file__))
env_yaml_path = os.path.join(script_path, "env.yaml")

data = yaml.safe_load(open('file.yaml'))

# CREATE VECTOR DB
pdf_output          = "/mnt/c/Users/bhage/Documents/code/RAG/output/pdf"
pdf_image_output    = "/mnt/c/Users/bhage/Documents/code/RAG/output/pdf/images"
persist_dir        = "/mnt/c/Users/bhage/Documents/code/RAG/output/chroma"

# Add this function to clear the directories
def clear_output_directories():
    pass

if __name__ == "__main__":
    navigation_buttons({"HOME": False, "LOGIN": False, "FILES": False, "CHAT": True, "IMAGE": False})

    st.warning('AI generated content!', icon="⚠️")

    if not 'files' in st.session_state: st.session_state['files'] = ''
    if not 'image' in st.session_state: st.session_state['image'] = ''
    if not 'rag' in st.session_state: st.session_state['rag'] = ''
    if "model" not in st.session_state: st.session_state["model"] = "gemma3:4b"
    
    col1, col2, col3 = st.columns(3, gap="small", vertical_alignment="bottom")
    with col1: 
        model = st.selectbox("Pick Model", models)
        if st.button("Download"):
            ollamaFunc = ollama.ollamaFunc(model=model, embedding_model="all-minilm")
            with st.spinner(f"Downloading model: {model}", show_time=True):
                ollamaFunc.pull_model()
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
   
    if prompt := st.chat_input(f"Ask {model} about your reports!"):

        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = "Oops! I am not able to answer this question. Please try again."
            with st.spinner(f"Thinking... ", show_time=True):
                if prompt and st.session_state['image']:
                    client = ImageDescriptionChain(model=st.session_state["model"], temperature=0)
                    response = client.query(prompt, st.session_state['image'])
                elif prompt and st.session_state['rag'] and not st.session_state['image']:
                    rag = st.session_state['rag']
                    retrieved_doc, metadata = rag.query_chromadb(prompt, n_results=2)
                    client = RAGDescriptionChain(
                        retrieved_doc=retrieved_doc,
                        metadata=metadata,
                        query_text=prompt,
                        llm_model=st.session_state["model"],
                    )
                    response = client.query_ollama()
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    col1, col2, col3 = st.columns(3, gap="small", vertical_alignment="top")
    with col1: 
        st.button("Clear Chat", on_click=lambda: st.session_state.pop("messages", None), type="secondary")
    with col2:
        if st.button("Clear Output Directories"):
            clear_output_directories()
            st.success("All output directories have been cleared!")