import os
import yaml
import shutil
import streamlit as st
from utils.ui import navigation_buttons
from utils.graph_rag import process_text_and_retrieve, generate_answer

st.title("GenomeConnect")
st.subheader("AI Powered NGS Querying")

script_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_yaml_path = os.path.join(script_path, "env.yaml")

data = yaml.safe_load(open(env_yaml_path))

MIAN_DIR         = data['MAIN']['PATH']

OLLAMA_URL         = data['OLLAMA']['URL']
OLLAMA_MODEL       = data['OLLAMA']['MODEL']
OLLAMA_EMBED_MODEL = data['OLLAMA']['EMBED_MODEL']

vectorDB_pdf_input          = os.path.join(MIAN_DIR,data['VectorDB']['pdf_input'])
vectorDB_pdf_output         = os.path.join(MIAN_DIR,data['VectorDB']['pdf_output'])
vectorDB_vector_persist_dir = os.path.join(MIAN_DIR,data['VectorDB']['vector_persist_dir'])

os.makedirs(vectorDB_pdf_output, exist_ok=True)
os.makedirs(vectorDB_vector_persist_dir, exist_ok=True)

def clear_output_directories():
    directories = [os.path.join(vectorDB_pdf_output, 'images'), vectorDB_vector_persist_dir]
    for directory in directories:
        if os.path.exists(directory):
            for file in os.listdir(directory):
                file_path = os.path.join(directory, file)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    st.error(f"Failed to delete {file_path}: {e}")

if __name__ == "__main__":
    navigation_buttons({"HOME": False, "LOGIN": False, "FILES": False, "CHAT": True, "IMAGE": False})

    st.warning('AI generated content!', icon="⚠️")
    
    st.markdown("-------------------------")

    col1, col2, col3 = st.columns(3, gap="small", vertical_alignment="top")
    with col1: 
        on = st.toggle("Query Report")

    if not 'image' in st.session_state: st.session_state['image'] = None
    if not "model" in st.session_state: st.session_state['model'] = "gemma3:4b"
    if not "embed_model" in st.session_state: st.session_state["embed_model"] = "nomic-embed-text"
    if not "files" in st.session_state: st.session_state['files'] = None
    if not "content" in st.session_state: st.session_state['content'] = None
    if not "embeddings" in st.session_state: st.session_state['embeddings'] = None
    if not "retriever" in st.session_state: st.session_state['retriever'] = None
    
    

    if "messages" not in st.session_state: st.session_state["messages"] = []
    
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if prompt := st.chat_input(f"Ask {st.session_state['model']} about your reports!"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            response = "Oops! I am not able to answer this question. Please try again."
            if prompt:
                relevant_texts = None
                if on:
                    if st.session_state['retriever'] and st.session_state['embeddings']:
                        with st.spinner(f"Sorting information...", show_time=True):
                            relevant_texts = process_text_and_retrieve(
                                embeddings = st.session_state['embeddings'],
                                retriever = st.session_state['retriever'],
                                query = prompt, 
                                num_results=3)
                with st.spinner(f"Thinking...", show_time=True):
                    response = generate_answer(
                        query=prompt,
                        retrieved_docs=relevant_texts, 
                        model=st.session_state['model'], 
                        base_url=OLLAMA_URL,
                        temperature=0.7
                        )
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        

    col1, col2, col3 = st.columns(3, gap="small", vertical_alignment="top")
    with col1: 
        st.button("Clear Chat", on_click=lambda: st.session_state.pop("messages", None), type="secondary")
    with col2:
        if st.button("Clear Metadata"):
            clear_output_directories()
            st.success("All output directories have been cleared!")
    with col3:
        if st.button("Image Chat"):
            st.switch_page("pages/3_Image.py")
