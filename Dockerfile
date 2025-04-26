FROM python:3.9.21

RUN apt-get update -y \
    && apt-get install -y build-essential poppler-utils tesseract-ocr libgl1-mesa-glx && \
    curl -fsSL https://ollama.com/install.sh | sh && \
    apt-get clean

RUN pip install --upgrade pip
RUN pip install -U --no-cache-dir \
    langchain-unstructured langchain-community langchain langchain-ollama \
    ollama "unstructured[pdf]" llama-index chromadb hf_xet pandas PyPDF2 networkx
RUN pip install -U --no-cache-dir \
    rank-bm25 sentence-transformers torch faiss-cpu streamlit streamlit-image-select

RUN mkdir -p ~/.streamlit/ && \
    streamlit config show > config.toml && \
    sed -i 's/# runOnSave = false/runOnSave = true/' config.toml && \
    sed -i 's/# fileWatcherType = "auto"/fileWatcherType = "poll"/' config.toml && \
    grep -v "#" config.toml | grep -v ' ~/.streamlit/config.toml.' > ~/.streamlit/config.toml