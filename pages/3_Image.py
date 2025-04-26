import os
import yaml
import streamlit as st
from utils.ui import navigation_buttons, imageSelectorUI
from utils.graph_rag import process_text_and_retrieve, generate_answer
from utils.image_rag import ImageDescriptionChain
from utils.parse import parseImage

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

if __name__ == "__main__":
    navigation_buttons({"HOME": False, "LOGIN": False, "FILES": False, "CHAT": False, "IMAGE": True})

    st.warning('AI generated content!', icon="⚠️")
    
    st.markdown("-------------------------")

    col1, col2, col3 = st.columns(3, gap="small", vertical_alignment="top")
    with col1: 
        on = st.toggle("Query Image")

    if not 'image' in st.session_state: st.session_state['image'] = os.path.join(vectorDB_pdf_output, 'images')
    if not "model" in st.session_state: st.session_state['model'] = "gemma3:4b"
    if not "embed_model" in st.session_state: st.session_state["embed_model"] = "nomic-embed-text"
    if not "files" in st.session_state: st.session_state['files'] = None
    if not "content" in st.session_state: st.session_state['content'] = None
    if not "embeddings" in st.session_state: st.session_state['embeddings'] = None
    if not "retriever" in st.session_state: st.session_state['retriever'] = None
    
    if st.session_state['image']:
        img, b64_encoding = imageSelectorUI(st.session_state['image'])
        st.write("Selected Image: ", [img])


    if "messages" not in st.session_state: st.session_state["messages"] = []
    
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if prompt := st.chat_input(f"Ask {st.session_state['model']} about your images!"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            response = "Oops! I am not able to answer this question. Please try again."
            if prompt:
                relevant_texts = None
                if on:
                    if img:
                        with st.spinner(f"Analysing image...", show_time=True):
                            client = ImageDescriptionChain(model=st.session_state["model"], temperature=0)
                            response = client.query(prompt, b64_encoding)
                else:
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
