import os
import streamlit as st
from modules.misc_UI import navigation_buttons
from modules.misc_UI import fileSelectorUI
from modules.misc_embedding import embeddings

from modules.parse_pdf import ParsePDF
from modules.parse_html import ParseHtml
from modules.parse_txt import ParseTxt
from modules.misc_UI import navigation_buttons, imageSelectorUI

st.title("GenomeConnect")
st.subheader("AI Powered NGS Querying")

# CREATE VECTOR DB
pdf_output          = "/mnt/c/Users/bhage/Documents/code/RAG/output/pdf"
html_output         = "/mnt/c/Users/bhage/Documents/code/RAG/output/html"
pdf_image_output    = "/mnt/c/Users/bhage/Documents/code/RAG/output/pdf/images"
persist_dir        = "/mnt/c/Users/bhage/Documents/code/RAG/output/chroma"

if __name__ == "__main__":
    disable_navigation_dict = {"HOME": False, "LOGIN": True, "FILES": False, "CHAT": False, "IMAGES": False}
    navigation_buttons(disable_navigation_dict)

    # COLLECT IMAGES
    pdf_images = []
    img = ''
    if os.path.exists(pdf_image_output):
        pdf_images = [os.path.join(pdf_image_output, f) for f in os.listdir(pdf_image_output)]
    
    img = imageSelectorUI(pdf_image_output, )
    
    if st.button("Clear Image Selection"):
        st.session_state['image'] = ''
        img = ''
        rag = st.session_state['rag']
        st.switch_page("pages/CHAT.py")
    
    st.write("Selected Image: ", [img])

    if st.button("Chat with Image"):
        st.switch_page("pages/CHAT.py")