# import os
# import streamlit as st
# from modules.misc_UI import navigation_buttons
# from modules.misc_UI import fileSelectorUI
# from modules.misc_embedding import embeddings

# from modules.parse_pdf import ParsePDF
# from modules.parse_html import ParseHtml
# from modules.parse_txt import ParseTxt

# st.title("GenomeConnect")
# st.subheader("AI Powered NGS Querying")

# path = "/mnt/c/Users/bhage/Documents/code/RAG/test_data"
# pdf_output  = "/mnt/c/Users/bhage/Documents/code/RAG/output/pdf"
# html_output = "/mnt/c/Users/bhage/Documents/code/RAG/output/html"
# persist_dir = "/mnt/c/Users/bhage/Documents/code/RAG/output/chroma"
# files = []

# def parse_files(file_list, persist_dir):
#     pdf_list = []
#     html_list = []
#     pdf_loader_object, html_loader_object = '',''
#     for file in file_list:
#         if file.endswith("pdf"):
#             pdf_list.append(file)
#         elif file.endswith("html"):
#             html_list.append(file)
#     rag = embeddings(persist_dir=persist_dir)
#     if len(pdf_list) > 0:
#         pdf_parser = ParsePDF(path=pdf_list, output=pdf_output)
#         pdf_loader_object = pdf_parser.UnstructuredPDFLoader()
#         data = ParseTxt(loader_obj_dict=pdf_loader_object)
#         data_dict = data.ingestFormatConversion()
#         for id, content in data_dict.items():
#             rag.add_documents(content, id)
#     if len(html_list) > 0:
#         html_parser = ParseHtml(path=html_list, output=html_output)
#         html_loader_object = html_parser.UnstructuredHtmlLoader()
#         data = ParseTxt(loader_obj_dict=html_loader_object)
#         data_dict = data.ingestFormatConversion()
#         for id, content in data_dict.items():
#             rag.add_documents(content, id)
#     st.session_state['rag'] = rag

# if __name__ == "__main__":
#     disable_navigation_dict = {"HOME": False, "LOGIN": False, "FILES": True, "CHAT": True, "IMAGES": True}
#     navigation_buttons(disable_navigation_dict)

#     fileSelectorUI(path=path)

#     if st.session_state['files'] and st.button("SUBMIT"):
#         with st.spinner(f"Parsing PDF: ", show_time=True):
#             with st.spinner(f"Creating vector DB: ", show_time=True):
#                 parse_files(st.session_state['files'], persist_dir)
#         st.switch_page("pages/CHAT.py")

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
OLLAMA_MODEL       = data['OLLAMA']['MODEL']# ["gemma3:4b", "deepseek-r1:7b"]
OLLAMA_EMBED_MODEL = data['OLLAMA']['EMBED_MODEL']# ["nomic-embed-text", "all-minilm"]

vectorDB_pdf_input          = os.path.join(MIAN_DIR,data['VectorDB']['pdf_input'])# "input"
vectorDB_pdf_output         = os.path.join(MIAN_DIR,data['VectorDB']['pdf_output'])# "pdf"
vectorDB_vector_persist_dir = os.path.join(MIAN_DIR,data['VectorDB']['vector_persist_dir'])# "vector_db"


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
                # parse_files(st.session_state['files'], persist_dir)
        st.switch_page("pages/2_Chat.py")
    