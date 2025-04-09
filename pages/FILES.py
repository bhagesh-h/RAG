import os
import streamlit as st
from modules.misc_UI import navigation_buttons
from modules.misc_UI import fileSelectorUI
from modules.misc_embedding import embeddings

from modules.parse_pdf import ParsePDF
from modules.parse_html import ParseHtml
from modules.parse_txt import ParseTxt

st.title("GenomeConnect")
st.subheader("AI Powered NGS Querying")

path = "/mnt/c/Users/bhage/Documents/code/RAG/test_data"
pdf_output  = "/mnt/c/Users/bhage/Documents/code/RAG/output/pdf"
html_output = "/mnt/c/Users/bhage/Documents/code/RAG/output/html"
persist_dir = "/mnt/c/Users/bhage/Documents/code/RAG/output/chroma"
files = []

def parse_files(file_list, persist_dir):
    pdf_list = []
    html_list = []
    pdf_loader_object, html_loader_object = '',''
    for file in file_list:
        if file.endswith("pdf"):
            pdf_list.append(file)
        elif file.endswith("html"):
            html_list.append(file)
    rag = embeddings(persist_dir=persist_dir)
    if len(pdf_list) > 0:
        pdf_parser = ParsePDF(path=pdf_list, output=pdf_output)
        pdf_loader_object = pdf_parser.UnstructuredPDFLoader()
        data = ParseTxt(loader_obj_dict=pdf_loader_object)
        data_dict = data.ingestFormatConversion()
        for id, content in data_dict.items():
            rag.add_documents(content, id)
    if len(html_list) > 0:
        html_parser = ParseHtml(path=html_list, output=html_output)
        html_loader_object = html_parser.UnstructuredHtmlLoader()
        data = ParseTxt(loader_obj_dict=html_loader_object)
        data_dict = data.ingestFormatConversion()
        for id, content in data_dict.items():
            rag.add_documents(content, id)
    st.session_state['rag'] = rag

if __name__ == "__main__":
    disable_navigation_dict = {"HOME": False, "LOGIN": False, "FILES": True, "CHAT": True, "IMAGES": False}
    navigation_buttons(disable_navigation_dict)

    fileSelectorUI(path=path)

    if st.session_state['files'] and st.button("SUBMIT"):
        with st.spinner(f"Parsing PDF: ", show_time=True):
            with st.spinner(f"Creating vector DB: ", show_time=True):
                parse_files(st.session_state['files'], persist_dir)
        st.switch_page("pages/CHAT.py")