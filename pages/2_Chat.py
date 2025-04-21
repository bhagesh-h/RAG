import os
import yaml
import ollama
import streamlit as st
from utils.ui import navigation_buttons

# from modules.simple_rag import RAGDescriptionChain
# from modules.simple_rag import ImageDescriptionChain

# from modules import misc_ollama as ollama
import shutil

st.title("GenomeConnect")
st.subheader("AI Powered NGS Querying")

models=["gemma3:4b"]

script_path = os.path.dirname(os.path.abspath(__file__))
env_yaml_path = os.path.join(script_path, "env.yaml")

data = yaml.safe_load(open(env_yaml_path))

MIAN_DIR         = data['MAIN']['PATH']# "/mnt/c/Users/bhage/Documents/code/RAG"

OLLAMA_URL         = os.path.join(MIAN_DIR,data['OLLAMA']['URL'])
OLLAMA_MODEL       = data['OLLAMA']['MODEL']# ["gemma3:4b", "deepseek-r1:7b"]
OLLAMA_EMBED_MODEL = data['OLLAMA']['EMBED_MODEL']# ["nomic-embed-text", "all-minilm"]

vectorDB_pdf_input          = os.path.join(MIAN_DIR,data['VectorDB']['pdf_input'])# "input"
vectorDB_pdf_output         = os.path.join(MIAN_DIR,data['VectorDB']['pdf_output'])# "pdf"
vectorDB_vector_persist_dir = os.path.join(MIAN_DIR,data['VectorDB']['vector_persist_dir'])# "vector_db"

if __name__ == "__main__":
    navigation_buttons({"HOME": False, "LOGIN": False, "FILES": False, "CHAT": True, "IMAGE": False})

    st.warning('AI generated content!', icon="⚠️")

    if not 'files' in st.session_state: st.session_state['files'] = ''
    if not 'image' in st.session_state: st.session_state['image'] = ''
    if not 'rag' in st.session_state: st.session_state['rag'] = ''
    if not "model" in st.session_state: st.session_state["model"] = "gemma3:4b"
    if not "embed_model" in st.session_state: st.session_state["embed_model"] = "nomic-embed-text"
    
    col1, col2, col3 = st.columns(3, gap="small", vertical_alignment="bottom")
    with col1: 
        st.session_state["model"] = st.selectbox("Language Model", OLLAMA_MODEL)
        if st.button("Download Model"):
            with st.spinner(f"Downloading model: {st.session_state['model']}", show_time=True):
                ollama.pull(st.session_state["model"])
    with col2: 
        st.session_state["embed_model"] = st.selectbox("Embed Model", OLLAMA_EMBED_MODEL)
        if st.button("Download Embed Model"):
            with st.spinner(f"Downloading model: {st.session_state['embed_model']}", show_time=True):
                ollama.pull(st.session_state["embed_model"])
    
#     if "messages" not in st.session_state:
#         st.session_state.messages = []
    
#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])
   
#     if prompt := st.chat_input(f"Ask {model} about your reports!"):

#         st.session_state.messages.append({"role": "user", "content": prompt})
        
#         with st.chat_message("user"):
#             st.markdown(prompt)

#         with st.chat_message("assistant"):
#             response = "Oops! I am not able to answer this question. Please try again."
#             with st.spinner(f"Thinking... ", show_time=True):
#                 if prompt and st.session_state['image']:
#                     client = ImageDescriptionChain(model=st.session_state["model"], temperature=0)
#                     response = client.query(prompt, st.session_state['image'])
#                 elif prompt and st.session_state['rag'] and not st.session_state['image']:
#                     rag = st.session_state['rag']
#                     retrieved_doc, metadata = rag.query_chromadb(prompt, n_results=2)
#                     client = RAGDescriptionChain(
#                         retrieved_doc=retrieved_doc,
#                         metadata=metadata,
#                         query_text=prompt,
#                         llm_model=st.session_state["model"],
#                     )
#                     response = client.query_ollama()
#             st.markdown(response)
#         st.session_state.messages.append({"role": "assistant", "content": response})
    
#     col1, col2, col3 = st.columns(3, gap="small", vertical_alignment="top")
#     with col1: 
#         st.button("Clear Chat", on_click=lambda: st.session_state.pop("messages", None), type="secondary")
#     with col2:
#         if st.button("Clear Output Directories"):
#             clear_output_directories()
#             st.success("All output directories have been cleared!")

    st.title("GenomeConnect")
    st.subheader("AI Powered NGS Querying")

    st.markdown("-------------------------")
    st.markdown("Welcome to **GenomeConnect** — your personalized companion for understanding genomic reports.")
    st.markdown("Powered by advanced **Retrieval-Augmented Generation** (RAG) technology, **GenomeConnect** enables users to ask questions directly about their genetic data and receive accurate, context-aware answers.") 
    st.markdown("Whether you're seeking clarity on variants, insights into your health, or support interpreting complex findings, **GenomeConnect** is here to bridge the gap between raw data and meaningful understanding.")
    st.markdown("-------------------------")
    
    if st.button("Proceed To Login"):
        st.switch_page("pages/LOGIN.py")