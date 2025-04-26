import os
import yaml
import ollama
import streamlit as st
from utils.ui import navigation_buttons
from utils.ui import fileSelectorUI
from utils.parse import PDFProcessor
from utils.graph_rag import create_embeddings, create_bm25_retriever

script_path = os.path.dirname(os.path.abspath(__file__))
env_yaml_path = os.path.join(os.path.dirname(script_path), "env.yaml")

data = yaml.safe_load(open(env_yaml_path))

MIAN_DIR         = data['MAIN']['PATH']

OLLAMA_URL         = data['OLLAMA']['URL']
OLLAMA_MODEL       = data['OLLAMA']['MODEL']
OLLAMA_EMBED_MODEL = data['OLLAMA']['EMBED_MODEL']

vectorDB_pdf_input          = os.path.join(MIAN_DIR,data['VectorDB']['pdf_input'])
vectorDB_pdf_output         = os.path.join(MIAN_DIR,data['VectorDB']['pdf_output'])
vectorDB_vector_persist_dir = os.path.join(MIAN_DIR,data['VectorDB']['vector_persist_dir'])


st.title("GenomeConnect")
st.subheader("AI Powered NGS Querying")

if __name__ == "__main__":
    navigation_buttons({"HOME": False, "FILES": False, "CHAT": True, "IMAGE": True})

    st.markdown("-------------------------")

    col1, col2, col3 = st.columns(3, gap="small", vertical_alignment="bottom")
    with col1:
        st.session_state["model"] = st.selectbox("LANGUAGE MODEL", OLLAMA_MODEL)
        if st.button("Download", key="llm"):
            with st.spinner(f"Downloading LLM: {st.session_state['model']}", show_time=True):
                ollama.pull(st.session_state["model"])
    with col2:
        st.session_state["embed_model"] = st.selectbox("EMBED MODEL", OLLAMA_EMBED_MODEL)
        if st.button("Download", key="embed"):
            with st.spinner(f"Downloading Embed Model: {st.session_state['embed_model']}", show_time=True):
                ollama.pull(st.session_state["embed_model"])

    st.markdown("-------------------------")

    fileSelectorUI(path=vectorDB_pdf_input)

    st.markdown("-------------------------")

    if st.session_state['files'] and st.button("SUBMIT"):
        with st.spinner(f"Parsing PDF: ", show_time=True):
            PDFProcessor_instance = PDFProcessor(split_dir=os.path.join(vectorDB_pdf_output,'splits'))
            st.session_state['content'] = PDFProcessor_instance.process_pdf_in_parallel(st.session_state['files'])
            images_dir = os.path.join(vectorDB_pdf_output, 'images')
            if len(os.listdir(images_dir)) > 0:
                st.session_state['image'] = images_dir
            with st.spinner(f"Creating vector DB: ", show_time=True):
                st.session_state['embeddings'] = create_embeddings(
                    text_contents=[content.text for content in st.session_state['content']], 
                    embedding_model=st.session_state["embed_model"], 
                    base_url=OLLAMA_URL
                    )
                with st.spinner(f"Creating Retriever: ", show_time=True):
                    st.session_state['retriever'] = create_bm25_retriever(
                        text_contents=[content.text for content in st.session_state['content']],
                    )
                    PDFProcessor_instance.clean()
        st.switch_page("pages/2_Chat.py")
    